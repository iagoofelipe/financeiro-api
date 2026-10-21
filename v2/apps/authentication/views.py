from http import HTTPStatus
import json

from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny

from django.http import HttpRequest, JsonResponse, HttpResponse
from django.contrib import auth as django_auth
from django.contrib.auth.models import User
from django.db.models import Q

@api_view(["POST"])
@permission_classes([AllowAny])
def create(request:HttpRequest):
    data = json.loads(request.body)

    try:
        if User.objects.filter(Q(username=data['username']) | Q(email=data['email'])).count():
            return JsonResponse({'detail':'já existe um usuário cadastrado com os dados fornecidos'}, status=HTTPStatus.BAD_REQUEST)

        User.objects.create_user(
            username=data['username'],
            password=data['password'],
            email=data['email'],
            first_name=data['firstName'],
            last_name=data['lastName'],
        ).save()
    except KeyError:
        return JsonResponse({'detail':'preencha todos os campos obrigatórios'}, status=HTTPStatus.BAD_REQUEST)
    return HttpResponse()

@api_view(["GET"])
def get(request:HttpRequest):
    if not request.user.is_authenticated:
        response = JsonResponse({'detail':'usuário não autenticado'}, status=HTTPStatus.UNAUTHORIZED)
    else:
        response = JsonResponse({
            'id': request.user.id,
            'username': request.user.username,
            'email': request.user.email,
            'firstName': request.user.first_name,
            'lastName': request.user.last_name,
        })
        
    return response

@api_view(["POST"])
def update(request:HttpRequest):
    params = json.loads(request.body)
    user = User.objects.filter(id=request.user.id).first()

    if user is None:
        return JsonResponse({'detail':'usuário não autenticado'}, status=HTTPStatus.UNAUTHORIZED)

    data = {}
    for request_field, model_field in (
        ('firstName', 'first_name'),
        ('lastName', 'last_name'),
        ('email', 'email'),
    ):
        if request_field in params:
            data[model_field] = params[request_field]

    for field, value in data.items():
        setattr(user, field, value)

    if 'password' in params:
        user.set_password(params['password'])
        Token.objects.filter(user=user).delete()

    if data or 'password' in params:
        user.save()

    return HttpResponse()

@api_view(["POST"])
def delete(request:HttpRequest):
    try:
        User.objects.get(id=request.user.id).delete()
        return HttpResponse()
    
    except User.DoesNotExist:
        return JsonResponse({'detail':'usuário não encontrado'}, status=HTTPStatus.NOT_FOUND)

@api_view(["POST"])
@permission_classes([AllowAny])
def generate_token(request:HttpRequest):
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return JsonResponse({'detail':'Parâmetros username e password necessários!'}, status=HTTPStatus.BAD_REQUEST)
    
    user = django_auth.authenticate(request, username=username, password=password)
    
    if user is None:
        return JsonResponse({'detail':'Usuário ou senha incorretos!'}, status=HTTPStatus.BAD_REQUEST)

    django_auth.login(request, user) 
    token, created = Token.objects.get_or_create(user=user)

    return JsonResponse({'token': token.key})

@api_view(['GET'])
def logout(request):
    django_auth.logout(request)
    return HttpResponse()
