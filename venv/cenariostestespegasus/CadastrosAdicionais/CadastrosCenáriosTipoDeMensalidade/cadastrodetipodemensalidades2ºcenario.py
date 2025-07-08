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

import random
import string

# Inclui letras, dígitos e símbolos
todos_caracteres = string.ascii_letters + string.digits + string.punctuation

identificador = ''.join(random.choices(todos_caracteres, k=2))


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

'''Nesse teste, o robô preencherá todos os dados e clicará em Cancelar'''

print('Nesse teste, o robô preencherá todos os dados e clicará em Cancelar')



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
campo_pesquisa.send_keys("Tipo de Mensalidade", Keys.ENTER)



time.sleep(3)

cadastrar = driver.find_element(By.CSS_SELECTOR, "#fmod_10027 > div.wdTelas > div.telaInicial.clearfix.overflow.overflowY > ul > li:nth-child(1) > a > span")
cadastrar.click()

time.sleep(2)


campo_nome = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "#fmod_10027 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_10029.categoriaHolder > div > div > div:nth-child(2) > input"))
)
campo_nome.send_keys('TESTE TIPO DE MENSALIDADE SELENIUM AUTOMATIZADO')

campo_descrição = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "#fmod_10027 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_10029.categoriaHolder > div > div > div:nth-child(3) > input"))
)
campo_descrição.send_keys('TESTE DESCRIÇÃO SELENIUM AUTOMATIZADO')


campo_identificador = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "#fmod_10027 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_10029.categoriaHolder > div > div > div:nth-child(4) > input"))
)
campo_identificador.clear()
campo_identificador.send_keys(identificador)


Select(driver.find_element(By.CSS_SELECTOR, "#fmod_10027 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_10029.categoriaHolder > div > div > div:nth-child(5) > select")).select_by_visible_text("Não")

campo_template = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "#fmod_10027 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_10029.categoriaHolder > div > div > div:nth-child(6) > input"))
)
campo_template.send_keys('TESTE TEMPLATE SELENIUM AUTOMATIZADO')

informações_financeiras = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.LINK_TEXT, "Informações Financeiras"))
)
informações_financeiras.click()

open_lov_conta_credito = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "#fmod_10027 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_10030.categoriaHolder > div:nth-child(1) > div > div:nth-child(2) > div > div > a"))
)
open_lov_conta_credito.click()
time.sleep(2)
campo_pesquisa = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.modalHolder > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div:nth-child(2) > input"))
)
campo_pesquisa.send_keys('748', Keys.ENTER)
time.sleep(1)   

# Espera até que a linha com o texto desejado esteja visível e clicável
conta_credito = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//tr[td[contains(text(), 'TESTE PLANO DE CONTAS SELENIUM AUTOMATIZADO')]]//a[contains(@class, 'linkAlterar')]"))
)
conta_credito.click()

open_lov_conta_debito = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "#fmod_10027 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_10030.categoriaHolder > div:nth-child(1) > div > div:nth-child(3) > div > div > a"))
)
open_lov_conta_debito.click()
time.sleep(2)

campo_pesquisa = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.modalHolder > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div:nth-child(2) > input"))
)
campo_pesquisa.send_keys('565', Keys.ENTER)
time.sleep(1)   

# Espera até que a linha com o texto desejado esteja visível e clicável
conta_debito = WebDriverWait(driver, 10).until(
    
    EC.element_to_be_clickable((By.XPATH, "//tr[td[contains(text(), 'TRANSITÓRIA DE CARTÃO DE DÉBITO')]]//a[contains(@class, 'linkAlterar')]"))
)
conta_debito.click()



open_lov_historico_padrao = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "#fmod_10027 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_10030.categoriaHolder > div:nth-child(1) > div > div:nth-child(4) > div > div > a"))
)
open_lov_historico_padrao.click()
time.sleep(2)

campo_pesquisa = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.modalHolder > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div:nth-child(2) > input"))
)
campo_pesquisa.send_keys('200129', Keys.ENTER)
time.sleep(1)   

# Espera até que a linha com o texto desejado esteja visível e clicável
historico_padrao = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//td[contains(text(), 'TESTE HISTÓRICO PADRÃO SELENIUM AUTOMATIZADO')]"))
)
historico_padrao.click()




open_lov_centro_de_custo = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "#fmod_10027 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_10030.categoriaHolder > div:nth-child(1) > div > div:nth-child(5) > div > div > a"))
)
open_lov_centro_de_custo.click()
time.sleep(2)

campo_pesquisa = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.modalHolder > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div:nth-child(2) > input"))
)
campo_pesquisa.send_keys('80.79.4703', Keys.ENTER)
time.sleep(1)   

