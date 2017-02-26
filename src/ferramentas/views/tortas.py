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
from django.utils.translation import ugettext as _
from sispag.models import *
from financeiro.models import *
import html5lib

import datetime
import cStringIO as StringIO
import ho.pisa as pisa
import cgi
import settings
import os
from openflashchart import graph as OpenFlashChartGraph, graph_object as OpenFlashChartObject


MESES = (
    ('Janeiro'),
    ('Fevereiro'),
    ('Marco'),
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




login_required = user_passes_test(lambda u: u.is_authenticated(),login_url='/sistema/admin')
cur_dir = os.path.dirname(os.path.abspath(__file__))

@login_required
def chart(request):
    title = u'Grafico Estatístico de Aproveitamento por Bimestre'
    if request.GET.get('pdf'):
        return render_to_pdf('admin/includes_ferramentas/tortas_pdf.html',locals())
    else:
        return render_to_response('admin/includes_ferramentas/tortas.html',locals(),context_instance=RequestContext(request))

@login_required
def chart2(request):
    title = u'Grafico Estatístico de Aproveitamento Geral'
    if request.GET.get('pdf'):
        return render_to_pdf('admin/includes_ferramentas/tortas2_pdf.html',locals())
    else:
        return render_to_response('admin/includes_ferramentas/tortas2.html',locals(),context_instance=RequestContext(request))

@login_required
def chart3(request):
    title = u'Grafico Estatístico de Faltas'
    if request.GET.get('pdf'):
        return render_to_pdf('admin/includes_ferramentas/tortas3_pdf.html',locals())
    else:
        return render_to_response('admin/includes_ferramentas/tortas3.html',locals(),context_instance=RequestContext(request))

@login_required    
def chart4(request):
    title = u'Grafico Estatístico de valores mensais das mensalidades'
    return render_to_response('admin/includes_ferramentas/tortas4.html',locals(),context_instance=RequestContext(request))

@login_required
def turmas(request):
    year = datetime.date.today().year
    turmas = DisciplinaProfessor.objects.filter(professor__user = request.user)
    turmas_id = []
    disciplinas_id = []
    for turma in turmas:
        turmas_id.append(turma.disciplina.turma)
        disciplinas_id.append(turma.disciplina.disciplina)
    title = u'Grafico Estatístico de Aproveitamento dos Alunos'
    if request.GET.get('disciplina'):
        disciplina = request.GET.get('disciplina')
        boletins = Boletim.objects.filter(ano_letivo__turma__in=turmas_id,disciplina__id = disciplina,ano_letivo__ano=year ) 
        return render_to_response('admin/includes_ferramentas/grafico_turma.html',locals(),context_instance=RequestContext(request))
    else: 
        boletins = Boletim.objects.filter(ano_letivo__turma__in=turmas_id,disciplina__in =  disciplinas_id,ano_letivo__ano=year ) 
        return render_to_response('admin/includes_ferramentas/turmas.html',locals(),context_instance=RequestContext(request))

@login_required
def estatistica_geral(request):
    ano = datetime.date.today().year
    mesCorrente = MESES[datetime.date.today().month -1]
    title = u'Grafico Estatístico de Pagamentos Anual'
    return render_to_response('admin/includes_ferramentas/estatistica_geral.html',locals(),context_instance=RequestContext(request))

@login_required
def estatistica_mensal(request):
    mesCorrente = datetime.date.today().month 
    meses = [] 
    for i in range(1,mesCorrente + 1):
        meses.append(MESES[i - 1])
    title = u'Grafico Estatístico de Pagamentos mensais'
    return render_to_response('admin/includes_ferramentas/estatistica_mensal.html',locals(),context_instance=RequestContext(request))

@login_required
def chart_estatistica_geral(request):
    mesCorrente = datetime.date.today().month 
    mesAnterior = mesCorrente -1  
    ano = datetime.date.today().year     
    mensalidades = Mensalidade.objects.filter(aluno__ano = ano)
    total = len(mensalidades)
    quites = 0
    data = []
    for mensalidade in mensalidades:
        meses_pago = MesPago.objects.filter(mensalidade=mensalidade.id)
        if mesAnterior == len(meses_pago) or mesCorrente == len(meses_pago):
            quites = quites + 1
    
    g = OpenFlashChartGraph()
   
           
    g.bg_colour = '#ffffff'
        
    data.append(quites*100/total)
    data.append((total - quites)*100/total)
    
    links = ["javascript:alert('%s')" %d for d in data]   
    g.pie(60,'#000000','{font-size: 12px; color: black;}',True,2)
    g.pie_values( data, ['Quites','Devendo'], links )  
    g.pie_slice_colours( ['#356aa0','#d01f3c'] )  
    g.set_tool_tip( '#val#%25' )  

    return HttpResponse(g.render())
            
@login_required
def chart_estatistica_mensal(request):
    mesCorrente = datetime.date.today().month 
    mesAnterior = mesCorrente -1  
    ano = datetime.date.today().year     
    mensalidades = Mensalidade.objects.filter(aluno__ano = ano)
    total = len(mensalidades)
    quites = 0
    data = []
    for mensalidade in mensalidades:
        meses_pago = MesPago.objects.filter(mensalidade=mensalidade.id, mes = int(request.GET.get('mes')))
        if meses_pago:
            quites = quites + 1
            
    g = OpenFlashChartGraph()
   
           
    g.bg_colour = '#ffffff'
        
    data.append(quites*100/total)
    data.append((total - quites)*100/total)
    
    links = ["javascript:alert('%s')" %d for d in data]   
    g.pie(60,'#000000','{font-size: 12px; color: black;}',True,2)
    g.pie_values( data, ['Quites','Devendo'], links )  
    g.pie_slice_colours( ['#356aa0','#d01f3c'] )  
    g.set_tool_tip( '#val#%25' )  

    return HttpResponse(g.render())        

@login_required
def chart_estatistica_mensal_valores(request):
    import random
    ano = datetime.date.today().year
    mesCorrente = datetime.date.today().month 
    g = OpenFlashChartGraph()
    data_1 = []
    meses = []
    valor = 0
    titulo = u'Grafico Estatístico de valores mensais das mensalidades'
    g.title(titulo.encode("utf-8"), '{color: #999999; font-size: 16; text-align: center}' );
    g.bg_colour = '#ffffff'
    
    for i in range(0,mesCorrente):
        meses.append(str(MESES[i]).encode( "utf-8" ))    
        meses_pago = MesPago.objects.filter(mensalidade__aluno__ano = ano, mes = i + 1 )
        for mes in meses_pago:
             valor = valor + mes.valor_pago
        data_1.append(valor)
        valor = 0        
  
    g.set_data( data_1 )
         
    g.line_dot( 3, 5,'#999900',ano, 11 )
            
    g.set_tool_tip( '#x_label#<br> Total : R$ #val#' )            
    g.set_x_labels([m for m in meses] )
    g.set_x_label_style( 11, '0x666666', 2, 1)

    g.set_y_max(max(data_1))
    g.y_label_steps(4)
    g.set_y_label_style( 10, '0x666666')

    return HttpResponse(g.render())

@login_required
def chart_data_turma(request):
    import random
    year = datetime.date.today().year
    g = OpenFlashChartGraph()
    disciplina = request.GET.get('disciplina')
    turma = DisciplinaProfessor.objects.get(disciplina__disciplina = disciplina, professor__user  = request.user)
    boletins = Boletim.objects.filter(ano_letivo__ano= year ,ano_letivo__turma = turma, disciplina__id = disciplina) 
    data_1 = []
    data_2 = []
    data_3 = []
    data_4 = []
    alunos = []
    titulo = u'Grafico Estatístico de Aproveitamento dos Alunos'
    g.title(titulo.encode("utf-8"), '{color: #999999; font-size: 16; text-align: center}' );
    g.bg_colour = '#ffffff'
    total = 10
    for boletim in boletins:
        if boletim.nota1:
            data_1.append(float(str(boletim.nota1))*100/total)
        else:
            data_1.append(0.0*100/total)
        if boletim.nota2:
            data_2.append(float(str(boletim.nota2))*100/total)
        else:
            data_2.append(0.0*100/total)
        if boletim.nota3:
            data_3.append(float(str(boletim.nota3))*100/total)
        else:
            data_3.append(0.0*100/total)
        if boletim.nota4:
            data_4.append(float(str(boletim.nota4))*100/total)
        else:
            data_4.append(0.0*100/total)
        alunos.append(boletim.ano_letivo.aluno.nome)
              
  
    g.set_data( data_1 )
    g.set_data( data_2 )
    g.set_data( data_3 )
    g.set_data( data_4 )

    
    g.line_dot( 3, 5,'#999900','1º Bimestre', 11 )
    g.line_dot( 3, 5,'#FF0000','2º Bimestre', 11 )        
    g.line_dot( 3, 5,'#663399','3º Bimestre', 11 )
    g.line_dot( 3, 5,'#0033CC','4º Bimestre', 11 )
                
    g.set_x_labels([aluno for aluno in alunos] )
    g.set_x_label_style( 11, '0x666666', 2, 1)
    g.set_tool_tip( '#x_label# (#key#)<br> Aproveitamento : #val#%25<br>'  )  
    g.set_y_max(100)
    g.y_label_steps(2)
    g.set_y_label_style( 10, '0x666666')

    return HttpResponse(g.render())


@login_required
def chart_data(request):

    import random
    year = datetime.date.today().year
    g = OpenFlashChartGraph()
    boletins = Boletim.objects.filter(ano_letivo__aluno__user=request.user,ano_letivo__ano= year).order_by('ano_letivo__ano','disciplina__nome')
    total = 10
    data_1 = []
    data_2 = []
    data_3 = []
    data_4 = []
    
    for boletim in boletins:
        if boletim.nota1:
            data_1.append(float(str(boletim.nota1))*100/total)
        else:
            data_1.append(0.0*100/total)
        if boletim.nota2:
            data_2.append(float(str(boletim.nota2))*100/total)
        else:
            data_2.append(0.0*100/total)
        if boletim.nota3:
            data_3.append(float(str(boletim.nota3))*100/total)
        else:
            data_3.append(0.0*100/total)
        if boletim.nota4:
            data_4.append(float(str(boletim.nota4))*100/total)
        else:
            data_4.append(0.0*100/total)
    
    titulo = u'Grafico Estatístico de Aproveitamento por Bimestre'
    g.title(titulo.encode( "utf-8" ), '{color: #999999; font-size: 16; text-align: center}' );
    g.bg_colour = '#ffffff'

    # we add 3 sets of data:
    g.set_data( data_1 )
    g.set_data( data_2 )
    g.set_data( data_3 )
    g.set_data( data_4 )
    
    g.bar_3d( 75, '#999900', '1º Bimestre', 10 )
    g.bar_3d( 75, '#33CCCC', '2º Bimestre', 10 )
    g.bar_3d( 75, '#663366', '3º Bimestre', 10 )
    g.bar_3d( 75, '#FF3300', '4º Bimestre', 10 )
    # we add the 3 line types and key labels
    
    g.set_x_axis_3d( 12 )

    g.set_x_labels([boletim.disciplina.nome.encode( "utf-8" ) for boletim in boletins] )
    g.set_x_label_style( 11, '0x666666', 2, 1)
    g.set_tool_tip( '#x_label# (#key#)<br> Aproveitamento : #val#%25<br>'  )  
    g.set_y_max(100)
    g.y_label_steps(2)
    g.set_y_label_style( 10, '0x666666')

    return HttpResponse(g.render())

@login_required
def chart_enquete(request):

    import random
    cores = ['#33CCCC', '#999900', '#663366','#FF3300', '0x666666' ]
    year = datetime.date.today().year
    g = OpenFlashChartGraph()
    enquetes = Opcoes.objects.select_related('enquete').filter(enquete__habilitada=True)
    data = []
    data_1 = []
    data_aux = []
    pergunta = ''
    perguntas = []
    tamanho = 0
    aux = []
    total = 0
    for enquete in enquetes:
        data_aux.append(int(enquete.votos))
        data_1.append(data_aux)
        data_aux = []
        data.append(enquete.opcao.encode( "utf-8" ))
        pergunta = str(enquete.enquete.pergunta.encode("utf-8"))
    
    for d in data_1:
        for da in d:
            total = total + da
    
    g.title(pergunta, '{color: #999999; font-size: 10; text-align: center}' );
    g.bg_colour = '#ffffff'
    perguntas.append(pergunta)
    data_aux = data_1[:]
    data_aux.sort()
    tamanho = data_aux.pop()
    tamanho = tamanho[0] 
    a = 0
    for d in data_1:
        a = d.pop()
        aux.append(a*100/total)
        g.set_data(aux)
        aux = []
    i = 0
    for d in data:
        g.bar_3d( 75, cores[i], str(d), 10 )
        i = i +1
    
    
    g.set_x_axis_3d( 12 )

    g.set_x_labels([u'Alternativas'])
    g.set_x_label_style( 10, '0x666666', 2, 1)
    g.set_tool_tip( '#key#<br> P.Votos : #val#%25' ) 
    
    g.set_y_max(100)
    g.y_label_steps(2)
    g.set_y_label_style( 10, '0x666666')

    return HttpResponse(g.render())

@login_required
def chart_data2(request):
    import random
    year = datetime.date.today().year
    g = OpenFlashChartGraph()
    boletins = Boletim.objects.filter(ano_letivo__aluno__user=request.user, ano_letivo__ano= year ).order_by('ano_letivo__ano','disciplina__nome')
    total = 10
    data_1 = []
    disciplinas = []
    titulo = u'Grafico Estatístico de Aproveitamento Geral'
    g.title(titulo.encode( "utf-8" ), '{color: #999999; font-size: 16; text-align: center}' );
    g.bg_colour = '#ffffff'

    for boletim in boletins:
        media1 = ''
        media2 = ''
        media = ''
        if boletim.nota1 and boletim.nota2 and not boletim.reavaliacao1  :
            media1 = (float(boletim.nota1)+float(boletim.nota2))/2
        elif boletim.nota1 and boletim.nota2 and boletim.reavaliacao1 :
            media1 = (((float(boletim.nota1)+float(boletim.nota2))/2) + float(boletim.reavaliacao1))/2
        if boletim.nota3 and boletim.nota4 and not boletim.reavaliacao2  :
            media2 = (float(boletim.nota3)+float(boletim.nota4))/2
        elif boletim.nota3 and boletim.nota4 and boletim.reavaliacao2 :
            media2 = (((float(boletim.nota3)+float(boletim.nota4))/2) + float(boletim.reavaliacao2))/2
        if media1 and media2:
            media = (media1 + media2)/2
        if media and boletim.reavaliacao_final:
            media = (media + boletim.reavaliacao_final)/2 
        if media:
            data_1.append((float(media)*100)/total)
        else:
            data_1.append(0.0*100/total)
        disciplinas.append(boletim.disciplina.nome.encode( "utf-8" ))         
  
    g.set_data( data_1 )

    
    g.line_dot( 3, 5,'#999900',year, 11 )
            
    g.set_tool_tip( '#x_label#<br> Aproveitamento : #val#%25' )            
    g.set_x_labels([d for d in disciplinas] )
    g.set_x_label_style( 11, '0x666666', 2, 1)

    g.set_y_max(100)
    g.y_label_steps(2)
    g.set_y_label_style( 10, '0x666666')

    return HttpResponse(g.render())

@login_required
def chart_data_pie(request):
    
    
    import random
    year = datetime.date.today().year
    g = OpenFlashChartGraph()
    boletins = Boletim.objects.filter(ano_letivo__aluno__user=request.user, ano_letivo__ano= year ).order_by('ano_letivo__ano','disciplina__nome')
    
    data_1 = []
    data_2 = []
    data_3 = []
    data = []
    
    g.bg_colour = '#ffffff'

    for boletim in boletins:
        media1 = ''
        media2 = ''
        media = ''
        if boletim.nota1 and boletim.nota2 and not boletim.reavaliacao1:
            media1 = (float(boletim.nota1)+float(boletim.nota2))/2
        elif boletim.nota1 and boletim.nota2 and boletim.reavaliacao1:
            media1 = (((float(boletim.nota1)+float(boletim.nota2))/2) + float(boletim.reavaliacao1))/2
        if boletim.nota3 and boletim.nota4 and not boletim.reavaliacao2:
            media2 = (float(boletim.nota3)+float(boletim.nota4))/2
        elif boletim.nota3 and boletim.nota4 and boletim.reavaliacao2:
            media2 = (((float(boletim.nota3)+float(boletim.nota4))/2) + float(boletim.reavaliacao2))/2
        if media1 and media2:
            media = (media1 + media2)/2
        if media and boletim.reavaliacao_final:
            media = (media + boletim.reavaliacao_final)/2
        if not media:
            media = 0;
        if media < 6 : data_1.append(media)
        elif media > 6 and  media <=8 :data_2.append(media)
        else: data_3.append(media)        
    
    total =  len(data_1) + len(data_2) + len(data_3)   
    data.append(len(data_1)*100/total)
    data.append(len(data_2)*100/total)
    data.append(len(data_3)*100/total)
    links = ["javascript:alert('%s')" %d for d in data]   
    g.pie(60,'#000000','{font-size: 12px; color: black;}',True,2)
    g.pie_values( data, ['Medias <6','Medias >6 e <8','Medias >8'], links )  
    g.pie_slice_colours( ['#d01f3c','#C79810', '#356aa0'] )  
    g.set_tool_tip( '#val#%25' )  
   


    return HttpResponse(g.render())

@login_required
def chart_data3(request):
    
    
    year = datetime.date.today().year
    g = OpenFlashChartGraph()
    boletins = Boletim.objects.filter(ano_letivo__aluno__user=request.user, ano_letivo__ano= year ).order_by('ano_letivo__ano','disciplina__nome')
    data_1 = []
    g.title('Grafico Estatistico de Faltas', '{color: #999999; font-size: 16; text-align: center}' );
    g.bg_colour = '#ffffff'

    for falta in boletins:
        faltas = 0
        if falta.f1:
            faltas = faltas + int(falta.f1)
        if falta.f2:
            faltas = faltas + int(falta.f2)
        if falta.f3:
            faltas = faltas + int(falta.f3)
        if falta.f4:
            faltas = faltas + int(falta.f4)
        data_1.append(faltas)   
            
  
    g.set_data( data_1 )

    g.line_dot( 3, 5,'#999900',year, 11 )
            
                
    g.set_x_labels([boletim.disciplina.nome.encode( "utf-8" ) for boletim in boletins] )
    g.set_x_label_style( 11, '0x666666', 2, 1)

    g.set_y_max(60)
    g.y_label_steps(4)
    g.set_y_label_style( 10, '0x666666')

    return HttpResponse(g.render())

@login_required
def chart_data4(request):
    import random
    
    g = OpenFlashChartGraph()
    boletins = Boletim.objects.filter(ano_letivo__aluno__user=request.user).order_by('ano_letivo__ano','disciplina__nome')
    
    data = []
    data_1 = []
    disciplinas = []
    ano = 0
    
    cor = ''
    g.title('Grafico Estatistico de Notas', '{color: #999999; font-size: 16; text-align: center}' );
    g.bg_colour = '#ffffff'

    for boletim in boletins:
        if ano == 0:
            ano = boletim.ano_letivo.ano
        if boletim.ano_letivo.ano != ano:
            ano = boletim.ano_letivo.ano 
            data.append(data_1)
            data_1 = []
            disciplinas = []
        data_1.append(boletim.nota_media)
        disciplinas.append(boletim.disciplina.nome.encode( "utf-8" ))         
    data.append(data_1)  
    for d in data:
        g.set_data( d )

    ano = 0
    for boletim in boletins:
        if boletim.ano_letivo.ano != ano:
            cor = '#'
            for i in range(6):
                cor += str(random.randint(0,9))
            g.line_dot( 3, 5, cor,boletim.ano_letivo.ano, 11 )
            ano = boletim.ano_letivo.ano
                
    g.set_x_labels([d for d in disciplinas] )
    g.set_x_label_style( 11, '0x666666', 2, 1)

    g.set_y_max(10)
    g.y_label_steps(4)
    g.set_y_label_style( 10, '0x666666')

    return HttpResponse(g.render())

@login_required
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
        response['Content-Disposition'] = 'filename=graficos.pdf'
        return response
    return http.HttpResponse('We had some errors<pre>%s</pre>' % cgi.escape(html))
