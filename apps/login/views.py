from django.contrib.auth import authenticate as django_authenticate, login as django_login
from django.shortcuts import render, redirect
from django.http import JsonResponse
from http import HTTPStatus
from rest_framework.authtoken.models import Token

def index(request):
    return redirect('/home') if request.user.is_authenticated else render(request, 'login.html')

def auth(request):
    if request.method != 'POST':
        return JsonResponse({'msg': 'POST method only'}, status=HTTPStatus.METHOD_NOT_ALLOWED)
    
    username = request.POST.get('username')
    password = request.POST.get('password')
    
    user = django_authenticate(request, username=username, password=password)
    
    if user is None:
        return JsonResponse({"msg": "Usuário ou senha incorretos!", 'success': False}, status=400)

    django_login(request, user) 
    token, created = Token.objects.get_or_create(user=user)

    return JsonResponse({'success': True, 'token': token.key})
