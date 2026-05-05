from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home-index'),
    path('nav-dash', views.dash, name='nav-dash'),
    path('nav-regs', views.regs, name='nav-regs'),
    path('nav-cards', views.cards, name='nav-cards'),
]