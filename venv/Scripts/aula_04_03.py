from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from time import sleep

def find_by_text(browser, tag, text):
    elementos = browser.find_elements(By.TAG_NAME, tag)  # Obtém todos os elementos da tag especificada
    
    for elemento in elementos:
        if elemento.text.strip() == text:  # Verifica se o texto é exatamente "quatro"
            return elemento  # Retorna o primeiro elemento encontrado

    return None  # Retorna None se não encontrar


# Configuração do WebDriver
service = Service(ChromeDriverManager().install())
browser = webdriver.Chrome(service=service)

# Abre a página
url = 'http://curso-python-selenium.netlify.app/aula_04_b.html'
browser.get(url)

# Aguarda a página carregar
sleep(2)

# Busca um <div> que contenha exatamente "quatro"

nomes_das_caixas = ['um', 'dois', 'tres', 'quatro']


for nome in nomes_das_caixas:
    elemento = find_by_text(browser, 'div', nome).click()  # Busca o elemento correto


for nome in nomes_das_caixas:
   sleep(0.3)
   browser.back()



for nome in nomes_das_caixas:
   sleep(0.3)   
   browser.forward()


# Aguarda permissão do usuário para fechar
input("Pressione Enter para fechar o navegador...")

browser.quit()
