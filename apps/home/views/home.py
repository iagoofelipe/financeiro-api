from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import datetime as dt

@login_required(login_url='/login')
def index(request):
    return render(request, 'home.html', {'user_name': f'{request.user.first_name} {request.user.last_name}', 'month_year': dt.date.today().strftime('%Y-%m')})