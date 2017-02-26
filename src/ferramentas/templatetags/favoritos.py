from django import template
from ferramentas.models.favoritos import Favoritos, FavoritosItem
from ferramentas.settings import *

register = template.Library()

def get_favoritos(user, path, title):
    
    object_list = FavoritosItem.objects.filter(favoritos__usuario=user)
    
    try:
        favoritos = Favoritos.objects.get(usuario=user)
    except Favoritos.DoesNotExist:
        favoritos = ""
    
    # check whether or not this site is already stored as a shortcut
    try:
        FavoritosItem.objects.get(favoritos__usuario=user, link=path)
        is_favoritos = True
    except FavoritosItem.DoesNotExist:
        is_favoritos = False
        
    # it's not allowed to store an add_form
    try:
        last_item = path.split('/')[4]
        if path.split('/')[4] == "add":
            is_allowed = False
        else:
            is_allowed = True
    except:
        is_allowed = True
    
    # render template
    return {
        'object_list': object_list,
        'usuario': user,
        'path': path,
        'titulo': title,
        'is_favoritos': is_favoritos,
        'is_allowed': is_allowed,
        'favoritos': favoritos,
        'admin_title': ADMIN_TITLE,
    }
register.inclusion_tag('admin/includes_ferramentas/favoritos.html')(get_favoritos)

