from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotAllowed
from uuid import uuid4

from services import registries
from services.tools import format_coin

@login_required(login_url='/login')
def index(request):
    return render(request, 'home.html', {'user_name': f'{request.user.first_name} {request.user.last_name}'})

def nav_regs(request):
    if not request.user.is_authenticated:
        return HttpResponseNotAllowed()
    
    return render(request, 'partials/home-regs.html', {
        'date_references': registries.get_date_references(request.user),
    })

def reg_trans_cards(request):
    if not request.user.is_authenticated:
        return HttpResponseNotAllowed()
    
    *_, regs = registries.get_by_filters(request.user, date_ref=request.GET.get('date_ref'))
    transactions_by_responsable = {}

    for reg in regs:
        if reg.responsable not in transactions_by_responsable:
            transactions_by_responsable[reg.responsable] = {
                'container_id': str(uuid4()),
                'title': reg.responsable.name if reg.responsable else 'Pessoais',
                'sum_inputs': 0,
                'sum_outputs': 0,
                'num_LATE': 0,
                'num_PENDING': 0,
                'num_OK': 0,
                'values': {
                    'Entradas': [],
                    'Saídas': [],
                },
            }
        
        obj = transactions_by_responsable[reg.responsable]
        obj['sum_inputs' if reg.type_in else 'sum_outputs'] += reg.value
        obj[f'num_{reg.STATUS[reg.status]}'] += 1
        obj['values']['Entradas' if reg.type_in else 'Saídas'].append(reg.to_dto())

    # formatando dados para exibição
    sum_inputs = 0
    sum_outputs = 0
    for v in transactions_by_responsable.values():
        sum_inputs += v['sum_inputs']
        v['sum_inputs'] = format_coin(v['sum_inputs'])

        sum_outputs += v['sum_outputs']
        v['sum_outputs'] = format_coin(v['sum_outputs'])

        for status, text in {'LATE': 'Atrasado', 'PENDING': 'Pendente', 'OK': 'Contabilizado'}.items():
            num_status = v['num_'+status]
            v[status] = f'{num_status} {text}{'' if num_status == 1 else 's'}' if num_status else ''

    # ordenando por título, fixando Pessoais no topo
    transactions = sorted(transactions_by_responsable.values(), key=lambda t: (t['title'] != 'Pessoais', t['title']))

    data = {
        'transactions': transactions,
        'sum_inputs': format_coin(sum_inputs),
        'sum_outputs': format_coin(sum_outputs),
        'date_references': registries.get_date_references(request.user),
    }

    return render(request, 'partials/home-regs-trans-cards.html', data)

def new_reg(request):
    default = dict(id=0, title='Jan 26')
    return render(request, 'partials/new-reg.html', {
        'invoices': [
            default,
            dict(id=1, title='Fev 26'),
            dict(id=3, title='Mar 26'),
        ],
        'default_invoice': default,
    })