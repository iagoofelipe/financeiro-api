from django.conf import settings
from django.db import models
from uuid import uuid4

class WalletModel(models.Model):
    id = models.CharField(default=uuid4, primary_key=True)
    name = models.CharField(max_length=20)
    cardType = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    FIELDS_ALLOW_UPDATE = {'name', 'cardType'}

    def to_dto(self, date=None):
        data = {
            'id': self.id,
            'name': self.name,
            'cardType': self.cardType,
        }

        if date:
            data['']

        return data

class WalletLimitModel(models.Model):
    id = models.CharField(default=uuid4, primary_key=True)
    date = models.DateField()
    limit = models.DecimalField()
    wallet = models.ForeignKey(WalletModel, on_delete=models.CASCADE, related_name='limits')
