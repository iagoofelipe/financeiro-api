from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('auth', views.auth),
    path('logout', views.logout),
    path('create-account', views.create_account),
]