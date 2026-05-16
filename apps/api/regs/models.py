from django.db import models
from django.conf import settings

from ..invoices.models import Invoice
from ..responsables.models import Responsable

__all__ = ('Registry', )
MONTHS = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']

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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, null=True, default=None)
    responsable = models.ForeignKey(Responsable, on_delete=models.CASCADE, null=True, default=None)

    def to_dto(self):
        return {
            'id': self.id,
            'title': self.title,
            'value': self.value,
            'status': self.STATUS[self.status],
            'occurrance': self.occurrance.strftime('%Y-%m-%d %H:%M'),
            'occurrance_formatted': self.occurrance.strftime('%d {MONTH} %y, %Hh%M').replace('{MONTH}', MONTHS[self.occurrance.month-1]),
            'description': self.description,
            'date_ref': self.date_ref.strftime('%Y-%m'),
            'type_in': self.type_in,
            # 'user_id': self.user.id,
            'card_name': self.invoice.card.name if self.invoice else None,
            'card_id': self.invoice.card.id if self.invoice else None,
            'invoice_ref': self.invoice.date_reference.strftime('%Y-%m') if self.invoice else None,
            'invoice_id': self.invoice.id if self.invoice else None,
            'responsable_name': self.responsable.name if self.responsable else None,
            'responsable_id': self.responsable.id if self.responsable else None,
        }