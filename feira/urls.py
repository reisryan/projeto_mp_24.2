from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login, name="login"),
    path("cadastro/", views.cadastro, name="cadastro"),
    path("consumidor/", views.consumidor_page, name="consumidor_page"),
    path("feirante/", views.feirante_page, name="feirante_page"),
    path('search/', views.search, name='search'),
    path('submit_review/<int:produto_id>/', views.submit_review, name='submit_review'),
    path('logout/', views.logout_view, name='logout'),
]