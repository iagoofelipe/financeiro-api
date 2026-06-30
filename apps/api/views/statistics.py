from rest_framework.decorators import api_view

from services.tools import response_obj_or_error
from services import statistics

@api_view(["GET"])
def get_values_by_category(request):
    return response_obj_or_error(200, '', statistics.values_by_category(request.user, **request.GET.dict()), safe=False)

@api_view(["GET"])
def get_balance(r):
    return response_obj_or_error(*statistics.balance(r.user, **r.GET.dict()))