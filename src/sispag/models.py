# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.sites.models import Site
from django.template import Context, loader
from django.db import models, transaction
from django.utils.translation import ugettext as _
import settings
from django.db.models import signals
from django.dispatch import dispatcher
import datetime
import os

SEXO = (
    ('Masculino','Masculino'),
    ('Feminino','Feminino'),
)

TIPO = (
    ('1','Administrador'),
    ('2','Caixa'),
    ('3','Cliente'),
    ('4', 'Entregador')
)

PARCELAS = (
    (1,'1x'),
    (2,'2x'),
    (3,'3x'),
    (4,'4x'),
    (5,'5x'),
    (6,'6x'),
    (7,'7x'),
    (8,'8x'),
    (9,'9x'),
    (10,'10x'),
    (11,'11x'),
    (12,'12x'),
)

FORMAS_PAGAMENTO = ((1,u'À vista'),(2,'À prazo'),(3,u'À cartão'),)

class EstacaoTrabalho(models.Model):
    nome = models.CharField(max_length = 150)
    
    class Meta:
       verbose_name = 'Estação de Trabalho' 
       verbose_name_plural = 'Estações de Trabalho' 
       
    def __unicode__(self):
        return self.nome
   
class Pessoa(models.Model):
    nome = models.CharField(max_length=150)
    sexo = models.CharField(max_length=12,choices=SEXO)
    foto = models.ImageField(upload_to= 'fotos/',null=True, blank=True)
    cpf = models.CharField(max_length=14)
    rg = models.CharField(max_length=50,null=True, blank=True)
    user = models.OneToOneField(User,editable=False)
    usuario = models.CharField(max_length=30)
    telefone = models.CharField(max_length=12)
    tipo = models.CharField(max_length=1,choices=TIPO)
    celular = models.CharField(max_length=12,null=True,blank=True)
    naturalidade_cidade = models.CharField('Cidade',max_length=20,null=True,blank=True)
    naturalidade_estado = models.CharField('Estado',max_length=2,null=True,blank=True)
    email = models.EmailField(help_text='Digite um e-mail valido.',max_length=50,null=True,blank=True)
    data_nascimento = models.DateField('Data de Nascimento', null = True, blank = True)
    observacao = models.TextField('Observação',max_length=150, blank=True, null=True)
    ativo = models.BooleanField(default=True) 
    logradouro = models.CharField(max_length=200)
    bairro = models.CharField(max_length=50)
    cidade = models.CharField(max_length=30)
    estado = models.CharField(max_length=2)
    cep = models.CharField(max_length=9,blank=True, null=True)
    
    def tipo_pessoa(self):
        if self.tipo == '1':
            return "Administrador"
        
        elif self.tipo == '2':
            return u"Caixa"
        
        elif self.tipo == '3':
            return u"Cliente"
        else:
            return u'Entregador'

    def save(self):
        for field in self._meta.fields:
            if field.name == 'foto':
                field.upload_to = 'fotos/%s' % self.cpf   
        if self.ativo == True:
            self.user.is_staff = True
        else:
            self.user.is_staff = False
        self.user.save()
        self.nome = self.nome.upper()
        self.logradouro = self.logradouro.upper()
        self.cidade = self.cidade.upper()
        super(Pessoa, self).save()
        
    class Meta:
       verbose_name = 'Cadastro de Pessoa' 
       verbose_name_plural = 'Cadastros de Pessoas' 
           
    def __unicode__(self):
        return self.nome

class EstacaoOperador(models.Model):
    estacao = models.ForeignKey(EstacaoTrabalho)
    operador = models.ForeignKey(Pessoa, unique = True)
    
    class Meta:
       verbose_name = 'Estação Operador' 
       verbose_name_plural = 'Estações / Operadores' 
       
    def __unicode__(self):
        return self.operador.nome
    
class Operadora(models.Model):
    nome = models.CharField(max_length=100)

    def __unicode__(self):
        return self.nome
    
class TipoProduto(models.Model):    
    nome = models.CharField(max_length = 100) 
    def __unicode__(self):
        return self.nome



        
class Produto(models.Model):
    tipo = models.ForeignKey(TipoProduto)
    descricao = models.CharField('Descricao',max_length=200)
    valor = models.FloatField()
    
    def __unicode__(self):
        return u'%s  %s' %(self.tipo,self.descricao)



    
