from django.conf import settings
from django.db import models
from uuid import uuid4
import datetime as dt

class Wallet(models.Model):
    id = models.CharField(default=uuid4, primary_key=True)
    name = models.CharField(max_length=20)
    cardType = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    FIELDS_ALLOW_UPDATE = {'name', 'cardType'}

    def to_dto(self, date:str=None, complete:bool=False):
        wallet_limit = None
        data = {
            'id': self.id,
            'name': self.name,
            'cardType': self.cardType,
        }

        if date:
            wallet_limit = self.limits.filter(date__lte=date+'-01').order_by('-date').first()
        elif self.cardType and complete:
            wallet_limit = self.limits.filter(date__lte=dt.date.today()).order_by('-date').first()

        if complete:
            print('complete')

        if wallet_limit:
            data['limit'] = wallet_limit.limit
            #TODO: adicionar limite utilizado (registro com status ACCOUNTED)

        return data

class WalletLimitChange(models.Model):
    id = models.CharField(default=uuid4, primary_key=True)
    date = models.DateField()
    limit = models.FloatField()
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='limits')


    def to_dto(self):
        return {
            'id': self.id,
            'date': self.date.strftime('%Y-%m'),
            'limit': self.limit,
        }