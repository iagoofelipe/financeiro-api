from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.decorators import api_view

from .views import account, card, invoice, installment, registry, responsable

from django.http import HttpResponse
from . import models

@api_view(['GET'])
def test(r):
    print(models.Registry._meta.get_field('done').get_default())
    return HttpResponse()

urlpatterns = [
    path('test', test),

    # Account
    path('auth', obtain_auth_token),
    path('createAccount', account.create_account),
    path('deleteAccount', account.delete_account),

    # Card
    path('getCards', card.get_cards),
    path('getCard/<int:cardid>', card.get_card),
    path('addCard', card.add_card),

    # Invoice
    path('getInvoices', invoice.get_invoices),
    path('getInvoice/<int:id>', invoice.get_invoice),
    path('getInvoiceByCard', invoice.get_invoice_by_card),

    # Installment
    path('deleteInstallment/<int:id>', installment.delete_installment),
    path('updateInstallments', installment.update_installments),

    # Registry
    path('getRegistries', registry.get_registries),
    path('getRegistry/<int:regid>', registry.get_registry),
    path('addRegistry', registry.add_registry),
    path('getRegistryDateReferences', registry.get_reg_date_references),
    path('hasRegistries', registry.has_registries),
    path('deleteRegistry/<int:regid>', registry.delete_registry),
    path('updateRegistry', registry.update_registry),

    # Responsable
    path('getResponsables', responsable.get_responsables),
    path('getResponsable/<int:id>', responsable.get_responsable),
    path('addResponsable', responsable.add_responsable),
]