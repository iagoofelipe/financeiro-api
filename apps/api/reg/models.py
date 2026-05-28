from django.db import models
from services.tools import format_coin
from django.conf import settings
import datetime as dt

from apps.api.models import Invoice, Responsable
from services.consts import MONTHS

CURRENT_YEAR = dt.date.today().year

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

    def __repr__(self):
        return self.__str__()
    
    def __str__(self):
        return f'<Registry id={self.id} title="{self.title}">'

    def to_dto(self):
        d = self.occurrance
        occurrance_formatted = d.strftime(f'%d {MONTHS[d.month-1]}{' %y' if d.year != CURRENT_YEAR else ''}, %Hh{'%M' if d.minute else ''}')
        
        return {
            'id': self.id,
            'title': self.title,
            'value': self.value,
            'value_formatted': format_coin(self.value),
            'status': self.STATUS[self.status],
            'occurrance': self.occurrance.strftime('%Y-%m-%d %H:%M'),
            'occurrance_formatted': occurrance_formatted,
            'description': self.description,
            'date_ref': self.date_ref.strftime('%Y-%m'),
            'type_in': self.type_in,
            'card_name': self.invoice.card.name if self.invoice else '',
            'card_id': self.invoice.card.id if self.invoice else None,
            'invoice_ref': self.invoice.date_ref.strftime('%Y-%m') if self.invoice else None,
            'invoice_id': self.invoice.id if self.invoice else None,
            'responsable_name': self.responsable.name if self.responsable else '',
            'responsable_id': self.responsable.id if self.responsable else None,
        }