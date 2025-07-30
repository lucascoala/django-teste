from django import forms
from .models import Despesas
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit

class DespesasForm(forms.ModelForm):
    class Meta:
        model = Despesas
        fields = ['descricao', 'valor', 'data_vencimento', 'data_pagamento', 
                 'tipo', 'clc', 'forma_pagamento', 'status', 
                 'comprovante', 'observacao']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('descricao', css_class='form-group col-md-6'),
                Column('valor', css_class='form-group col-md-6'),
            ),
            Row(
                Column('data_vencimento', css_class='form-group col-md-6'),
                Column('data_pagamento', css_class='form-group col-md-6'),
            ),
            Row(
                Column('tipo', css_class='form-group col-md-4'),
                Column('clc', css_class='form-group col-md-4'),
                Column('forma_pagamento', css_class='form-group col-md-4'),
            ),
            Row(
                Column('status', css_class='form-group col-md-6'),
                Column('comprovante', css_class='form-group col-md-6'),
            ),
            'observacao',
            Submit('submit', 'Salvar', css_class='btn btn-primary')
        )