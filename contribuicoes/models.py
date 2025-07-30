from django.db import models


class Contribuicoes(models.Model):
    TIPO_TRANSFERENCIA = (
        ('TED', 'TED'),
        ('DOC', 'DOC'),
        ('PIX', 'PIX'),
        ('Cédula', 'Cédula'),
    )
    
    RECEITAS_CHOICES = (
        ('4100', 'Dízimo'),
        ('4200', 'Oferta'),
        ('4300', 'Oferta Missionária'),
        ('4400', 'Repasse Presbitério'),
        ('4500', 'Receita Financeira'),
        ('4600', 'Aluguel/Cessão'),
        ('4900', 'Outras Receitas'),
    )
    
    membro = models.ForeignKey('membros.Membros', on_delete=models.CASCADE, verbose_name="Membro")
    descricao = models.CharField(max_length=50, null=True, blank=True, verbose_name="Descrição da operação")
    codigo = models.CharField(max_length=10, null=True, blank=True, verbose_name="Código da operação")
    tipo_transferencia = models.TextField(choices=TIPO_TRANSFERENCIA, verbose_name="Tipo da transação")
    clc = models.CharField(max_length=4, choices=RECEITAS_CHOICES, verbose_name="Classe de Custo")
    valor = models.DecimalField(max_digits=19, decimal_places=2, verbose_name="Valor")
    data = models.DateField()

    def __str__(self):
        return "{}({})  do dia {} no valor de R$ {} do membro {}".format(
            self.descricao, self.codigo, self.data, self.valor, self.membro
        )

    class Meta:
        verbose_name = "Contribuição"
        verbose_name_plural = "Contribuições"