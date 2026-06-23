from rest_framework.decorators import api_view

from services.tools import response_success_error
from services import installments


@api_view(['POST'])
def delete_installment(request, id):
    return response_success_error(*installments.delete(request.user, id))