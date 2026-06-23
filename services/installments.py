from apps.api import models
from http import HTTPStatus

def delete(user, id) -> tuple[HTTPStatus, str]:
    installment = models.Installment.objects.filter(id=id).first()
    if not installment:
        return HTTPStatus.NOT_FOUND, 'nenhum valor encontrado para o id fornecido'
    
    if installment.user != user:
        return HTTPStatus.FORBIDDEN, 'permissão de acesso negada'
    
    installment.delete()
    return HTTPStatus.OK, ''
