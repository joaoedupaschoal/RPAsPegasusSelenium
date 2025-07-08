from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from docx import Document
from datetime import datetime
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
    doc.add_paragraph("Cadastro de Controle de Cremação Teste.")
    doc.add_paragraph(f"🗕️ Data do teste: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    doc.add_paragraph("Neste teste, o robô preencherá os campos obrigatórios e cancelará o cadastro de um novo Controle de Cremação.")

    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    wait = WebDriverWait(driver, 10)

    def finalizar_relatorio():
        doc_name = f"relatorio_controle_cremacao_cenario1_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"
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
        campo.send_keys("Controle Cremação", Keys.ENTER)
        time.sleep(3)

    def acessar_formulario():
        cadastrar = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 
            "#fmod_200010 > div.wdTelas > div.telaInicial.clearfix.overflow.overflowY > ul > li:nth-child(1) > a > span")))
        cadastrar.click()
        time.sleep(2)

    def abrir_lov_falecido():
        log(doc, "🔄 Abrindo LOV de Falecido.")
        open_lov_falecido = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 
            "#fmod_200010 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div > div > div > div:nth-child(2) > div > a")))
        open_lov_falecido.click()
        log(doc, "✅ LOV de Falecido aberto.")

    def pesquisar_e_selecionar_falecido():
        log(doc, "🔄 Pesquisando e selecionando falecido.")
        campo_pesquisa = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#txtPesquisa")))
        campo_pesquisa.send_keys('ALEX LOUREIRO SERRAVALLE', Keys.ENTER)
        time.sleep(2)
        falecido = wait.until(EC.element_to_be_clickable((By.XPATH, "//td[contains(text(), 'ALEX LOUREIRO SERRAVALLE')]")))
        falecido.click()
        log(doc, "✅ Falecido selecionado.")

    def preencher_numero_os():
        log(doc, "🔄 Preenchendo campo 'Número OS'.")
        numero_OS = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 
            "#fmod_200010 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div > div > div > div:nth-child(3) > input")))
        numero_OS.send_keys('201680')
        log(doc, "✅ Campo 'Número OS' preenchido.")

    def selecionar_status_aguardando():
        log(doc, "🔄 Selecionando status 'Aguardando'.")
        select_aguardando = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,
            "#fmod_200010 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div > div > div > div:nth-child(4) > select")))
        Select(select_aguardando).select_by_visible_text("Aguardando")
        log(doc, "✅ Status 'Aguardando' selecionado.")

    def selecionar_forno():
        log(doc, "🔄 Selecionando 'Forno 1'.")
        select_forno = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,
            "#fmod_200010 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div > div > div > div:nth-child(5) > select")))
        Select(select_forno).select_by_visible_text("Forno 1")
        log(doc, "✅ 'Forno 1' selecionado.")

    def cancelar():
        cancelar_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,
            "#fmod_200010 > div.wdTelas > div.telaCadastro.clearfix > div.btnHolder > a.btModel.btGray.btcancel")))
        cancelar_btn.click()
        time.sleep(2)



    def confirmar_cancelamento():
        confirmar_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,
            "#BtYes")))
        confirmar_btn.click()
        time.sleep(2)         

    def fechar_modal():
        x_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,
            "#fmod_200010 > div.wdTop.ui-draggable-handle > div.wdClose > a")))
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

    if not safe_action(doc, "Abrindo menu Controle Cremação", abrir_menu, driver, wait)[0]:
        finalizar_relatorio()
        return
    registrar_screenshot_unico("menu_aberto", driver, doc, "Menu 'Controle Cremação' aberto.")

    if not safe_action(doc, "Acessando formulário de cadastro", acessar_formulario, driver, wait)[0]:
        finalizar_relatorio()
        return
    registrar_screenshot_unico("formulario_aberto", driver, doc, "Formulário de cadastro aberto.")

    # PREENCHIMENTO DOS CAMPOS - safe_action individual para cada campo
    if not safe_action(doc, "Abrindo LOV de Falecido", abrir_lov_falecido, driver, wait)[0]:
        finalizar_relatorio()
        return

    if not safe_action(doc, "Pesquisando e selecionando falecido", pesquisar_e_selecionar_falecido, driver, wait)[0]:
        finalizar_relatorio()
        return

    if not safe_action(doc, "Preenchendo Número OS", preencher_numero_os, driver, wait)[0]:
        finalizar_relatorio()
        return

    if not safe_action(doc, "Selecionando status Aguardando", selecionar_status_aguardando, driver, wait)[0]:
        finalizar_relatorio()
        return

    if not safe_action(doc, "Selecionando Forno", selecionar_forno, driver, wait)[0]:
        finalizar_relatorio()
        return

    registrar_screenshot_unico("campos_preenchidos", driver, doc, "Todos os campos preenchidos.")

    # SALVANDO O CADASTRO
    if not safe_action(doc, "Clicando no botão Cancelar", cancelar, driver, wait)[0]:
        finalizar_relatorio()
        return
    registrar_screenshot_unico("apos_cancelar", driver, doc, "Clique no botão Cancelar realizado.")

    if not safe_action(doc, "Clicando no botão Sim", confirmar_cancelamento, driver, wait)[0]:
        finalizar_relatorio()
        return
    registrar_screenshot_unico("apos_cancelar", driver, doc, "Clique no botão Sim realizado.")
    
    # VERIFICANDO MENSAGEM DE RETORNO
    _, tipo_alerta = encontrar_mensagem_alerta(driver, doc)
    if tipo_alerta == "sucesso":
        log(doc, "✅ Mensagem de sucesso exibida.")
    elif tipo_alerta == "alerta":
        log(doc, "⚠️ Mensagem de alerta exibida.")
    elif tipo_alerta == "erro":
        log(doc, "❌ Mensagem de erro exibida.")
    else:
        log(doc, "⚠️ Nenhuma mensagem encontrada após cancelar.")
    registrar_screenshot_unico("mensagem_final", driver, doc, "Mensagem exibida após cancelar.")

    # FECHANDO O FORMULÁRIO
    if not safe_action(doc, "Fechando formulário", fechar_modal, driver, wait)[0]:
        finalizar_relatorio()
        return
    registrar_screenshot_unico("formulario_fechado", driver, doc, "Formulário fechado.")

    log(doc, "✅ Teste de cadastro de Controle de Cremação concluído com sucesso.")
    finalizar_relatorio()

if __name__ == "__main__":
    main()