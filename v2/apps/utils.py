from typing import Protocol, Iterable, Any
from django.http import JsonResponse

SUFFIX_FILTERS_BY_TYPE = {
    'number': {'gt', 'gte', 'lt', 'lte'},
    'string': {'contains', 'icontains'},
}

class DtoParser(Protocol):
    def to_dto(self, **kwargs) -> dict: ...

def response_dto_or_error(statuscode:int, msg:str, obj:DtoParser|Iterable[DtoParser], iterable=False, dto_params={}):
    if statuscode == 200:
        data = [o.to_dto(**dto_params) for o in obj] if iterable else obj.to_dto(**dto_params)
    else:
        data = {'detail': msg}
    return JsonResponse(data, status=statuscode, safe=False)

def response_obj_or_error(statuscode:int=200, msg:str='', obj:object={}):
    return JsonResponse(obj if statuscode == 200 else {'detail':msg}, status=statuscode, safe=False)

def response_success_error(statuscode:int=200, msg:str=''):
    return JsonResponse({'detail': msg} if msg else {}, status=statuscode)

def params_validator(params:dict[str, Any], valids:dict[str, Iterable[str]]):
    for k, v in params.items():
        suffix = ''
        if '__' in k:
            k, suffix = k.split('__', 1)

        if k not in valids or (suffix and suffix not in valids[k]):
            return k

        