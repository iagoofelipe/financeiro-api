from http import HTTPStatus
import datetime as dt
from dateutil.relativedelta import relativedelta

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from django.db.models import BaseManager

from . import consts
from apps.api import models
from . import invoices

def get_by_filters(user, **filters) -> tuple[HTTPStatus, str, "BaseManager"[models.Registry] | None]:
    """ consulta os registros aplicando os filtros fornecidos. A filtragem segue o padrão de `key__condition` do django """
    # adicionando filtros
    invalid_filters = set(filters) - consts.REGISTRY_FILTERS
    if invalid_filters:
        return  HTTPStatus.BAD_REQUEST, f'parâmetros {invalid_filters} inválidos', None

    filters = { k: filters[k] for k in set(filters) & consts.REGISTRY_FILTERS }

    occurrance_init = ''
    occurrance_end = ''
    if 'occurrance_init' in filters:
        occurrance_init = filters.pop('occurrance_init')

    if 'ocurrance_end' in filters:
        occurrance_end = filters.pop('occurrance_end')
    
    if occurrance_init or occurrance_end:
        filters['occurrance__range'] = (occurrance_init, occurrance_end)

    regs = models.Registry.objects \
        .filter(user=user, **filters) \
        .order_by('-occurrance') \
        .all()

    return HTTPStatus.OK, '', regs

def get_by_id(user, regid:int) -> tuple[HTTPStatus, str, models.Registry | None]:
    reg = models.Registry.objects.filter(id=regid).first()
    if not reg:
        return HTTPStatus.NOT_FOUND, 'nenhum dado encontrado para o ID fornecido', None
    
    if reg.user != user:
        return HTTPStatus.METHOD_NOT_ALLOWED, 'permissão de acesso negada', None
    
    return HTTPStatus.OK, '', reg

def create(user, **data) -> tuple[HTTPStatus, str, models.Registry | None]:
    """ cria um novo registro, retorna statuscode, error, object """

    if 'installment_current' in data and not 'installment_total' in data:
        return HTTPStatus.BAD_REQUEST, f'installment_total é necessário para installment_current', None

    # validando dados
    try:
        occurrance = dt.datetime.strptime(data['occurrance'], '%d/%m/%Y %H:%M')
    except ValueError:
        return HTTPStatus.BAD_REQUEST, f'occurrance deve seguir o formato dd/mm/aaaa hh:mm', None

    # consultando dependências
    ids_to_query = {
        'responsable_id': { 'model': models.Responsable, 'attr_with_user': 'self', 'name': 'responsable' },
        'card_id': { 'model': models.Card, 'attr_with_user': 'self', 'name': 'card' },
    }

    for id_to_query, params in ids_to_query.items():
        if id_to_query not in data or data[id_to_query] in ('', None):
            continue

        obj = params['model'].objects.filter(id=data[id_to_query]).first()
        data[params['name']] = obj
        attr_with_user = params['attr_with_user']

        if not obj:
            return HTTPStatus.BAD_REQUEST, f'nenhum id válido encontrado para {id_to_query}', None

        if attr_with_user:
            obj_with_user = obj if attr_with_user == 'self' else getattr(obj, attr_with_user)
            if obj_with_user.user != user:
                return HTTPStatus.FORBIDDEN, f'o ID fornecido em {id_to_query} não é vinculado ao usuário atual', None

    try:
        date_ref = dt.date.strptime(data['date_ref'], '%Y-%m')
        invoice = invoices.get_or_create(data['card'], date_ref) if 'card' in data else None
        value = data['value']
        done = data.get('done', False)
        responsable = data.get('responsable')
        
        reg = models.Registry(
            title=data['title'],
            value=value,
            occurrance=occurrance,
            description=data.get('description'),
            date_ref=date_ref,
            type_in=data['type_in'],
            done=done,
            accounted=data.get('accounted', False) if not done else False,
            user=user,
            invoice=invoice,
            responsable=responsable,
        )
    except KeyError as e:
        return HTTPStatus.BAD_REQUEST, f'missing required param {e}', None
    except ValueError:
        return HTTPStatus.BAD_REQUEST, f'o parâmetro date-ref deve seguir o formato AAAA-MM', None
   
    reg.save()
    regid = reg.id

    # criando grupo de parcelas
    if data.get('installment_total', 0) > 1:
        index = data.get('installment_current', 1) - 1
        total = data['installment_total']

        if index >= total:
            return HTTPStatus.BAD_REQUEST, f'a parcela atual deve ser menor ou igual ao total de parcelas', None
        
        total_value = value * total
        paid_value = value * (index + reg.done)
        installment = models.Installment(
            user=user,
            num_items=total,
            value=total_value,
            paid=paid_value,
            pending=total_value - paid_value,
        )
        installment.save()

        type_in = data['type_in']

        for i in range(index, total):
            if i != index: # criando um novo registro caso não seja o primeiro index
                date_ref += relativedelta(months=1)
                
                if type_in: # caso seja uma saída, a data de ocorrência é fixa
                    occurrance += relativedelta(months=1)

                if invoice:
                    invoice = invoices.get_or_create(invoice.card, date_ref)
                
                reg = models.Registry(
                    title=data['title'],
                    value=value,
                    accounted=not type_in,
                    occurrance=occurrance,
                    description=data.get('description'),
                    date_ref=date_ref,
                    type_in=type_in,
                    user=user,
                    invoice=invoice,
                    responsable=responsable,
                )
                reg.save()

            installment_item = models.InstallmentItem(
                index=i,
                installment=installment,
                registry=reg
            )
            installment_item.save()

    return HTTPStatus.OK, '', models.Registry.objects.get(id=regid)


def delete(user, id, all_parents=True) -> tuple[HTTPStatus, str]:
    reg = models.Registry.objects.filter(id=id).first()

    if not reg:
        return HTTPStatus.NOT_FOUND, 'nenhum valor encontrado para o id fornecido'
    
    if reg.user != user:
        return HTTPStatus.FORBIDDEN, 'permissão de acesso negada'
    
    if all_parents and (installment_item := reg.installment_item.first()):
        # captura o id dos registros relacionados ao Installment do registro pesquisado, através de InstallmentItem
        installment = installment_item.installment
        reg_ids_to_delete = installment.items.values_list('registry', flat=True)
        
        models.Registry.objects.filter(id__in=reg_ids_to_delete).delete()
        installment.delete()
    
    else:
        reg.delete()

    return HTTPStatus.OK, ''


def update(user, **data) -> tuple[HTTPStatus, str, models.Registry | None]:
    if 'id' not in data:
        return HTTPStatus.BAD_REQUEST, 'o parâmetro id é obrigatório', None

    base_manager_reg = models.Registry.objects.filter(id=data.pop('id'))
    reg = base_manager_reg.first()

    if not reg:
        return HTTPStatus.NOT_FOUND, 'nenhum valor encontrado para o id fornecido', None
    
    if reg.user != user:
        return HTTPStatus.FORBIDDEN, 'permissão de acesso negada', None
    
    try:
        if 'occurrance' in data:
            data['occurrance'] = dt.datetime.strptime(data['occurrance'], '%d/%m/%Y %H:%M')
        
        base_manager_reg.update(**data)

    except ValueError:
        return HTTPStatus.BAD_REQUEST, 'o parâmetro occurrance deve seguir o formato DD/MM/AAAA HH:MM', None

    except Exception as e:
        return HTTPStatus.BAD_REQUEST, e.__str__(), None

    return HTTPStatus.OK, '', base_manager_reg.first()