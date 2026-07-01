from django.shortcuts import render
# import datetime as dt

def index(request):
    # today = dt.date.today()

    return render(request, 'partials/home/nav-dash/index.html', {
        'cards': request.user.card_set.all(),
        # 'month_year': today.strftime('%Y-%m'),
    })