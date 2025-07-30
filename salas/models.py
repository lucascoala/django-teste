from django.db import models
from membros.models import Membros


class Salas(models.Model):
    CLASSE_4_6_ANOS = '4 a 6 anos'
    CLASSE_7_10_ANOS = '7 a 10 anos'
    CLASSE_JUNIORES = 'Juniores'
    CLASSE_ADOLESCENTES_JOVENS = 'Adolescentes e Jovens'
    CLASSE_CASAIS = 'Casais'
    CLASSE_NOVA_VIDA = 'Nova Vida'
    CLASSE_ADULTOS = 'Adultos'
    CLASSE_BERCARIO = 'Berçário'
    
    CLASSE_CHOICES = [
        (CLASSE_4_6_ANOS, 'Classe de 4 a 6 anos'),
        (CLASSE_7_10_ANOS, 'Classe de 7 a 10 anos'),
        (CLASSE_JUNIORES, 'Classe de Juniores'),
        (CLASSE_ADOLESCENTES_JOVENS, 'Classe de Adolescentes e Jovens'),
        (CLASSE_CASAIS, 'Classe de Casais'),
        (CLASSE_NOVA_VIDA, 'Classe Nova Vida'),
        (CLASSE_ADULTOS, 'Classe de Adultos'),
        (CLASSE_BERCARIO, 'Berçário'),
    ]
    
    professor = models.ForeignKey(Membros, on_delete=models.PROTECT, limit_choices_to={'cargo__in': [Membros.PROFESSOR, Membros.PRESBITERO, Membros.PASTOR, Membros.MEMBRO_ATIVO]}, related_name='salas_como_professor')
    data = models.DateField()
    alunos = models.ManyToManyField(Membros, through='Presenca', related_name='salas_como_aluno')
    licao_dada = models.TextField(blank=True)  # Tornando não obrigatório
    visitantes = models.TextField(blank=True, help_text='Registre os nomes dos visitantes, um por linha')
    classe = models.CharField(max_length=50, choices=CLASSE_CHOICES, verbose_name='Classe', help_text='Selecione a classe em que o professor estará lecionando')

    class Meta:
        verbose_name = "Sala"
        verbose_name_plural = "Salas"
        ordering = ['-data']  # Ordenação padrão

    def __str__(self):
        return f"{self.professor} - {self.data} - {self.licao_dada}"


class Presenca(models.Model):
    sala = models.ForeignKey(Salas, on_delete=models.CASCADE)
    aluno = models.ForeignKey(Membros, on_delete=models.CASCADE)
    presente = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Presença"
        verbose_name_plural = "Presenças"
        unique_together = ['sala', 'aluno']

    def __str__(self):
        return f"{self.aluno} - {self.sala.data} - {'Presente' if self.presente else 'Ausente'}"