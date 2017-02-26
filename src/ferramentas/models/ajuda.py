# coding: utf-8

from django.db import models, transaction
from django.utils.translation import ugettext as _

from ferramentas.fields import PositionField

class Ajuda(models.Model):
 
    
    titulo = models.CharField(_('Titulo'), max_length=50)
    
    # order
    ordem = PositionField(_('Ordem'))
    
    class Meta:
        app_label = "ferramentas"
        verbose_name = _('Ajuda')
        verbose_name_plural = _('Ajuda')
        ordering = ['ordem']
    
    def __unicode__(self):
        return u"%s" % (self.titulo)
    
    save = transaction.commit_on_success(models.Model.save)
    

class AjudaItem(models.Model):
   
    
    ajuda = models.ForeignKey(Ajuda)
    titulo = models.CharField(_('Titulo'), max_length=200)
    link = models.CharField(_('Link'), max_length=200, help_text=_('The Link should be relative, e.g. /admin/blog/.'))
    corpo = models.TextField(_('Corpo'))
    
    # order
    ordem = PositionField(unique_for_field='ajuda')
    
    class Meta:
        app_label = "ferramentas"
        verbose_name = _('Item de Ajuda')
        verbose_name_plural = _('Itens de Ajuda')
        ordering = ['ajuda', 'ordem']
    
    def __unicode__(self):
        return u"%s" % (self.titulo)
    
    def get_corpo(self):
        corpo = self.corpo.replace('<h2>', '</div><div class="module"><h2>')
        return corpo
    
    save = transaction.commit_on_success(models.Model.save)
    

