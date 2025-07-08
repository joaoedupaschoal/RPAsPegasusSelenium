from selenium.common.exceptions import TimeoutException, NoSuchElementException

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from docx import Document
from docx.shared import Inches
from datetime import datetime
from faker import Faker
from faker.providers import BaseProvider
import subprocess
import random
import time
import os

# Relatório

doc = Document()
doc.add_heading('RELATÓRIO DO TESTE', 0)
doc.add_paragraph("Cadastro de Velórios.")
doc.add_paragraph(f"🗕️ Data do teste: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
doc.add_paragraph("Nesse teste, o robô preencherá todos os dados e clicará em Cancelar.")

SCREENSHOT_DIR = "screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

# Funções utilitárias
def log(msg):
    print(msg)
    doc.add_paragraph(msg)

def take_screenshot(driver, filename):
    path = os.path.join(SCREENSHOT_DIR, f"{filename}_{datetime.now().strftime('%H%M%S')}.png")
    driver.save_screenshot(path)
    log(f"🖼️ Screenshot saved: {path}")
    doc.add_picture(path, width=Inches(5.5))
    return path

# Dados simulados
faker = Faker('pt_BR')
class BrasilProvider(BaseProvider):
    def rg(self):
        return ''.join([str(random.randint(0, 9)) for _ in range(8)]) + '-' + str(random.randint(0, 9))
faker.add_provider(BrasilProvider)

def generate_velorio_data():
    return {
        "name": "TESTE VELÓRIO SELENIUM AUTOMATIZADO",
        "cidade_uf": "SÃO JOSÉ DO RIO PRETO - SP",
        "cemetery_name": f"Cemitério {faker.last_name()} {faker.random.choice(['Eterno', 'da Paz', 'Memorial', 'Descanso'])}",
        "qtd_parcelas_em_atraso": int(faker.random.choice(['1', '2', '3', '4', '5'])),
        "dias_para_exumar": int(faker.random.choice(['365', '730', '1095', '1460', '1825'])),
        "ruas": random.randint(1, 10),
        "jazigos_por_rua": random.randint(1, 20),
        "altura_cm": random.randint(100, 200),
        "largura_cm": random.randint(100, 200),
        "comprimento_cm": random.randint(100, 200),
        "valor_taxa_adesao": round(random.uniform(2000, 10000), 2)
    }

# Ações e interação
URL = "http://localhost:8080/gs/index.xhtml"
LOGIN_EMAIL = 'joaoeduardo.gold@outlook.com'
LOGIN_PASSWORD = '071999gs'

def ajustar_zoom(driver):
    driver.execute_script("document.body.style.zoom='90%'")

def encontrar_mensagem_alerta(driver):
    seletores = [
        (".alerts.salvo", "sucesso"),
        (".alerts.alerta", "alerta"),
        (".alerts.erro", "erro"),
    ]

    for seletor, tipo in seletores:
        try:
            elemento = driver.find_element(By.CSS_SELECTOR, seletor)
            if elemento.is_displayed():
                try:
                    texto = elemento.find_element(By.TAG_NAME, "p").text.strip()
                except NoSuchElementException:
                    texto = elemento.text.strip()
                log(f"⚠️ Mensagem de {tipo}: {texto}")
                take_screenshot(driver, f"mensagem_{tipo}")
                return elemento, tipo
        except NoSuchElementException:
            continue

    log("❌ Nenhuma mensagem de alerta encontrada.")
    take_screenshot(driver, "mensagem_nao_encontrada")
    return None, None

def safe_action(action_name, action_func, driver, error_msg=None):
    log(f"🔄 {action_name}...")
    try:
        result = action_func()
        log(f"✅ {action_name} realizado com sucesso.")
        take_screenshot(driver, action_name.lower().replace(' ', '_'))
        return True, result
    except (TimeoutException, NoSuchElementException) as e:
        log(error_msg or f"❌ Erro ao tentar {action_name.lower()}: {str(e)}")
        take_screenshot(driver, f"erro_{action_name.lower().replace(' ', '_')}")
        return False, None

def main():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=Options())
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)
    velorio_data = generate_velorio_data()
    error_status = {key: False for key in ["login", "encontrar_menu", "abrir_cadastro", "preencher_nome", "preencher_cidade_uf", "salvar", "fechar_modal"]}

    success, _ = safe_action("Acessar URL", lambda: driver.get(URL), driver)
    error_status["login"] = not success

    if not error_status["login"]:
        def login():
            wait.until(EC.presence_of_element_located((By.ID, "j_id15:email"))).send_keys(LOGIN_EMAIL)
            wait.until(EC.presence_of_element_located((By.ID, "j_id15:senha"))).send_keys(LOGIN_PASSWORD, Keys.ENTER)
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            time.sleep(3)
        success, _ = safe_action("Login", login, driver)
        error_status["login"] = not success

    if not error_status["login"]:
        safe_action("Ajustar Zoom", lambda: ajustar_zoom(driver), driver)
        safe_action("Abrir menu Velórios", lambda: driver.find_element(By.TAG_NAME, "body").send_keys(Keys.F2), driver)

        def buscar_menu():
            campo = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Busque um cadastro']")))
            campo.click()
            campo.send_keys("Velórios", Keys.ENTER)
            time.sleep(3)
        success, _ = safe_action("Buscar menu Velórios", buscar_menu, driver)
        error_status["encontrar_menu"] = not success

    if not error_status["encontrar_menu"]:
        success, _ = safe_action("Clicar em Cadastrar", lambda: wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#fmod_10036 > div.wdTelas > div.telaInicial.clearfix.overflow.overflowY > ul > li:nth-child(1) > a > span"))).click() or time.sleep(2), driver)
        error_status["abrir_cadastro"] = not success

    if not error_status["abrir_cadastro"]:
        success, _ = safe_action("Preencher nome", lambda: wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#fmod_10036 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div > div > div > div:nth-child(2) > input"))).send_keys(velorio_data["name"]), driver)
        error_status["preencher_nome"] = not success

        success, _ = safe_action("Preencher cidade-UF", lambda: wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#fmod_10036 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div > div > div > div:nth-child(3) > input"))).send_keys(velorio_data["cidade_uf"]), driver)
        error_status["preencher_cidade_uf"] = not success

        success, _ = safe_action("Selecionar cidade-UF", lambda: wait.until(EC.visibility_of_element_located((
            By.CSS_SELECTOR, "ul.ui-autocomplete"))) and wait.until(EC.element_to_be_clickable((
            By.XPATH, "//li[text()='São José do Rio Preto - SP']"))).click(), driver)

        success, _ = safe_action("Clicar em Cancelar", lambda: wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                "#fmod_10036 > div.wdTelas > div.telaCadastro.clearfix > div.btnHolder > a.btModel.btGray.btcancel"))).click(), driver)
        error_status["cancelar"] = not success

        success, _ = safe_action("Confirmar Cancelamento", lambda: wait.until(
            EC.element_to_be_clickable((By.ID, "BtYes"))).click(), driver)
        error_status["confirmar_cancelamento"] = not success

    

        success, _ = safe_action("Fechar modal", lambda: wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#fmod_10036 > div.wdTop.ui-draggable-handle > div.wdClose > a"))).click() or time.sleep(2), driver)
        error_status["fechar_modal"] = not success

    log("\n=== RELATÓRIO FINAL ===")
    if any(error_status.values()):
        falhas = [k for k, v in error_status.items() if v]
        log(f"❌ Teste concluído com falhas nas etapas: {', '.join(falhas)}")
    else:
        log("✅ Teste concluído com sucesso! Todos os passos foram executados sem erros.")

    nome_doc = f"relatorio_capelas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"
    doc.save(nome_doc)
    log(f"📄 Relatório salvo como: {nome_doc}")

    try:
        subprocess.run(["start", "winword", nome_doc], shell=True)
    except Exception as e:
        log(f"Erro ao abrir Word: {e}")

    input("Pressione '.' e ENTER para encerrar...")
    driver.quit()

if __name__ == "__main__":
    main()
