from apps.api import models
from http import HTTPStatus
from django.db.models import Sum

def delete(user, id) -> tuple[HTTPStatus, str]:
    installment = models.Installment.objects.filter(id=id).first()
    if not installment:
        return HTTPStatus.NOT_FOUND, 'nenhum valor encontrado para o id fornecido'
    
    if installment.user != user:
        return HTTPStatus.FORBIDDEN, 'permissão de acesso negada'
    
    installment.delete()
    return HTTPStatus.OK, ''

def update_values(installment:models.Installment):
    value = installment.items.aggregate(value=Sum('registry__value'))['value']
    paid = installment.items.filter(registry__done=True).aggregate(paid=Sum('registry__value'))['paid']
    
    if paid is None:
        paid = 0

    models.Installment.objects.filter(id=installment.id).update(
        value=value,
        paid=paid,
        pending=value - paid
    )

def update_all_values(user):
    for installment in models.Installment.objects.filter(user=user).all():
        update_values(installment)