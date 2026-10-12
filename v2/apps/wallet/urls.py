from django.urls import path
from . import views

urlpatterns = [
  path('create', views.create),
  path('all', views.get_all),
  path('<str:id>', views.get_by_id),
  path('<str:id>/update', views.update),
  path('<str:id>/delete', views.delete),
]