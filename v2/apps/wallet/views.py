from rest_framework.decorators import api_view
from django.http import HttpRequest
from http import HTTPStatus
import json, datetime as dt

from .models import WalletLimitChange, Wallet
from ..utils import response_success_error, response_dto_or_error
from . import services as wallet_services

@api_view(['POST'])
def create(request:HttpRequest):
    data = json.loads(request.body)
    cardType = data.get('cardType', False)

    if not data.get('name') or (cardType and (not data.get('limit') or not data.get('date'))):
        return response_success_error(HTTPStatus.BAD_REQUEST, 'preencha todos os campos obrigatórios')

    if Wallet.objects.filter(name=data['name'], user=request.user, cardType=cardType).count():
        return response_success_error(HTTPStatus.BAD_REQUEST, 'já existe uma carteira com esse nome')

    wallet = Wallet(name=data['name'], cardType=cardType, user=request.user)
    if cardType:
        try:
            data['date'] = dt.datetime.strptime(data['date']+'-01', '%Y-%m-%d')
        except ValueError:
            return response_success_error(HTTPStatus.BAD_REQUEST, 'o parâmetro "date" deve seguir o formato AAAA-MM')

        wallet.save()
        WalletLimitChange(date=data['date'], limit=data['limit'], wallet=wallet).save()
    else:
        wallet.save()

    return response_dto_or_error(200, '', wallet)

@api_view(['GET'])
def get_by_id(request:HttpRequest, id):
    dto_params = request.GET.dict()
    dto_params['complete'] = dto_params['complete'] == 'True'
    return response_dto_or_error(*wallet_services.get_wallet_by_id(request.user, id), dto_params=dto_params)

@api_view(['GET'])
def get_all(request:HttpRequest):
    return response_dto_or_error(200, '', obj=Wallet.objects.filter(user=request.user), iterable=True)

@api_view(['POST'])
def update(request:HttpRequest, id):
    result = wallet_services.get_wallet_by_id(request.user, id)
    if result[0] != 200:
        return response_dto_or_error(*result)
    
    params = json.loads(request.body)
    wallet = result[2]

    for field in set(params) & Wallet.FIELDS_ALLOW_UPDATE:
        setattr(wallet, field, params[field])
    wallet.save()
    return response_dto_or_error(200, '', wallet)

@api_view(['POST'])
def delete(request:HttpRequest, id):
    status, msg, wallet = wallet_services.get_wallet_by_id(request.user, id)
    if not wallet:
        return response_success_error(status, msg)

    wallet.delete()
    return response_success_error()