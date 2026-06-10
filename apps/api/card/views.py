from django.http import HttpRequest
from rest_framework.decorators import api_view

from services import cards
from services.tools import response_dto_or_error, response_obj_or_error

@api_view(["GET"])
def get_cards(request:HttpRequest):
    return response_dto_or_error(*cards.get_by_filters(request.user, **request.GET.dict()), iterable=True, safe=False)

@api_view(["GET"])
def get_card(request:HttpRequest, cardid:int):
    return response_dto_or_error(*cards.get_by_id(request.user, cardid))