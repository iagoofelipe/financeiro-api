from rest_framework.decorators import api_view
from django.http import HttpRequest
from django.core.exceptions import ValidationError
from http import HTTPStatus
import json

from .models import Registry
from ..wallet.models import Wallet
from ..utils import response_success_error, response_dto_or_error, SUFFIX_FILTERS_BY_TYPE, params_validator

GET_ALL_VALID_FILTERS = {
    'title': SUFFIX_FILTERS_BY_TYPE['string'],
    'value': SUFFIX_FILTERS_BY_TYPE['number'],
    'occurrence': SUFFIX_FILTERS_BY_TYPE['number'],
    'status': [],
}

CREATE_FIELDS = { 'title', 'value', 'occurrence', 'reference', 'typeIn', 'status', 'description', 'category', 'wallet', 'user' }


@api_view(['POST'])
def create(request:HttpRequest):
    data = json.loads(request.body)
    data['user'] = request.user

    if 'walletId' in data:
        data['wallet'] = Wallet.objects.filter(id=data['walletId']).first()
        if data['wallet'] is None:
            return response_success_error(HTTPStatus.NOT_FOUND, 'não foi possível localizar a carteira fornecida')
        if data['wallet'].user != request.user:
            return response_success_error(HTTPStatus.FORBIDDEN, 'a carteira fonecida não pertence ao usuário conectado')
        
    try:
        params = { k: data[k] for k in CREATE_FIELDS if (k in data and data[k] is not None) }
        params['reference'] += '-01'
        reg = Registry(**params)
        reg.save()
    except KeyError:
        return response_success_error(HTTPStatus.BAD_REQUEST, 'preencha todos os campos obrigatórios!')
    except ValidationError as e:
        return response_success_error(HTTPStatus.BAD_REQUEST, e.__str__())
    
    return response_dto_or_error(200, '', Registry.objects.filter(id=reg.id).first())

@api_view(['GET'])
def get_all(request:HttpRequest):
    params = request.GET.dict()
    invalid = params_validator(params, GET_ALL_VALID_FILTERS)
    if invalid:
        return response_success_error(HTTPStatus.BAD_REQUEST, f'invalid param "{invalid}"')

    params['user'] = request.user
    return response_dto_or_error(200, '', Registry.objects.filter(**params), True)

@api_view(['GET'])
def get_by_id(request:HttpRequest, id):
    obj = Registry.objects.filter(id=id, user=request.user).first()
    if obj:
        status = 200
        msg = ''
    else:
        status = 404
        msg = 'dados não encontrados'
    return response_dto_or_error(status, msg, obj)