from django.urls import path
from . import views

app_name = 'gerencia'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
]