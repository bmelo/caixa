# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django import forms
from django.forms.fields import EMPTY_VALUES
from django.contrib.auth.models import User, Group
from django.contrib.sites.models import Site
from django.template import Context, loader
from django.contrib.localflavor.br.forms import BRCPFField,BRStateChoiceField,BRPhoneNumberField,BRZipCodeField,BRCNPJField
from django.utils.translation import ugettext_lazy as _
from sispag.models import *
from django.forms.extras.widgets import SelectDateWidget
from django.forms.widgets import Widget
from django.contrib.admin.widgets import AdminDateWidget
from middleware import threadlocals



class EntradaEstoqueForm(ModelForm):
    
    def save(self, *args, **kwargs):
        quantidade = self.data.get('quantidade')
        est = self.data.get('estoque')
        try:
            estoque = Estoque.objects.get(id = int(est))
        except Estoque.DoesNotExist:
            estoque = []
        if estoque:
           estoque.quantidade = estoque.quantidade + int(quantidade)    
           estoque.save()    
        return super(EntradaEstoqueForm,self).save(*args, **kwargs)
    
    def clean_quantidade(self):
        quantidade = int(self.cleaned_data['quantidade'])
        if quantidade > 0:
            return self.cleaned_data['quantidade']
        raise forms.ValidationError(u'O valor deste campo só pode ser maior que zero')
    
    class Meta:
        model = EntradaEstoque
        exclude = ('data_hora')
      
class PessoaForm(ModelForm):
    telefone = BRPhoneNumberField(help_text = _("Formato de telefone xx-xxxx-xxxx "))
    celular = BRPhoneNumberField(required=False,help_text = _("Formato de celular xx-xxxx-xxxx "))
    cpf = BRCPFField(label='CPF',required=False)
    estado = BRStateChoiceField(initial = 'AL')
    naturalidade_estado = BRStateChoiceField(label='Estado',initial='AL')
    usuario = forms.RegexField(label=_("Username"), max_length=30, regex=r'^\w+$',
        help_text = _("Required. 30 characters or fewer. Alphanumeric characters only (letters, digits and underscores)."),
        error_message = _("This value must contain only letters, numbers and underscores."))       


    def __init__(self, *args, **kwargs):
        self.base_fields['data_nascimento'].widget = SelectDateWidget()
        super(PessoaForm, self).__init__(*args, **kwargs)

        
    def clean_usuario(self):
        
        queryset = User.objects.filter(username=self.cleaned_data['usuario'])
        if self.instance.id:
            queryset = queryset.exclude(pk=self.instance.user.id)
        if len(queryset) == 0:
            return self.cleaned_data['usuario']
        raise forms.ValidationError(u'Nome de usuário já cadastrado. Escolha outro.')

    def clean_rg(self):
        
        rg = self.cleaned_data['rg']
        if rg not in EMPTY_VALUES:
            
            try:
                int(rg)
            except ValueError:
                raise forms.ValidationError(u'O RG deve conter apenas números')
            length = len(rg)
            if length < 6:
                raise forms.ValidationError(u'Certifique-se de que o valor tenha mais que \
                                      7 caracters (ele possui %d)' % length)
            
            queryset = Pessoa.objects.filter(rg=self.cleaned_data['rg'])
            if len(queryset) == 0:
                return self.cleaned_data['rg']
            raise forms.ValidationError(u'Já existe uma Pessoa Física cadastrada com o RG: %s' % rg)
 
    def save(self, *args, **kwargs):
        if not self.instance.id:
            try:
                user = User.objects.get(username=self.data.get('usuario'))
            except User.DoesNotExist:
                user = []
            if user :
                self.instance.user = user
            else:
                u = User.objects.create_user(self.data.get('usuario'), self.data.get('email'), '123456')
                tipo = self.data.get('tipo')
                if tipo =='1':
                    grupo = Group.objects.filter(name='Administrador')
                    u.groups.add(grupo[0])  
                elif tipo == '2':
                    grupo = Group.objects.filter(name='Caixa')
                    u.groups.add(grupo[0])      
                elif tipo == '3':
                    grupo = Group.objects.filter(name='Cliente')
                    u.groups.add(grupo[0])                
                u.save()                
                self.instance.user = u
        else:
            self.instance.user.groups.clear()
            tipo = self.data.get('tipo')
            if tipo =='1':
                grupo = Group.objects.filter(name='Administrador')
                self.instance.user.groups.add(grupo[0])  
            elif tipo == '2':
                grupo = Group.objects.filter(name='Caixa')
                self.instance.user.groups.add(grupo[0])      
            elif tipo == '3':
                grupo = Group.objects.filter(name='Cliente')
                self.instance.user.groups.add(grupo[0])  
            self.instance.user.save()        
        return super(PessoaForm,self).save(*args, **kwargs)
    
    class Meta:
        model = Pessoa
        exclude = ('user')



