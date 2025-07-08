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

cemetery_name = f"Cemitério {faker.last_name()} {faker.random.choice(['Eterno', 'da Paz', 'Memorial', 'Descanso'])}"

qtd_parcelas_em_atraso = int(faker.random.choice(['1', '2', '3', '4', '5']))

from datetime import datetime, timedelta
import random

from datetime import datetime, timedelta
import random

from datetime import datetime, timedelta
import random

def gerar_dados_multa(intervalo_max_passado=30):
    """
    Gera dados completos de uma multa:
    - data_multa: entre hoje e X dias atrás
    - hora_multa: horário aleatório (HH:MM)
    - data_notificacao: de 0 a 5 dias após a multa
    - data_vencimento: de 10 a 20 dias após a multa
    - data_pagamento: entre notificação e vencimento

    Retorna um dicionário com todas as datas e hora no formato dd/mm/yyyy e HH:MM.
    """
    # Base da multa
    data_multa_dt = datetime.now() - timedelta(days=random.randint(0, intervalo_max_passado))

    # Gera hora no formato HH:MM
    hora = random.randint(0, 23)
    minuto = random.randint(0, 59)
    hora_multa_dt = f"{hora:02d}:{minuto:02d}"

    # Demais datas relacionadas
    data_notificacao_dt = data_multa_dt + timedelta(days=random.randint(0, 5))
    data_vencimento_dt = data_multa_dt + timedelta(days=random.randint(10, 20))
    data_pagamento_dt = random.choice([
        data_notificacao_dt + timedelta(days=random.randint(0, (data_vencimento_dt - data_notificacao_dt).days)),
        data_vencimento_dt
    ])

    return (
        data_multa_dt.strftime("%d/%m/%Y"),
        hora_multa_dt,
        data_notificacao_dt.strftime("%d/%m/%Y"),
        data_vencimento_dt.strftime("%d/%m/%Y"),
        data_pagamento_dt.strftime("%d/%m/%Y"),
    )


data_multa, hora_multa, data_notificacao, data_vencimento, data_pagamento = gerar_dados_multa()

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

'''Nesse teste, o robô preencherá apenas os Cmapos Obrigatórios e clicará em Salvar'''

print('Nesse teste, o robô preencherá apenas os Cmapos Obrigatórios e clicará em Salvar')



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
campo_pesquisa.send_keys("Multa", Keys.ENTER)



time.sleep(3)

cadastrar = driver.find_element(By.CSS_SELECTOR, "#fmod_10092 > div.wdTelas > div.telaInicial.clearfix.overflow.overflowY > ul > li:nth-child(1) > a > span")
cadastrar.click()

time.sleep(2)



# Preenche o campo Veículo (com autocomplete ou seletor de modal)
open_lov_veiculo = wait.until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "#fmod_10092 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroMulta > div.catWrapper > div > div.cat_categoriaDadosMulta.categoriaHolder > div > div > div > div:nth-child(3) > div > a"))
)
open_lov_veiculo.click()



campo_pesquisa_veiculo = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.modalHolder > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div.formCol.divPesquisa > div:nth-child(1) > input"))
)
time.sleep(1)
campo_pesquisa_veiculo.send_keys('SANDERO 2013')

time.sleep(1)

pesquisar = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.modalHolder > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div:nth-child(3) > a"))
)   
pesquisar.click()


# Espera até que a linha com o cemitério específico esteja visível
veiculo = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//td[contains(text(), 'SANDERO 2013')]"))
)

# Clica na linha para selecioná-la
veiculo.click()




# Preenche o campo Veículo (com autocomplete ou seletor de modal)
open_lov_motorista = wait.until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "#fmod_10092 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroMulta > div.catWrapper > div > div.cat_categoriaDadosMulta.categoriaHolder > div > div > div > div:nth-child(4) > div > a"))
)
open_lov_motorista.click()



campo_pesquisa_motorista = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.modalHolder > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div.formCol.divPesquisa > input"))
)
time.sleep(1)
campo_pesquisa_motorista.send_keys('CRISPIM MALAFAIA')

time.sleep(1)

pesquisar = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.modalHolder > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div:nth-child(3) > a"))
)   
pesquisar.click()



# Espera até que a linha com o cemitério específico esteja visível
motorista = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//td[contains(text(), 'CRISPIM MALAFAIA')]"))
)

# Clica na linha para selecioná-la
motorista.click()




campo_data_multa = wait.until(EC.element_to_be_clickable((
    By.XPATH,
    "//input[@maxlength='10' and @name='dataMulta' and contains(@class, 'hasDatepicker dataMulta mandatory')]"
)))


# Preenche com a data desejada
campo_data_multa.click()
campo_data_multa.send_keys(data_multa)


# Preenche a Hora da Multa

campo_hora_multa = wait.until(EC.element_to_be_clickable((
    By.CSS_SELECTOR,
    "#fmod_10092 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroMulta > div.catWrapper > div > div.cat_categoriaDadosMulta.categoriaHolder > div > div > div > div:nth-child(6) > input"
)))


# Preenche com a data desejada
campo_hora_multa.click()
campo_hora_multa.clear()

campo_hora_multa.send_keys(hora_multa, Keys.TAB)



# Preenche o valor
campo_valor = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#fmod_10092 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroMulta > div.catWrapper > div > div.cat_categoriaDadosMulta.categoriaHolder > div > div > div > div:nth-child(12) > input")))
campo_valor.clear()
campo_valor.send_keys(f"{faker.random_int(min=100, max=1000)}.{faker.random_int(min=0, max=99):02d}", Keys.TAB)


# Clique no botão "Salvar"
Salvar = driver.find_element(By.CSS_SELECTOR, "#fmod_10092 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroMulta > div.btnHolder > a.btModel.btGray.btsave")
Salvar.click()
time.sleep(1)


BtNo = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "#BtNo"))
)
# Clica no botão "Não"
BtNo.click()

# Fechar modal
X = driver.find_element(By.CSS_SELECTOR, "#fmod_10092 > div.wdTop.ui-draggable-handle > div.wdClose > a")
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




