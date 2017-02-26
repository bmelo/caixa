# -*- coding: utf-8 -*-#

from django.shortcuts import render_to_response, get_object_or_404
from django.conf.urls.defaults import *
from django.template import Context, loader
from sispag.forms import *
from sispag.models import *
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django import forms
from django.template import RequestContext,Context, loader
import datetime
from django.contrib.auth.decorators import user_passes_test
from django.forms.models import inlineformset_factory, BaseInlineFormSet
from django.forms.fields import EMPTY_VALUES
import html5lib
cur_dir = os.path.dirname(os.path.abspath(__file__))

import datetime
import cStringIO as StringIO
import ho.pisa as pisa
import cgi
import time
import os
import math
login_required = user_passes_test(lambda u: u.is_authenticated(),login_url='/admin')

   
@login_required
def perfil_usuario(request,username=''):
    pessoa = get_object_or_404(Pessoa,user__username = username)
    user = request.user
    title = 'Perfil de ' + str(username)
    if request.method == 'POST':
        mensagem = request.POST.get('mensagem')
        data = {'pessoa':pessoa.id,
                'user':user.id,
                'mensagem':mensagem,
                'data_mensagem':datetime.datetime.now(),
                }
        f = ComentarioForm(data)
        if f.is_valid():
            c = f.save()
            next = '/sistema/usuario/' + str(username)+'/'
            request.user.message_set.create(message='Mensagem postada com sucesso!')
            return HttpResponseRedirect(next)
    else:
        f = ComentarioForm()    
    return render_to_response('admin/includes_ferramentas/usuario.html',locals(),context_instance=RequestContext(request))

def maior(x , y):
    if (x.venda.data_venda - y.venda.data_venda) > (y.venda.data_venda - x.venda.data_venda) : return 1
    elif (x.venda.data_venda - y.venda.data_venda) == (y.venda.data_venda - x.venda.data_venda): return 0
    else: return -1
    
@login_required
def lista_clientes_nome(request):
    title = 'Cliente'
    year = datetime.date.today().year
    if request.GET.get('nome'): 
        nome = request.GET.get('nome') 
        pessoas = Pessoa.objects.filter(nome__icontains = nome) 
        if not pessoas:
            erro = u' Nenhum Cliente encontrado com este nome'
    else: 
        pessoas = Pessoa.objects.all() 
        
    if request.GET.get('pdf'):
        return render_to_pdf('admin/includes_ferramentas/cliente_nome_pdf.html',locals())
    else:
        return render_to_response('admin/includes_ferramentas/cliente_nome.html',locals(),context_instance=RequestContext(request))


@login_required
def lista_clientes_endereco(request):
    title = 'Cliente'
    year = datetime.date.today().year
    if request.GET.get('endereco'): 
        endereco = request.GET.get('endereco') 
        pessoas = Pessoa.objects.filter(logradouro__icontains = endereco) 
        if not pessoas:
            erro = u' Nenhum Cliente encontrado com este endereco'
    else: 
        pessoas = []
        erro = u'Endereco do cliente não digitado'
    
    if request.GET.get('pdf'):
        return render_to_pdf('admin/includes_ferramentas/cliente_nome_pdf.html',locals())
    else:
        return render_to_response('admin/includes_ferramentas/cliente_nome.html',locals(),context_instance=RequestContext(request))

@login_required
def relatorio_cliente_atraso(request):
    title = u'Relatório de Clientes em atraso'
    vendas = Venda.objects.filter(previsao_pagamento__lte = datetime.date.today(),pagamento = 2)
    if not vendas:
        erro = u'Não existe clientes em atraso no pagamento'
    
    if request.GET.get('pdf'):
        return render_to_pdf('admin/includes_ferramentas/relatorio_clientes_devendo_pdf.html',locals())
    else:
        return render_to_response('admin/includes_ferramentas/relatorio_clientes_devendo.html',locals(),context_instance=RequestContext(request))


