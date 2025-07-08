
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from validate_docbr import CPF
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
import pyautogui
chrome_options = Options()
chrome_options.add_argument("--start-maximized")  # Inicia já maximizado

driver = webdriver.Chrome(options=chrome_options)

# Abrir a URL
driver.get("https://andromeda.erp-pegasus.com.br/gs/login.xhtml")



# Preencher login
driver.find_element(By.ID, "j_id15:email").send_keys("joaoeduardo.gold@outlook.com")
driver.find_element(By.ID, "j_id15:senha").send_keys("071999gs", Keys.ENTER)


time.sleep(5) 



driver.execute_script("document.body.style.zoom='90%'")





# Simula o pressionamento da tecla F2
driver.find_element(By.TAG_NAME, "body").send_keys(Keys.F2)
time.sleep(1) 





time.sleep(5) 

# Navegação inicial
campo_pesquisa = driver.find_element(By.XPATH, "//input[@placeholder='Busque um cadastro']")

campo_pesquisa.click()

# Digita um texto na pesquisa
campo_pesquisa.send_keys("Pessoas")

# Simula pressionar ENTER (se for necessário para pesquisar)
campo_pesquisa.send_keys(Keys.RETURN)

# Aguarda um tempo para ver o resultado

# 


campo_pesquisa.click()

time.sleep(2)

cadastrar = driver.find_element(By.CSS_SELECTOR, "#fmod_1 > div.wdTelas > div.telaInicial.clearfix.overflow.overflowY > ul > li:nth-child(1) > a > span")


cadastrar.click()

time.sleep(5)



# Preenchendo os dados pessoais
driver.find_element(By.CSS_SELECTOR, "#fmod_1 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroPessoa > div.catWrapper > div > div.cat_dadosPessoais.categoriaHolder > div > div > div:nth-child(2) > div:nth-child(2) > input").send_keys("teste")
Select(driver.find_element(By.CSS_SELECTOR, "#fmod_1 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroPessoa > div.catWrapper > div > div.cat_dadosPessoais.categoriaHolder > div > div > div:nth-child(2) > div:nth-child(3) > select")).select_by_visible_text("Física")
Select(driver.find_element(By.CSS_SELECTOR, "#fmod_1 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroPessoa > div.catWrapper > div > div.cat_dadosPessoais.categoriaHolder > div > div > div:nth-child(2) > div:nth-child(4) > select")).select_by_visible_text("Carteira de Identidade Classista")
driver.find_element(By.CSS_SELECTOR, "#fmod_1 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroPessoa > div.catWrapper > div > div.cat_dadosPessoais.categoriaHolder > div > div > div.formRow.divPessoaFISICA > div:nth-child(1) > input").send_keys("48.768.159-9")

time.sleep(0.5)


# Data de Nascimento


campo_data = WebDriverWait(driver, 10).until(
EC.presence_of_element_located((By.CSS_SELECTOR, "input.dataExpedicao"))
) 
campo_data.click()  # Clica no campo de data
campo_data.send_keys("21/03/2025")  # Digita a data


time.sleep(0.5)

# Gera um CPF válido
cpf = CPF().generate()

# Localiza o campo de CPF
cpf_field = driver.find_element(By.CSS_SELECTOR, "#fmod_1 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroPessoa > div.catWrapper > div > div.cat_dadosPessoais.categoriaHolder > div > div > div.formRow.divPessoaFISICA > div:nth-child(3) > input")

# Preenche o campo com o CPF gerado
cpf_field.click()
cpf_field.send_keys(cpf)

time.sleep(1)


# Dados Complementares
driver.find_element(By.LINK_TEXT, "Dados Complementares").click()

time.sleep(1)

Select(driver.find_element(By.CSS_SELECTOR, "#fmod_1 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroPessoa > div.catWrapper > div > div.cat_dadosComplementares.categoriaHolder > div > div > div > div:nth-child(1) > select")).select_by_visible_text("Solteiro")
Select(driver.find_element(By.CSS_SELECTOR, "#fmod_1 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroPessoa > div.catWrapper > div > div.cat_dadosComplementares.categoriaHolder > div > div > div > div:nth-child(2) > select")).select_by_visible_text("Feminino")

driver.find_element(By.CSS_SELECTOR, "#fmod_1 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroPessoa > div.catWrapper > div > div.cat_dadosComplementares.categoriaHolder > div > div > div > div:nth-child(9) > input").send_keys("teste@teste.com")

campo_data = WebDriverWait(driver, 10).until(
EC.presence_of_element_located((By.CSS_SELECTOR, "input.dataNascimento"))
) 
campo_data.click()  # Clica no campo de data
campo_data.send_keys("21/03/1998")  # Digita a data


#dp1742932609553


time.sleep(2)

