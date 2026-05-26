from django.contrib import auth as django_auth
from django.shortcuts import render, redirect
from django.http import JsonResponse
from http import HTTPStatus
from rest_framework.authtoken.models import Token
import json

def index(request):
    return redirect('/home') if request.user.is_authenticated else render(request, 'login-auth.html')

def auth(request):
    if request.method != 'POST':
        return JsonResponse({'detail': 'POST method only'}, status=HTTPStatus.METHOD_NOT_ALLOWED)
    
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return JsonResponse({"detail": "Parâmetros username e password necessários!"}, status=HTTPStatus.BAD_REQUEST)
    
    user = django_auth.authenticate(request, username=username, password=password)
    
    if user is None:
        return JsonResponse({"detail": "Usuário ou senha incorretos!"}, status=HTTPStatus.BAD_REQUEST)

    django_auth.login(request, user) 
    token, created = Token.objects.get_or_create(user=user)

    return JsonResponse({'success': True, 'token': token.key})

def logout(request):
    django_auth.logout(request)
    return JsonResponse({'success': True})

def create_account(request):
    return render(request, 'login-create-account.html')