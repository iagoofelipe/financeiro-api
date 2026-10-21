from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.request import Request
from http import HTTPStatus

from .models import Wallet, WalletSerializer

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
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, HTTPStatus.CREATED)

    def retrieve(self, request:Request, pk):
        obj = self.queryset.filter(pk=pk).first()
        if not obj:
            data, status = {'detail': 'dados não encontrados'}, HTTPStatus.NOT_FOUND
        elif obj.user != request.user:
            data, status = {'detail': 'acesso negado'}, HTTPStatus.FORBIDDEN
        else:
            data, status = self.serializer_class(obj).data, HTTPStatus.OK
        return Response(data, status)