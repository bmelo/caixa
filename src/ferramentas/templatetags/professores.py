from django import template
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from sispag.models import *

register = template.Library()

def get_professores(request,user):
    year = datetime.date.today().year
    boletins = Boletim.objects.filter(ano_letivo__aluno__user = user, ano_letivo__ano = year)
    turma = 0
    for b in boletins:
        turma = b.ano_letivo.turma
    disciplinas = DisciplinaProfessor.objects.filter(disciplina__turma = turma)
    professores_list = disciplinas
    professores = []
    
    paginador = Paginator(professores_list, 5)
    if request.GET.get('pp'):
        pagina = int(request.GET.get('pp'))
    else:
        pagina = 1
    try:
        professores = paginador.page(pagina)
    except (EmptyPage, InvalidPage):
        professores = paginador.page(paginador.num_pages)
    return {
        'professores_list': professores,
    }

register.inclusion_tag('admin/includes_ferramentas/professores.html')(get_professores)
