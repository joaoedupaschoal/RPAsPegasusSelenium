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
import time
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
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
campo_pesquisa.send_keys("Conta Bancária", Keys.ENTER)



time.sleep(3)

cadastrar = driver.find_element(By.CSS_SELECTOR, "#fmod_10 > div.wdTelas > div.telaInicial.clearfix.overflow.overflowY > ul > li:nth-child(1) > a > span")
cadastrar.click()

time.sleep(2)


campo_nome = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "#fmod_10 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_22.categoriaHolder > div > div > div:nth-child(2) > input"))
)
campo_nome.send_keys('TESTE CONTA BANCÁRIA SELENIUM AUTOMATIZADO')


Select(driver.find_element(By.CSS_SELECTOR, "#fmod_10 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_22.categoriaHolder > div > div > div:nth-child(3) > select")).select_by_visible_text("001 - Banco do Brasil S.A.")

campo_cedente = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "#fmod_10 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_22.categoriaHolder > div > div > div:nth-child(5) > input"))
)
campo_cedente.send_keys('TESTE CEDENTE SELENIUM AUTOMATIZADO')


Select(driver.find_element(By.CSS_SELECTOR, "#fmod_10 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_22.categoriaHolder > div > div > div:nth-child(6) > select")).select_by_visible_text("Física")

campo_CPF = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "#fmod_10 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_22.categoriaHolder > div > div > div:nth-child(7) > input"))
)
campo_CPF.click()
campo_CPF.send_keys(fake.cpf())

cod_cedente = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "#fmod_10 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_22.categoriaHolder > div > div > div:nth-child(9) > input"))
)
cod_cedente.send_keys(fake.random_int(min=10000000000, max=100000000000))

taxa_antecipação = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "#fmod_10 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_22.categoriaHolder > div > div > div:nth-child(10) > input"))
)
taxa_antecipação.send_keys(fake.random_int(min=10000, max=100000))


Select(driver.find_element(By.CSS_SELECTOR, "#fmod_10 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_22.categoriaHolder > div > div > div:nth-child(11) > select")).select_by_visible_text("Sim")

especie_de_documento = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "#fmod_10 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_22.categoriaHolder > div > div > div:nth-child(12) > input"))
)
especie_de_documento.send_keys('Nota de Débito')

carteira = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "#fmod_10 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_22.categoriaHolder > div > div > div:nth-child(13) > input"))
)
carteira.send_keys(fake.random_int(min=100, max=200))


Select(driver.find_element(By.CSS_SELECTOR, "#fmod_10 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_22.categoriaHolder > div > div > div:nth-child(14) > select")).select_by_visible_text("Com Registro")

cod_empresa_banco = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "#fmod_10 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_22.categoriaHolder > div > div > div:nth-child(15) > input"))
)
cod_empresa_banco.send_keys(fake.random_int(min=10000, max=2000000))

identificador_cedente = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "#fmod_10 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_22.categoriaHolder > div > div > div:nth-child(16) > input"))
)
identificador_cedente.send_keys('§')

instrução_1 = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "#fmod_10 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_22.categoriaHolder > div > div > div:nth-child(17) > input"))
)
instrução_1.send_keys('TESTE INSTRUÇÃO 1')

instrução_2 = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "#fmod_10 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_22.categoriaHolder > div > div > div:nth-child(18) > input"))
)
instrução_2.send_keys('TESTE INSTRUÇÃO 2')

instrução_3 = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "#fmod_10 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_22.categoriaHolder > div > div > div:nth-child(19) > input"))
)
instrução_3.send_keys('TESTE INSTRUÇÃO 3')

instrução_4 = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "#fmod_10 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_22.categoriaHolder > div > div > div:nth-child(20) > input"))
)
instrução_4.send_keys('TESTE INSTRUÇÃO 4')


endereço_completo = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "#fmod_10 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_22.categoriaHolder > div > div > div:nth-child(22) > input"))
)
endereço_completo.send_keys('RUA DAS FLORES, 1221, BAIRRO TESTE SELENIUM, CASA')

open_lov = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "#fmod_10 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_22.categoriaHolder > div > div > div:nth-child(23) > div > div > a"))
)
driver.execute_script("arguments[0].scrollIntoView();", open_lov)

open_lov.click()

time.sleep(1)
campo_pesquisa_conta_debito = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.modalHolder > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div:nth-child(2) > input"))
)
campo_pesquisa_conta_debito.send_keys('745', Keys.ENTER)

time.sleep(1)

element = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//tr[td[@ref='1' and contains(text(), 'PLANO DE CONTAS DÉBITO SELENIUM')]]//a[@class='linkAlterar']"))
)
element.click()

local_pagamento = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "#fmod_10 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_22.categoriaHolder > div > div > div:nth-child(24) > input"))
)
local_pagamento.send_keys('TESTE LOCAL PAGAMENTO')

Select(driver.find_element(By.CSS_SELECTOR, "#fmod_10 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_22.categoriaHolder > div > div > div:nth-child(25) > select")).select_by_visible_text("Não")

