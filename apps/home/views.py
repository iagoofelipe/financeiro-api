from django.shortcuts import render, redirect

def index(request):
    return render(request, 'home.html')

def dash(request):
    return render(request, 'home-dash.html')

def regs(request):
    return render(request, 'home-regs.html')

def cards(request):
    return render(request, 'home-cards.html')