import pytest
from django.contrib.auth.models import User
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.contrib.auth import get_user_model
from django.test import Client


@pytest.mark.django_db
def test_admin_200(client):
    url = "/admin/login/?next=/admin/"
    response = client.get(url)
    assert response.status_code == 200

User = get_user_model()

@pytest.mark.django_db
def test_create_superuser():
    user = User.objects.create_superuser(
        username='admin',
        email='admin@dominio.com',
        password='naosei132'
    )

    assert user.username == 'admin'
    assert user.is_superuser is True
    assert user.is_staff is True
    assert user.check_password('naosei132') is True

@pytest.mark.django_db
def test_admin_preenche(client):
    user = User.objects.create_superuser(username='admin', email='admin@dominio.com', password='naosei132')
    client.force_login(user) 
    response = client.get('/admin/')
    assert response.status_code == 200

'''
@pytest.fixture(scope="function")
def browser():
    options = Options()
    options.add_argument("--headless") 

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    yield driver
    driver.quit() 

@pytest.mark.django_db
def test_admin_botao_login(browser, live_server):   
    User.objects.create_superuser(username='admin', email='admin@dominio.com', password='naosei132')

    login_url = f'{live_server.url}/admin/login/?next=/admin/'
    browser.get(login_url)
  
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.NAME, 'username'))).send_keys('admin')
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.NAME, 'password'))).send_keys('naosei132')

    WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, '//input[@type="submit"]'))).click()

    WebDriverWait(browser, 10).until(EC.url_contains('/admin/'))
    print("aaaaaaaaaaaaaa",browser.current_url)
    assert '/login/' not in browser.current_url
    assert '/admin/' in browser.current_url

@pytest.fixture(scope="function")
def logged_in_browser(browser, live_server):
    User.objects.create_superuser(username='admin', email='admin@dominio.com', password='naosei132')

    login_url = f'{live_server.url}/admin/login/?next=/admin/'
    browser.get(login_url)

    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.NAME, 'username'))).send_keys('admin')
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.NAME, 'password'))).send_keys('naosei132')
    WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, '//input[@type="submit"]'))).click()

    WebDriverWait(browser, 10).until(EC.url_contains('/admin/'))

    yield browser 

    browser.quit()


@pytest.mark.django_db
def test_cadastra_feira(logged_in_browser, live_server):
    logged_in_browser.get(f'{live_server.url}/admin/')

    feiras_link = WebDriverWait(logged_in_browser, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Feiras"))
    )
    feiras_link.click()

    WebDriverWait(logged_in_browser, 10).until(EC.url_contains('/feira/'))
    assert '/feira/' in logged_in_browser.current_url

@pytest.mark.django_db
def test_cadastra_barraca(logged_in_browser, live_server):
    logged_in_browser.get(f'{live_server.url}/admin/')

    barracas_link = WebDriverWait(logged_in_browser, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Barracas"))
    )
    barracas_link.click()

    WebDriverWait(logged_in_browser, 10).until(EC.url_contains('/barraca/'))
    assert '/barraca/' in logged_in_browser.current_url


@pytest.mark.django_db
def test_cadastra_produto(logged_in_browser, live_server):
    logged_in_browser.get(f'{live_server.url}/admin/')

    produtos_link = WebDriverWait(logged_in_browser, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Produtos"))
    )
    produtos_link.click()

    WebDriverWait(logged_in_browser, 10).until(EC.url_contains('/produto/'))
    assert '/produto/' in logged_in_browser.current_url
'''

@pytest.mark.django_db
def test_tela_login():
    client = Client()  # Instancia o cliente de teste do Django
    response = client.get("/feira/")  # Faz uma requisição GET à URL

    assert response.status_code == 200  # Verifica se a página carregou com sucesso
    assert "Bem vindo" in response.content.decode()  # Verifica se o texto está na página

@pytest.mark.django_db
def test_tela_cadastro():
    client = Client()  # Instancia o cliente de teste do Django
    response = client.get("/feira/cadastro/")  # Faz uma requisição GET à URL

    assert response.status_code == 200  # Verifica se a página carregou com sucesso
    assert "Bem vindo" in response.content.decode()  # Verifica se o texto está na página

import pytest
from django.test import Client

@pytest.mark.django_db
def test_cadastro_usuario():
    client = Client()

    # Dados do formulário simulando um cadastro
    form_data = {
        "username": "usuario_teste",
        "email": "teste@email.com",
        "telefone": "11999999999",
        "password": "SenhaForte123",
        "tipo_user": "CON",  # Ajustado para corresponder ao nome esperado no backend
    }

    # Envia o formulário via POST
    response = client.post("/feira/cadastro/", form_data)

    # Verifica se o cadastro foi bem-sucedido e redirecionou corretamente
    assert response.status_code in [200, 302]  # Aceita tanto 200 quanto 302
    assert response.url == "/feira/"  # Garante que o redirecionamento foi para a página esperada


@pytest.mark.django_db
def test_login_usuario():
    client = Client()

    # Criar usuário para o teste
    user = User.objects.create_user(
        username="usuario_teste",
        email="teste@email.com",
        password="SenhaForte123"
    )

    # Dados de login com tipo de usuário
    login_data = {
        "username": "usuario_teste",
        "password": "SenhaForte123",
        "tipo_usuario": "CON",  # Ajuste conforme necessário (FEI ou CON)
    }

    # URL de login (ajuste conforme necessário)
    login_url = "/feira/"

    # Acessa a página de login para verificar se existe
    response = client.get(login_url)
    assert response.status_code == 200, "Página de login não encontrada"

    # Enviar requisição POST para login
    response = client.post(login_url, login_data)

    # Verificar se o login foi bem-sucedido (código 200 ou redirecionamento 302)
    assert response.status_code in [200, 302], f"Erro no login: {response.status_code}"

    # Verificar se o usuário foi autenticado
    assert "_auth_user_id" in client.session, "Usuário não autenticado"

@pytest.mark.django_db
def test_logout(client):
    # Cria um superusuário
    user = User.objects.create_superuser(username="admin", email="admin@dominio.com", password="senha123")
    
    # Faz login
    assert client.login(username="admin", password="senha123"), "Falha no login."

    # Faz logout
    response = client.get("/feira/logout/")  

    # Verifica se houve redirecionamento
    assert response.status_code == 302, f"Esperado 302, mas recebeu {response.status_code}."

    # Confirma se redirecionou para a página correta
    assert response.url == "/feira/", f"Redirecionamento incorreto: {response.url}"

    # Confirma se o usuário foi deslogado
    assert "_auth_user_id" not in client.session, "Usuário ainda está logado."