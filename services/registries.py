from http import HTTPStatus
import datetime as dt

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from django.db.models import BaseManager

from . import consts
from apps.api import models

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
    ids_to_query = {
        'invoice_id': dict(obj=None, model=models.Invoice, attr_with_user='self'),
        'responsable_id': dict(obj=None, model=models.Responsable, attr_with_user='card'),
    }

    for id_to_query, params in ids_to_query.items():
        if id_to_query not in data:
            continue

        obj = params['model'].objects.filter(id=data[id_to_query]).first()
        attr_with_user = params['attr_with_user']

        if not obj:
            return HTTPStatus.BAD_REQUEST, f'nenhum id válido encontrado para {id_to_query}', None

        if attr_with_user:
            obj_with_user = obj if attr_with_user == 'self' else getattr(obj, attr_with_user)
            if obj_with_user.user != user:
                return HTTPStatus.FORBIDDEN, f'o ID fornecido em {id_to_query} não é vinculado ao usuário atual', None

    try:
        reg = models.Registry(
            title=data['title'],
            value=data['value'],
            status=data['status'][0],
            occurrance=data['occurrance'],
            description=data.get('description'),
            date_ref=f'{data['ref_year']}-{str(data['ref_month']).zfill(2)}-01',
            type_in=data['type_in'],
            user=user,
            invoice=ids_to_query['invoice_id']['obj'],
            responsable=ids_to_query['responsable_id']['obj'],
        )
    except KeyError as e:
        return HTTPStatus.BAD_REQUEST, f'missing required param {e}', None

    reg.save()
    
    return HTTPStatus.OK, '', models.Registry.objects.get(id=reg.id)