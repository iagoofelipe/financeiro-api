from http import HTTPStatus

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from django.db.models import BaseManager

from apps.api import models

def get_all(user) -> tuple[HTTPStatus, str, "BaseManager"[models.Card] | None]:
    """ consulta todos os cartões """
    return HTTPStatus.OK, '', user.card_set.all()

def get_by_id(user, cardid:int) -> tuple[HTTPStatus, str, models.Card | None]:
    obj = models.Card.objects.filter(id=cardid).first()
    if not obj:
        return HTTPStatus.NOT_FOUND, 'nenhum dado encontrado para o ID fornecido', None
    
    if obj.user != user:
        return HTTPStatus.FORBIDDEN, 'permissão de acesso negada', None
    
    return HTTPStatus.OK, '', obj

def create(user, **data) -> tuple[HTTPStatus, str, models.Card | None]:
    try:
        card = models.Card(
            name=data['name'],
            closing_day=data['closing_day'],
            due_day=data['due_day'],
            limit=data['limit'],
            user=user,
        )
        closing = data.get('closing_previous_month')
        if closing is not None:
            card.closing_previous_month = closing

        card.save()
    except KeyError as e:
        return HTTPStatus.BAD_REQUEST, f'missing required param {e}', None
    except Exception as e:
        return HTTPStatus.BAD_REQUEST, str(e), None


    return HTTPStatus.OK, '', card