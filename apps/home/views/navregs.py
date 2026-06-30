from django.shortcuts import render
from django.http import HttpResponseForbidden, HttpResponseBadRequest
from uuid import uuid4
import datetime as dt

from apps.api import models
from services import registry
from services.tools import format_coin, months_with_current

def index(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden()
    
    if 'date_ref' in request.GET:
        try:
            date = dt.date.strptime(request.GET['date_ref'], '%Y-%m-01')
        except ValueError:
            return HttpResponseBadRequest('o parâmetro date_ref deve seguir o padrão AAAA-MM-01')
    
    else:
        date = dt.date.today()
    
    return render(request, 'partials/home/nav-regs/index.html', {
        'cards': models.Card.objects.filter(user=request.user),
        'current_year': date.year,
        'date_formatted': date.strftime('%B %Y'),
        'months': months_with_current(date),
    })

def trans_cards(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden()
    
    *_, regs = registry.get_by_filters(request.user, **request.GET.dict())
    transactions_by_responsable = {}

    for reg in regs:
        if reg.responsable not in transactions_by_responsable:
            transactions_by_responsable[reg.responsable] = {
                'container_id': str(uuid4()),
                'title': reg.responsable.name if reg.responsable else 'Pessoais',
                'sum_inputs': 0,
                'sum_outputs': 0,
                'values': {
                    'Entradas': [],
                    'Saídas': [],
                },
            }
        
        obj = transactions_by_responsable[reg.responsable]
        num_status = f'num_{reg.status}'
        if num_status not in obj:
            obj[num_status] = 0

        obj['sum_inputs' if reg.type_in else 'sum_outputs'] += reg.value
        obj[num_status] += 1
        obj['values']['Entradas' if reg.type_in else 'Saídas'].append(reg.to_dto())

    # formatando dados para exibição
    sum_inputs = 0
    sum_outputs = 0
    for v in transactions_by_responsable.values():
        sum_inputs += v['sum_inputs']
        v['sum_inputs'] = format_coin(v['sum_inputs'])

        sum_outputs += v['sum_outputs']
        v['sum_outputs'] = format_coin(v['sum_outputs'])

        for status, text in {'LATE': 'Atrasado', 'PENDING': 'Pendente', 'OK': 'Pago', 'ACCOUNTED': 'Contabilizado'}.items():
            num_status = v.get('num_'+status, 0)
            v[status] = f'{num_status} {text}{'' if num_status == 1 else 's'}' if num_status else ''

    # ordenando por título, fixando Pessoais no topo
    transactions = sorted(transactions_by_responsable.values(), key=lambda t: (t['title'] != 'Pessoais', t['title']))
    
    total_inout = sum_inputs - sum_outputs
    return render(request, 'partials/home/nav-regs/trans-cards.html', {
        'transactions': transactions,
        'sum_inputs': format_coin(sum_inputs),
        'sum_outputs': format_coin(sum_outputs),
        'total_inout': format_coin(total_inout),
        'positive_inout': total_inout >= 0,
    })

def form(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden()

    now = dt.datetime.now()
    mode = request.GET.get('mode', 'NEW')
    reg = None

    if mode in ('EDIT', 'COPY'):
        if 'id' in request.GET:
            reg = models.Registry.objects.filter(id=request.GET['id']).first()

        if not reg:
            return HttpResponseBadRequest('o parâmetro id não corresponde a um registro válido')
        
        if reg.user != request.user:
            return HttpResponseForbidden('acesso negado')

    if mode in ('NEW', 'COPY'):
        title = 'Novo Registro'
    
    elif mode == 'EDIT':
        title = 'Atualização de Registro'

    else:
        return HttpResponseBadRequest('o parâmetro mode deve ser NEW, EDIT ou vazio')
    
    data = {
        'title': title,
        'cards': models.Card.objects.filter(user=request.user),
        'responsables': models.Responsable.objects.filter(user=request.user).order_by('name'),
        'months': months_with_current(now),
        'current_date': now,
        'has_regs': models.Registry.objects.filter(user=request.user).count(),
        'status': {
            'ACCOUNTED': {'text': 'Contabilizado', 'selected': False},
            'OK': {'text': 'Pago', 'selected': False},
            'PENDING': {'text': 'Pendente', 'selected': False},
        },
        'edit_mode': mode == 'EDIT',
        'reg': reg,
        'current_installment': '',
        'num_installments': '',
        'hide_installment_quantity_alert': True,
        'show_installment_updates_alert': False,
        'categories': request.user.registry_set.filter(category__isnull=False).values_list('category', flat=True).distinct(),
    }

    if reg:
        data['status'][reg.status_without_late]['selected'] = True
        data['reg_occurrance'] = reg.occurrance.strftime('%d/%m/%Y %H:%M')
        data['reg_month_number'] = reg.date_ref.strftime('%m')
        
        if installment_item := reg.installment_item.first():
            data['current_installment'] = installment_item.index + 1
            data['num_installments'] = installment_item.installment.num_items
            data['hide_installment_quantity_alert'] = installment_item.index <= 0 or mode == 'EDIT'
            data['show_installment_updates_alert'] = mode == 'EDIT'

    else:
        data['status']['PENDING']['selected'] = True
        data['reg_occurrance'] = now.strftime('%d/%m/%Y %H:%M')
        data['reg_month_number'] = now.strftime('%m')
    
    return render(request, 'partials/home/nav-regs/form.html', data)