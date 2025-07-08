import faker
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
from selenium.common.exceptions import TimeoutException
import sys
import subprocess
from selenium import webdriver
# Redireciona saída padrão e erros para o arquivo log.txt
sys.stdout = open("log.txt", "w", encoding="utf-8")
sys.stderr = sys.stdout  # Erros também vão para o mesmo arquivo

from faker import Faker

faker = Faker('pt_BR')  # Certifique-se de instanciar o Faker corretamente

cemetery_name = f"Cemitério {faker.last_name()} {faker.random.choice(['Eterno', 'da Paz', 'Memorial', 'Descanso'])}"



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
campo_pesquisa.send_keys("Cemitérios")

campo_pesquisa.send_keys(Keys.RETURN)

time.sleep(3)


cadastrar = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "#fmod_5 > div.wdTelas > div > ul > li:nth-child(1) > a > span"))
)
cadastrar.click()



campo_nome = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "#fmod_5 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroCemiterio > div.catWrapper > div > div.cat_categoriaDadosCemiterio.categoriaHolder > div.groupHolder.clearfix.grupo_grupoDadosCemiterio > div > div > div:nth-child(2) > input"))
)
campo_nome.send_keys(cemetery_name)


Select(driver.find_element(By.CSS_SELECTOR, "#fmod_5 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroCemiterio > div.catWrapper > div > div.cat_categoriaDadosCemiterio.categoriaHolder > div.groupHolder.clearfix.grupo_grupoDadosCemiterio > div > div > div:nth-child(3) > select")).select_by_visible_text("Ativo")



campo_dias_para_exumar = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "#fmod_5 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroCemiterio > div.catWrapper > div > div.cat_categoriaDadosCemiterio.categoriaHolder > div.groupHolder.clearfix.grupo_grupoDadosCemiterio > div > div > div:nth-child(4) > input"))
)
campo_dias_para_exumar.send_keys(dias_para_exumar)

# Aguarda o primeiro select estar visível e seleciona "30 Minutos"
select_30_minutos = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((
        By.CSS_SELECTOR,
        "#fmod_5 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroCemiterio > div.catWrapper > div > div.cat_categoriaDadosCemiterio.categoriaHolder > div.groupHolder.clearfix.grupo_grupoDadosCemiterio > div > div > div:nth-child(5) > select"
    ))
)
Select(select_30_minutos).select_by_visible_text("30 Minutos")

# Aguarda o segundo select estar visível e seleciona "Não"
select_nao = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((
        By.CSS_SELECTOR,
        "#fmod_5 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroCemiterio > div.catWrapper > div > div.cat_categoriaDadosCemiterio.categoriaHolder > div.groupHolder.clearfix.grupo_grupoDadosCemiterio > div > div > div:nth-child(6) > select"
    ))
)
Select(select_nao).select_by_visible_text("Não")
    # Preenche o campo de endereço
try:
    elemento = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#fmod_5 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroCemiterio > div.catWrapper > div > div.cat_categoriaDadosCemiterio.categoriaHolder > div.groupHolder.clearfix.grupo_grupoEnderecoCemiterio > div > div > div:nth-child(1) > div > input"))
    )


    # Preenche o campo de endereço
    elemento.click()
    elemento.send_keys("15081115")


    time.sleep(2)

    # Aguarda o botão aparecer e clica nele
    botao = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#fmod_5 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroCemiterio > div.catWrapper > div > div.cat_categoriaDadosCemiterio.categoriaHolder > div.groupHolder.clearfix.grupo_grupoEnderecoCemiterio > div > div > div:nth-child(1) > div > a"))
    )
    botao.click()

except Exception as e:
    print(f"Erro: {e}")

time.sleep(5)

element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#BtYes")))

element.click()


elemento = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#fmod_5 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroCemiterio > div.catWrapper > div > div.cat_categoriaDadosCemiterio.categoriaHolder > div.groupHolder.clearfix.grupo_grupoEnderecoCemiterio > div > div > div:nth-child(4) > input")))
elemento.send_keys("1733")



elemento = driver.find_element(By.CSS_SELECTOR, "#fmod_5 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroCemiterio > div.catWrapper > div > div.cat_categoriaDadosCemiterio.categoriaHolder > div.groupHolder.clearfix.grupo_grupoEnderecoCemiterio > div > div > div:nth-child(5) > input")
elemento.send_keys("Casa")


wait = WebDriverWait(driver, 7)  # Tempo máximo de espera
categoria = wait.until(
    EC.element_to_be_clickable((By.LINK_TEXT, "Exumação por Idade"))
    )
categoria.click()


campo_idade_de = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "#fmod_5 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroCemiterio > div.catWrapper > div > div.cat_categoriaExumacaoPorIdade.categoriaHolder > div > div.group_grupoExumacaoPorIdade.clearfix.grupoHolder.lista > div > div:nth-child(1) > input"))
)
campo_idade_de.send_keys(fake.random_int(min=1, max=15))


campo_idade_até = driver.find_element(By.CSS_SELECTOR, "#fmod_5 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroCemiterio > div.catWrapper > div > div.cat_categoriaExumacaoPorIdade.categoriaHolder > div > div.group_grupoExumacaoPorIdade.clearfix.grupoHolder.lista > div > div:nth-child(2) > input")
campo_idade_até.send_keys(fake.random_int(min=15, max=99))

exumação_por_idade = driver.find_element(By.CSS_SELECTOR, "#fmod_5 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroCemiterio > div.catWrapper > div > div.cat_categoriaExumacaoPorIdade.categoriaHolder > div > div.group_grupoExumacaoPorIdade.clearfix.grupoHolder.lista > div > div:nth-child(3) > input").send_keys(dias_para_exumar)


botao_adicionar = driver.find_element(By.CSS_SELECTOR, '#fmod_5 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroCemiterio > div.catWrapper > div > div.cat_categoriaExumacaoPorIdade.categoriaHolder > div > div.btnListHolder > a.btAddGroup').click()
time.sleep(3)



Cancelar = wait.until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, '#fmod_5 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroCemiterio > div.btnHolder > a.btModel.btGray.btcancel'))
)
Cancelar.click()




fechar_modal = wait.until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, '#fmod_5 > div.wdTop.ui-draggable-handle > div.wdClose > a'))
)
fechar_modal.click()


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