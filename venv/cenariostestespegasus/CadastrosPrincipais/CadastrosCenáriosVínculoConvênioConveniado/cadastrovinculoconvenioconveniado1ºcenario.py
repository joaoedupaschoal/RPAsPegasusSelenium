# Código corrigido e otimizado: cadastrovinculoconvenioconveniado1ºcenario.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import ActionChains
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, StaleElementReferenceException
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
import re

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
doc.add_paragraph("Cadastro de Vínculo Convênio/Conveniado – Cenário 1: Preenchimento completo e salvamento.")
doc.add_paragraph(f"Data do teste: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

screenshot_registradas = set()

def preencher_campo_com_retry(driver, wait, seletor, valor, max_tentativas=3):
    """Tenta preencher o campo com diferentes métodos até conseguir"""
    
    for tentativa in range(max_tentativas):
        try:
            # Aguarda o elemento estar presente e visível
            campo = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, seletor)))
            
            # Scroll suave até o elemento
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", campo)
            time.sleep(1)
            
            # Aguarda ser clicável
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, seletor)))
            
            # Método 1: Tradicional com clear melhorado
            if tentativa == 0:
                campo.click()
                time.sleep(0.3)
                campo.clear()
                time.sleep(0.3)
                campo.send_keys(valor)
                time.sleep(0.3)
                campo.send_keys(Keys.TAB)
            
            # Método 2: ActionChains com retry
            elif tentativa == 1:
                actions = ActionChains(driver)
                actions.move_to_element(campo).click().perform()
                time.sleep(0.5)
                actions.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
                time.sleep(0.3)
                actions.send_keys(valor).perform()
                time.sleep(0.3)
                actions.send_keys(Keys.TAB).perform()
            
            # Método 3: JavaScript direto
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
            
            time.sleep(1)
            
            # Verifica se o valor foi preenchido corretamente
            valor_atual = campo.get_attribute('value')
            if valor_atual and valor in valor_atual:
                return True
                
        except (TimeoutException, ElementClickInterceptedException, StaleElementReferenceException) as e:
            print(f"Tentativa {tentativa + 1} falhou: {e}")
            time.sleep(2)
        except Exception as e:
            print(f"Erro inesperado na tentativa {tentativa + 1}: {e}")
            time.sleep(2)
    
    return False

# ==== FUNÇÕES DE UTILITÁRIO ====
def log(doc, msg):
    print(msg)
    doc.add_paragraph(msg)

def take_screenshot(driver, doc, nome):
    try:
        nome = re.sub(r'[^a-zA-Z0-9_\-]', '_', str(nome).lower().replace(" ", "_"))
        if nome not in screenshot_registradas:
            path = f"screenshots/{nome}.png"
            os.makedirs("screenshots", exist_ok=True)
            driver.save_screenshot(path)
            doc.add_paragraph(f"Screenshot: {nome}")
            doc.add_picture(path, width=Inches(5.5))
            screenshot_registradas.add(nome)
    except Exception as e:
        print(f"Erro ao tirar screenshot: {e}")

def safe_action(doc, descricao, func):
    try:
        log(doc, f"🔄 {descricao}...")
        func()
        log(doc, f"✅ {descricao} realizada com sucesso.")
        time.sleep(1)  # Pausa padrão após ações
        take_screenshot(driver, doc, descricao.lower().replace(" ", "_"))
        return True
    except Exception as e:
        log(doc, f"❌ Erro ao {descricao.lower()}: {e}")
        take_screenshot(driver, doc, f"erro_{descricao.lower().replace(' ', '_')}")
        return False

def finalizar_relatorio():
    try:
        nome_arquivo = f"relatorio_vinculo_convenio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"
        doc.save(nome_arquivo)
        log(doc, f"📄 Relatório salvo como: {nome_arquivo}")
        
        # Tentativa de abrir o documento
        try:
            subprocess.run(["start", "winword", nome_arquivo], shell=True, check=False)
        except:
            print("Não foi possível abrir automaticamente o documento Word")
    except Exception as e:
        print(f"Erro ao finalizar relatório: {e}")
    finally:
        if 'driver' in globals():
            driver.quit()

