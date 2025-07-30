from django.db import models



class Presbitero(models.Model):
    nome = models.TextField(max_length=200)
    cargo = models.CharField(max_length=100)
    data_ordem = models.DateField()

    def __str__(self):
        return self.nome
    
class ReuniaoConselho(models.Model):
    data = models.DateField()
    presbiteros = models.TextField(max_length=200, verbose_name="Presença",null=True)
    pauta = models.CharField(max_length=100)
    relatorio = models.TextField(verbose_name="Relatório")
    local = models.CharField(max_length=100)

    def __str__(self):
        return "Reunião do Conselho ({})".format(self.data)

class ReuniaoDiaconos(models.Model):
    diaconos = models.TextField(max_length=200, verbose_name="Presença", null=True)
    data = models.DateField()
    relatorio = models.TextField(verbose_name="Relatório")
    local = models.CharField(max_length=100)
    pauta = models.TextField()

    def __str__(self):
        return "Reunião dos Diaconos ({})".format(self.data)

