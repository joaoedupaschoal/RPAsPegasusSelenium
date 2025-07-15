from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from webdriver_manager.chrome import ChromeDriverManager
from docx import Document
from docx.shared import Inches
from faker import Faker
from faker.providers import BaseProvider
import os, random, subprocess, time, sys
from datetime import datetime, timedelta
from selenium.webdriver import ActionChains

# ========================== CONFIGURAÇÃO ==========================
URL = "http://localhost:8080/gs/index.xhtml"
EMAIL = "joaoeduardo.gold@outlook.com"
SENHA = "071999gs"
fake = Faker("pt_BR")
faker = Faker("pt_BR")
doc = Document()
doc.add_heading("RELATÓRIO DO TESTE", 0)
doc.add_paragraph("Cadastro de Cemitérios – Cenário 2: Preenchimento completo e cancelamento.")
doc.add_paragraph(f"Data do teste: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

wait = None
screenshot_registradas = set()

class BrasilProvider(BaseProvider):
    def rg(self):
        numeros = [str(random.randint(0, 9)) for _ in range(8)]
        return ''.join(numeros) + '-' + str(random.randint(0, 9))

fake.add_provider(BrasilProvider)

# ========================== FUNÇÕES AUXILIARES ==========================
def log(msg):
    print(msg)
    doc.add_paragraph(msg)

def take_screenshot(driver, nome):
    if nome not in screenshot_registradas:
        path = f"screenshots/{nome}.png"
        os.makedirs("screenshots", exist_ok=True)
        driver.save_screenshot(path)
        doc.add_paragraph(f"📸 Screenshot: {nome}")
        doc.add_picture(path, width=Inches(5.5))
        screenshot_registradas.add(nome)

def wait_for_modal_to_disappear():
    """Aguarda que qualquer modal/overlay desapareça"""
    try:
        # Aguarda até que o overlay desapareça
        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, ".blockScreen"))
        )
        time.sleep(1)  # Aguarda adicional para garantir
    except TimeoutException:
        pass  # Se não encontrar o overlay, continua

def safe_click(element):
    """Clica em um elemento de forma segura, aguardando que seja clicável"""
    try:
        # Aguarda o elemento ser clicável
        clickable_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(element)
        )
        
        # Rola até o elemento se necessário
        driver.execute_script("arguments[0].scrollIntoView(true);", clickable_element)
        time.sleep(0.5)
        
        # Tenta clicar
        clickable_element.click()
        
    except ElementClickInterceptedException:
        # Se ainda houver interceptação, tenta JavaScript
        if isinstance(element, tuple):
            element_obj = driver.find_element(*element)
        else:
            element_obj = element
        driver.execute_script("arguments[0].click();", element_obj)

def safe_action(descricao, func):
    try:
        log(f"🔄 {descricao}")
        
        # Aguarda modais desaparecerem antes de executar
        wait_for_modal_to_disappear()
        
        func()
        log(f"✅ {descricao} concluída.")
        take_screenshot(driver, descricao.lower().replace(" ", "_"))
    except Exception as e:
        log(f"❌ Erro ao {descricao.lower()}: {e}")
        take_screenshot(driver, f"erro_{descricao.lower().replace(' ', '_')}")

def ajustar_zoom():
    try:
        driver.execute_script("document.body.style.zoom='90%'")
        log("🔍 Zoom ajustado para 90%.")
    except Exception as e:
        log(f"⚠️ Erro ao ajustar zoom: {e}")

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
                log(f"📢 {tipo}: {elemento.text}")
                return elemento
        except NoSuchElementException:
            continue
    
    log("ℹ️ Nenhuma mensagem de alerta encontrada.")
    return None

def finalizar_relatorio():
    nome_arquivo = f"relatorio_cemiterio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"
    doc.save(nome_arquivo)
    log(f"📄 Relatório salvo como: {nome_arquivo}")
    try:
        subprocess.run(["start", "winword", nome_arquivo], shell=True)
    except Exception as e:
        log(f"⚠️ Erro ao abrir relatório: {e}")
    driver.quit()

