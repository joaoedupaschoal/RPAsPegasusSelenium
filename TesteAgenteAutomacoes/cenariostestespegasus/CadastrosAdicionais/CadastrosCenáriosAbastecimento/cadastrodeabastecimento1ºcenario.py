import sys
import os

# Adiciona a raiz do projeto ao sys.path
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../..")
    )
)


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



def gerar_dados_abastecimento():
    """
    Gera um conjunto completo de dados para um abastecimento:
    - KM Atual
    - Volume abastecido (L)
    - Valor unitário por litro (R$)
    - Desconto (R$)
    - Valor total (calculado: volume × valor unitário - desconto)
    
    Retorna os dados como uma tupla.
    """
    km = random.randint(10000, 300000)
    volume = round(random.uniform(10, 80), 2)
    valor_unitario = round(random.uniform(4.50, 7.00), 2)
    desconto = round(random.uniform(0.00, 20.00), 2)
    valor_total = round(max((volume * valor_unitario) - desconto, 0), 2)

    return km, volume, valor_unitario, desconto, valor_total

km, volume, valor_unitario, desconto, valor_total = gerar_dados_abastecimento()




from datetime import datetime, timedelta


def gerar_dados_frotas(intervalo_max_passado=30):
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
    hoje = datetime.now()
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

    trinta_dias_atras = hoje - timedelta(days=30)

    data_abastecimento_dt = faker.date_between(start_date=trinta_dias_atras, end_date=hoje) 

    return (
        data_multa_dt.strftime("%d/%m/%Y"),
        hora_multa_dt,
        data_notificacao_dt.strftime("%d/%m/%Y"),
        data_vencimento_dt.strftime("%d/%m/%Y"),
        data_pagamento_dt.strftime("%d/%m/%Y"),
        data_abastecimento_dt.strftime("%d/%m/%Y"),

    )


data_multa, hora_multa, data_notificacao, data_vencimento, data_pagamento, data_abastecimento_dt = gerar_dados_frotas()





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
campo_pesquisa.send_keys("Abastecimento", Keys.ENTER)



time.sleep(3)

cadastrar = driver.find_element(By.CSS_SELECTOR, "#fmod_10090 > div.wdTelas > div > ul > li:nth-child(1) > a > span")
cadastrar.click()

time.sleep(2)



campo_data_abastecimento = wait.until(EC.element_to_be_clickable((
    By.XPATH,
    "//input[@maxlength='10' and @name='data' and contains(@class, 'hasDatepicker data mandatory')]"
)))


# Preenche com a data desejada
campo_data_abastecimento.send_keys(data_abastecimento_dt, Keys.TAB)

select_combustivel = Select(wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#fmod_10090 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroAbastecimento > div.catWrapper > div > div > div > div > div > div:nth-child(3) > select"))))
select_combustivel.select_by_visible_text("Gasolina")


# Preenche o campo Veículo (com autocomplete ou seletor de modal)
open_lov_motorista = wait.until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "#fmod_10090 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroAbastecimento > div.catWrapper > div > div > div > div > div > div:nth-child(4) > div > a"))
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



# Preenche o campo Veículo (com autocomplete ou seletor de modal)
open_lov_veiculo = wait.until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "#fmod_10090 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroAbastecimento > div.catWrapper > div > div > div > div > div > div:nth-child(5) > div > a"))
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
open_lov_posto_combustivel = wait.until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "#fmod_10090 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroAbastecimento > div.catWrapper > div > div > div > div > div > div:nth-child(6) > div > a"))
)
open_lov_posto_combustivel.click()



novo_registro_posto_combustível = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.modalHolder > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div:nth-child(3) > a"))
)
time.sleep(1)
novo_registro_posto_combustível.click()



