from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
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
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from utils.actions import log, take_screenshot, safe_action, encontrar_mensagem_alerta, ajustar_zoom

URL = "http://localhost:8080/gs/index.xhtml"
LOGIN_EMAIL = "joaoeduardo.gold@outlook.com"
LOGIN_PASSWORD = "071999gs"

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
    doc.add_paragraph("Cadastro de Cartões - Bandeira – Cenário 1: Preenchimento completo e salvamento.")
    doc.add_paragraph(f"🗕️ Data do teste: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    wait = WebDriverWait(driver, 10)

    def finalizar_relatorio():
        doc_name = f"relatorio_cartoesbandeira_cenario4_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"
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
        time.sleep(3)

    def abrir_menu():
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.F2)
        campo = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Busque um cadastro']")))
        campo.click()
        campo.send_keys("Cartão - Bandeira", Keys.ENTER)


    def acessar_formulario():
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,
            "#fmod_10010 > div.wdTelas > div > ul > li:nth-child(1) > a > span"))).click()
        time.sleep(3)

    def preencher_campos_nao_obrigatorios():
            log(doc, "🔄 Preenchendo apenas os campos não obrigatórios.")

            def selecionar_lov(css_selector_lov, termo_busca, texto_tr):
                driver.find_element(By.CSS_SELECTOR, css_selector_lov).click()
                campo_pesquisa = wait.until(EC.visibility_of_element_located((
                    By.CSS_SELECTOR, 
                    "body > div.modalHolder > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div:nth-child(2) > input"
                )))
                wait.until(EC.element_to_be_clickable((
                    By.CSS_SELECTOR, 
                    "body > div.modalHolder > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div:nth-child(2) > input"
                )))
                time.sleep(1.5)
                from selenium.webdriver.common.keys import Keys
                campo_pesquisa.send_keys(termo_busca + Keys.ENTER)
                time.sleep(3)
                driver.find_element(By.XPATH, f"//tr[contains(., '{texto_tr}')]").click()
                time.sleep(3)


            safe_action(doc, "Selecionando conta crédito 2", lambda: selecionar_lov(
                "#fmod_10010 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_10010.categoriaHolder > div:nth-child(2) > div > div:nth-child(2) > div > div > a",
                "745", "PLANO DE CONTAS DÉBITO SELENIUM"
            ), driver, wait)

            safe_action(doc, "Selecionando histórico padrão", lambda: selecionar_lov(
                "#fmod_10010 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_10010.categoriaHolder > div:nth-child(2) > div > div:nth-child(4) > div > div > a",
                "200116", "DESPESA COM TARIFAS DE CARTÃO"
            ), driver, wait)

            safe_action(doc, "Selecionando centro de custo", lambda: selecionar_lov(
                "#fmod_10010 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_10010.categoriaHolder > div:nth-child(2) > div > div:nth-child(3) > div > div > a",
                "80.79.4703", "TESTE CENTRO DE CUSTO SELENIUM AUTOMATIZADO"
            ), driver, wait)
            
            # Clicar na aba 'Parametrização'
            wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Parametrização"))).click()
            time.sleep(2)

            log(doc, "✍️ Preenchendo campos de parametrização.")

            driver.find_element(By.CSS_SELECTOR,
                "#fmod_10010 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_10094.categoriaHolder > div > div > div:nth-child(3) > input"
            ).send_keys("1")

            driver.find_element(By.CSS_SELECTOR,
                "#fmod_10010 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_10094.categoriaHolder > div > div > div:nth-child(4) > input"
            ).send_keys("12")

            driver.find_element(By.CSS_SELECTOR,
                "#fmod_10010 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_10094.categoriaHolder > div > div > div:nth-child(5) > input"
            ).send_keys("4,2")

            log(doc, "✅ Campos preenchidos. Clicando em Adicionar.")

            driver.find_element(By.CSS_SELECTOR,
                "#fmod_10010 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_10094.categoriaHolder > div > div > div.btnListHolder > a.btAddGroup"
            ).click()
            
            registrar_screenshot_unico("nao_obrigatorios_preenchidos", driver, doc)


    def salvar():
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,
            "#fmod_10010 > div.wdTelas > div.telaCadastro.clearfix > div.btnHolder > a.btModel.btGray.btsave"))).click()
        time.sleep(3)

    def fechar_modal():
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,
            "#fmod_10010 > div.wdTop.ui-draggable-handle > div.wdClose > a"))).click()
        time.sleep(3)

    # FLUXO
    if not safe_action(doc, "Acessando o sistema", lambda: driver.get(URL), driver, wait)[0]: finalizar_relatorio(); return
    registrar_screenshot_unico("url_acessada", driver, doc)

    if not safe_action(doc, "Realizando login", login, driver, wait)[0]: finalizar_relatorio(); return
    registrar_screenshot_unico("login_concluido", driver, doc)

    if not safe_action(doc, "Ajustando zoom", lambda: ajustar_zoom(driver), driver, wait)[0]: finalizar_relatorio(); return
    if not safe_action(doc, "Abrindo menu Cartão Bandeira", abrir_menu, driver, wait)[0]: finalizar_relatorio(); return
    registrar_screenshot_unico("menu_aberto", driver, doc)

    if not safe_action(doc, "Acessando formulário", acessar_formulario, driver, wait)[0]: finalizar_relatorio(); return
    registrar_screenshot_unico("formulario_aberto", driver, doc)

    if not safe_action(doc, "Preenchendo campos Não Obrigatórios", preencher_campos_nao_obrigatorios, driver, wait)[0]: finalizar_relatorio(); return
    if not safe_action(doc, "Clicando em Salvar", salvar, driver, wait)[0]: finalizar_relatorio(); return
    registrar_screenshot_unico("apos_salvar", driver, doc)

    _, tipo_alerta = encontrar_mensagem_alerta(driver, doc)
    if tipo_alerta == "sucesso":
        log(doc, "✅ Mensagem de sucesso exibida.")
    elif tipo_alerta == "alerta":
        log(doc, "⚠️ Mensagem de alerta exibida.")
    elif tipo_alerta == "erro":
        log(doc, "❌ Mensagem de erro exibida.")
    else:
        log(doc, "⚠️ Nenhuma mensagem exibida.")
    registrar_screenshot_unico("mensagem_final", driver, doc)

    if not safe_action(doc, "Fechando formulário", fechar_modal, driver, wait)[0]: finalizar_relatorio(); return
    registrar_screenshot_unico("formulario_fechado", driver, doc)

    log(doc, "✅ Teste concluído com sucesso.")
    finalizar_relatorio()

if __name__ == "__main__":
    main()
