from django import forms
from .models import Pedido

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