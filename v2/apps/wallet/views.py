from rest_framework.decorators import api_view
from django.http import HttpRequest
from http import HTTPStatus
import json, datetime as dt

from .models import WalletLimitModel, WalletModel
from ..utils import response_success_error, response_dto_or_error

def _get_by_id(user, id) -> tuple[HTTPStatus, str, WalletModel|None]:
    wallet = WalletModel.objects.filter(id=id).first()

    if not wallet:
        return HTTPStatus.NOT_FOUND, 'dados não encontrados', None
    
    if user != wallet.user:
        return HTTPStatus.UNAUTHORIZED, 'permissão de acesso negada', None
    
    return 200, '', wallet

@api_view(['POST'])
def create(request:HttpRequest):
    data = json.loads(request.body)
    cardType = data.get('cardType', False)

    if not data.get('name') or (cardType and (not data.get('limit') or not data.get('date'))):
        return response_success_error(HTTPStatus.BAD_REQUEST, 'preencha todos os campos obrigatórios')

    if WalletModel.objects.filter(name=data['name'], user=request.user, cardType=cardType).count():
        return response_success_error(HTTPStatus.BAD_REQUEST, 'já existe uma carteira com esse nome')

    wallet = WalletModel(name=data['name'], cardType=cardType, user=request.user)
    if cardType:
        try:
            data['date'] = dt.datetime.strptime(data['date']+'-01', '%Y-%m-%d')
        except ValueError:
            return response_success_error(HTTPStatus.BAD_REQUEST, 'o parâmetro "date" deve seguir o formato AAAA-MM')

        wallet.save()
        WalletLimitModel(date=data['date'], limit=data['limit'], wallet=wallet).save()
    else:
        wallet.save()

    return response_success_error()

@api_view(['GET'])
def get_by_id(request:HttpRequest, id):
    return response_dto_or_error(*_get_by_id(request.user, id))

@api_view(['GET'])
def get_all(request:HttpRequest):
    return response_dto_or_error(200, '', obj=WalletModel.objects.filter(user=request.user), iterable=True, safe=False)

@api_view(['POST'])
def update(request:HttpRequest, id):
    result = _get_by_id(request.user, id)
    if result[0] != 200:
        return response_dto_or_error(*result)
    
    params = json.loads(request.body)
    wallet = result[2]

    for field in set(params) & WalletModel.FIELDS_ALLOW_UPDATE:
        setattr(wallet, field, params[field])
    
    return response_dto_or_error(200, '', wallet)

@api_view(['POST'])
def delete(request:HttpRequest, id):
    r = _get_by_id(request.user, id)
    if r[0] != 200:
        return response_success_error(*r)

    r[2].delete()
    return response_success_error()