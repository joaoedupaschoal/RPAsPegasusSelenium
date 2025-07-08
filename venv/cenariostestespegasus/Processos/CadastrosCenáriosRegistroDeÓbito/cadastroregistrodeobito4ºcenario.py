from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from faker import Faker  # Importando o Faker
from faker.providers import BaseProvider
from validate_docbr import CPF
import random
import time
from datetime import datetime, timedelta
# Inicializando o Faker
fake = Faker()
from selenium.common.exceptions import TimeoutException

import random
from datetime import timedelta
from faker import Faker
import sys
import subprocess
from selenium import webdriver
# Redireciona saída padrão e erros para o arquivo log.txt
sys.stdout = open("log.txt", "w", encoding="utf-8")
sys.stderr = sys.stdout  # Erros também vão para o mesmo arquivo


def gerar_datas_validas():
    """Gera datas coerentes para nascimento, falecimento e sepultamento dentro de um intervalo válido."""
    
    hoje = datetime.today().date()
    dez_anos_atras = hoje - timedelta(days=3650)  # Limite máximo de 10 anos atrás
    
    # Gera uma data de falecimento entre 10 anos atrás e hoje
    data_falecimento = fake.date_between(start_date=dez_anos_atras, end_date=hoje)

    # Garante que a pessoa tenha no mínimo 18 anos na data do falecimento
    idade_minima = 18
    idade_maxima = 110
    data_nascimento = data_falecimento - timedelta(days=random.randint(idade_minima * 365, idade_maxima * 365))

    # Sepultamento entre 1 e 10 dias após o falecimento
    data_sepultamento = data_falecimento + timedelta(days=random.randint(1, 10))

    # Registro entre 1 e 10 dias após o sepultamento
    data_registro = data_sepultamento + timedelta(days=random.randint(1, 10))

    return (
        data_nascimento.strftime("%d/%m/%Y"),
        data_falecimento.strftime("%d/%m/%Y"),
        data_sepultamento.strftime("%d/%m/%Y"),
        data_registro.strftime("%d/%m/%Y")
    )

# Gera os valores corretos
data_nascimento, data_falecimento, data_sepultamento, data_registro = gerar_datas_validas()
hora_falecimento = fake.time(pattern="%H:%M")  # Horário aleatório no formato HH:MM
hora_sepultamento = fake.time(pattern="%H:%M")  # Horário aleatório no formato HH:MM
localizacao = fake.city()  # Nome de uma cidade aleatória


'''Nesse teste, o robô preencherá apenas os Campos Não Obrigatórios e salvará o cadastro'''

print('Nesse teste, o robô preencherá apenas os Campos Não Obrigatórios e salvará o cadastro')


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
# Simula o pressionamento da tecla F3
driver.find_element(By.TAG_NAME, "body").send_keys(Keys.F3)


wait = WebDriverWait(driver, 7)  # Tempo máximo de espera
botao_registro_obito = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > div.menuLayer.animate.process.overflow.overflowY.boxsize.active > ul > li:nth-child(14) > img')))
botao_registro_obito.click()

wait = WebDriverWait(driver, 7)  # Tempo máximo de espera
botao_cadastrar = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#fmod_23 > div.wdTelas > div.telaInicial.clearfix.overflow.overflowY > ul > li:nth-child(1) > a > span')))
botao_cadastrar.click()

wait = WebDriverWait(driver, 7)  # Tempo máximo de espera
wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#fmod_23 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div > div:nth-child(1) > div > div:nth-child(2) > div > a'))).click()

wait = WebDriverWait(driver, 7)  # Tempo máximo de espera
wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > div.modalHolder > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div:nth-child(4) > a'))).click()

wait = WebDriverWait(driver, 7)  # Tempo máximo de espera
wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#cg_10029 > div.wdTelas > div > div.catWrapper > div > div > div > div > div > input'))).send_keys('CARTÓRIO TESTE SELENIUM AUTOMATIZADO')


