from django.shortcuts import render, HttpResponse

def index(request):
    return HttpResponse('Index')

def login(request):
    return HttpResponse('Login')
