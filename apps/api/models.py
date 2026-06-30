from django.db import models
from django.conf import settings
from django.db.models import Sum, Q
import datetime as dt

from services.tools import format_coin

class Card(models.Model):
    name = models.CharField(max_length=20)
    closing_day = models.IntegerField()
    due_day = models.IntegerField()
    closing_previous_month = models.BooleanField(default=False)
    limit = models.FloatField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def to_dto(self):
        return {
            'id': self.id,
            'name': self.name,
            'closing_day': self.closing_day,
            'due_day': self.due_day,
            'limit': self.limit,
            'closing_previous_month': self.closing_previous_month,
        }

class Responsable(models.Model):
    name = models.CharField(max_length=30)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def to_dto(self):
        return {
            'id': self.id,
            'name': self.name,
        }

class Invoice(models.Model):
    date_ref = models.DateField()
    closing_date = models.DateField()
    due_date = models.DateField()
    limit = models.FloatField()
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='invoices')

    @property
    def limit_formatted(self):
        return format_coin(self.limit, show_decimal='if_value')

    @property
    def date_ref_formatted(self):
        return self.date_ref.strftime('%b %y')
    
    @property
    def closing_date_formatted(self):
        return self.closing_date.strftime('%d %b %y')
    
    @property
    def due_date_formatted(self):
        return self.due_date.strftime('%d %b %y')
    
    @property
    def sum_registred(self):
        """ soma dos registros de saída com status OK ou ACCOUNTED """
        r = self.registries.filter(Q(type_in=False) & (Q(done=True) | Q(accounted=True))).aggregate(result=Sum('value'))['result']
        return r if r else 0
    
    @property
    def sum_registred_formatted(self):
        return format_coin(self.sum_registred, show_decimal='if_value')

    @property
    def sum_pending(self):
        """ soma dos registros de saída com status PENDING ou LATE """
        r = self.registries.filter(type_in=False, done=False, accounted=False).aggregate(result=Sum('value'))['result']
        return r if r else 0
    
    @property
    def sum_pending_formatted(self):
        return format_coin(self.sum_pending, show_decimal='if_value')

    def to_dto(self):
        return {
            'id': self.id,
            'date_ref': self.date_ref,
            'date_ref_formatted': self.date_ref_formatted,
            'closing_date': self.closing_date,
            'closing_date_formatted': self.closing_date_formatted,
            'due_date': self.due_date,
            'due_date_formatted': self.due_date_formatted,
            'limit': self.limit,
            'limit_formatted': self.limit_formatted,
            'card_id': self.card.id,
            'card_name': self.card.name,
            'sum_registred': self.sum_registred,
            'sum_registred_formatted': self.sum_registred_formatted,
            'sum_pending': self.sum_pending,
            'sum_pending_formatted': self.sum_pending_formatted,
        }
    
class Category(models.Model):
    title = models.CharField(max_length=100)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class Registry(models.Model):
    title = models.CharField(max_length=100)
    value = models.FloatField()
    occurrance = models.DateTimeField()
    description = models.CharField(max_length=100, null=True, default=None)
    date_ref = models.DateField()
    type_in = models.BooleanField(default=False)
    done = models.BooleanField(default=False)
    accounted = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, null=True, default=None, related_name='registries')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, default=None)
    responsable = models.ForeignKey(Responsable, on_delete=models.CASCADE, null=True, default=None)

    @property
    def status(self):
        if self.done:
            return 'OK'
        if self.accounted:
            return 'ACCOUNTED'
        return 'LATE' if  dt.datetime.now() > self.occurrance else 'PENDING'
    
    @property
    def status_without_late(self):
        if self.done:
            return 'OK'
        return 'ACCOUNTED' if self.accounted else 'PENDING'

    @property
    def installment_formatted(self):
        item = self.installment_item.first()
        return f'{item.index+1} de {item.installment.num_items}' if item else ''
    
    @property
    def occurrance_formatted(self):
        d = self.occurrance
        return d.strftime(f'%d %b %y{f', %Hh{'%M' if d.minute else ''}' if d.hour or d.minute else ''}')
    
    @property
    def category_title(self):
        return self.category.title if self.category else 'Outros'

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
            'status': self.status,
            'occurrance': self.occurrance.strftime('%d/%m/%Y %H:%M'),
            'occurrance_formatted': self.occurrance_formatted,
            'description': self.description,
            'category': self.category_title,
            'date_ref': self.date_ref.strftime('%Y-%m'),
            'type_in': self.type_in,
            'done': self.done,
            'accounted': self.accounted,
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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class InstallmentItem(models.Model):
    index = models.IntegerField()
    registry = models.ForeignKey(Registry, on_delete=models.CASCADE, related_name='installment_item')
    installment = models.ForeignKey(Installment, on_delete=models.CASCADE, related_name='items')