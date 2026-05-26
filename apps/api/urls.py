from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import views
from .reg import views as reg_views

urlpatterns = [
    # Auth
    path('auth', obtain_auth_token),
    path('createAccount', views.create_account),

    # Registry
    path('getRegistries', reg_views.get_registries),
    path('getRegistry/<int:regid>', reg_views.get_registry),
    path('addRegistry', reg_views.add_registry),
]