def gerar_datas_validas():
    """Gera datas coerentes para nascimento, falecimento, sepultamento e agendamento dentro de um intervalo válido."""
    
    hoje = datetime.today().date()
    dez_anos_atras = hoje - timedelta(days=3650)  # Limite máximo de 10 anos atrás
    sessenta_dias_depois = hoje + timedelta(days=60)
    
    # Gera data de agendamento (até 60 dias a partir de hoje)
    data_agendamento = fake.date_between(start_date=hoje, end_date=sessenta_dias_depois)

    # Gera data de nascimento (antes de 100 anos)
    data_nascimento = fake.date_between(start_date=dez_anos_atras - timedelta(days=36500), end_date=dez_anos_atras)
    
    # Gera uma data de falecimento entre 10 anos atrás e hoje (não pode ser posterior ao nascimento)
    data_falecimento = fake.date_between(start_date=data_nascimento, end_date=hoje)
    
    # Gera uma data de sepultamento entre o dia de falecimento e 60 dias após a data de falecimento
    data_sepultamento = fake.date_between(start_date=data_falecimento, end_date=sessenta_dias_depois)

    # Ajuste de idade mínima e máxima
    idade_minima = 18
    idade_maxima = 110
    data_nascimento = data_falecimento - timedelta(days=random.randint(idade_minima * 365, idade_maxima * 365))

    # Sepultamento entre 1 e 10 dias após o falecimento
    data_sepultamento = data_falecimento + timedelta(days=random.randint(1, 10))

    # Registro entre 1 e 10 dias após o sepultamento
    data_registro = data_sepultamento + timedelta(days=random.randint(1, 10))

    data_efetivacao = fake.date_between(start_date=hoje - timedelta(days=365*5), end_date=hoje - timedelta(days=365))

    # Verifica se o ano é menor que 1900 e ajusta a data, se necessário
    def formatar_data(data):
        if data.year < 1900:
            data = data.replace(year=hoje.year)  # Ajusta para o ano atual se for menor que 1900
        return data.strftime('%d/%m/%y')

    # Formata as datas para o formato ddmmyy
    data_nascimento = formatar_data(data_nascimento)
    data_falecimento = formatar_data(data_falecimento)
    data_sepultamento = formatar_data(data_sepultamento)
    data_agendamento = formatar_data(data_agendamento)
    data_registro = formatar_data(data_registro)
    data_efetivacao = formatar_data(data_efetivacao)

    return data_nascimento, data_falecimento, data_sepultamento, data_agendamento, data_registro, data_efetivacao

def gerar_data_e_hora_compromisso():
    data = datetime.now() + timedelta(days=random.randint(1, 10))
    hora = f"{random.randint(8, 18):02d}:{random.choice(['00', '30'])}"
    return data.strftime("%d/%m/%Y"), hora

def preencher_data(selector, valor):
    def acao():
        campo = wait.until(EC.presence_of_element_located((By.XPATH, selector)))
        campo.click()  # Clica no campo para garantir que ele esteja ativo
        campo.clear()  # Limpa o campo antes de preencher
        campo.send_keys(valor)  # Simula o foco no próximo campo
        time.sleep(0.2)
        campo.send_keys(valor)  # Simula o foco no próximo campo
        time.sleep(0.2)
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
def acao_preencher_cep():
    sucesso = preencher_campo_com_retry(
        driver,
        wait,
        "#fmod_5 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroCemiterio > div.catWrapper > div > div.cat_categoriaDadosCemiterio.categoriaHolder > div.groupHolder.clearfix.grupo_grupoEnderecoCemiterio > div > div > div:nth-child(1) > div > input",
        "15081115"
    )
    if not sucesso:
        raise Exception("Não foi possível preencher o campo CEP")
    
    campo = driver.find_element(By.CSS_SELECTOR, "#fmod_5 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroCemiterio > div.catWrapper > div > div.cat_categoriaDadosCemiterio.categoriaHolder > div.groupHolder.clearfix.grupo_grupoEnderecoCemiterio > div > div > div:nth-child(1) > div > input")
    campo.send_keys(Keys.ENTER)
    time.sleep(2)



def preencher_campo_seguro(selector, valor):
    """Preenche um campo de forma segura, aguardando que esteja disponível"""
    try:
        campo = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
        campo.clear()
        campo.send_keys(valor)
        time.sleep(0.3)
    except TimeoutException:
        log(f"⚠️ Campo {selector} não encontrado ou não clicável")
        raise

# ========================== DADOS ALEATÓRIOS ==========================
cemetery_name = f"Cemitério {faker.last_name()} {faker.random.choice(['Eterno', 'da Paz', 'Memorial', 'Descanso'])}"
dias_para_exumar = int(faker.random.choice(['365', '730', '1095', '1460', '1825']))
idade_inicio = fake.random_int(min=1, max=15)
idade_fim = fake.random_int(min=idade_inicio+1, max=99)

# Chama a função para obter as datas
data_nascimento, data_falecimento, data_sepultamento, data_agendamento, data_registro, data_efetivacao = gerar_datas_validas()

# ========================== INICIALIZAÇÃO ==========================
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
wait = WebDriverWait(driver, 15)  # Aumentei o timeout

