import sys
import subprocess

def install_packages():
    
    packages = [
        "pycodestyle", "pytest", "django", "pyflakes", "coverage", 
        "sphinx", "pytest-django", "selenium","webdriver-manager","geopy"
    ]
    
    try:
        # Atualiza o pip antes de instalar os pacotes
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        
        # Instala os pacotes necessários
        subprocess.check_call([sys.executable, "-m", "pip", "install"] + packages)
        print("\nTodas as bibliotecas foram instaladas com sucesso!")
    except subprocess.CalledProcessError:
        print("Erro ao instalar as bibliotecas. Verifique sua conexão com a internet e tente novamente.")

if __name__ == "__main__":
    install_packages()
