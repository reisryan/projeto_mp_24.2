from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth import logout
from .models import Produto, Barraca, Review
from django.db.models import Q

def index(request):
    return HttpResponse("Hello, world. You're at the feiras index.")

from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponse
from geopy.distance import geodesic


def index(request):
    if request.method == 'GET':
        return render(request, 'index.html')

'''
***************************************************************************
* Função: login
* Descrição:
* Realiza a autenticação do usuário com base no nome de usuário e senha
* recebidos via requisição HTTP POST.
*
* Parâmetros:
* request - objeto HttpRequest contendo os dados da requisição.
*
* Valor retornado:
* Página de login em caso de requisição GET.
* Redirecionamento para a página do consumidor ou feirante em caso de login bem-sucedido.
* Mensagem de erro em caso de falha na autenticação.
*
* Assertiva de entrada:
* request não é None.
* request é um objeto válido de HttpRequest.
* Se request.method == 'POST', então 'username' e 'password' devem estar em request.POST.
***************************************************************************
'''
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
            except Exception as e:
                return HttpResponse(f'Erro ao cadastrar usuário: {e}')
            else:
                user.save()
                HttpResponse('Usuario cadastrado com sucesso')
                return redirect('login')
            
def consumidor_page(request):
    if request.method == 'GET':
        username = request.GET['username']
        produtos = Produto.objects.all()
        barracas = Barraca.objects.all()
        produtos = calc_dist_user_barraca(request, produtos)
        return render(request, 'usuarioLogado.html', {'produtos': produtos, 'barracas': barracas})
        

def feirante_page(request):
    if request.method == 'GET':
        return render(request, 'feirante.html')
    
def search(request):
    # Obtemos o parâmetro de pesquisa da query string
    searched = request.GET.get('query', '')
    filtro = request.GET.get('filtro', '')
    categoria = request.GET.get('categoria', '')
    barraca_id = request.GET.get('barraca', '')

    produtos = Produto.objects.all()
    barracas = Barraca.objects.all()

    if barraca_id:
        produtos = produtos.filter(barraca_id=barraca_id)

    if searched:
        produtos = Produto.objects.filter(Q(nome__icontains=searched))
    
    if categoria:
        produtos = produtos.filter(tipo_produto=categoria)

     # Aplicar filtro de preço
    if filtro == 'menor_preco':
        produtos = produtos.order_by('preco')
    elif filtro == 'maior_preco':
        produtos = produtos.order_by('-preco')
    
    produtos = calc_dist_user_barraca(request , produtos)

    return render(request, 'usuarioLogado.html', {'produtos': produtos, 'barracas': barracas})

def calc_dist_user_barraca(request, produtos):
    user_location = (request.user.latitude, request.user.longitude)
    for produto in produtos:
        barraca_location = (produto.barraca.latitude, produto.barraca.longitude)
        produto.distancia = geodesic(user_location, barraca_location).miles
    return produtos

def logout_view(request):
    logout(request)  # Realiza o logout
    return redirect('login')  # Redireciona para a página de login (ou pode ser outra página)

def submit_review(request, produto_id):
    if request.method == 'POST' and request.user.is_authenticated:
        produto = Produto.objects.get(id=produto_id)
        nota = int(request.POST.get('nota'))
        comentario = request.POST.get('comentario', '')
        
        # Cria a avaliação
        Review.objects.create(
            user=request.user,
            produto=produto,
            nota=nota,
            comentario=comentario
        )
        
        # Atualiza a média
        reviews = produto.review_set.all()
        produto.nota_media = sum(r.nota for r in reviews) / reviews.count()
        produto.save()
        
    return redirect('consumidor_page')