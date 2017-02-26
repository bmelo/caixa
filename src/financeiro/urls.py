from django.conf.urls.defaults import *

urlpatterns = patterns('',
    
    # SHORTCUTS
    (r'^data/$', 'financeiro.views.boleto'),  
    (r'^meses_atrasados/$', 'financeiro.views.mes_atraso'),  
)
