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
    nome = models.CharField(max_length=100)
    longitude = models.FloatField()
    latitude = models.FloatField()

    def __str__(self):
        return self.nome

class Barraca(models.Model):
    nome = models.CharField(max_length=100)
    dono_user = models.ForeignKey(User, on_delete=models.CASCADE)
    longitude = models.FloatField()
    latitude = models.FloatField()
    feira = models.ForeignKey(Feira, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nome} - {self.feira.nome}"

class TipoProduto(models.Model):
    descricao = models.CharField(max_length=50)

    def __str__(self):
        return self.descricao

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    tipo_produto = models.ForeignKey(TipoProduto, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

class ProdutoBarraca(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    barraca = models.ForeignKey(Barraca, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('produto', 'barraca')

    def __str__(self):
        return f"{self.produto.nome} em {self.barraca.nome}"
