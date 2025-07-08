from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import time
from faker import Faker  
from validate_docbr import CPF
from faker.providers import BaseProvider
import random
from faker import Faker
import string
from selenium.common.exceptions import TimeoutException
import sys
import subprocess
from selenium import webdriver
# Redireciona saída padrão e erros para o arquivo log.txt
sys.stdout = open("log.txt", "w", encoding="utf-8")
sys.stderr = sys.stdout  # Erros também vão para o mesmo arquivo


faker = Faker()
numero_aleatorio = random.randint(1, 100)  # Gera um número aleatório entre 1 e 100
letra_aleatoria = random.choice(string.ascii_uppercase)  # Gera uma letra maiúscula aleatória

import random
import string

def gerar_placa_aleatoria():
    if random.choice(["antigo", "mercosul"]) == "antigo":
        # Exemplo: ABC-1234
        letras = ''.join(random.choices(string.ascii_uppercase, k=3))
        numeros = ''.join(random.choices(string.digits, k=4))
        return f"{letras}-{numeros}"
    else:
        # Exemplo: ABC1D23 (Mercosul)
        letras = ''.join(random.choices(string.ascii_uppercase, k=3))
        meio = random.choice(string.digits)
        letra_final = random.choice(string.ascii_uppercase)
        fim = ''.join(random.choices(string.digits, k=2))
        return f"{letras}{meio}{letra_final}{fim}"

placa = gerar_placa_aleatoria()



tipos_combustivel = [
    "Gasolina Comum",
    "Gasolina Aditivada",
    "Etanol",
    "Diesel",
    "Diesel S10",
    "GNV (Gás Natural Veicular)",
    "Flex (Gasolina/Etanol)",
    "Elétrico",
    "Híbrido",
    "Biodiesel",
]
# Gera um tipo de combustível aleatório

from datetime import datetime, timedelta
import random

# Gera uma data de manutenção aleatória entre hoje e 30 dias atrás
data_manutencao = datetime.today() - timedelta(days=random.randint(0, 30))
data_manutencao_str = data_manutencao.strftime('%d/%m/%Y')

# Gera uma data de verificação entre a data de manutenção e até 30 dias depois
data_verificacao = data_manutencao + timedelta(days=random.randint(1, 30))
data_verificacao_str = data_verificacao.strftime('%d/%m/%Y')

import random
from datetime import datetime, timedelta

# Km verificado entre 10.000 e 200.000
km_verificado = random.randint(10000, 200000)

# Km após manutenção: entre +10 e +1000 km
km_apos_manutencao = km_verificado + random.randint(10, 1000)

# Data de verificação já gerada anteriormente (string dd/mm/yyyy)
# Exemplo de parsing se você tiver ela em string:
data_verificacao = datetime.strptime(data_verificacao_str, "%d/%m/%Y")

# Próximo check entre 30 e 120 dias depois da verificação
data_proximo_check = data_verificacao + timedelta(days=random.randint(30, 120))
data_proximo_check_str = data_proximo_check.strftime("%d/%m/%Y")



combustivel_escolhido = random.choice(tipos_combustivel)

cemetery_name = f"Cemitério {faker.last_name()} {faker.random.choice(['Eterno', 'da Paz', 'Memorial', 'Descanso'])}"

qtd_parcelas_em_atraso = int(faker.random.choice(['1', '2', '3', '4', '5']))

# Gerar um modelo fictício (você pode personalizar com nomes reais de veículos se quiser)
modelos = ["Fox", "Gol", "Uno", "Celta", "Civic", "Palio", "Corolla", "HB20"]
modelo = random.choice(modelos)

# Gerar ano aleatório entre 1995 e 2024
ano = str(random.randint(1995, 2024))

dias_para_exumar = int(faker.random.choice(['365', '730', '1095', '1460', '1825']))

def gerar_jazigos():
    quantidade_ruas = random.randint(1, 10)  # Ex: entre 1 e 10 ruas
    max_jazigos_por_rua = random.randint(1, 20)  # Ex: entre 1 e 20 jazigos por rua
    quantidade_total_jazigos = quantidade_ruas * max_jazigos_por_rua
    return quantidade_ruas, max_jazigos_por_rua, quantidade_total_jazigos

ruas, jazigos_por_rua, total_jazigos = gerar_jazigos()
altura_cm = random.randint(100, 200)
largura_cm = random.randint(100, 200)
comprimento_cm = random.randint(100, 200)
# Gera valor aleatório com centavos
valor_taxa_adesao = round(random.uniform(2000, 10000), 2)
cemetery_name = f"Cemitério {faker.last_name()} {faker.random.choice(['Eterno', 'da Paz', 'Memorial', 'Descanso'])}"

qtd_parcelas_em_atraso = int(faker.random.choice(['1', '2', '3', '4', '5']))


dias_para_exumar = int(faker.random.choice(['365', '730', '1095', '1460', '1825']))

'''Nesse teste, o robô preencherá apenas os Campos Obrigatórios e clicará em Salvar'''

print('Nesse teste, o robô preencherá apenas os Campos Obrigatórios e clicará em Salvar')



class BrasilProvider(BaseProvider):
    def rg(self):
        numeros = [str(random.randint(0, 9)) for _ in range(8)]
        return ''.join(numeros) + '-' + str(random.randint(0, 9))

fake = Faker("pt_BR")
fake.add_provider(BrasilProvider)  # Adiciona o provedor


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
campo_pesquisa.send_keys("Veículos")


elemento = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "/html/body/div[17]/ul/li[53]/a"))
)
elemento.click()

time.sleep(3)

cadastrar = driver.find_element(By.CSS_SELECTOR, "#fmod_10004 > div.wdTelas > div.telaInicial.clearfix.overflow.overflowY > ul > li:nth-child(1) > a > span")
cadastrar.click()

time.sleep(1)


nome_veiculo = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "#fmod_10004 > div.wdTelas > div > div.catWrapper > div > div > div > div > div:nth-child(2) > input"))
)
nome_veiculo.send_keys('TESTE VEÍCULO SELENIUM AUTOMATIZADO')


campo_placa = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "#fmod_10004 > div.wdTelas > div > div.catWrapper > div > div > div > div > div:nth-child(8) > input")) 
)
campo_placa.click()
campo_placa.send_keys(placa)
campo_placa.send_keys(placa)

# Clique no botão "Salvar"
Salvar = driver.find_element(By.CSS_SELECTOR, "#fmod_10004 > div.wdTelas > div.telaCadastro.clearfix > div.btnHolder > a.btModel.btGray.btsave")
Salvar.click()
time.sleep(1)

# Fechar modal
X = driver.find_element(By.CSS_SELECTOR, "#fmod_10004 > div.wdTop.ui-draggable-handle > div.wdClose > a")
X.click()
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




