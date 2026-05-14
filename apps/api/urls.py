from django.urls import path, include

from . import views

urlpatterns = [
    path('regs/', include('apps.api.regs.urls')),
]