from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('nav-regs', views.nav_regs),
    path('new-reg', views.new_reg),
    path('regs-trans-cards', views.reg_trans_cards),
    
]