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
import random
import time
from datetime import datetime, timedelta
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


fake = Faker()
numero_aleatorio = random.randint(1, 100)  # Gera um número aleatório entre 1 e 100
letra_aleatoria = random.choice(string.ascii_uppercase)  # Gera uma letra maiúscula aleatória

cemetery_name = f"Cemitério {fake.last_name()} {fake.random.choice(['Eterno', 'da Paz', 'Memorial', 'Descanso'])}"

qtd_parcelas_em_atraso = int(fake.random.choice(['1', '2', '3', '4', '5']))


# Gera hora aleatória entre 08:00 e 17:59
hora = random.randint(8, 17)
minuto = random.randint(0, 59)
hora_formatada = f"{hora:02d}:{minuto:02d}"

dias_para_exumar = int(fake.random.choice(['365', '730', '1095', '1460', '1825']))

def gerar_datas_validas():
    """Gera datas coerentes para nascimento, falecimento e sepultamento dentro de um intervalo válido."""
    
    hoje = datetime.today().date()
    dez_anos_atras = hoje - timedelta(days=3650)  # Limite máximo de 10 anos atrás
    
    # Gera uma data de falecimento entre 10 anos atrás e hoje
    data_falecimento = faker.date_between(start_date=dez_anos_atras, end_date=hoje)

    # Garante que a pessoa tenha no mínimo 18 anos na data do falecimento
    idade_minima = 18
    idade_maxima = 110
    data_nascimento = data_falecimento - timedelta(days=random.randint(idade_minima * 365, idade_maxima * 365))

    # Sepultamento entre 1 e 10 dias após o falecimento
    data_sepultamento = data_falecimento + timedelta(days=random.randint(1, 10))

    # Registro entre 1 e 10 dias após o sepultamento
    data_registro = data_sepultamento + timedelta(days=random.randint(1, 10))


  
    data_emissão = hoje - timedelta(days=random.randint(1, 100)) 
    data_vencimento = hoje + timedelta(days=random.randint(30, 180)) 
    data_consulta = faker.date_between(start_date=hoje, end_date=data_vencimento) 

    # Gera data aleatória
    hoje = datetime.today().date()

    data_de = hoje + timedelta(days=random.randint(1, 10))
    data_ate = data_de + timedelta(days=random.randint(1, 100))




    return (
        data_nascimento.strftime("%d/%m/%Y"),
        data_falecimento.strftime("%d/%m/%Y"),
        data_sepultamento.strftime("%d/%m/%Y"),
        data_registro.strftime("%d/%m/%Y"),
        data_de.strftime("%d/%m/%Y"),
        data_ate.strftime("%d/%m/%Y"),
        data_emissão.strftime("%d/%m/%Y"),
        data_vencimento.strftime("%d/%m/%Y"),
        data_consulta.strftime("%d/%m/%Y"),
    )



faker = Faker('pt_BR')  # Gera dados no formato brasileiro

def gerar_dados_documentos():
    carteira_trabalho = str(random.randint(10000000, 99999999))  # 8 dígitos
    pis = faker.cpf().replace('.', '').replace('-', '')[:11]     # Simula PIS com 11 dígitos (não válido oficialmente)
    cnh = str(random.randint(10000000000, 99999999999))           # CNH tem 11 dígitos
    
    return carteira_trabalho, pis, cnh


carteira_trabalho, pis, cnh = gerar_dados_documentos()



vencimento_cnh = faker.date_between(start_date='today', end_date='+10y')
vencimento_cnh_str = vencimento_cnh.strftime('%d/%m/%Y')


# Gera uma data de admissão entre 10 anos atrás e hoje
data_admissao = faker.date_between(start_date='-10y', end_date='today')
data_admissao_str = data_admissao.strftime('%d/%m/%Y')

# Gera os valores corretos
data_nascimento, data_falecimento, data_sepultamento, data_registro, data_de, data_ate, data_consulta, data_vencimento, data_emissão, = gerar_datas_validas()

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

'''Nesse teste, o robô preencherá todos os dados e clicará em Cancelar'''

print('Nesse teste, o robô preencherá todos os dados e clicará em Cancelar')



class BrasilProvider(BaseProvider):
    def rg(self):
        numeros = [str(random.randint(0, 9)) for _ in range(8)]
        return ''.join(numeros) + '-' + str(random.randint(0, 9))

