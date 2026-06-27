from django.http import HttpRequest
from rest_framework.decorators import api_view
import json

from services import responsable
from services.tools import response_dto_or_error

@api_view(["GET"])
def get_responsables(request:HttpRequest):
    return response_dto_or_error(200, '', responsable.get_all(request.user), iterable=True, safe=False)

@api_view(["GET"])
def get_responsable(request:HttpRequest, id:int):
    return response_dto_or_error(*responsable.get_by_id(request.user, id))

@api_view(["POST"])
def add_responsable(request:HttpRequest):
    return response_dto_or_error(*responsable.create(request.user, **json.loads(request.body)))