from django.shortcuts import render

def index(request):
    return render(request, 'partials/home/nav-dash/index.html')