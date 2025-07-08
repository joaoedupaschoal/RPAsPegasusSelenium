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
import string
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


faker = Faker('pt_BR')
import random
from datetime import timedelta
from faker import Faker

valor_taxa_adesao = round(random.uniform(2000, 10000), 2)
cemetery_name = f"Cemitério {faker.last_name()} {faker.random.choice(['Eterno', 'da Paz', 'Memorial', 'Descanso'])}"

qtd_parcelas_em_atraso = int(faker.random.choice(['1', '2', '3', '4', '5']))


dias_para_exumar = int(faker.random.choice(['365', '730', '1095', '1460', '1825']))

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
data_nascimento, data_falecimento, data_sepultamento, data_registro, data_de, data_ate, = gerar_datas_validas()
hora_falecimento = fake.time(pattern="%H:%M")  # Horário aleatório no formato HH:MM
hora_sepultamento = fake.time(pattern="%H:%M")  # Horário aleatório no formato HH:MM
localizacao = fake.city()  # Nome de uma cidade aleatória

# Gera uma data de admissão entre 10 anos atrás e hoje
data_admissao = faker.date_between(start_date='-10y', end_date='today')
data_admissao_str = data_admissao.strftime('%d/%m/%Y')

'''Nesse teste, o robô preencherá todos os dados e salvará o cadastro'''

print('Nesse teste, o robô preencherá todos os dados e salvará o cadastro')


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
time.sleep(0.5)
botao_contratos = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable(
        (By.XPATH, "//li[@class='iconElement shortcutIcon ui-draggable ui-draggable-handle' and @cname='I.CT' and @ref='I.CT']")
    )
)
botao_contratos.click()
wait = WebDriverWait(driver, 10)  # Tempo máximo de espera
botao_cadastrar = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#gsContratos > div.wdTelas > div > ul > li:nth-child(1) > a > span')))
botao_cadastrar.click()

time.sleep(0.5)

wait = WebDriverWait(driver, 7)  # Tempo máximo de espera
open_lov_tipo_contrato = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#gsContratos > div.wdTelas > div.wdWizard.clearfix.telaConsulta > div.wizardHolder > div > div.stepPacote.step1 > div > div > div > div > a')))
open_lov_tipo_contrato.click()




campo_pesquisa = WebDriverWait(driver, 15).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.modalHolder > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div:nth-child(2) > input"))
)
campo_pesquisa.send_keys('TIPO DE CONTRATO TESTE SELENIUM AUTOMATIZADO', Keys.ENTER)

time.sleep(1)
# Espera até que a linha com o cemitério específico esteja visível
tipo_contrato = WebDriverWait(driver, 15).until(
    EC.element_to_be_clickable((By.XPATH, "//td[contains(text(), 'TIPO DE CONTRATO TESTE SELENIUM AUTOMATIZADO')]"))
)

# Clica na linha para selecioná-la
tipo_contrato.click()

time.sleep(3)

WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.XPATH, "//h3[text()='PACOTE TESTE SELENIUM AUTOMATIZADO']"))
).click()

wait = WebDriverWait(driver, 7)  # Tempo máximo de espera
avançar_1 = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#gsContratos > div.wdTelas > div.wdWizard.clearfix.telaConsulta > div.btnHolder > a:nth-child(3)')))
avançar_1.click()

wait = WebDriverWait(driver, 7)  # Tempo máximo de espera
open_lov_plano_empresa = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#gsContratos > div.wdTelas > div.wdWizard.clearfix.telaConsulta > div.wizardHolder > div > div.stepPacote.step3 > div.formRow.divPlanoEmpresa > div:nth-child(1) > div > a')))
open_lov_plano_empresa.click()

wait = WebDriverWait(driver, 20)  # Tempo máximo de espera
novo_registro_plano_empresa = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > div.modalHolder > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div:nth-child(5) > a')))
novo_registro_plano_empresa.click()


nome = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "#cg_10055 > div.wdTelas > div > div.catWrapper > div > div > div:nth-child(1) > div > div:nth-child(2) > input"))
)
nome.send_keys('PLANO EMPRESA TESTE SELENIUM AUTOMATIZADO')

CNPJ = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "#cg_10055 > div.wdTelas > div > div.catWrapper > div > div > div:nth-child(1) > div > div:nth-child(3) > input"))
)
CNPJ.click()
CNPJ.send_keys(fake.cnpj())

time.sleep(0.5)

telefone = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "#cg_10055 > div.wdTelas > div > div.catWrapper > div > div > div:nth-child(1) > div > div:nth-child(4) > input"))
)
telefone.click()
telefone.send_keys(fake.phone_number())
time.sleep(0.5)
fax = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "#cg_10055 > div.wdTelas > div > div.catWrapper > div > div > div:nth-child(1) > div > div:nth-child(5) > input"))
)
fax.send_keys(fake.phone_number())

email = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "#cg_10055 > div.wdTelas > div > div.catWrapper > div > div > div:nth-child(1) > div > div:nth-child(6) > input"))
)
email.send_keys(fake.email())


try:
    elemento = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#cg_10055 > div.wdTelas > div > div.catWrapper > div > div > div:nth-child(2) > div > div:nth-child(2) > div > input"))
    )


    # Preenche o campo de endereço
    elemento.click()
    elemento.send_keys("15081115")

    time.sleep(2)

    # Aguarda o botão aparecer e clica nele
    botao = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#cg_10055 > div.wdTelas > div > div.catWrapper > div > div > div:nth-child(2) > div > div:nth-child(2) > div > a"))
    )
    botao.click()

except Exception as e:
    print(f"Erro: {e}")



elemento = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#cg_10055 > div.wdTelas > div > div.catWrapper > div > div > div:nth-child(2) > div > div:nth-child(5) > input")))
elemento.send_keys("1733")



elemento = driver.find_element(By.CSS_SELECTOR, "#cg_10055 > div.wdTelas > div > div.catWrapper > div > div > div:nth-child(2) > div > div:nth-child(6) > input")
elemento.send_keys("Casa")

wait = WebDriverWait(driver, 10)  # Tempo máximo de espera
botao_salvar_plano_empresa = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#cg_10055 > div.wdTelas > div > div.btnHolder > a.btModel.btGray.btsave')))
botao_salvar_plano_empresa.click()
time.sleep(2)

wait = WebDriverWait(driver, 10)  # Tempo máximo de espera
open_lov_fonte_informação = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#gsContratos > div.wdTelas > div.wdWizard.clearfix.telaConsulta > div.wizardHolder > div > div.stepPacote.step3 > div.formRow.divPlanoEmpresa > div:nth-child(2) > div > a')))
open_lov_fonte_informação.click()

wait = WebDriverWait(driver, 7)  # Tempo máximo de espera
novo_registro_fonte_informação= wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > div.modalHolder > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div:nth-child(3) > a')))
novo_registro_fonte_informação.click()


nome_fonte = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "#cg_10069 > div.wdTelas > div > div.catWrapper > div > div > div > div > div > div:nth-child(2) > input"))
)
nome_fonte.send_keys('FONTE DE INFORMÇÃO TESTE SELENIUM AUTOMATIZADO')

wait = WebDriverWait(driver, 7)  # Tempo máximo de espera
botao_salvar_fonte = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#cg_10069 > div.wdTelas > div > div.btnHolder > a.btModel.btGray.btsave')))
botao_salvar_fonte.click()



wait = WebDriverWait(driver, 7)  # Tempo máximo de espera
open_lov_supervisor = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#gsContratos > div.wdTelas > div.wdWizard.clearfix.telaConsulta > div.wizardHolder > div > div.stepPacote.step3 > div:nth-child(8) > div.formCol.supervisorHolder > div > div > a')))
open_lov_supervisor.click()

time.sleep(3)

wait = WebDriverWait(driver, 20)  # Tempo máximo de espera
novo_registro_supervisor= wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > div.modalHolder > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div:nth-child(4) > a')))
novo_registro_supervisor.click()


wait = WebDriverWait(driver, 7)  # Tempo máximo de espera
open_lov_pessoa_supervisor= wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#cg_10018 > div.wdTelas > div > div.catWrapper > div > div > div > div > div:nth-child(2) > div > a')))
open_lov_pessoa_supervisor.click()

wait = WebDriverWait(driver, 7)  # Tempo máximo de espera
novo_registro_pessoa_supervisor= wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > div.modalHolder > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div:nth-child(3) > a')))
novo_registro_pessoa_supervisor.click()


# Preenchendo os dados pessoais com o Faker
driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosPessoais.categoriaHolder > div > div > div:nth-child(2) > div:nth-child(2) > input").send_keys('SUPERVISOR TESTE SELENIUM AUTOMATIZADO')  # Nome falso
Select(driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosPessoais.categoriaHolder > div > div > div:nth-child(2) > div:nth-child(3) > select")).select_by_visible_text("Física")
Select(driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosPessoais.categoriaHolder > div > div > div:nth-child(2) > div:nth-child(4) > select")).select_by_visible_text("Carteira de Identidade Classista")
driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosPessoais.categoriaHolder > div > div > div.formRow.divPessoaFISICA > div:nth-child(1) > input").send_keys(fake.rg()) # Gerando RG falso
time.sleep(0.5)

# Data de Nascimento com o Faker
campo_data = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "input.dataExpedicao"))
) 
campo_data.click()  # Clica no campo de data
campo_data.send_keys(fake.date_of_birth(minimum_age=18, maximum_age=60).strftime("%d/%m/%Y"))  # Gerando uma data de nascimento aleatória

time.sleep(0.5)

