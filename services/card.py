from apps.api import models
from http import HTTPStatus

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from django.db.models import BaseManager

from . import consts

def get_by_filters(user, **filters) -> tuple[HTTPStatus, str, "BaseManager"[models.Card] | None]:
    """ consulta os cartões aplicando os filtros fornecidos. A filtragem segue o padrão de `key__condition` do django """
    
    # adicionando filtros
    invalid_filters = set(filters) - consts.CARD_FILTERS
    if invalid_filters:
        return  HTTPStatus.BAD_REQUEST, f'parâmetros {invalid_filters} inválidos', None

    filters = { k: filters[k] for k in set(filters) & consts.CARD_FILTERS }

    return HTTPStatus.OK, '', models.Card.objects.filter(user=user, **filters).all()

def get_by_id(user, cardid:int) -> tuple[HTTPStatus, str, models.Card | None]:
    obj = models.Card.objects.filter(id=cardid).first()
    if not obj:
        return HTTPStatus.NOT_FOUND, 'nenhum dado encontrado para o ID fornecido', None
    
    if obj.user != user:
        return HTTPStatus.METHOD_NOT_ALLOWED, 'permissão de acesso negada', None
    
    return HTTPStatus.OK, '', obj

def create(user, **data) -> tuple[HTTPStatus, str, models.Card | None]:
    try:
        card = models.Card(
            name=data['name'],
            closing_day=data['closing_day'],
            due_day=data['due_day'],
            closing_previous_month=data.get('closing_previous_month'),
            limit=data['limit'],
            user=user,
        )
    except KeyError as e:
        return HTTPStatus.BAD_REQUEST, f'missing required param {e}', None

    card.save()
    return HTTPStatus.OK, '', card