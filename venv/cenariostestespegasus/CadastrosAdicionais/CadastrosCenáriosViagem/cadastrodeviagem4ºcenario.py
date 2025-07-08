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
from datetime import datetime, timedelta
import random
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

def gerar_datas_e_horas_viagem(max_dias_ate_saida=30, max_duracao_viagem=10):
    hoje = datetime.today()
    
    # Gera a data de saída
    dias_ate_saida = random.randint(0, max_dias_ate_saida)
    data_saida = hoje + timedelta(days=dias_ate_saida)

    # Gera a hora de saída aleatória entre 00:00 e 23:59
    hora_saida = datetime(
        year=data_saida.year,
        month=data_saida.month,
        day=data_saida.day,
        hour=random.randint(0, 23),
        minute=random.randint(0, 59)
    )

    # Duração da viagem (em dias)
    duracao_dias = random.randint(1, max_duracao_viagem)

    # Hora de retorno aleatória depois da hora de saída
    hora_retorno = hora_saida + timedelta(
        days=duracao_dias,
        hours=random.randint(0, 5),     # até 5 horas extras de viagem
        minutes=random.randint(0, 59)
    )

    data_saida_str = hora_saida.strftime('%d/%m/%Y')
    hora_saida_str = hora_saida.strftime('%H:%M')

    data_retorno_str = hora_retorno.strftime('%d/%m/%Y')
    hora_retorno_str = hora_retorno.strftime('%H:%M')

    return data_saida_str, hora_saida_str, data_retorno_str, hora_retorno_str

data_saida, hora_saida, data_retorno, hora_retorno = gerar_datas_e_horas_viagem()



def gerar_kms():
    km_inicial =  random.randint(100, 1000)  # Gera um valor aleatório entre 100 e 1000 km
    km_final = km_inicial + random.randint(100, 1000)
    km_percorridos = km_final - km_inicial     
    return km_inicial, km_final, km_percorridos

km_inicial, km_final, km_percorridos = gerar_kms()






'''Nesse teste, o robô preencherá apenas os Campos Não Obrigatórios e clicará em Salvar'''

print('Nesse teste, o robô preencherá apenas os Campos Não Obrigatórios e clicará em Salvar')



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
campo_pesquisa.send_keys("Viagem", Keys.ENTER)



time.sleep(3)

cadastrar = driver.find_element(By.CSS_SELECTOR, "#fmod_10094 > div.wdTelas > div.telaInicial.clearfix.overflow.overflowY > ul > li:nth-child(1) > a > span")
cadastrar.click()

time.sleep(2)


campo_data_retorno = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((
        By.XPATH,
        '//input[contains(@class, "hasDatepicker dataRetorno")]'
    ))
)
campo_data_retorno.click()
campo_data_retorno.send_keys(data_retorno)

campo_hora_retorno = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((
        By.CSS_SELECTOR,
        '#fmod_10094 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroViagem > div.catWrapper > div > div.cat_categoriaDadosExame.categoriaHolder > div > div > div > div:nth-child(8) > input'  # ajuste o 'ref'
    ))
)
campo_hora_retorno.click()
campo_hora_retorno.send_keys(hora_retorno)

campo_km_inicial = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((
        By.CSS_SELECTOR,
        '#fmod_10094 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroViagem > div.catWrapper > div > div.cat_categoriaDadosExame.categoriaHolder > div > div > div > div:nth-child(12) > input'  # ajuste o 'ref'
    ))
)
campo_km_inicial.click()
campo_km_inicial.send_keys(km_inicial)

campo_km_final = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((
        By.CSS_SELECTOR,
        '#fmod_10094 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroViagem > div.catWrapper > div > div.cat_categoriaDadosExame.categoriaHolder > div > div > div > div:nth-child(13) > input'  # ajuste o 'ref'
    ))
)
campo_km_final.click()
campo_km_final.send_keys(km_final)


campo_descrição = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((
        By.CSS_SELECTOR,
        '#fmod_10094 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroViagem > div.catWrapper > div > div.cat_categoriaDadosExame.categoriaHolder > div > div > div > div:nth-child(15) > textarea'  # ajuste o 'ref'
    ))
)
campo_descrição.send_keys('TESTE DESCRIÇÃO VIAGEM SELENIUM AUTOMATIZADO: CORREU TUDO BEM FOI EFETUADO A VIAGEM COM SEGURANÇA, PAREI NO POSTO, ABASTECI, E FUI MUITO BEM HOSPEDADO PELO HOTEL, A VIAGEM FOI MUITO BOA, E O MOTORISTA FOI MUITO ATENCIOSO, E O VEÍCULO ESTAVA EM PERFEITAS CONDIÇÕES DE USO, NÃO TEVE NENHUM PROBLEMA DURANTE A VIAGEM, TUDO CORREU BEM, E VOLTEI PARA CASA COM SEGURANÇA.')


# Clique no botão "Salvar"
Salvar = driver.find_element(By.CSS_SELECTOR, "#fmod_10094 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroViagem > div.btnHolder > a.btModel.btGray.btsave")
Salvar.click()



# Fechar modal
X = driver.find_element(By.CSS_SELECTOR, "#fmod_10094 > div.wdTop.ui-draggable-handle > div.wdClose > a")
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