# Gera um CPF válido
cpf = CPF().generate()

# Localiza o campo de CPF
cpf_field = driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosPessoais.categoriaHolder > div > div > div.formRow.divPessoaFISICA > div:nth-child(3) > input")

# Preenche o campo com o CPF gerado
cpf_field.click()
time.sleep(0.5)

cpf_field.send_keys(cpf)

time.sleep(1)

# Dados Complementares
driver.find_element(By.LINK_TEXT, "Dados Complementares").click()

time.sleep(1)

Select(driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosComplementares.categoriaHolder > div > div > div > div:nth-child(1) > select")).select_by_visible_text("Solteiro")
Select(driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosComplementares.categoriaHolder > div > div > div > div:nth-child(2) > select")).select_by_visible_text("Feminino")

# Gerando um e-mail e preenchendo
driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosComplementares.categoriaHolder > div > div > div > div:nth-child(9) > input").send_keys(fake.email())

campo_data = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "input.dataNascimento"))
) 
campo_data.click()  # Clica no campo de data
campo_data.send_keys(fake.date_of_birth(minimum_age=18, maximum_age=60).strftime("%d/%m/%Y"))  # Gerando uma data de nascimento aleatória

time.sleep(0.5)


# Contato
driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosComplementares.categoriaHolder > div > div > div > div:nth-child(5) > input").send_keys(fake.phone_number())  # Gerando um número de telefone falso
driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosComplementares.categoriaHolder > div > div > div > div:nth-child(6) > input").send_keys(fake.phone_number())  # Gerando um número de telefone falso
driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosComplementares.categoriaHolder > div > div > div > div:nth-child(7) > input").send_keys(fake.phone_number())  # Gerando um número de telefone falso
driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosComplementares.categoriaHolder > div > div > div > div:nth-child(9) > input").send_keys(fake.email())  # Gerando um e-mail falso
driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosComplementares.categoriaHolder > div > div > div > div:nth-child(11) > input").send_keys(fake.city())  # Gerando uma cidade fictícia
driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosComplementares.categoriaHolder > div > div > div > div:nth-child(12) > input").send_keys(fake.country())  # Gerando um país fictício
driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosComplementares.categoriaHolder > div > div > div > div:nth-child(13) > input").send_keys(fake.first_name())  # Gerando o nome do pai fictício
driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosComplementares.categoriaHolder > div > div > div > div:nth-child(14) > input").send_keys(fake.first_name())  # Gerando o nome da mãe fictício

time.sleep(0.5)

# Profissão
driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosComplementares.categoriaHolder > div > div > div > div:nth-child(16) > input").send_keys(fake.job())  # Gerando uma profissão fictícia

time.sleep(0.5)

time.sleep(0.5)

driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.categorias.overflow.overflowY > ul > li.li_enderecos > a").click()


time.sleep(3)

# Aguarda até o elemento estar presente na página
try:
    elemento = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_enderecos.categoriaHolder > div.groupHolder.clearfix.grupo_enderecoResidencial > div > div:nth-child(2) > div:nth-child(1) > div > input"))
    )


    # Preenche o campo de endereço
    elemento.send_keys("15081115")
    

    # Aguarda o botão aparecer e clica nele
    botao = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_enderecos.categoriaHolder > div.groupHolder.clearfix.grupo_enderecoResidencial > div > div:nth-child(2) > div:nth-child(1) > div > a"))
    )
    botao.click()

except Exception as e:
    print(f"Erro: {e}")

time.sleep(5)

element = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#BtYes")))

element.click()
element.click()

wait = WebDriverWait(driver, 1)  


elemento = driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_enderecos.categoriaHolder > div.groupHolder.clearfix.grupo_enderecoResidencial > div > div:nth-child(3) > div:nth-child(2) > input")
elemento.send_keys("1733")



elemento = driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_enderecos.categoriaHolder > div.groupHolder.clearfix.grupo_enderecoResidencial > div > div:nth-child(3) > div:nth-child(3) > input")
elemento.send_keys("Casa")



time.sleep(3)


driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_enderecos.categoriaHolder > div.groupHolder.clearfix.grupo_enderecoResidencial > div > div:nth-child(3) > div:nth-child(9) > label > input").click()

time.sleep(2)


# Clique no botão "Salvar"
driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.btnHolder > a.btModel.btGray.btsave").click()


wait = WebDriverWait(driver, 7)  # Tempo máximo de espera
comissao_porcentagem= wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#cg_10018 > div.wdTelas > div > div.catWrapper > div > div > div > div > div:nth-child(3) > input')))
comissao_porcentagem.send_keys(fake.random_int(min=10, max=500))

wait = WebDriverWait(driver, 7)  # Tempo máximo de espera
comissao_reais= wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#cg_10018 > div.wdTelas > div > div.catWrapper > div > div > div > div > div:nth-child(4) > input')))
comissao_reais.send_keys(fake.random_int(min=10, max=500))

time.sleep(5)

wait = WebDriverWait(driver, 7)  # Tempo máximo de espera
auto_cod= wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#cg_10018 > div.wdTelas > div > div.catWrapper > div > div > div > div > div:nth-child(6) > input')))
auto_cod.click()



