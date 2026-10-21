from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.request import Request
from http import HTTPStatus

from .models import RegistrySerializer, Registry

class RegistryViewSet(ModelViewSet):
    queryset = Registry.objects.all()
    serializer_class = RegistrySerializer

    def list(self, request:Request):
        try:
            values = Registry.objects.filter(user=request.user, **request.query_params.dict())
        except Exception as e:
            return Response({'detail': e.__str__()}, HTTPStatus.BAD_REQUEST)
        return Response(self.serializer_class(values, many=True).data)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        if 'user_id' not in context: context['user_id'] = self.request.user.id
        return context

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def retrieve(self, request, pk):
        obj = self.queryset.filter(pk=pk).first()
        if not obj:
            data, status = {'detail': 'dados não encontrados'}, HTTPStatus.NOT_FOUND
        elif obj.user != request.user:
            data, status = {'detail': 'acesso negado'}, HTTPStatus.FORBIDDEN
        else:
            data, status = self.serializer_class(obj).data, HTTPStatus.OK
        return Response(data, status)