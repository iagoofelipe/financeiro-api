from http import HTTPStatus
import datetime as dt
from dateutil.relativedelta import relativedelta

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from django.db.models import BaseManager

from . import consts
from apps.api import models
from . import invoice
from . import installment


# campos que necessitam da verificação de pertencimento do usuário
# field: {model: source_model, attr_with_user: field_to_validate (default self), name: destiny_name}
REGISTRY_IS_OWNER_VALIDATION = {
    'responsable_id': { 'model': models.Responsable, 'name': 'responsable' },
    'card_id': { 'model': models.Card, 'name': 'card' },
}
SET_REGISTRY_IS_OWNER_VALIDATION = set(REGISTRY_IS_OWNER_VALIDATION)


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
    
    if 'card_id' in filters:
        v = filters.pop('card_id')
        if v:
            filters['invoice__card__id'] = v

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

def validations(user, data:dict, required_fields:set=None, validate_installment=False, remove_if_empty=True) -> tuple[HTTPStatus, str] | None:
    set_data = set(data)
    data['user'] = user

    # substituindo string vazias por None
    for k in filter(lambda k: data[k] == '', data):
        data[k] = None

    # verificando campos obrigatórios
    if required_fields and isinstance(required_fields, set):
        missing_fields = required_fields - set_data
        if missing_fields:
            return HTTPStatus.BAD_REQUEST, f'campos obrigatórios ausentes {missing_fields}'

    if validate_installment:
        if 'installment_current' in data and not 'installment_total' in data:
            return HTTPStatus.BAD_REQUEST, f'installment_total é necessário para installment_current'
        
        data['installment_total'] = total = data.get('installment_total', 0)
        data['installment_index'] = index = data.pop('installment_current', 1) - 1

        if total > 1 and index >= total:
            return HTTPStatus.BAD_REQUEST, f'a parcela atual deve ser menor ou igual ao total de parcelas'
    
    # validando vínculo do usuário com os ids fornecidos
    for field in SET_REGISTRY_IS_OWNER_VALIDATION & set_data:
        if data[field] is None:
            if remove_if_empty:
                data.pop(field)
            continue

        # coletando informações do campo
        model = REGISTRY_IS_OWNER_VALIDATION[field]['model']
        attr_with_user = REGISTRY_IS_OWNER_VALIDATION[field].get('attr_with_user', 'self')
        name = REGISTRY_IS_OWNER_VALIDATION[field]['name']

        # coletando dados para validação
        obj = model.objects.filter(id=data.pop(field)).first()

        if not obj:
            return HTTPStatus.BAD_REQUEST, f'nenhum id válido encontrado para {field}'

        obj_with_user = obj if attr_with_user == 'self' else getattr(obj, attr_with_user)
        if obj_with_user.user != user:
            return HTTPStatus.FORBIDDEN, f'o ID fornecido em {field} não é vinculado ao usuário atual'
        
        data[name] = obj
    
    # tratando dados de entrada
    try:
        if 'occurrance' in data:
            data['occurrance'] = dt.datetime.strptime(data['occurrance'], '%d/%m/%Y %H:%M')
        
        if 'date_ref' in data:
            data['date_ref'] = dt.date.strptime(data['date_ref'], '%Y-%m')

    except ValueError as e:
        return HTTPStatus.BAD_REQUEST, e.__str__()
    
    if 'status' in data:
        data['done'] = False
        data['accounted'] = False
        status = data.pop('status')

        if status not in ('PENDING', 'ACCOUNTED', 'OK'):
            return HTTPStatus.BAD_REQUEST, 'o parâmetro status deve ser PENDING, ACCOUNTED ou OK'
        
        match status:
            # case 'PENDING':     done e accounted False
            case 'ACCOUNTED':   data['accounted'] = True
            case 'OK':          data['done'] = True

    # if 'category' in data:
    #     if data['category']:
    #         data['category'], created = models.Category.objects.get_or_create(title=data['category'], user=user)
        
    #     elif remove_if_empty:
    #         data.pop('category')

    if 'card' in data:
        data['invoice'] = invoice.get_or_create(data.pop('card'), data['date_ref'])
    elif 'card_id' in data and data['card_id'] is None:
        data['invoice'] = data.pop('card_id')


def create(user, **data) -> tuple[HTTPStatus, str, models.Registry | None]:
    """ cria um novo registro, retorna statuscode, error, object """

    validation_result = validations(user, data, {'title', 'value', 'occurrance', 'date_ref'}, validate_installment=True)

    # em caso de erro na validação
    if validation_result:
        return *validation_result, None
    
    # removendo dados adicionados na validação que não são passados para models.Registry
    installment_total = data.pop('installment_total')
    installment_index = data.pop('installment_index')

    reg = models.Registry(**data)
    reg.save()
    regid = reg.id

    # criando grupo de parcelas
    if installment_total > 1:
        total_value = data['value'] * installment_total
        paid_value = data['value'] * (installment_index + reg.done)

        installment = models.Installment(
            user=user,
            num_items=installment_total,
            value=total_value,
            paid=paid_value,
            pending=total_value - paid_value,
        )
        installment.save()

        for i in range(installment_index, installment_total):
            if i != installment_index: # criando um novo registro caso não seja o primeiro index
                data['date_ref'] += relativedelta(months=1)
                
                if reg.type_in: # caso seja uma saída, a data de ocorrência é fixa
                    data['occurrance'] += relativedelta(months=1)

                if 'invoice' in data:
                    data['invoice'] = invoice.get_or_create(data['invoice'].card, data['date_ref'])

                data['done'] = False
                data['accounted'] = not reg.type_in
                
                reg = models.Registry(**data)
                reg.save()

            models.InstallmentItem(index=i, installment=installment, registry=reg).save()

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
    validation_result = validations(user, data, {'id'}, remove_if_empty=False)

    if validation_result:
        return *validation_result, None

    base_manager_reg = models.Registry.objects.filter(id=data.pop('id'))
    reg = base_manager_reg.first()

    if not reg:
        return HTTPStatus.NOT_FOUND, 'nenhum valor encontrado para o id fornecido', None
    
    if reg.user != user:
        return HTTPStatus.FORBIDDEN, 'permissão de acesso negada', None
    
    try:
        base_manager_reg.update(**data)
    except Exception as e:
        return HTTPStatus.BAD_REQUEST, e.__str__(), None
    
    # atualizando parcelas, caso haja
    if installment_item := reg.installment_item.first():
        installment.update_values(installment_item.installment)

    return HTTPStatus.OK, '', reg

