from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Configurar o driver
driver = webdriver.Chrome()
driver.maximize_window()  # Inicia em tela cheia

# Abrir a URL
driver.get("https://andromeda.erp-pegasus.com.br/gs/login.xhtml")

# Esperar até que os campos de login estejam visíveis
wait = WebDriverWait(driver, 10)
email_input = wait.until(EC.presence_of_element_located((By.ID, "j_id15:email")))
senha_input = wait.until(EC.presence_of_element_located((By.ID, "j_id15:senha")))

# Preencher login
email_input.send_keys("joaoeduardo.gold@outlook.com")
senha_input.send_keys("071999gs", Keys.ENTER)

time.sleep(3) 

# Simula o pressionamento da tecla F2 
driver.find_element(By.TAG_NAME, "body").send_keys(Keys.F2)

# Aguarda até o campo de pesquisa aparecer 
campo_pesquisa = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Busque um cadastro']")))
campo_pesquisa.click()
campo_pesquisa.send_keys("Pessoas", Keys.RETURN)

# Aguarda o botão "Cadastrar" aparecer e clica
cadastrar = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#fmod_1 .telaInicial ul li:nth-child(1) a span")))
cadastrar.click()

# Preencher Nome
# Aguardar até que o campo esteja visível e interativo
nome_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".cat_dadosPessoais input")))

wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,  "#fmod_1 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroPessoa > div.catWrapper > div > div.cat_dadosPessoais.categoriaHolder > div > div > div:nth-child(2) > div:nth-child(2) > input']"))).send_keys("teste")

# Selecionar tipo de pessoa
Select(wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#fmod_1 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroPessoa > div.catWrapper > div > div.cat_dadosPessoais.categoriaHolder > div > div > div:nth-child(2) > div:nth-child(3) > select")))).select_by_visible_text("Física")


Select(wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#fmod_1 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroPessoa > div.catWrapper > div > div.cat_dadosPessoais.categoriaHolder > div > div > div:nth-child(2) > div:nth-child(4) > select")))).select_by_visible_text("Carteira de Identidade Classista")


# Preencher CPF
cpf_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".divPessoaFISICA input")))
cpf_field.send_keys("385.022.090-78")

# Clique no botão "Salvar"
salvar_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".btnHolder .btsave")))
salvar_button.click()

# Fechar modal, se necessário
try:
    close_modal = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".wdTop .wdClose a")))
    close_modal.click()
except:
    print("Nenhum modal para fechar.")

# Aguarda entrada do usuário para fechar o navegador
input('Pressione "Enter" para fechar o navegador...')
driver.quit()
