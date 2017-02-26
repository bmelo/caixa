# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.translation import ugettext as _

from ferramentas.models.favoritos import Favoritos, FavoritosItem

def add_favoritos(request):
    
    
    if request.GET:
        if request.GET.get('path') and request.GET.get('titulo'):
            next = request.GET.get('path')
            try:
                favoritos = Favoritos.objects.get(usuario=request.user)
            except Favoritos.DoesNotExist:
                favoritos = Favoritos(usuario=request.user)
                favoritos.save()
            favoritositem = FavoritosItem(favoritos=favoritos, titulo=request.GET.get('titulo'), link=request.GET.get('path'))
            favoritositem.save()
            msg = _('Site adicionado ao Favoritos.')
        else:
            msg = _('Error: Site nao pode ser adicionado ao Favoritos.')
            next = "/admin/"
    else:
        msg = _('Error: Site nao pode ser adicionado ao Favoritos.')
    
    # MESSAGE & REDIRECT
    request.user.message_set.create(message=msg)
    return HttpResponseRedirect(next)
add_shortcut = staff_member_required(add_favoritos)

def remove_favoritos(request):
    
    
    if request.GET:
        if request.GET.get('path'):
            next = request.GET.get('path')
            try:
                favoritositem = FavoritosItem.objects.get(favoritos__usuario=request.user, link=request.GET.get('path'))
                favoritositem.delete()
                msg = _('Site removido do Favoritos.')
            except FavoritosItem.DoesNotExist:
                msg = _('Error: Site nao pode ser removido do Favoritos.')
        else:
            next = "/admin/"
    else:
        msg = _('Error: Site nao pode ser removido do Favoritos.')
    
    # MESSAGE & REDIRECT
    request.user.message_set.create(message=msg)
    return HttpResponseRedirect(next)
remove_shortcut = staff_member_required(remove_favoritos)

