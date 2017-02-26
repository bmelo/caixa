from django import template
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from sispag.models import *

register = template.Library()

def get_download(request):
   
    year = datetime.date.today().year
    boletins = Boletim.objects.filter(ano_letivo__aluno__user = request.user, ano_letivo__ano = year)
    disciplinas_turma =[] 
    for b in boletins:
        disciplinas_turma.append(b.disciplina)   
    downloads_list = Download.objects.filter(disciplina_turma__in=disciplinas_turma)
    paginador = Paginator(downloads_list, 5)
    if request.GET.get('page'):
        pagina = int(request.GET.get('page'))
    else:
        pagina = 1
    try:
        downloads = paginador.page(pagina)
    except (EmptyPage, InvalidPage):
        downloads = paginador.page(paginador.num_pages)

    
    # render template
    return {
        'downloads_list': downloads,
    }

register.inclusion_tag('admin/includes_ferramentas/download.html')(get_download)
