from django.contrib import admin
from .models import Configuracoes

@admin.register(Configuracoes)
class ConfiguracoesAdmin(admin.ModelAdmin):
    list_display = ['id', 'taxa_atualizacao', 'data_atualizacao']