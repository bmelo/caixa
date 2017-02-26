# -*- coding: utf-8 -*-

from django.db import models, transaction
from django.utils.translation import ugettext as _

from ferramentas.fields import PositionField
from sispag.models import *

ITEM_CATEGORIA_ALTERNATIVAS = (
    ('1', _('interno')),
    ('2', _('externo')),
)

class Navegacao(models.Model):
   
    
    titulo = models.CharField(_('Titulo'), max_length=30)
    
 
    ordem = PositionField(_('Ordem'))
    
    class Meta:
        app_label = "ferramentas"
        verbose_name = _(u'Link Util')
        verbose_name_plural = _(u'Links Uteis')
        ordering = ['ordem',]
    
    def __unicode__(self):
        return u"%s" % (self.titulo)
        
    save = transaction.commit_on_success(models.Model.save)
    

class NavegacaoItem(models.Model):
    
    
    navegacao = models.ForeignKey(Navegacao)
    titulo = models.CharField(_('Titulo'), max_length=30)
    link = models.CharField(_('Link'), max_length=200, help_text=_('The Link should be relative, e.g. /admin/blog/.'))
    categoria = models.CharField(_('Categoria'), max_length=1, choices=ITEM_CATEGORIA_ALTERNATIVAS)
    
   
    usuarios = models.ManyToManyField('sispag.Pessoa', verbose_name=_('Usuarios'), blank=True, related_name="admin_navegacao_set")
    
    
    ordem = PositionField(unique_for_field='navegacao')
    
    class Meta:
        app_label = "ferramentas"
        verbose_name = _(u'Item de Links Uteis')
        verbose_name_plural = _(u'Itens de Links Uteis')
        ordering = ['navegacao', 'ordem']
    
    def __unicode__(self):
        return u"%s" % (self.titulo)
        
    save = transaction.commit_on_success(models.Model.save)
    

