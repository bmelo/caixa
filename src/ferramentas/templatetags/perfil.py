from django import template

from sispag.models import *

register = template.Library()

def get_perfil(user):
    
    usuario_list = Pessoa.objects.filter(user = user)
    
    # render template
    return {
        'usuario_list': usuario_list,
    }
    

register.inclusion_tag('admin/includes_ferramentas/perfil.html')(get_perfil)


