from django.http import HttpRequest
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
import json

from services import registries
from services.tools import response_dto_or_msg_error

@api_view(["GET"])
# @permission_classes([IsAuthenticated])
def get_registries(request:HttpRequest):
    return response_dto_or_msg_error(*registries.get_by_filters(request.user, **request.GET.dict()), iterable=True, safe=False)
    # statuscode, error, obj = registries.get_by_filters(request.user, **request.GET.dict())
    # return JsonResponse(to_dto_or_msg_error(statuscode, error, obj, True), status=statuscode, safe=False)

@api_view(["GET"])
# @permission_classes([IsAuthenticated])
def get_registry(request:HttpRequest, regid:int):
    return response_dto_or_msg_error(*registries.get_by_id(request.user, regid))
    # statuscode, error, obj = registries.get_by_id(request.user, regid)
    # return JsonResponse(to_dto_or_msg_error(statuscode, error, obj), status=statuscode)

@api_view(["POST"])
# @permission_classes([IsAuthenticated])
def add_registry(request:HttpRequest):
    return response_dto_or_msg_error(*registries.create(request.user, **json.loads(request.body)))
    # statuscode, error, obj = registries.create(request.user, **json.loads(request.body))
    # return JsonResponse(to_dto_or_msg_error(statuscode, error, obj), status=statuscode)