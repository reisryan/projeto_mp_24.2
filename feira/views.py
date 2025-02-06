from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

def index(request):
    return HttpResponse("Hello, world. You're at the feiras index.")

def login_view(request):
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
    return render(request, 'front/login.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            #login(request, user)  # Loga o usuário após o cadastro
            return redirect('login')  # Redirecionar para a página inicial
    else:
        form = UserCreationForm()
    return render(request, 'front/signup.html', {'form': form})