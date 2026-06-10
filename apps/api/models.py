from django.db import models
from django.conf import settings

from services.tools import format_coin

class Card(models.Model):
    name = models.CharField(max_length=20)
    closing_day = models.IntegerField()
    due_day = models.IntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def to_dto(self):
        return {
            'id': self.id,
            'name': self.name,
            'closing_day': self.closing_day,
            'due_day': self.due_day,
        }

class Responsable(models.Model):
    name = models.CharField(max_length=30)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Invoice(models.Model):
    date_ref = models.DateField()
    closing_date = models.DateField()
    due_date = models.DateField()
    limit = models.FloatField()
    card = models.ForeignKey(Card, on_delete=models.CASCADE)

    def to_dto(self):
        return {
            'id': self.id,
            'date_ref': self.date_ref,
            'closing_date': self.closing_date,
            'due_date': self.due_date,
            'limit': self.limit,
            'card_id': self.card.id,
            'card_name': self.card.name,
        }


class Registry(models.Model):
    STATUS = {
        'P': 'PENDING',
        'O': 'OK',
        'L': 'LATE',
        'A': 'ACCOUNTED',
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

    @property
    def installment_formatted(self):
        item = self.installment_item.first()
        return f'{item.index+1} de {item.installment.num_items}' if item else ''
    
    @property
    def occurrance_formatted(self):
        d = self.occurrance
        return d.strftime(f'%d %b %y{f', %Hh{'%M' if d.minute else ''}' if d.hour or d.minute else ''}')

    def __repr__(self):
        return self.__str__()
    
    def __str__(self):
        return f'<Registry id={self.id} title="{self.title}">'

    def to_dto(self, complete=True):
        data = {
            'id': self.id,
            'title': self.title,
            'value': self.value,
            'value_formatted': format_coin(self.value),
            'status': self.STATUS[self.status],
            'occurrance': self.occurrance.strftime('%Y-%m-%d %H:%M'),
            'occurrance_formatted': self.occurrance_formatted,
            'description': self.description,
            'date_ref': self.date_ref.strftime('%Y-%m'),
            'type_in': self.type_in,
            'card_name': self.invoice.card.name if self.invoice else '',
            'responsable_name': self.responsable.name if self.responsable else '',
            'responsable_id': self.responsable.id if self.responsable else None,
            'installment_formatted': self.installment_formatted,
        }

        if complete:
            if self.invoice:
                data['card_id'] = self.invoice.card.id
                data['invoice_ref_formatted'] = self.invoice.date_ref.strftime(f'%b %y')
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


class Installment(models.Model):
    num_items = models.IntegerField(default=0)
    value = models.FloatField(default=0)
    paid = models.FloatField(default=0)
    pending = models.FloatField(default=0)


class InstallmentItem(models.Model):
    index = models.IntegerField()
    registry = models.ForeignKey(Registry, on_delete=models.CASCADE, related_name='installment_item')
    installment = models.ForeignKey(Installment, on_delete=models.CASCADE, related_name='items')