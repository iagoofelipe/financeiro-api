from django.db import models
from services.tools import format_coin
from django.conf import settings

from apps.api.models import Invoice, Responsable
from services.consts import MONTHS

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

    def to_dto(self, complete=True):
        d = self.occurrance
        occurrance_formatted = d.strftime(f'%d {MONTHS[d.month-1]} %y{f', %Hh{'%M' if d.minute else ''}' if d.hour or d.minute else ''}')
        data = {
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
            'responsable_name': self.responsable.name if self.responsable else '',
            'responsable_id': self.responsable.id if self.responsable else None,
        }

        if complete:
            if self.invoice:
                data['card_id'] = self.invoice.card.id
                data['invoice_ref_formatted'] = self.invoice.date_ref.strftime(f'{MONTHS[self.invoice.date_ref.month-1]} %y')
                data['invoice_id'] = self.invoice.id

            installment_item = self.installment_item.first()
            if installment_item:
                installment = installment_item.installment
                data['installment_index'] = installment_item.index
                data['installment_num_items'] = installment.num_items
                data['installment_value'] = installment.value
                data['installment_value_formatted'] = format_coin(installment.value)
                data['installment_paid'] = installment.paid
                data['installment_paid_formatted'] = format_coin(installment.paid)
                data['installment_pending'] = installment.pending
                data['installment_pending_formatted'] = format_coin(installment.pending)
        
        return data