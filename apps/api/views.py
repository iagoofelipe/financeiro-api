from django.http import JsonResponse, HttpRequest
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
import json

from services import registries
from services.tools import to_dto_or_msg_error

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_registries(request:HttpRequest):
    statuscode, error, obj = registries.get_by_filters(request.user, **request.GET.dict())
    return JsonResponse(to_dto_or_msg_error(statuscode, error, obj, True), status=statuscode, safe=False)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_registry(request:HttpRequest, regid:int):
    statuscode, error, obj = registries.get_by_id(request.user, regid)
    return JsonResponse(to_dto_or_msg_error(statuscode, error, obj), status=statuscode)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_registry(request:HttpRequest):
    statuscode, error, obj = registries.create(request.user, **json.loads(request.body))
    return JsonResponse(to_dto_or_msg_error(statuscode, error, obj), status=statuscode)
