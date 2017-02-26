from django import template

from ferramentas.models.navegacao import Navegacao, NavegacaoItem
from ferramentas.settings import *
from sispag.models import *

register = template.Library()

def get_navegacao(request):
    
    if request.user.is_superuser:
        object_list = NavegacaoItem.objects.all()
    else:
        pessoa = Pessoa.objects.get(user = request.user)
        object_list = pessoa.admin_navegacao_set.all()
    
    # render template
    return {
        'object_list': object_list,
    }
    

register.inclusion_tag('admin/includes_ferramentas/navegacao.html')(get_navegacao)


