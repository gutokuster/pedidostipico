from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('buffet/', views.buffet, name='buffet'),
    path('cozinha_quente/', views.cozinha_quente, name='cozinha_quente'),
    path('cozinha_fria/', views.cozinha_fria, name='cozinha_fria'),
    path('login/', views.login, name='login'),
]