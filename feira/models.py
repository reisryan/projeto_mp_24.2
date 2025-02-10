from django.db import models
from django.contrib.auth.models import AbstractUser
from random import uniform
from math import radians, sin, cos

class Localizacao(models.Model):
    BASE_LATITUDE = -23.5505  # Exemplo: São Paulo
    BASE_LONGITUDE = -46.6333
    RADIUS_METERS = 200

    latitude = models.FloatField()
    longitude = models.FloatField()

    @staticmethod
    def gerar_localizacao():
        deslocamento_graus = Localizacao.RADIUS_METERS / 111000  # Aproximadamente 111 km por grau
        angulo = radians(uniform(0, 360))
        distancia = uniform(0, deslocamento_graus)

        latitude = Localizacao.BASE_LATITUDE + (distancia * sin(angulo))
        longitude = Localizacao.BASE_LONGITUDE + (distancia * cos(angulo)) / cos(radians(Localizacao.BASE_LATITUDE))
        
        return Localizacao.objects.create(latitude=latitude, longitude=longitude)

class User(AbstractUser):
    class TipoUser(models.TextChoices):
        ADMINISTRADOR = 'ADM', 'Administrador'
        FEIRANTE = 'FEI', 'Feirante'
        CONSUMIDOR = 'CON', 'Consumidor'
    
    base_user = TipoUser.ADMINISTRADOR
    tipo_user = models.CharField(max_length=3, choices=TipoUser.choices, default=base_user)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)

class Feira(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.nome

class Barraca(models.Model):
    nome = models.CharField(max_length=100)
    dono_user = models.ForeignKey(User, on_delete=models.CASCADE)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True)
    feira = models.ForeignKey(Feira, on_delete=models.CASCADE)
    observacoes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.nome} - {self.feira.nome}"

class Produto(models.Model):
    class TipoProduto(models.TextChoices):
        VESTIMENTA = 'VEST', 'Vestimenta'
        ACESSORIOS = 'ACES', 'Acessórios'
        TECNOLOGIA = 'TECN', 'Tecnologia'

    base_tipo_produto = TipoProduto.ACESSORIOS
    tipo_produto = models.CharField(max_length=4, choices=TipoProduto.choices, default=base_tipo_produto)
    barraca = models.ForeignKey(Barraca, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    nota_media = models.FloatField(default=0.0)

    def __str__(self):
        return self.nome

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, null=True, blank=True)
    barraca = models.ForeignKey(Barraca, on_delete=models.CASCADE, null=True, blank=True)
    nota = models.IntegerField()  # Escala de 1 a 5
    comentario = models.TextField(blank=True, null=True)
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review de {self.user.username} - Nota: {self.nota}"

class PesquisaUsuario(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    termo_pesquisa = models.CharField(max_length=255)
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} pesquisou '{self.termo_pesquisa}'"

class RelatorioAdministrador(models.Model):
    data_geracao = models.DateTimeField(auto_now_add=True)
    total_usuarios = models.IntegerField()
    termos_mais_pesquisados = models.TextField()
    locais_mais_populares = models.TextField()

    def __str__(self):
        return f"Relatório de {self.data_geracao.strftime('%Y-%m-%d')}"