# Preenchendo os dados pessoais com o Faker
driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosPessoais.categoriaHolder > div > div > div:nth-child(2) > div:nth-child(2) > input").send_keys('POSTO COMBUSTÍVEL TESTE SELENIUM AUTOMATIZADO')  # Nome falso
Select(driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosPessoais.categoriaHolder > div > div > div:nth-child(2) > div:nth-child(3) > select")).select_by_visible_text("Jurídica")  # Seleciona Pessoa Jurídica
Select(driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosPessoais.categoriaHolder > div > div > div:nth-child(2) > div:nth-child(4) > select")).select_by_visible_text("Carteira de Identidade Classista")

campo_cnpj =  wait.until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosPessoais.categoriaHolder > div > div > div.formRow.divPessoaJURIDICA > div:nth-child(1) > input"))
)
campo_cnpj.click()      
campo_cnpj.send_keys(fake.cnpj())  # Preenche com um CNPJ válido gerado pelo Faker

campo_nome_fantasia =  wait.until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosPessoais.categoriaHolder > div > div > div.formRow.divPessoaJURIDICA > div:nth-child(2) > input"))
)
campo_nome_fantasia.click()      
campo_nome_fantasia.send_keys('POSTO COMBUSTÍVEL TESTE SELENIUM AUTOMATIZADO')  # Nome fantasia do posto

campo_inscricao_estadual = wait.until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosPessoais.categoriaHolder > div > div > div.formRow.divPessoaJURIDICA > div:nth-child(3) > input"))
)   
campo_inscricao_estadual.click()
campo_inscricao_estadual.send_keys(fake.random_int(min=10000000, max=99999999))  # Inscrição estadual aleatória


campo_inscrcao_municipal = wait.until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosPessoais.categoriaHolder > div > div > div.formRow.divPessoaJURIDICA > div:nth-child(4) > input"))
)
campo_inscrcao_municipal.click()
campo_inscrcao_municipal.send_keys(fake.random_int(min=10000000, max=99999999))  # Inscrição municipal aleatória

open_lov_pacote = wait.until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosPessoais.categoriaHolder > div > div > div.formRow.divPessoaJURIDICA > div.formCol.pacotes > div > a"))
)
open_lov_pacote.click()


campo_pesquisa_pacote = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.modalHolder > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div:nth-child(2) > input"))          
)
campo_pesquisa_pacote.send_keys('PACOTE TESTE SELENIUM AUTOMATIZADO', Keys.ENTER)

pacote = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//td[contains(text(), 'PACOTE TESTE SELENIUM AUTOMATIZADO')]"))
)
# Clica na linha para selecioná-la
pacote.click()

select_classificacao = Select(wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosPessoais.categoriaHolder > div > div > div.formRow.divPessoaJURIDICA > div:nth-child(6) > select"))))
select_classificacao.select_by_visible_text("01 - Ótimo")


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

# Clique no botão "Salvar"
driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.btnHolder > a.btModel.btGray.btsave").click()

time.sleep(5)

km_atual_input = wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "#fmod_10090 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroAbastecimento > div.catWrapper > div > div > div > div > div > div:nth-child(7) > input"))
)
km_atual_input.send_keys(str(km), Keys.TAB)

volume_abastecido_input = wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "#fmod_10090 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroAbastecimento > div.catWrapper > div > div > div > div > div > div:nth-child(8) > input"))
)
volume_abastecido_input.send_keys(str(volume), Keys.TAB)


valor_unitario_input = wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "#fmod_10090 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroAbastecimento > div.catWrapper > div > div > div > div > div > div:nth-child(9) > input"))
)
valor_unitario_input.send_keys(str(valor_unitario), Keys.TAB)

desconto_input = wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "#fmod_10090 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroAbastecimento > div.catWrapper > div > div > div > div > div > div:nth-child(10) > input"))
)
desconto_input.send_keys(str(desconto), Keys.TAB)


# Clique no botão "Salvar"
Salvar = driver.find_element(By.CSS_SELECTOR, "#fmod_10090 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroAbastecimento > div.btnHolder > a.btModel.btGray.btsave")
Salvar.click()
time.sleep(1)


BtNo = wait.until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "#BtNo"))
)   
BtNo.click()


# Fechar modal
X = driver.find_element(By.CSS_SELECTOR, "#fmod_10090 > div.wdTop.ui-draggable-handle > div.wdClose > a")
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




