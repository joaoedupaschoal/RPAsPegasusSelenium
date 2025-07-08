from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from docx import Document
from datetime import datetime, timedelta
import subprocess
import time
import os
import sys
from faker import Faker
from faker.providers import BaseProvider
import random
import string
from selenium.common.exceptions import TimeoutException, NoSuchElementException

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from utils.actions import log, take_screenshot, safe_action, encontrar_mensagem_alerta, ajustar_zoom

URL = "http://localhost:8080/gs/index.xhtml"
LOGIN_EMAIL = "joaoeduardo.gold@outlook.com"
LOGIN_PASSWORD = "071999gs"

# Configuração do Faker
class BrasilProvider(BaseProvider):
    def rg(self):
        numeros = [str(random.randint(0, 9)) for _ in range(8)]
        return ''.join(numeros) + '-' + str(random.randint(0, 9))

fake = Faker("pt_BR")
fake.add_provider(BrasilProvider)

# Geração de dados aleatórios
def gerar_datas_validas(dias_adiante=30):
    hoje = datetime.today()
    data_inicial = hoje.strftime('%d/%m/%Y')
    data_final = (hoje + timedelta(days=dias_adiante)).strftime('%d/%m/%Y')
    return data_inicial, data_final

data_inicio, data_fim = gerar_datas_validas()

# Controle de screenshots únicas
screenshot_registradas = set()
def registrar_screenshot_unico(nome, driver, doc, descricao=None):
    if nome not in screenshot_registradas:
        if descricao:
            log(doc, f"📸 {descricao}")
        take_screenshot(driver, doc, nome)
        screenshot_registradas.add(nome)

