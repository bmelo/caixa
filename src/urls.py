from django.conf.urls.defaults import *
import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
urlpatterns = patterns('',
    # Example:
    # (r'^sistema/', include('foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #(r'^admin/sispag/saldo_inicial/', 'sispag.views.saldo_inicial'),
    (r'^admin/sispag/abrir_caixa/', 'sispag.views.abrir_caixa'),
    (r'^admin/sispag/fechar_caixa/', 'sispag.views.fechar_caixa'),
    (r'^admin/sispag/retirada_caixa/', 'sispag.views.retirada_caixa'),
    (r'^admin/sispag/cadastro_cliente/', 'sispag.views.cadastro_cliente'),
    (r'^ferramentas/', include('ferramentas.urls')),
    (r'^admin/sispag/usuario/(?P<username>\w+)/$', 'sispag.views.perfil_usuario'),
    (r'^admin/sispag/cliente/', 'sispag.views.cliente'),
    (r'^admin/sispag/cliente_nome/', 'sispag.views.lista_clientes_nome'),
    (r'^admin/sispag/cliente_endereco/', 'sispag.views.lista_clientes_endereco'),
    (r'^admin/sispag/cliente_telefone/', 'sispag.views.lista_clientes_telefone'),
    (r'^admin/sispag/iniciar_venda/(?P<cliente>\d+)/$', 'sispag.views.cliente_iniciar_venda'),
    (r'^admin/sispag/venda/(?P<venda>\d+)/$', 'sispag.views.cliente_venda'),
    (r'^admin/sispag/finalizar_venda/(?P<venda>\d+)/$', 'sispag.views.cliente_finalizar_venda'),
    (r'^admin/sispag/cancelar_venda/(?P<venda>\d+)/$', 'sispag.views.cliente_cancelar_venda'),
    (r'^admin/sispag/venda_prazo/(?P<venda>\d+)/$', 'sispag.views.cliente_pagar_prazo'),
    (r'^admin/sispag/relatorio_cliente_atraso/', 'sispag.views.relatorio_cliente_atraso'),
    (r'^admin/sispag/relatorio_vendas/', 'sispag.views.relatorio_vendas'),
    (r'^admin/sispag/relatorio_entradas/', 'sispag.views.relatorio_entradas'),
    (r'^admin/sispag/relatorio_aniversariantes/', 'sispag.views.relatorio_aniversariantes'),


    (r'^admin/(.*)', admin.site.root),
    #(r'^salvar_mensagem/$', 'sispag.views.salvar_mensagem'),
    #(r'^boleto/', include('boleto.urls')),
    #(r'^financeiro/', include('financeiro.urls')),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
