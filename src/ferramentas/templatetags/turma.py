from django import template
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from sispag.models import *

register = template.Library()

def get_turma(request,user):
    year = datetime.date.today().year
    turma = AnoLetivo.objects.filter(aluno__user = user, ano = year)
    alunos = []
    for t in turma:
        turma = t.turma
    if turma:
        turma_list = AnoLetivo.objects.filter(turma = turma,ano = year).order_by('aluno__nome')
        paginador = Paginator(turma_list, 5)
        if request.GET.get('pt'):
            pagina = int(request.GET.get('pt'))
        else:
            pagina = 1
        try:
            alunos = paginador.page(pagina)
        except (EmptyPage, InvalidPage):
            alunos = paginador.page(paginador.num_pages)
        # render template
        return {
                'turma_list': alunos,
                'turma': turma.codigo + '-' + turma.periodo.turno
        }
    else:
        turma_list = []
        # render template
        return {
            'turma_list': turma_list,
            'turma':turma
        }
        
    
    
    

register.inclusion_tag('admin/includes_ferramentas/turma.html')(get_turma)
