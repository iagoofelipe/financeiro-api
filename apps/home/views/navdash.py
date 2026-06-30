from django.shortcuts import render
import datetime as dt

from services import statistics
from services import invoice
from apps.api import models

def index(request):
    today = dt.date.today()
    statistics_result = statistics.balance(request.user, date_ref=today.strftime('%Y-%m-01'))[2]

    return render(request, 'partials/home/nav-dash/index.html', {
        'value_in': statistics_result['total_in_formatted'],
        'value_out': statistics_result['total_out_formatted'],
        'value_balance': statistics_result['total_balance_formatted'],
        'cards': request.user.card_set.all(),
        'month_year': today.strftime('%Y-%m'),
    })