time.sleep(1)
wait = WebDriverWait(driver, 15)  # Tempo máximo de espera
salvar_supervisor = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#cg_10018 > div.wdTelas > div > div.btnHolder > a.btModel.btGray.btsave')))
salvar_supervisor.click()
'''
time.sleep(1)
wait = WebDriverWait(driver, 20)  # Tempo máximo de espera
open_lov_vendedor = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#gsContratos > div.wdTelas > div.wdWizard.clearfix.telaConsulta > div.wizardHolder > div > div.stepPacote.step3 > div:nth-child(8) > div.formCol.vendedorHolder > div > div > a')))
open_lov_vendedor.click()

wait = WebDriverWait(driver, 7)  # Tempo máximo de espera
novo_registro_vendedor= wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > div.modalHolder > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div:nth-child(4) > a')))
novo_registro_vendedor.click()


wait = WebDriverWait(driver, 7)  # Tempo máximo de espera
open_lov_pessoa_vendedor= wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#cg_10020 > div.wdTelas > div > div.catWrapper > div > div > div > div > div:nth-child(2) > div > a')))
open_lov_pessoa_vendedor.click()

wait = WebDriverWait(driver, 7)  # Tempo máximo de espera
novo_registro_pessoa_vendedor= wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > div.modalHolder > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div:nth-child(3) > a')))
novo_registro_pessoa_vendedor.click()


# Preenchendo os dados pessoais com o Faker
driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosPessoais.categoriaHolder > div > div > div:nth-child(2) > div:nth-child(2) > input").send_keys('VENDEDOR TESTE SELENIUM AUTOMATIZADO')  # Nome falso
Select(driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosPessoais.categoriaHolder > div > div > div:nth-child(2) > div:nth-child(3) > select")).select_by_visible_text("Física")
Select(driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosPessoais.categoriaHolder > div > div > div:nth-child(2) > div:nth-child(4) > select")).select_by_visible_text("Carteira de Identidade Classista")
driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosPessoais.categoriaHolder > div > div > div.formRow.divPessoaFISICA > div:nth-child(1) > input").send_keys(fake.rg()) # Gerando RG falso
time.sleep(0.5)

# Data de Nascimento com o Faker
campo_data = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "input.dataExpedicao"))
) 
campo_data.click()  # Clica no campo de data
campo_data.send_keys(fake.date_of_birth(minimum_age=18, maximum_age=60).strftime("%d/%m/%Y"))  # Gerando uma data de nascimento aleatória

time.sleep(0.5)

# Gera um CPF válido
cpf = CPF().generate()

# Localiza o campo de CPF
cpf_field = driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosPessoais.categoriaHolder > div > div > div.formRow.divPessoaFISICA > div:nth-child(3) > input")

# Preenche o campo com o CPF gerado
cpf_field.click()
time.sleep(0.5)

cpf_field.send_keys(cpf)

time.sleep(1)

# Dados Complementares
driver.find_element(By.LINK_TEXT, "Dados Complementares").click()

time.sleep(1)

Select(driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosComplementares.categoriaHolder > div > div > div > div:nth-child(1) > select")).select_by_visible_text("Solteiro")
Select(driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosComplementares.categoriaHolder > div > div > div > div:nth-child(2) > select")).select_by_visible_text("Feminino")

# Gerando um e-mail e preenchendo
driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosComplementares.categoriaHolder > div > div > div > div:nth-child(9) > input").send_keys(fake.email())

campo_data = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "input.dataNascimento"))
) 
campo_data.click()  # Clica no campo de data
campo_data.send_keys(fake.date_of_birth(minimum_age=18, maximum_age=60).strftime("%d/%m/%Y"))  # Gerando uma data de nascimento aleatória

time.sleep(0.5)


# Contato
driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosComplementares.categoriaHolder > div > div > div > div:nth-child(5) > input").send_keys(fake.phone_number())  # Gerando um número de telefone falso
driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosComplementares.categoriaHolder > div > div > div > div:nth-child(6) > input").send_keys(fake.phone_number())  # Gerando um número de telefone falso
driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosComplementares.categoriaHolder > div > div > div > div:nth-child(7) > input").send_keys(fake.phone_number())  # Gerando um número de telefone falso
driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosComplementares.categoriaHolder > div > div > div > div:nth-child(9) > input").send_keys(fake.email())  # Gerando um e-mail falso
driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosComplementares.categoriaHolder > div > div > div > div:nth-child(11) > input").send_keys(fake.city())  # Gerando uma cidade fictícia
driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosComplementares.categoriaHolder > div > div > div > div:nth-child(12) > input").send_keys(fake.country())  # Gerando um país fictício
driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosComplementares.categoriaHolder > div > div > div > div:nth-child(13) > input").send_keys(fake.first_name())  # Gerando o nome do pai fictício
driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosComplementares.categoriaHolder > div > div > div > div:nth-child(14) > input").send_keys(fake.first_name())  # Gerando o nome da mãe fictício

time.sleep(0.5)

# Profissão
driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosComplementares.categoriaHolder > div > div > div > div:nth-child(16) > input").send_keys(fake.job())  # Gerando uma profissão fictícia

time.sleep(0.5)

time.sleep(0.5)

driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.categorias.overflow.overflowY > ul > li.li_enderecos > a").click()


time.sleep(3)

# Aguarda até o elemento estar presente na página
try:
    elemento = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_enderecos.categoriaHolder > div.groupHolder.clearfix.grupo_enderecoResidencial > div > div:nth-child(2) > div:nth-child(1) > div > input"))
    )


    # Preenche o campo de endereço
    elemento.send_keys("15081115")
    

    # Aguarda o botão aparecer e clica nele
    botao = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_enderecos.categoriaHolder > div.groupHolder.clearfix.grupo_enderecoResidencial > div > div:nth-child(2) > div:nth-child(1) > div > a"))
    )
    botao.click()

except Exception as e:
    print(f"Erro: {e}")

time.sleep(5)

element = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#BtYes")))

element.click()
element.click()

wait = WebDriverWait(driver, 1)  


elemento = driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_enderecos.categoriaHolder > div.groupHolder.clearfix.grupo_enderecoResidencial > div > div:nth-child(3) > div:nth-child(2) > input")
elemento.send_keys("1733")



elemento = driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_enderecos.categoriaHolder > div.groupHolder.clearfix.grupo_enderecoResidencial > div > div:nth-child(3) > div:nth-child(3) > input")
elemento.send_keys("Casa")



time.sleep(3)


driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_enderecos.categoriaHolder > div.groupHolder.clearfix.grupo_enderecoResidencial > div > div:nth-child(3) > div:nth-child(9) > label > input").click()

time.sleep(2)

# Clique no botão "Salvar"
driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.btnHolder > a.btModel.btGray.btsave").click()





wait = WebDriverWait(driver, 10)

# Aguarda o campo aparecer
campo_data_admissao = wait.until(EC.element_to_be_clickable((
    By.XPATH,
    "//input[@grupo='10024' and @ref='10066' and contains(@class, 'hasDatepicker')]"
)))


# Preenche com a data desejada
campo_data_admissao.send_keys(data_admissao_str)

driver.execute_script("arguments[0].value = arguments[1];", campo_data_admissao, data_admissao_str)

campo_data_admissao.send_keys(Keys.TAB)


campo = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "#cg_10020 > div.wdTelas > div > div.catWrapper > div > div > div > div > div:nth-child(4) > input"))  # ou ID, CSS_SELECTOR etc.
)
campo.click()
campo.send_keys(carteira_trabalho)


WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, '#cg_10020 > div.wdTelas > div > div.catWrapper > div > div > div > div > div:nth-child(5) > input'))
).send_keys(pis)


wait = WebDriverWait(driver, 7)  # Tempo máximo de espera
open_lov_tipo_supervisor= wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#cg_10020 > div.wdTelas > div > div.catWrapper > div > div > div > div > div:nth-child(6) > div > a')))
open_lov_tipo_supervisor.click()

campo_pesquisa_supervisor = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.modalHolder > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div:nth-child(2) > input.nomePesquisa"))
)
campo_pesquisa_supervisor.send_keys('SUPERVISOR TESTE SELENIUM AUTOMATIZADO', Keys.ENTER)
time.sleep(1)
# Espera até que a linha com o cemitério específico esteja visível
supervisor = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//td[contains(text(), 'SUPERVISOR TESTE SELENIUM AUTOMATIZADO')]"))
)

# Clica na linha para selecioná-la
supervisor.click()


wait = WebDriverWait(driver, 7)  # Tempo máximo de espera
comissao_porcentagem= wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#cg_10020 > div.wdTelas > div > div.catWrapper > div > div > div > div > div:nth-child(7) > input')))
comissao_porcentagem.send_keys(fake.random_int(min=10, max=500))

wait = WebDriverWait(driver, 7)  # Tempo máximo de espera
comissao_reais= wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#cg_10020 > div.wdTelas > div > div.catWrapper > div > div > div > div > div:nth-child(8) > input')))
comissao_reais.send_keys(fake.random_int(min=10, max=500))

Select(driver.find_element(By.CSS_SELECTOR, "#cg_10020 > div.wdTelas > div > div.catWrapper > div > div > div > div > div:nth-child(9) > select")).select_by_visible_text("Interno")
Select(driver.find_element(By.CSS_SELECTOR, "#cg_10020 > div.wdTelas > div > div.catWrapper > div > div > div > div > div:nth-child(11) > select")).select_by_visible_text("Carteira Assinada")

wait = WebDriverWait(driver, 7)  # Tempo máximo de espera
campo_auto= wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#cg_10020 > div.wdTelas > div > div.catWrapper > div > div > div > div > div:nth-child(12) > input')))
campo_auto.click()
time.sleep(5)
wait = WebDriverWait(driver, 7)  # Tempo máximo de espera
salvar_vendedor= wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#cg_10020 > div.wdTelas > div > div.btnHolder > a.btModel.btGray.btsave')))
salvar_vendedor.click()


'''

time.sleep(2)

open_lov_rateio = driver.find_element(By.CSS_SELECTOR, "#gsContratos > div.wdTelas > div.wdWizard.clearfix.telaConsulta > div.wizardHolder > div > div.stepPacote.step3 > div:nth-child(11) > div > div > a")

# Rolando para o elemento
driver.execute_script("arguments[0].scrollIntoView();", open_lov_rateio)
open_lov_rateio.click()

wait = WebDriverWait(driver, 7)  # Tempo máximo de espera
novo_registro_grupo_rateio= wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > div.modalHolder > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div:nth-child(5) > a')))
novo_registro_grupo_rateio.click()

wait = WebDriverWait(driver, 7)  # Tempo máximo de espera
nome_grupo_rateio= wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#cg_10051 > div.wdTelas > div > div.catWrapper > div > div > div > div > div:nth-child(2) > input')))
nome_grupo_rateio.send_keys('GRUPO DE RATEIO TESTE SELENIUM AUTOMATIZADO')


wait = WebDriverWait(driver, 7)  # Tempo máximo de espera
qtd_max_contratos= wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#cg_10051 > div.wdTelas > div > div.catWrapper > div > div > div > div > div:nth-child(4) > input')))
qtd_max_contratos.send_keys(fake.random_int(min=1, max=20))

Select(driver.find_element(By.CSS_SELECTOR, "#cg_10051 > div.wdTelas > div > div.catWrapper > div > div > div > div > div:nth-child(6) > select")).select_by_visible_text("Apenas Primeiro Sepultamento")

wait = WebDriverWait(driver, 7)  # Tempo máximo de espera
valor= wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#cg_10051 > div.wdTelas > div > div.catWrapper > div > div > div > div > div:nth-child(7) > input')))
valor.send_keys(fake.random_int(min=10, max=5000))
time.sleep(2)
wait = WebDriverWait(driver, 7)  # Tempo máximo de espera
salvar_grupo_rateio= wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#cg_10051 > div.wdTelas > div > div.btnHolder > a.btModel.btGray.btsave')))
salvar_grupo_rateio.click()

time.sleep(2)


wait = WebDriverWait(driver, 15)  # Tempo máximo de espera
avançar_2 = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#gsContratos > div.wdTelas > div.wdWizard.clearfix.telaConsulta > div.btnHolder > a:nth-child(3)')))
avançar_2.click()

wait = WebDriverWait(driver, 7)  # Tempo máximo de espera
open_lov_titular = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#ui-id-2 > div:nth-child(1) > div:nth-child(1) > div > a')))
open_lov_titular.click()

wait = WebDriverWait(driver, 7)  # Tempo máximo de espera
novo_registo_titular = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > div.modalHolder > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div:nth-child(3) > a')))
novo_registo_titular.click()

# Preenchendo os dados pessoais com o Faker
driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosPessoais.categoriaHolder > div > div > div:nth-child(2) > div:nth-child(2) > input").send_keys(faker.name())  # Nome falso
Select(driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosPessoais.categoriaHolder > div > div > div:nth-child(2) > div:nth-child(3) > select")).select_by_visible_text("Física")
Select(driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosPessoais.categoriaHolder > div > div > div:nth-child(2) > div:nth-child(4) > select")).select_by_visible_text("Carteira de Identidade Classista")
driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosPessoais.categoriaHolder > div > div > div.formRow.divPessoaFISICA > div:nth-child(1) > input").send_keys(fake.rg()) # Gerando RG falso
time.sleep(0.5)

# Data de Nascimento com o Faker
campo_data = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "input.dataExpedicao"))
) 
campo_data.click()  # Clica no campo de data
campo_data.send_keys(fake.date_of_birth(minimum_age=18, maximum_age=60).strftime("%d/%m/%Y"))  # Gerando uma data de nascimento aleatória

time.sleep(0.5)

# Gera um CPF válido
cpf = CPF().generate()