@login_required
def relatorio_vendas(request):
    title = u'Relatório de vendas'
    anos = []
    ano_inicio = int(datetime.date.today().year) - 5
    ano_fim = int(datetime.date.today().year) + 5
    for i in range(ano_inicio,ano_fim):
            anos.append(i)
    if request.method == 'POST':
            try:
                if request.POST.get('ano_inicio') and request.POST.get('mes_inicio') and request.POST.get('dia_inicio') and request.POST.get('ano_termino') and request.POST.get('mes_termino') and request.POST.get('dia_termino'):
                     data_inicio = datetime.date(int(request.POST.get('ano_inicio')),int(request.POST.get('mes_inicio')),int(request.POST.get('dia_inicio')))
                     data_fim = datetime.date(int(request.POST.get('ano_termino')),int(request.POST.get('mes_termino')),int(request.POST.get('dia_termino')))
                     data_inicio_str = str(data_inicio)
                     data_fim_str = str(data_fim)
                     if request.POST.get('hoje'):
                         hoje = request.POST.get('hoje')
                         venda_avista = Venda.objects.filter(pagamento = 1,data_venda__year=int(datetime.datetime.today().year),data_venda__month=int(datetime.datetime.today().month),data_venda__day=int(datetime.datetime.today().day))
                         venda_aprazo = Venda.objects.filter(pagamento = 2,data_venda__year=int(datetime.datetime.today().year),data_venda__month=int(datetime.datetime.today().month),data_venda__day=int(datetime.datetime.today().day))
                         venda_acartao = Venda.objects.filter(pagamento = 3,data_venda__year=int(datetime.datetime.today().year),data_venda__month=int(datetime.datetime.today().month),data_venda__day=int(datetime.datetime.today().day))
                     elif request.POST.get('mes'):
                         mes = request.POST.get('mes')
                         venda_avista = Venda.objects.filter(pagamento = 1,data_venda__month=int(datetime.datetime.today().month))
                         venda_aprazo = Venda.objects.filter(pagamento = 2,data_venda__month=int(datetime.datetime.today().month))
                         venda_acartao = Venda.objects.filter(pagamento = 3,data_venda__month=int(datetime.datetime.today().month))
                     
                     else:
                         venda_avista = Venda.objects.filter(pagamento = 1,data_venda__range=(data_inicio, data_fim))
                         venda_aprazo = Venda.objects.filter(pagamento = 2,data_venda__range=(data_inicio, data_fim))
                         venda_acartao = Venda.objects.filter(pagamento = 3,data_venda__range=(data_inicio, data_fim))
                     total_avista = 0
                     total_aprazo = 0
                     total_acartao = 0  
                     saldo_devedor_prazo = 0
                     for v in venda_avista:
                         total_avista  = total_avista + v.valor_pago
                     for v in venda_aprazo:
                         total_aprazo  = total_aprazo + v.valor_pago
                         saldo_devedor_prazo = saldo_devedor_prazo + math.fabs(v.troco)
                     for v in venda_acartao:
                         total_acartao  = total_acartao + v.valor_pago
                         
                     
                else:
                    venda_avista= []
                    venda_aprazo = []
                    venda_acartao = []
                    erro = 'Selecione as datas de inicio e termino do intervalo'
            except ValueError:
                venda_avista= []
                venda_aprazo = []
                venda_acartao = []
                erro = 'Selecione as datas de inicio e termino do intervalo'
    else:
        if request.GET.get('pdf'):
                     data_inicio_str = str(request.GET.get('data_inicio'))
                     data_fim_str = str(request.GET.get('data_fim'))
                     
                     data_inicio = datetime.date(int(data_inicio_str[:4]),int(data_inicio_str[5:7]),int(data_inicio_str[8:10]))  
                     data_fim = datetime.date(int(data_fim_str[:4]),int(data_fim_str[5:7]),int(data_fim_str[8:10]))  
                 
                     if request.GET.get('hoje'):
                         hoje = request.GET.get('hoje')
                         venda_avista = Venda.objects.filter(pagamento = 1,data_venda__year=int(datetime.datetime.today().year),data_venda__month=int(datetime.datetime.today().month),data_venda__day=int(datetime.datetime.today().day))
                         venda_aprazo = Venda.objects.filter(pagamento = 2,data_venda__year=int(datetime.datetime.today().year),data_venda__month=int(datetime.datetime.today().month),data_venda__day=int(datetime.datetime.today().day))
                         venda_acartao = Venda.objects.filter(pagamento = 3,data_venda__year=int(datetime.datetime.today().year),data_venda__month=int(datetime.datetime.today().month),data_venda__day=int(datetime.datetime.today().day))
                     elif request.GET.get('mes'):
                         mes = request.GET.get('mes')
                         venda_avista = Venda.objects.filter(pagamento = 1,data_venda__month=int(datetime.datetime.today().month))
                         venda_aprazo = Venda.objects.filter(pagamento = 2,data_venda__month=int(datetime.datetime.today().month))
                         venda_acartao = Venda.objects.filter(pagamento = 3,data_venda__month=int(datetime.datetime.today().month))
                     else:
                         venda_avista = Venda.objects.filter(pagamento = 1,data_venda__range=(data_inicio, data_fim))
                         venda_aprazo = Venda.objects.filter(pagamento = 2,data_venda__range=(data_inicio, data_fim))
                         venda_acartao = Venda.objects.filter(pagamento = 3,data_venda__range=(data_inicio, data_fim))
                     total_avista = 0
                     total_aprazo = 0
                     total_acartao = 0  
                     saldo_devedor_prazo = 0
                     for v in venda_avista:
                         total_avista  = total_avista + v.valor_pago
                     for v in venda_aprazo:
                         total_aprazo  = total_aprazo + v.valor_pago
                         saldo_devedor_prazo = saldo_devedor_prazo + math.fabs(v.troco)
                     for v in venda_acartao:
                         total_acartao  = total_acartao + v.valor_pago
                     return render_to_pdf('admin/includes_ferramentas/relatorio_vendas_pdf.html',locals())
        else:
            venda_avista= []
            venda_aprazo = []
            venda_acartao = []
    
    return render_to_response('admin/includes_ferramentas/relatorio_vendas.html',locals(),context_instance=RequestContext(request))


