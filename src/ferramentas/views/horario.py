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
from sispag.models import *
import html5lib

import datetime
import cStringIO as StringIO
import ho.pisa as pisa
import cgi

import os

login_required = user_passes_test(lambda u: u.is_authenticated(),login_url='/sistema/admin')
cur_dir = os.path.dirname(os.path.abspath(__file__))

@login_required
def mostrar_horario(request):
    year = datetime.date.today().year
    colegio = EscolaPrincipal.objects.filter(ativo=True)
    horarios = ''
    turmas = TurmaAluno.objects.filter(ano_letivo__aluno__user=request.user,turma__periodo__ano = year )
    for turma in turmas:
        horarios = Horario.objects.filter(horarioturma__turma=turma.turma, horarioturma__ano=year).order_by('horario')
    if request.GET.get('pdf'):
        return render_to_pdf('admin/includes_ferramentas/horario_pdf.html',locals())
    else:
        return render_to_response('admin/includes_ferramentas/horario.html',locals(),context_instance=RequestContext(request))


def render_to_pdf(template_src, context_dict):
    template = loader.get_template(template_src)
    context = Context(context_dict)
    html  = template.render(context)
    result = StringIO.StringIO()
    MEDIA_URL = getattr(settings,'MEDIA_ROOT')
    css = open(cur_dir +'/css/pisa.css').read()
    pdf = pisa.CreatePDF(StringIO.StringIO(html.encode("ISO-8859-1")), result,default_css=css)
    if not pdf.err:
        response = HttpResponse(result.getvalue(), mimetype='application/pdf')
        response['Content-Disposition'] = 'filename=historico.pdf'
        return response
    return http.HttpResponse('We had some errors<pre>%s</pre>' % cgi.escape(html))
