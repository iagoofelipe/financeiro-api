from django.urls import path

from .views import home
from .views import navregs

urlpatterns = [
    path('', home.index),
    path('nav-reg', navregs.index),
    path('nav-reg/form', navregs.form),
    path('nav-reg/trans-cards', navregs.trans_cards),
    
]