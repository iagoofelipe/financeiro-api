from rest_framework import serializers
from django.conf import settings
from django.db import models, transaction
from django.db.models import Sum, Q
from uuid import uuid4
import datetime as dt

class Wallet(models.Model):
    id = models.CharField(default=uuid4, primary_key=True)
    name = models.CharField(max_length=20)
    cardType = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class WalletSerializer(serializers.ModelSerializer):
    cardLimit = serializers.FloatField(write_only=True, required=False)
    cardDateReference = serializers.DateField(write_only=True, required=False)
    cardAvailable = serializers.FloatField(write_only=True, required=False)
    available = serializers.FloatField(write_only=True, required=False)
    finalAvailable = serializers.FloatField(write_only=True, required=False)
    totalIn = serializers.SerializerMethodField(method_name='get_total_in')
    totalOut = serializers.SerializerMethodField(method_name='get_total_out')
    pendingTotalIn = serializers.SerializerMethodField(method_name='get_pending_total_in')
    pendingTotalOut = serializers.SerializerMethodField(method_name='get_pending_total_out')

    class Meta:
        model = Wallet
        read_only_fields = ['id']
        fields = [
            'id', 'name', 'cardType', 'totalIn', 'totalOut',
            'pendingTotalIn', 'pendingTotalOut', 'available',
            'finalAvailable', 'cardDateReference', 'cardLimit', 'cardAvailable',
        ]

    def __init__(self, *args, **kwargs):
        self._cache = {'sums': {}}
        super().__init__(*args, **kwargs)

    def _get_sums(self, obj):
        if obj.pk not in self._cache['sums']:
            sums = obj.registry_set.aggregate(
                inputs_ok=Sum('value', filter=Q(typeIn=True, status='OK')),
                outputs_ok=Sum('value', filter=Q(typeIn=False, status='OK')),
                inputs_pending=Sum('value', filter=Q(typeIn=True, status='PENDING')),
                outputs_pending=Sum('value', filter=Q(typeIn=False, status='PENDING')),
            )
            self._cache['sums'][obj.pk] = {k: sums[k] if sums[k] else 0 for k in sums}
        return self._cache['sums'][obj.pk]

    def get_total_in(self, obj): return self._get_sums(obj)['inputs_ok']
    def get_total_out(self, obj): return self._get_sums(obj)['outputs_ok']
    def get_pending_total_in(self, obj): return self._get_sums(obj)['inputs_pending']
    def get_pending_total_out(self, obj): return self._get_sums(obj)['outputs_pending']

    def validate(self, attrs):
        if attrs.get('cardType', False):
            missing_fields = {}
            if 'cardDateReference' not in attrs:
                missing_fields['cardDateReference'] = 'This field is required when cardType is true.'
            if 'cardLimit' not in attrs:
                missing_fields['cardLimit'] = 'This field is required when cardType is true.'
            if missing_fields:
                raise serializers.ValidationError(missing_fields)

        return attrs

    def create(self, validated_data):
        card_date_reference = validated_data.pop('cardDateReference', None)
        card_limit = validated_data.pop('cardLimit', None)

        with transaction.atomic(): # garantindo que seja gravado apenas se tudo ocorrer com sucesso
            wallet = super().create(validated_data)
            if wallet.cardType:
                WalletLimitChange.objects.create(
                    wallet=wallet,
                    date=card_date_reference,
                    limit=card_limit,
                )

        return wallet

    def to_representation(self, instance):
        data = super().to_representation(instance)
        
        if instance.cardType:
            date = self.context.get('maxCardDateReference', dt.date.today())
            limit_change = instance.limits.filter(date__lte=date).order_by('-date').first()
        else:
            limit_change = None

        data['cardDateReference'] = limit_change.date if limit_change else None
        data['cardLimit'] = limit_change.limit if limit_change else None
        
        cardLimit = data['cardLimit'] if data['cardLimit'] else 0
        data['cardAvailable'] = cardLimit - data['totalIn'] + data['totalOut'] if limit_change else None
        data['available'] = data['totalIn'] - data['totalOut']
        data['finalAvailable'] = (data['totalIn'] + data['pendingTotalIn']) - (data['totalOut'] + data['pendingTotalOut'])

        return data

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