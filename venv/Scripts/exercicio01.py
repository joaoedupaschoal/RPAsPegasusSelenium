
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from time import sleep

# Instala automaticamente o ChromeDriver correto
service = Service(ChromeDriverManager().install())
navegador = webdriver.Chrome(service=service)

url = 'https://curso-python-selenium.netlify.app/exercicio_01.html#'
navegador.get(url)

sleep(1)

# Encontrando elementos
a = navegador.find_element(By.TAG_NAME, '<atributo="texto1">')
p = navegador.find_element(By.TAG_NAME,  '<atributo="texto2">')
 


print ({'texto1 ': {'<atributo="texto2">'}})
         






  


 