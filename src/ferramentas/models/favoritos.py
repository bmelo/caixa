# -*- coding: utf-8 -*-

from django.db import models, transaction
from django.utils.translation import ugettext as _

from ferramentas.fields import PositionField

class Favoritos(models.Model):
   
    
    usuario = models.ForeignKey('auth.User', limit_choices_to={'is_staff': True}, verbose_name=_('Usuario'), related_name="admin_favoritos_set")
    
    class Meta:
        app_label = "ferramentas"
        verbose_name = _('Favorito')
        verbose_name_plural = _('Favoritos')
        ordering = ['usuario',]
    
    def __unicode__(self):
        return u"%s" % (self.usuario)
        
    save = transaction.commit_on_success(models.Model.save)
    

class FavoritosItem(models.Model):
    
    
    favoritos = models.ForeignKey(Favoritos)
    titulo = models.CharField(_('Titulo'), max_length=80)
    link = models.CharField(_('Link'), max_length=200, help_text=_('The Link should be relative, e.g. /admin/blog/.'))
    
    # order
    ordem = PositionField(unique_for_field='favoritos')
    
    class Meta:
        app_label = "ferramentas"
        verbose_name = _('Item do Favoritos')
        verbose_name_plural = _('Items do Favoritos')
        ordering = ['ordem']
    
    def __unicode__(self):
        return u"%s" % (self.titulo)
        
    save = transaction.commit_on_success(models.Model.save)
    

