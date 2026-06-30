from django.urls import path
from django.http import HttpResponseBadRequest
from django.shortcuts import render
from rest_framework.authtoken.views import obtain_auth_token

from .views import account, card, invoice, installment, registry, responsable, statistics

def tests(r):
    template_name = r.GET.get('template')
    if template_name is None:
        return HttpResponseBadRequest('"template" parameter must be provided')
    
    return render(r, f'tests/{template_name}.html')

urlpatterns = [
    # Tests Templates
    path('test', tests),

    # Account
    path('auth', obtain_auth_token),
    path('createAccount', account.create_account),
    path('deleteAccount', account.delete_account),
    path('user', account.get_user),

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

    # Statistics
    path('valuesByCategory', statistics.get_values_by_category),
    path('balance', statistics.get_balance),
]