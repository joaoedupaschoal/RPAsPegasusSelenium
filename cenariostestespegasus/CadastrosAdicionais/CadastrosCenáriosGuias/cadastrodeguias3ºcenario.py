# Refatorado e organizado: cadastrodeguias1ºcenario.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from docx import Document
from docx.shared import Inches
from faker import Faker
from faker.providers import BaseProvider
from validate_docbr import CPF
from datetime import datetime, timedelta
import subprocess
import os
import time
import random
import string
from selenium.common.exceptions import TimeoutException, NoSuchElementException


# ==== PROVIDERS CUSTOMIZADOS ====
class BrasilProvider(BaseProvider):
    def rg(self):
        numeros = [str(random.randint(0, 9)) for _ in range(8)]
        return ''.join(numeros) + '-' + str(random.randint(0, 9))

fake = Faker("pt_BR")
faker = Faker('pt_BR')
fake.add_provider(BrasilProvider)

# ==== CONFIGURAÇÕES ====
URL = "http://localhost:8080/gs/index.xhtml"
LOGIN_EMAIL = "joaoeduardo.gold@outlook.com"
LOGIN_PASSWORD = "071999gs"

# ==== DOCUMENTO ====
doc = Document()
doc.add_heading("RELATÓRIO DO TESTE", 0)
doc.add_paragraph("Cadastro de Guias – Cenário 3: Preenchimento dos campos obrigatórios e salvamento.")
doc.add_paragraph(f"Data do teste: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

screenshot_registradas = set()

# ==== FUNÇÕES DE UTILITÁRIO ====
def log(doc, msg):
    print(msg)
    doc.add_paragraph(msg)

def take_screenshot(driver, doc, nome):
    if nome not in screenshot_registradas:
        path = f"screenshots/{nome}.png"
        os.makedirs("screenshots", exist_ok=True)
        driver.save_screenshot(path)
        doc.add_paragraph(f"Screenshot: {nome}")
        doc.add_picture(path, width=Inches(5.5))
        screenshot_registradas.add(nome)



def safe_action(doc, descricao, func):
    try:
        log(doc, f"🔄 {descricao}...")
        func()
        log(doc, f"✅ {descricao} realizada com sucesso.")
        take_screenshot(driver, doc, descricao.lower().replace(" ", "_"))
    except Exception as e:
        log(doc, f"❌ Erro ao {descricao.lower()}: {e}")
        take_screenshot(driver, doc, f"erro_{descricao.lower().replace(' ', '_')}")

def finalizar_relatorio():
    nome_arquivo = f"relatorio_guias_cenario_3_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"
    doc.save(nome_arquivo)
    log(doc, f"📄 Relatório salvo como: {nome_arquivo}")
    subprocess.run(["start", "winword", nome_arquivo], shell=True)
    driver.quit()

def gerar_datas_validas():
    """Gera datas coerentes para o cadastro de guias."""
    hoje = datetime.today().date()
    
    # Data de emissão no passado
    data_emissao = hoje - timedelta(days=random.randint(1, 100))
    
    # Data de vencimento no futuro
    data_vencimento = hoje + timedelta(days=random.randint(30, 180))
    
    # Data de consulta entre hoje e vencimento
    data_consulta = faker.date_between(start_date=hoje, end_date=data_vencimento)
    
    return (
        data_emissao.strftime("%d/%m/%Y"),
        data_vencimento.strftime("%d/%m/%Y"),
        data_consulta.strftime("%d/%m/%Y")
    )

def gerar_dados_guia():
    """Gera dados fictícios para o cadastro de guia."""
    data_emissao, data_vencimento, data_consulta = gerar_datas_validas()
    
    # Gera hora aleatória entre 08:00 e 17:59
    hora = random.randint(8, 17)
    minuto = random.randint(0, 59)
    hora_formatada = f"{hora:02d}:{minuto:02d}"
    
    return data_emissao, data_vencimento, data_consulta, hora_formatada

def encontrar_mensagem_alerta():
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
    try:
        driver.execute_script("document.body.style.zoom='90%'")
        log(doc, "🔍 Zoom ajustado para 90%.")
    except Exception as e:
        log(doc, f"⚠️ Erro ao ajustar zoom: {e}")

def selecionar_opcao(selector, texto):
    def acao():
        select_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
        Select(select_element).select_by_visible_text(texto)
    return acao

def preencher_campo_data(xpath, valor):
    def acao():
        campo = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        campo.send_keys(valor)
        campo.send_keys(Keys.TAB)
    return acao

def abrir_modal_e_selecionar(btn_selector, pesquisa_selector, termo_pesquisa, btn_pesquisar_selector, resultado_xpath):
    def acao():
        # Abre o modal
        open_lov = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, btn_selector)))
        open_lov.click()

        # Aguarda campo pesquisa
        campo_pesquisa = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, pesquisa_selector)))
        campo_pesquisa.clear()
        campo_pesquisa.send_keys(termo_pesquisa)

        # Clica pesquisar
        pesquisar = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, btn_pesquisar_selector)))
        pesquisar.click()
        time.sleep(1)
        # Espera o resultado carregar
        wait.until(EC.presence_of_element_located((By.XPATH, resultado_xpath)))
        wait.until(EC.visibility_of_element_located((By.XPATH, resultado_xpath)))
        wait.until(EC.element_to_be_clickable((By.XPATH, resultado_xpath)))

        # Relocaliza no último instante (evita stale element)
        resultado = driver.find_element(By.XPATH, resultado_xpath)
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", resultado)
        time.sleep(0.2)
        resultado.click()

    return acao


