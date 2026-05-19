from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import views

urlpatterns = [
    # Auth
    path('auth', obtain_auth_token),

    # Registry
    path('getRegistries', views.get_registries),
    path('getRegistry/<int:regid>', views.get_registry),
    path('addRegistry', views.add_registry),
]