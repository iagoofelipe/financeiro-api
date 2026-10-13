from rest_framework.decorators import api_view
from django.http import HttpRequest
from http import HTTPStatus

from .models import Registry
from ..utils import response_success_error, response_dto_or_error, SUFFIX_FILTERS_BY_TYPE, params_validator

GET_ALL_VALID_FILTERS = {
    'title': SUFFIX_FILTERS_BY_TYPE['string'],
    'value': SUFFIX_FILTERS_BY_TYPE['number'],
    'occurrence': SUFFIX_FILTERS_BY_TYPE['number'],
    'status': [],
}

@api_view(['POST'])
def create(request:HttpRequest): raise NotImplementedError()

@api_view(['GET'])
def get_all(request:HttpRequest):
    params = request.GET.dict()
    invalid = params_validator(params, GET_ALL_VALID_FILTERS)
    if invalid:
        return response_success_error(HTTPStatus.BAD_REQUEST, f'invalid param "{invalid}"')

    params['user'] = request.user
    return response_dto_or_error(200, '', Registry.objects.filter(**params), True)

@api_view(['GET'])
def get_by_id(request:HttpRequest, id): raise NotImplementedError()