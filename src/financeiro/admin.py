# -*- coding: utf-8 -*-
from financeiro.models import *
from django.contrib  import admin
from django import forms


class MesPagoInline(admin.StackedInline):
    
    model = MesPago
    extra = 1
    classes = ('collapse-open',)

class BoletoAdmin(admin.ModelAdmin):
    
    model = Boleto
    list_display = ('aluno',)
    search_fields = ['aluno__ano','aluno__aluno__nome']
      
    fieldsets = [
        ('Aluno',{'fields': ['aluno']}),
        ('Boletos',{'fields': ['boleto_janeiro','boleto_fevereiro','boleto_marco','boleto_abril','boleto_maio','boleto_junho','boleto_julho','boleto_agosto', 'boleto_setembro','boleto_outubro','boleto_novembro','boleto_dezembro']}),
    ]
    list_per_page = 15
    list_filter = ['aluno']    
    
class MensalidadeAdmin(admin.ModelAdmin):
    model = Mensalidade
    list_display = ('aluno','quites')
    search_fields = ['aluno__aluno__nome', 'aluno__ano']  
    list_filter = ['aluno']
    inlines = [MesPagoInline]
    def change_view(self, request, object_id, extra_context=None):

        result = super(MensalidadeAdmin, self).change_view(request, object_id, extra_context)

        document = Mensalidade.objects.get(id__exact=object_id)

        if not request.POST.has_key('_addanother') and not request.POST.has_key('_continue'):
            result['Location'] = '/sistema/admin/financeiro/mensalidade/'+object_id+'/'
        return result

class PagamentosDispesasAdmin(admin.ModelAdmin):
    model = PagamentosDispesas
    list_display = ('tipo','data','valor')
    search_fields = ['tipo__titulo', 'data','valor']  
    list_filter = ['tipo', 'data', 'valor']
    
admin.site.register(Mensalidade,MensalidadeAdmin)
admin.site.register(Boleto,BoletoAdmin)
admin.site.register(PagamentosDispesas,PagamentosDispesasAdmin)
admin.site.register(TipoDespesa)

