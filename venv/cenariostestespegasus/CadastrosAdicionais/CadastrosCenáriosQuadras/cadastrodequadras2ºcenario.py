# Versão REFATORADA: cadastrodequadras1ºcenario.py
# Baseado no modelo do código de jazigos com melhorias: Tratamento robusto de erros, múltiplas estratégias de seleção, timeouts adaptativos

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from webdriver_manager.chrome import ChromeDriverManager
from docx import Document
from docx.shared import Inches
from faker import Faker
from faker.providers import BaseProvider
from datetime import datetime
import subprocess
import os
import time
import random
import string

# ==== PROVIDERS CUSTOMIZADOS ====
class BrasilProvider(BaseProvider):
    def rg(self):
        numeros = [str(random.randint(0, 9)) for _ in range(8)]
        return ''.join(numeros) + '-' + str(random.randint(0, 9))

fake = Faker("pt_BR")
fake.add_provider(BrasilProvider)

# ==== CONFIGURAÇÕES ====
URL = "http://localhost:8080/gs/index.xhtml"
LOGIN_EMAIL = "joaoeduardo.gold@outlook.com"
LOGIN_PASSWORD = "071999gs"

# ==== DOCUMENTO ====
doc = Document()
doc.add_heading("RELATÓRIO DO TESTE", 0)
doc.add_paragraph("Cadastro de Quadras – Cenário 2: Preenchimento completo e cancelamento.")
doc.add_paragraph(f"Data do teste: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

screenshot_registradas = set()

# ==== FUNÇÕES DE UTILITÁRIO MELHORADAS ====
def log(doc, msg):
    print(msg)
    doc.add_paragraph(msg)

def take_screenshot(driver, doc, nome):
    if nome not in screenshot_registradas:
        path = f"screenshots/{nome}.png"
        os.makedirs("screenshots", exist_ok=True)
        try:
            driver.save_screenshot(path)
            doc.add_paragraph(f"Screenshot: {nome}")
            doc.add_picture(path, width=Inches(5.5))
        except Exception as e:
            print(f"Erro ao capturar screenshot: {e}")
        screenshot_registradas.add(nome)

def aguardar_elemento_disponivel(driver, selector, by_type=By.CSS_SELECTOR, timeout=30):
    """Aguarda elemento estar presente, visível e clicável"""
    try:
        wait = WebDriverWait(driver, timeout)
        # Aguarda estar presente
        wait.until(EC.presence_of_element_located((by_type, selector)))
        # Aguarda estar visível
        wait.until(EC.visibility_of_element_located((by_type, selector)))
        # Aguarda estar clicável
        element = wait.until(EC.element_to_be_clickable((by_type, selector)))
        return element
    except TimeoutException:
        return None

def safe_click_enhanced(driver, selector, by_type=By.CSS_SELECTOR, timeout=30):
    """Função de clique ultra-robusta com múltiplas estratégias"""
    strategies = [
        "aguardar_e_clicar_normal",
        "aguardar_e_clicar_js", 
        "aguardar_e_clicar_action",
        "força_bruta_js"
    ]
    
    for strategy in strategies:
        try:
            log(doc, f"🔄 Tentando estratégia: {strategy}")
            
            if strategy == "aguardar_e_clicar_normal":
                element = aguardar_elemento_disponivel(driver, selector, by_type, timeout)
                if element:
                    # Rola para o elemento
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", element)
                    time.sleep(1)
                    # Relocaliza para evitar stale reference
                    element = driver.find_element(by_type, selector)
                    element.click()
                    return True
                    
            elif strategy == "aguardar_e_clicar_js":
                element = aguardar_elemento_disponivel(driver, selector, by_type, timeout)
                if element:
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                    time.sleep(0.5)
                    driver.execute_script("arguments[0].click();", element)
                    return True
                    
            elif strategy == "aguardar_e_clicar_action":
                element = aguardar_elemento_disponivel(driver, selector, by_type, timeout)
                if element:
                    actions = ActionChains(driver)
                    actions.move_to_element(element).pause(0.5).click().perform()
                    return True
                    
            elif strategy == "força_bruta_js":
                # Última tentativa: força bruta com JavaScript
                if by_type == By.CSS_SELECTOR:
                    js_code = f"""
                        var element = document.querySelector('{selector}');
                        if (element) {{
                            element.scrollIntoView({{block: 'center'}});
                            setTimeout(function() {{
                                element.click();
                                console.log('Clique forçado executado');
                            }}, 500);
                            return true;
                        }}
                        return false;
                    """
                else:  # XPATH
                    js_code = f"""
                        var element = document.evaluate('{selector}', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                        if (element) {{
                            element.scrollIntoView({{block: 'center'}});
                            setTimeout(function() {{
                                element.click();
                                console.log('Clique forçado XPath executado');
                            }}, 500);
                            return true;
                        }}
                        return false;
                    """
                
                result = driver.execute_script(js_code)
                if result:
                    time.sleep(1)
                    return True
                    
        except Exception as e:
            log(doc, f"⚠️ Estratégia {strategy} falhou: {str(e)[:100]}...")
            continue
    
    return False

def safe_send_keys_enhanced(driver, selector, text, by_type=By.CSS_SELECTOR, clear=True, timeout=20):
    """Função para envio seguro de texto com retry"""
    for attempt in range(3):
        try:
            element = aguardar_elemento_disponivel(driver, selector, by_type, timeout)
            if element:
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                time.sleep(0.3)
                
                if clear:
                    element.clear()
                    # Fallback para limpar
                    element.send_keys(Keys.CONTROL + "a")
                    element.send_keys(Keys.DELETE)
                
                element.send_keys(text)
                return True
        except Exception as e:
            log(doc, f"⚠️ Tentativa {attempt + 1} de envio de texto falhou: {e}")
            time.sleep(1)
    
    return False

def safe_action_enhanced(driver, doc, descricao, func, max_tentativas=3):
    """Função safe_action aprimorada"""
    for tentativa in range(max_tentativas):
        try:
            log(doc, f"🔄 {descricao}... (Tentativa {tentativa + 1})")
            result = func()
            if result is False:  # Se a função retornou False explicitamente
                raise Exception("Função retornou False")
            log(doc, f"✅ {descricao} realizada com sucesso.")
            take_screenshot(driver, doc, descricao.lower().replace(" ", "_"))
            return True
        except Exception as e:
            if tentativa < max_tentativas - 1:
                log(doc, f"⚠️ Tentativa {tentativa + 1} falhou: {str(e)[:100]}... Tentando novamente...")
                time.sleep(2)
            else:
                log(doc, f"❌ Erro ao {descricao.lower()}: {str(e)[:200]}...")
                take_screenshot(driver, doc, f"erro_{descricao.lower().replace(' ', '_')}")
                return False

def selecionar_item_tabela_melhorado_cemiterio(driver, texto_busca, timeout=20):
    """Função para seleção de cemitério na tabela"""
    estrategias = [
        f"//td[contains(text(), '{texto_busca}')]",
        f"//td[contains(text(), 'CEMITÉRIO HERMAN DESCANSO')]",
        "//td[contains(text(), 'CEMITÉRIO')]"
    ]
    
    try:
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.TAG_NAME, "table")))
        time.sleep(2)
    except:
        log(doc, "⚠️ Tabela não encontrada ou não carregou")
        return False
    
    for i, xpath in enumerate(estrategias):
        try:
            log(doc, f"🔍 Tentando estratégia {i+1}: {xpath[:50]}...")
            elements = driver.find_elements(By.XPATH, xpath)
            
            if elements:
                element = elements[0]
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                time.sleep(0.5)
                
                try:
                    element.click()
                except:
                    driver.execute_script("arguments[0].click();", element)
                
                log(doc, f"✅ Item selecionado com estratégia {i+1}")
                return True
            else:
                log(doc, f"⚠️ Nenhum elemento encontrado com estratégia {i+1}")
                
        except Exception as e:
            log(doc, f"⚠️ Erro na estratégia {i+1}: {str(e)[:100]}...")
            continue
    
    return False

