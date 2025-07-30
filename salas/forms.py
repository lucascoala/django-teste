from django import forms
from .models import Salas
from membros.models import Membros
from django.db.models import Q

class SalasForm(forms.ModelForm):
    
    class Meta:
        model = Salas
        fields = ['professor', 'data', 'classe', 'licao_dada', 'visitantes']
        widgets = {
            'data': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date',
                    'required': 'required'
                }
            ),
            'classe': forms.Select(
                attrs={
                    'class': 'form-control',
                    'required': 'required'
                }
            ),
            'visitantes': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                    'placeholder': 'Digite o nome dos visitantes, um por linha'
                }
            ),
            'licao_dada': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3
                }
            )
        }
    
    def __init__(self, *args, **kwargs):
        super(SalasForm, self).__init__(*args, **kwargs)
        # Filtra apenas professores
        self.fields['professor'].queryset = Membros.objects.filter(
            Q(cargo=Membros.MEMBRO_ATIVO) |
            Q(cargo=Membros.PRESBITERO) |
            Q(cargo=Membros.PASTOR)
        )
        self.fields['professor'].widget.attrs.update({'class': 'form-control select2'})