@login_required
def relatorio_entradas(request):
    title = u'Relatório de Entrada de Mercadoria'
    anos = []
    ano_inicio = int(datetime.date.today().year) - 5
    ano_fim = int(datetime.date.today().year) + 5
    for i in range(ano_inicio,ano_fim):
            anos.append(i)
    if request.method == 'POST':
        try:
            if request.POST.get('ano_inicio') and request.POST.get('mes_inicio') and request.POST.get('dia_inicio') and request.POST.get('ano_termino') and request.POST.get('mes_termino') and request.POST.get('dia_termino'):
                 data_inicio = datetime.date(int(request.POST.get('ano_inicio')),int(request.POST.get('mes_inicio')),int(request.POST.get('dia_inicio')))
                 data_fim = datetime.date(int(request.POST.get('ano_termino')),int(request.POST.get('mes_termino')),int(request.POST.get('dia_termino')))
                 data_inicio_str = str(data_inicio)
                 data_fim_str = str(data_fim)
                 if request.POST.get('hoje'):
                     entradas = EntradaEstoque.objects.filter(data_hora__year=int(datetime.datetime.today().year),data_hora__month=int(datetime.datetime.today().month),data_hora__day=int(datetime.datetime.today().day))
                 elif request.POST.get('mes'):
                     entradas = EntradaEstoque.objects.filter(data_hora__year=int(datetime.datetime.today().year),data_hora__month=int(datetime.datetime.today().month))
                 else:
                     entradas = EntradaEstoque.objects.filter(data_hora__range=(data_inicio, data_fim))
                 total_produtos = 0
                 for e in entradas:
                     total_produtos  = total_produtos + e.quantidade
            else:
                entradas = []
                total_produtos = 0
                erro = 'Selecione as datas de inicio e termino do intervalo'
        except ValueError:
            entradas = []
            total_produtos = 0
            erro = 'Selecione as datas de inicio e termino do intervalo'
    else:
        entradas = []
        total_produtos = 0
    
    if request.GET.get('pdf'):
        data_inicio_str = str(request.GET.get('data_inicio'))
        data_fim_str = str(request.GET.get('data_fim'))
                     
        data_inicio = datetime.date(int(data_inicio_str[:4]),int(data_inicio_str[5:7]),int(data_inicio_str[8:10]))  
        data_fim = datetime.date(int(data_fim_str[:4]),int(data_fim_str[5:7]),int(data_fim_str[8:10]))  
        if request.GET.get('hoje'):
            entradas = EntradaEstoque.objects.filter(data_hora__year=int(datetime.datetime.today().year),data_hora__month=int(datetime.datetime.today().month),data_hora__day=int(datetime.datetime.today().day))
        elif request.GET.get('mes'):
            entradas = EntradaEstoque.objects.filter(data_hora__year=int(datetime.datetime.today().year),data_hora__month=int(datetime.datetime.today().month))
        else:
            entradas = EntradaEstoque.objects.filter(data_hora__range=(data_inicio, data_fim))
        total_produtos = 0
        for e in entradas:
            total_produtos  = total_produtos + e.quantidade
        return render_to_pdf('admin/includes_ferramentas/relatorio_entradas_pdf.html',locals())
    
    return render_to_response('admin/includes_ferramentas/relatorio_entradas.html',locals(),context_instance=RequestContext(request))


@login_required
def relatorio_aniversariantes(request):
    title = u'Relatório de Aniversariantes'
    anos = []
    ano_inicio = int(datetime.date.today().year) - 5
    ano_fim = int(datetime.date.today().year) + 5
    for i in range(ano_inicio,ano_fim):
            anos.append(i)
    if request.method == 'POST':
            if request.POST.get('hoje'):
                hoje = request.POST.get('hoje')
                pessoas = Pessoa.objects.filter(data_nascimento__month=int(datetime.datetime.today().month),data_nascimento__day=int(datetime.datetime.today().day))
            elif request.POST.get('mes'):
                mes = request.POST.get('mes')
                pessoas = Pessoa.objects.filter(data_nascimento__month=int(datetime.datetime.today().month))
            else:
                pessoas = []
    
        
    else:
        pessoas = []
    
    if request.GET.get('pdf'):
            if request.GET.get('hoje'):
                hoje = request.GET.get('hoje')
                pessoas = Pessoa.objects.filter(data_nascimento__month=int(datetime.datetime.today().month),data_nascimento__day=int(datetime.datetime.today().day))
            elif request.GET.get('mes'):
                mes = request.GET.get('mes')
                pessoas = Pessoa.objects.filter(data_nascimento__month=int(datetime.datetime.today().month))
            else:
                pessoas = []
            return render_to_pdf('admin/includes_ferramentas/relatorio_aniversariantes_pdf.html',locals())
        
    return render_to_response('admin/includes_ferramentas/relatorio_aniversariantes.html',locals(),context_instance=RequestContext(request))


@login_required
def lista_clientes_telefone(request):
    title = 'Cliente'
    year = datetime.date.today().year
    if request.GET.get('telefone'): 
        telefone = request.GET.get('telefone') 
        pessoas = Pessoa.objects.filter(telefone__icontains = telefone) 
        if not pessoas:
            erro = u' Nenhum Cliente encontrado com este telefone'
    else: 
        pessoas = []
        erro = u'Telefone do cliente não digitado'
    
    if request.GET.get('pdf'):
        return render_to_pdf('admin/includes_ferramentas/cliente_nome_pdf.html',locals())
    else:
        return render_to_response('admin/includes_ferramentas/cliente_nome.html',locals(),context_instance=RequestContext(request))
        