class PessoaClienteForm(ModelForm):
    telefone = BRPhoneNumberField(help_text = _("Formato de telefone xx-xxxx-xxxx "))
    celular = BRPhoneNumberField(required=False,help_text = _("Formato de celular xx-xxxx-xxxx "))
    cpf = BRCPFField(label='CPF',required=False)
    estado = BRStateChoiceField(initial = 'AL')
    naturalidade_estado = BRStateChoiceField(label='Estado',initial='AL')
    usuario = forms.RegexField(label=_("Username"), max_length=30, regex=r'^\w+$',
        help_text = _("Required. 30 characters or fewer. Alphanumeric characters only (letters, digits and underscores)."),
        error_message = _("This value must contain only letters, numbers and underscores."))       

    def __init__(self, *args, **kwargs):
        self.base_fields['data_nascimento'].widget = SelectDateWidget()
        super(PessoaClienteForm, self).__init__(*args, **kwargs)
        
    def clean_usuario(self):
        
        queryset = User.objects.filter(username=self.cleaned_data['usuario'])
        if self.instance.id:
            queryset = queryset.exclude(pk=self.instance.user.id)
        if len(queryset) == 0:
            return self.cleaned_data['usuario']
        raise forms.ValidationError(u'Nome de usuário já cadastrado. Escolha outro.')

    def clean_rg(self):
        rg = self.cleaned_data['rg']
        if rg not in EMPTY_VALUES:
            
            try:
                int(rg)
            except ValueError:
                raise forms.ValidationError(u'O RG deve conter apenas números')
            length = len(rg)
            if length < 6:
                raise forms.ValidationError(u'Certifique-se de que o valor tenha mais que \
                                      7 caracters (ele possui %d)' % length)
            
            queryset = Pessoa.objects.filter(rg=self.cleaned_data['rg'])
            if len(queryset) == 0:
                return self.cleaned_data['rg']
            raise forms.ValidationError(u'Já existe uma Pessoa Física cadastrada com o RG: %s' % rg)
 
    def save(self, *args, **kwargs):
        if not self.instance.id:
            try:
                user = User.objects.get(username=self.data.get('usuario'))
            except User.DoesNotExist:
                user = []
            if user :
                self.instance.user = user
            else:
                u = User.objects.create_user(self.data.get('usuario'), self.data.get('email'), '123456')
                grupo = Group.objects.filter(name='Cliente')
                u.groups.add(grupo[0])                
                u.save()                
                self.instance.user = u
        else:
            self.instance.user.groups.clear()
            grupo = Group.objects.filter(name='Cliente')
            self.instance.user.groups.add(grupo[0])  
            self.instance.user.save()
                
        return super(PessoaClienteForm,self).save(*args, **kwargs)
    
    class Meta:
        model = Pessoa
        exclude = ('user','tipo','ativo')        
       

       
class RecadoForm(ModelForm):
    mensagem = forms.CharField(widget=forms.Textarea(attrs={'cols': 20, 'rows':5}))
    
    class Meta:
        model = Recado
        

