from django.conf.urls.defaults import *

urlpatterns = patterns('',
    
    # SHORTCUTS
    (r'^favoritos/add/$', 'ferramentas.views.favoritos.add_favoritos'),
    (r'^favoritos/remove/$', 'ferramentas.views.favoritos.remove_favoritos'),
    #(r'^buscar_ficha_individual/$', 'ferramentas.views.ficha_individual.buscar_ficha_individual'),
    #(r'^buscar_ficha_individual_alunos/$', 'ferramentas.views.ficha_individual.get_alunos'),
    #(r'^buscar_ficha_individual_resultado/$', 'ferramentas.views.ficha_individual.get_resultados'),
    
    # GENERIC
    (r'^obj_lookup/$', 'ferramentas.views.generic.generic_lookup'),
    
    # FOREIGNKEY LOOKUP
    (r'^related_lookup/$', 'ferramentas.views.related.related_lookup'),
    (r'^m2m_lookup/$', 'ferramentas.views.related.m2m_lookup'),
    
)
