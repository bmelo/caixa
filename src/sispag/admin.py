# -*- coding: utf-8 -*-
from sispag.models import *
from django.contrib  import admin
from django import forms
from django.contrib.auth.models import User
from sispag.forms import *

    
class ProdutoVendasInline(admin.StackedInline):

    model = ProdutoVendas
    extra = 1
    classes = ('collapse-open',)

class PessoaAdmin(admin.ModelAdmin):

    fieldsets = [
        ('Informações Pessoais',{'fields': ['nome','sexo','cpf','rg','data_nascimento','foto']}),
        ('Tipo de Pessoa',{'fields': ['tipo']}),
        ('Naturalidade',{'fields': ['naturalidade_cidade','naturalidade_estado']}),
        ('Endereço',{'fields':['logradouro','bairro','cidade','estado','cep']}),
        ('Acesso',{'fields': ['usuario']}),
        ('Contato', {'fields': ['telefone','celular','email']}),
        ('Observação', {'fields': ['observacao']}),
        ('Situação', {'fields': ['ativo']}),
        ]
    list_display = ('id','user', 'nome', 'cpf', 'tipo_pessoa', 'sexo','ativo')
    list_filter = ['nome', 'tipo', 'sexo','ativo']
    search_fields = ['nome','cpf']
    form =PessoaForm
    list_per_page = 15
    
    def queryset(self, request):
        return Pessoa.objects.filter(ativo = True)
       
        

class OperadoraAdmin(admin.ModelAdmin):

    list_display = ('nome',)
    list_filter = ['nome',]
    list_per_page = 15

       
    class Meta:
        model = Operadora

class TipoProdutoAdmin(admin.ModelAdmin):

    list_display = ('nome',)
    list_filter = ['nome',]
    list_per_page = 15

    
    class Meta:
        model = TipoProduto

class ProdutoAdmin(admin.ModelAdmin):

    list_display = ('tipo','op','descricao','valor')
    list_filter = ['tipo']
    list_per_page = 15

    def op(self,obj):
      if obj.operadora:
        return str(obj.operadora.nome)
      return ''
    op.short_description = 'Operadora'
    
    class Meta:
        model = Produto

class VendaAdmin(admin.ModelAdmin):

    list_display = ('data_venda','vendedor','cliente','pagamento','parcelas','valor_pago','aberto')
    list_filter = ['data_venda','vendedor', 'cliente','pagamento','aberto']
    inlines = [ProdutoVendasInline]
    list_per_page = 15

    class Meta:
        model = Venda
        
class RetiradaAdmin(admin.ModelAdmin):

    list_display = ('valor','usuario','data_hora')
    list_filter = ['data_hora','usuario']
    list_per_page = 15
    
    class Meta:
        model = Retirada


class EstoqueAdmin(admin.ModelAdmin):

    list_display = ('produto','quantidade','data_hora')
    list_filter = ['produto','data_hora']
    list_per_page = 15
    
    class Meta:
        model = Estoque


class EntradaEstoqueAdmin(admin.ModelAdmin):

    list_display = ('estoque','quantidade','data_hora')
    list_filter = ['estoque','data_hora']
    list_per_page = 15
    form = EntradaEstoqueForm
    class Meta:
        model = EntradaEstoque
        
        
class CaixaAdmin(admin.ModelAdmin):

    list_display = ('valor_inicial','valor','situacao','usuario_abertura','usuario_fechamento','data_hora_abertura','data_hora_fechamento','estacao')
    list_filter = ['estacao']
    list_per_page = 15
    
    class Meta:
        model = Caixa
        
                
admin.site.register(Banner)
admin.site.register(Caixa,CaixaAdmin)
admin.site.register(Retirada,RetiradaAdmin)
admin.site.register(Estoque,EstoqueAdmin)
admin.site.register(EntradaEstoque,EntradaEstoqueAdmin)
admin.site.register(EstacaoOperador)
admin.site.register(EstacaoTrabalho)
admin.site.register(Pessoa,PessoaAdmin)
admin.site.register(Operadora,OperadoraAdmin)
admin.site.register(Produto, ProdutoAdmin)
admin.site.register(TipoProduto, TipoProdutoAdmin)
admin.site.register(Recado)
admin.site.register(Recarga)
admin.site.register(Venda,VendaAdmin)



