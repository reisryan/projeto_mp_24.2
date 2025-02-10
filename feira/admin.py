from django.contrib import admin
from .models import Feira, Barraca, Produto, User, Review, PesquisaUsuario, RelatorioAdministrador, Localizacao

# Register your models here.

admin.site.register(Feira)
admin.site.register(Barraca)
admin.site.register(Produto)
admin.site.register(User)
admin.site.register(Review)
admin.site.register(PesquisaUsuario)
admin.site.register(RelatorioAdministrador)
admin.site.register(Localizacao)