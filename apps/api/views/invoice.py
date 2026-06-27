from django.http import HttpRequest
from django.shortcuts import redirect
from rest_framework.decorators import api_view
import datetime as dt

from services import invoice
from services.tools import response_dto_or_error, response_obj_or_error, response_success_error

@api_view(["GET"])
def get_invoices(request:HttpRequest):
    return response_dto_or_error(*invoice.get_by_filters(request.user, **request.GET.dict()), iterable=True, safe=False)

@api_view(["GET"])
def get_invoice(request:HttpRequest, id:int):
    return response_dto_or_error(*invoice.get_by_id(request.user, id))

@api_view(["GET"])
def get_invoice_by_card(request:HttpRequest):
    if 'q' not in request.GET:
        return response_success_error(400, 'o parâmetro q é necessário para a consulta')

    q = request.GET['q']
    field = request.GET.get('field', 'id')
    date_ref = request.GET.get('date_ref')

    if not date_ref:
        today = dt.date.today()
        date_ref = dt.date(today.year, today.month, 1)
    
    return response_dto_or_error(*invoice.get_by_card(request.user, field, q, date_ref))