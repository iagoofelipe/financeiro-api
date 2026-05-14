from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index),
    path('addRegistry', views.add_registry),
    path('<int:reg_id>', views.get_registry),
]