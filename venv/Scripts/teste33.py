from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from faker import Faker
from validate_docbr import CPF
from selenium.webdriver.support.ui import Select
import random
import time


class BrasilProvider:
    """Classe customizada para gerar dados brasileiros (ex: RG)."""
    @staticmethod
    def rg():
        """Gera um número de RG fictício."""
        return ''.join([str(random.randint(0, 9)) for _ in range(8)]) + '-' + str(random.randint(0, 9))


def ajustar_zoom(driver):
    """Ajusta o zoom da página sem interferir em outras guias."""
    driver.execute_script("document.body.style.zoom='90%'")

def preencher_campo(driver, selector, value, wait_time=10):
    """Preenche campos de entrada de forma genérica."""
    campo = WebDriverWait(driver, wait_time).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
    )
    campo.send_keys(value)

def selecionar_dropdown(driver, selector, option_text, wait_time=10):
    """Seleciona uma opção de dropdown baseado no texto visível."""
    dropdown = WebDriverWait(driver, wait_time).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
    )
    Select(dropdown).select_by_visible_text(option_text)

def clicar_botao(driver, selector, wait_time=10):
    """Clica em um botão esperando ele se tornar clicável."""
    botao = WebDriverWait(driver, wait_time).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
    )
    botao.click()

def login(driver, email, senha):
    """Efetua login no sistema."""
    driver.get("https://andromeda.erp-pegasus.com.br/gs/login.xhtml")
    preencher_campo(driver, "#j_id15:email", email)
    preencher_campo(driver, "#j_id15:senha", senha, wait_time=5)
    driver.find_element(By.ID, "j_id15:senha").send_keys(Keys.ENTER)

def preencher_dados_produto(driver, fake):
    """Preenche os dados do produto usando o Faker."""
    preencher_campo(driver, "#fmod_3 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_18.categoriaHolder > div:nth-child(1) > div > div:nth-child(2) > input", fake.word())
    preencher_campo(driver, "#fmod_3 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_18.categoriaHolder > div:nth-child(1) > div > div:nth-child(3) > input", fake.random_number(digits=6))
    preencher_campo(driver, "#fmod_3 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_18.categoriaHolder > div:nth-child(1) > div > div:nth-child(5) > input", fake.random_int(min=1, max=1000))
    preencher_campo(driver, "#fmod_3 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_18.categoriaHolder > div:nth-child(1) > div > div:nth-child(7) > input", fake.ean13())

    selecionar_dropdown(driver, "#fmod_3 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_18.categoriaHolder > div:nth-child(1) > div > div:nth-child(6) > select", "Unidade 1")
    selecionar_dropdown(driver, "#fmod_3 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_18.categoriaHolder > div:nth-child(1) > div > div:nth-child(8) > select", "Departamento 1")
    selecionar_dropdown(driver, "#fmod_3 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_18.categoriaHolder > div:nth-child(1) > div > div:nth-child(11) > select", "Grupo 1")

def preencher_dados_pessoais(driver, fake):
    """Preenche os dados pessoais usando o Faker."""
    preencher_campo(driver, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosPessoais.categoriaHolder > div > div > div:nth-child(2) > div:nth-child(2) > input", fake.name())
    selecionar_dropdown(driver, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosPessoais.categoriaHolder > div > div > div:nth-child(2) > div:nth-child(3) > select", "Física")
    selecionar_dropdown(driver, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosPessoais.categoriaHolder > div > div > div:nth-child(2) > div:nth-child(4) > select", "Carteira de Identidade Classista")
    preencher_campo(driver, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosPessoais.categoriaHolder > div > div > div.formRow.divPessoaFISICA > div:nth-child(1) > input", fake.rg())
    
    campo_data = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input.dataExpedicao")))
    campo_data.click()
    campo_data.send_keys(fake.date_of_birth(minimum_age=18, maximum_age=60).strftime("%d/%m/%Y"))

    cpf_field = driver.find_element(By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosPessoais.categoriaHolder > div > div > div.formRow.divPessoaFISICA > div:nth-child(3) > input")
    cpf = CPF().generate()
    cpf_field.click()
    cpf_field.send_keys(cpf)

def realizar_cadastro(driver, fake):
    """Realiza o preenchimento completo do cadastro."""
    preencher_dados_produto(driver, fake)
    preencher_dados_pessoais(driver, fake)

def main():
    fake = Faker("pt_BR")
    email = 'joaoeduardo.gold@outlook.com'
    senha = '071999gs'
    
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        login(driver, email, senha)
        ajustar_zoom(driver)

        # Navega até a página de cadastro
        driver.get("URL DO SISTEMA AQUI")
        realizar_cadastro(driver, fake)

        # Clica no botão salvar
        clicar_botao(driver, "#cg_1 > div.wdTelas > div > div.btnHolder > a.btModel.btGray.btsave")
        print("Cadastro realizado com sucesso!")
    
    except Exception as e:
        print(f"Erro durante a execução: {e}")
    
    finally:
        time.sleep(3)
        driver.quit()

if __name__ == "__main__":
    main()
