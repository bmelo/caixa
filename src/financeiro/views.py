# Create your views here.
# -*- coding: utf-8 -*-
import sys
import site
site.addsitedir('/home/user/.python/lib')

from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth import authenticate,logout,login as authlogin
from django.contrib.auth.decorators import user_passes_test
from django.core.urlresolvers import reverse
from django.template import RequestContext,Context, loader
from django.shortcuts import render_to_response,get_object_or_404
from django import forms
from django.http import HttpResponse, HttpResponseServerError
from django.conf import settings
from financeiro.models import *
import html5lib

import datetime
import cStringIO as StringIO
import ho.pisa as pisa
import cgi

import os

login_required = user_passes_test(lambda u: u.is_authenticated(),login_url='/sistema/admin')
cur_dir = os.path.dirname(os.path.abspath(__file__))



MESES = (
    ('Janeiro'),
    ('Fevereiro'),
    (u'Março'),
    ('Abril'),
    ('Maio'),  
    ('Junho'), 
    ('Julho'), 
    ('Agosto'), 
    ('Setembro'), 
    ('Outubro'), 
    ('Novembro'), 
    ('Dezembro'), 
)

@login_required
def boleto(request):
   year = datetime.date.today().year
   meses = MESES
   title = u'Impressão de Boleto'
   try:
       boleto = Boleto.objects.get(aluno__aluno__user = request.user, aluno__ano = year )
   except BoletoDoesExist:
       boleto = []
   return render_to_response('admin/includes_ferramentas/boleto_data.html',locals(),context_instance=RequestContext(request))

@login_required
def mes_atraso(request):
    mesCorrente = datetime.date.today().month
    mensalidade = Mensalidade.objects.get(aluno__aluno__user = request.user)
    mensalidades = MesPago.objects.filter(mensalidade=mensalidade)
    meses = len(mensalidades)
    meses_atrazados = []
    for i in range(meses+1,mesCorrente):
        meses_atrazados.append(MESES[i - 1])
    title = u'Meses Atrasados'
    return render_to_response('admin/includes_ferramentas/meses_atrazados.html',locals(),context_instance=RequestContext(request))  
        

       
    