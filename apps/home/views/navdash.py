from django.shortcuts import render
import datetime as dt

from services.tools import format_coin
from services import statistics
from apps.api import models

def index(request):
    today = dt.date.today()
    statistics_result = statistics.balance(request.user, date_ref=today.strftime('%Y-%m-01'))[2]
    total_in = statistics_result['total_in']
    total_out = statistics_result['total_out']
    value_balance = total_in - total_out

    return render(request, 'partials/home/nav-dash/index.html', {
        'value_in': format_coin(total_in, prefix=None, show_decimal='if_value'),
        'value_out': format_coin(total_out, prefix=None, show_decimal='if_value'),
        'value_balance': format_coin(value_balance, prefix=None, show_decimal='if_value'),
        'cards': models.Card.objects.filter(user=request.user),
        'month_year': today.strftime('%Y-%m'),
    })