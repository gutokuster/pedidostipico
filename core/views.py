import datetime

from django.shortcuts import render, redirect, get_object_or_404
from .models import Item, PedidoAtrasado, Pedido
from django.db.models import Q


def atualiza_situacao_pedido(pk, hora_atual):
    pedido = get_object_or_404(Pedido, pk=pk)
    if pedido.limite_entrega < hora_atual and pedido.situacao != 'Atrasado':
        pedido.situacao = 'Atrasado'
        pedido_atrasado = PedidoAtrasado()
        pedido_atrasado.pedido_id = pedido.pk
        pedido.save()
        pedido_atrasado.save()

def index(request):
    contexto = {
        'titulo_pagina': 'Sistema de Pedidos'
    }
    return render(request, 'core/index.html', contexto)


def login(request):
    return render(request, 'core/login.html')

'''
Funções Buffet
'''
def buffet(request):
    pedidos = Pedido.objects.filter(Q(situacao='Em Preparo') | Q(situacao='Atrasado') | Q(situacao='Entregue'))
    hora_atual = datetime.datetime.now().time()
    print(type(hora_atual))
    if pedidos.count() > 0:
        for pedido in pedidos:
            atualiza_situacao_pedido(pedido.id, hora_atual)

    contexto = {
        'hora_atual': hora_atual,
        'titulo_pagina': 'Pedidos Buffet',
        'itens': Item.objects.all(),
        'pedidos': pedidos,
    }
    return render(request, 'core/buffet.html', contexto)


def criar_pedido(request):
    pk = request.GET['pk']
    quantidade = request.GET['quantidade']
    item = get_object_or_404(Item, pk=pk)
    pedido = Pedido(item=item, quantidade=quantidade)
    tempoPreparo = str(item.tempo_preparo)
    horas = tempoPreparo[0:2]
    minutos = tempoPreparo[3:5]
    pedido.limite_entrega = datetime.datetime.now() + datetime.timedelta(minutes=int(minutos))
    print('Limite: ', pedido.limite_entrega)
    pedido.save()
    return redirect('core:buffet')

def baixar_pedido(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
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
    contexto = {
        'titulo_pagina': 'Pedido Cozinha Quente',
        'pedidos': pedidos,
        'itens': itens,
        'hora_atual': hora_atual,
    #    'tempo_restante': tempo_restante,
    }
    return render(request, 'core/cozinha.html', contexto)


def cozinha_fria(request):
    pedidos = Pedido.objects.filter(Q(situacao='Em Preparo') | Q(situacao='Atrasado'))
    itens = Item.objects.filter(Q(destino='Cozinha Fria') | Q(destino='Sobremesas'))
    hora_atual = datetime.datetime.now().time()
    contexto = {
        'titulo_pagina': 'Pedido Cozinha Fria',
        'pedidos': pedidos,
        'itens': itens,
        'hora_atual': hora_atual,
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
TODO: Incluir 'tempo restante' na cozinha
DONE: Alterar cor da linha dos itens atrasado na cozinha
TODO: AJAX para atualizar as telas (15 seg)
DONE: Cancelar pedido
TODO: Cardápio com itens fixos + variaveis
'''