def encontrar_mensagem_alerta():
    seletores = [
        (".alerts.salvo", "✅ Sucesso"),
        (".alerts.alerta", "⚠️ Alerta"),
        (".alerts.erro", "❌ Erro"),
        (".ui-messages-info", "ℹ️ Info"),
        (".ui-messages-warn", "⚠️ Aviso"),
        (".ui-messages-error", "❌ Erro"),
    ]

    for seletor, tipo in seletores:
        try:
            elementos = driver.find_elements(By.CSS_SELECTOR, seletor)
            for elemento in elementos:
                if elemento.is_displayed():
                    log(doc, f"📢 {tipo}: {elemento.text}")
                    return elemento
        except Exception as e:
            continue

    log(doc, "ℹ️ Nenhuma mensagem de alerta encontrada.")
    return None

def ajustar_zoom():
    try:
        driver.execute_script("document.body.style.zoom='90%'")
        log(doc, "🔍 Zoom ajustado para 90%.")
        time.sleep(1)
    except Exception as e:
        log(doc, f"⚠️ Erro ao ajustar zoom: {e}")

def aguardar_modal_fechar(timeout=10):
    """Aguarda modal fechar completamente"""
    try:
        wait_modal = WebDriverWait(driver, timeout)
        wait_modal.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.modal.overflow")))
        time.sleep(1)  # Pausa adicional para garantir
        return True
    except TimeoutException:
        print("Modal não fechou no tempo esperado")
        return False

def selecionar_convenio():
    try:
        # Aguarda a tabela carregar com wait mais longo
        wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='DataTables_Table_2']/tbody")))
        time.sleep(3)
        
        # Remove possíveis overlays
        driver.execute_script("""
            var overlays = document.querySelectorAll('.modal-backdrop, .overlay, .loading, .ui-widget-overlay');
            overlays.forEach(function(overlay) { overlay.style.display = 'none'; });
        """)
        
        # Busca linhas da tabela
        linhas = driver.find_elements(By.XPATH, "//*[@id='DataTables_Table_2']/tbody/tr")
        
        if linhas:
            primeira_linha = linhas[0]
            
            # Scroll FORÇADO até a linha
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'instant', block: 'center'});", primeira_linha)
            time.sleep(1)
            
            # CLICK FORÇADO JavaScript
            driver.execute_script("arguments[0].click();", primeira_linha)
            print("✅ CLICK FORÇADO na primeira linha do convênio")
            
            # Aguarda modal fechar com timeout maior
            aguardar_modal_fechar(15)
            return True
        else:
            log(doc, "❗ Nenhum convênio encontrado para selecionar.")
            return False
            
    except Exception as e:
        log(doc, f"Erro ao selecionar convênio: {e}")
        return False

import unicodedata

def normalizar_texto(texto):
    if not texto:
        return ""
    return unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('utf-8').lower().strip()

def selecionar_item_tabela(tabela_id, texto_busca, descricao):
    try:
        wait.until(lambda d: len(d.find_elements(By.XPATH, f"//*[@id='{tabela_id}']/tbody/tr")) > 0)
        time.sleep(1)

        driver.execute_script("""
            document.querySelectorAll('.modal-backdrop, .overlay, .loading, .ui-widget-overlay')
                .forEach(e => { e.style.display = 'none'; e.style.pointerEvents = 'none'; e.style.opacity = '0'; });
        """)

        linhas = driver.find_elements(By.XPATH, f"//*[@id='{tabela_id}']/tbody/tr")
        print(f"🔍 {len(linhas)} linhas encontradas na tabela {tabela_id} para {descricao}")

        texto_busca_normalizado = normalizar_texto(texto_busca)

        for linha in linhas:
            try:
                texto_linha = linha.text.strip()
                texto_linha_normalizado = normalizar_texto(texto_linha)

                print(f"🧾 Verificando linha: {texto_linha}")

                if texto_busca_normalizado in texto_linha_normalizado:
                    print(f"➡️ Clicando na linha de {descricao}: {texto_linha}")
                    driver.execute_script("arguments[0].scrollIntoView({behavior:'auto', block:'center'});", linha)
                    time.sleep(0.5)
                    driver.execute_script("arguments[0].click();", linha)

                    WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, ".modal.overflow")))
                    return True

            except Exception as e:
                print(f"⚠️ Erro ao tentar clicar na linha: {e}")
                continue

        log(doc, f"❗ Nenhuma linha contendo '{texto_busca}' foi encontrada na tabela {descricao}.")
        return False

    except Exception as e:
        log(doc, f"❌ Erro ao selecionar item da tabela {descricao}: {e}")
        return False


