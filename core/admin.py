from django.contrib import admin
from .models import Pedido, Item, PedidoAtrasado

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ['item', 'quantidade', 'limite_entrega', 'situacao', 'hora_pedido', 'hora_situacao']

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['nome', 'tempo_preparo', 'destino', 'ativo', 'diario', 'data_cadastro', 'data_atualizacao']

@admin.register(PedidoAtrasado)
class PedidoAtrasadoAdmin(admin.ModelAdmin):
    list_display = ['pedido', 'data_atraso', 'tempo_atraso']
