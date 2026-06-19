from apps.api import models
from http import HTTPStatus
import datetime as dt
from dateutil.relativedelta import relativedelta

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from django.db.models import BaseManager

from . import consts

def get_by_filters(user, **filters) -> tuple[HTTPStatus, str, "BaseManager"[models.Invoice] | None]:
    """ consulta os cartões aplicando os filtros fornecidos. A filtragem segue o padrão de `key__condition` do django """
    
    # adicionando filtros
    invalid_filters = set(filters) - consts.INVOICE_FILTERS
    if invalid_filters:
        return  HTTPStatus.BAD_REQUEST, f'parâmetros {invalid_filters} inválidos', None

    filters = { k: filters[k] for k in set(filters) & consts.INVOICE_FILTERS }

    # TODO: adicionar filtragem por usuário em Card.user
    return HTTPStatus.OK, '', models.Invoice.objects.filter(**filters).all()

def get_by_id(user, id:int) -> tuple[HTTPStatus, str, models.Invoice | None]:
    obj = models.Invoice.objects.filter(id=id).first()
    if not obj:
        return HTTPStatus.NOT_FOUND, 'nenhum dado encontrado para o ID fornecido', None
    
    if obj.card.user != user:
        return HTTPStatus.METHOD_NOT_ALLOWED, 'permissão de acesso negada', None
    
    return HTTPStatus.OK, '', obj

def get_or_create(card:models.Card, date_ref:dt.date):
    obj = models.Invoice.objects.filter(card=card, date_ref=date_ref).first()
    if obj:
        return obj
    
    closing_date = dt.date(date_ref.year, date_ref.month, card.closing_day)

    if card.closing_previous_month:
        closing_date -= relativedelta(months=1)

    obj = models.Invoice(
        date_ref=date_ref,
        closing_date=closing_date,
        due_date=dt.date(date_ref.year, date_ref.month, card.due_day),
        limit=card.limit,
        card=card,
    )
    obj.save()

    return obj