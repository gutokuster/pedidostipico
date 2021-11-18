from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('logar/', views.logar, name='logar'),

    # Buffet
    path('buffet/', views.buffet, name='buffet'),
    path('buffet/pedido/', views.criar_pedido, name='criar_pedido'),
    path('buffet/baixar_pedido/<int:pk>', views.baixar_pedido, name='baixar_pedido'),
    path('buffet/cancelar_pedido/', views.cancelar_pedido, name='cancelar_pedido'),
    # Cozinha
    path('cozinha_quente/', views.cozinha_quente, name='cozinha_quente'),
    path('cozinha_fria/', views.cozinha_fria, name='cozinha_fria'),
    path('buffet/liberar_pedido/<int:pk>', views.liberar_pedido, name='liberar_pedido'),
    # Enquetes
    path('enquete_clientes/', views.enquete_clientes, name='enquete_clientes'),
    path('enquete_clientes/salvar', views.salvar_enquete_clientes, name='salvar_enquete_clientes'),
    path('enquete_funcionarios/', views.enquete_funcionarios, name='enquete_funcionarios'),
    ]