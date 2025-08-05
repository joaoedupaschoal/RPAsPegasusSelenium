# Corrigido: cadastroregistrodeobito1cenario.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from webdriver_manager.chrome import ChromeDriverManager
from docx import Document
from docx.shared import Inches
from faker import Faker
from faker.providers import BaseProvider
from validate_docbr import CPF
from datetime import datetime, timedelta
from selenium.webdriver import ActionChains
import subprocess
import os
import time
import random

# ==== PROVIDERS CUSTOMIZADOS ====
class BrasilProvider(BaseProvider):
    def rg(self):
        numeros = [str(random.randint(0, 9)) for _ in range(8)]
        return ''.join(numeros) + '-' + str(random.randint(0, 9))

fake = Faker("pt_BR")
fake.add_provider(BrasilProvider)

def gerar_datas_validas():
    """Gera datas coerentes para nascimento, falecimento e sepultamento dentro de um intervalo válido."""
    hoje = datetime.today().date()
    dez_anos_atras = hoje - timedelta(days=3650)  # Limite máximo de 10 anos atrás
    
    # Gera uma data de falecimento entre 10 anos atrás e hoje
    data_falecimento = fake.date_between(start_date=dez_anos_atras, end_date=hoje)

    # Garante que a pessoa tenha no mínimo 18 anos na data do falecimento
    idade_minima = 18
    idade_maxima = 110
    data_nascimento = data_falecimento - timedelta(days=random.randint(idade_minima * 365, idade_maxima * 365))

    # Sepultamento entre 1 e 10 dias após o falecimento
    data_sepultamento = data_falecimento + timedelta(days=random.randint(1, 10))

    # Registro entre 1 e 10 dias após o sepultamento
    data_registro = data_sepultamento + timedelta(days=random.randint(1, 10))

    data_velorio = fake.date_between(start_date=data_falecimento, end_date=data_sepultamento)

    return (
        data_nascimento.strftime("%d/%m/%Y"),
        data_falecimento.strftime("%d/%m/%Y"),
        data_sepultamento.strftime("%d/%m/%Y"),
        data_velorio.strftime("%d/%m/%Y"),
        data_registro.strftime("%d/%m/%Y")
    )

# Gera os valores corretos
data_nascimento, data_falecimento, data_sepultamento, data_velorio, data_registro = gerar_datas_validas()
hora_falecimento = fake.time(pattern="%H:%M")
hora_sepultamento = fake.time(pattern="%H:%M")
localizacao = fake.city()

# ==== CONFIGURAÇÕES ====
URL = "http://localhost:8080/gs/index.xhtml"
LOGIN_EMAIL = "joaoeduardo.gold@outlook.com"
LOGIN_PASSWORD = "071999gs"