# Localiza o campo de CPF
cpf_field = driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosPessoais.categoriaHolder > div > div > div.formRow.divPessoaFISICA > div:nth-child(3) > input")

# Preenche o campo com o CPF gerado
cpf_field.click()
time.sleep(0.5)

cpf_field.send_keys(cpf)

time.sleep(1)

# Dados Complementares
driver.find_element(By.LINK_TEXT, "Dados Complementares").click()

time.sleep(1)

Select(driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosComplementares.categoriaHolder > div > div > div > div:nth-child(1) > select")).select_by_visible_text("Solteiro")
Select(driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosComplementares.categoriaHolder > div > div > div > div:nth-child(2) > select")).select_by_visible_text("Feminino")

# Gerando um e-mail e preenchendo
driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosComplementares.categoriaHolder > div > div > div > div:nth-child(9) > input").send_keys(fake.email())

campo_data = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "input.dataNascimento"))
) 
campo_data.click()  # Clica no campo de data
campo_data.send_keys(fake.date_of_birth(minimum_age=18, maximum_age=60).strftime("%d/%m/%Y"))  # Gerando uma data de nascimento aleatória

time.sleep(0.5)


# Contato
driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosComplementares.categoriaHolder > div > div > div > div:nth-child(5) > input").send_keys(fake.phone_number())  # Gerando um número de telefone falso
driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosComplementares.categoriaHolder > div > div > div > div:nth-child(6) > input").send_keys(fake.phone_number())  # Gerando um número de telefone falso
driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosComplementares.categoriaHolder > div > div > div > div:nth-child(7) > input").send_keys(fake.phone_number())  # Gerando um número de telefone falso
driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosComplementares.categoriaHolder > div > div > div > div:nth-child(9) > input").send_keys(fake.email())  # Gerando um e-mail falso
driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosComplementares.categoriaHolder > div > div > div > div:nth-child(11) > input").send_keys(fake.city())  # Gerando uma cidade fictícia
driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosComplementares.categoriaHolder > div > div > div > div:nth-child(12) > input").send_keys(fake.country())  # Gerando um país fictício
driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosComplementares.categoriaHolder > div > div > div > div:nth-child(13) > input").send_keys(fake.first_name())  # Gerando o nome do pai fictício
driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosComplementares.categoriaHolder > div > div > div > div:nth-child(14) > input").send_keys(fake.first_name())  # Gerando o nome da mãe fictício

time.sleep(0.5)

# Profissão
driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosComplementares.categoriaHolder > div > div > div > div:nth-child(16) > input").send_keys(fake.job())  # Gerando uma profissão fictícia

time.sleep(0.5)

time.sleep(0.5)

driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.categorias.overflow.overflowY > ul > li.li_enderecos > a").click()


time.sleep(3)

# Aguarda até o elemento estar presente na página
try:
    elemento = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_enderecos.categoriaHolder > div.groupHolder.clearfix.grupo_enderecoResidencial > div > div:nth-child(2) > div:nth-child(1) > div > input"))
    )


    # Preenche o campo de endereço
    elemento.send_keys("15081115")
    

    # Aguarda o botão aparecer e clica nele
    botao = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_enderecos.categoriaHolder > div.groupHolder.clearfix.grupo_enderecoResidencial > div > div:nth-child(2) > div:nth-child(1) > div > a"))
    )
    botao.click()

except Exception as e:
    print(f"Erro: {e}")

time.sleep(5)

element = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#BtYes")))

element.click()

wait = WebDriverWait(driver, 1)  


elemento = driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_enderecos.categoriaHolder > div.groupHolder.clearfix.grupo_enderecoResidencial > div > div:nth-child(3) > div:nth-child(2) > input")
elemento.send_keys("1733")



elemento = driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_enderecos.categoriaHolder > div.groupHolder.clearfix.grupo_enderecoResidencial > div > div:nth-child(3) > div:nth-child(3) > input")
elemento.send_keys("Casa")



time.sleep(3)


driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_enderecos.categoriaHolder > div.groupHolder.clearfix.grupo_enderecoResidencial > div > div:nth-child(3) > div:nth-child(9) > label > input").click()

time.sleep(2)

# Clique no botão "Salvar"
driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.btnHolder > a.btModel.btGray.btsave").click()

time.sleep(3)   

wait = WebDriverWait(driver, 7)  # Tempo máximo de espera
salvar_titular = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#ui-id-2 > div:nth-child(9) > div:nth-child(5) > a')))

# Rolando para o elemento
driver.execute_script("arguments[0].scrollIntoView();", salvar_titular)
salvar_titular.click()

time.sleep(5)
wait = WebDriverWait(driver, 7)  # Tempo máximo de espera
botao_cadastro_dependente = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#gsContratos > div.wdTelas > div.wdWizard.clearfix.telaConsulta > div.wizardHolder > div > div.stepPacote.step4 > div.blockHolder.titulares > ul > li > a.sprites.sp-addDependentes')))
botao_cadastro_dependente.click()

wait = WebDriverWait(driver, 7)  # Tempo máximo de espera
novo_registo_dependente = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > div.modalHolder > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div:nth-child(3) > a')))
novo_registo_dependente.click()


# Preenchendo os dados pessoais com o Faker
driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosPessoais.categoriaHolder > div > div > div:nth-child(2) > div:nth-child(2) > input").send_keys(faker.name())  # Nome falso
Select(driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosPessoais.categoriaHolder > div > div > div:nth-child(2) > div:nth-child(3) > select")).select_by_visible_text("Física")
Select(driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosPessoais.categoriaHolder > div > div > div:nth-child(2) > div:nth-child(4) > select")).select_by_visible_text("Carteira de Identidade Classista")
driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosPessoais.categoriaHolder > div > div > div.formRow.divPessoaFISICA > div:nth-child(1) > input").send_keys(fake.rg()) # Gerando RG falso
time.sleep(0.5)

# Data de Nascimento com o Faker
campo_data = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "input.dataExpedicao"))
) 
campo_data.click()  # Clica no campo de data
campo_data.send_keys(fake.date_of_birth(minimum_age=18, maximum_age=60).strftime("%d/%m/%Y"))  # Gerando uma data de nascimento aleatória

time.sleep(0.5)

# Gera um CPF válido
cpf = CPF().generate()

# Localiza o campo de CPF
cpf_field = driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosPessoais.categoriaHolder > div > div > div.formRow.divPessoaFISICA > div:nth-child(3) > input")

# Preenche o campo com o CPF gerado
cpf_field.click()
time.sleep(0.5)

cpf_field.send_keys(cpf)

time.sleep(1)

# Dados Complementares
driver.find_element(By.LINK_TEXT, "Dados Complementares").click()

time.sleep(1)

Select(driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosComplementares.categoriaHolder > div > div > div > div:nth-child(1) > select")).select_by_visible_text("Solteiro")
Select(driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosComplementares.categoriaHolder > div > div > div > div:nth-child(2) > select")).select_by_visible_text("Feminino")

# Gerando um e-mail e preenchendo
driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosComplementares.categoriaHolder > div > div > div > div:nth-child(9) > input").send_keys(fake.email())

campo_data = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "input.dataNascimento"))
) 
campo_data.click()  # Clica no campo de data
campo_data.send_keys(fake.date_of_birth(minimum_age=18, maximum_age=60).strftime("%d/%m/%Y"))  # Gerando uma data de nascimento aleatória

time.sleep(0.5)


# Contato
driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosComplementares.categoriaHolder > div > div > div > div:nth-child(5) > input").send_keys(fake.phone_number())  # Gerando um número de telefone falso
driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosComplementares.categoriaHolder > div > div > div > div:nth-child(6) > input").send_keys(fake.phone_number())  # Gerando um número de telefone falso
driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosComplementares.categoriaHolder > div > div > div > div:nth-child(7) > input").send_keys(fake.phone_number())  # Gerando um número de telefone falso
driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosComplementares.categoriaHolder > div > div > div > div:nth-child(9) > input").send_keys(fake.email())  # Gerando um e-mail falso
driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosComplementares.categoriaHolder > div > div > div > div:nth-child(11) > input").send_keys(fake.city())  # Gerando uma cidade fictícia
driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosComplementares.categoriaHolder > div > div > div > div:nth-child(12) > input").send_keys(fake.country())  # Gerando um país fictício
driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosComplementares.categoriaHolder > div > div > div > div:nth-child(13) > input").send_keys(fake.first_name())  # Gerando o nome do pai fictício
driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosComplementares.categoriaHolder > div > div > div > div:nth-child(14) > input").send_keys(fake.first_name())  # Gerando o nome da mãe fictício

time.sleep(0.5)

# Profissão
driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosComplementares.categoriaHolder > div > div > div > div:nth-child(16) > input").send_keys(fake.job())  # Gerando uma profissão fictícia

time.sleep(0.5)

time.sleep(0.5)

driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.categorias.overflow.overflowY > ul > li.li_enderecos > a").click()


time.sleep(3)

# Aguarda até o elemento estar presente na página
try:
    elemento = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_enderecos.categoriaHolder > div.groupHolder.clearfix.grupo_enderecoResidencial > div > div:nth-child(2) > div:nth-child(1) > div > input"))
    )


    # Preenche o campo de endereço
    elemento.send_keys("15081115")
    

    # Aguarda o botão aparecer e clica nele
    botao = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_enderecos.categoriaHolder > div.groupHolder.clearfix.grupo_enderecoResidencial > div > div:nth-child(2) > div:nth-child(1) > div > a"))
    )
    botao.click()

