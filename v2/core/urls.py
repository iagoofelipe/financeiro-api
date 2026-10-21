from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('apps.authentication.urls')),
    path('wallets/', include('apps.wallet.urls')),
    path('registries/', include('apps.registry.urls')),
]
