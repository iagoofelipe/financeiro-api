from django.urls import path

from . import views

urlpatterns = [
    path('create', views.create),
    path('getAll', views.get_all),
    path('<str:id>', views.get_by_id),
]