except Exception as e:
    print(f"Erro: {e}")

time.sleep(5)

element = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#BtYes")))

element.click()
element.click()

wait = WebDriverWait(driver, 1)  


elemento = driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_enderecos.categoriaHolder > div.groupHolder.clearfix.grupo_enderecoResidencial > div > div:nth-child(3) > div:nth-child(2) > input")
elemento.send_keys("1733")



elemento = driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_enderecos.categoriaHolder > div.groupHolder.clearfix.grupo_enderecoResidencial > div > div:nth-child(3) > div:nth-child(3) > input")
elemento.send_keys("Casa")



time.sleep(3)


driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_enderecos.categoriaHolder > div.groupHolder.clearfix.grupo_enderecoResidencial > div > div:nth-child(3) > div:nth-child(9) > label > input").click()

time.sleep(2)

# Clique no botão "Salvar"

driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.btnHolder > a.btModel.btGray.btsave").click()



time.sleep(5)

Select(driver.find_element(By.CSS_SELECTOR, "#gsContratos > div.wdTelas > div.wdWizard.clearfix.telaConsulta > div.wizardHolder > div > div.stepPacote.step4 > div.blockHolder.titulares > ul > li > div.blockHolder.dependentes > ul > li:nth-child(2) > select")).select_by_visible_text("Agregado")



wait = WebDriverWait(driver, 7)  # Tempo máximo de espera
botao_cadastro_registro_obito = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#gsContratos > div.wdTelas > div.wdWizard.clearfix.telaConsulta > div.wizardHolder > div > div.stepPacote.step4 > div.blockHolder.titulares > ul > li > a.sprites.sp-addRegistroObito')))
botao_cadastro_registro_obito.click()

wait = WebDriverWait(driver, 7)  # Tempo máximo de espera
open_lov_falecido = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#cg_23 > div.wdTelas > div > div.catWrapper > div > div > div:nth-child(1) > div > div:nth-child(6) > div > a')))
open_lov_falecido.click()


wait = WebDriverWait(driver, 7)  # Tempo máximo de espera
novo_registo_falecido = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > div.modalHolder > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div:nth-child(3) > a')))
novo_registo_falecido.click()

# Preenchendo os dados pessoais com o Faker
driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosPessoais.categoriaHolder > div > div > div:nth-child(2) > div:nth-child(2) > input").send_keys(faker.name())  # Nome falso
Select(driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosPessoais.categoriaHolder > div > div > div:nth-child(2) > div:nth-child(3) > select")).select_by_visible_text("Física")
Select(driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosPessoais.categoriaHolder > div > div > div:nth-child(2) > div:nth-child(4) > select")).select_by_visible_text("Carteira de Identidade Classista")
driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosPessoais.categoriaHolder > div > div > div.formRow.divPessoaFISICA > div:nth-child(1) > input").send_keys(fake.rg()) # Gerando RG falso
time.sleep(0.5)

# Data de Nascimento com o Faker
campo_data = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "input.dataExpedicao"))
) 
campo_data.click()  # Clica no campo de data
campo_data.send_keys(fake.date_of_birth(minimum_age=18, maximum_age=60).strftime("%d/%m/%Y"))  # Gerando uma data de nascimento aleatória

time.sleep(0.5)

# Gera um CPF válido
cpf = CPF().generate()

# Localiza o campo de CPF
cpf_field = driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosPessoais.categoriaHolder > div > div > div.formRow.divPessoaFISICA > div:nth-child(3) > input")

# Preenche o campo com o CPF gerado
cpf_field.click()
time.sleep(0.5)

cpf_field.send_keys(cpf)

time.sleep(1)

# Dados Complementares
driver.find_element(By.LINK_TEXT, "Dados Complementares").click()

time.sleep(1)

Select(driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosComplementares.categoriaHolder > div > div > div > div:nth-child(1) > select")).select_by_visible_text("Solteiro")
Select(driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosComplementares.categoriaHolder > div > div > div > div:nth-child(2) > select")).select_by_visible_text("Feminino")

# Gerando um e-mail e preenchendo
driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosComplementares.categoriaHolder > div > div > div > div:nth-child(9) > input").send_keys(fake.email())

campo_data = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "input.dataNascimento"))
) 
campo_data.click()  # Clica no campo de data
campo_data.send_keys(fake.date_of_birth(minimum_age=18, maximum_age=60).strftime("%d/%m/%Y"))  # Gerando uma data de nascimento aleatória

time.sleep(0.5)


# Contato
driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosComplementares.categoriaHolder > div > div > div > div:nth-child(5) > input").send_keys(fake.phone_number())  # Gerando um número de telefone falso
driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosComplementares.categoriaHolder > div > div > div > div:nth-child(6) > input").send_keys(fake.phone_number())  # Gerando um número de telefone falso
driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosComplementares.categoriaHolder > div > div > div > div:nth-child(7) > input").send_keys(fake.phone_number())  # Gerando um número de telefone falso
driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosComplementares.categoriaHolder > div > div > div > div:nth-child(9) > input").send_keys(fake.email())  # Gerando um e-mail falso
driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosComplementares.categoriaHolder > div > div > div > div:nth-child(11) > input").send_keys(fake.city())  # Gerando uma cidade fictícia
driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosComplementares.categoriaHolder > div > div > div > div:nth-child(12) > input").send_keys(fake.country())  # Gerando um país fictício
driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosComplementares.categoriaHolder > div > div > div > div:nth-child(13) > input").send_keys(fake.first_name())  # Gerando o nome do pai fictício
driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosComplementares.categoriaHolder > div > div > div > div:nth-child(14) > input").send_keys(fake.first_name())  # Gerando o nome da mãe fictício

time.sleep(0.5)

# Profissão
driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosComplementares.categoriaHolder > div > div > div > div:nth-child(16) > input").send_keys(fake.job())  # Gerando uma profissão fictícia

time.sleep(0.5)

time.sleep(0.5)

driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.categorias.overflow.overflowY > ul > li.li_enderecos > a").click()


time.sleep(3)

# Aguarda até o elemento estar presente na página
try:
    elemento = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_enderecos.categoriaHolder > div.groupHolder.clearfix.grupo_enderecoResidencial > div > div:nth-child(2) > div:nth-child(1) > div > input"))
    )


    # Preenche o campo de endereço
    elemento.send_keys("15081115")
    

    # Aguarda o botão aparecer e clica nele
    botao = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_enderecos.categoriaHolder > div.groupHolder.clearfix.grupo_enderecoResidencial > div > div:nth-child(2) > div:nth-child(1) > div > a"))
    )
    botao.click()

except Exception as e:
    print(f"Erro: {e}")

time.sleep(5)

element = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#BtYes")))

element.click()
element.click()

wait = WebDriverWait(driver, 1)  


elemento = driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_enderecos.categoriaHolder > div.groupHolder.clearfix.grupo_enderecoResidencial > div > div:nth-child(3) > div:nth-child(2) > input")
elemento.send_keys("1733")



elemento = driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_enderecos.categoriaHolder > div.groupHolder.clearfix.grupo_enderecoResidencial > div > div:nth-child(3) > div:nth-child(3) > input")
elemento.send_keys("Casa")



time.sleep(3)


driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_enderecos.categoriaHolder > div.groupHolder.clearfix.grupo_enderecoResidencial > div > div:nth-child(3) > div:nth-child(9) > label > input").click()

time.sleep(2)

# Clique no botão "Salvar"
driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.btnHolder > a.btModel.btGray.btsave").click()

time.sleep(5)

# Localiza o campo pelo ID
wait = WebDriverWait(driver, 7)  # Tempo máximo de espera
campo_data_falecimento = wait.until(EC.element_to_be_clickable((By.XPATH,
    "//input[@grupo='10036' and @ref='25' and contains(@class, 'mandatory')]"
)))
# Limpa o campo (opcional, mas recomendado)
campo_data_falecimento.click()
campo_data_falecimento.send_keys(data_falecimento)

time.sleep(1)



campo_data_sepultamento = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,
    "//input[@grupo='10036' and @ref='96' and contains(@class, 'mandatory')]"
)))

# Tentando clicar após rolar para a posição correta
campo_data_sepultamento.click()
campo_data_sepultamento.send_keys(data_sepultamento)

wait = WebDriverWait(driver, 7)  # Tempo máximo de espera
declaracao_obito= wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#cg_23 > div.wdTelas > div > div.catWrapper > div > div > div:nth-child(1) > div > div:nth-child(44) > input')))
declaracao_obito.send_keys(fake.random_int(min=10, max=10000))

Select(driver.find_element(By.CSS_SELECTOR, "#cg_23 > div.wdTelas > div > div.catWrapper > div > div > div:nth-child(1) > div > div:nth-child(48) > select")).select_by_visible_text("Agregado")

wait = WebDriverWait(driver, 7)  # Tempo máximo de espera
open_lov_declarante = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#cg_23 > div.wdTelas > div > div.catWrapper > div > div > div:nth-child(2) > div > div:nth-child(2) > div > a')))
open_lov_declarante.click()


wait = WebDriverWait(driver, 7)  # Tempo máximo de espera
novo_registo_declarante = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > div.modalHolder > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div:nth-child(3) > a')))
novo_registo_declarante.click()