# Espera até que a linha com o texto desejado esteja visível e clicável
centro_de_custo = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//td[contains(text(), '80.79.4703')]"))
)
centro_de_custo.click()





open_lov_conta_credito_2 = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "#fmod_10027 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_10030.categoriaHolder > div:nth-child(2) > div > div:nth-child(2) > div > div > a"))
)
open_lov_conta_credito_2.click()
time.sleep(2)

campo_pesquisa = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.modalHolder > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div:nth-child(2) > input"))
)
campo_pesquisa.send_keys('748', Keys.ENTER)
time.sleep(1)   

# Espera até que a linha com o texto desejado esteja visível e clicável
conta_credito_2 = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//tr[td[contains(text(), 'TESTE PLANO DE CONTAS SELENIUM AUTOMATIZADO')]]//a[contains(@class, 'linkAlterar')]"))
)
conta_credito_2.click()



open_lov_conta_debito_2 = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "#fmod_10027 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_10030.categoriaHolder > div:nth-child(2) > div > div:nth-child(3) > div > div > a"))
)
open_lov_conta_debito_2.click()
time.sleep(2)

campo_pesquisa = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.modalHolder > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div:nth-child(2) > input"))
)
campo_pesquisa.send_keys('565', Keys.ENTER)
time.sleep(1)   

# Espera até que a linha com o texto desejado esteja visível e clicável
conta_debito_2 = WebDriverWait(driver, 10).until(
    
    EC.element_to_be_clickable((By.XPATH, "//tr[td[contains(text(), 'TRANSITÓRIA DE CARTÃO DE DÉBITO')]]//a[contains(@class, 'linkAlterar')]"))
)
conta_debito_2.click()


open_lov_historico_padrao_2 = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "#fmod_10027 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_10030.categoriaHolder > div:nth-child(2) > div > div:nth-child(4) > div > div > a"))
)
open_lov_historico_padrao_2.click()
time.sleep(2)

campo_pesquisa = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.modalHolder > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div:nth-child(2) > input"))
)
campo_pesquisa.send_keys('200129', Keys.ENTER)
time.sleep(1)   

# Espera até que a linha com o texto desejado esteja visível e clicável
historico_padrao_2 = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//td[contains(text(), 'TESTE HISTÓRICO PADRÃO SELENIUM AUTOMATIZADO')]"))
)
historico_padrao_2.click()




open_lov_centro_de_custo_2 = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "#fmod_10027 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_10030.categoriaHolder > div:nth-child(2) > div > div:nth-child(5) > div > div > a"))
)
open_lov_centro_de_custo_2.click()
time.sleep(2)

campo_pesquisa = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.modalHolder > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div:nth-child(2) > input"))
)
campo_pesquisa.send_keys('80.79.4703', Keys.ENTER)
time.sleep(1)   

# Espera até que a linha com o texto desejado esteja visível e clicável
centro_de_custo_2 = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//td[contains(text(), '80.79.4703')]"))
)
centro_de_custo_2.click()





open_lov_conta_credito_3 = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "#fmod_10027 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_10030.categoriaHolder > div:nth-child(3) > div > div:nth-child(2) > div > div > a"))
)
open_lov_conta_credito_3.click()
time.sleep(2)

campo_pesquisa = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.modalHolder > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div:nth-child(2) > input"))
)
campo_pesquisa.send_keys('748', Keys.ENTER)
time.sleep(1)   

# Espera até que a linha com o texto desejado esteja visível e clicável
conta_credito_3 = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//tr[td[contains(text(), 'TESTE PLANO DE CONTAS SELENIUM AUTOMATIZADO')]]//a[contains(@class, 'linkAlterar')]"))
)
conta_credito_3.click()


open_lov_conta_debito_3 = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "#fmod_10027 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_10030.categoriaHolder > div:nth-child(3) > div > div:nth-child(3) > div > div > a"))
)
open_lov_conta_debito_3.click()
time.sleep(2)

campo_pesquisa = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.modalHolder > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div:nth-child(2) > input"))
)
campo_pesquisa.send_keys('565', Keys.ENTER)
time.sleep(1)   

# Espera até que a linha com o texto desejado esteja visível e clicável
conta_debito_3 = WebDriverWait(driver, 10).until(
    
    EC.element_to_be_clickable((By.XPATH, "//tr[td[contains(text(), 'TRANSITÓRIA DE CARTÃO DE DÉBITO')]]//a[contains(@class, 'linkAlterar')]"))
)
conta_debito_3.click()


open_lov_historico_padrao_3 = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "#fmod_10027 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_10030.categoriaHolder > div:nth-child(3) > div > div:nth-child(4) > div > div > a"))
)
open_lov_historico_padrao_3.click()
time.sleep(2)