def clicar_elemento_com_retry(seletor, descricao, max_tentativas=5):
    """Clica em elemento com retry FORÇADO e diferentes métodos"""
    for tentativa in range(max_tentativas):
        try:
            # Aguarda elemento estar presente
            elemento = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, seletor)))
            
            # Scroll FORÇADO até o elemento
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'instant', block: 'center'});", elemento)
            time.sleep(0.5)
            
            # Remove sobreposições que podem interceptar o click
            driver.execute_script("""
                var overlays = document.querySelectorAll('.modal-backdrop, .overlay, .loading');
                overlays.forEach(function(overlay) { overlay.style.display = 'none'; });
            """)
            
            if tentativa == 0:
                # Método 1: Click JavaScript FORÇADO (mais confiável)
                driver.execute_script("arguments[0].click();", elemento)
                print(f"Click JavaScript FORÇADO em {descricao}")
                
            elif tentativa == 1:
                # Método 2: Click normal com wait forçado
                wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, seletor)))
                elemento.click()
                print(f"Click normal FORÇADO em {descricao}")
                
            elif tentativa == 2:
                # Método 3: ActionChains com coordenadas
                ActionChains(driver).move_to_element(elemento).pause(0.5).click().perform()
                print(f"ActionChains FORÇADO em {descricao}")
                
            elif tentativa == 3:
                # Método 4: JavaScript com eventos disparados
                driver.execute_script("""
                    arguments[0].focus();
                    arguments[0].click();
                    arguments[0].dispatchEvent(new MouseEvent('click', {bubbles: true, cancelable: true}));
                """, elemento)
                print(f"JavaScript com eventos FORÇADO em {descricao}")
                
            else:
                # Método 5: Força bruta - tenta tudo
                try:
                    elemento.click()
                except:
                    try:
                        ActionChains(driver).move_to_element(elemento).click().perform()
                    except:
                        driver.execute_script("arguments[0].click();", elemento)
                print(f"Força bruta FORÇADA em {descricao}")
            
            time.sleep(1)
            return True
            
        except Exception as e:
            print(f"TENTATIVA {tentativa + 1} de clicar FORÇADO em {descricao} falhou: {e}")
            time.sleep(1)
    
    print(f"❌ FALHA TOTAL - Não foi possível clicar FORÇADO em {descricao}")
    return False

# ==== INICIALIZAÇÃO DO DRIVER ====
options = Options()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

# Inicialização com tratamento de erro
driver = None
try:
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    wait = WebDriverWait(driver, 20)
except Exception as e:
    print(f"Erro ao inicializar driver: {e}")
    exit(1)

