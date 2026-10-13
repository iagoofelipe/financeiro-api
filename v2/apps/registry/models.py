from django.conf import settings
from django.db import models
from uuid import uuid4

from ..wallet.models import Wallet

class Registry(models.Model):

    class Status(models.TextChoices):
        PENDING = 'P', 'PENDING'
        OK = 'O', 'OK'
        ACCOUNTED = 'A', 'ACCOUNTED'

    StatusMapped = dict(Status.choices)

    id = models.CharField(primary_key=True, default=uuid4)
    title = models.CharField(max_length=100)
    value = models.FloatField()
    occurrence = models.DateTimeField()
    reference = models.DateField()
    typeIn = models.BooleanField(default=False)
    status = models.CharField(choices=Status.choices, default=Status.PENDING)
    description = models.CharField(max_length=100, null=True, default=None)
    category = models.CharField(max_length=100, null=True, default=None)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, null=True)

    def to_dto(self):
        return {
            'id': self.id,
            'title': self.title,
            'value': self.value,
            'occurrence': self.occurrence.strftime('%Y-%m-%d %H:%M'),
            'description': self.description,
            'category': self.category,
            'reference': self.reference.strftime('%Y-%m'),
            'typeIn': self.typeIn,
            'status': self.StatusMapped[self.status],
            'walletId': self.wallet.id if self.wallet else None,
            'walletName': self.wallet.name if self.wallet else None,
        }