class VendaPrazoForm(ModelForm):
    
    ''' def clean_valor_pago(self):
        if self.cleaned_data['valor_pago'] != 0.0:
            return self.cleaned_data['valor_pago']
        raise forms.ValidationError(u'Digite a quantia paga')
    '''
    def __init__(self, *args, **kwargs):
        self.base_fields['previsao_pagamento'].widget = SelectDateWidget()
        super(VendaPrazoForm, self).__init__(*args, **kwargs)

    
    class Meta:
        model = Venda
        exclude = ('data_venda','vendedor','cliente','total','troco','finalizada','aberto','data_pagamento','pagamento','parcelas')
        


class VendaOutrosForm(ModelForm):
    
    pagamento = forms.ChoiceField(choices=(((1,u'À vista'),(3,u'À cartão'))))

    def clean_valor_pago(self):
        if self.cleaned_data['valor_pago'] != 0.0:
            return self.cleaned_data['valor_pago']
        raise forms.ValidationError(u'Digite a quantia paga')
    
       
    class Meta:
        model = Venda
        exclude = ('data_venda','vendedor','cliente','total','troco','finalizada','aberto','data_pagamento','previsao_pagamento','parcelas')
 

class VendaForm(ModelForm):
    
    ''' def clean_valor_pago(self):
        if self.cleaned_data['valor_pago'] != 0.0:
            return self.cleaned_data['valor_pago']
        raise forms.ValidationError(u'Digite a quantia paga')
    '''
    def __init__(self, *args, **kwargs):
        self.base_fields['previsao_pagamento'].widget = SelectDateWidget()
        super(VendaForm, self).__init__(*args, **kwargs)

    
    class Meta:
        model = Venda
        exclude = ('data_venda','vendedor','cliente','total','troco','finalizada','aberto','data_pagamento')
        
class ProdutoVendasForm(ModelForm):
    
    def clean_quantidade(self):
        try:
            estoque = Estoque.objects.get(produto = self.cleaned_data['produto'])
        except Estoque.DoesNotExist:
            estoque = []
        if estoque:
            if int(self.cleaned_data['quantidade']) <= int(estoque.quantidade):
                if int(self.cleaned_data['quantidade']) != 0.0:
                    return self.cleaned_data['quantidade']
                raise forms.ValidationError(u'Digite a quantidade')
            raise forms.ValidationError(u'O estoque tem %d produtos, digite uma quantidade menor' % estoque.quantidade)
        else:
            raise forms.ValidationError(u'Este produto não consta no estoque, cadastre antes de efetuar a venda')
        
        
    
    class Meta:
        model = ProdutoVendas
        exclude = ('venda','valor')

class CaixaForm(ModelForm):
    
    class Meta:
        model = Caixa
        exclude = ('valor','situacao','usuario_abertura','data_hora_abertura','data_hora_fechamento','usuario_fechamento','estacao')

        
class RecargaForm(ModelForm):
    
    class Meta:
        model = Recarga
        exclude = ('venda','total')        

class RetiradaForm(ModelForm):
    
    
    
    '''def clean_valor(self):''
      try:
        estacao = EstacaoOperador.objects.get(operador__id = int(self.cleaned_data['usuario']))
      except EstacaoOperador.DoesNotExist:
        estacao = []
      if estacao:
          try:
              caixa = Caixa.objects.get(data_hora_abertura__year = int(datetime.datetime.today().year),data_hora_abertura__month = int(datetime.datetime.today().month),data_hora_abertura__day = int(datetime.datetime.today().day),situacao = '1',estacao = estacao.estacao)
          except Caixa.DoesNotExist:
              caixa = []
          if caixa:
              if float(self.cleaned_data['valor']) <= caixa.valor:
                  return self.cleaned_data['valor']
              raise forms.ValidationError(u'A quantida digitada excede a quantida que o caixa possui R$ %f'  % caixa.valor )
          raise forms.ValidationError(u'O caixa se encontra fechado, para fazer retirada favor abrir o caixa primeiro' ) 
      else:
          raise forms.ValidationError(u'O Usuario logado ainda não foi relacionado com nunhuma estação de trabalho' ) 
      '''
    
            
    class Meta:
        model = Retirada
        exclude = ('data_hora','usuario')
        

class ComentarioForm(ModelForm):
    mensagem = forms.CharField(widget=forms.Textarea(attrs={'cols': 20, 'rows':5}))
    
    class Meta:
        model = Comentario
