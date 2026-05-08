"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect, render
from django.http import HttpRequest, HttpResponseBadRequest, HttpResponseNotFound
from django.template.exceptions import TemplateDoesNotExist

def templates(request:HttpRequest):
    data = request.GET.dict()
    try:
        template = data.pop('template')
        return render(request, template, data)
    except KeyError:
        return HttpResponseBadRequest('parameter template required')
    except TemplateDoesNotExist:
        return HttpResponseNotFound(f'template "{template}" not found')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda r: redirect('/home')),
    path('templates/', templates, name='templates'),
    path('home/', include('apps.home.urls')),
    path('test/', lambda r: render(r, 'home/regs/index.html'))
]
