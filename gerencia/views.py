from django.shortcuts import render, HttpResponse

def dashboard(request):
    return render(request, 'gerencia/dashboard.html')
