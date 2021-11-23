from django.shortcuts import render, redirect, get_object_or_404
from .models import Item, PedidoAtrasado, Pedido, EnqueteClientes, EnqueteFuncionarios
from gerencia.models import Configuracoes
from django.db.models import Q
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from datetime import datetime, timedelta, time

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
    if datetime.now().time() > pedido.limite_entrega:
        pedido.tempo_restante = time(0, 0, 0)
        pedido.situacao = 'Atrasado'
    else:
        hora = pedido.limite_entrega.hour - hora_atual.hour
        minuto = pedido.limite_entrega.minute - hora_atual.minute
        pedido.tempo_restante = time(hora, minuto, 0)

    pedido.save()


def index(request):
    contexto = {
        'titulo_pagina': 'Sistema de Pedidos'
    }
    return render(request, 'core/index.html', contexto)


def logar(request):
    if request.method == 'POST':
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
    hora_atual = datetime.now().time()
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
    pedido.limite_entrega = datetime.now() + timedelta(minutes=int(minutos))
    pedido.hora_entrega = pedido.limite_entrega
    pedido.save()
    return redirect('core:buffet')


def baixar_pedido(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    if pedido.situacao == 'Entregue':
        pedido.situacao = 'Baixado'
        pedido.save()
    return redirect('core:buffet')


def cancelar_pedido(request, pk):
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
    hora_atual = datetime.now().time()
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
    hora_atual = datetime.now().time()
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
        tempo_atraso = (datetime.today() - timedelta(hours=hora, minutes=minuto)).strftime('%H:%M:%S')
        pedido_atrasado = PedidoAtrasado(pedido=pedido, tempo_atraso=tempo_atraso)
        pedido_atrasado.save()
    pedido.situacao = 'Entregue'
    pedido.save()
    if item.destino == 'Cozinha Quente':
        return redirect('core:cozinha_quente')
    else:
        return redirect('core:cozinha_fria')


'''
Funções Enquete Funcionários
'''
def enquete_funcionarios(request):
    contexto = {
        'titulo_pagina': 'Enquetes Funcionários',
    }
    return render(request, 'core/enquete_funcionarios.html', contexto)

'''
Funções Enquetes Clientes
'''
def enquete_clientes(request):
    contexto = {
        'nome': 'Enquete Clientes',
    }
    return render(request, 'core/enquete_clientes.html', contexto)


def salvar_enquete_clientes(request):
    nota_cozinha = request.POST['nota_cozinha']
    nota_atendimento = request.POST['nota_atendimento']
    recomendaria = request.POST['recomendaria']
    resposta = EnqueteClientes(resp1=nota_cozinha, resp2=nota_atendimento, resp3=recomendaria )
    resposta.save()
    return redirect('core:enquete_clientes')

def resultado_enquete_clientes(request):
    hoje = datetime.now(tz=timezone.utc)
    semana = hoje - timedelta(days=6)
    hoje_formatado = hoje.strftime('%d/%m/%Y')
    semana_formatado = semana.strftime('%d/%m/%Y')
    total_enquetes_hoje = EnqueteClientes.objects.filter(date__date=hoje).count()
    total_enquetes_semana = EnqueteClientes.objects.filter(date__range=[semana, hoje]).count()
    soma_nota_cozinha = EnqueteClientes.objects.filter(date__date=hoje).aggregate(Sum('resp1'))['resp1__sum']
    soma_nota_atendimento = EnqueteClientes.objects.filter(date__date=hoje).aggregate(Sum('resp2'))['resp2__sum']
    soma_recomendaria = EnqueteClientes.objects.filter(date__date=hoje).aggregate(Sum('resp3'))['resp3__sum']
    soma_nota_cozinha_semana = EnqueteClientes.objects.filter(date__range=[semana, hoje]).aggregate(Sum('resp1'))['resp1__sum']
    soma_nota_atendimento_semana = EnqueteClientes.objects.filter(date__range=[semana, hoje]).aggregate(Sum('resp2'))['resp2__sum']
    soma_recomendaria_semana = EnqueteClientes.objects.filter(date__range=[semana, hoje]).aggregate(Sum('resp3'))['resp3__sum']
    '''
     Validação para evitar erros no relatório quando não há respostas
    '''
    if total_enquetes_hoje is None or soma_nota_cozinha is None:
        media_cozinha = 0
    else:
        media_cozinha = round(soma_nota_cozinha / total_enquetes_hoje, 2)
    if total_enquetes_hoje is None or soma_nota_atendimento is None:
        media_atendimento = 0
    else:
        media_atendimento = round(soma_nota_atendimento / total_enquetes_hoje, 2)
    if total_enquetes_hoje is None or soma_recomendaria is None:
        perc_recomenda = 0
        soma_recomendaria = 0
    else:
        perc_recomenda = round(soma_recomendaria * 100 / total_enquetes_hoje, 2)

    media_cozinha_semana = round(soma_nota_cozinha_semana / total_enquetes_semana, 2)
    media_atendimento_semana = round(soma_nota_atendimento_semana / total_enquetes_semana, 2)
    perc_recomenda_semana = round(soma_recomendaria_semana * 100 / total_enquetes_semana, 2)

    contexto = {
        'titulo_pagina': 'Resultado de enquetes dos clientes',
        'semana_formatado': semana_formatado,
        'hoje_formatado': hoje_formatado,
        'media_cozinha': media_cozinha,
        'media_atendimento': media_atendimento,
        'total_enquetes': total_enquetes_hoje,
        'soma_recomendaria': soma_recomendaria,
        'perc_recomenda': perc_recomenda,
        'media_cozinha_semana': media_cozinha_semana,
        'media_atendimento_semana': media_atendimento_semana,
        'total_enquetes_semana': total_enquetes_semana,
        'soma_recomendaria_semana': soma_recomendaria_semana,
        'perc_recomenda_semana': perc_recomenda_semana,
    }
    return render(request, 'gerencia:resultado_clientes.html', contexto)
'''
    total_enquetes = EnqueteClientes.objects.all().count()

'''

'''
TODO: Verificar situações sem resposta
'''