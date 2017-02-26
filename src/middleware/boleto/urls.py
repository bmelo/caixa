from django.conf.urls.defaults import *
from boleto.views import imagem_barras

urlpatterns = patterns('',
    # Example:
    # (r'^djboleto/', include('djboleto.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'imagem_barras/$', imagem_barras, name='imagem_barras'),
    (r'^bb/$', 'boleto.views.boleto_bb'),
    (r'^br/$', 'boleto.views.boleto_real'),
    (r'^bc/$', 'boleto.views.boleto_caixa'),
    (r'^bcs/$', 'boleto.views.boleto_caixa_sigcb'),
    (r'^bbd/$', 'boleto.views.boleto_bradesco'),
                       
)
