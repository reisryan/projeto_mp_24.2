from django.contrib import admin
from .models import Feira, Barraca, Produto, ProdutoBarraca, TipoProduto, TipoUser, User, Review, PesquisaUsuario, RelatorioAdministrador

# Register your models here.

admin.site.register(Feira)
admin.site.register(Barraca)
admin.site.register(Produto)
admin.site.register(ProdutoBarraca)
admin.site.register(TipoProduto)
admin.site.register(TipoUser)
admin.site.register(User)
admin.site.register(Review)
admin.site.register(PesquisaUsuario)
admin.site.register(RelatorioAdministrador)