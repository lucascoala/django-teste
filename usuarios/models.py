from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

class Perfil(models.Model):
    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='perfil'
    )
    acesso_reunioes = models.BooleanField(default=False, null=False)
    acesso_celulas = models.BooleanField(default=False, null=False)
    acesso_visitantes = models.BooleanField(default=False, null=False)
    acesso_membros = models.BooleanField(default=False, null=False)
    acesso_financeiro = models.BooleanField(default=False, null=False)
    acesso_salas = models.BooleanField(default=False, null=False)
    acesso_matriz = models.BooleanField(default=False, null=False)
    acesso_missao = models.BooleanField(default=False, null=False)
    acesso_usuarios = models.BooleanField(default=False, null=False)
    acesso_despesas = models.BooleanField(default=False, null=False)
    acesso_contribuicoes = models.BooleanField(default=False, null=False)

    def __str__(self):
        return self.usuario.username if self.usuario else ''
