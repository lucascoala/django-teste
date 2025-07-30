from django import forms
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError
from .models import Perfil

class UsuarioForm(forms.ModelForm):
    password1 = forms.CharField(label='Senha', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmação de Senha', widget=forms.PasswordInput)
    grupo = forms.ModelChoiceField(queryset=Group.objects.all(), required=False, label="Grupo de Permissões")
    
    # Campos de permissões
    acesso_celulas = forms.BooleanField(required=False, initial=True)
    acesso_visitantes = forms.BooleanField(required=False, initial=True)
    acesso_membros = forms.BooleanField(required=False, initial=True)
    acesso_financeiro = forms.BooleanField(required=False, initial=True)
    acesso_salas = forms.BooleanField(required=False, initial=True)
    acesso_reunioes = forms.BooleanField(required=False, initial=True)
    acesso_matriz = forms.BooleanField(required=False, initial=True)
    acesso_missao = forms.BooleanField(required=False, initial=True)
    acesso_usuarios = forms.BooleanField(required=False, initial=True)
    acesso_despesas = forms.BooleanField(required=False, initial=True)
    acesso_contribuicoes = forms.BooleanField(required=False, initial=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError("As senhas não coincidem.")

        return cleaned_data

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError(f"O email ({email}) já está em uso.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])

        if commit:
            user.save()

            # Associando grupo
            grupo = self.cleaned_data.get('grupo')
            if grupo:
                user.groups.clear()  # Limpa grupos existentes antes de adicionar
                user.groups.add(grupo)

            # Criando ou atualizando perfil
            perfil, created = Perfil.objects.get_or_create(usuario=user)
            perfil.acesso_celulas = self.cleaned_data.get('acesso_celulas', True)
            perfil.acesso_visitantes = self.cleaned_data.get('acesso_visitantes', True)
            perfil.acesso_membros = self.cleaned_data.get('acesso_membros', True)
            perfil.acesso_financeiro = self.cleaned_data.get('acesso_financeiro', True)
            perfil.acesso_salas = self.cleaned_data.get('acesso_salas', True)
            perfil.acesso_reunioes = self.cleaned_data.get('acesso_reunioes', True)
            perfil.acesso_matriz = self.cleaned_data.get('acesso_matriz', True)
            perfil.acesso_missao = self.cleaned_data.get('acesso_missao', True)
            perfil.acesso_usuarios = self.cleaned_data.get('acesso_usuarios', True)
            perfil.acesso_despesas = self.cleaned_data.get('acesso_despesas', True)
            perfil.acesso_contribuicoes = self.cleaned_data.get('acesso_contribuicoes', True)
            perfil.save()

        return user