dias_devolução = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "#fmod_10 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_22.categoriaHolder > div > div > div:nth-child(26) > input"))
)
driver.execute_script("arguments[0].scrollIntoView();", dias_devolução)

dias_devolução.send_keys(fake.random_int(min=1, max=30))

Select(driver.find_element(By.CSS_SELECTOR, "#fmod_10 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_22.categoriaHolder > div > div > div:nth-child(27) > select")).select_by_visible_text("Banco")

campo_auxiliar = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "#fmod_10 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_22.categoriaHolder > div > div > div:nth-child(29) > input"))
)
driver.execute_script("arguments[0].scrollIntoView();", campo_auxiliar)

campo_auxiliar.send_keys('TESTE')
'''
codigo_flash = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "#fmod_10 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_22.categoriaHolder > div > div > div:nth-child(30) > input"))
)
codigo_flash.send_keys('1231224')
'''

campo_multa = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "#fmod_10 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_22.categoriaHolder > div > div > div:nth-child(32) > input"))
)
driver.execute_script("arguments[0].scrollIntoView();", campo_multa)

campo_multa.send_keys(fake.random_int(min=10000, max=100000))
'''
carencia_dias_multa = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "#fmod_10 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_22.categoriaHolder > div > div > div:nth-child(33) > input"))
)
carencia_dias_multa.send_keys(fake.random_int(min=0, max=30))
'''
juros_de_mora = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "#fmod_10 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_22.categoriaHolder > div > div > div:nth-child(35) > input"))
)
driver.execute_script("arguments[0].scrollIntoView();", juros_de_mora)

juros_de_mora.send_keys(fake.random_int(min=100, max=10000))

nome_sacador = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "#fmod_10 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_22.categoriaHolder > div > div > div:nth-child(36) > input"))
)
driver.execute_script("arguments[0].scrollIntoView();", nome_sacador)

nome_sacador.send_keys(fake.name())

desconto = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "#fmod_10 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_22.categoriaHolder > div > div > div:nth-child(39) > input"))
)
driver.execute_script("arguments[0].scrollIntoView();", desconto)

desconto.send_keys(fake.random_int(min=100, max=500))

Select(driver.find_element(By.CSS_SELECTOR, "#fmod_10 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_22.categoriaHolder > div > div > div:nth-child(38) > select")).select_by_visible_text("Percentual")

qtd_dias_para_desconto = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "#fmod_10 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_22.categoriaHolder > div > div > div:nth-child(40) > input"))
)
qtd_dias_para_desconto.send_keys(fake.random_int(min=1, max=15))

'''qtd_dias_para_protesto = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "#fmod_10 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_22.categoriaHolder > div > div > div:nth-child(46) > input"))
)
driver.execute_script("arguments[0].scrollIntoView();", qtd_dias_para_protesto)

qtd_dias_para_protesto.send_keys(fake.random_int(min=100, max=500))

Select(driver.find_element(By.CSS_SELECTOR, "#fmod_10 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_22.categoriaHolder > div > div > div:nth-child(45) > select")).select_by_visible_text("Sim")
'''
element = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "#fmod_10 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_22.categoriaHolder > div > div > div:nth-child(49) > select"))
)

# Dá scroll até o elemento
driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)

# Faz a seleção
Select(element).select_by_visible_text("Sim")

taxas = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.LINK_TEXT, "Taxas"))
)
taxas.click()


liquidação_boleto_pago = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "#fmod_10 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_10091.categoriaHolder > div > div > div:nth-child(2) > input"))
)
liquidação_boleto_pago.send_keys(fake.random_int(min=100, max=10000))

registro_de_boleto = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "#fmod_10 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_10091.categoriaHolder > div > div > div:nth-child(3) > input"))
)
registro_de_boleto.send_keys(fake.random_int(min=100, max=10000))


alteração_dados_boleto = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "#fmod_10 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_10091.categoriaHolder > div > div > div:nth-child(4) > input"))
)
alteração_dados_boleto.send_keys(fake.random_int(min=100, max=10000))

pix = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.LINK_TEXT, "Pix"))
)
pix.click()



element = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "#fmod_10 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_10092.categoriaHolder > div > div > div:nth-child(2) > select"))
)
Select(element).select_by_visible_text("Celular")

chave_celular = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "#fmod_10 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_10092.categoriaHolder > div > div > div:nth-child(3) > input"))
)
chave_celular.send_keys(fake.phone_number())




# Clique no botão "Salvar"
Cancelar = driver.find_element(By.CSS_SELECTOR, "#fmod_10 > div.wdTelas > div.telaCadastro.clearfix > div.btnHolder > a.btModel.btGray.btcancel")
Cancelar.click()
time.sleep(1)


# Fechar modal
X = driver.find_element(By.CSS_SELECTOR, "#fmod_10 > div.wdTop.ui-draggable-handle > div.wdClose > a")
X.click()
time.sleep(1)

from selenium.common.exceptions import TimeoutException, NoSuchElementException



def encontrar_mensagem_alerta(timeout=20):
    seletores = [
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



