from django.http import HttpResponse
from django.contrib.auth.models import User

def index(request):
    return HttpResponse("Hello, world. You're at the feiras index.")

from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponse

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirecionar para a página inicial
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def cadastro(request):
    if request.method == 'GET':
        return render(request, 'cadastro.html')
    else:
        username = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        senha = request.POST['password']
        tipo_usuario = request.POST['user_type']

        user = User.objects.get(username=username, email=email, password=senha)
        if user:
            return HttpResponse('Já existe um usuário com esse email')
        else:
            '''user = User.objects.create_user(username, email, senha)
            user.save()
            return redirect('login')'''
        
        return HttpResponse('Usuário cadastrado com sucesso')