# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.sites.models import Site
from django.template import Context, loader
from django.contrib.localflavor.br.forms import BRCPFField,BRStateChoiceField,BRPhoneNumberField,BRZipCodeField
from django.utils.translation import ugettext_lazy as _
from sispag.models import *


       
class PessoaForm(ModelForm):
    telefone = BRPhoneNumberField()
    celular = BRPhoneNumberField(required=False)
    cpf = BRCPFField(label='CPF')
    usuario = forms.RegexField(label=_("Username"), max_length=30, regex=r'^\w+$',
        help_text = _("Required. 30 characters or fewer. Alphanumeric characters only (letters, digits and underscores)."),
        error_message = _("This value must contain only letters, numbers and underscores."))
    
    
    def save(self, *args, **kwargs):
        if not self.instance.id:
            u = User.objects.create_user(self.data.get('usuario'), self.data.get('email'), '123456')
            tipo = self.data.get('tipo')
            if tipo == '2':
                grupo = Group.objects.filter(name='Professores')
                u.groups.add(grupo[0])                
            elif tipo == '3':
                grupo = Group.objects.filter(name='Alunos')
                u.groups.add(grupo[0])
            u.is_staff = True
            u.save()                
            self.instance.user = u
        return super(PessoaForm,self).save(*args, **kwargs)
    
    class Meta:
        model = Pessoa
        exclude = ('user')

        
class TurmaForm(ModelForm):
    professor = forms.ModelChoiceField(queryset=Pessoa.objects.filter(tipo='2'))
    
    class Meta:
        model = Turma

class DisciplinaProfessorForm(ModelForm):
    professor = forms.ModelChoiceField(queryset=Pessoa.objects.filter(tipo='2'))
    
    class Meta:
        model = DisciplinaProfessor

class AnoLetivoForm(ModelForm):
    aluno = forms.ModelChoiceField(queryset=Pessoa.objects.filter(tipo='3'))
    
    class Meta:
        model = AnoLetivo

        
class TurmaAlunoForm(ModelForm):
    aluno = forms.ModelChoiceField(queryset=Pessoa.objects.filter(tipo='3'))
    
    class Meta:
        model = TurmaAluno  
        
class EnderecoForm(ModelForm):
    cep = BRZipCodeField()
    estado = BRStateChoiceField(initial='AL')
    
    class Meta:
        model = Endereco  
