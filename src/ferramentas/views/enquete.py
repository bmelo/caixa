# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from sispag.models import *
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.translation import ugettext as _

def add_voto(request):
    ip = request.META['REMOTE_ADDR']
    next = "/admin/"
    if request.GET:
        if request.GET.get('opt'):
            opcao = int(request.GET.get('opt'))
            enquete = int(request.GET.get('enquete_id'))
            opcoes = Opcoes.objects.get(id = opcao, enquete__id=enquete)
            votos = int(opcoes.votos)
            votos = votos + 1 
            opcoes.votos = votos
            opcoes.save()
            enquete_votacao = EnqueteVotacao(opcao = opcoes, ip_usuario = ip )
            enquete_votacao.save()
            msg = _(u'Voto computado com sucesso!')
        else:
            msg = _(u'Error: O voto não pode ser computado, tente novamente!')
            next = "/admin/"
    else:
        msg = _(u'Error: O voto não pode ser computado, tente novamente!')
    
    # MESSAGE & REDIRECT
    request.user.message_set.create(message=msg)
    return HttpResponseRedirect(next)
add_shortcut = staff_member_required(add_voto)
