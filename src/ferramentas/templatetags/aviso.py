from django import template
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from ferramentas.models import Aviso
from sispag.models import *

register = template.Library()

def get_avisos(request):
    
    if request.user.is_superuser:
        aviso_list = Aviso.objects.all()
    else:
        pessoa = Pessoa.objects.get(user = request.user)
        aviso_list = pessoa.admin_aviso_set.all()
    # render template
    paginador = Paginator(aviso_list, 5)
    if request.GET.get('pa'):
        pagina = int(request.GET.get('pa'))
    else:
        pagina = 1
    try:
        avisos = paginador.page(pagina)
    except (EmptyPage, InvalidPage):
        avisos = paginador.page(paginador.num_pages)
    return {
        'aviso_list': avisos,
    }
    

register.inclusion_tag('admin/includes_ferramentas/avisos.html')(get_avisos)


