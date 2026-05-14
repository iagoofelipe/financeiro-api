from django.http import HttpResponse, JsonResponse, HttpRequest, HttpResponseBadRequest, HttpResponseNotAllowed
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
import json

from . import models
from tools.utils import make_param_filters

GET_REGISTRIES_KEY_FILTERS = make_param_filters('int', 'value') | make_param_filters('str', 'title') | {'status', 'type_in'}

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def index(request:HttpRequest):

    # adicionando filtros
    filters = { k: request.GET[k] for k in set(request.GET) & GET_REGISTRIES_KEY_FILTERS }

    if 'status' in filters:
        filters['status'] = filters['status'][0] # necessário pois a base armazena o STATUS apenas como a primeira letra

    regs = models.Registry.objects.filter(user=request.user, **filters).all()
    return JsonResponse([ o.to_dto() for o in regs ], safe=False)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_registry(request:HttpRequest, reg_id:int):
    reg = models.Registry.objects.filter(id=reg_id).first()
    if not reg:
        return HttpResponseBadRequest(json.dumps({'msg': 'nenhum dado encontrado para o id fornecido'}))
    return HttpResponseNotAllowed() if reg.user != request.user else JsonResponse(reg.to_dto())

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_registry(request:HttpRequest):
    data = json.loads(request.body)
    invoice = None
    responsable = None

    if 'invoice_id' in data:
        invoice = models.Invoice.objects.filter(id=data['invoice_id']).first()
        
        if not invoice:
            return HttpResponseBadRequest(json.dumps({'msg': 'nenhuma fatura válida encontrada para o ID fornecido'}))

        elif invoice.card.user != request.user:
            return HttpResponseNotAllowed()
    
    if 'responsable_id' in data:
        responsable = models.Responsable.objects.filter(id=data['responsable_id']).first()
        
        if not responsable:
            return HttpResponseBadRequest(json.dumps({'msg': 'nenhum responsável encontrado para o ID fornecido'})) 
        
        elif responsable.user != request.user:
            return HttpResponseNotAllowed()

    try:
        reg = models.Registry(
            title=data['title'],
            value=data['value'],
            status=data['status'][0],
            occurrance=data['occurrance'],
            description=data.get('description'),
            date_ref=f'{data['ref_year']}-{str(data['ref_month']).zfill(2)}-01',
            type_in=data['type_in'],
            user=request.user,
            invoice=invoice,
            responsable=responsable,
        )
    except KeyError as e:
        return HttpResponseBadRequest(json.dumps({'msg': f'missing required param {e}'}))

    reg.save()
    
    return JsonResponse(models.Registry.objects.get(id=reg.id).to_dto())