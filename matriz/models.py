from django.db import models

class MatrizGUT(models.Model):
    GRUPO_CHOICES = (
        ('G1', 'Grupo 1'),
        ('G2', 'Grupo 2'),
        ('G3', 'Grupo 3'),
        ('G4', 'Grupo 4'),
    )

    G_CHOICES = (
        (1, '1 - Muito Baixa'),
        (2, '2 - Baixa'),
        (3, '3 - Média'),
        (4, '4 - Alta'),
        (5, '5 - Muito Alta'),
    )

    nome = models.CharField(max_length=100, verbose_name="Problema", null=True)
    causa = models.CharField(max_length=100)
    grupo = models.CharField(max_length=2, choices=GRUPO_CHOICES)
    gravidade = models.IntegerField(choices=G_CHOICES)
    urgencia = models.IntegerField(choices=G_CHOICES)
    tendencia = models.IntegerField(choices=G_CHOICES)

    def _str_(self):
        return self.nome


class Matriz5W2H(models.Model):
    what = models.CharField(max_length=255)
    why = models.TextField()
    who = models.CharField(max_length=255)
    when = models.DateTimeField()
    where = models.CharField(max_length=255)
    how = models.TextField()
    how_much = models.DecimalField(max_digits=8, decimal_places=2)

    def _str_(self):
        return self.what