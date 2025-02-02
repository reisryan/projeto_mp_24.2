from django.db import models

class TipoUser(models.Model):
    descricao = models.CharField(max_length=50)

    def __str__(self):
        return self.descricao

class User(models.Model):
    tipo_user = models.ForeignKey(TipoUser, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    senha = models.CharField(max_length=128)  # Melhor usar Django's authentication system

    def __str__(self):
        return self.nome

class Feira(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    longitude = models.FloatField()
    latitude = models.FloatField()

    def __str__(self):
        return self.nome

class Barraca(models.Model):
    nome = models.CharField(max_length=100)
    dono_user = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'tipo_user__descricao': 'Feirante'})
    longitude = models.FloatField()
    latitude = models.FloatField()
    feira = models.ForeignKey(Feira, on_delete=models.CASCADE)
    observacoes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.nome} - {self.feira.nome}"

class TipoProduto(models.Model):
    descricao = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.descricao

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    tipo_produto = models.ForeignKey(TipoProduto, on_delete=models.CASCADE)
    nota_media = models.FloatField(default=0.0)

    def __str__(self):
        return self.nome

class ProdutoBarraca(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    barraca = models.ForeignKey(Barraca, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('produto', 'barraca')

    def __str__(self):
        return f"{self.produto.nome} em {self.barraca.nome}"

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