class Venda(models.Model):
    data_venda = models.DateTimeField(default = datetime.datetime.now())
    previsao_pagamento = models.DateField(default = datetime.date.today())
    data_pagamento = models.DateField(null=True, blank = True)
    vendedor = models.ForeignKey(Pessoa, related_name = 'vendedor_set')
    cliente = models.ForeignKey(Pessoa, null=True, blank=True, related_name = 'cliente_set')
    pagamento = models.CharField(max_length=2, choices = FORMAS_PAGAMENTO,default = 1)
    parcelas = models.CharField(max_length=2, choices = PARCELAS,default = 1)
    valor_pago = models.FloatField(default = 0)
    entregador =  models.ForeignKey(Pessoa, null=True, blank=True, related_name = 'entregador_set')
    total  = models.FloatField(default = 0)
    troco  = models.FloatField(default = 0)
    finalizada = models.BooleanField(default = False)
    dinheiro_recebido = models.BooleanField(default = False)
    aberto = models.BooleanField(default = False)
    
    def __unicode__(self):
        return str(self.data_venda)


class Recarga(models.Model):
    venda = models.ForeignKey(Venda)
    operadora = models.ForeignKey(Operadora)
    quantidade = models.IntegerField()
    valor = models.FloatField()
    total = models.FloatField()
    
    def __unicode__(self):
        return self.operadora.nome
    
class ProdutoVendas(models.Model):
    produto = models.ForeignKey(Produto)
    venda = models.ForeignKey(Venda)
    quantidade = models.IntegerField()
    valor = models.FloatField()

    def __unicode__(self):
        return self.produto.tipo.nome
        
class Banner(models.Model):
    banner = models.ImageField(upload_to= 'banners/')
    nome = models.CharField(max_length=200)
    data_publicacao = models.DateTimeField(default = datetime.datetime.now())
    
    def __unicode__(self):
        return self.data_publicacao

class Recado(models.Model):
    pessoa = models.ForeignKey(Pessoa)
    user = models.ForeignKey(User)
    mensagem = models.TextField()
    data_mensagem = models.DateTimeField(default = datetime.datetime.now())
    
    def pegar(self):
        pes = get_object_or_404(Pessoa,user = self.user)  
        return pes
     
    def __unicode__(self):
        return self.pessoa.nome
      


class Caixa(models.Model):
    valor_inicial = models.FloatField(max_length=200)
    valor = models.FloatField(max_length=200)
    situacao = models.CharField(max_length = 1, default = '0')
    usuario_abertura = models.ForeignKey(Pessoa, related_name = 'usuario_abertura_set')
    data_hora_abertura = models.DateTimeField(default = datetime.datetime.now)
    data_hora_fechamento = models.DateTimeField(null=True, blank= True)
    usuario_fechamento = models.ForeignKey(Pessoa, null=True, blank=True, related_name = 'usuario_fechamento_set')
    estacao = models.ForeignKey(EstacaoTrabalho)
    
    class Meta:
       verbose_name = u'Abert. / Fech. do Caixa'
       verbose_name_plural = u'Abert. / Fech. do Caixa'

    def __unicode__(self):
        return str(self.data_hora_abertura)
    
class Retirada(models.Model):
    valor = models.FloatField(max_length=200)
    usuario = models.ForeignKey(Pessoa)
    observacao = models.TextField()
    data_hora = models.DateTimeField(default = datetime.datetime.now, editable = False)
    
    def __unicode__(self):
        return str(self.data_hora)

class Estoque(models.Model):
    produto = models.ForeignKey(Produto,unique = True)
    quantidade = models.IntegerField(default = 0)
    data_hora = models.DateTimeField(default = datetime.datetime.now,editable = False, auto_now = True)
    
    def __unicode__(self):
        return self.produto.tipo.nome

class EntradaEstoque(models.Model):
    estoque = models.ForeignKey(Estoque)
    quantidade = models.IntegerField(default = 0)
    data_hora = models.DateTimeField(default = datetime.datetime.now,editable = False)
    
    def __unicode__(self):
        return self.estoque.produto.tipo.nome
      
class Comentario(models.Model):
    pessoa = models.ForeignKey(Pessoa)
    user = models.ForeignKey(User)
    mensagem = models.TextField()
    data_mensagem = models.DateTimeField(default = datetime.datetime.now())
    
    def pegar(self):
        pes = get_object_or_404(Pessoa,user = self.user)  
        return pes
     
    def __unicode__(self):
        return self.pessoa.nome