@login_required
def cliente(request): 
    title = 'Cliente' 
    year = datetime.date.today().year
    if request.GET.get('id'): 
        id = request.GET.get('id') 
        try:
            pessoa = Pessoa.objects.get(id = id ) 
            venda = ProdutoVendas.objects.filter(venda__cliente = pessoa)
            recargas = Recarga.objects.filter(venda__cliente = pessoa)
            lista = []
            total = 0 
            troco = 0
            vendas_id = []
            for v in venda:
                lista.append(v)
                total = total  + (v.produto.valor * v.quantidade)
                if v.venda not in vendas_id:
                    vendas_id.append(v.venda)
            for r in recargas:
                lista.append(r)
                total = total + r.total
                if r.venda not in vendas_id:
                    vendas_id.append(r.venda)
            for v in vendas_id:
                if v.aberto == 1:
                    troco = troco + math.fabs(v.total - v.valor_pago)
            lista.sort(maior)          
            title = 'Cliente - ' + pessoa.nome
        except Pessoa.DoesNotExist:
            pessoa = []
            erro =  u'Cliente não encontrado'
    else: 
        pessoa = []
        lista = []
        erro = u'numero do cliente não digitado'
    
    if request.GET.get('pdf'):
        return render_to_pdf('admin/includes_ferramentas/cliente_pdf.html',locals())
    else:
        return render_to_response('admin/includes_ferramentas/cliente.html',locals(),context_instance=RequestContext(request))

@login_required
def cliente_iniciar_venda(request,cliente = 0):
      try:
          vendedor = Pessoa.objects.get(user = request.user)
      except Pessoa.DoesNotExist:
          vendedor = []
      if vendedor:
          try:
            estacao = EstacaoOperador.objects.get(operador = vendedor)
          except EstacaoOperador.DoesNotExist:
            estacao = []
          if estacao:
              try:
                      caixa = Caixa.objects.get(data_hora_abertura__year = int(datetime.datetime.today().year),data_hora_abertura__month = int(datetime.datetime.today().month),data_hora_abertura__day = int(datetime.datetime.today().day),situacao = '1',estacao = estacao.estacao)
              except Caixa.DoesNotExist:
                      caixa = []
              if caixa:  
                   
                  try:
                      pessoa = Pessoa.objects.get(id = cliente) 
                      vend = Venda(vendedor = vendedor, cliente = pessoa)
                  
                  except Pessoa.DoesNotExist:
                      vend = Venda(vendedor = vendedor)
                  vend.save()
                  next = '/admin/sispag/venda/' + str(vend.id) + '/'   
                  return HttpResponseRedirect(next)
              else:
                   request.user.message_set.create(message='O caixa se encontra fechado, para iniciar uma venda o caixa precisa estar aberto.')
                   try:
                      pessoa = Pessoa.objects.get(id = cliente) 
                               
                   except Pessoa.DoesNotExist:
                      pessoa = []
                   
                   if pessoa:
                       next = '/admin/sispag/cliente/?id=' + str(pessoa.id)
                       return HttpResponseRedirect(next)
                   else:
                       return HttpResponseRedirect('/admin/')
          else:
               erro = 'O usuario logado ainda não foi relacionado com nunhuma estação de trabalho'
               return HttpResponseRedirect('/admin/')
      else:
               request.user.message_set.create(message='O usuario logado não possui uma pessoa cadastrada')
               return HttpResponseRedirect('/admin/')

@login_required
def cliente_finalizar_venda(request,venda = 0):
    title = 'Cliente'
    year = datetime.date.today().year       
    try:
       vend = Venda.objects.get(id = venda) 
       vend.finalizada = True
       vend.save()
       request.user.message_set.create(message='VENDA FINALIZADA')
       next = '/admin/sispag/venda/' + str(vend.id) + '/'
    except venda.DoesNotExist:
       vend = []
       next = '/admin/sispag/venda/'
    return HttpResponseRedirect(next)


@login_required
def cliente_cancelar_venda(request,venda = 0):
    title = 'Cliente'
    year = datetime.date.today().year       
    try:
       vend = Venda.objects.get(id = venda)
       produtos = ProdutoVendas.objects.filter(venda = vend)
       if vend.finalizada:
           for produto in produtos:
                try:
                    estoque = Estoque.objects.get(produto = produto.produto)
                except Estoque.DoesNotExist:
                    estoque = []
                if estoque:
                    estoque.quantidade = int(estoque.quantidade) + int(produto.quantidade)
                estoque.save()
                prod = ProdutoVendas.objects.get(id = produto.id)
                prod.delete()
       else:
            for produto in produtos:
                prod = ProdutoVendas.objects.get(id = produto.id)
                prod.delete()
       vend.delete()
       request.user.message_set.create(message='VENDA CANCELADA')
       next = '/admin/'
    except Venda.DoesNotExist:
       vend = []
       request.user.message_set.create(message='VENDA NÃO EXISTE')
       next = '/admin/'
    return HttpResponseRedirect(next)

