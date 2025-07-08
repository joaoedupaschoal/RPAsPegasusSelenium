from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from time import sleep
from pprint import pprint

# Configuração do WebDriver
service = Service(ChromeDriverManager().install())
browser = webdriver.Chrome(service=service)

# Abre a página
url = 'http://curso-python-selenium.netlify.app/aula_04.html'
browser.get(url)


def get_links(browser, elemento):
    """Pega todos os links dentro de um elemento"""
    
    resultado = {}

    element = browser.find_element(By.TAG_NAME, elemento)  # Usa o argumento `elemento`
    ancoras = element.find_elements(By.TAG_NAME, 'a')  # Busca dentro do elemento

    for ancora in ancoras:
        resultado[ancora.text] = ancora.get_attribute('href')

    return resultado  # Retorna o dicionário


aulas = get_links(browser, 'aside')

# Chama a função e imprime o resultado
sleep(2)


pprint(aulas)





exercicios = get_links(browser, 'main' )



pprint(exercicios)


browser.get(exercicios ['Exercício 3'])
browser.get()


# Aguarda permissão do usuário para fechar
input("Pressione Enter para fechar o navegador...")
browser.quit()
