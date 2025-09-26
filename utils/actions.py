
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from docx.shared import Inches
from datetime import datetime
import os
import time
SCREENSHOT_DIR = "screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

def registrar_screenshot_unico(nome, driver, doc, descricao=None):
    if nome not in screenshot_registradas:
        if descricao:
            log(doc, f"📸 {descricao}")
        take_screenshot(driver, doc, nome)
        screenshot_registradas.add(nome)


def log(doc, msg):
    print(msg)
    doc.add_paragraph(msg)

def take_screenshot(driver, doc, filename):
    path = os.path.join(SCREENSHOT_DIR, f"{filename}_{datetime.now().strftime('%H%M%S')}.png")
    driver.save_screenshot(path)
    log(doc, f"🖼️ Screenshot: {path}")
    doc.add_picture(path, width=Inches(5.5))
    return path

def safe_action(doc, name, func, driver, wait, error_msg=None):
    log(doc, f"🔄 {name}...")
    try:
        result = func()
        log(doc, f"✅ {name} realizado com sucesso.")
        take_screenshot(driver, doc, name.lower().replace(" ", "_"))
        return True, result
    except (TimeoutException, NoSuchElementException) as e:
        log(doc, error_msg if error_msg else f"❌ Erro ao tentar {name.lower()}: {str(e)}")
        take_screenshot(driver, doc, f"erro_{name.lower().replace(' ', '_')}")
        return False, None

def encontrar_mensagem_alerta():
    seletores = [
        (".alerts.salvo", "✅ Menasagem de Sucesso"),
        (".alerts.alerta", "⚠️ Menasagem de Alerta"),
        (".alerts.erro", "❌ Menasagem de Erro"),
    ]
    for seletor, tipo, emoji in seletores:
        try:
            elemento = driver.find_element(By.CSS_SELECTOR, seletor)
            if elemento.is_displayed():
                try:
                    texto = elemento.find_element(By.TAG_NAME, "p").text.strip()
                except NoSuchElementException:
                    texto = elemento.text.strip()
                log(doc, f"{emoji} Mensagem de {tipo}: {texto}")
                take_screenshot(driver, doc, f"mensagem_{tipo}")
                return elemento, tipo
        except NoSuchElementException:
            continue
    log(doc, "❌ Nenhuma mensagem de alerta encontrada.")
    take_screenshot(driver, doc, "mensagem_nao_encontrada")
    return None, None

def ajustar_zoom(driver):
    driver.execute_script("document.body.style.zoom='90%'")



# Adicione esta função ao final do seu arquivo utils/actions.py

