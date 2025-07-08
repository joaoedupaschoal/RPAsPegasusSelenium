from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from faker import Faker  # Importando o Faker
from validate_docbr import CPF
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import NoAlertPresentException
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
from faker.providers import BaseProvider
import random
from selenium.common.exceptions import TimeoutException
import sys
import subprocess
from selenium import webdriver
# Redireciona saída padrão e erros para o arquivo log.txt
sys.stdout = open("log.txt", "w", encoding="utf-8")
sys.stderr = sys.stdout  # Erros também vão para o mesmo arquivo

# Inicializando o Faker
fake = Faker()

class BrasilProvider(BaseProvider):
    def rg(self):
        numeros = [str(random.randint(0, 9)) for _ in range(8)]
        return ''.join(numeros) + '-' + str(random.randint(0, 9))

fake = Faker("pt_BR")
fake.add_provider(BrasilProvider)  # Adiciona o provedor

'''Nesse teste, o robô preencherá apenas os Campos Não Obrigatórios'''

print('Nesse teste, o robô preencherá apenas os Campos Não Obrigatórios')


URL = "http://localhost:8080/gs/index.xhtml"

def ajustar_zoom(driver):
    """ Ajusta o zoom da página sem interferir em outras guias. """
    driver.execute_script("document.body.style.zoom='90%'")

# Configuração do ChromeDriver
chrome_options = Options()
chrome_options.add_argument("--start-maximized")  # Maximiza a janela

# Inicializando o driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Acessa a URL
driver.get(URL)

# Espera até que o campo de login esteja presente
wait = WebDriverWait(driver, 10)
email_input = wait.until(EC.presence_of_element_located((By.ID, "j_id15:email")))
email_input.send_keys('joaoeduardo.gold@outlook.com')

password_input = wait.until(EC.presence_of_element_located((By.ID, "j_id15:senha")))
password_input.send_keys("071999gs", Keys.ENTER)

# Aguarda a página carregar
time.sleep(5)

ajustar_zoom(driver)
# Simula o pressionamento da tecla F2
driver.find_element(By.TAG_NAME, "body").send_keys(Keys.F2)
time.sleep(1)

time.sleep(5)

# Navegação inicial
campo_pesquisa = driver.find_element(By.XPATH, "//input[@placeholder='Busque um cadastro']")
campo_pesquisa.click()

# Digita um texto na pesquisa
campo_pesquisa.send_keys("Tipo de Contrato")

# Simula pressionar ENTER (se for necessário para pesquisar)
campo_pesquisa.send_keys(Keys.RETURN)

time.sleep(3)

cadastrar = driver.find_element(By.CSS_SELECTOR, "#fmod_10040 > div.wdTelas > div > ul > li:nth-child(1) > a > span")
cadastrar.click()

time.sleep(2)



driver.find_element(By.CSS_SELECTOR, "#fmod_10040 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div > div > div > div:nth-child(4) > input").send_keys('0')  

time.sleep(2)

wait = WebDriverWait(driver, 10)  # Espera até 10 segundos
element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#fmod_10040 > div.wdTelas > div.telaCadastro.clearfix > div.btnHolder > a.btModel.btGray.btsave")))
element.click()



wait = WebDriverWait(driver, 10)  # Espera até 10 segundos
element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#fmod_10040 > div.wdTop.ui-draggable-handle > div.wdClose > a")))
element.click()
time.sleep(1)



from selenium.common.exceptions import TimeoutException, NoSuchElementException

def encontrar_mensagem_alerta():
    seletores = [
        (".alerts.salvo", "sucesso"),
        (".alerts.alerta", "alerta"),
        (".alerts.erro", "erro"),
    ]

    for seletor, tipo in seletores:
        try:
            elemento = driver.find_element(By.CSS_SELECTOR, seletor)
            if elemento.is_displayed():  # garante que está visível
                print(f"Mensagem de {tipo}:", elemento.text)
                return elemento
        except NoSuchElementException:
            continue

    print("Nenhuma mensagem encontrada.")
    return None

# Espera apenas pelo container de alertas como um todo (melhora desempenho)
try:
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".alerts")))
    encontrar_mensagem_alerta()
except TimeoutException:
    print("Nenhum alerta apareceu dentro do tempo limite.")




print('Teste executado com sucesso!')
import sys
import subprocess
from selenium import webdriver
# Redireciona saída padrão e erros para o arquivo log.txt
sys.stdout = open("log.txt", "w", encoding="utf-8")
sys.stderr = sys.stdout  # Erros também vão para o mesmo arquivo

sys.stdout.close()
subprocess.run(["notepad", "log.txt"])
# Aguarda o usuário pressionar "." para fechar o navegador
print('Pressione "." para fechar o navegador...')
while True:
    if input() == ".":
        break  

# Espera 10 segundos antes de fechar (opcional)
time.sleep(3)

# Fecha o navegador
driver.quit()