# ==== INICIALIZAÇÃO DE VARIÁVEIS GLOBAIS ====
doc = Document()
doc.add_heading("RELATÓRIO DO TESTE", 0)
doc.add_paragraph("Cadastro de Registro de Óbito – Cenário 1: Preenchimento completo e salvamento.")
doc.add_paragraph(f"Data do teste: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

screenshot_registradas = set()
driver = None
wait = None

# ==== FUNÇÕES DE UTILITÁRIO MELHORADAS ====
def log(doc, msg):
    print(msg)
    doc.add_paragraph(msg)

def take_screenshot(driver, doc, nome):
    if driver is None:
        return
    if nome not in screenshot_registradas:
        path = f"screenshots/{nome}.png"
        os.makedirs("screenshots", exist_ok=True)
        try:
            driver.save_screenshot(path)
            doc.add_paragraph(f"Screenshot: {nome}")
            doc.add_picture(path, width=Inches(5.5))
            screenshot_registradas.add(nome)
        except Exception as e:
            log(doc, f"⚠️ Erro ao tirar screenshot {nome}: {e}")

def safe_action(doc, descricao, func, max_retries=3):
    """Executa uma ação com retry e tratamento robusto de erros"""
    global driver
    
    for attempt in range(max_retries):
        try:
            if attempt == 0:
                log(doc, f"🔄 {descricao}...")
            else:
                log(doc, f"🔄 {descricao}... (Tentativa {attempt + 1})")
            
            func()
            log(doc, f"✅ {descricao} realizada com sucesso.")
            take_screenshot(driver, doc, descricao.lower().replace(" ", "_"))
            return True
            
        except (TimeoutException, NoSuchElementException, StaleElementReferenceException) as e:
            if attempt < max_retries - 1:
                log(doc, f"⚠️ Tentativa {attempt + 1} falhou para {descricao}, tentando novamente...")
                time.sleep(2)
                continue
            else:
                log(doc, f"❌ Erro ao {descricao.lower()} após {max_retries} tentativas: {e}")
                take_screenshot(driver, doc, f"erro_{descricao.lower().replace(' ', '_')}")
                return False
        except Exception as e:
            log(doc, f"❌ Erro inesperado ao {descricao.lower()}: {e}")
            take_screenshot(driver, doc, f"erro_{descricao.lower().replace(' ', '_')}")
            return False

def finalizar_relatorio():
    global driver, doc
    
    nome_arquivo = f"relatorio_obito_cenario_1_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"
    try:
        doc.save(nome_arquivo)
        log(doc, f"📄 Relatório salvo como: {nome_arquivo}")
        try:
            subprocess.run(["start", "winword", nome_arquivo], shell=True)
        except:
            pass
    except Exception as e:
        print(f"Erro ao salvar relatório: {e}")
    
    if driver:
        try:
            driver.quit()
        except:
            pass

def encontrar_mensagem_alerta():
    global driver, doc
    
    if driver is None:
        return None
        
    seletores = [
        (".alerts.salvo", "✅ Sucesso"),
        (".alerts.alerta", "⚠️ Alerta"),
        (".alerts.erro", "❌ Erro"),
    ]

    for seletor, tipo in seletores:
        try:
            elemento = driver.find_element(By.CSS_SELECTOR, seletor)
            if elemento.is_displayed():
                log(doc, f"📢 {tipo}: {elemento.text}")
                return elemento
        except:
            continue

    log(doc, "ℹ️ Nenhuma mensagem de alerta encontrada.")
    return None

def ajustar_zoom():
    global driver, doc
    
    if driver is None:
        return
        
    try:
        driver.execute_script("document.body.style.zoom='90%'")
        log(doc, "🔍 Zoom ajustado para 90%.")
    except Exception as e:
        log(doc, f"⚠️ Erro ao ajustar zoom: {e}")

def safe_scroll_and_interact(selector, action_type="click", value=None, timeout=10, by_xpath=False):
    """Função robusta para rolar até elemento e interagir com ele"""
    global driver, doc
    
    if driver is None:
        return None
        
    try:
        # Escolhe o tipo de seletor
        by_type = By.XPATH if by_xpath else By.CSS_SELECTOR
        
        # Aguarda o elemento estar presente
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by_type, selector))
        )
        
        # Rola até o elemento
        driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", element)
        time.sleep(0.5)
        
        # Aguarda o elemento estar clicável se necessário
        if action_type in ["click", "send_keys"]:
            element = WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable((by_type, selector))
            )
        
        # Executa a ação
        if action_type == "click":
            element.click()
        elif action_type == "send_keys" and value:
            element.clear()
            element.send_keys(value)
        elif action_type == "select" and value:
            Select(element).select_by_visible_text(value)
            
        return element
        
    except Exception as e:
        log(doc, f"❌ Erro ao interagir com elemento {selector}: {e}")
        return None

def preencher_campo_robusto(selector, valor, clear_first=True):
    """Preenche campo de forma robusta"""
    def acao():
        element = safe_scroll_and_interact(selector, "send_keys", valor)
        if element is None:
            raise Exception(f"Não foi possível encontrar o elemento: {selector}")
    return acao

def selecionar_opcao_robusta(selector, texto):
    """Seleciona opção de forma robusta"""
    def acao():
        element = safe_scroll_and_interact(selector, "select", texto)
        if element is None:
            raise Exception(f"Não foi possível encontrar o select: {selector}")
    return acao

def clicar_elemento_robusto(selector):
    """Clica em elemento de forma robusta"""
    def acao():
        element = safe_scroll_and_interact(selector, "click")
        if element is None:
            raise Exception(f"Não foi possível clicar no elemento: {selector}")
    return acao