# Preenchendo os dados pessoais com o Faker
driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosPessoais.categoriaHolder > div > div > div:nth-child(2) > div:nth-child(2) > input").send_keys(faker.name())  # Nome falso
Select(driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosPessoais.categoriaHolder > div > div > div:nth-child(2) > div:nth-child(3) > select")).select_by_visible_text("Física")
Select(driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosPessoais.categoriaHolder > div > div > div:nth-child(2) > div:nth-child(4) > select")).select_by_visible_text("Carteira de Identidade Classista")
driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosPessoais.categoriaHolder > div > div > div.formRow.divPessoaFISICA > div:nth-child(1) > input").send_keys(fake.rg()) # Gerando RG falso
time.sleep(0.5)

# Data de Nascimento com o Faker
campo_data = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "input.dataExpedicao"))
) 
campo_data.click()  # Clica no campo de data
campo_data.send_keys(fake.date_of_birth(minimum_age=18, maximum_age=60).strftime("%d/%m/%Y"))  # Gerando uma data de nascimento aleatória

time.sleep(0.5)

# Gera um CPF válido
cpf = CPF().generate()

# Localiza o campo de CPF
cpf_field = driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosPessoais.categoriaHolder > div > div > div.formRow.divPessoaFISICA > div:nth-child(3) > input")

# Preenche o campo com o CPF gerado
cpf_field.click()
time.sleep(0.5)

cpf_field.send_keys(cpf)

time.sleep(1)

# Dados Complementares
driver.find_element(By.LINK_TEXT, "Dados Complementares").click()

time.sleep(1)

Select(driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosComplementares.categoriaHolder > div > div > div > div:nth-child(1) > select")).select_by_visible_text("Solteiro")
Select(driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosComplementares.categoriaHolder > div > div > div > div:nth-child(2) > select")).select_by_visible_text("Feminino")

# Gerando um e-mail e preenchendo
driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosComplementares.categoriaHolder > div > div > div > div:nth-child(9) > input").send_keys(fake.email())

campo_data = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "input.dataNascimento"))
) 
campo_data.click()  # Clica no campo de data
campo_data.send_keys(fake.date_of_birth(minimum_age=18, maximum_age=60).strftime("%d/%m/%Y"))  # Gerando uma data de nascimento aleatória

time.sleep(0.5)


# Contato
driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosComplementares.categoriaHolder > div > div > div > div:nth-child(5) > input").send_keys(fake.phone_number())  # Gerando um número de telefone falso
driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosComplementares.categoriaHolder > div > div > div > div:nth-child(6) > input").send_keys(fake.phone_number())  # Gerando um número de telefone falso
driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosComplementares.categoriaHolder > div > div > div > div:nth-child(7) > input").send_keys(fake.phone_number())  # Gerando um número de telefone falso
driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosComplementares.categoriaHolder > div > div > div > div:nth-child(9) > input").send_keys(fake.email())  # Gerando um e-mail falso
driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosComplementares.categoriaHolder > div > div > div > div:nth-child(11) > input").send_keys(fake.city())  # Gerando uma cidade fictícia
driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosComplementares.categoriaHolder > div > div > div > div:nth-child(12) > input").send_keys(fake.country())  # Gerando um país fictício
driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosComplementares.categoriaHolder > div > div > div > div:nth-child(13) > input").send_keys(fake.first_name())  # Gerando o nome do pai fictício
driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosComplementares.categoriaHolder > div > div > div > div:nth-child(14) > input").send_keys(fake.first_name())  # Gerando o nome da mãe fictício

time.sleep(0.5)

# Profissão
driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosComplementares.categoriaHolder > div > div > div > div:nth-child(16) > input").send_keys(fake.job())  # Gerando uma profissão fictícia

time.sleep(0.5)

time.sleep(0.5)

driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.categorias.overflow.overflowY > ul > li.li_enderecos > a").click()


time.sleep(3)

# Aguarda até o elemento estar presente na página
try:
    elemento = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_enderecos.categoriaHolder > div.groupHolder.clearfix.grupo_enderecoResidencial > div > div:nth-child(2) > div:nth-child(1) > div > input"))
    )


    # Preenche o campo de endereço
    elemento.send_keys("15081115")
    

    # Aguarda o botão aparecer e clica nele
    botao = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_enderecos.categoriaHolder > div.groupHolder.clearfix.grupo_enderecoResidencial > div > div:nth-child(2) > div:nth-child(1) > div > a"))
    )
    botao.click()

except Exception as e:
    print(f"Erro: {e}")

time.sleep(5)

element = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#BtYes")))

element.click()
element.click()

wait = WebDriverWait(driver, 1)  


elemento = driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_enderecos.categoriaHolder > div.groupHolder.clearfix.grupo_enderecoResidencial > div > div:nth-child(3) > div:nth-child(2) > input")
elemento.send_keys("1733")



elemento = driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_enderecos.categoriaHolder > div.groupHolder.clearfix.grupo_enderecoResidencial > div > div:nth-child(3) > div:nth-child(3) > input")
elemento.send_keys("Casa")



time.sleep(3)


driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_enderecos.categoriaHolder > div.groupHolder.clearfix.grupo_enderecoResidencial > div > div:nth-child(3) > div:nth-child(9) > label > input").click()

time.sleep(2)

# Clique no botão "Salvar"
driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.btnHolder > a.btModel.btGray.btsave").click()

time.sleep(5)

wait = WebDriverWait(driver, 7)  # Tempo máximo de espera
salvar_reg_obito= driver.find_element(By.CSS_SELECTOR, "#cg_23 > div.wdTelas > div > div.btnHolder > a.btModel.btGray.btsave")
salvar_reg_obito.click()


wait = WebDriverWait(driver, 7)  # Tempo máximo de espera
avançar_3 = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#gsContratos > div.wdTelas > div.wdWizard.clearfix.telaConsulta > div.btnHolder > a:nth-child(3)')))
avançar_3.click()

wait = WebDriverWait(driver, 7)  # Tempo máximo de espera
open_lov_serviço = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#gsContratos > div.wdTelas > div.wdWizard.clearfix.telaConsulta > div.wizardHolder > div > div.stepPacote.step2 > div.tableServicos > div.tbHeader.holderTabelaServicos > div.pickerServicos.formCol > div > a')))
open_lov_serviço.click()


wait = WebDriverWait(driver, 7)  # Tempo máximo de espera
novo_registo_serviço = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > div.modalHolder > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div:nth-child(5) > a')))
novo_registo_serviço.click()







# Preenche o campo "Nome"
campo_nome = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#cg_4 > div.wdTelas > div > div.catWrapper > div > div.cat_19.categoriaHolder > div > div > div:nth-child(2) > input")))
campo_nome.send_keys('SERVIÇO TESTE SELENIUM')


# Preenche o campo "Taxa Mensal"
campo_valor_custo_mensal = driver.find_element(By.CSS_SELECTOR, "#cg_4 > div.wdTelas > div > div.catWrapper > div > div.cat_19.categoriaHolder > div > div > div:nth-child(4) > input")
campo_valor_custo_mensal.send_keys(fake.random_int(min=10, max=500))

# Preenche o campo "Taxa Bimestral"
campo_valor_custo_bimestral = driver.find_element(By.CSS_SELECTOR, "#cg_4 > div.wdTelas > div > div.catWrapper > div > div.cat_19.categoriaHolder > div > div > div:nth-child(5) > input.fc.money.mandatory")
campo_valor_custo_bimestral.send_keys(fake.random_int(min=10, max=500))

# Preenche o campo "Taxa Trimestral"
campo_valor_custo_trimestral = driver.find_element(By.CSS_SELECTOR, "#cg_4 > div.wdTelas > div > div.catWrapper > div > div.cat_19.categoriaHolder > div > div > div:nth-child(6) > input.fc.money")
campo_valor_custo_trimestral.send_keys(fake.random_int(min=10, max=500))


# Preenche o campo "Taxa Quadrimestral"
campo_valor_custo_quadrimestral = driver.find_element(By.CSS_SELECTOR, "#cg_4 > div.wdTelas > div > div.catWrapper > div > div.cat_19.categoriaHolder > div > div > div:nth-child(7) > input.fc.money.mandatory")
campo_valor_custo_quadrimestral.send_keys(fake.random_int(min=10, max=500))

# Preenche o campo "Taxa Semestral"
campo_valor_custo_semestral = driver.find_element(By.CSS_SELECTOR, "#cg_4 > div.wdTelas > div > div.catWrapper > div > div.cat_19.categoriaHolder > div > div > div:nth-child(8) > input.fc.money")
campo_valor_custo_semestral.send_keys(fake.random_int(min=10, max=500))


# Preenche o campo "Taxa Anual"
campo_valor_custo_anual = driver.find_element(By.CSS_SELECTOR, "#cg_4 > div.wdTelas > div > div.catWrapper > div > div.cat_19.categoriaHolder > div > div > div:nth-child(9) > input.fc.money")
campo_valor_custo_anual.send_keys(fake.random_int(min=10, max=500))


# Preenche o campo "Taxa Avulsa"
campo_valor_custo_taxa_avulsa = driver.find_element(By.CSS_SELECTOR, "#cg_4 > div.wdTelas > div > div.catWrapper > div > div.cat_19.categoriaHolder > div > div > div:nth-child(10) > input")
campo_valor_custo_taxa_avulsa.send_keys(fake.random_int(min=10, max=500))


# Preenche o campo "Carência (em dias) para pagamento"
campo_valor_custo_taxa_avulsa = driver.find_element(By.CSS_SELECTOR, "#cg_4 > div.wdTelas > div > div.catWrapper > div > div.cat_19.categoriaHolder > div > div > div:nth-child(11) > input")
campo_valor_custo_taxa_avulsa.send_keys(fake.random_int(min=10, max=99))


