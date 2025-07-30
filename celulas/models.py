from django.db import models

class Celulas(models.Model):
    lider = models.ForeignKey('membros.Membros', on_delete=models.CASCADE, verbose_name="Líder", null=True, blank=True)
    local = models.CharField(max_length=150, null=True, blank=True)
    dia_semana = models.DateField(verbose_name="Data", null=True, blank=True)
    descricao = models.TextField(max_length=200, verbose_name="Lição", null=True, blank=True)
    hora_incio = models.TimeField(verbose_name="Horário de íncio", null=True, blank=True)
    hora_fim = models.TimeField(verbose_name="Horário do fim", null=True, blank=True)
    quant_visitantes = models.IntegerField(verbose_name="Quantidade de visitantes", null=True, blank=True)
    quant_membros = models.IntegerField(verbose_name="Quantidade de membros", null=True, blank=True)

    def __str__(self):
        return "{} ({})".format(self.descricao)




