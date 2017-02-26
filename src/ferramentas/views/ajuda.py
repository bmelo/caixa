from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required

from ferramentas.models.ajuda import Ajuda, AjudaItem

def detalhe(request, object_id):
    
    obj = get_object_or_404(AjudaItem, pk=object_id)
    menu = Ajuda.objects.filter(ajudaitem__isnull=False).distinct()
    
    return render_to_response('ferramentas/ajuda/ajuda_detalhe.html', {
        'object': obj,
        'menu': menu,
        'titulo': obj.titulo,
    }, context_instance=RequestContext(request) )
detalhe = staff_member_required(detalhe)
    

def ajuda(request):
    
    menu = Ajuda.objects.filter(ajudaitem__isnull=False).distinct()
    
    return render_to_response('ferramentas/ajuda/ajuda.html', {
        'menu': menu,
        'titulo': 'Ajuda',
    }, context_instance=RequestContext(request) )
ajuda = staff_member_required(ajuda)