# ========================== EXECUÇÃO DO TESTE ==========================
try:
    safe_action("Acessando sistema", lambda: driver.get(URL))

    safe_action("Login no sistema", lambda: (
        wait.until(EC.presence_of_element_located((By.ID, "j_id15:email"))).send_keys(EMAIL),
        wait.until(EC.presence_of_element_located((By.ID, "j_id15:senha"))).send_keys(SENHA, Keys.ENTER)
    ))

    safe_action("Esperando o ícone do usuario aparecer e ajustando zoom", lambda: (
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.HEADER.clearfix > div.user > h2 > sup > span"))),
        ajustar_zoom()
    ))

    safe_action("Abrir menu com F2", lambda: (
        safe_click((By.CSS_SELECTOR, "body > div.sideMenu.animate > div.menuHolder > a.button.btModules > span")),
        time.sleep(2)
    ))

    safe_action("Buscar por Cemitérios", lambda: (
        wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Busque um cadastro']")))
        .send_keys("Cemitérios", Keys.RETURN),
        time.sleep(3)
    ))

    safe_action("Clicar em Cadastrar", lambda: (
        safe_click((By.CSS_SELECTOR, "#fmod_5 > div.wdTelas > div > ul > li:nth-child(1) > a > span"))
    ))

    safe_action("Preencher Nome", lambda: preencher_campo_seguro(
        "#fmod_5 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroCemiterio > div.catWrapper > div > div.cat_categoriaDadosCemiterio.categoriaHolder > div.groupHolder.clearfix.grupo_grupoDadosCemiterio > div > div > div:nth-child(2) > input",
        cemetery_name
    ))

    safe_action("Selecionar Status Ativo", lambda: Select(driver.find_element(
        By.CSS_SELECTOR,
        "#fmod_5 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroCemiterio > div.catWrapper > div > div.cat_categoriaDadosCemiterio.categoriaHolder > div.groupHolder.clearfix.grupo_grupoDadosCemiterio > div > div > div:nth-child(3) > select"
    )).select_by_visible_text("Ativo"))

    safe_action("Preencher Dias para Exumar", lambda: preencher_campo_seguro(
        "#fmod_5 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroCemiterio > div.catWrapper > div > div.cat_categoriaDadosCemiterio.categoriaHolder > div.groupHolder.clearfix.grupo_grupoDadosCemiterio > div > div > div:nth-child(4) > input",
        str(dias_para_exumar)
    ))

    safe_action("Preencher CEP", acao_preencher_cep)


    safe_action("Confirmar preenchimento de endereço", lambda: (
        time.sleep(2),  # Aguarda o modal aparecer
        safe_click((By.CSS_SELECTOR, "#BtYes"))
    ))

    safe_action("Preencher Número", lambda: preencher_campo_seguro(
        "#fmod_5 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroCemiterio > div.catWrapper > div > div.cat_categoriaDadosCemiterio.categoriaHolder > div.groupHolder.clearfix.grupo_grupoEnderecoCemiterio > div > div > div:nth-child(4) > input",
        "1733"
    ))

    safe_action("Preencher Complemento", lambda: preencher_campo_seguro(
        "#fmod_5 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroCemiterio > div.catWrapper > div > div.cat_categoriaDadosCemiterio.categoriaHolder > div.groupHolder.clearfix.grupo_grupoEnderecoCemiterio > div > div > div:nth-child(5) > input",
        "Casa"
    ))


    safe_action("Acessar aba Exumação por Idade", lambda: (
        safe_click((By.LINK_TEXT, "Exumação por Idade")),
        time.sleep(2)  # Aguarda a aba carregar
    ))

    safe_action("Preencher Idade Inicial", lambda: preencher_campo_seguro(
        "#fmod_5 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroCemiterio > div.catWrapper > div > div.cat_categoriaExumacaoPorIdade.categoriaHolder > div > div.group_grupoExumacaoPorIdade.clearfix.grupoHolder.lista > div > div:nth-child(1) > input",
        str(idade_inicio)
    ))

    safe_action("Preencher Idade Final", lambda: preencher_campo_seguro(
        "#fmod_5 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroCemiterio > div.catWrapper > div > div.cat_categoriaExumacaoPorIdade.categoriaHolder > div > div.group_grupoExumacaoPorIdade.clearfix.grupoHolder.lista > div > div:nth-child(2) > input",
        str(idade_fim)
    ))

    safe_action("Preencher Dias para Exumar por Idade", lambda: preencher_campo_seguro(
        "#fmod_5 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroCemiterio > div.catWrapper > div > div.cat_categoriaExumacaoPorIdade.categoriaHolder > div > div.group_grupoExumacaoPorIdade.clearfix.grupoHolder.lista > div > div:nth-child(3) > input",
        str(dias_para_exumar)
    ))

    safe_action("Adicionar faixa de exumação", lambda: safe_click((
        By.CSS_SELECTOR,
        "#fmod_5 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroCemiterio > div.catWrapper > div > div.cat_categoriaExumacaoPorIdade.categoriaHolder > div > div.btnListHolder > a.btAddGroup"
    )))

    safe_action("Cancelar Cemitério", lambda: safe_click((
        By.CSS_SELECTOR,
        "#fmod_5 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroCemiterio > div.btnHolder > a.btModel.btGray.btcancel"
    )))

    # Aguarda mensagem de alerta
    time.sleep(3)
    encontrar_mensagem_alerta()

    safe_action("Fechar modal", lambda: safe_click((
        By.CSS_SELECTOR,
        "#fmod_5 > div.wdTop.ui-draggable-handle > div.wdClose > a"
    )))

except Exception as e:
    log(f"❌ ERRO FATAL: {e}")
    take_screenshot(driver, "erro_fatal")

finally:
    # CORREÇÃO: Remover o parâmetro 'doc' da função log()
    log("✅ Teste concluído com sucesso.")
    finalizar_relatorio()