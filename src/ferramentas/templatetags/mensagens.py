from django import template
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.shortcuts import render_to_response, get_object_or_404
from sispag.models import *

register = template.Library()

def get_mensagens(request,pessoa):
    
    pessoa = get_object_or_404(Pessoa,user = pessoa.user)
    mensagem_list = Comentario.objects.filter(pessoa = pessoa).order_by('-data_mensagem')
    # render template
    paginador = Paginator(mensagem_list, 10)
    if request.GET.get('pm'):
        pagina = int(request.GET.get('pm'))
    else:
        pagina = 1
    try:
        mensagem = paginador.page(pagina)
    except (EmptyPage, InvalidPage):
        mensagem = paginador.page(paginador.num_pages)
    return {
        'mensagem_list': mensagem,
    }
    

register.inclusion_tag('admin/includes_ferramentas/mensagens.html')(get_mensagens)