def main():
    doc = Document()
    doc.add_heading("RELATÓRIO DO TESTE", 0)
    doc.add_paragraph("Cadastro de Comissão Teste.")
    doc.add_paragraph(f"🗕️ Data do teste: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    doc.add_paragraph("Neste teste, o robô preencherá os campos obrigatórios e salvará o cadastro de uma nova Comissão.")

    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    wait = WebDriverWait(driver, 10)

    def finalizar_relatorio():
        doc_name = f"relatorio_comissao_cenario1_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"
        doc.save(doc_name)
        log(doc, f"📄 Relatório salvo como: {doc_name}")
        try:
            subprocess.run(["start", "winword", doc_name], shell=True)
        except Exception as e:
            log(doc, f"Erro ao abrir o Word: {e}")
        driver.quit()

    def login():
        wait.until(EC.presence_of_element_located((By.ID, "j_id15:email"))).send_keys(LOGIN_EMAIL)
        wait.until(EC.presence_of_element_located((By.ID, "j_id15:senha"))).send_keys(LOGIN_PASSWORD, Keys.ENTER)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        time.sleep(2)

    def abrir_menu():
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.F2)
        campo = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Busque um cadastro']")))
        campo.click()
        campo.send_keys("Comissão")
        
        elemento = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[17]/div[2]/ul/li[8]/a")))
        elemento.click()
        time.sleep(3)

    def acessar_formulario():
        cadastrar = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 
            "#fmod_200030 > div.wdTelas > div.telaInicial.clearfix.overflow.overflowY > ul > li:nth-child(1) > a > span")))
        cadastrar.click()
        time.sleep(2)

    def preencher_comissao_porcentagem_vendedor():
        log(doc, "🔄 Preenchendo campo 'Comissão Porcentagem Vendedor'.")
        campo_comissao_porcentagem_vendedor = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 
            "#fmod_200030 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_200035.categoriaHolder > div > div > div:nth-child(2) > input")))
        campo_comissao_porcentagem_vendedor.send_keys(fake.random_int(min=10, max=500))
        log(doc, "✅ Campo 'Comissão Porcentagem Vendedor' preenchido.")

    def preencher_comissao_meta_vendedor():
        log(doc, "🔄 Preenchendo campo 'Comissão Meta Vendedor'.")
        campo_comissao_meta_vendedor = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 
            "#fmod_200030 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_200035.categoriaHolder > div > div > div:nth-child(3) > input")))
        campo_comissao_meta_vendedor.send_keys(fake.random_int(min=10, max=500))
        log(doc, "✅ Campo 'Comissão Meta Vendedor' preenchido.")

    def preencher_data_inicial_vendedor():
        log(doc, "🔄 Preenchendo campo 'Data Inicial Vendedor'.")
        comissao_data_inicial = wait.until(EC.element_to_be_clickable((By.XPATH,
            "//input[@grupo='100059' and @ref='100212' and contains(@class, 'mandatory')]")))
        comissao_data_inicial.click()
        comissao_data_inicial.send_keys(data_inicio)
        comissao_data_inicial.send_keys(data_inicio)
        log(doc, "✅ Campo 'Data Inicial Vendedor' preenchido.")

    def preencher_data_final_vendedor():
        log(doc, "🔄 Preenchendo campo 'Data Final Vendedor'.")
        comissao_data_final = wait.until(EC.element_to_be_clickable((By.XPATH,
            "//input[@grupo='100059' and @ref='100213' and contains(@class, 'mandatory')]")))
        comissao_data_final.click()
        comissao_data_final.send_keys(data_fim)
        comissao_data_final.send_keys(data_fim)
        log(doc, "✅ Campo 'Data Final Vendedor' preenchido.")

    def preencher_campanha_vendedor():
        log(doc, "🔄 Preenchendo campo 'Campanha Vendedor'.")
        campo_campanha_vendedor = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 
            "#fmod_200030 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_200035.categoriaHolder > div > div > div:nth-child(6) > input")))
        campo_campanha_vendedor.send_keys('TESTE CAMPANHA VENDEDOR SELENIUM AUTOMATIZADO')
        log(doc, "✅ Campo 'Campanha Vendedor' preenchido.")

    def acessar_aba_supervisores():
        log(doc, "🔄 Acessando aba 'Comissões - Supervisores'.")
        click_comissao_supervisores = wait.until(EC.visibility_of_element_located((By.LINK_TEXT, "Comissões - Supervisores")))
        click_comissao_supervisores.click()
        log(doc, "✅ Aba 'Comissões - Supervisores' acessada.")

    def preencher_comissao_porcentagem_supervisor():
        log(doc, "🔄 Preenchendo campo 'Comissão Porcentagem Supervisor'.")
        campo_comissao_porcentagem_supervisor = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 
            "#fmod_200030 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_200036.categoriaHolder > div > div > div:nth-child(2) > input")))
        campo_comissao_porcentagem_supervisor.send_keys(fake.random_int(min=10, max=500))
        log(doc, "✅ Campo 'Comissão Porcentagem Supervisor' preenchido.")

    def preencher_comissao_meta_supervisor():
        log(doc, "🔄 Preenchendo campo 'Comissão Meta Supervisor'.")
        campo_comissao_meta_supervisor = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 
            "#fmod_200030 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_200036.categoriaHolder > div > div > div:nth-child(3) > input")))
        campo_comissao_meta_supervisor.send_keys(fake.random_int(min=10, max=500))
        log(doc, "✅ Campo 'Comissão Meta Supervisor' preenchido.")

    def preencher_data_inicial_supervisor():
        log(doc, "🔄 Preenchendo campo 'Data Inicial Supervisor'.")
        comissao_data_inicial_sup = wait.until(EC.element_to_be_clickable((By.XPATH,
            "//input[@grupo='100060' and @ref='100212' and contains(@class, 'mandatory')]")))
        comissao_data_inicial_sup.click()
        comissao_data_inicial_sup.send_keys(data_inicio)
        comissao_data_inicial_sup.send_keys(data_inicio)
        log(doc, "✅ Campo 'Data Inicial Supervisor' preenchido.")

    def preencher_data_final_supervisor():
        log(doc, "🔄 Preenchendo campo 'Data Final Supervisor'.")
        comissao_data_final_sup = wait.until(EC.element_to_be_clickable((By.XPATH,
            "//input[@grupo='100060' and @ref='100213' and contains(@class, 'mandatory')]")))
        comissao_data_final_sup.click()
        comissao_data_final_sup.send_keys(data_fim)
        comissao_data_final_sup.send_keys(data_fim)
        log(doc, "✅ Campo 'Data Final Supervisor' preenchido.")

    def preencher_campanha_supervisor():
        log(doc, "🔄 Preenchendo campo 'Campanha Supervisor'.")
        campo_campanha_supervisor = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 
            "#fmod_200030 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_200036.categoriaHolder > div > div > div:nth-child(6) > input")))
        campo_campanha_supervisor.send_keys('TESTE CAMPANHA SUPERVISOR SELENIUM AUTOMATIZADO')
        log(doc, "✅ Campo 'Campanha Supervisor' preenchido.")

    def salvar():
        salvar_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,
            "#fmod_200030 > div.wdTelas > div.telaCadastro.clearfix > div.btnHolder > a.btModel.btGray.btsave")))
        salvar_btn.click()
        time.sleep(2)

    def fechar_modal():
        x_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,
            "#fmod_200030 > div.wdTop.ui-draggable-handle > div.wdClose > a")))
        x_btn.click()
        time.sleep(1)

    # EXECUÇÃO COM safe_action INDIVIDUAL PARA CADA AÇÃO
    if not safe_action(doc, "Acessando o sistema", lambda: driver.get(URL), driver, wait)[0]:
        finalizar_relatorio()
        return
    registrar_screenshot_unico("url_acessada", driver, doc, "Sistema acessado.")

    if not safe_action(doc, "Realizando login", login, driver, wait)[0]:
        finalizar_relatorio()
        return
    registrar_screenshot_unico("login_concluido", driver, doc, "Login realizado.")

    if not safe_action(doc, "Ajustando zoom", lambda: ajustar_zoom(driver), driver, wait)[0]:
        finalizar_relatorio()
        return

    if not safe_action(doc, "Abrindo menu Comissão", abrir_menu, driver, wait)[0]:
        finalizar_relatorio()
        return
    registrar_screenshot_unico("menu_aberto", driver, doc, "Menu 'Comissão' aberto.")

    if not safe_action(doc, "Acessando formulário de cadastro", acessar_formulario, driver, wait)[0]:
        finalizar_relatorio()
        return
    registrar_screenshot_unico("formulario_aberto", driver, doc, "Formulário de cadastro aberto.")

    # SEÇÃO VENDEDORES - safe_action individual para cada campo
    if not safe_action(doc, "Preenchendo Comissão Porcentagem Vendedor", preencher_comissao_porcentagem_vendedor, driver, wait)[0]:
        finalizar_relatorio()
        return

    if not safe_action(doc, "Preenchendo Comissão Meta Vendedor", preencher_comissao_meta_vendedor, driver, wait)[0]:
        finalizar_relatorio()
        return

    if not safe_action(doc, "Preenchendo Data Inicial Vendedor", preencher_data_inicial_vendedor, driver, wait)[0]:
        finalizar_relatorio()
        return

    if not safe_action(doc, "Preenchendo Data Final Vendedor", preencher_data_final_vendedor, driver, wait)[0]:
        finalizar_relatorio()
        return

    if not safe_action(doc, "Preenchendo Campanha Vendedor", preencher_campanha_vendedor, driver, wait)[0]:
        finalizar_relatorio()
        return

    registrar_screenshot_unico("vendedores_preenchido", driver, doc, "Campos de Vendedores preenchidos.")

    # ACESSANDO ABA SUPERVISORES
    if not safe_action(doc, "Acessando aba Supervisores", acessar_aba_supervisores, driver, wait)[0]:
        finalizar_relatorio()
        return

    # SEÇÃO SUPERVISORES - safe_action individual para cada campo
    if not safe_action(doc, "Preenchendo Comissão Porcentagem Supervisor", preencher_comissao_porcentagem_supervisor, driver, wait)[0]:
        finalizar_relatorio()
        return

    if not safe_action(doc, "Preenchendo Comissão Meta Supervisor", preencher_comissao_meta_supervisor, driver, wait)[0]:
        finalizar_relatorio()
        return

    if not safe_action(doc, "Preenchendo Data Inicial Supervisor", preencher_data_inicial_supervisor, driver, wait)[0]:
        finalizar_relatorio()
        return

    if not safe_action(doc, "Preenchendo Data Final Supervisor", preencher_data_final_supervisor, driver, wait)[0]:
        finalizar_relatorio()
        return

    if not safe_action(doc, "Preenchendo Campanha Supervisor", preencher_campanha_supervisor, driver, wait)[0]:
        finalizar_relatorio()
        return

    registrar_screenshot_unico("supervisores_preenchido", driver, doc, "Campos de Supervisores preenchidos.")

    # SALVANDO O CADASTRO
    if not safe_action(doc, "Clicando no botão Salvar", salvar, driver, wait)[0]:
        finalizar_relatorio()
        return
    registrar_screenshot_unico("apos_salvar", driver, doc, "Clique no botão Salvar realizado.")

    # VERIFICANDO MENSAGEM DE RETORNO
    _, tipo_alerta = encontrar_mensagem_alerta(driver, doc)
    if tipo_alerta == "sucesso":
        log(doc, "✅ Mensagem de sucesso exibida.")
    elif tipo_alerta == "alerta":
        log(doc, "⚠️ Mensagem de alerta exibida.")
    elif tipo_alerta == "erro":
        log(doc, "❌ Mensagem de erro exibida.")
    else:
        log(doc, "⚠️ Nenhuma mensagem encontrada após salvar.")
    registrar_screenshot_unico("mensagem_final", driver, doc, "Mensagem exibida após salvar.")

    # FECHANDO O FORMULÁRIO
    if not safe_action(doc, "Fechando formulário", fechar_modal, driver, wait)[0]:
        finalizar_relatorio()
        return
    registrar_screenshot_unico("formulario_fechado", driver, doc, "Formulário fechado.")

    log(doc, "✅ Teste de cadastro de Comissão concluído com sucesso.")
    finalizar_relatorio()

if __name__ == "__main__":
    main()