from django import forms
from .models import Configuracoes

class ConfiguracoesForm(forms.ModelForm):
    taxa_atualizacao = forms.IntegerField(label='Atualização Automática (seg)')

    class Meta:
        model = Configuracoes
        fields = '__all__'