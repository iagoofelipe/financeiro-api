from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import views
from .reg import views as reg_views
from .card import views as card_views
from .invoice import views as invoice_views
from .responsable import views as responsable_views
from .installment import views as installment_views

urlpatterns = [
    # Account
    path('auth', obtain_auth_token),
    path('createAccount', views.create_account),
    path('deleteAccount', views.delete_account),

    # Card
    path('getCards', card_views.get_cards),
    path('getCard/<int:cardid>', card_views.get_card),
    path('addCard', card_views.add_card),

    # Invoice
    path('getInvoices', invoice_views.get_invoices),
    path('getInvoice/<int:id>', invoice_views.get_invoice),

    # Installment
    path('deleteInstallment/<int:id>', installment_views.delete_installment),
    path('updateInstallments', installment_views.update_installments),

    # Registry
    path('getRegistries', reg_views.get_registries),
    path('getRegistry/<int:regid>', reg_views.get_registry),
    path('addRegistry', reg_views.add_registry),
    path('getRegistryDateReferences', reg_views.get_reg_date_references),
    path('hasRegistries', reg_views.has_registries),
    path('deleteRegistry/<int:regid>', reg_views.delete_registry),
    path('updateRegistry', reg_views.update_registry),

    # Responsable
    path('getResponsables', responsable_views.get_responsables),
    path('getResponsable/<int:id>', responsable_views.get_responsable),
    path('addResponsable', responsable_views.add_responsable),
]