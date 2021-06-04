from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from core.forms import ItemForm
from core.models import Item, PedidoAtrasado, Pedido

@login_required
def dashboard(request):
    contexto = {
        'titulo_pagina': 'Gestão de Pedidos',
        'usuario': User,
        'total_pedidos': Pedido.objects.all().count(),
        'total_pedidos_cancelados': Pedido.objects.filter(situacao='Cancelado').count(),
        'total_pedidos_atrasados': PedidoAtrasado.objects.all().count(),
    }
    return render(request, 'gerencia/dashboard.html', contexto)

@login_required
def sair(request):
    logout(request)
    return render(request, 'core/index.html')

@login_required
def cadastrar_item(request):
    form = ItemForm(request.POST or None)
    if str(request.method) == 'POST':
        if form.is_valid():
            form.save()
            return redirect('gerencia:listar_itens')
    contexto = {
        'titulo_pagina': 'Cadastro de Itens',
        'titulo': 'Inclusão de novo item',
        'form': form,
    }
    return render(request, 'gerencia/cadastro_item.html', contexto)

@login_required
def listar_itens(request):
    itens = Item.objects.all()
    contexto = {
        'titulo_pagina': 'Relação de Itens',
        'titulo': 'Relação de Itens Cadastrados',
        'itens': itens,
    }
    return render(request, 'gerencia/itens.html', contexto)

@login_required
def excluir_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if str(request.method) == 'POST':
        item.delete()
        return redirect('gerencia:listar_itens')
    return render(request, 'gerencia/itens.html')

@login_required
def atualizar_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    form = ItemForm(request.POST or None, instance=item)
    if str(request.method) == 'POST':
        if form.is_valid():
            form.save()
            return redirect('gerencia:listar_itens')
    contexto = {
        'form': form,
        'id_item': pk,
    }
    return render(request, 'gerencia/atualiza_item.html', contexto)

