from django.db import models

class Visitantes(models.Model):
    data = models.DateField(verbose_name="Data da visita", null=True, blank=True)
    nome = models.CharField(max_length=50, unique=True, blank=False)  # Nome obrigatório
    endereco = models.CharField(max_length=100, verbose_name="Endereço", blank=True, null=True)
    filhos = models.CharField(max_length=16, verbose_name="Quantidade de filhos", blank=True, null=True)
    telefone = models.CharField(max_length=16, blank=True, null=True)

    def __str__(self):
        return "{}(Visitante)".format(self.nome)




