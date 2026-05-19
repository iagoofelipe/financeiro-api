from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda r: redirect('/home')),
    path('admin/', admin.site.urls),
    path('api/', include('apps.api.urls')),
    path('home/', include('apps.home.urls')),
    path('login/', include('apps.login.urls')),
]