# Preenche o campo "Carência (em dias) para utilização"
campo_valor_custo_taxa_avulsa = driver.find_element(By.CSS_SELECTOR, "#cg_4 > div.wdTelas > div > div.catWrapper > div > div.cat_19.categoriaHolder > div > div > div:nth-child(12) > input")
campo_valor_custo_taxa_avulsa.send_keys(fake.random_int(min=10, max=99))

# Escolhe uma opção nos dropdowns de "Departamento"


dropdown_tipo_de_serviço = Select(driver.find_element(By.CSS_SELECTOR, "#cg_4 > div.wdTelas > div > div.catWrapper > div > div.cat_19.categoriaHolder > div > div > div:nth-child(13) > select")).select_by_visible_text("Teste")



# Escolhe uma opção nos dropdowns de "Tipo de Serviço"


# Espera até o elemento <select> aparecer no DOM
wait = WebDriverWait(driver, 10)
dropdown_element = wait.until(EC.presence_of_element_located(
    (By.CSS_SELECTOR, "#cg_4 > div.wdTelas > div > div.catWrapper > div > div.cat_19.categoriaHolder > div > div > div:nth-child(14) > select")
))

# Agora sim, usa o Select do Selenium
dropdown_tipo_de_serviço = Select(dropdown_element)

# Seleciona pela opção visível
dropdown_tipo_de_serviço.select_by_visible_text("PET")


openlov = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "#cg_4 > div.wdTelas > div > div.catWrapper > div > div.cat_19.categoriaHolder > div > div > div:nth-child(16) > div > a"))
)
openlov.click()


botao_novo_cemiterio = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.modalHolder > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div:nth-child(4) > a"))
)
botao_novo_cemiterio.click()



wait = WebDriverWait(driver, 10)

campo_cemiterio = wait.until(EC.element_to_be_clickable((
    By.CSS_SELECTOR, "#cg_5 > div.wdTelas > div > div.catWrapper > div > div.cat_categoriaDadosCemiterio.categoriaHolder > div.groupHolder.clearfix.grupo_grupoDadosCemiterio > div > div > div:nth-child(2) > input"
)))

campo_cemiterio.send_keys(cemetery_name)

dropdown_status_cemiterio = driver.find_element(By.CSS_SELECTOR, "#cg_5 > div.wdTelas > div > div.catWrapper > div > div.cat_categoriaDadosCemiterio.categoriaHolder > div.groupHolder.clearfix.grupo_grupoDadosCemiterio > div > div > div:nth-child(3) > select")
dropdown_status_cemiterio.send_keys(Keys.ARROW_DOWN, Keys.RETURN)

campo_dias_para_exumar = driver.find_element(By.CSS_SELECTOR, "#cg_5 > div.wdTelas > div > div.catWrapper > div > div.cat_categoriaDadosCemiterio.categoriaHolder > div.groupHolder.clearfix.grupo_grupoDadosCemiterio > div > div > div:nth-child(4) > input").send_keys(dias_para_exumar)
time.sleep(1)

    # Preenche o campo de endereço
    
    # Preenche o campo de endereço
try:
    elemento = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#cg_5 > div.wdTelas > div > div.catWrapper > div > div.cat_categoriaDadosCemiterio.categoriaHolder > div.groupHolder.clearfix.grupo_grupoEnderecoCemiterio > div > div > div:nth-child(1) > div > input"))
    )


    # Preenche o campo de endereço
    elemento.click()
    elemento.send_keys("15081115")
    elemento.send_keys("15081115")
    elemento.send_keys("15081115")
    elemento.send_keys("15081115")
    elemento.send_keys("15081115")

    time.sleep(2)

    # Aguarda o botão aparecer e clica nele
    botao = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#cg_5 > div.wdTelas > div > div.catWrapper > div > div.cat_categoriaDadosCemiterio.categoriaHolder > div.groupHolder.clearfix.grupo_grupoEnderecoCemiterio > div > div > div:nth-child(1) > div > a"))
    )
    botao.click()

except Exception as e:
    print(f"Erro: {e}")

time.sleep(5)

element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#BtYes")))

element.click()
element.click()


elemento = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#cg_5 > div.wdTelas > div > div.catWrapper > div > div.cat_categoriaDadosCemiterio.categoriaHolder > div.groupHolder.clearfix.grupo_grupoEnderecoCemiterio > div > div > div:nth-child(4) > input")))
elemento.send_keys("1733")



elemento = driver.find_element(By.CSS_SELECTOR, "#cg_5 > div.wdTelas > div > div.catWrapper > div > div.cat_categoriaDadosCemiterio.categoriaHolder > div.groupHolder.clearfix.grupo_grupoEnderecoCemiterio > div > div > div:nth-child(5) > input")
elemento.send_keys("Casa")



wait = WebDriverWait(driver, 7)  # Tempo máximo de espera
categoria = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#cg_5 > div.wdTelas > div > div.categorias.overflow.overflowY > ul > li.li_categoriaExumacaoPorIdade > a')))
categoria.click()


campo_idade_de = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "#cg_5 > div.wdTelas > div > div.catWrapper > div > div.cat_categoriaExumacaoPorIdade.categoriaHolder > div > div.group_grupoExumacaoPorIdade.clearfix.grupoHolder.lista > div > div:nth-child(1) > input"))
)
campo_idade_de.send_keys(fake.random_int(min=1, max=15))


campo_idade_até = driver.find_element(By.CSS_SELECTOR, "#cg_5 > div.wdTelas > div > div.catWrapper > div > div.cat_categoriaExumacaoPorIdade.categoriaHolder > div > div.group_grupoExumacaoPorIdade.clearfix.grupoHolder.lista > div > div:nth-child(2) > input")
campo_idade_até.send_keys(fake.random_int(min=15, max=99))

exumação_por_idade = driver.find_element(By.CSS_SELECTOR, "#cg_5 > div.wdTelas > div > div.catWrapper > div > div.cat_categoriaExumacaoPorIdade.categoriaHolder > div > div.group_grupoExumacaoPorIdade.clearfix.grupoHolder.lista > div > div:nth-child(3) > input").send_keys(dias_para_exumar)


botao_adicionar = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "#cg_5 > div.wdTelas > div > div.catWrapper > div > div.cat_categoriaExumacaoPorIdade.categoriaHolder > div > div.btnListHolder > a.btAddGroup"))
)
botao_adicionar.click()





driver.find_element(By.CSS_SELECTOR, '#cg_5 > div.wdTelas > div > div.btnHolder > a.btModel.btGray.btsave').click()
time.sleep(3)




campo_valor_custo = driver.find_element(By.CSS_SELECTOR, "#cg_4 > div.wdTelas > div > div.catWrapper > div > div.cat_19.categoriaHolder > div > div > div:nth-child(17) > input")
campo_valor_custo.send_keys(fake.random_int(min=10, max=500))





wait = WebDriverWait(driver, 10)  # Tempo máximo de espera
teste = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#cg_4 > div.wdTelas > div > div.categorias.overflow.overflowY > ul > li:nth-child(2) > a')))
teste.click()

wait = WebDriverWait(driver, 7)  # Tempo máximo de espera

campo_idade_de = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "#cg_4 > div.wdTelas > div > div.catWrapper > div > div.cat_10021.categoriaHolder > div > div > div:nth-child(3) > input"))
)
campo_idade_de.send_keys(fake.random_int(min=1, max=15))


campo_idade_até = driver.find_element(By.CSS_SELECTOR, "#cg_4 > div.wdTelas > div > div.catWrapper > div > div.cat_10021.categoriaHolder > div > div > div:nth-child(4) > input")
campo_idade_até.send_keys(fake.random_int(min=15, max=99))



# Preenche o campo "Taxa Mensal"
campo_valor_custo_mensal = driver.find_element(By.CSS_SELECTOR, "#cg_4 > div.wdTelas > div > div.catWrapper > div > div.cat_10021.categoriaHolder > div > div > div:nth-child(5) > input")
campo_valor_custo_mensal.send_keys(fake.random_int(min=10, max=500))

# Preenche o campo "Taxa Bimestral"
campo_valor_custo_bimestral = driver.find_element(By.CSS_SELECTOR, "#cg_4 > div.wdTelas > div > div.catWrapper > div > div.cat_10021.categoriaHolder > div > div > div:nth-child(6) > input.fc.isList.money.mandatory")
campo_valor_custo_bimestral.send_keys(fake.random_int(min=10, max=500))

# Preenche o campo "Taxa Trimestral"
campo_valor_custo_trimestral = driver.find_element(By.CSS_SELECTOR, "#cg_4 > div.wdTelas > div > div.catWrapper > div > div.cat_10021.categoriaHolder > div > div > div:nth-child(7) > input.fc.isList.money")
campo_valor_custo_trimestral.send_keys(fake.random_int(min=10, max=500))


# Preenche o campo "Taxa Quadrimestral"
campo_valor_custo_quadrimestral = driver.find_element(By.CSS_SELECTOR, "#cg_4 > div.wdTelas > div > div.catWrapper > div > div.cat_10021.categoriaHolder > div > div > div:nth-child(8) > input.fc.isList.money.mandatory")
campo_valor_custo_quadrimestral.send_keys(fake.random_int(min=10, max=500))

# Preenche o campo "Taxa Semestral"
campo_valor_custo_semestral = driver.find_element(By.CSS_SELECTOR, "#cg_4 > div.wdTelas > div > div.catWrapper > div > div.cat_10021.categoriaHolder > div > div > div:nth-child(9) > input.fc.isList.money")
campo_valor_custo_semestral.send_keys(fake.random_int(min=10, max=500))


