from django.contrib import admin
from .models import Pedido, Item, PedidoAtrasado, EnqueteClientes, EnqueteFuncionarios

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ['item', 'quantidade', 'limite_entrega', 'situacao', 'hora_pedido', 'hora_situacao']

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['nome', 'tempo_preparo', 'destino', 'ativo', 'diario', 'data_cadastro', 'data_atualizacao']

@admin.register(PedidoAtrasado)
class PedidoAtrasadoAdmin(admin.ModelAdmin):
    list_display = ['pedido', 'data_atraso', 'tempo_atraso']

@admin.register(EnqueteFuncionarios)
class EnqueteFuncionariosAdmin(admin.ModelAdmin):
   list_display = ['resp1', 'resp2', 'resp3']

@admin.register(EnqueteClientes)
class EnqueteClientesAdmin(admin.ModelAdmin):
   list_display = ['id', 'date', 'resp1', 'resp2', 'resp3']