# -*- coding: utf-8 -*-

from django.db import models, transaction
from django.utils.translation import ugettext as _
from django.contrib.auth.models import Group
from ferramentas.fields import PositionField
from sispag.models import *

class Aviso(models.Model):
   
    
    titulo = models.CharField(_('Titulo'), max_length=30)
 
    texto = models.TextField(_('Texto'))
    
    usuarios = models.ManyToManyField('sispag.Pessoa', verbose_name=_('Usuarios'), blank=True, related_name="admin_aviso_set")

    
    ativo = models.BooleanField(default=True)
    
    ordem = PositionField(_('Ordem'))
    
    class Meta:
        app_label = "ferramentas"
        verbose_name = _(u'Aviso')
        verbose_name_plural = _(u'Avisos')
        ordering = ['ordem',]
    
    def status(self):
        if self.ativo:
             return "Ativo"
        else:
             return "Inativo"
        
    def __unicode__(self):
        return u"%s" % (self.titulo)
        
    save = transaction.commit_on_success(models.Model.save)
    
    

