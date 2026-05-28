from django.http import HttpRequest, JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
import json

from services import registries
from services.tools import response_dto_or_error, response_obj_or_error

@api_view(["GET"])
def get_registries(request:HttpRequest):
    return response_dto_or_error(*registries.get_by_filters(request.user, **request.GET.dict()), iterable=True, safe=False)

@api_view(["GET"])
def get_registry(request:HttpRequest, regid:int):
    return response_dto_or_error(*registries.get_by_id(request.user, regid))

@api_view(["POST"])
def add_registry(request:HttpRequest):
    return response_dto_or_error(*registries.create(request.user, **json.loads(request.body)))

@api_view(["GET"])
def get_reg_date_references(request:HttpRequest):
    return response_obj_or_error(200, '', list(registries.get_date_references(request.user)), safe=False)