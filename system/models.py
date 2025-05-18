from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class Usuario(AbstractUser):
    GENEROS = (
        ('M', 'Masculino'),
        ('F', 'Feminino'),
    )

    TIMES = (
        ('azul', 'Azul'),
        ('roxo', 'Roxo'),
    )

    genero = models.CharField(max_length=1, choices=GENEROS)
    data_nascimento = models.DateField(null=True, blank=True)
    time = models.CharField(max_length=10, choices=TIMES)
    is_lider = models.BooleanField(default=False)
    is_adolescente = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class Evento(models.Model):
    DIAS_SEMANA = [
        ('sexta', 'Sexta-feira'),
        ('sabado', 'Sábado'),
        ('domingo', 'Domingo'),
        ('segunda', 'Segunda-feira'),
        ('terca', 'Terça-feira'),
        ('quarta', 'Quarta-feira'),
        ('quinta', 'Quinta-feira'),
    ]

    nome = models.CharField(max_length=100)
    data = models.DateField(null=True, blank=True)
    dia_semana = models.CharField(max_length=10, choices=DIAS_SEMANA, null=True, blank=True)
    horario = models.TimeField()
    local = models.CharField(max_length=100)
    eh_periodico = models.BooleanField(default=False)
    criador = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome


class Presenca(models.Model):
    adolescente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=[('sim', 'Compareci'), ('nao', 'Não fui')])
    data_resposta = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('adolescente', 'evento')  # Um evento por adolescente

