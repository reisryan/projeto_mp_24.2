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