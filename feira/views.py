from django.http import HttpResponse
from django.contrib.auth import get_user_model

def index(request):
    return HttpResponse("Hello, world. You're at the feiras index.")

from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponse

def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        username = request.POST['username']
        password = request.POST['password']

        # Autentica o usuário
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            # se for consumidor redireciona para a página do consumidor
            if user.tipo_user == 'CON':
                return redirect('consumidor_page')
            # se for feirante redireciona para a página do feirante
            else:
                return redirect('feirante_page')
        else:
            # Retorna uma mensagem de erro se a autenticação falhar
            return HttpResponse('Usuário ou senha incorretos')

def cadastro(request):
    if request.method == 'GET':
        return render(request, 'cadastro.html')
    else:
        username = request.POST['username']
        email = request.POST['email']
        phone = request.POST['telefone']
        senha = request.POST['password']
        tipo_usuario = request.POST['tipo_user']

        if get_user_model().objects.filter(username=username).exists():
            return HttpResponse('Usuário já cadastrado')
        else:
            try:
                user = get_user_model().objects.create_user(username=username, email=email, telefone=phone, password=senha, tipo_user=tipo_usuario)
            except:
                return HttpResponse('Erro ao cadastrar usuário')
            else:
                user.save()
                HttpResponse('Usuario cadastrado com sucesso')
                return redirect('login')
            
def consumidor_page(request):
    if request.method == 'GET':
        return render(request, 'usuarioLogado.html')

def feirante_page(request):
    if request.method == 'GET':
        return render(request, 'feirante.html')