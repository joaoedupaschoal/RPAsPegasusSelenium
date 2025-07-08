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




'''Nesse teste, o robô preencherá apenas os Campos Obrigatórios e salvará o cadastro'''

print('Nesse teste, o robô preencherá apenas os Campos Obrigatórios e salvará o cadastro')



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
wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#fmod_23 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div > div:nth-child(1) > div > div:nth-child(6) > div > a'))).click()

wait = WebDriverWait(driver, 7)  # Tempo máximo de espera
wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > div.modalHolder > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div:nth-child(3) > a'))).click()


# Preenchendo os dados pessoais com o Faker
driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosPessoais.categoriaHolder > div > div > div:nth-child(2) > div:nth-child(2) > input").send_keys(fake.name())  # Nome falso
Select(driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosPessoais.categoriaHolder > div > div > div:nth-child(2) > div:nth-child(3) > select")).select_by_visible_text("Física")
Select(driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosPessoais.categoriaHolder > div > div > div:nth-child(2) > div:nth-child(4) > select")).select_by_visible_text("Carteira de Identidade Classista")
driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosPessoais.categoriaHolder > div > div > div.formRow.divPessoaFISICA > div:nth-child(1) > input").send_keys(fake.ssn())  # Gerando um RG falso

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

driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.categorias.overflow.overflowY > ul > li.li_enderecos > a").click()


time.sleep(3)

# Aguarda até o elemento estar presente na página
try:
    elemento = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_enderecos.categoriaHolder > div.groupHolder.clearfix.grupo_enderecoResidencial > div > div:nth-child(2) > div:nth-child(1) > div > input"))
    )


    # Preenche o campo de endereço
    elemento.send_keys("15081115")
    
    print("Elemento encontrado, efetuando preenchimento!")

    # Aguarda o botão aparecer e clica nele
    botao = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_enderecos.categoriaHolder > div.groupHolder.clearfix.grupo_enderecoResidencial > div > div:nth-child(2) > div:nth-child(1) > div > a"))
    )
    botao.click()

except Exception as e:
    print(f"Erro: {e}")


element = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#BtYes")))

element.click()
element.click()


time.sleep(5)




elemento = driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_enderecos.categoriaHolder > div.groupHolder.clearfix.grupo_enderecoResidencial > div > div:nth-child(3) > div:nth-child(2) > input")
elemento.send_keys("1733")



elemento = driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_enderecos.categoriaHolder > div.groupHolder.clearfix.grupo_enderecoResidencial > div > div:nth-child(3) > div:nth-child(3) > input")
elemento.send_keys("Casa")



time.sleep(3)


driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_enderecos.categoriaHolder > div.groupHolder.clearfix.grupo_enderecoResidencial > div > div:nth-child(3) > div:nth-child(9) > label > input").click()

time.sleep(2)


# Clique no botão "Salvar"
driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.btnHolder > a.btModel.btGray.btsave").click()

time.sleep(1)





campo_data_falecimento = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "input.hasDatepicker.mandatory.fc"))
)

# Interage com o campo diretamente
campo_data_falecimento.click()
campo_data_falecimento.clear()
campo_data_falecimento.send_keys(data_falecimento)







time.sleep(3)

campo_data_sepultamento = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[grupo="10036"][ref="96"]'))
)

# Rolando até o elemento
driver.execute_script("arguments[0].scrollIntoView();", campo_data_sepultamento)

# Tentando clicar após rolar para a posição correta
campo_data_sepultamento.click()
campo_data_sepultamento.clear()
campo_data_sepultamento.send_keys(data_sepultamento)
campo_data_sepultamento.send_keys(data_sepultamento)
campo_data_sepultamento.send_keys(data_sepultamento)




campo_numero_declaracao_obito = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "#fmod_23 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div > div:nth-child(1) > div > div:nth-child(44) > input"))
)
campo_numero_declaracao_obito.send_keys(fake.random_int(min=1, max=99))

Select(driver.find_element(By.CSS_SELECTOR, "#fmod_23 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div > div:nth-child(1) > div > div:nth-child(45) > select")).select_by_visible_text("Particular")

