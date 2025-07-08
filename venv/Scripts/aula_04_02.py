from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from time import sleep

def find_by_href(browser, link):
    elementos = browser.find_elements(By.TAG_NAME, 'a')  # Obtém todos os links
    
    for elemento in elementos:
        href = elemento.get_attribute('href')  # Obtém o atributo href
        if href and link in href:
            return elemento  # Retorna o primeiro link encontrado

service = Service(ChromeDriverManager().install())
browser = webdriver.Chrome(service=service)

url = 'https://curso-python-selenium.netlify.app/aula_04_a.html'
browser.get(url)

# Testa a função buscando um link que contenha "ddg"
elemento_ddg = find_by_href(browser, 'ddg')

if elemento_ddg:
    print("Elemento encontrado:", elemento_ddg.text)
    elemento_ddg.click()

sleep(3)  # Espera um pouco para ver o resultado antes de fechar
browser.quit()

