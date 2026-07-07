from django.db.models import Sum
from http import HTTPStatus

from apps.api import models

def update_values(installment:models.Installment):
    value = installment.items.aggregate(value=Sum('registry__value'))['value']
    paid = installment.items.filter(registry__done=True).aggregate(paid=Sum('registry__value'))['paid']
    
    if paid is None:
        paid = 0

    models.Installment.objects.filter(id=installment.id).update(
        value=round(value, 2),
        paid=round(paid, 2),
        pending=round(value - paid, 2),
    )

def update_values_by_registry(reg:models.Registry):
    installment_item = reg.installment_item.first()
    if installment_item:
        update_values(installment_item.installment)

def update_values_by_user(user):
    for installment in user.installment_set.all():
        update_values(installment)