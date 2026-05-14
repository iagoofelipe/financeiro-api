from django.db import models

from ..users.models import User
from ..invoices.models import Invoice
from ..responsables.models import Responsable

__all__ = ('Registry', )

class Registry(models.Model):
    STATUS = {
        'P': 'PENDING',
        'O': 'OK',
        'L': 'LATE',
    }

    title = models.CharField(max_length=100)
    value = models.FloatField()
    status = models.CharField(choices=STATUS, max_length=1)
    occurrance = models.DateTimeField()
    description = models.CharField(max_length=100, null=True, default=None)
    date_ref = models.DateField()
    type_in = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, null=True, default=None)
    responsable = models.ForeignKey(Responsable, on_delete=models.CASCADE, null=True, default=None)

    def to_dto(self):
        return {
            'title': self.title,
            'value': self.value,
            'status': self.status,
            'occurrance': self.occurrance.strftime('%Y-%m-%d %H:%M'),
            'description': self.description,
            'date_ref': self.date_ref.strftime('%Y-%m'),
            'user_id': self.user.id,
            'card_name': self.invoice.card.name if self.invoice else None,
            'card_id': self.invoice.card.id if self.invoice else None,
            'invoice_ref': self.invoice.date_reference.strftime('%Y-%m') if self.invoice else None,
            'invoice_id': self.invoice.id if self.invoice else None,
            'responsable_name': self.responsable.name if self.responsable else None,
            'responsable_id': self.responsable.id if self.responsable else None,
        }