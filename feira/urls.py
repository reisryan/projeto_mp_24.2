from django.urls import path
from . import views

urlpatterns = [
    path("", views.login, name="login"),
    path("cadastro/", views.cadastro, name="cadastro"),
    path("consumidor/", views.consumidor_page, name="consumidor_page"),
    path("feirante/", views.feirante_page, name="feirante_page"),
]