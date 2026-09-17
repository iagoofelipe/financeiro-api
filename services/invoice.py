from http import HTTPStatus
import datetime as dt
from dateutil.relativedelta import relativedelta
from django.db.models import Sum

from typing import Literal

from apps.api import models

def get_by_id(user, id:int) -> tuple[HTTPStatus, str, models.Invoice | None]:
    obj = models.Invoice.objects.filter(id=id).first()
    if not obj:
        return HTTPStatus.NOT_FOUND, 'nenhum dado encontrado para o ID fornecido', None
    
    if obj.card.user != user:
        return HTTPStatus.METHOD_NOT_ALLOWED, 'permissão de acesso negada', None
    
    return HTTPStatus.OK, '', obj

def get_by_card(user, condition:Literal['id', 'name'], key:int|str, date_ref:dt.date|str) -> tuple[HTTPStatus, str, models.Invoice | None]:
    filters = {
        'card__user': user,
        'date_ref': date_ref,
    }

    if isinstance(date_ref, str):
        try:
            filters['date_ref'] = dt.date.strptime(date_ref, '%Y-%m-01')
        except ValueError:
            return HTTPStatus.BAD_REQUEST, 'date_ref deve seguir o formato AAAA-MM-01', None
    
    match condition:
        case 'id':
            key_is_str = isinstance(key, str)
            
            if key_is_str and not key.isdigit():
                return HTTPStatus.BAD_REQUEST, 'o id deve ser um inteiro', None

            filters['card__id'] = int(key)

        case 'name': filters['card__name'] = key
        case _: return HTTPStatus.BAD_REQUEST, 'condition deve ser id ou name', None
    
    obj = models.Invoice.objects.filter(**filters).first()
    if not obj:
        return HTTPStatus.NOT_FOUND, 'nenhum dado encontrado para os parâmetros fornecidos', None
    
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

def update_values_by_id(user, invoice_id:int) -> tuple[HTTPStatus, str, models.Invoice | None]:
    r = get_by_id(user, invoice_id)
    invoice = r[2]

    if invoice is None:
        return r

    sum_inputs = invoice.registries.filter(type_in=True).aggregate(value=Sum('value'))['value']
    sum_outputs = invoice.registries.filter(type_in=False).aggregate(value=Sum('value'))['value']

    invoice.used = (sum_outputs if sum_outputs else 0) - (sum_inputs if sum_inputs else 0)
    invoice.available = invoice.limit - invoice.used
    invoice.save()

    return 200, '', invoice

def update_all_by_user(user):
    invoices = models.Invoice.objects.filter(card__user=user)

    for invoice in invoices:
        sum_inputs = invoice.registries.filter(type_in=True).aggregate(value=Sum('value'))['value']
        sum_outputs = invoice.registries.filter(type_in=False).aggregate(value=Sum('value'))['value']

        invoice.used = (sum_outputs if sum_outputs else 0) - (sum_inputs if sum_inputs else 0)
        invoice.available = invoice.limit - invoice.used

    models.Invoice.objects.bulk_update(invoices, ['used', 'available'])

    return 200, ''