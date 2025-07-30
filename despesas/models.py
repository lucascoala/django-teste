from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Despesas(models.Model):
    TIPO_CHOICES = [
        ('Fixa', 'Despesa Fixa'),
        ('Variável', 'Despesa Variável'),
        ('Eventual', 'Despesa Eventual'),
    ]

    DESPESAS_CHOICES = [
        # 50 - DESPESA COM PESSOAL
        ('5001', 'Côngruas - Pastor'),
        ('5002', 'Férias + 1/3 - Pastor'),
        ('5003', 'Décimo Terceiro - Pastor'),
        ('5004', 'FAP - Pastor'),
        ('5005', 'INSS - Pastor'),
        ('5006', 'Moradia - Pastor'),
        ('5007', 'Assistência Médica - Pastor'),
        ('5008', 'Transporte - Pastor'),
        ('5009', 'Outras Despesas Com Pastor'),
        # Evangelista
        ('5011', 'Côngruas - Evangelista'),
        ('5012', 'Férias + 1/3 - Evangelista'),
        ('5013', 'Décimo Terceiro - Evangelista'),
        ('5014', 'FAP - Evangelista'),
        ('5015', 'INSS - Evangelista'),
        ('5016', 'Moradia - Evangelista'),
        ('5017', 'Assistência Médica - Evangelista'),
        ('5018', 'Transporte - Evangelista'),
        ('5019', 'Outras Despesas Com Evangelista'),
        # Seminarista
        ('5021', 'Seminário DNE'),
        ('5022', 'Moradia e Alimentação - Seminarista'),
        ('5023', 'Transporte - Seminarista'),
        ('5029', 'Outras Despesas Com Seminarista'),
        # Administrativo
        ('5031', 'Salário - Administrativo'),
        ('5032', 'Férias + 1/3 - Administrativo'),
        ('5033', 'Décimo Terceiro - Administrativo'),
        ('5034', 'FGTS'),
        ('5035', 'INSS - Administrativo'),
        ('5036', 'Assistência Médica/Odontológica'),
        ('5037', 'Outros Encargos'),
        ('5038', 'Transporte e Alimentação'),
        ('5039', 'Outras Despesas Com Administrativo'),
        # 51 - PRESBITÉRIO E SUPREMO CONCÍLIO
        ('5100', 'Dízimo Supremo Concílio'),
        ('5110', 'Dízimo Presbitério'),
        ('5190', 'Outras Despesas Com PRTI e SC'),
        # 52 - MISSÕES, EVANGELISMO E FILANTROPIA
        ('5200', 'Proventos'),
        ('5210', 'Ofertas'),
        ('5220', 'Transporte'),
        ('5230', 'Cesta Básica / Alimentação'),
        ('5240', 'Hospedagem'),
        ('5250', 'Eventos e Datas Comemorativas'),
        ('5260', 'Junta Diaconal'),
        ('5290', 'Outras Despesas Missões'),
        # 53 - SOCIEDADES INTERNAS
        ('5300', 'Escola Bíblica Dominical'),
        ('5310', 'Ministério Infantil'),
        ('5320', 'Ministério de Jovens e Adolescentes'),
        ('5330', 'Ministério de Casais'),
        ('5340', 'Ministério de Homens'),
        ('5350', 'Ministério de Mulheres'),
        ('5360', 'Ministério de Células'),
        ('5370', 'Ministério de Louvor'),
        ('5390', 'Outras Sociedades'),
        # 54 - LOCAÇÕES E SERVIÇOS PÚBLICOS
        ('5400', 'Energia Elétrica'),
        ('5410', 'Água e Esgoto'),
        ('5420', 'Telefonia e Internet'),
        ('5430', 'Correios'),
        ('5440', 'Aluguel de Equipamento'),
        ('5450', 'Aluguel de Imóvel'),
        ('5460', 'Aluguel de Veículo'),
        ('5490', 'Outras Locações e Serviços Públicos'),
        # 55 - SERVIÇOS CONTRATADOS
        ('5500', 'Limpeza'),
        ('5510', 'Manutenção Predial'),
        ('5520', 'Manutenção Equipamentos'),
        ('5530', 'Frete/Transporte'),
        ('5540', 'Contador'),
        ('5550', 'Reprografia e Publicidade'),
        ('5590', 'Outros Serviços Contratados'),
        # 56 - DESPESAS COM MATERIAIS
        ('5600', 'Material de Escritório'),
        ('5610', 'Material de Expediente'),
        ('5620', 'Material de Limpeza'),
        ('5630', 'Material Manutenção Predial'),
        ('5640', 'Material Manutenção Equipamento'),
        ('5650', 'Combustível'),
        ('5660', 'Literatura e Publicações'),
        ('5690', 'Outros Materiais'),
        # 57 - DESPESAS FINANCEIRAS
        ('5700', 'Manutenção de Conta'),
        ('5710', 'Tarifa Bancária'),
        ('5720', 'Juros e Multas'),
        ('5730', 'Outras Despesas Financeiras'),
        # 58 - IMOBILIZADO
        ('5800', 'Móveis e Utensílios'),
        ('5810', 'Sonorização e Instrumentos'),
        ('5820', 'Máquinas e Equipamentos'),
        ('5830', 'Veículos'),
        ('5840', 'Imóveis'),
        ('5850', 'Construções e Benfeitorias'),
        ('5890', 'Outros Imobilizados'),
    ]

    FORMA_PAGAMENTO_CHOICES = [
        ('Dinheiro', 'Dinheiro'),
        ('PIX', 'PIX'),
        ('Cartão Débito', 'Cartão Débito'),
        ('Cartão Crédito', 'Cartão Crédito'),
        ('Transferência', 'Transferência'),
    ]

    STATUS_CHOICES = [
        ('Pendente', 'Pendente'),
        ('Pago', 'Pago'),
        ('Atrasado', 'Atrasado'),
        ('Cancelado', 'Cancelado'),
    ]

    descricao = models.CharField(max_length=200, verbose_name="Descrição")
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_vencimento = models.DateField(verbose_name="Data de Vencimento")
    data_pagamento = models.DateField(verbose_name="Data de Pagamento", null=True, blank=True)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    clc = models.CharField(max_length=4, choices=DESPESAS_CHOICES, verbose_name="Classe de Custo")
    forma_pagamento = models.CharField(max_length=20, choices=FORMA_PAGAMENTO_CHOICES, verbose_name="Forma de Pagamento")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pendente')
    comprovante = models.FileField(upload_to='comprovantes/despesas/', null=True, blank=True)
    observacao = models.TextField(verbose_name="Observação", blank=True)
    usuario_cadastro = models.ForeignKey(User, on_delete=models.PROTECT)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    ultima_alteracao = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Despesa"
        verbose_name_plural = "Despesas"
        ordering = ['-data_vencimento']

    def __str__(self):
        return f"{self.descricao} - R$ {self.valor} - {self.data_vencimento}"

    def save(self, *args, **kwargs):
        if self.status == 'Pago' and not self.data_pagamento:
            self.data_pagamento = datetime.now()
        super().save(*args, **kwargs)

    @property
    def esta_atrasada(self):
        if self.status == 'Pendente' and self.data_vencimento < datetime.now().date():
            return True
        return False