@login_required
def cliente_pagar_prazo(request,venda = 0):
    title = 'Cliente'
    year = datetime.date.today().year
    try:
        vend = Venda.objects.get(id = venda) 
        venda = ProdutoVendas.objects.filter(venda = vend)
        recargas = Recarga.objects.filter(venda = vend)
        lista = []
        for v in venda:
            lista.append(v)
        for r in recargas:
            lista.append(r)
        lista.sort(maior) 
        total = 0
        for v in venda:
            total = total  + (v.produto.valor * v.quantidade)
        for r in recargas:
            total = total + r.total     
        title = 'Cliente - ' + str(vend.cliente.nome) 
        if vend.troco < 0:
            desconto = True
        if request.method == 'POST':
            try:
                    previsao = datetime.date(int(request.POST.get('previsao_pagamento_year')),int(request.POST.get('previsao_pagamento_month')),int(request.POST.get('previsao_pagamento_day')))
            except ValueError:
                    previsao = 0
            data = {'data_venda': vend.data_venda,
                        'data_pagamento': datetime.datetime.now(),
                        'previsao_pagamento': previsao,
                        'vendedor': vend.vendedor.id,
                        'cliente': vend.cliente.id,
                        'pagamento': vend.pagamento,
                        'parcelas':vend.parcelas,
                        'valor_pago':request.POST.get('valor_pago'),
                        'total': vend.total,
                        'troco': vend.troco,
                        'finalizada': True,
                }
            v = VendaPrazoForm(data)
            if v.is_valid():
                if int(vend.parcelas) > 1:
                    vend.parcelas = int(vend.parcelas) - 1
                    valor = request.POST.get('valor_pago')
                    vend.data_pagamento = datetime.datetime.now()
                    vend.previsao_pagamento = previsao
                    vend.valor_pago = float(vend.valor_pago) + float(valor)
                    vend.troco = float(vend.troco) + float(valor)
                    vend.save()
                    for produto in venda:
                        try:
                            estoque = Estoque.objects.get(produto = produto.produto)
                        except Estoque.DowsNotExist:
                            estoque = []
                        if estoque:
                            estoque.quantidade = int(estoque.quantidade) - int(produto.quantidade)
                            estoque.save()
                    vendedor = Pessoa.objects.get(user = request.user)  
                    try:
                        estacao = EstacaoOperador.objects.get(operador = vendedor)
                    except EstacaoOperador.DoesNotExist:
                        estacao = []
                    if estacao:
                        try:
                            caixa = Caixa.objects.get(data_hora_abertura__year = int(datetime.datetime.today().year),data_hora_abertura__month = int(datetime.datetime.today().month),data_hora_abertura__day = int(datetime.datetime.today().day),situacao = '1',estacao = estacao.estacao)
                        except Caixa.DoesNotExist:
                            caixa = []
                        if caixa:  
                            if float(vend.valor_pago) <= float(vend.total):
                                caixa.valor = float(caixa.valor) + float(vend.valor_pago)
                                caixa.save()
                            else:
                                caixa.valor = float(caixa.valor) + float(vend.total)
                                caixa.save()
                else:
                    if int(vend.aberto) == 1 :
                        vend.aberto = False
                        vend.parcelas = int(vend.parcelas) - 1
                        valor = request.POST.get('valor_pago')
                        vend.data_pagamento = datetime.datetime.now()
                        vend.previsao_pagamento = previsao
                        vend.valor_pago = float(vend.valor_pago) + float(valor)
                        vend.troco = float(vend.troco) + float(valor)
                        vend.save()
                        for produto in venda:
                            try:
                                estoque = Estoque.objects.get(produto = produto.produto)
                            except Estoque.DowsNotExist:
                                estoque = []
                            if estoque:
                                estoque.quantidade = int(estoque.quantidade) - int(produto.quantidade)
                                estoque.save()
                        vendedor = Pessoa.objects.get(user = request.user)  
                        try:
                            estacao = EstacaoOperador.objects.get(operador = vendedor)
                        except EstacaoOperador.DoesNotExist:
                            estacao = []
                        if estacao:
                            try:
                                caixa = Caixa.objects.get(data_hora_abertura__year = int(datetime.datetime.today().year),data_hora_abertura__month = int(datetime.datetime.today().month),data_hora_abertura__day = int(datetime.datetime.today().day),situacao = '1',estacao = estacao.estacao)
                            except Caixa.DoesNotExist:
                                caixa = []
                            if caixa:  
                                if float(vend.valor_pago) <= float(vend.total):
                                    caixa.valor = float(caixa.valor) + float(vend.valor_pago)
                                    caixa.save()
                                else:
                                    caixa.valor = float(caixa.valor) + float(vend.total)
                                    caixa.save()
                if vend.troco < 0:
                    desconto = True
        else:
            v = VendaPrazoForm()
    except Venda.DoesNotExist:
        vend = []
        erro = u'Venda não encontrada'
    return render_to_response('admin/includes_ferramentas/cliente_venda_prazo.html',locals(),context_instance=RequestContext(request))   


