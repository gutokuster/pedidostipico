from django.shortcuts import render, HttpResponse

def dashboard(request):
    return HttpResponse('Dashboard')
