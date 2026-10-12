from django.urls import path

from . import views

urlpatterns = [
  path('createUser', views.create),
  path('getUser', views.get),
  path('updateUser', views.update),
  path('deleteUser', views.delete),
  path('generateToken', views.generate_token),
  path('logout', views.logout),
]