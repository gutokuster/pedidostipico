from django.shortcuts import render, HttpResponse

def index(request):
    return render(request, 'core/index.html')

def login(request):
    return render(request, 'core/login.html')

def buffet(request):
    return HttpResponse('Buffet')

def cozinha_quente(request):
    return HttpResponse('Quente')

def cozinha_fria(request):
    return HttpResponse('Fria')

