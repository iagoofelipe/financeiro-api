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

    if 'status' in filters:
        filters['status'] = filters['status'][0] # necessário pois a base armazena o STATUS apenas como a primeira letra

    occurrance_init = ''
    occurrance_end = ''
    if 'occurrance_init' in filters:
        occurrance_init = filters.pop('occurrance_init')

    if 'ocurrance_end' in filters:
        occurrance_end = filters.pop('occurrance_end')
    
    if occurrance_init or occurrance_end:
        filters['occurrance__range'] = (occurrance_init, occurrance_end)

    if 'date_ref' not in filters or not filters['date_ref']:
        filters['date_ref'] = dt.date.today().strftime('%Y-%m-01')

    regs = models.Registry.objects \
        .filter(user=user, **filters) \
        .order_by('-occurrance') \
        .all()

    return HTTPStatus.OK, '', regs

def get_date_references(user):
    date_refs = models.Registry.objects.filter(user=user).values_list('date_ref', flat=True).distinct().order_by()
    return [ {'value': v.strftime('%Y-%m-%d'), 'formatted': v.strftime('%b %y')} for v in date_refs ]

def get_default_date_reference(user) -> dt.date | None:
    current = models.Registry.objects.filter(user=user, date_ref=dt.date.today().strftime('%Y-%m-01')).first()
    if current:
        return current.date_ref
    
    return models.Registry.objects.filter(user=user).values_list('date_ref', flat=True).distinct().order_by().first()

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

    ids_to_query = {
        'responsable_id': dict(obj=None, model=models.Responsable, attr_with_user='self'),
    }

    if 'card_id' in data and data['card_id']:
        ids_to_query['card_id'] = dict(obj=None, model=models.Card, attr_with_user='self')

    for id_to_query, params in ids_to_query.items():
        if id_to_query not in data:
            continue

        obj = params['model'].objects.filter(id=data[id_to_query]).first()
        params['obj'] = obj
        attr_with_user = params['attr_with_user']

        if not obj:
            return HTTPStatus.BAD_REQUEST, f'nenhum id válido encontrado para {id_to_query}', None

        if attr_with_user:
            obj_with_user = obj if attr_with_user == 'self' else getattr(obj, attr_with_user)
            if obj_with_user.user != user:
                return HTTPStatus.FORBIDDEN, f'o ID fornecido em {id_to_query} não é vinculado ao usuário atual', None
        
    date_ref = dt.date(data['ref_year'], data['ref_month'], 1)
    invoice = invoices.get_or_create(ids_to_query['card_id']['obj'], date_ref) if 'card_id' in data else None
    # print(invoice.id)
    # return HTTPStatus.FORBIDDEN, f'teste', None
    try:
        reg = models.Registry(
            title=data['title'],
            value=data['value'],
            status=data['status'][0],
            occurrance=data['occurrance'],
            description=data.get('description'),
            date_ref=date_ref,
            type_in=data['type_in'],
            user=user,
            invoice=invoice,
            responsable=ids_to_query['responsable_id']['obj'],
        )
    except KeyError as e:
        return HTTPStatus.BAD_REQUEST, f'missing required param {e}', None
   
    reg.save()
    regid = reg.id

    # criando grupo de parcelas
    if 'installment_total' in data:
        index = data.get('installment_current', 1) - 1
        total = data['installment_total']

        if index >= total:
            return HTTPStatus.BAD_REQUEST, f'a parcela atual deve ser menor ou igual ao total de parcelas', None
        
        installment = models.Installment(
            num_items=total,
            value=data['value'] * total
        )
        installment.save()

        occurrance = dt.datetime.strptime(data['occurrance'], '%Y-%m-%d %H:%M')
        type_in = data['type_in']

        for i in range(index, total):
            if i != index: # criando um novo registro caso não seja o primeiro index
                date_ref += relativedelta(months=1)
                if type_in:
                    occurrance += relativedelta(months=1)

                elif invoice:
                    invoice = invoices.get_or_create(invoice.card, date_ref)
                
                reg = models.Registry(
                    title=data['title'],
                    value=data['value'],
                    status='A',
                    occurrance=occurrance,
                    description=data.get('description'),
                    date_ref=date_ref,
                    type_in=type_in,
                    user=user,
                    invoice=invoice,
                    responsable=ids_to_query['responsable_id']['obj'],
                )
                reg.save()

            installment_item = models.InstallmentItem(
                index=i,
                installment=installment,
                registry=reg
            )
            installment_item.save()


    return HTTPStatus.OK, '', models.Registry.objects.get(id=regid)