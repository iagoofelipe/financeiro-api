from rest_framework import serializers
from django.conf import settings
from django.db import models
from uuid import uuid4
import datetime as dt

class Wallet(models.Model):
    id = models.CharField(default=uuid4, primary_key=True)
    name = models.CharField(max_length=20)
    cardType = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class WalletSerializer(serializers.ModelSerializer):
    cardLimit = serializers.SerializerMethodField(method_name='get_card_limit')
    cardDateReference = serializers.SerializerMethodField(method_name='get_card_date_ref')

    class Meta:
        model = Wallet
        read_only_fields = ['id']
        fields = ['id', 'name', 'cardType', 'cardDateReference', 'cardLimit']

    def _get_limit_change(self, obj):
        if not obj.cardType:
            return None

        if not hasattr(self, '_limit_change_cache'):
            self._limit_change_cache = {}

        if obj.pk not in self._limit_change_cache:
            date = self.context.get('maxCardDateReference', dt.date.today())
            self._limit_change_cache[obj.pk] = (
                obj.limits.filter(date__lte=date)
                .order_by('-date')
                .first()
            )

        return self._limit_change_cache[obj.pk]

    def get_card_limit(self, obj):
        limit_change = self._get_limit_change(obj)
        return limit_change.limit if limit_change else None

    def get_card_date_ref(self, obj):
        limit_change = self._get_limit_change(obj)
        return limit_change.date if limit_change else None

class WalletLimitChange(models.Model):
    id = models.CharField(default=uuid4, primary_key=True)
    date = models.DateField()
    limit = models.FloatField()
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='limits')

class WalletLimitChangeSerializer(serializers.ModelSerializer):
    walletId = serializers.SerializerMethodField(method_name='get_wallet_id')
    
    class Meta:
        model = WalletLimitChange
        read_only_fields = ['id']
        fields = ['id', 'date', 'limit', 'walletId']

    def get_wallet_id(self, obj): return obj.wallet.id