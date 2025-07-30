from django import forms
from .models import Membros
from django.core.exceptions import ValidationError
from datetime import datetime
from django.utils.dateparse import parse_date

class MembrosForm(forms.ModelForm):
    class Meta:
        model = Membros
        fields = ['nome', 'cargo', 'estadocivil', 'profissao', 'escolaridade', 
                 'data_nascimento', 'data_batismo', 'data_casamento', 'cep', 'endereco', 'numero',
                 'bairro', 'cidade', 'estado', 'telefone', 'telefone_fixo', 'email', 'faixa_etaria']
        widgets = {
            'data_nascimento': forms.DateInput(format='%d/%m/%Y', attrs={'class': 'form-control', 'placeholder': 'dd/mm/yyyy', 'type': 'text'}),
            'data_batismo': forms.DateInput(format='%d/%m/%Y', attrs={'class': 'form-control', 'placeholder': 'dd/mm/yyyy', 'type': 'text'}),
            'data_casamento': forms.DateInput(format='%d/%m/%Y', attrs={'class': 'form-control', 'placeholder': 'dd/mm/yyyy', 'type': 'text'}),
            'cep': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_cep'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_endereco'}),
            'bairro': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_bairro'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_cidade'}),
            'estado': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_estado'}),
            'numero': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_numero'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cargo'].widget = forms.Select(choices=Membros.CARGOS_CHOICES)

    def clean_data_nascimento(self):
        data_nascimento = self.cleaned_data.get('data_nascimento')
        # A validação de formato é feita pelo DateField + widget + DATE_INPUT_FORMATS.
        # Aqui fazemos apenas a validação de negócio.
        if data_nascimento and data_nascimento > datetime.now().date():
            raise ValidationError('Data de nascimento não pode ser futura.')
        return data_nascimento

    def clean_data_batismo(self):
        data_batismo = self.cleaned_data.get('data_batismo')
        # A validação de formato é feita pelo DateField + widget + DATE_INPUT_FORMATS.
        # Adicione validações de negócio aqui se necessário.
        # Exemplo:
        # if data_batismo and data_batismo > datetime.now().date():
        #     raise ValidationError('Data de batismo não pode ser futura.')
        return data_batismo

    def clean_data_casamento(self):
        data_casamento = self.cleaned_data.get('data_casamento')
        # A validação de formato é feita pelo DateField + widget + DATE_INPUT_FORMATS.
        # Adicione validações de negócio aqui se necessário.
        # Exemplo:
        # if data_casamento and data_casamento > datetime.now().date():
        #     raise ValidationError('Data de casamento não pode ser futura.')
        return data_casamento