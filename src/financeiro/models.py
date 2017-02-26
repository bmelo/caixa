# -*- coding: utf-8 -*-
from django.db import models
from sispag.models import AnoLetivo
from financeiro.models import *
import datetime
from datetime import date
import math

MESES = (
        (1,'Janeiro'),
        (2,'Fevereiro'),
        (3,u'Março'),
        (4,'Abril'),
        (5,'Maio'),  
        (6,'Junho'), 
        (7,'Julho'), 
        (8,'Agosto'), 
        (9,'Setembro'), 
        (10,'Outubro'), 
        (11,'Novembro'), 
        (12,'Dezembro'), 
)

class Mensalidade(models.Model):
    aluno = models.ForeignKey(AnoLetivo)
    
    def ano(self):
        return self.aluno.ano_letivo
    
    def quites(self):
        mesCorrente = datetime.date.today().month
        mesAnterior = mesCorrente -1
        mensalidades = MesPago.objects.filter(mensalidade=self.id)
        if mesAnterior == len(mensalidades) or mesCorrente == len(mensalidades):
            return "OK"
        else:
            return u"Não"
        
    def __unicode__(self):
        return "Aluno: %s | Ano: %s" %(self.aluno.aluno.nome, self.aluno.ano) 

class MesPago(models.Model):
    
    
    mensalidade = models.ForeignKey(Mensalidade)
    mes = models.CharField(max_length=2, choices=MESES)   
    valor_pago = models.FloatField('Valor da Mensalidade',default=180.00)
    observacao = models.TextField(null=True,blank=True)  
    pago = models.BooleanField(editable=False)
    vencimento = models.DateField()
    porcentagem = models.FloatField('Taxa',default=0.15)
    data_pagamento = models.DateField()
    
    
    class Meta:
       unique_together = ['mensalidade','mes']
       verbose_name = 'Mensalidades'
       verbose_name_plural = 'Mensalidades'  
    
    def diffDate(self,data1, data2):
        d1 = data1
        d2 = data2
        delta = d2-d1
        r = delta.days 
        return r
    
    def calcularValor(self):
        vencimento = self.vencimento
        data_pagamento = self.data_pagamento
        dias = self.diffDate(data_pagamento,vencimento)
        valor = self.valor_pago
        juros = 0
        if dias < 0:
            dias = int(math.fabs(dias))
            juros = (valor*self.porcentagem)/100
            valor = valor + (juros*dias)    
        return valor
    
    def save(self):
        if self.mensalidade:
            self.pago = True  
        valor = self.calcularValor()
        self.valor_pago = valor
        super(MesPago, self).save()
          
    def __unicode__(self):
        return "Aluno: %s | MES/Ano: %s/%s" %(self.mensalidade.aluno.aluno.nome, self.mes,self.mensalidade.aluno.ano) 

class Boleto(models.Model):
    aluno = models.ForeignKey(AnoLetivo)  
    boleto_janeiro = models.ImageField('Boleto de janeiro',upload_to= 'boletos/',null=True, blank=True)
    boleto_fevereiro = models.ImageField('Boleto de fevereiro',upload_to= 'boletos/',null=True, blank=True)
    boleto_marco = models.ImageField('Boleto de março',upload_to= 'boletos/',null=True, blank=True)
    boleto_abril = models.ImageField('Boleto de abril',upload_to= 'boletos/',null=True, blank=True)
    boleto_maio = models.ImageField('Boleto de maio',upload_to= 'boletos/',null=True, blank=True)
    boleto_junho = models.ImageField('Boleto de junho',upload_to= 'boletos/',null=True, blank=True)
    boleto_julho = models.ImageField('Boleto de julho', upload_to= 'boletos/',null=True, blank=True)
    boleto_agosto = models.ImageField('Boleto de agosto',upload_to= 'boletos/',null=True, blank=True)
    boleto_setembro = models.ImageField('Boleto de setembro',upload_to= 'boletos/',null=True, blank=True)
    boleto_outubro = models.ImageField('Boleto de outubro',upload_to= 'boletos/',null=True, blank=True)
    boleto_novembro = models.ImageField('Boleto de novembro',upload_to= 'boletos/',null=True, blank=True)
    boleto_dezembro = models.ImageField('Boleto de dezembro',upload_to= 'boletos/',null=True, blank=True)
    
    def ano(self):
        return self.aluno.ano_letivo
    
    def __unicode__(self):
        return "Aluno: %s | Ano: %s" %(self.aluno.aluno.nome, self.aluno.ano) 
      
class TipoDespesa(models.Model):
    titulo = models.CharField(max_length=100) 
    
    def __unicode__(self):
        return self.titulo
    
class PagamentosDispesas(models.Model):   
    tipo = models.ForeignKey(TipoDespesa)
    data = models.DateField()
    valor = models.FloatField()
    observacao = models.TextField()
    
    class Meta:
       verbose_name = 'Pagamento Despesa' 
       verbose_name_plural = 'Pagamentos Despesas' 
       
    def __unicode__(self):
        return self.tipo.titulo 
# Create your models here.