# Preenche o campo "Taxa Anual"
campo_valor_custo_anual = driver.find_element(By.CSS_SELECTOR, "#cg_4 > div.wdTelas > div > div.catWrapper > div > div.cat_10021.categoriaHolder > div > div > div:nth-child(10) > input.fc.isList.money")
campo_valor_custo_anual.send_keys(fake.random_int(min=10, max=500))


# Preenche o campo "Taxa Avulsa"
campo_valor_custo_taxa_avulsa = driver.find_element(By.CSS_SELECTOR, "#cg_4 > div.wdTelas > div > div.catWrapper > div > div.cat_10021.categoriaHolder > div > div > div:nth-child(11) > input")
campo_valor_custo_taxa_avulsa.send_keys(fake.random_int(min=10, max=500))

# Preenche o campo "Repasse"
campo_valor_custo_taxa_avulsa = driver.find_element(By.CSS_SELECTOR, "#cg_4 > div.wdTelas > div > div.catWrapper > div > div.cat_10021.categoriaHolder > div > div > div:nth-child(12) > input")
campo_valor_custo_taxa_avulsa.send_keys(fake.random_int(min=10, max=500))


driver.find_element(By.CSS_SELECTOR, '#cg_4 > div.wdTelas > div > div.catWrapper > div > div.cat_10021.categoriaHolder > div > div > div.btnListHolder > a.btAddGroup').click()

time.sleep(3)

botao_salvar = driver.find_element(By.CSS_SELECTOR, '#cg_4 > div.wdTelas > div > div.btnHolder > a.btModel.btGray.btsave').click()
time.sleep(5)
wait = WebDriverWait(driver, 7)  # Tempo máximo de espera
open_lov_vendedor_serviço = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="gsContratos"]/div[2]/div[2]/div[2]/div/div[4]/div[2]/div[2]/ul/li/ul/li[5]/div/a')))
open_lov_vendedor_serviço.click()


campo_pesquisa_vendedor_serviço = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.modalHolder > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div:nth-child(2) > input"))
)
campo_pesquisa_vendedor_serviço.send_keys('VENDEDOR TESTE SELENIUM AUTOMATIZADO', Keys.ENTER)
time.sleep(0.5)
# Espera até que a linha com o texto desejado esteja visível e clicável
vendedor_serviço = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//td[contains(text(), 'VENDEDOR TESTE SELENIUM AUTOMATIZADO')]"))
)

# Aguarda meio segundo para garantir que o elemento está realmente interagível

# Clica na linha para selecioná-la
vendedor_serviço.click()


 
open_lov_jazigos = WebDriverWait(driver, 7).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#gsContratos > div.wdTelas > div.wdWizard.clearfix.telaConsulta > div.wizardHolder > div > div.stepPacote.step2 > div.cemiHolder > div > div > div > a')))
open_lov_jazigos.click()

wait = WebDriverWait(driver, 7)  # Tempo máximo de espera
novo_registro_jazigos= wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > div.modalHolder > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div.formRow > div:nth-child(2) > a')))
novo_registro_jazigos.click()


campo_numero = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "#cg_7 > div.wdTelas > div > div.catWrapper > div > div > div > div > div > div:nth-child(2) > input"))
)
campo_numero.send_keys(numero_aleatorio)

campo_letra = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "#cg_7 > div.wdTelas > div > div.catWrapper > div > div > div > div > div > div:nth-child(3) > input"))
)
campo_letra.send_keys(letra_aleatoria)

open_lov = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "#cg_7 > div.wdTelas > div > div.catWrapper > div > div > div > div > div > div:nth-child(4) > div > a"))
)
open_lov.click()

open_lov_2 = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.modalHolder > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div.formCol.divPesquisa > div:nth-child(1) > div > a"))
)
open_lov_2.click()



campo_pesquisa_cemi = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.modalHolder > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div.formCol.divPesquisa > input"))
)
campo_pesquisa_cemi.send_keys('cemitério herman descanso', Keys.ENTER)

# Espera até que a linha com o cemitério específico esteja visível
cemiterio = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//td[contains(text(), 'CEMITÉRIO HERMAN DESCANSO')]"))
)

# Clica na linha para selecioná-la
cemiterio.click()


pesquisar = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.modalHolder > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div:nth-child(2) > a"))
)

# Clica na linha para selecioná-la
pesquisar.click()

quadra = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//td[contains(text(), 'QUADRA TESTE SELENIUM AUTOMATIZADO')]"))
)

# Clica na linha para selecioná-la
quadra.click()


select_element = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((
        By.CSS_SELECTOR,
        "#cg_7 > div.wdTelas > div > div.catWrapper > div > div > div > div > div > div:nth-child(5) > select"
    ))
)

# Usa o Select para escolher o valor
Select(select_element).select_by_visible_text("001 - Oito Gavetas com Área de Serviço")



select_element = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((
        By.CSS_SELECTOR,
        "#cg_7 > div.wdTelas > div > div.catWrapper > div > div > div > div > div > div:nth-child(7) > select"
    ))
)

# Usa o Select para escolher o valor
Select(select_element).select_by_visible_text("Disponível")






select_element = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((
        By.CSS_SELECTOR,
        "#cg_7 > div.wdTelas > div > div.catWrapper > div > div > div > div > div > div:nth-child(10) > select"
    ))
)

# Usa o Select para escolher o valor
Select(select_element).select_by_visible_text("Direito")



select_element = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((
        By.CSS_SELECTOR,
        "#cg_7 > div.wdTelas > div > div.catWrapper > div > div > div > div > div > div:nth-child(12) > select"
    ))
)

# Usa o Select para escolher o valor
Select(select_element).select_by_visible_text("Perpétuo")

campo_altura = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "#cg_7 > div.wdTelas > div > div.catWrapper > div > div > div > div > div > div:nth-child(13) > input"))
)
campo_largura = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "#cg_7 > div.wdTelas > div > div.catWrapper > div > div > div > div > div > div:nth-child(14) > input"))
)
campo_comprimento = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "#cg_7 > div.wdTelas > div > div.catWrapper > div > div > div > div > div > div:nth-child(15) > input"))
)

# Preenche os valores nos campos
campo_altura.clear()
campo_altura.send_keys(str(altura_cm))

campo_largura.clear()
campo_largura.send_keys(str(largura_cm))

campo_comprimento.clear()
campo_comprimento.send_keys(str(comprimento_cm))

# Clique no botão "Salvar"
Salvar = driver.find_element(By.CSS_SELECTOR, "#cg_7 > div.wdTelas > div > div.btnHolder > a.btModel.btGray.btsave")
Salvar.click()
time.sleep(5)

wait = WebDriverWait(driver, 7)  # Tempo máximo de espera
avançar_final = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#gsContratos > div.wdTelas > div.wdWizard.clearfix.telaConsulta > div.btnHolder > a:nth-child(3)')))
avançar_final.click()
time.sleep(0.5)
avançar_final.click()
time.sleep(0.5)
avançar_final.click()
time.sleep(0.5)



wait = WebDriverWait(driver, 7)  # Tempo máximo de espera
finalizar_cadastro = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#gsContratos > div.wdTelas > div.wdWizard.clearfix.telaConsulta > div.btnHolder > div')))
finalizar_cadastro.click()

wait = WebDriverWait(driver, 7)  # Tempo máximo de espera
Bt_No = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#BtNo')))
Bt_No.click()


wait = WebDriverWait(driver, 7)  # Tempo máximo de espera
teste = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > div.DESKTOP > div.SIDEBAR.overflow > div > div > div.jazigoAssociado.clearfix > ul > li > a')))
teste.click()

realizar_sepultamento = driver.find_element(By.CSS_SELECTOR, "body > div.DESKTOP > div.SIDEBAR.overflow > div > div > div.listaRO > ul > li > a:nth-child(2)")

# Rolando para o elemento
driver.execute_script("arguments[0].scrollIntoView();", realizar_sepultamento)
realizar_sepultamento.click()

wait = WebDriverWait(driver, 7)  # Tempo máximo de espera
seleçao_gaveta = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#sg > ul > li:nth-child(1)')))
seleçao_gaveta.click()

wait = WebDriverWait(driver, 7)  # Tempo máximo de espera
open_lov_origem_sepultamento = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#sepultar > div.wdTelas > div > div > div:nth-child(4) > div:nth-child(1) > div > div > a')))
open_lov_origem_sepultamento.click()

wait = WebDriverWait(driver, 7)  # Tempo máximo de espera
novo_registro_origem_sepultamento = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > div.modalHolder > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div:nth-child(5) > a')))
novo_registro_origem_sepultamento.click()

wait = WebDriverWait(driver, 7)  # Tempo máximo de espera
locais_traslado = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#cg_8 > div.wdTelas > div > div.catWrapper > div > div > div > div > div:nth-child(2) > input')))
locais_traslado.send_keys('FUNERARIA TESTE SELENIUM AUTOMATIZADO')

wait = WebDriverWait(driver, 7)  # Tempo máximo de espera
salvar_origem_sepultamento = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#cg_8 > div.wdTelas > div > div.btnHolder > a.btModel.btGray.btsave')))
salvar_origem_sepultamento.click()

wait = WebDriverWait(driver, 7)  # Tempo máximo de espera
botao_confirmar = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#sepultar > div.wdTelas > div > div > div.buttonHolder.fRight.padding10 > a:nth-child(2)')))
botao_confirmar.click()

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
