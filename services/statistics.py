from http import HTTPStatus
from django.db.models import Sum, Q
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
    date_ref = dt.date.strptime(params['date_ref'] if 'date_ref' in params else dt.date.today().strftime('%Y-%m-01'), '%Y-%m-%d')
    prev_date = date_ref - relativedelta(months=1)
    condition_filter = Q(done=True) | Q(accounted=True)
    results = models.Registry.objects.filter(user=user).aggregate(
        total_in=Sum('value', filter=Q(date_ref=date_ref, type_in=True)),
        total_out=Sum('value', filter=Q(date_ref=date_ref, type_in=False)),
        prev_month_in=Sum('value', filter=Q(date_ref=prev_date, type_in=True) & condition_filter),
        prev_month_out=Sum('value', filter=Q(date_ref=prev_date, type_in=False) & condition_filter),
        current_balance_in=Sum('value', filter=Q(date_ref__lte=date_ref, type_in=True) & condition_filter),
        current_balance_out=Sum('value', filter=Q(date_ref__lte=date_ref, type_in=False) & condition_filter),
    )


    total_in            = results['total_in'] if results['total_in'] else 0
    total_out           = results['total_out'] if results['total_out'] else 0
    prev_month_in       = results['prev_month_in'] if results['prev_month_in'] else 0
    prev_month_out      = results['prev_month_out'] if results['prev_month_out'] else 0
    total_in_progress   = total_in >= prev_month_in
    current_balance = round((results['current_balance_in'] if results['current_balance_in'] else 0) - (results['current_balance_out'] if results['current_balance_out'] else 0), 2)

    result = {
        'total_in': total_in,
        'total_in_progress': total_in_progress,
        'total_in_progress_description': f'{'+' if total_in_progress else '-'}{(100 * abs(total_in - prev_month_in) / prev_month_in):.2f}% comparado ao mês anterior' if prev_month_in > 0 else '',
        'total_out': total_out,
        'total_out_progress': total_out <= prev_month_out,
        'total_out_progress_description': f'{'+' if total_out >= prev_month_out else '-'}{(100 * abs(total_out - prev_month_out) / prev_month_out):.2f}% comparado ao mês anterior' if prev_month_out > 0 else '',
        'prev_month_in': prev_month_in,
        'prev_month_out': prev_month_out,
        'current_balance': current_balance,
    }

    return 200, '', result