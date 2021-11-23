from django.contrib.sessions.models import Session
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from core.forms import ItemForm
from .forms import ConfiguracoesForm
from core.models import Item, PedidoAtrasado, Pedido, EnqueteClientes, EnqueteFuncionarios
from .models import Configuracoes
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Sum

@login_required(login_url='/logar/')
def dashboard(request):
    User = request.user
    itens = Item.objects.all()
    pedidos_atrasados = PedidoAtrasado.objects.all()
    pedidos = Pedido.objects.all()
    contexto = {
        'titulo_pagina': 'Gestão de Pedidos',
        'usuario': User,
        'itens': itens,
        'pedidos': pedidos,
        'total_pedidos': pedidos.count(),
        'total_pedidos_cancelados': pedidos.filter(situacao='Cancelado').count(),
        'pedidos_atrasados': pedidos_atrasados,
        'total_pedidos_atrasados': pedidos_atrasados.count(),
    }
    return render(request, 'gerencia/dashboard.html', contexto)

@login_required(login_url='/logar/')
def sair(request):
    logout(request)
    return render(request, 'core/index.html')

@login_required(login_url='/logar/')
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

@login_required(login_url='/logar/')
def listar_itens(request):
    itens = Item.objects.all()
    contexto = {
        'titulo_pagina': 'Relação de Itens',
        'titulo': 'Relação de Itens Cadastrados',
        'itens': itens,
    }
    return render(request, 'gerencia/itens.html', contexto)

@login_required(login_url='/logar/')
def excluir_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if str(request.method) == 'POST':
        item.delete()
        return redirect('gerencia:listar_itens')
    return render(request, 'gerencia/itens.html')

@login_required(login_url='/logar/')
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

@login_required(login_url='/logar/')
def configuracoes(request):
    configuracoes = Configuracoes.objects.filter(pk=1)
    form = ConfiguracoesForm(request.POST or None)
    contexto = {
        'titulo_pagina': 'Configurações Gerais do Sistema',
        'form': form,
       }
    return render(request, 'gerencia/configuracoes.html', contexto)


@login_required(login_url='/logar/')
def salvar_configuracoes(request):
    configuracoes = get_object_or_404(Configuracoes, pk=1)
    form = ConfiguracoesForm(request.POST or None, instance=configuracoes)
    if str(request.method) == 'POST':
        if form.is_valid():
            form.save()
            return redirect('gerencia:configuracoes')
    contexto = {
        'form': form,
    }
    return render(request, 'gerencia/configuracoes.html', contexto)

@login_required(login_url='/logar/')
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
    return render(request, 'gerencia/resultado_clientes.html', contexto)

@login_required(login_url='/logar/')
def resultado_enquete_funcionarios(request):
    contexto = {
        'titulo_pagina': 'Resultados de enquetes dos funcionários',
    }
    return render(request, 'gerencia/resultado_funcionarios.html', contexto)


