import datetime

from django.shortcuts import render, redirect, get_object_or_404
from .models import Item, PedidoAtrasado, Pedido
from gerencia.models import Configuracoes
from django.db.models import Q
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm


def atualiza_situacao_pedido(pk, hora_atual):
    pedido = get_object_or_404(Pedido, pk=pk)
    if str(pedido.tempo_restante) == '00:00:00' and pedido.situacao == 'Em Preparo':
        pedido.situacao = 'Atrasado'
        pedido_atrasado = PedidoAtrasado()
        pedido_atrasado.pedido_id = pedido.pk
        pedido.save()
        pedido_atrasado.save()


def atualiza_tempo_restante(pk, hora_atual):
    pedido = get_object_or_404(Pedido, pk=pk)
    if datetime.datetime.now().time() > pedido.limite_entrega:
        pedido.tempo_restante = datetime.time(0, 0, 0)
        pedido.situacao = 'Atrasado'
    else:
        hora = pedido.limite_entrega.hour - hora_atual.hour
        minuto = pedido.limite_entrega.minute - hora_atual.minute
        pedido.tempo_restante = datetime.time(hora, minuto, 0)

    pedido.save()


def index(request):
    contexto = {
        'titulo_pagina': 'Sistema de Pedidos'
    }
    return render(request, 'core/index.html', contexto)


def logar(request):
    if request.method == 'POST':
        print(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        usuario = authenticate(request, username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect('gerencia:dashboard')
        else:
            form_login = AuthenticationForm()
    else:
        form_login = AuthenticationForm()
    return render(request, 'core/login.html', {'form_login': form_login})


'''
Funções Buffet
'''
def buffet(request):
    pedidos = Pedido.objects.filter(Q(situacao='Em Preparo') | Q(situacao='Atrasado') | Q(situacao='Entregue'))
    hora_atual = datetime.datetime.now().time()
    lista_pedidos = []
    for pedido in pedidos:
        lista_pedidos.append(pedido.item_id)
    contexto = {
        'titulo_pagina': 'Pedidos Buffet',
        'itens': Item.objects.filter(ativo=True).order_by('nome'),
        'pedidos': pedidos,
        'lista_pedidos': lista_pedidos,
        'configuracao': get_object_or_404(Configuracoes, pk=1),
    }
    return render(request, 'core/buffet.html', contexto)


def criar_pedido(request):
    pk = request.GET['pk']
    quantidade = request.GET['quantidade']
    item = get_object_or_404(Item, pk=pk)
    pedido = Pedido(item=item, quantidade=quantidade)
    minutos = str(item.tempo_preparo)
    pedido.limite_entrega = datetime.datetime.now() + datetime.timedelta(minutes=int(minutos))
    pedido.hora_entrega = pedido.limite_entrega
    pedido.save()
    return redirect('core:buffet')


def baixar_pedido(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    if pedido.situacao == 'Entregue':
        pedido.situacao = 'Baixado'
        pedido.save()
    return redirect('core:buffet')


def cancelar_pedido(request):
    pk = request.GET['pk']
    pedido = get_object_or_404(Pedido, pk=pk)
    pedido.situacao = 'Cancelado'
    pedido.save()
    return redirect('core:buffet')


'''
Funções Cozinha
'''
def cozinha_quente(request):
    pedidos = Pedido.objects.filter(Q(situacao='Em Preparo') | Q(situacao='Atrasado'))
    hora_atual = datetime.datetime.now().time()
    itens = Item.objects.filter(destino='Cozinha Quente')
    if pedidos.count() > 0:
        for pedido in pedidos:
            atualiza_tempo_restante(pedido.id, hora_atual)
    contexto = {
        'titulo_pagina': 'Pedidos Cozinha Quente',
        'pedidos': pedidos,
        'itens': itens,
        'configuracao': get_object_or_404(Configuracoes, pk=1),
    }
    return render(request, 'core/cozinha.html', contexto)


def cozinha_fria(request):
    pedidos = Pedido.objects.filter(Q(situacao='Em Preparo') | Q(situacao='Atrasado'))
    itens = Item.objects.filter(Q(destino='Cozinha Fria') | Q(destino='Sobremesas'))
    hora_atual = datetime.datetime.now().time()
    #tempo_restante = hora_atual - pedido.limite_entrega
    if pedidos.count() > 0:
        for pedido in pedidos:
            atualiza_tempo_restante(pedido.id, hora_atual)

    contexto = {
        'titulo_pagina': 'Pedidos Cozinha Fria',
        'pedidos': pedidos,
        'itens': itens,
        'configuracao': get_object_or_404(Configuracoes, pk=1),
    }
    return render(request, 'core/cozinha.html', contexto)


def liberar_pedido(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    item = get_object_or_404(Item, pk=pedido.item_id)
    if pedido.situacao == 'Atrasado':
        hora = int(pedido.limite_entrega.strftime('%H:%M')[0:2])
        minuto = int(pedido.limite_entrega.strftime('%H:%M')[3:5])
        tempo_atraso = (datetime.datetime.today() - datetime.timedelta(hours=hora, minutes=minuto)).strftime('%H:%M:%S')
        pedido_atrasado = PedidoAtrasado(pedido=pedido, tempo_atraso=tempo_atraso)
        pedido_atrasado.save()
    pedido.situacao = 'Entregue'
    pedido.save()
    if item.destino == 'Cozinha Quente':
        return redirect('core:cozinha_quente')
    else:
        return redirect('core:cozinha_fria')

'''
DONE: Incluir 'tempo restante' na cozinha
DONE: Alterar cor da linha dos itens atrasado na cozinha
DONE: JS para atualizar as telas (via gerencia/configuração)
DONE: Cancelar pedido
CANC: Cardápio com itens fixos + variaveis

TODO: Permitir incluir novos pedidos com itens em aberto - Usar JS, perguntar se deseja baixar o pedido ou incluir um novo
TODO: Relatórios gerenciais
'''
