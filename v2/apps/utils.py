from django.http import JsonResponse

def response_dto_or_error(statuscode:int, msg:str, obj:object, iterable=False, safe=True, **dto_kwargs):
    if statuscode == 200:
        data = [o.to_dto(**dto_kwargs) for o in obj] if iterable else obj.to_dto(**dto_kwargs)
    else:
        data = {'detail': msg}
    return JsonResponse(data, status=statuscode, safe=safe)

def response_obj_or_error(statuscode:int=200, msg:str='', obj:object={}, safe=True):
    return JsonResponse(obj if statuscode == 200 else {'detail':msg}, status=statuscode, safe=safe)

def response_success_error(statuscode:int=200, msg:str='', success:object=None):
    d = {'success': bool(success or statuscode == 200)}
    if msg:
        d['detail'] = msg
    return JsonResponse(d, status=statuscode)