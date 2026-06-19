from apps.api import models
from http import HTTPStatus

def get_all(user):
    return models.Responsable.objects.filter(user=user).order_by('name')

def get_by_id(user, id:int) -> tuple[HTTPStatus, str, models.Responsable | None]:
    obj = models.Responsable.objects.filter(id=id).first()
    if not obj:
        return HTTPStatus.NOT_FOUND, 'nenhum dado encontrado para o ID fornecido', None
    
    if obj.user != user:
        return HTTPStatus.METHOD_NOT_ALLOWED, 'permissão de acesso negada', None
    
    return HTTPStatus.OK, '', obj

def create(user, **data) -> tuple[HTTPStatus, str, models.Responsable | None]:
    try:
        obj = models.Responsable(
            name=data['name'],
            user=user,
        )
    except KeyError as e:
        return HTTPStatus.BAD_REQUEST, f'missing required param {e}', None

    obj.save()
    return HTTPStatus.OK, '', obj