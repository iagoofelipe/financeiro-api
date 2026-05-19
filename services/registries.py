from . import consts
from apps.api import models
import http
from http import HTTPStatus

def get_by_filters(user, **filters):
    """ consulta os registros aplicando os filtros fornecidos. A filtragem segue o padrão de `key__condition` do django """
    # adicionando filtros
    filters = { k: filters[k] for k in set(filters) & consts.REGISTRIES_FILTERS }

    if 'status' in filters:
        filters['status'] = filters['status'][0] # necessário pois a base armazena o STATUS apenas como a primeira letra

    return models.Registry.objects.filter(user=user, **filters).all()

def get_by_id(user, regid:int) -> tuple[HTTPStatus, str, models.Registry | None]:
    reg = models.Registry.objects.filter(id=regid).first()
    if not reg:
        return HTTPStatus.NOT_FOUND, 'nenhum dado encontrado para o ID fornecido', None
    
    if reg.user != user:
        return HTTPStatus.METHOD_NOT_ALLOWED, 'permissão de acesso negada', None
    
    return HTTPStatus.OK, '', reg

def create(user, **data) -> tuple[HTTPStatus, str, models.Registry | None]:
    """ cria um novo registro, retorna statuscode, error, object """
    invoice = None
    responsable = None

    if 'invoice_id' in data:
        invoice = models.Invoice.objects.filter(id=data['invoice_id']).first()
        
        if not invoice:
            return HTTPStatus.BAD_REQUEST, 'nenhuma fatura válida encontrada para o ID fornecido', None

        elif invoice.card.user != user:
            return HTTPStatus.FORBIDDEN, '', None
    
    if 'responsable_id' in data:
        responsable = models.Responsable.objects.filter(id=data['responsable_id']).first()
        
        if not responsable:
            return HTTPStatus.BAD_REQUEST, 'nenhum responsável encontrado para o ID fornecido', None
        
        elif responsable.user != user:
            return HTTPStatus.FORBIDDEN, '', None

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
            invoice=invoice,
            responsable=responsable,
        )
    except KeyError as e:
        return http.HTTPStatus.BAD_REQUEST, f'missing required param {e}', None

    reg.save()
    
    return HTTPStatus.OK, '', models.Registry.objects.get(id=reg.id)