@login_required
def cliente_venda_cupom(request,venda = 0): 
    title = 'Cliente cupom venda'
    try:
        vend = Venda.objects.get(id = int(venda))
        if vend.troco < 0:
            desconto = True
    except Venda.DoesNotExist:
        vend = []
    if not vend:
        erro = 'Venda não encontrada'
    return render_to_pdf('admin/includes_ferramentas/cliente_venda_cupom.html',locals())
        

@login_required
def cliente_venda_prazo_cupom(request,venda = 0): 
    title = 'Cliente cupom venda'
    try:
        vend = Venda.objects.get(id = int(venda))
        if vend.troco < 0:
            desconto = True
    except Venda.DoesNotExist:
        vend = []
    if not vend:
        erro = 'Venda não encontrada'
    return render_to_pdf('admin/includes_ferramentas/cliente_venda_prazo_cupom.html',locals())

@login_required
def cliente_venda(request,venda = 0): 
    title = 'Cliente'
    year = datetime.date.today().year
    try:
        vend = Venda.objects.get(id = venda) 
        venda = ProdutoVendas.objects.filter(venda = vend)
        recargas = Recarga.objects.filter(venda = vend)
        lista = []
        for v in venda:
            lista.append(v)
        for r in recargas:
            lista.append(r)
        lista.sort(maior) 
        count = len(lista)
        total = 0
        for v in venda:
            total = total  + (v.produto.valor * v.quantidade)
        for r in recargas:
            total = total + r.total
        
        if vend.cliente:
            title = 'Cliente - ' + str(vend.cliente.nome)
            
        if vend.troco < 0:
            desconto = True
        if request.method == 'POST':
            v = VendaForm(instance = vend)
            if vend.finalizada==True and vend.valor_pago == 0:
                try:
                     valor_pago = float(request.POST.get('valor_pago'))
                except ValueError:
                     valor_pago = 0.0
                troco = valor_pago - total     
                try:
                    if request.POST.get('previsao_pagamento_year') and request.POST.get('previsao_pagamento_month') and request.POST.get('previsao_pagamento_day'):
                        previsao = datetime.date(int(request.POST.get('previsao_pagamento_year')),int(request.POST.get('previsao_pagamento_month')),int(request.POST.get('previsao_pagamento_day')))
                    else:
                        previsao = vend.previsao_pagamento
                except ValueError:
                    previsao = 0
                    
                if vend.cliente:
                    cliente = vend.cliente.id
                else:
                    cliente = ''   
                if vend.cliente:                 
                    data = {'data_venda': vend.data_venda,
                            'data_pagamento': datetime.datetime.now(),
                            'previsao_pagamento': previsao,
                            'vendedor': vend.vendedor.id,
                            'cliente': cliente ,
                            'pagamento': request.POST.get('pagamento'),
                            'parcelas':request.POST.get('parcelas'),
                            'valor_pago':request.POST.get('valor_pago'),
                            'total': total,
                            'troco': troco,
                            'dinheiro_recebido': True,
                            'finalizada': True,
                            'entregador': request.POST.get('entregador') ,
                            }
                    v = VendaForm(data)
                else:
                     data = {'data_venda': vend.data_venda,
                            'data_pagamento': datetime.datetime.now(),
                            'previsao_pagamento': previsao,
                            'vendedor': vend.vendedor.id,
                            'cliente': cliente ,
                            'pagamento': request.POST.get('pagamento'),
                            'parcelas':vend.parcelas,
                            'valor_pago':request.POST.get('valor_pago'),
                            'total': total,
                            'troco': troco,
                            'dinheiro_recebido': True,
                            'finalizada': True,
                            }
                     v = VendaOutrosForm(data)
                
                if v.is_valid():
                    if request.POST.get('parcelas'):
                        if int(request.POST.get('parcelas')) != 1:
                            vend.aberto = True
                        vend.parcelas = request.POST.get('parcelas')
                    if (int(request.POST.get('pagamento')) == 1) or (int(request.POST.get('pagamento')) == 3):
                        vend.data_pagamento = datetime.datetime.now()
                    vend.previsao_pagamento = previsao
                    vend.pagamento = request.POST.get('pagamento')
                    vend.valor_pago = request.POST.get('valor_pago')
                    vend.dinheiro_recebido = True
                    if request.POST.get('entregador'):
                        entregador = Pessoa.objects.get(id = int(request.POST.get('entregador')))
                        vend.entregador = entregador
                    vend.total = total
                    vend.troco = troco
                    vend.save()
                    for produto in venda:
                        try:
                            estoque = Estoque.objects.get(produto = produto.produto)
                        except Estoque.DowsNotExist:
                            estoque = []
                        if estoque:
                            estoque.quantidade = int(estoque.quantidade) - int(produto.quantidade)
                            estoque.save()
                             
                    if vend.valor_pago:
                        vendedor = Pessoa.objects.get(user = request.user)  
                        try:
                            estacao = EstacaoOperador.objects.get(operador = vendedor)
                        except EstacaoOperador.DoesNotExist:
                            estacao = []
                        if estacao:
                              try:
                                      caixa = Caixa.objects.get(data_hora_abertura__year = int(datetime.datetime.today().year),data_hora_abertura__month = int(datetime.datetime.today().month),data_hora_abertura__day = int(datetime.datetime.today().day),situacao = '1',estacao = estacao.estacao)
                              except Caixa.DoesNotExist:
                                      caixa = []
                              if caixa:  
                                  if float(vend.valor_pago) <= float(vend.total):
                                      caixa.valor = float(caixa.valor) + float(vend.valor_pago)
                                      caixa.save()
                                  else:
                                      caixa.valor = float(caixa.valor) + float(vend.total)
                                      caixa.save()
                            
                    next = '/admin/sispag/venda/' + str(vend.id) + '/'
                    request.user.message_set.create(message='VENDA CONCLUIDA')
                    return HttpResponseRedirect(next)
                        
            if request.POST.get('recarga'):
                f = ProdutoVendasForm()
                data = {'venda': vend.id,
                        'operadora': request.POST.get('operadora'),
                        'valor': request.POST.get('valor'),
                        'quantidade':request.POST.get('quantidade'),
                        'total': 0,
                }
                r = RecargaForm(data)
                if r.is_valid():
                    c = r.save(commit = False)
                    c.venda = vend
                    c.total = float(c.valor)* int(c.quantidade)
                    c.save()
                    next = '/admin/sispag/venda/' + str(vend.id) + '/'
                    request.user.message_set.create(message='RECARGA INSERIDA NA COMPRA')
                    return HttpResponseRedirect(next)
            else:
                r = RecargaForm()
                data = {'produto':request.POST.get('produto'),
                        'venda': vend.id,
                        'quantidade':request.POST.get('quantidade'),
                        'valor':0,
                }
                f = ProdutoVendasForm(data)
                if f.is_valid():
                    c = f.save(commit = False)
                    c.valor = float(c.produto.valor)* int(c.quantidade)
                    c.venda = vend
                    c.save()
                    next = '/admin/sispag/venda/' + str(vend.id) + '/'
                    request.user.message_set.create(message='PRODUTO INSERIDO NA COMPRA')
                    return HttpResponseRedirect(next)
        else:
            f = ProdutoVendasForm()
            r = RecargaForm()
            if vend.cliente:
                v = VendaForm(instance = vend)
            else:
                v = VendaOutrosForm(instance = vend)
    except Venda.DoesNotExist:
        vend = []
        erro = u'Venda não encontrada'
    
    return render_to_response('admin/includes_ferramentas/cliente_venda.html',locals(),context_instance=RequestContext(request))
  

