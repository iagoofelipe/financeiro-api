from http import HTTPStatus
from django.contrib.auth.models import User
from django.db.models import Q


def create_user(**data) -> tuple[HTTPStatus, str, User | None]:
    """ cria um novo usuário """
    fields = {'username', 'password', 'email', 'first_name', 'last_name'}
    fields_missing = fields - set(data)

    if fields_missing:
        return HTTPStatus.BAD_REQUEST, f"os campos '{"','".join(fields_missing)}' não foram fornecidos", None
    
    if User.objects.filter(Q(username=data['username']) | Q(email=data['email'])).count():
        return HTTPStatus.BAD_REQUEST, 'já existe um usuário cadastrado com os dados fornecidos', None

    user = User.objects.create_user(**{ f: data[f] for f in fields })
    user.save()

    return HTTPStatus.OK, '', user

def delete_user(user:User):
    try:
        User.objects.get(id=user.id).delete()
        return HTTPStatus.OK, '', True
    
    except User.DoesNotExist:
        return HTTPStatus.NOT_FOUND, 'usuário não encontrado', False