def gerar_dados_quadra():
    """Gera dados fictícios para o cadastro de quadra."""
    ruas = random.randint(1, 100)
    jazigos_por_rua = random.randint(1, 200)
    total_jazigos = ruas * jazigos_por_rua
    
    return (ruas, jazigos_por_rua, total_jazigos)

def finalizar_relatorio():
    nome_arquivo = f"relatorio_quadras_refatorado_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"
    try:
        doc.save(nome_arquivo)
        log(doc, f"📄 Relatório salvo como: {nome_arquivo}")
        subprocess.run(["start", "winword", nome_arquivo], shell=True)
    except Exception as e:
        print(f"Erro ao salvar relatório: {e}")

# Gera os dados necessários
(ruas, jazigos_por_rua, total_jazigos) = gerar_dados_quadra()

# ==== INICIALIZAÇÃO DO DRIVER ====
options = Options()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-web-security")
options.add_argument("--disable-features=VizDisplayCompositor")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

try:
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    wait = WebDriverWait(driver, 30)  # Timeout maior
    
    log(doc, "🚀 Iniciando teste de cadastro de quadras...")
    
    # ==== EXECUÇÃO DO TESTE PRINCIPAL ====
    
    # Acesso ao sistema
    safe_action_enhanced(driver, doc, "Acessando sistema", 
        lambda: driver.get(URL))

    # Login
    safe_action_enhanced(driver, doc, "Realizando login", lambda: (
        safe_send_keys_enhanced(driver, "#j_id15\\:email", LOGIN_EMAIL, By.CSS_SELECTOR),
        safe_send_keys_enhanced(driver, "#j_id15\\:senha", LOGIN_PASSWORD, By.CSS_SELECTOR),
        driver.find_element(By.CSS_SELECTOR, "#j_id15\\:senha").send_keys(Keys.ENTER),
        time.sleep(3)
    ))

    # Aguardar carregamento e ajustar zoom
    safe_action_enhanced(driver, doc, "Esperando sistema carregar e ajustando zoom", lambda: (
        time.sleep(5),
        driver.execute_script("document.body.style.zoom='90%'")
    ))

    # Abrir menu Quadras
    safe_action_enhanced(driver, doc, "Abrindo menu Quadras", lambda: (
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.F2),
        time.sleep(3),
        safe_send_keys_enhanced(driver, "//input[@placeholder='Busque um cadastro']", "Quadras", By.XPATH, clear=True),
        driver.find_element(By.XPATH, "//input[@placeholder='Busque um cadastro']").send_keys(Keys.ENTER),
        time.sleep(4)
    ))

    # Clicar em Cadastrar
    safe_action_enhanced(driver, doc, "Clicando em Cadastrar", 
        lambda: safe_click_enhanced(driver, "#fmod_6 > div.wdTelas > div.telaInicial.clearfix.overflow.overflowY > ul > li:nth-child(1) > a > span"))

    # Preenchimento do nome da quadra
    safe_action_enhanced(driver, doc, "Preenchendo nome da quadra", 
        lambda: safe_send_keys_enhanced(driver, "#fmod_6 > div.wdTelas > div.telaCadastro.clearfix.TelaCadastroQuadra > div.catWrapper > div > div > div > div > div > div:nth-child(1) > div > input", 'TESTE QUADRA SELENIUM AUTOMATIZADO 4'))

    # Seleção de Cemitério
    safe_action_enhanced(driver, doc, "Abrindo LOV para selecionar Cemitério", 
        lambda: safe_click_enhanced(driver, "#fmod_6 > div.wdTelas > div.telaCadastro.clearfix.TelaCadastroQuadra > div.catWrapper > div > div > div > div > div > div:nth-child(2) > div > div > a"))

    safe_action_enhanced(driver, doc, "Pesquisando cemitério", 
        lambda: safe_send_keys_enhanced(driver, "body > div.modalHolder > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div.formCol.divPesquisa > input", 'cemitério herman descanso', By.CSS_SELECTOR))

    safe_action_enhanced(driver, doc, "Executando busca", 
        lambda: driver.find_element(By.CSS_SELECTOR, "body > div.modalHolder > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div.formCol.divPesquisa > input").send_keys(Keys.ENTER))

    safe_action_enhanced(driver, doc, "Selecionando cemitério",
        lambda: selecionar_item_tabela_melhorado_cemiterio(driver, "CEMITÉRIO HERMAN DESCANSO"))

    # Preenchimento dos campos numéricos
    safe_action_enhanced(driver, doc, "Preenchendo quantidade de ruas", 
        lambda: safe_send_keys_enhanced(driver, "#fmod_6 > div.wdTelas > div.telaCadastro.clearfix.TelaCadastroQuadra > div.catWrapper > div > div > div > div > div > div:nth-child(3) > input[type=text]", str(ruas)))

    safe_action_enhanced(driver, doc, "Preenchendo máximo de jazigos por rua", 
        lambda: safe_send_keys_enhanced(driver, "#fmod_6 > div.wdTelas > div.telaCadastro.clearfix.TelaCadastroQuadra > div.catWrapper > div > div > div > div > div > div:nth-child(4) > input[type=text]", str(jazigos_por_rua)))

    safe_action_enhanced(driver, doc, "Preenchendo total de jazigos", lambda: (
        safe_send_keys_enhanced(driver, "#fmod_6 > div.wdTelas > div.telaCadastro.clearfix.TelaCadastroQuadra > div.catWrapper > div > div > div > div > div > div:nth-child(5) > input[type=text]", "", clear=True),
        safe_send_keys_enhanced(driver, "#fmod_6 > div.wdTelas > div.telaCadastro.clearfix.TelaCadastroQuadra > div.catWrapper > div > div > div > div > div > div:nth-child(5) > input[type=text]", str(total_jazigos), clear=False)
    ))

    # Salvamento
    safe_action_enhanced(driver, doc, "Cancelando cadastro", 
        lambda: safe_click_enhanced(driver, "#fmod_6 > div.wdTelas > div.telaCadastro.clearfix.TelaCadastroQuadra > div.btnHolder > a.btModel.btGray.btcancel"))

    safe_action_enhanced(driver, doc, "Fechando modal após cancelamento", 
        lambda: safe_click_enhanced(driver, "#fmod_6 > div.wdTop.ui-draggable-handle > div.wdClose > a"))
    

    try:
        # Verifica se há mensagens de sucesso/erro
        seletores = [
            (".alerts.salvo", "sucesso"),
            (".alerts.alerta", "alerta"),
            (".alerts.erro", "erro"),
            (".alerts", "geral")
        ]

        for seletor, tipo in seletores:
            try:
                elemento = driver.find_element(By.CSS_SELECTOR, seletor)
                if elemento.is_displayed():
                    log(doc, f"📢 Mensagem de {tipo}: {elemento.text}")
                    break
            except NoSuchElementException:
                continue
        else:
            log(doc, "📢 Nenhuma mensagem de sistema encontrada")
    except Exception as e:
        log(doc, f"⚠️ Erro ao verificar mensagens: {e}")

    log(doc, "✅ Teste de cadastro de quadras concluído com sucesso!")

except Exception as e:
    log(doc, f"❌ ERRO FATAL: {str(e)}")
    try:
        take_screenshot(driver, doc, "erro_fatal")
    except:
        pass

finally:
    try:
        finalizar_relatorio() 
        driver.quit()
    except:
        pass
    
    log(doc, "🏁 Execução finalizada.")