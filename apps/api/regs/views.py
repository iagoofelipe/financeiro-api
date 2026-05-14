from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods

from . import models

def index(r):
    return JsonResponse([ o.to_dto() for o in models.Registry.objects.all() ], safe=False)


@require_http_methods(["POST"])
def add_registry(r):
    return HttpResponse()