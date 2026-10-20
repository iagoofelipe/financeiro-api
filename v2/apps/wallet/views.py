from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view
from django.http import HttpRequest
from http import HTTPStatus
import json, datetime as dt

from .models import WalletLimitChange, Wallet, WalletSerializer
from ..utils import response_success_error, response_dto_or_error
from . import services as wallet_services

class WalletViewSet(ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer

    def list(self, request:Request):
        params = request.query_params.dict()
        if {'user', 'user_id', 'user__id'} & set(params):
            return Response({'detail': 'parâmetro user não permitido'}, HTTPStatus.BAD_REQUEST)
        try:
            values = self.queryset.filter(user=request.user, **params)
        except Exception as e:
            return Response({'detail': e.__str__()}, HTTPStatus.BAD_REQUEST)
        return Response(self.serializer_class(values, many=True).data)

    def retrieve(self, request, pk):
        if not self.queryset.filter(pk=pk, user=request.user).count():
            return Response({'detail': 'dados não encontrados'}, HTTPStatus.NOT_FOUND)
        return super().retrieve(request, pk)


# @api_view(['POST'])
# def create(request:HttpRequest):
#     data = json.loads(request.body)
#     cardType = data.get('cardType', False)

#     if not data.get('name') or (cardType and (not data.get('limit') or not data.get('date'))):
#         return response_success_error(HTTPStatus.BAD_REQUEST, 'preencha todos os campos obrigatórios')

#     if Wallet.objects.filter(name=data['name'], user=request.user, cardType=cardType).count():
#         return response_success_error(HTTPStatus.BAD_REQUEST, 'já existe uma carteira com esse nome')

#     wallet = Wallet(name=data['name'], cardType=cardType, user=request.user)
#     if cardType:
#         try:
#             data['date'] = dt.datetime.strptime(data['date']+'-01', '%Y-%m-%d')
#         except ValueError:
#             return response_success_error(HTTPStatus.BAD_REQUEST, 'o parâmetro "date" deve seguir o formato AAAA-MM')

#         wallet.save()
#         WalletLimitChange(date=data['date'], limit=data['limit'], wallet=wallet).save()
#     else:
#         wallet.save()

#     return response_dto_or_error(200, '', wallet)

# @api_view(['GET'])
# def get_by_id(request:HttpRequest, id):
#     dto_params = request.GET.dict()
#     dto_params['complete'] = dto_params['complete'] == 'True'
#     return response_dto_or_error(*wallet_services.get_wallet_by_id(request.user, id), dto_params=dto_params)

# @api_view(['GET'])
# def get_all(request:HttpRequest):
#     return response_dto_or_error(200, '', obj=Wallet.objects.filter(user=request.user), iterable=True)

# @api_view(['POST'])
# def update(request:HttpRequest, id):
#     result = wallet_services.get_wallet_by_id(request.user, id)
#     if result[0] != 200:
#         return response_dto_or_error(*result)
    
#     params = json.loads(request.body)
#     wallet = result[2]

#     for field in set(params) & Wallet.FIELDS_ALLOW_UPDATE:
#         setattr(wallet, field, params[field])
#     wallet.save()
#     return response_dto_or_error(200, '', wallet)

# @api_view(['POST'])
# def delete(request:HttpRequest, id):
#     status, msg, wallet = wallet_services.get_wallet_by_id(request.user, id)
#     if not wallet:
#         return response_success_error(status, msg)

#     wallet.delete()
#     return response_success_error()