# Contato
driver.find_element(By.CSS_SELECTOR, "#fmod_1 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroPessoa > div.catWrapper > div > div.cat_dadosComplementares.categoriaHolder > div > div > div > div:nth-child(5) > input").send_keys("(17)3302-93092")
driver.find_element(By.CSS_SELECTOR, "#fmod_1 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroPessoa > div.catWrapper > div > div.cat_dadosComplementares.categoriaHolder > div > div > div > div:nth-child(6) > input").send_keys("(17)3304-93042")
driver.find_element(By.CSS_SELECTOR, "#fmod_1 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroPessoa > div.catWrapper > div > div.cat_dadosComplementares.categoriaHolder > div > div > div > div:nth-child(7) > input").send_keys("(17)99103-3920")
driver.find_element(By.CSS_SELECTOR, "#fmod_1 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroPessoa > div.catWrapper > div > div.cat_dadosComplementares.categoriaHolder > div > div > div > div:nth-child(9) > input").send_keys("teste@teste.com")
driver.find_element(By.CSS_SELECTOR, "#fmod_1 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroPessoa > div.catWrapper > div > div.cat_dadosComplementares.categoriaHolder > div > div > div > div:nth-child(11) > input").send_keys("rio-pretense")
driver.find_element(By.CSS_SELECTOR, "#fmod_1 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroPessoa > div.catWrapper > div > div.cat_dadosComplementares.categoriaHolder > div > div > div > div:nth-child(12) > input").send_keys("brasileiro")
driver.find_element(By.CSS_SELECTOR, "#fmod_1 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroPessoa > div.catWrapper > div > div.cat_dadosComplementares.categoriaHolder > div > div > div > div:nth-child(13) > input").send_keys("teste pai")
driver.find_element(By.CSS_SELECTOR, "#fmod_1 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroPessoa > div.catWrapper > div > div.cat_dadosComplementares.categoriaHolder > div > div > div > div:nth-child(14) > input").send_keys("teste mae")

time.sleep(0.5)





# Profissão 

driver.find_element(By.CSS_SELECTOR, "#fmod_1 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroPessoa > div.catWrapper > div > div.cat_dadosComplementares.categoriaHolder > div > div > div > div:nth-child(16) > input").send_keys("teste")

time.sleep(0.5)

driver.find_element(By.CSS_SELECTOR, "#fmod_1 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroPessoa > div.categorias.overflow.overflowY > ul > li.li_enderecos > a").click()


time.sleep(3)

# Aguarda até o elemento estar presente na página
try:
    elemento = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#fmod_1 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroPessoa > div.catWrapper > div > div.cat_enderecos.categoriaHolder > div.groupHolder.clearfix.grupo_enderecoResidencial > div > div:nth-child(2) > div:nth-child(1) > div > input"))
    )


    # Preenche o campo de endereço
    elemento.send_keys("15081115")
    
    print("Elemento encontrado, efetuando preenchimento!")

    # Aguarda o botão aparecer e clica nele
    botao = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#fmod_1 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroPessoa > div.catWrapper > div > div.cat_enderecos.categoriaHolder > div.groupHolder.clearfix.grupo_enderecoResidencial > div > div:nth-child(2) > div:nth-child(1) > div > a"))
    )
    botao.click()

except Exception as e:
    print(f"Erro: {e}")

time.sleep(5)

element = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#BtYes")))

element.click()
element.click()
element.click()
element.click()

wait = WebDriverWait(driver, 1)  


elemento = driver.find_element(By.CSS_SELECTOR, "#fmod_1 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroPessoa > div.catWrapper > div > div.cat_enderecos.categoriaHolder > div.groupHolder.clearfix.grupo_enderecoResidencial > div > div:nth-child(3) > div:nth-child(2) > input")
elemento.send_keys("1733")



elemento = driver.find_element(By.CSS_SELECTOR, "#fmod_1 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroPessoa > div.catWrapper > div > div.cat_enderecos.categoriaHolder > div.groupHolder.clearfix.grupo_enderecoResidencial > div > div:nth-child(3) > div:nth-child(3) > input")
elemento.send_keys("Casa")



time.sleep(3)


driver.find_element(By.CSS_SELECTOR, "#fmod_1 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroPessoa > div.catWrapper > div > div.cat_enderecos.categoriaHolder > div.groupHolder.clearfix.grupo_enderecoResidencial > div > div:nth-child(3) > div:nth-child(9) > label > input").click()

time.sleep(2)


# Clique no botão "Salvar"
driver.find_element(By.CSS_SELECTOR, "#fmod_1 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroPessoa > div.btnHolder > a.btModel.btGray.btsave").click()

time.sleep(1)

# Fechar modal
driver.find_element(By.CSS_SELECTOR, "#fmod_1 > div.wdTop.ui-draggable-handle > div.wdClose > a").click()

time.sleep(1)

print('Pessoa salva com sucesso!')


# Aguarda o usuário pressionar "." para fechar o navegador
print('Pressione "." para fechar o navegador...')
while True:
    if input() == ".":  
        break  

# Espera 10 segundos antes de fechar (opcional)



# Fecha o navegador
driver.quit()
