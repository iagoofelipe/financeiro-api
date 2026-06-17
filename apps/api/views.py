from django.http import HttpRequest, JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
import json

from services import user
from services.tools import response_success_error

@api_view(["POST"])
@permission_classes([AllowAny])
def create_account(request:HttpRequest):
    return response_success_error(*user.create_user(**json.loads(request.body)))

@api_view(["POST"])
def delete_account(request:HttpRequest):
    return response_success_error(*user.delete_user(request.user))
    