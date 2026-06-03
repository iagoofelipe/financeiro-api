from typing import Literal
from django.http import JsonResponse

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

def response_obj_or_error(statuscode:int, msg:str, obj:object, safe=True):
    return JsonResponse(obj if statuscode == 200 else {'detail':msg}, status=statuscode, safe=safe)

def response_success_error(statuscode:int, msg:str, success:object):
    d = {'success': bool(success)}
    if msg:
        d['detail'] = msg
    return JsonResponse(d, status=statuscode)

def format_coin(val:float):
    return f"R$ {val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")