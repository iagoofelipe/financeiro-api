from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.request import Request
from http import HTTPStatus
import json

from .models import Wallet, WalletSerializer, WalletLimitChangeSerializer

class WalletViewSet(ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer

    def list(self, request:Request):
        params = request.query_params.dict()
        context = {}
        if 'maxCardDateReference' in params:
            context['maxCardDateReference'] = params.pop('maxCardDateReference')

        try:
            values = self.queryset.filter(user=request.user, **params)
        except Exception as e:
            return Response({'detail': e.__str__()}, HTTPStatus.BAD_REQUEST)
        return Response(self.serializer_class(values, many=True, context=context).data)

    def create(self, request:Request):
        data = json.loads(request.body)
        
        card_type = data.get('cardType', False)
        if card_type and ('cardDateReference' not in data or 'cardLimit' not in data):
            return Response(
                {'detail': 'cardDateReference and cardLimit required when cardType'},
                HTTPStatus.BAD_REQUEST,
            )

        serializer = self.serializer_class(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, HTTPStatus.BAD_REQUEST)

        limit_serializer = None
        if card_type:
            limit_serializer = WalletLimitChangeSerializer(data={
                'date': data['cardDateReference'],
                'limit': data['cardLimit'],
            })
            if not limit_serializer.is_valid():
                return Response(limit_serializer.errors, HTTPStatus.BAD_REQUEST)
        
        wallet = serializer.save(user=request.user)
        if limit_serializer:
            limit_serializer.save(wallet=wallet)        

        return Response(self.serializer_class(wallet).data, HTTPStatus.CREATED)

    def retrieve(self, request:Request, pk):
        obj = self.queryset.filter(pk=pk).first()
        if not obj:
            data, status = {'detail': 'dados não encontrados'}, HTTPStatus.NOT_FOUND
        elif obj.user != request.user:
            data, status = {'detail': 'acesso negado'}, HTTPStatus.FORBIDDEN
        else:
            data, status = self.serializer_class(obj).data, HTTPStatus.OK
        return Response(data, status)