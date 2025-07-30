from django.db import models

from django.db import models

class Missao(models.Model):
    nome_missionario = models.CharField(max_length=100)
    local = models.CharField(max_length=100)
    valor_aplicado = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nome_missionario