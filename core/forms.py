from django import forms
from .models import Pedido, Item

class PedidoForm(forms.ModelForm):
    SITUACAO_CHOICES = (
        ('Em Preparo', 'Em Preparo'),
        ('Entregue', 'Entregue'),
        ('Cancelado', 'Cancelado'),
        ('Baixado', 'Baixado'),
        ('Atrasado', 'Atrasado'),
    )
    item = forms.IntegerField(label='Item')
    situacao = forms.ChoiceField(label='Situação', choices=SITUACAO_CHOICES)
    quantidade = forms.IntegerField(label='Quantidade')

    class Meta:
        model = Pedido
        fields = '__all__'

class ItemForm(forms.ModelForm):
    DESTINO_CHOICES = (
        ('Cozinha Fria', 'Cozinha Fria'),
        ('Cozinha Quente', 'Cozinha Quente'),
        ('Sobremesas', 'Sobremesas'),
    )
    nome = forms.CharField(label='Nome', max_length=100)
    tempo_preparo = forms.TimeField(label='Tempo de Preparo')
    ativo = forms.BooleanField(label='Ativo?', required=False)
    diario = forms.BooleanField(label='Cardápio Diário', required=False)
    destino = forms.ChoiceField(label='Cozinha Destino', choices=DESTINO_CHOICES)

    class Meta:
        model = Item
        fields = '__all__'