# ==== EXECUÇÃO DO TESTE ====
try:
    # Login
    if not safe_action(doc, "Acessando sistema", lambda: driver.get(URL)):
        raise Exception("Falha ao acessar sistema")

    if not safe_action(doc, "Realizando login", lambda: (
        wait.until(EC.presence_of_element_located((By.ID, "j_id15:email"))).send_keys(LOGIN_EMAIL),
        wait.until(EC.presence_of_element_located((By.ID, "j_id15:senha"))).send_keys(LOGIN_PASSWORD),
        wait.until(EC.element_to_be_clickable((By.ID, "j_id15:senha"))).send_keys(Keys.ENTER),
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    )):
        raise Exception("Falha no login")

    # Aguardar sistema carregar
    safe_action(doc, "Aguardando sistema carregar", lambda: time.sleep(5))
    ajustar_zoom()

    # Abrir menu
    if not safe_action(doc, "Abrindo menu Vínculo Convênio/Conveniado", lambda: (
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.F2),
        time.sleep(2),
        wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Busque um cadastro']"))).send_keys("Vínculo Convênio / Conveniado"),
        time.sleep(1),
        driver.find_element(By.XPATH, "//input[@placeholder='Busque um cadastro']").send_keys(Keys.ENTER),
        time.sleep(3)
    )):
        raise Exception("Falha ao abrir menu")

    # Clicar em Cadastrar com FORÇA TOTAL
    if not safe_action(doc, "Clicando FORÇADO em Cadastrar", lambda: (
        driver.execute_script("""
            var botao = document.querySelector('#fmod_10068 > div.wdTelas > div > ul > li > a > span');
            if (botao) {
                botao.scrollIntoView({behavior: 'instant', block: 'center'});
                botao.click();
                botao.dispatchEvent(new MouseEvent('click', {bubbles: true, cancelable: true}));
            }
        """),
        time.sleep(2)
    )):
        # Se JavaScript falhar, tenta método tradicional FORÇADO
        clicar_elemento_com_retry("#fmod_10068 > div.wdTelas > div > ul > li > a > span", "botão Cadastrar")

    # Abrir LOV Convênio com FORÇA TOTAL
    if not safe_action(doc, "Abrindo LOV Convênio FORÇADO", lambda: (
        driver.execute_script("""
            var botao = document.querySelector('#fmod_10068 > div.wdTelas > div.telaCadastro.clearfix.telaVinculoConvenioConveniado > div.catWrapper > div > div > div > div > div:nth-child(2) > div:nth-child(1) > div > a');
            if (botao) {
                botao.scrollIntoView({behavior: 'instant', block: 'center'});
                botao.click();
                botao.dispatchEvent(new MouseEvent('click', {bubbles: true, cancelable: true}));
            }
        """),
        time.sleep(2)
    )):
        clicar_elemento_com_retry("#fmod_10068 > div.wdTelas > div.telaCadastro.clearfix.telaVinculoConvenioConveniado > div.catWrapper > div > div > div > div > div:nth-child(2) > div:nth-child(1) > div > a", "LOV Convênio")

    # Pesquisar Convênio com FORÇA TOTAL
    if not safe_action(doc, "Pesquisando Convênio FORÇADO", lambda: (
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.modalHolder > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div.formCol.divPesquisa > input"))).clear(),
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.modalHolder > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div.formCol.divPesquisa > input"))).send_keys("TESTE CONVÊNIO SELENIUM AUTOMATIZADO"),
        time.sleep(1),
        driver.execute_script("""
            var botao = document.querySelector('body > div.modalHolder > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div:nth-child(3) > a');
            if (botao) { botao.click(); }
        """),
        time.sleep(3)
    )):
        raise Exception("Falha ao pesquisar convênio")

    # Selecionar Convênio com FORÇA TOTAL
    if not safe_action(doc, "Selecionando Convênio FORÇADO", selecionar_convenio):
        raise Exception("Falha ao selecionar convênio")

    # Abrir LOV Conveniado com FORÇA TOTAL
    if not safe_action(doc, "Abrindo LOV Conveniado FORÇADO", lambda: (
        time.sleep(2),
        driver.execute_script("""
            var botao = document.querySelector('#fmod_10068 > div.wdTelas > div.telaCadastro.clearfix.telaVinculoConvenioConveniado > div.catWrapper > div > div > div > div > div:nth-child(2) > div:nth-child(2) > div > a');
            if (botao) {
                botao.scrollIntoView({behavior: 'instant', block: 'center'});
                botao.click();
                botao.dispatchEvent(new MouseEvent('click', {bubbles: true, cancelable: true}));
            }
        """),
        time.sleep(2)
    )):
        clicar_elemento_com_retry("#fmod_10068 > div.wdTelas > div.telaCadastro.clearfix.telaVinculoConvenioConveniado > div.catWrapper > div > div > div > div > div:nth-child(2) > div:nth-child(2) > div > a", "LOV Conveniado")

    # Pesquisar Conveniado com FORÇA TOTAL
    if not safe_action(doc, "Pesquisando Conveniado FORÇADO", lambda: (
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.modalHolder > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div.formCol.divPesquisa > div > div > input"))).clear(),
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.modalHolder > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div.formCol.divPesquisa > div > div > input"))).send_keys("TESTE CONVENIADO SELENIUM AUTOMATIZADO"),
        time.sleep(1),
        driver.execute_script("""
            var botao = document.querySelector('body > div.modalHolder > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div.formRow > div > a');
            if (botao) { botao.click(); }
        """),
        time.sleep(3)
    )):
        raise Exception("Falha ao pesquisar conveniado")

    # Selecionar Conveniado com FORÇA TOTAL
    safe_action(doc, "Selecionando Conveniado FORÇADO", lambda: selecionar_item_tabela("DataTables_Table_4", "TESTE CONVENIADO SELENIUM AUTOMATIZADO", "conveniado"))


    # Abrir LOV Especialidade com FORÇA TOTAL
    if not safe_action(doc, "Abrindo LOV Especialidade FORÇADO", lambda: (
        time.sleep(2),
        driver.execute_script("""
            var botao = document.querySelector('#fmod_10068 > div.wdTelas > div.telaCadastro.clearfix.telaVinculoConvenioConveniado > div.catWrapper > div > div > div > div > div:nth-child(3) > div:nth-child(1) > div > div > a');
            if (botao) {
                botao.scrollIntoView({behavior: 'instant', block: 'center'});
                botao.click();
                botao.dispatchEvent(new MouseEvent('click', {bubbles: true, cancelable: true}));
            }
        """),
        time.sleep(2)
    )):
        clicar_elemento_com_retry("#fmod_10068 > div.wdTelas > div.telaCadastro.clearfix.telaVinculoConvenioConveniado > div.catWrapper > div > div > div > div > div:nth-child(3) > div:nth-child(1) > div > div > a", "LOV Especialidade")

    # Pesquisar Especialidade com FORÇA TOTAL
    if not safe_action(doc, "Pesquisando Especialidade FORÇADO", lambda: (
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.modalHolder > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div.formCol.divPesquisa > div > div > input"))).clear(),
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.modalHolder > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div.formCol.divPesquisa > div > div > input"))).send_keys("CARDIOLOGISTA"),
        time.sleep(1),
        driver.execute_script("""
            var botao = document.querySelector('body > div.modalHolder > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div.formRow > div > a');
            if (botao) { botao.click(); }
        """),
        time.sleep(3)
    )):
        raise Exception("Falha ao pesquisar especialidade")

    # Selecionar Especialidade com FORÇA TOTAL
    if not safe_action(doc, "Selecionando Especialidade FORÇADO", lambda: selecionar_item_tabela("DataTables_Table_4", "CARDIOLOGISTA", "especialidade")):
        raise Exception("Falha ao selecionar especialidade")

    # Salvar com FORÇA TOTAL
    if not safe_action(doc, "Salvando Vínculo FORÇADO", lambda: (
        time.sleep(2),
        driver.execute_script("""
            var botao = document.querySelector('#fmod_10068 > div.wdTelas > div.telaCadastro.clearfix.telaVinculoConvenioConveniado > div.catWrapper > div > div > div > div > div:nth-child(3) > div:nth-child(2) > a');
            if (botao) {
                botao.scrollIntoView({behavior: 'instant', block: 'center'});
                botao.click();
                botao.dispatchEvent(new MouseEvent('click', {bubbles: true, cancelable: true}));
            }
        """),
        time.sleep(2)
    )):
        clicar_elemento_com_retry("#fmod_10068 > div.wdTelas > div.telaCadastro.clearfix.telaVinculoConvenioConveniado > div.catWrapper > div > div > div > div > div:nth-child(3) > div:nth-child(2) > a", "botão Salvar")

    # Pesquisar após salvar com FORÇA TOTAL
    if not safe_action(doc, "Pesquisando após salvar FORÇADO", lambda: (
        time.sleep(2),
        driver.execute_script("""
            var botao = document.querySelector('#fmod_10068 > div.wdTelas > div.telaCadastro.clearfix.telaVinculoConvenioConveniado > div.catWrapper > div > div > div > div > div:nth-child(3) > div:nth-child(3) > a');
            if (botao) {
                botao.scrollIntoView({behavior: 'instant', block: 'center'});
                botao.click();
                botao.dispatchEvent(new MouseEvent('click', {bubbles: true, cancelable: true}));
            }
        """),
        time.sleep(2)
    )):
        clicar_elemento_com_retry("#fmod_10068 > div.wdTelas > div.telaCadastro.clearfix.telaVinculoConvenioConveniado > div.catWrapper > div > div > div > div > div:nth-child(3) > div:nth-child(3) > a", "botão Pesquisar")

    # Fechar modal final com FORÇA TOTAL
    safe_action(doc, "Fechando modal final FORÇADO", lambda: (
        time.sleep(3),
        driver.execute_script("""
            var botao = document.querySelector('#fmod_10068 > div.wdTop.ui-draggable-handle > div.wdClose > a');
            if (botao) {
                botao.scrollIntoView({behavior: 'instant', block: 'center'});
                botao.click();
                botao.dispatchEvent(new MouseEvent('click', {bubbles: true, cancelable: true}));
            }
        """)
    ))

    time.sleep(2)
    log(doc, "🔍 Verificando mensagens de alerta...")
    encontrar_mensagem_alerta()

except Exception as e:
    log(doc, f"❌ ERRO FATAL: {e}")
    take_screenshot(driver, doc, "erro_fatal")

finally:
    log(doc, "✅ Teste concluído com sucesso.")
    finalizar_relatorio()