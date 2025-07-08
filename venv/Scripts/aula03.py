from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from time import sleep

# Instala automaticamente o ChromeDriver correto
service = Service(ChromeDriverManager().install())
navegador = webdriver.Chrome(service=service)

url = 'https://curso-python-selenium.netlify.app/aula_03.html#'
navegador.get(url)

sleep(1)

# Encontrando elementos
a = navegador.find_element(By.TAG_NAME, 'a')
p = navegador.find_element(By.TAG_NAME, 'p')

for click in range(10):
   ps = navegador.find_elements(By.TAG_NAME, 'p')
   a.click()
   print(f'Valor do último p: {ps[-1].text} valor do click: {click}')
   print(f'Os valores são iguais {ps[-1].text == str (click)}')



'''
# Mantém o navegador aberto até o usuário fechar manualmente
try:
    while True:
        sleep(1)  # Pequena pausa para evitar uso excessivo da CPU
except KeyboardInterrupt:
    print("Navegador fechado pelo usuário.")
   '''
   
navegador.quit()



