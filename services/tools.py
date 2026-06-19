from typing import Literal
from django.http import JsonResponse
import datetime as dt

SUFFIX_FILTERS_TYPE = {
    'int': {'gt', 'gte', 'lt', 'lte'},
    'str': {'icontains'},
} 

def make_param_filters(type:Literal['int', 'str'], param:str, include_itself=True, ignore=[]):
    filters = { f'{param}__{v}' for v in SUFFIX_FILTERS_TYPE[type] if v not in ignore }

    if include_itself:
        filters.add(param)

    return filters

def response_dto_or_error(statuscode:int, msg:str, obj:object, iterable=False, safe=True, **dto_kwargs):
    if statuscode == 200:
        data = [o.to_dto(**dto_kwargs) for o in obj] if iterable else obj.to_dto(**dto_kwargs)
    else:
        data = {'detail': msg}
    return JsonResponse(data, status=statuscode, safe=safe)

def response_obj_or_error(statuscode:int=200, msg:str='', obj:object={}, safe=True):
    return JsonResponse(obj if statuscode == 200 else {'detail':msg}, status=statuscode, safe=safe)

def response_success_error(statuscode:int, msg:str, success:object):
    d = {'success': bool(success)}
    if msg:
        d['detail'] = msg
    return JsonResponse(d, status=statuscode)

def format_coin(val:float):
    return f"R$ {val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def months_with_current(today:dt.date=None):
    months = [ # Num Mês, Texto Mês, Mês Atual
        ['01', 'Janeiro', False],
        ['02', 'Fevereiro', False],
        ['03', 'Março', False],
        ['04', 'Abril', False],
        ['05', 'Maio', False],
        ['06', 'Junho', False],
        ['07', 'Julho', False],
        ['08', 'Agosto', False],
        ['09', 'Setembro', False],
        ['10', 'Outubro', False],
        ['11', 'Novembro', False],
        ['12', 'Dezembro', False],
    ]

    # definindo como True o mês atual
    months[(today if today else dt.date.today()).month-1][2] = True
    
    return months