@login_required
def abrir_caixa(request):
  #situacao_caixa { 0 -> Fechado, 1 -> Aberto }
  title = 'Abertura de Caixa'
  pessoa = Pessoa.objects.get(user = request.user)
  try:
    estacao = EstacaoOperador.objects.get(operador = pessoa)
  except EstacaoOperador.DoesNotExist:
    estacao = []
  if estacao:
      if request.method == 'POST':
          
              data = {
                      'valor_inicial': request.POST.get('valor_inicial'),
                    }
              c = CaixaForm(data)
              if c.is_valid():
                  f = c.save(commit = False)
                  f.valor = float(request.POST.get('valor_inicial'))
                  f.usuario_abertura = pessoa
                  f.situacao = '1'
                  f.estacao  = estacao.estacao
                  f.save()
                  next = '/admin/'
                  request.user.message_set.create(message='CAIXA ABERTO')
                  return HttpResponseRedirect(next)
          
      else:
          try:
              caixa = Caixa.objects.get(data_hora_abertura__year = int(datetime.datetime.today().year),data_hora_abertura__month = int(datetime.datetime.today().month),data_hora_abertura__day = int(datetime.datetime.today().day),situacao = '1',estacao = estacao.estacao)
          except Caixa.DoesNotExist:
              caixa = []
              c = CaixaForm()  
  else:
      erro = 'O usuario logado ainda não foi relacionado com nunhuma estação de trabalho'
  return render_to_response('admin/includes_ferramentas/abrir_caixa.html', locals(), context_instance=RequestContext(request))


@login_required
def cadastro_cliente(request):
  
  title = 'Cadastro de cliente'
  if request.method == 'POST':
  
              c = PessoaClienteForm(request.POST,request.FILES)
              
              if c.is_valid():
                  f = c.save(commit = False)
                  f.tipo = '3'
                  f.ativo = True
                  f.save()
                  next = '/admin/'
                  request.user.message_set.create(message='CLIENTE CADASTRADO COM SUCESSO')
                  return HttpResponseRedirect(next)
          
  else:
         c = PessoaClienteForm()  
  
  return render_to_response('admin/includes_ferramentas/cadastro_cliente.html', locals(), context_instance=RequestContext(request))


