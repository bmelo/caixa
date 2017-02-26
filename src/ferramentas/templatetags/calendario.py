from django import template
from django.core.paginator import Paginator, InvalidPage, EmptyPage
import settings
from sispag.models import *

register = template.Library()

def get_calendario(request):
   
    year = datetime.date.today().year
    calendario = Calendario.objects.filter(ano = year)
    MEDIA_URL = getattr(settings,'MEDIA_ROOT')
    xml  = open( MEDIA_URL + "flash/Eventos.xml","w")
    xml.write("<?xml version='1.0' encoding='utf-8'?>")
    xml.write("<events startDate='2008-01-01' endDate='2020-12-31'>")
    for cal in calendario:
        xml.write("<event title='" + str(cal.titulo.encode("utf-8"))+ "' description='" + str(cal.descricao.encode("utf-8"))+" ' id='" + str(cal.id)+ "' area='" + str(cal.tipo) +"' startDate='"  + str(cal.data_inicio) +"' endDate='"+ str(cal.data_fim) +"' allDay='1' eventType='once'>")
        xml.write("<pattern day='wed' week='3' recur='1' /></event>")
    
    xml.write("</events>")    
    # render template
    return {
        'xml': xml,
    }

register.inclusion_tag('admin/includes_ferramentas/calendario.html')(get_calendario)