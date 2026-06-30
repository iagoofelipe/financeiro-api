from http import HTTPStatus
from django.db.models import Sum
import datetime as dt
from dateutil.relativedelta import relativedelta

from apps.api import models
from services.tools import format_coin

def dto_values_by_category(p:dict=None, **params):
    if p is None: p = params
    elif params: p.update(params)

    return {
        'title': p['category'] if p['category'] else 'Outros',
        'total': round(p['sum'], 2),
        'total_formatted': format_coin(p['sum']),
    }

def values_by_category(user, **params) -> tuple[HTTPStatus, str, dict | None]:
    date_ref = params.get('date_ref', dt.date.today().strftime('%Y-%m-01'))
    try:
        limit = int(params.get('limit', -1))
    except ValueError:
        return HTTPStatus.BAD_REQUEST, 'o parâmetro limit deve ser do tipo inteiro', None
    
    query_in = models.Registry.objects.filter(user=user, date_ref=date_ref, type_in=True).values('category').annotate(sum=Sum('value')).order_by('-sum')
    query_out = models.Registry.objects.filter(user=user, date_ref=date_ref, type_in=False).values('category').annotate(sum=Sum('value')).order_by('-sum')

    results = {
        'in': [],
        'out': [],
    }

    for query, key in ((query_in, 'in'), (query_out, 'out')):
        if 0 < limit < query.__len__():
            vals_category_not_null = query.filter(category__isnull=False)
            val_category_null = query.filter(category__isnull=True).first()
            sum_others = val_category_null['sum'] if val_category_null else 0

            # caso não haja null e a quantidade seja maior que o limite
            decrease_limit = bool(val_category_null or vals_category_not_null.__len__() > limit)
            results[key].extend(map(dto_values_by_category, vals_category_not_null[:limit-decrease_limit]))
                
            # somando valores restantes
            sum_others += sum(v['sum'] for v in vals_category_not_null[limit-decrease_limit:])
            
            if sum_others:
                results[key].append(dto_values_by_category(category='Outros', sum=sum_others))

        else:
            results[key].extend(map(dto_values_by_category, query))

    return 200, '', results

def balance(user, **params) -> tuple[HTTPStatus, str, None | dict]:
    date_ref = params.get('date_ref', dt.date.today().strftime('%Y-%m-01'))
    
    # prev_date = date_ref - relativedelta(months=1)
    total_in = models.Registry.objects.filter(user=user, date_ref=date_ref, type_in=True).aggregate(sum=Sum('value'))['sum']
    total_out = models.Registry.objects.filter(user=user, date_ref=date_ref, type_in=False).aggregate(sum=Sum('value'))['sum']
    # prev_total_in = models.Registry.objects.filter(user=user, date_ref=prev_date, type_in=True).aggregate(sum=Sum('value'))['sum']
    # prev_total_out = models.Registry.objects.filter(user=user, date_ref=prev_date, type_in=False).aggregate(sum=Sum('value'))['sum']
    
    if total_in is None: total_in = 0
    if total_out is None: total_out = 0

    total_balance = round(total_in - total_out, 2)

    result = {
        # 'reference': date_ref.strftime('%Y-%m-%d'),
        # 'previous_reference': prev_date.strftime('%Y-%m-%d'),
        'total_in': total_in,
        'total_in_formatted': format_coin(total_in, prefix=None, show_decimal='if_value'),
        'total_out': total_out,
        'total_out_formatted': format_coin(total_out, prefix=None, show_decimal='if_value'),
        'total_balance': total_balance,
        'total_balance_formatted': format_coin(total_balance, prefix=None, show_decimal='if_value'),
        # 'prev_total_in': prev_total_in,
        # 'prev_total_out': prev_total_out,
    }

    return 200, '', result