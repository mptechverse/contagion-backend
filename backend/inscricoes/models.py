from django.db import models
from django.conf import settings
from datetime import date


class Evento(models.Model):

    nome = models.CharField(max_length=255)

    data_inicio = models.DateTimeField()

    data_fim = models.DateTimeField()

    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome


class Inscricao(models.Model):

    TIPO = (
        ('primeira_vez', 'Primeira Vez'),
        ('servo', 'Servo'),
    )

    TAMANHO_CAMISA = (
        ('PP', 'PP'),
        ('P', 'P'),
        ('M', 'M'),
        ('G', 'G'),
        ('GG', 'GG'),
        ('XG', 'XG'),
    )

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    evento = models.ForeignKey(
        Evento,
        on_delete=models.CASCADE
    )

    tipo = models.CharField(
        max_length=28,
        choices=TIPO
    )

    nome_completo = models.CharField(
        max_length=255
    )

    idade = models.IntegerField(
        blank=True,
        null=True
    )

    data_nascimento = models.DateField()

    telefone = models.CharField(
        max_length=20
    )

    email = models.EmailField(
        blank=True,
        null=True
    )

    cidade = models.CharField(
        max_length=255
    )

    estado = models.CharField(
        max_length=100
    )

    tamanho_camisa = models.CharField(
        max_length=5,
        choices=TAMANHO_CAMISA
    )

    quer_servir = models.BooleanField(
        default=False
    )

    # =========================
    # IGREJA
    # =========================

    participa_igreja = models.BooleanField(
        default=False
    )

    igreja = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    pastor_lider = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    telefone_lider = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    tempo_igreja = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    # =========================
    # EMERGÊNCIA
    # =========================

    responsavel_nome = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    telefone_responsavel = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    parentesco = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    # =========================
    # SAÚDE
    # =========================

    alergias = models.TextField(
        blank=True,
        null=True
    )

    doencas_pre_existentes = models.TextField(
        blank=True,
        null=True
    )

    medicamentos_continuos = models.TextField(
        blank=True,
        null=True
    )

    restricoes_alimentares = models.TextField(
        blank=True,
        null=True
    )

    observacoes_medicas = models.TextField(
        blank=True,
        null=True
    )

    # =========================
    # OUTRAS INFORMAÇÕES
    # =========================

    como_conheceu = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    autoriza_imagem = models.BooleanField(
        default=False
    )

    observacoes = models.TextField(
        blank=True,
        null=True
    )

    criado_em = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.nome_completo

    def calcular_idade(self):

        hoje = date.today()

        return (
            hoje.year
            - self.data_nascimento.year
            - (
                (hoje.month, hoje.day)
                <
                (
                    self.data_nascimento.month,
                    self.data_nascimento.day
                )
            )
        )

    def save(self, *args, **kwargs):

        if self.data_nascimento:
            self.idade = self.calcular_idade()

        super().save(*args, **kwargs)