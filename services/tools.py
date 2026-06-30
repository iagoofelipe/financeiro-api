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

def response_success_error(statuscode:int, msg:str, success:object=None):
    d = {'success': bool(success or statuscode == 200)}
    if msg:
        d['detail'] = msg
    return JsonResponse(d, status=statuscode)

def format_coin(val:float, prefix:str|None='R$', show_decimal:Literal['always', 'if_value']='always'):
    _str = (prefix+' ') if prefix is not None else ''
    _str += f'{val:,.2f}' if show_decimal == 'always' or (show_decimal == 'if_value' and not val.is_integer()) else f'{val:,.0f}'
    return _str.replace(",", "X").replace(".", ",").replace("X", ".")

def months_with_current(today:dt.date=None):
    months = [
        {'number': '01', 'text': 'janeiro', 'is_current': False},
        {'number': '02', 'text': 'fevereiro', 'is_current': False},
        {'number': '03', 'text': 'março', 'is_current': False},
        {'number': '04', 'text': 'abril', 'is_current': False},
        {'number': '05', 'text': 'maio', 'is_current': False},
        {'number': '06', 'text': 'junho', 'is_current': False},
        {'number': '07', 'text': 'julho', 'is_current': False},
        {'number': '08', 'text': 'agosto', 'is_current': False},
        {'number': '09', 'text': 'setembro', 'is_current': False},
        {'number': '10', 'text': 'outubro', 'is_current': False},
        {'number': '11', 'text': 'novembro', 'is_current': False},
        {'number': '12', 'text': 'dezembro', 'is_current': False},
    ]

    # definindo como True o mês atual
    months[(today if today else dt.date.today()).month-1]['is_current'] = True
    
    return months