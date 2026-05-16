from django.shortcuts import render

def index(request):
    return render(request, 'v2/home.html')

def regs(request):
    return render(request, 'v2/home-regs.html', { 'transactions': {  } })