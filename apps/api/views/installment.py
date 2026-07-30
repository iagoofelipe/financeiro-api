from django.http import HttpRequest, HttpResponse
from rest_framework.decorators import api_view

from services import installment

@api_view(["POST"])
def update_all(request:HttpRequest):
    installment.update_values_by_user(request.user)
    return HttpResponse()