def preencher_campo_com_retry(driver, wait, seletor, valor, max_tentativas=2):
    """Tenta preencher o campo com diferentes métodos até conseguir"""
    
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
            else:
                print()
                
        except Exception as e:
            time.sleep(1)
    

    return False

from selenium.webdriver.support.ui import Select

def abrir_dropdown_tipo_modelo(driver, wait):
    try:
        print("🔵 Abrindo dropdown de Tipo de Modelo...")
        dropdown = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#tipoModelo")))
        dropdown.click()

        print("🟢 Aguardando opções carregarem...")
        # Aguardar pelo menos uma opção visível — ajusta se necessário!
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "ul li")))
        print("✅ Lista carregada.")
        return True
    except Exception as e:
        print(f"❌ Erro ao abrir o dropdown: {e}")
        return False
from selenium.webdriver.support.ui import Select

def selecionar_modelo_com_select(driver, wait, texto_opcao):
    try:
        print(f"🔵 Selecionando '{texto_opcao}' no dropdown #tipoModelo...")
        select_element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#tipoModelo")))
        select = Select(select_element)
        select.select_by_visible_text(texto_opcao)
        print(f"✅ '{texto_opcao}' selecionado com sucesso.")
        return True
    except Exception as e:
        print(f"❌ Erro ao selecionar '{texto_opcao}': {e}")
        return False



# Gera os dados necessários
data_emissao, data_vencimento, data_consulta, hora_formatada = gerar_dados_guia()

# ==== INICIALIZAÇÃO DO DRIVER ====
options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 20)



