from django.db import models
from usuarios.models import Perfil
from django.contrib.auth.models import User



class Membros(models.Model):

    PASTOR = 'Pastor'
    PRESBITERO = 'Presbítero'
    DIACONO = 'Diácono'
    SECRETARIA = 'Secretaria'
    TESOUREIRO = 'Tesoureiro'
    MEMBRO_ATIVO = 'Membro Ativo'
    MEMBRO_INATIVO = 'Membro Inativo'
    VISITANTE = 'Visitante'
    PROFESSOR = 'Professor'

    CARGOS_CHOICES = [
        (PASTOR, 'Pastor'),
        (PRESBITERO, 'Presbítero'),
        (DIACONO, 'Diácono'),
        (SECRETARIA, 'Secretaria'),
        (TESOUREIRO, 'Tesoureiro'),
        (MEMBRO_ATIVO, 'Membro Ativo'),
        (MEMBRO_INATIVO, 'Membro Inativo'),
        (VISITANTE, 'Visitante'),
        (PROFESSOR, 'Professor'),

    ]

    ESTADOCIVIL_CHOICES = [
        ('Divorciado(a)', 'Divorciado(a)'),
        ('Solteiro(a)', 'Solteiro(a)'),
        ('Casado(a)', 'Casado(a)'),
        ('Viúvo(a)', 'Viúvo(a)'),
    ]

    ESCOLARIDADE_CHOICES = [
        ('Ensino fundamental incompleto', 'Ensino fundamental incompleto'),
        ('Ensino fundamental completo', 'Ensino fundamental completo'),
        ('Ensino médio incompleto', 'Ensino médio completo'),
        ('Superior completo (ou graduação)', 'Superior completo (ou graduação)'),
        ('Superior incompleto (ou graduação)', 'Superior incompleto (ou graduação)'),
    ]

    FAIXA_ETARIA_CHOICES = (
        ('Infantil' , 'Infantil') ,  
        ('Juvenil' , 'Juvenil') ,
        ('Juvenil1', 'Juvenil1') ,
        ('Adulto' , 'Adulto') ,
    )

    nome = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100, choices=CARGOS_CHOICES)
    faixa_etaria = models.CharField(max_length=20, choices=FAIXA_ETARIA_CHOICES, null=True, blank=True)
    estadocivil = models.CharField(max_length=40, choices=ESTADOCIVIL_CHOICES, verbose_name="Estado civil", null=True, blank=True)
    escolaridade = models.CharField(max_length=70, choices=ESCOLARIDADE_CHOICES, null=True, blank=True, verbose_name="Nível de escolaridade")
    data_nascimento = models.DateField(verbose_name="Data de nascimento", null=True, blank=True)
    profissao = models.CharField(max_length=100, verbose_name="Profissão", null=True, blank=True)
    data_batismo = models.DateField(null=True, blank=True, verbose_name="Data do batismo")
    data_recebimento = models.DateField(null=True, blank=True, verbose_name="Data de recebimento")
    cep = models.CharField(max_length=9, verbose_name="CEP", null=True, blank=True)
    endereco = models.CharField(max_length=200, verbose_name="Endereço", null=True, blank=True)
    numero = models.CharField(max_length=20, verbose_name="Número", null=True, blank=True)
    bairro = models.CharField(max_length=100, verbose_name="Bairro", null=True, blank=True)
    cidade = models.CharField(max_length=100, verbose_name="Cidade", null=True, blank=True)
    estado = models.CharField(max_length=2, verbose_name="Estado", null=True, blank=True)
    telefone = models.CharField(max_length=16, unique=True, null=True, blank=True)
    telefone_fixo = models.CharField(max_length=10, null=True, blank=True)
    email = models.EmailField(max_length=100, verbose_name="E-mail", null=True, blank=True)
    data_casamento = models.DateField(verbose_name="Data de casamento", null=True, blank=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} ({}) [{}]".format(self.nome, self.cargo, self.faixa_etaria)