@login_required
def retirada_caixa(request):
  #situacao_caixa { 0 -> Fechado, 1 -> Aberto }
  title = 'Retirada de Dinheiro'
  pessoa = Pessoa.objects.get(user = request.user)
  try:
    estacao = EstacaoOperador.objects.get(operador = pessoa)
  except EstacaoOperador.DoesNotExist:
    estacao = []
  if estacao:
      try:
              caixa = Caixa.objects.get(data_hora_abertura__year = int(datetime.datetime.today().year),data_hora_abertura__month = int(datetime.datetime.today().month),data_hora_abertura__day = int(datetime.datetime.today().day),situacao = '1',estacao = estacao.estacao)
      except Caixa.DoesNotExist:
              caixa = []
      if caixa:                                                                                                                 
          if request.method == 'POST':
                if request.POST.get('valor'):
                  if float(request.POST.get('valor')) > float(caixa.valor):
                      errox = 'Não foi possivel executar a retirada, a quantida digitada excede a quantida que o caixa possui R$ %d' %caixa.valor
                      c = RetiradaForm(request.POST) 
                  else:    
                      data = {
                              'valor': request.POST.get('valor'),
                              'observacao': request.POST.get('observacao'),
                            }
                      c = RetiradaForm(data)
                      if c.is_valid():
                          f = c.save(commit = False)
                          f.usuario = pessoa
                          f.data_hora = datetime.datetime.now()
                          f.save()
                          caixa.valor = float(caixa.valor) - float(f.valor)
                          caixa.save()
                          next = '/admin/'
                          request.user.message_set.create(message='Retirada Efetuada R$ %d' % f.valor)
                          return HttpResponseRedirect(next)
                else:
                    c = RetiradaForm(request.POST) 
          else:
                 c = RetiradaForm()
                   
      else:
          erro = 'O caixa se encontra fechado, para fazer uma retirada precisa abrir o caixa antes.'
  else:
      erro = 'O usuario logado ainda não foi relacionado com nunhuma estação de trabalho.'
  return render_to_response('admin/includes_ferramentas/retirada_caixa.html', locals(), context_instance=RequestContext(request))

@login_required
def fechar_caixa(request):
  #situacao_caixa { 0 -> Fechado, 1 -> Aberto }
  title = 'Fechamento de Caixa'
  try:
      pessoa = Pessoa.objects.get(user = request.user)
  except Pessoa.DoesNotExist:
      pessoa= []
  if pessoa:
      try:
        estacao = EstacaoOperador.objects.get(operador = pessoa)
      except EstacaoOperador.DoesNotExist:
        estacao = []
      if estacao:
          caixas = Caixa.objects.filter(data_hora_abertura__year = int(datetime.datetime.today().year),data_hora_abertura__month = int(datetime.datetime.today().month),data_hora_abertura__day = int(datetime.datetime.today().day),estacao = estacao.estacao)
          retiradas = Retirada.objects.filter(data_hora__year = int(datetime.datetime.today().year),data_hora__month = int(datetime.datetime.today().month),data_hora__day = int(datetime.datetime.today().day))
          total_caixa = 0
          total_retiradas = 0
          total = 0
          for c in caixas:
              total_caixa = total_caixa + float(c.valor)
          for retirada in retiradas:
              total_caixa  = total_caixa - float(retirada.valor)
              total_retiradas = total_retiradas + float(retirada.valor)
          total  = total_caixa + total_retiradas
          if request.method == 'POST':
              try:
                  caixa = Caixa.objects.get(data_hora_abertura__year = int(datetime.datetime.today().year),data_hora_abertura__month = int(datetime.datetime.today().month),data_hora_abertura__day = int(datetime.datetime.today().day),situacao = '1',estacao = estacao.estacao)
                  caixa.situacao = '0'
                  pessoa = Pessoa.objects.get(user = request.user)
                  caixa.usuario_fechamento = pessoa
                  caixa.data_hora_fechamento = datetime.datetime.now()
                  caixa.save()
                  next = '/admin/sispag/fechar_caixa/'
                  request.user.message_set.create(message='CAIXA FECHADO')
                  return HttpResponseRedirect(next)
              except Caixa.DoesNotExist:
                  caixa = []
          else:
              try:
                  caixa = Caixa.objects.get(data_hora_abertura__year = int(datetime.datetime.today().year),data_hora_abertura__month = int(datetime.datetime.today().month),data_hora_abertura__day = int(datetime.datetime.today().day),situacao = '1',estacao = estacao.estacao)
              except Caixa.DoesNotExist:
                  caixa = [] 
      else:
          erro = 'O usuario logado ainda não foi relacionado com nunhuma estação de trabalho'
  else:
      erro = 'O usuario logado ainda não possui uma pessoa cadastrada!'
  return render_to_response('admin/includes_ferramentas/fechar_caixa.html', locals(), context_instance=RequestContext(request))
       

def render_to_pdf(template_src, context_dict):
    template = loader.get_template(template_src)
    context = Context(context_dict)
    html  = template.render(context)
    result = StringIO.StringIO()
    MEDIA_URL = getattr(settings,'MEDIA_ROOT')
    css = open(cur_dir +'/css/pisa.css').read()
    pdf = pisa.CreatePDF(StringIO.StringIO(html.encode("ISO-8859-1")), result,default_css=css)
    if not pdf.err:
        response = HttpResponse(result.getvalue(), mimetype='application/pdf')
        response['Content-Disposition'] = 'filename=relatorio.pdf'
        return response
    return http.HttpResponse('We had some errors<pre>%s</pre>' % cgi.escape(html))