def preencher_campo_com_retry(driver, wait, seletor, valor, max_tentativas=3):
    """Tenta preencher o campo com diferentes métodos até conseguir"""
    global doc
    
    if driver is None or wait is None:
        return False
    
    for tentativa in range(max_tentativas):
        try:
            # Aguarda o elemento
            campo = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, seletor)))
            
            # Scroll até o elemento se necessário
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", campo)
            time.sleep(0.5)
            
            # Método 1: Tradicional
            if tentativa == 0:
                campo.click()
                campo.clear()
                campo.send_keys(valor)
                campo.send_keys(Keys.TAB)
            
            # Método 2: ActionChains
            elif tentativa == 1:
                ActionChains(driver).move_to_element(campo).click().perform()
                time.sleep(0.2)
                ActionChains(driver).key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
                ActionChains(driver).send_keys(valor).perform()
                ActionChains(driver).send_keys(Keys.TAB).perform()
            
            # Método 3: JavaScript
            else:
                driver.execute_script("""
                    var element = arguments[0];
                    var valor = arguments[1];
                    element.focus();
                    element.value = '';
                    element.value = valor;
                    element.dispatchEvent(new Event('input', { bubbles: true }));
                    element.dispatchEvent(new Event('change', { bubbles: true }));
                    element.blur();
                """, campo, valor)
            
            time.sleep(0.5)
            
            # Verifica se o valor foi preenchido
            valor_atual = campo.get_attribute('value')
            if valor_atual == valor:
                return True
                
        except Exception as e:
            log(doc, f"⚠️ Tentativa {tentativa + 1} falhou: {e}")
            time.sleep(1)
    
    return False