fake = Faker("pt_BR")
faker.add_provider(BrasilProvider)  # Adiciona o provedor


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
campo_pesquisa.send_keys("Guias", Keys.ENTER)



time.sleep(3)

cadastrar = driver.find_element(By.CSS_SELECTOR, "#fmod_10067 > div.wdTelas > div.telaInicial.clearfix.overflow.overflowY > ul > li:nth-child(1) > a > span")
cadastrar.click()

time.sleep(2)


campo_data_emissao = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,
    "//input[contains(@class, 'hasDatepicker dataEmissao mandatory')]"
)))

# Tentando clicar após rolar para a posição correta


campo_data_emissao.send_keys(data_emissão)
campo_data_emissao.send_keys(data_emissão, Keys.TAB)




campo_data_vencimento = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,
    "//input[contains(@class, 'hasDatepicker dataVencimento mandatory')]"
)))

# Tentando clicar após rolar para a posição correta
campo_data_vencimento.send_keys(data_vencimento)

campo_data_consulta = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,
    "//input[contains(@class, 'hasDatepicker dataConsulta')]"
)))

# Tentando clicar após rolar para a posição correta
campo_data_consulta.click()

campo_data_consulta.send_keys(data_consulta)
time.sleep(0.5)
campo_data_consulta.send_keys(data_consulta)



Select(driver.find_element(By.CSS_SELECTOR, "#fmod_10067 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroGuia > div.catWrapper > div > div > div > div > div:nth-child(2) > div:nth-child(4) > select")).select_by_visible_text("Consulta")

Select(driver.find_element(By.CSS_SELECTOR, "#fmod_10067 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroGuia > div.catWrapper > div > div > div > div > div:nth-child(2) > div:nth-child(5) > select")).select_by_visible_text("Particular")


open_lov_paciente = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "#fmod_10067 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroGuia > div.catWrapper > div > div > div > div > div.formRow.linhaTipoParticular > div > div > a"))
)
open_lov_paciente.click()

time.sleep(0.5)
campo_pesquisa_paciente = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "#txtPesquisa"))
)
time.sleep(1)
campo_pesquisa_paciente.send_keys('RAVY MENDONÇA', Keys.ENTER)

time.sleep(1)


# Espera até que a linha com o cemitério específico esteja visível
paciente = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//td[contains(text(), 'RAVY MENDONÇA')]"))
)

# Clica na linha para selecioná-la
paciente.click()


hora_consulta = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "#fmod_10067 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroGuia > div.catWrapper > div > div > div > div > div:nth-child(5) > div:nth-child(2) > input"))
)

# Clica e preenche com a hora aleatória
hora_consulta.click()
hora_consulta.send_keys(hora_formatada)

open_lov_vinculo = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "#fmod_10067 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroGuia > div.catWrapper > div > div > div > div > div:nth-child(6) > div > div > a"))
)
open_lov_vinculo.click()

time.sleep(0.5)


open_lov_conveniado = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.modalHolder > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div:nth-child(2) > div:nth-child(1) > div > a"))
)
open_lov_conveniado.click()

time.sleep(0.5)


campo_pesquisa_conveniado = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div:nth-child(302) > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div.formCol.divPesquisa > div > div > input"))
)
campo_pesquisa_conveniado.click()
campo_pesquisa_conveniado.send_keys('ANA DA SILVA')

time.sleep(0.5)

pesquisar = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div:nth-child(302) > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div.formRow > div > a"))
)
pesquisar.click()

time.sleep(1)

# Espera até que a linha com o cemitério específico esteja visível
conveniado = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//td[contains(text(), 'ANA DA SILVA')]"))
)

# Clica na linha para selecioná-la
conveniado.click()

time.sleep(1)

pesquisar_vinculo = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.modalHolder > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div:nth-child(2) > div:nth-child(2) > a"))
)
pesquisar_vinculo.click()


time.sleep(1)


vinculo = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//td[contains(text(), 'CONVENIO A')]"))
)

# Clica na linha para selecioná-la
vinculo.click()


time.sleep(2)

# Clique no botão "Cancelar"
Cancelar = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "#fmod_10067 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroGuia > div.btnHolder > a.btModel.btGray.btcancel"))
)
Cancelar.click()



# Fechar modal
X = driver.find_element(By.CSS_SELECTOR, "#fmod_10067 > div.wdTop.ui-draggable-handle > div.wdClose > a")
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




