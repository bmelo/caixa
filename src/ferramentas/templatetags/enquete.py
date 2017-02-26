from django import template
from sispag.models import *

register = template.Library()

def get_enquete(request):
    
    ip = request.META['REMOTE_ADDR']
    enquete = 0
    enquetes = Opcoes.objects.select_related('enquete').filter(enquete__habilitada=True)
    for e in enquetes:
        enquete = e.enquete.id
    enquete_votacao = EnqueteVotacao.objects.filter(opcao__enquete__id = enquete)        
    return {
        'enquetes': enquetes,
        'ja_votou': enquete_votacao,
    }

register.inclusion_tag('admin/includes_ferramentas/enquete.html')(get_enquete)
