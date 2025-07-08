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
from datetime import datetime, timedelta
from validate_docbr import CPF
from faker.providers import BaseProvider
import random
from faker import Faker
from selenium.common.exceptions import NoSuchElementException, TimeoutException

import string
from selenium.common.exceptions import TimeoutException
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
'''Nesse teste, o robô preencherá todos os dados e clicará em Salvar'''

print('Nesse teste, o robô preencherá todos os dados e clicará em Salvar')



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
campo_pesquisa.send_keys("Vendedor")

elemento = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "/html/body/div[17]/ul/li[55]/a"))
)
elemento.click()


time.sleep(3)

cadastrar = driver.find_element(By.CSS_SELECTOR, "#fmod_10020 > div.wdTelas > div.telaInicial.clearfix.overflow.overflowY > ul > li:nth-child(1) > a > span")
cadastrar.click()

time.sleep(2)


wait = WebDriverWait(driver, 7)  # Tempo máximo de espera
open_lov_pessoa_vendedor= wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#fmod_10020 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div > div > div > div:nth-child(2) > div > a')))
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

'''

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
'''
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
    EC.element_to_be_clickable((By.CSS_SELECTOR, "#fmod_10020 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div > div > div > div:nth-child(4) > input"))  # ou ID, CSS_SELECTOR etc.
)
campo.click()
campo.send_keys(carteira_trabalho)


WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, '#fmod_10020 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div > div > div > div:nth-child(5) > input'))
).send_keys(pis)


wait = WebDriverWait(driver, 7)  # Tempo máximo de espera
open_lov_tipo_supervisor= wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#fmod_10020 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div > div > div > div:nth-child(6) > div > a')))
open_lov_tipo_supervisor.click()

campo_pesquisa_supervisor = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.modalHolder > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div:nth-child(2) > input.nomePesquisa"))
)
time.sleep(1)
campo_pesquisa_supervisor.send_keys('SUPERVISOR TESTE SELENIUM AUTOMATIZADO', Keys.ENTER)

time.sleep(1)


# Espera até que a linha com o cemitério específico esteja visível
supervisor = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//td[contains(text(), 'SUPERVISOR TESTE SELENIUM AUTOMATIZADO')]"))
)

# Clica na linha para selecioná-la
supervisor.click()


wait = WebDriverWait(driver, 7)  # Tempo máximo de espera
comissao_porcentagem= wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#fmod_10020 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div > div > div > div:nth-child(7) > input')))
comissao_porcentagem.send_keys(fake.random_int(min=10, max=500))

wait = WebDriverWait(driver, 7)  # Tempo máximo de espera
comissao_reais= wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#fmod_10020 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div > div > div > div:nth-child(8) > input')))
comissao_reais.send_keys(fake.random_int(min=10, max=500))

Select(driver.find_element(By.CSS_SELECTOR, "#fmod_10020 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div > div > div > div:nth-child(9) > select")).select_by_visible_text("Interno")
Select(driver.find_element(By.CSS_SELECTOR, "#fmod_10020 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div > div > div > div:nth-child(11) > select")).select_by_visible_text("Carteira Assinada")

wait = WebDriverWait(driver, 7)  # Tempo máximo de espera
campo_auto= wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#fmod_10020 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div > div > div > div:nth-child(12) > input')))
campo_auto.click()
time.sleep(5)




# Clique no botão "Salvar"
Salvar = driver.find_element(By.CSS_SELECTOR, "#fmod_10020 > div.wdTelas > div.telaCadastro.clearfix > div.btnHolder > a.btModel.btGray.btsave")
Salvar.click()
time.sleep(1)

# Fechar modal
X = driver.find_element(By.CSS_SELECTOR, "#fmod_10020 > div.wdTop.ui-draggable-handle > div.wdClose > a")
X.click()
time.sleep(1)

from selenium.common.exceptions import TimeoutException, NoSuchElementException

def encontrar_mensagem_alerta(timeout=20):
    seletores = [
        (".alerts.salvo", "sucesso"),
        (".alerts.salvo", "sucesso"),
        (".alerts.alerta", "alerta"),
        (".alerts.erro", "erro"),
    ]
    
    fim = time.time() + timeout
    while time.time() < fim:
        for seletor, tipo in seletores:
            try:
                elemento = driver.find_element(By.CSS_SELECTOR, seletor)
                if elemento.is_displayed():
                    print(f"Mensagem de {tipo}:", elemento.text)
                    return elemento
            except NoSuchElementException:
                continue
        time.sleep(0.5)  # Espera meio segundo antes de tentar de novo (evita travar o CPU)

    print("Nenhuma mensagem encontrada dentro dos 10 segundos.")
    return None

# Espera inicialmente o container de alertas (ainda é útil para performance)
try:
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".alerts")))
    encontrar_mensagem_alerta(timeout=10)
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

time.sleep(3)
driver.quit()