Select(driver.find_element(By.CSS_SELECTOR, "#fmod_23 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div > div:nth-child(1) > div > div:nth-child(48) > select")).select_by_visible_text("Avô(ó)")

declarante = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, '#fmod_23 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div > div:nth-child(2) > div > div:nth-child(2) > div > a'))
)

# Rolando até o elemento
driver.execute_script("arguments[0].scrollIntoView();", declarante)

# Tentando clicar após rolar para a posição correta
declarante.click()




# Rolando para o elemento




wait = WebDriverWait(driver, 7)  # Tempo máximo de espera
wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > div.modalHolder > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div:nth-child(3) > a'))).click()


# Preenchendo os dados pessoais com o Faker
driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosPessoais.categoriaHolder > div > div > div:nth-child(2) > div:nth-child(2) > input").send_keys(fake.name())  # Nome falso
Select(driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosPessoais.categoriaHolder > div > div > div:nth-child(2) > div:nth-child(3) > select")).select_by_visible_text("Física")
Select(driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosPessoais.categoriaHolder > div > div > div:nth-child(2) > div:nth-child(4) > select")).select_by_visible_text("Carteira de Identidade Classista")
driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosPessoais.categoriaHolder > div > div > div.formRow.divPessoaFISICA > div:nth-child(1) > input").send_keys(fake.ssn())  # Gerando um RG falso

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


element = driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosComplementares.categoriaHolder > div > div > div > div:nth-child(11) > input")

# Rolando até o elemento
driver.execute_script("arguments[0].scrollIntoView();", element)

# Inserindo o valor no campo de entrada
element.send_keys(fake.city())
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
    
    print("Elemento encontrado, efetuando preenchimento!")

    # Aguarda o botão aparecer e clica nele
    botao = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_enderecos.categoriaHolder > div.groupHolder.clearfix.grupo_enderecoResidencial > div > div:nth-child(2) > div:nth-child(1) > div > a"))
    )
    botao.click()

except Exception as e:
    print(f"Erro: {e}")


element = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#BtYes")))

element.click()
element.click()


time.sleep(5)




elemento = driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_enderecos.categoriaHolder > div.groupHolder.clearfix.grupo_enderecoResidencial > div > div:nth-child(3) > div:nth-child(2) > input")
elemento.send_keys("1733")



elemento = driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_enderecos.categoriaHolder > div.groupHolder.clearfix.grupo_enderecoResidencial > div > div:nth-child(3) > div:nth-child(3) > input")
elemento.send_keys("Casa")



time.sleep(3)


driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_enderecos.categoriaHolder > div.groupHolder.clearfix.grupo_enderecoResidencial > div > div:nth-child(3) > div:nth-child(9) > label > input").click()

time.sleep(2)


# Clique no botão "Salvar"

driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.btnHolder > a.btModel.btGray.btsave").click()









Select(driver.find_element(By.CSS_SELECTOR, "#fmod_23 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div > div:nth-child(2) > div > div:nth-child(12) > select")).select_by_visible_text("Avô(ó)")


driver.find_element(By.CSS_SELECTOR, "#fmod_23 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div > div:nth-child(2) > div > div:nth-child(13) > input").send_keys(fake.phone_number())  # Gerando um número de telefone falso
driver.find_element(By.CSS_SELECTOR, "#fmod_23 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div > div:nth-child(2) > div > div:nth-child(14) > input").send_keys(fake.phone_number())  # Gerando um número de telefone falso
driver.find_element(By.CSS_SELECTOR, "#fmod_23 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div > div:nth-child(2) > div > div:nth-child(15) > input").send_keys(fake.phone_number())  # Gerando um número de telefone falso

time.sleep(10)
# Clique no botão "Salvar"

salvar = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "#fmod_23 > div.wdTelas > div.telaCadastro.clearfix > div.btnHolder > a.btModel.btGray.btsave > span"))
) 
salvar.click()  




wait = WebDriverWait(driver, 10)
botao_nao = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#BtNo")))
botao_nao.click()
botao_nao.click()
botao_nao.click()

time.sleep(3)

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