def preencher_campos_completos(driver, wait, doc):
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.support import expected_conditions as EC
    import time

    def safe_input(description, selector, value):
        safe_action(doc, description, lambda: driver.find_element(By.CSS_SELECTOR, selector).send_keys(value), driver, wait)

    def safe_select(description, selector, value):
        safe_action(doc, description, lambda: driver.find_element(By.CSS_SELECTOR, selector).send_keys(value), driver, wait)

    def selecionar_lov(css_selector_lov, termo_busca, texto_tr):
        safe_action(doc, f"Abrindo LOV {termo_busca}", lambda: driver.find_element(By.CSS_SELECTOR, css_selector_lov).click(), driver, wait)
        campo_pesquisa = wait.until(EC.visibility_of_element_located((
            By.CSS_SELECTOR,
            "body > div.modalHolder > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div:nth-child(2) > input"
        )))
        campo_pesquisa.send_keys(termo_busca + Keys.ENTER)
        time.sleep(2)
        safe_action(doc, f"Clicando no resultado da LOV {texto_tr}", lambda: driver.find_element(By.XPATH, f"//tr[contains(., '{texto_tr}')]").click(), driver, wait)
        time.sleep(2)

    log(doc, "🔄 Preenchendo campos obrigatórios.")
    safe_input("Preenchendo nome", "#fmod_10010 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_10010.categoriaHolder > div:nth-child(1) > div > div:nth-child(2) > input", "BANDEIRA TESTE")
    safe_input("Preenchendo tarifa", "#fmod_10010 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_10010.categoriaHolder > div:nth-child(1) > div > div:nth-child(3) > input", "3,25")
    safe_input("Preenchendo qtd dias", "#fmod_10010 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_10010.categoriaHolder > div:nth-child(1) > div > div:nth-child(4) > input", "30")
    safe_select("Selecionando tipo cartão", "#fmod_10010 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_10010.categoriaHolder > div:nth-child(1) > div > div:nth-child(5) > select", "Crédito")
    safe_select("Selecionando tipo cobrança", "#fmod_10010 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_10010.categoriaHolder > div:nth-child(1) > div > div:nth-child(7) > select", "Boleto")
    selecionar_lov("#fmod_10010 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_10010.categoriaHolder > div:nth-child(1) > div > div:nth-child(8) > div > div > a", "745", "PLANO DE CONTAS DÉBITO SELENIUM")

    log(doc, "🔄 Preenchendo campos não obrigatórios.")
    selecionar_lov("#fmod_10010 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_10010.categoriaHolder > div:nth-child(2) > div > div:nth-child(2) > div > div > a", "745", "PLANO DE CONTAS DÉBITO SELENIUM")
    selecionar_lov("#fmod_10010 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_10010.categoriaHolder > div:nth-child(2) > div > div:nth-child(4) > div > div > a", "200116", "DESPESA COM TARIFAS DE CARTÃO")
    selecionar_lov("#fmod_10010 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_10010.categoriaHolder > div:nth-child(2) > div > div:nth-child(3) > div > div > a", "80.79.4703", "TESTE CENTRO DE CUSTO SELENIUM AUTOMATIZADO")

    safe_action(doc, "Clicando na aba Parametrização", lambda: driver.find_element(By.LINK_TEXT, "Parametrização").click(), driver, wait)
    safe_input("Preenchendo campo De", "#fmod_10010 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_10094.categoriaHolder > div > div > div:nth-child(3) > input", "1")
    safe_input("Preenchendo campo Até", "#fmod_10010 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_10094.categoriaHolder > div > div > div:nth-child(4) > input", "31")
    safe_input("Preenchendo campo Tarifa", "#fmod_10010 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_10094.categoriaHolder > div > div > div:nth-child(5) > input", "2,5")
    safe_action(doc, "Clicando em Adicionar", lambda: driver.find_element(By.CSS_SELECTOR,
        "#fmod_10010 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div.cat_10094.categoriaHolder > div > div > div.btnListHolder > a.btAddGroup").click(), driver, wait)

    registrar_screenshot_unico("preenchimento_completo", driver, doc)


# Sim. No `utils/actions.py`, a função `preencher_campos_completos` já está assim:

def selecionar_lov(css_selector_lov, termo_busca, texto_tr, driver, wait, doc, descricao):
    def acao():
        log(doc, f"🔍 {descricao}")

        # Clica para abrir o LOV
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector_lov))).click()

        # Espera o campo de busca aparecer
        campo_pesquisa = wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR,
            "body > div.modalHolder > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div:nth-child(2) > input"
        )))

        # Aguarda o campo estar clicável
        wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            "body > div.modalHolder > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div:nth-child(2) > input"
        )))

        # Aguarda um pequeno intervalo por precaução
        time.sleep(2)
        campo_pesquisa.clear()
        campo_pesquisa.send_keys(termo_busca)

        # Aguarda resultados carregarem
        time.sleep(3)

        # Clica na linha do resultado
        wait.until(EC.element_to_be_clickable((By.XPATH, f"//tr[contains(., '{texto_tr}')]"))).click()
        time.sleep(2)

    safe_action(doc, descricao, acao, driver, wait)

# Ele usa:
# - `wait.until(EC.visibility_of_element_located(...))` para aguardar o campo de busca
# - `safe_action(...)` para garantir que o clique ocorra com espera
# - `time.sleep(2)` para evitar que selecione antes do carregamento

# Se quiser, podemos refinar ainda mais usando:
# wait.until(EC.element_to_be_clickable(...))
# ou aumentar o tempo de espera.
