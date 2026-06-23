from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('nav-regs', views.nav_regs),
    path('reg-form', views.reg_form),
    path('regs-trans-cards', views.reg_trans_cards),
    
]