from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.request import Request
from http import HTTPStatus
import json

from .models import RegistrySerializer, Registry

class RegistryViewSet(ModelViewSet):
    queryset = Registry.objects.all()
    serializer_class = RegistrySerializer

    def list(self, request:Request):
        params = request.query_params.dict()
        if {'user', 'user_id', 'user__id'} & set(params):
            return Response({'detail': 'parâmetro user não permitido'}, HTTPStatus.BAD_REQUEST)

        try:
            values = Registry.objects.filter(user=request.user, **params)
        except Exception as e:
            return Response({'detail': e.__str__()}, HTTPStatus.BAD_REQUEST)
        return Response(self.serializer_class(values, many=True).data)
    
    def create(self, request:Request):
        serializer = self.serializer_class(data=json.loads(request.body), context={'user_id': request.user.id})
        if serializer.is_valid():
            serializer.save(user=request.user)
            status = HTTPStatus.OK
            data = serializer.data
        else:
            status = HTTPStatus.BAD_REQUEST
            data = serializer.errors
        return Response(data, status)

    def retrieve(self, request, pk):
        if not self.queryset.filter(pk=pk, user=request.user).count():
            return Response({'detail': 'dados não encontrados'}, HTTPStatus.NOT_FOUND)
        return super().retrieve(request, pk)