wait = WebDriverWait(driver, 7)  # Tempo máximo de espera
wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#cg_10029 > div.wdTelas > div > div.btnHolder > a.btModel.btGray.btsave'))).click()

campo_folha = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "#fmod_23 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div > div:nth-child(1) > div > div:nth-child(3) > input"))
)
campo_folha.send_keys(fake.random_int(min=1, max=99))


campo_livro = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "#fmod_23 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div > div:nth-child(1) > div > div:nth-child(4) > input"))
)
campo_livro.send_keys(fake.random_int(min=1, max=99))


campo_numero = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "#fmod_23 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div > div:nth-child(1) > div > div:nth-child(5) > input"))
)
campo_numero.send_keys(fake.random_int(min=1, max=99))



# Aguarda até que o dropdown esteja presente antes de selecionar um valor
select_element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "#fmod_23 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div > div:nth-child(1) > div > div:nth-child(7) > select"))
)

# Cria um objeto Select e escolhe a opção "Feminino"
Select(select_element).select_by_visible_text("Feminino")



campo_data_falecimento = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "input.hasDatepicker.mandatory.fc"))
)



campo_hora_falecimento = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "#fmod_23 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div > div:nth-child(1) > div > div:nth-child(9) > input"))
)

# Garante que o campo está visível e interagível antes de preencher
campo_hora_falecimento.click()
campo_hora_falecimento.clear()  # Remove qualquer valor existente
campo_hora_falecimento.send_keys(hora_falecimento)



driver.find_element(By.CSS_SELECTOR, "#fmod_23 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div > div:nth-child(1) > div > div:nth-child(10) > input").send_keys(fake.locale())  










driver.find_element(By.CSS_SELECTOR, "#fmod_23 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div > div:nth-child(1) > div > div:nth-child(25) > input").send_keys(fake.name())  




driver.find_element(By.CSS_SELECTOR, "#fmod_23 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div > div:nth-child(1) > div > div:nth-child(30) > input").send_keys(fake.name())  

driver.find_element(By.CSS_SELECTOR, "#fmod_23 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div > div:nth-child(1) > div > div:nth-child(32) > input").send_keys(fake.name())  



driver.find_element(By.CSS_SELECTOR, "#fmod_23 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div > div:nth-child(1) > div > div:nth-child(17) > input").send_keys(fake.first_name())  # Gerando o nome do cônjuge fictício




elemento_causa = driver.find_element(By.CSS_SELECTOR, "#fmod_23 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div > div:nth-child(1) > div > div:nth-child(34) > input")

# Rolando para o elemento
driver.execute_script("arguments[0].scrollIntoView();", elemento_causa)
elemento_causa.send_keys('TESTE CAUSA MORTIS ') 



driver.find_element(By.CSS_SELECTOR, "#fmod_23 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div > div:nth-child(1) > div > div:nth-child(35) > input").send_keys('TESTE CAUSA MORTIS 2')  
driver.find_element(By.CSS_SELECTOR, "#fmod_23 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div > div:nth-child(1) > div > div:nth-child(36) > input").send_keys('TESTE CAUSA MORTIS 3')  
driver.find_element(By.CSS_SELECTOR, "#fmod_23 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div > div:nth-child(1) > div > div:nth-child(37) > input").send_keys('TESTE CAUSA MORTIS 4')  

local_sepultamento = driver.find_element(By.CSS_SELECTOR, "#fmod_23 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div > div:nth-child(1) > div > div:nth-child(38) > input")

# Rolando para o elemento
driver.execute_script("arguments[0].scrollIntoView();", local_sepultamento)
local_sepultamento.send_keys(fake.locale()) 



time.sleep(3)


# Clique no botão "Salvar"


salvar = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "#fmod_23 > div.wdTelas > div.telaCadastro.clearfix > div.btnHolder > a.btModel.btGray.btsave > span"))
) 
salvar.click()  






# Fechar modal


X = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "#fmod_23 > div.wdTop.ui-draggable-handle > div.wdClose"))
) 
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
