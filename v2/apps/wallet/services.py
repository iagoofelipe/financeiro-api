from .models import Wallet
from http import HTTPStatus

def get_wallet_by_id(user, id) -> tuple[HTTPStatus, str, Wallet|None]:
    wallet = Wallet.objects.filter(id=id).first()

    if not wallet:
        return HTTPStatus.NOT_FOUND, 'dados não encontrados', None
    
    if user != wallet.user:
        return HTTPStatus.UNAUTHORIZED, 'permissão de acesso negada', None
    
    return 200, '', wallet