# ==== EXECUÇÃO DO TESTE ====
try:
    safe_action(doc, "Acessando sistema", lambda: driver.get(URL))

    safe_action(doc, "Realizando login", lambda: (
        wait.until(EC.presence_of_element_located((By.ID, "j_id15:email"))).send_keys(LOGIN_EMAIL),
        wait.until(EC.presence_of_element_located((By.ID, "j_id15:senha"))).send_keys(LOGIN_PASSWORD, Keys.ENTER),
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    ))

    safe_action(doc, "Esperando sistema carregar e ajustando zoom", lambda: (
        time.sleep(5),
        ajustar_zoom()
    ))

    safe_action(doc, "Abrindo menu Guias", lambda: (
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.F2),
        time.sleep(1),
        wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Busque um cadastro']"))).send_keys("Guias", Keys.ENTER),
        time.sleep(3)
    ))

    safe_action(doc, "Clicando em Cadastrar", lambda: (
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#fmod_10067 > div.wdTelas > div.telaInicial.clearfix.overflow.overflowY > ul > li:nth-child(1) > a > span"))).click(),
        time.sleep(2)
    ))

    # Preenchendo dados da guia
    safe_action(doc, "Preenchendo Data de Emissão", preencher_campo_data(
        "//input[contains(@class, 'hasDatepicker dataEmissao mandatory')]", data_emissao
    ))

    safe_action(doc, "Preenchendo Data de Vencimento", preencher_campo_data(
        "//input[contains(@class, 'hasDatepicker dataVencimento mandatory')]", data_vencimento
    ))


    safe_action(doc, "Selecionando Tipo de Agendamento", selecionar_opcao(
        "#fmod_10067 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroGuia > div.catWrapper > div > div > div.groupHolder.clearfix.grupo_geral > div > div:nth-child(2) > div:nth-child(4) > select",
        "Agenda médica"
    ))

    safe_action(doc, "Selecionando Tipo de Guia", selecionar_opcao(
        "#fmod_10067 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroGuia > div.catWrapper > div > div > div.groupHolder.clearfix.grupo_geral > div > div:nth-child(2) > div:nth-child(5) > select",
        "Consulta"
    ))

    safe_action(doc, "Selecionando Tipo de Cliente", selecionar_opcao(
        "#fmod_10067 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroGuia > div.catWrapper > div > div > div.groupHolder.clearfix.grupo_geral > div > div:nth-child(2) > div:nth-child(6) > select",
        "Particular"
    ))


    safe_action(doc, "Selecionando Paciente", abrir_modal_e_selecionar(
        "#fmod_10067 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroGuia > div.catWrapper > div > div > div.groupHolder.clearfix.grupo_geral > div > div.formRow.linhaTipoParticular > div:nth-child(1) > div > a",
        "#txtPesquisa",
        "VINICIUS RODRIGUES SOARES",
        "body > div.modalHolder > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div:nth-child(2) > a",
        "//td[contains(text(), 'VINICIUS RODRIGUES SOARES')]"
    ))

    safe_action(doc, "Selecionando Conveniado", abrir_modal_e_selecionar(
        "#fmod_10067 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroGuia > div.catWrapper > div > div > div.groupHolder.clearfix.grupo_geral > div > div.formRow.linhaTipoParticular > div:nth-child(2) > div > a",
        "body > div.modalHolder > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div.formCol.divPesquisa > div > div > input",
        "APOLLO MENDONÇA",
        "body > div.modalHolder > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div.formRow > div > a",
        "//td[contains(text(), 'APOLLO MENDONÇA')]"
    ))

    safe_action(doc, "Selecionando Especialidade", abrir_modal_e_selecionar(
        "#fmod_10067 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroGuia > div.catWrapper > div > div > div.groupHolder.clearfix.grupo_geral > div > div.formRow.linhaTipoParticular > div:nth-child(3) > div > a",
        "body > div.modalHolder > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div.formCol.divPesquisa > div > div > input",
        "CARDIOLOGISTA",
        "body > div.modalHolder > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div.formRow > div > a",
        "//td[contains(text(), 'CARDIOLOGISTA')]"
    ))





    safe_action(doc, "Salvando cadastro", lambda: (
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#fmod_10067 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroGuia > div.btnHolder > a.btModel.btGray.btsave"))).click(),
    ))


    safe_action(doc, "Fechando modal de documentos", lambda: (
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.modalHolder > div.modal.overflow > a"))).click(),
        time.sleep(1)
    ))



    safe_action(doc, "Fechando modal após salvamento", lambda: (
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#fmod_10067 > div.wdTop.ui-draggable-handle > div.wdClose > a"))).click(),
        time.sleep(1)
    ))

    encontrar_mensagem_alerta()

except Exception as e:
    log(doc, f"❌ ERRO FATAL: {e}")
    take_screenshot(driver, doc, "erro_fatal")

finally:
    log(doc, "✅ Teste concluído com sucesso.")
    finalizar_relatorio()