def abrir_modal_e_selecionar_robusto(btn_selector, pesquisa_selector, termo_pesquisa, btn_pesquisar_selector, resultado_xpath):
    """Versão robusta da função de modal"""
    global driver, wait, doc
    
    def acao():
        if driver is None or wait is None:
            raise Exception("Driver ou wait não inicializados")
            
        # Abre o modal
        safe_scroll_and_interact(btn_selector, "click")
        time.sleep(1)

        # Aguarda e preenche campo pesquisa
        campo_pesquisa = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, pesquisa_selector))
        )
        campo_pesquisa.clear()
        campo_pesquisa.send_keys(termo_pesquisa)
        time.sleep(0.5)

        # Clica pesquisar
        pesquisar = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, btn_pesquisar_selector))
        )
        pesquisar.click()
        time.sleep(2)
        
        # Aguarda resultado e clica
        resultado = wait.until(
            EC.element_to_be_clickable((By.XPATH, resultado_xpath))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", resultado)
        time.sleep(0.5)
        resultado.click()
        time.sleep(1)

    return acao

def inicializar_driver():
    """Inicializa o driver do Chrome"""
    global driver, wait
    
    try:
        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        wait = WebDriverWait(driver, 20)
        
        return True
    except Exception as e:
        log(doc, f"❌ Erro ao inicializar driver: {e}")
        return False

# ==== EXECUÇÃO DO TESTE ====
def executar_teste():
    global driver, wait, doc
    
    try:
        # Inicializa o driver
        if not inicializar_driver():
            return False

        safe_action(doc, "Acessando sistema", lambda: driver.get(URL))

        safe_action(doc, "Realizando login", lambda: (
            wait.until(EC.presence_of_element_located((By.ID, "j_id15:email"))).send_keys(LOGIN_EMAIL),
            wait.until(EC.presence_of_element_located((By.ID, "j_id15:senha"))).send_keys(LOGIN_PASSWORD, Keys.ENTER),
            time.sleep(5)
        ))

        safe_action(doc, "Ajustando zoom e abrindo menu", lambda: (
            ajustar_zoom(),
            driver.find_element(By.TAG_NAME, "body").send_keys(Keys.F3)
        ))

        safe_action(doc, "Acessando Registro de Óbito", lambda: (
            wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[15]/ul/li[14]/img'))).click()
        ))

        safe_action(doc, "Clicando em Cadastrar", lambda: (
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#fmod_23 > div.wdTelas > div.telaInicial.clearfix.overflow.overflowY > ul > li:nth-child(1) > a > span'))).click()
        ))

        safe_action(doc, "Selecionando Cartório", abrir_modal_e_selecionar_robusto(
            '#fmod_23 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div > div:nth-child(1) > div > div:nth-child(2) > div > a',
            'body > div.modalHolder > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div:nth-child(2) > input.nomePesquisa',
            'CARTÓRIO TESTE SELENIUM AUTOMATIZADO',
            'body > div.modalHolder > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div:nth-child(3) > a',
            "//a[contains(@class, 'linkAlterar')]"
        ))

        safe_action(doc, "Preenchendo informações do registro", lambda: (
            safe_scroll_and_interact("#fmod_23 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div > div:nth-child(1) > div > div:nth-child(3) > input", "send_keys", str(fake.random_int(min=1, max=99))),
            safe_scroll_and_interact("#fmod_23 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div > div:nth-child(1) > div > div:nth-child(4) > input", "send_keys", str(fake.random_int(min=1, max=99))),
            safe_scroll_and_interact("#fmod_23 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div > div:nth-child(1) > div > div:nth-child(5) > input", "send_keys", str(fake.random_int(min=1, max=99)))
        ))

        safe_action(doc, "Selecionando pessoa falecida", abrir_modal_e_selecionar_robusto(
            '#fmod_23 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div > div:nth-child(1) > div > div:nth-child(6) > div > a',
            '#txtPesquisa',
            'FALECIDO TESTE SELENIUM AUTOMATIZADO',
            'body > div.modalHolder > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div:nth-child(2) > a',
            "//td[contains(text(), 'FALECIDO TESTE SELENIUM AUTOMATIZADO')]"
        ))

        safe_action(doc, "Selecionando Situação do Falecido", selecionar_opcao_robusta(
            "#fmod_23 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div > div:nth-child(1) > div > div:nth-child(7) > select",
            "Nenhuma das opções"
        ))

        safe_action(doc, "Selecionando sexo da pessoa falecida", selecionar_opcao_robusta(
            "#fmod_23 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div > div:nth-child(1) > div > div:nth-child(8) > select",
            "Masculino"
        ))

# Data do falecimento
        safe_action(doc, "Preenchendo Data do falecimento", lambda: preencher_campo_com_retry(
            driver, wait, "input[ref='25']", data_falecimento)).send_keys(Keys.TAB)

        safe_action(doc, "Preenchendo hora do falecimento", lambda: preencher_campo_com_retry(
            safe_scroll_and_interact("#fmod_23 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div > div:nth-child(1) > div > div:nth-child(10) > input", "send_keys", hora_falecimento)
        ))

        safe_action(doc, "Preenchendo Local de Falecimento", preencher_campo_robusto(
            '#fmod_23 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div > div:nth-child(1) > div > div:nth-child(11) > input',
            'LOCAL DE FALECIMENTO TESTE SELENIUM AUTOMATIZADO'
        ))

        safe_action(doc, "Selecionando Cor da pessoa falecida", abrir_modal_e_selecionar_robusto(
            '#fmod_23 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div > div:nth-child(1) > div > div:nth-child(15) > div > a',
            'body > div.modalHolder > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div:nth-child(2) > input.nomePesquisa',
            'BRANCO',
            'body > div.modalHolder > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div:nth-child(3) > a',
            "//td[contains(text(), 'BRANCO')]"
        ))

        safe_action(doc, "Preenchendo Nome do Cônjuge", preencher_campo_robusto(
            '#fmod_23 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div > div:nth-child(1) > div > div:nth-child(18) > input',
            fake.name()
        ))

        safe_action(doc, "Preenchendo Nome do Filho", preencher_campo_robusto(
            '#fmod_23 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div > div:nth-child(1) > div > div:nth-child(26) > input',
            fake.name()
        ))

        safe_action(doc, "Selecionando a opção para o Falecido possuir Bens", selecionar_opcao_robusta(
            "#fmod_23 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div > div:nth-child(1) > div > div:nth-child(27) > select",
            "Sim"
        ))

        safe_action(doc, "Selecionando a opção para o Falecido possuir Testamento", selecionar_opcao_robusta(
            "#fmod_23 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div > div:nth-child(1) > div > div:nth-child(28) > select",
            "Sim"
        ))

        safe_action(doc, "Preenchendo Nome do Médico Responsável", preencher_campo_robusto(
            '#fmod_23 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div > div:nth-child(1) > div > div:nth-child(31) > input',
            fake.name()
        ))

        safe_action(doc, "Preenchendo CRM", preencher_campo_robusto(
            '#fmod_23 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div > div:nth-child(1) > div > div:nth-child(32) > input',
            str(fake.random_int(min=100000, max=999999))
        ))

        safe_action(doc, "Preenchendo Nome do Médico Responsável 2", preencher_campo_robusto(
            '#fmod_23 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div > div:nth-child(1) > div > div:nth-child(33) > input',
            fake.name()
        ))

        safe_action(doc, "Preenchendo CRM 2", preencher_campo_robusto(
            '#fmod_23 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div > div:nth-child(1) > div > div:nth-child(34) > input',
            str(fake.random_int(min=100000, max=999999))
        ))

        safe_action(doc, "Preenchendo Causa Mortis", preencher_campo_robusto(
            '#fmod_23 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div > div:nth-child(1) > div > div:nth-child(35) > input',
            'CAUSA MORTIS TESTE SELENIUM AUTOMATIZADO'
        ))

        safe_action(doc, "Preenchendo Causa Mortis 2", preencher_campo_robusto(
            '#fmod_23 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div > div:nth-child(1) > div > div:nth-child(36) > input',
            'CAUSA MORTIS 2 TESTE SELENIUM AUTOMATIZADO'
        ))

        safe_action(doc, "Preenchendo Causa Mortis 3", preencher_campo_robusto(
            '#fmod_23 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div > div:nth-child(1) > div > div:nth-child(37) > input',
            'CAUSA MORTIS 3 TESTE SELENIUM AUTOMATIZADO'
        ))

        safe_action(doc, "Preenchendo Causa Mortis 4", preencher_campo_robusto(
            '#fmod_23 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div > div:nth-child(1) > div > div:nth-child(38) > input',
            'CAUSA MORTIS 4 TESTE SELENIUM AUTOMATIZADO'
        ))

        safe_action(doc, "Preenchendo Local Sepultamento", preencher_campo_robusto(
            '#fmod_23 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div > div:nth-child(1) > div > div:nth-child(39) > input',
            'LOCAL SEPULTAMENTO TESTE SELENIUM AUTOMATIZADO'
        ))

        safe_action(doc, "Preenchendo Data da Registro", lambda: preencher_campo_com_retry(
    driver, wait, "input[ref='10118']", data_registro,)).send_keys(Keys.TAB)
        
        safe_action(doc, "Selecionando Local de Velório", abrir_modal_e_selecionar_robusto(
            '#fmod_23 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div > div:nth-child(1) > div > div:nth-child(41) > div > a',
            'body > div.modalHolder > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div:nth-child(2) > input.nomePesquisa',
            'TESTE VELÓRIO SELENIUM AUTOMATIZADO',
            'body > div.modalHolder > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div:nth-child(3) > a',
            "//td[contains(text(), 'TESTE VELÓRIO SELENIUM AUTOMATIZADO')]"
        ))

        safe_action(doc, "Preenchendo Data da Sepultamento", lambda: preencher_campo_com_retry(
    driver, wait, "input[ref='96']", data_sepultamento, )).send_keys(Keys.TAB)
        
        safe_action(doc, "Preenchendo Hora do Sepultamento", lambda: preencher_campo_com_retry(
            safe_scroll_and_interact("#fmod_23 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div > div:nth-child(1) > div > div:nth-child(43) > input", "send_keys", hora_sepultamento)
        ))

        safe_action(doc, "Preenchendo Declaração de Óbito", preencher_campo_robusto(
            '#fmod_23 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div > div:nth-child(1) > div > div:nth-child(45) > input',
            str(fake.random_int(min=1000, max=9999))
        ))

        safe_action(doc, "Selecionando a opção para o Tipo de Óbito ser Particular", selecionar_opcao_robusta(
            "#fmod_23 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div > div:nth-child(1) > div > div:nth-child(46) > select",
            "Particular"
        ))

        safe_action(doc, "Preenchendo Ordem Serviço", preencher_campo_robusto(
            '#fmod_23 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div > div:nth-child(1) > div > div:nth-child(48) > input',
            str(fake.random_int(min=1000, max=9999))
        ))

        safe_action(doc, "Selecionando Grau de Parentesco", selecionar_opcao_robusta(
            "#fmod_23 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div > div:nth-child(1) > div > div:nth-child(49) > select",
            "Agregado"
        ))

        safe_action(doc, "Selecionando Religião", abrir_modal_e_selecionar_robusto(
            '#fmod_23 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div > div:nth-child(1) > div > div:nth-child(50) > div > a',
            'body > div.modalHolder > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div:nth-child(2) > input.nomePesquisa',
            'TESTE RELIGIÃO SELENIUM AUTOMATIZADO',
            'body > div.modalHolder > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div:nth-child(3) > a',
            "//td[contains(text(), 'TESTE RELIGIÃO SELENIUM AUTOMATIZADO')]"
        ))

        safe_action(doc, "Preenchendo Matrícula", preencher_campo_robusto(
            '#fmod_23 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div > div:nth-child(1) > div > div:nth-child(52) > input',
            str(fake.random_int(min=1000, max=9999))
        ))

        safe_action(doc, "Selecionando Declarante", abrir_modal_e_selecionar_robusto(
            '#fmod_23 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div > div:nth-child(2) > div > div:nth-child(2) > div > a',
            '#txtPesquisa',
            'TESTE DECLARANTE SELENIUM AUTOMATIZADO',
            'body > div.modalHolder > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div:nth-child(2) > a',
            "//td[contains(text(), 'TESTE DECLARANTE SELENIUM AUTOMATIZADO')]"
        ))

        safe_action(doc, "Selecionando Estado Civil", selecionar_opcao_robusta(
            "#fmod_23 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div > div:nth-child(4) > div > div:nth-child(2) > select",
            "Casado(a)"
        ))

        safe_action(doc, "Preenchendo Cidade Sepultamento", preencher_campo_robusto(
            '#fmod_23 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div > div:nth-child(4) > div > div:nth-child(4) > input',
            'TESTE CIDADE SEPULTAMENTO SELENIUM AUTOMATIZADO'
        ))

        safe_action(doc, "Preenchendo Data da Velório", lambda: preencher_campo_com_retry(
    driver, wait, "input[ref='100159']", data_velorio,)).send_keys(Keys.TAB)
        
        safe_action(doc, "Preenchendo Observações do Óbito", preencher_campo_robusto(
            '#fmod_23 > div.wdTelas > div.telaCadastro.clearfix > div.catWrapper > div > div > div:nth-child(4) > div > div:nth-child(7) > textarea',
            'TESTE OBSERVAÇÕES DO ÓBITO SELENIUM AUTOMATIZADO'
        ))

        safe_action(doc, "Salvando cadastro", clicar_elemento_robusto(
            '#fmod_23 > div.wdTelas > div.telaCadastro.clearfix > div.btnHolder > a.btModel.btGray.btsave'
        ))

        # Aguarda um pouco após salvar
        time.sleep(3)

        safe_action(doc, "Fechando modal após o salvamento", clicar_elemento_robusto(
            '#fmod_23 > div.wdTop.ui-draggable-handle > div.wdClose > a'
        ))

        # Procura por mensagens de alerta
        encontrar_mensagem_alerta()

        return True

    except Exception as e:
        log(doc, f"❌ ERRO FATAL: {e}")
        take_screenshot(driver, doc, "erro_fatal")
        return False

    finally:
        log(doc, "✅ Teste concluído.")

# ==== FUNÇÃO PRINCIPAL ====
def main():
    """Função principal que executa o teste"""
    global doc
    
    try:
        log(doc, "🚀 Iniciando teste de cadastro de registro de óbito...")
        
        sucesso = executar_teste()
        
        if sucesso:
            log(doc, "✅ Teste executado com sucesso!")
        else:
            log(doc, "❌ Teste finalizado com erros.")
            
    except Exception as e:
        log(doc, f"❌ Erro na execução principal: {e}")
        
    finally:
        finalizar_relatorio()

# ==== EXECUÇÃO ====
if __name__ == "__main__":
    main()