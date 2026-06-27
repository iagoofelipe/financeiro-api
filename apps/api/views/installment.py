from rest_framework.decorators import api_view

from services.tools import response_success_error
from services import installment

@api_view(['POST'])
def delete_installment(request, id):
    return response_success_error(*installment.delete(request.user, id))

@api_view(['GET'])
def update_installments(request):
    installment.update_all_values(request.user)
    return response_success_error(200, '')