from rest_framework import serializers
from django.conf import settings
from django.db import models
from uuid import uuid4
import re

from ..wallet.models import Wallet

class Registry(models.Model):
    id = models.CharField(primary_key=True, default=uuid4)
    title = models.CharField(max_length=100)
    value = models.FloatField()
    occurrence = models.DateTimeField()
    reference = models.CharField(max_length=7)
    typeIn = models.BooleanField(default=False)
    status = models.CharField(max_length=100, default='PENDING')
    description = models.CharField(max_length=100, null=True, default=None)
    category = models.CharField(max_length=100, null=True, default=None)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, null=True)

class RegistrySerializer(serializers.ModelSerializer):
    occurrence = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    status = serializers.CharField(max_length=100, default='PENDING')
    walletId = serializers.PrimaryKeyRelatedField(
        source='wallet',
        queryset=Wallet.objects.all(),
        required=False,
        allow_null=True,
    )
    walletName = serializers.SerializerMethodField(method_name='get_wallet_name')

    class Meta:
        model = Registry
        read_only_fields = ['id']
        fields = [
            'id', 'title', 'value', 'occurrence',
            'description', 'category', 'reference', 'typeIn',
            'status', 'walletId', 'walletName',
        ]

    def get_wallet_name(self, obj):
        return obj.wallet.name if obj.wallet else None

    def validate_walletId(self, wallet):
        user_id = self.context.get('user_id')
        if user_id is None:
            raise serializers.ValidationError('user_id ausente no contexto do serializer')
        if wallet.user_id != user_id:
            raise serializers.ValidationError('a carteira fornecida não pertence ao usuário conectado')
        return wallet

    def validate_status(self, status):
        if status not in ['PENDING', 'ACCOUNTED', 'OK']:
            raise serializers.ValidationError(f'o valor "{status}" não é um status válido')
        return status

    def validate_reference(self, reference):
        if not re.fullmatch(r'\d{4}-(0(1|2|3|4|5|6|7|8|9)|1(0|1|2))', reference):
            raise serializers.ValidationError("'reference' deve seguir o padrão AAAA-MM")
        return reference
