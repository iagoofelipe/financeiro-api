from http import HTTPStatus
from django.db.models import Sum
import datetime as dt
from dateutil.relativedelta import relativedelta

from apps.api import models
from services.tools import format_coin

def values_by_category(user, **params):
    date_ref = params.get('date_ref', dt.date.today().strftime('%Y-%m-01'))
    results = {
        'in': [],
        'out': [],
    }

    for result in models.Registry.objects.filter(user=user, date_ref=date_ref).values('category__title', 'type_in').annotate(sum=Sum('value')):
        title = result['category__title']
        results['in' if result['type_in'] else 'out'].append({
            'title': title if title else 'Outros',
            'total': result['sum'],
            'total_formatted': format_coin(result['sum']),
        })

    return results

def balance(user, **params) -> tuple[HTTPStatus, str, None | dict]:
    try:
        date_ref = params.get('date_ref')
        today = dt.date.today()
        date_ref = dt.date.strptime(date_ref, '%Y-%m-01') if date_ref else dt.date(today.year, today.month, 1)

    except ValueError:
        return HTTPStatus.BAD_REQUEST, 'o parâmetro date_ref deve seguir o formato AAAA-MM-01', None
    
    prev_date = date_ref - relativedelta(months=1)
    total_in = models.Registry.objects.filter(user=user, date_ref=date_ref, type_in=True).aggregate(sum=Sum('value'))['sum']
    total_out = models.Registry.objects.filter(user=user, date_ref=date_ref, type_in=False).aggregate(sum=Sum('value'))['sum']
    prev_total_in = models.Registry.objects.filter(user=user, date_ref=prev_date, type_in=True).aggregate(sum=Sum('value'))['sum']
    prev_total_out = models.Registry.objects.filter(user=user, date_ref=prev_date, type_in=False).aggregate(sum=Sum('value'))['sum']

    result = {
        'reference': date_ref.strftime('%Y-%m-%d'),
        'previous_reference': prev_date.strftime('%Y-%m-%d'),
        'total_in': total_in,
        'total_out': total_out,
        'prev_total_in': prev_total_in,
        'prev_total_out': prev_total_out,
    }

    return 200, '', result