campo_pesquisa = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.modalHolder > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div:nth-child(2) > input"))
)
campo_pesquisa.send_keys('200129', Keys.ENTER)
time.sleep(1)   

# Espera até que a linha com o texto desejado esteja visível e clicável
historico_padrao_3 = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//td[contains(text(), 'TESTE HISTÓRICO PADRÃO SELENIUM AUTOMATIZADO')]"))
)
historico_padrao_3.click()




open_lov_centro_de_custo_3 = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "#fmod_10027 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_10030.categoriaHolder > div:nth-child(3) > div > div:nth-child(5) > div > div > a"))
)
open_lov_centro_de_custo_3.click()
time.sleep(2)

campo_pesquisa = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.modalHolder > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div:nth-child(2) > input"))
)
campo_pesquisa.send_keys('80.79.4703', Keys.ENTER)
time.sleep(1)   

# Espera até que a linha com o texto desejado esteja visível e clicável
centro_de_custo_3 = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//td[contains(text(), '80.79.4703')]"))
)
centro_de_custo_3.click()






open_lov_conta_credito_4 = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "#fmod_10027 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_10030.categoriaHolder > div:nth-child(4) > div > div:nth-child(2) > div > div > a"))
)

# Scroll até o elemento
driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", open_lov_conta_credito_4)


open_lov_conta_credito_4.click()
time.sleep(2)

campo_pesquisa = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.modalHolder > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div:nth-child(2) > input"))
)
campo_pesquisa.send_keys('748', Keys.ENTER)
time.sleep(3)   

# Espera até que a linha com o texto desejado esteja visível e clicável
conta_credito_4 = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.XPATH, "//tr[td[contains(text(), 'TESTE PLANO DE CONTAS SELENIUM AUTOMATIZADO')]]//a[contains(@class, 'linkAlterar')]"))
)
conta_credito_4.click()



open_lov_conta_debito_4 = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "#fmod_10027 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_10030.categoriaHolder > div:nth-child(4) > div > div:nth-child(3) > div > div > a"))
)
open_lov_conta_debito_4.click()
time.sleep(2)

campo_pesquisa = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.modalHolder > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div:nth-child(2) > input"))
)
campo_pesquisa.send_keys('565', Keys.ENTER)
time.sleep(3)   

# Espera até que a linha com o texto desejado esteja visível e clicável
conta_debito_4 = WebDriverWait(driver, 10).until(
    
    EC.visibility_of_element_located((By.XPATH, "//tr[td[contains(text(), 'TRANSITÓRIA DE CARTÃO DE DÉBITO')]]//a[contains(@class, 'linkAlterar')]"))
)
conta_debito_4.click()




open_lov_historico_padrao_4 = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "#fmod_10027 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_10030.categoriaHolder > div:nth-child(4) > div > div:nth-child(4) > div > div > a"))
)
open_lov_historico_padrao_4.click()
time.sleep(2)

campo_pesquisa = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.modalHolder > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div:nth-child(2) > input"))
)
campo_pesquisa.send_keys('200129', Keys.ENTER)
time.sleep(3)   

# Espera até que a linha com o texto desejado esteja visível e clicável
historico_padrao_4 = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.XPATH, "//td[contains(text(), 'TESTE HISTÓRICO PADRÃO SELENIUM AUTOMATIZADO')]"))
)
historico_padrao_4.click()




open_lov_centro_de_custo_4 = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "#fmod_10027 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_10030.categoriaHolder > div:nth-child(4) > div > div:nth-child(5) > div > div > a"))
)
open_lov_centro_de_custo_4.click()
time.sleep(2)

campo_pesquisa = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.modalHolder > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div:nth-child(2) > input"))
)
campo_pesquisa.send_keys('80.79.4703', Keys.ENTER)
time.sleep(3)   

# Espera até que a linha com o texto desejado esteja visível e clicável
centro_de_custo_4 = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.XPATH, "//td[contains(text(), '80.79.4703')]"))
)
centro_de_custo_4.click()







# Clique no botão "Cancelar"
Cancelar = driver.find_element(By.CSS_SELECTOR, "#fmod_10027 > div.wdTelas > div.telaCadastro.clearfix > div.btnHolder > a.btModel.btGray.btcancel")
Cancelar.click()
time.sleep(1)

Sim = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "#BtYes"))
)
Sim.click()

# Fechar modal
X = driver.find_element(By.CSS_SELECTOR, "#fmod_10027 > div.wdTop.ui-draggable-handle > div.wdClose > a")
X.click()
time.sleep(3)

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




