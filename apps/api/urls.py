from django.urls import path, include
from rest_framework.authtoken import views as rest_views

from . import views

urlpatterns = [
    path('regs/', include('apps.api.regs.urls')),
    path('auth/', rest_views.obtain_auth_token),
]