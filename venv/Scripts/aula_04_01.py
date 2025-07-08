from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from time import sleep

# Instala automaticamente o ChromeDriver correto
service = Service(ChromeDriverManager().install())
navegador = webdriver.Chrome(service=service)

url = 'https://curso-python-selenium.netlify.app/aula_04_a.html'
navegador.get(url)

lista_n_ordenada = navegador.find_element(By.TAG_NAME, 'a')

lis  = lista_n_ordenada.find_element(By.TAG_NAME, 'li')


lis[0].navegador.find_element(By.TAG_NAME, 'a')