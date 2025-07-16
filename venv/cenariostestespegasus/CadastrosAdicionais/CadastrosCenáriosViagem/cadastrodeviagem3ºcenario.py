# Refatorado e organizado: cadastrodeescalamotorista2ºcenario.py

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



# ==== PROVIDERS CUSTOMIZADOS ====
class BrasilProvider(BaseProvider):
    def rg(self):
        numeros = [str(random.randint(0, 9)) for _ in range(8)]
        return ''.join(numeros) + '-' + str(random.randint(0, 9))

fake = Faker("pt_BR")
faker = Faker("pt_BR")

fake.add_provider(BrasilProvider)

def gerar_datas_validas():
    """Gera datas coerentes para admissão, início e fim da escala, e vencimento da CNH."""
    hoje = datetime.today().date()
    
    # Data de admissão entre 10 anos atrás e hoje
    data_admissao = fake.date_between(start_date=hoje - timedelta(days=3650), end_date=hoje)
    
    # Data de início da escala entre hoje e 1 ano no futuro
    data_inicio = fake.date_between(start_date=hoje, end_date=hoje + timedelta(days=365))
    
    # Data fim entre 1 e 180 dias após a data de início
    data_fim = data_inicio + timedelta(days=random.randint(1, 180))
    
    # Vencimento CNH entre hoje e 10 anos no futuro
    vencimento_cnh = fake.date_between(start_date=hoje, end_date=hoje + timedelta(days=3650))
    
    return (data_admissao.strftime('%d/%m/%Y'), 
            data_inicio.strftime('%d/%m/%Y'), 
            data_fim.strftime('%d/%m/%Y'), 
            vencimento_cnh.strftime('%d/%m/%Y'))

def gerar_dados_documentos():
    """Gera documentos fictícios para o cadastro."""
    carteira_trabalho = str(random.randint(10000000, 99999999))
    pis = fake.cpf().replace('.', '').replace('-', '')[:11]
    cnh = str(random.randint(10000000000, 99999999999))
    cpf = CPF().generate()
    
    return carteira_trabalho, pis, cnh, cpf

# Gera os dados necessários
data_admissao, data_inicio, data_fim, vencimento_cnh = gerar_datas_validas()
carteira_trabalho, pis, cnh, cpf_valido = gerar_dados_documentos()

# ==== CONFIGURAÇÕES ====
URL = "http://localhost:8080/gs/index.xhtml"
LOGIN_EMAIL = "joaoeduardo.gold@outlook.com"
LOGIN_PASSWORD = "071999gs"

# ==== DOCUMENTO ====
doc = Document()
doc.add_heading("RELATÓRIO DO TESTE", 0)
doc.add_paragraph("Cadastro de Viagens – Cenário 3: Preenchimento dos campos obrigatórios e salvamento.")
doc.add_paragraph(f"Data do teste: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

screenshot_registradas = set()

# ==== FUNÇÕES DE UTILITÁRIO ====
def log(doc, msg):
    print(msg)
    doc.add_paragraph(msg)



dias_para_exumar = int(faker.random.choice(['365', '730', '1095', '1460', '1825']))

def gerar_datas_e_horas_viagem(max_dias_ate_saida=30, max_duracao_viagem=10):
    hoje = datetime.today()
    
    # Gera a data de saída
    dias_ate_saida = random.randint(0, max_dias_ate_saida)
    data_saida = hoje + timedelta(days=dias_ate_saida)

    # Gera a hora de saída aleatória entre 00:00 e 23:59
    hora_saida = datetime(
        year=data_saida.year,
        month=data_saida.month,
        day=data_saida.day,
        hour=random.randint(0, 23),
        minute=random.randint(0, 59)
    )

    # Duração da viagem (em dias)
    duracao_dias = random.randint(1, max_duracao_viagem)

    # Hora de retorno aleatória depois da hora de saída
    hora_retorno = hora_saida + timedelta(
        days=duracao_dias,
        hours=random.randint(0, 5),     # até 5 horas extras de viagem
        minutes=random.randint(0, 59)
    )

    data_saida_str = hora_saida.strftime('%d/%m/%Y')
    hora_saida_str = hora_saida.strftime('%H:%M')

    data_retorno_str = hora_retorno.strftime('%d/%m/%Y')
    hora_retorno_str = hora_retorno.strftime('%H:%M')

    return data_saida_str, hora_saida_str, data_retorno_str, hora_retorno_str

data_saida, hora_saida, data_retorno, hora_retorno = gerar_datas_e_horas_viagem()



def gerar_kms():
    km_inicial =  random.randint(100, 1000)  # Gera um valor aleatório entre 100 e 1000 km
    km_final = km_inicial + random.randint(100, 1000)
    km_percorridos = km_final - km_inicial     
    return km_inicial, km_final, km_percorridos

km_inicial, km_final, km_percorridos = gerar_kms()





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
    nome_arquivo = f"relatorio_viagens_cenario_3_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"
    doc.save(nome_arquivo)
    log(doc, f"📄 Relatório salvo como: {nome_arquivo}")
    subprocess.run(["start", "winword", nome_arquivo], shell=True)
    driver.quit()



def click_element_safely(driver, wait, selector, by=By.CSS_SELECTOR, timeout=10):
    """Clica em um elemento de forma segura, tentando diferentes métodos"""
    try:
        element = wait.until(EC.presence_of_element_located((by, selector)))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        time.sleep(0.5)
        
        element = wait.until(EC.element_to_be_clickable((by, selector)))
        
        try:
            element.click()
            return True
        except:
            try:
                ActionChains(driver).move_to_element(element).click().perform()
                return True
            except:
                driver.execute_script("arguments[0].click();", element)
                return True
                
    except Exception as e:
        print(f"Erro ao clicar no elemento {selector}: {e}")
        return False

def abrir_modal_e_selecionar(btn_selector, pesquisa_selector, termo_pesquisa, btn_pesquisar_selector, resultado_xpath):
    def acao():
        wait = WebDriverWait(driver, 20)
        
        if not click_element_safely(driver, wait, btn_selector):
            raise Exception("Não foi possível abrir o modal")
        
        time.sleep(1)
        
        campo_pesquisa = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, pesquisa_selector)))
        campo_pesquisa.clear()
        campo_pesquisa.send_keys(termo_pesquisa)
        
        if not click_element_safely(driver, wait, btn_pesquisar_selector):
            raise Exception("Não foi possível clicar no botão pesquisar")
        
        time.sleep(2)
        
        wait.until(EC.presence_of_element_located((By.XPATH, resultado_xpath)))
        wait.until(EC.element_to_be_clickable((By.XPATH, resultado_xpath)))
        
        resultado = driver.find_element(By.XPATH, resultado_xpath)
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", resultado)
        time.sleep(0.5)
        
        if not click_element_safely(driver, wait, resultado_xpath, By.XPATH):
            raise Exception("Não foi possível selecionar o resultado")
    
    return acao


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


def preencher_campo_com_retry(driver, wait, seletor, valor, max_tentativas=3):
    """Tenta preencher o campo com diferentes métodos até conseguir"""
    for tentativa in range(max_tentativas):
        try:
            campo = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, seletor)))
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", campo)
            time.sleep(0.5)
            
            if tentativa == 0:
                campo.click()
                campo.clear()
                campo.send_keys(valor)
                campo.send_keys(Keys.TAB)
            elif tentativa == 1:
                ActionChains(driver).move_to_element(campo).click().perform()
                time.sleep(0.2)
                ActionChains(driver).key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
                ActionChains(driver).send_keys(valor).perform()
                ActionChains(driver).send_keys(Keys.TAB).perform()
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
            valor_atual = campo.get_attribute('value')
            if valor_atual == str(valor):
                return True
                
        except Exception as e:
            print(f"Tentativa {tentativa + 1} falhou: {e}")
            time.sleep(1)
    
    return False

def preencher_campo_data_xpath(xpath, valor):
    def acao():
        campo = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        campo.send_keys(valor)
        driver.execute_script("arguments[0].value = arguments[1];", campo, valor)
        campo.send_keys(Keys.TAB)
        time.sleep(0.2)
    return acao


def preencher_campo_data(selector, valor):
    def acao():
        campo = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
        campo.click()
        campo.clear()
        campo.send_keys(valor)
        time.sleep(0.2)
    return acao

def selecionar_opcao(selector, texto):
    def acao():
        select_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
        Select(select_element).select_by_visible_text(texto)
    return acao

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

    safe_action(doc, "Abrindo menu Viagens", lambda: (
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.F2),
        time.sleep(1),
        wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Busque um cadastro']"))).send_keys("Viagens", Keys.ENTER)
    ))

    safe_action(doc, "Clicando em Cadastrar", lambda: (
        time.sleep(5),
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#fmod_10089 > div.wdTelas > div.telaInicial.clearfix.overflow.overflowY > ul > li:nth-child(1) > a > span"))).click()
    ))



    safe_action(doc, "Selecionando Motorista", abrir_modal_e_selecionar(
        "#fmod_10089 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroViagem > div.catWrapper > div > div.cat_categoriaDadosExame.categoriaHolder > div > div > div > div:nth-child(2) > div > a",
        "body > div.modalHolder > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div.formCol.divPesquisa > input",
        "CRISPIM MALAFAIA",
        "body > div.modalHolder > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div:nth-child(3) > a",
        "//td[contains(text(), 'CRISPIM MALAFAIA')]"
    ))

    safe_action(doc, "Selecionando Veículo", abrir_modal_e_selecionar(
        "#fmod_10089 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroViagem > div.catWrapper > div > div.cat_categoriaDadosExame.categoriaHolder > div > div > div > div:nth-child(3) > div > a",
        "body > div.modalHolder > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div.formCol.divPesquisa > div:nth-child(1) > input",
        "TESTE VEÍCULO SELENIUM AUTOMATIZADO",
        "body > div.modalHolder > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div:nth-child(3) > a",
        "//td[contains(text(), 'TESTE VEÍCULO SELENIUM AUTOMATIZADO')]"
    ))


    safe_action(doc, "Selecionando Situação", selecionar_opcao(
        "#fmod_10089 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroViagem > div.catWrapper > div > div.cat_categoriaDadosExame.categoriaHolder > div > div > div > div:nth-child(4) > select",
        "Pendente"
    ))

    safe_action(doc, "Preenchendo Data Saída", preencher_campo_data_xpath(
        "//input[contains(@class, 'hasDatepicker dataSaida mandatory')]",
        data_saida
    ))


    safe_action(doc, "Preenchendo Horário Saída", lambda: 
        preencher_campo_com_retry(
            driver, wait,
            "#fmod_10089 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroViagem > div.catWrapper > div > div.cat_categoriaDadosExame.categoriaHolder > div > div > div > div:nth-child(6) > input",
            hora_saida
        )
    )

    safe_action(doc, "Preenchendo Data Retorno", preencher_campo_data_xpath(
        "//input[contains(@class, 'hasDatepicker dataRetorno')]",
        data_retorno
    ))

    safe_action(doc, "Preenchendo Horário Retorno", lambda: 
        preencher_campo_com_retry(
            driver, wait,
            "#fmod_10089 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroViagem > div.catWrapper > div > div.cat_categoriaDadosExame.categoriaHolder > div > div > div > div:nth-child(8) > input",
            hora_retorno
        )
    )

    safe_action(doc, "Selecionando Tipo Cliente", selecionar_opcao(
        "#fmod_10089 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroViagem > div.catWrapper > div > div.cat_categoriaDadosExame.categoriaHolder > div > div > div > div:nth-child(9) > select",
        "Particular"
    ))

    safe_action(doc, "Selecionando Cliente", abrir_modal_e_selecionar(
        "#fmod_10089 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroViagem > div.catWrapper > div > div.cat_categoriaDadosExame.categoriaHolder > div > div > div > div:nth-child(10) > div > a",
        "#txtPesquisa",
        "SR. GAEL COSTELA",
        "body > div.modalHolder > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div:nth-child(2) > a",
        "//td[contains(text(), 'SR. GAEL COSTELA')]"
    ))



    safe_action(doc, "Acessando aba Rotas", lambda: (
        wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Rotas"))).click(),
        time.sleep(1)
    ))

    safe_action(doc, "Preenchendo CEP de Origem", lambda: 
        preencher_campo_com_retry(
            driver, wait,
            "#fmod_10089 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroViagem > div.catWrapper > div > div.cat_categoriaRotas.categoriaHolder > div.groupHolder.clearfix.grupo_grupoRotas > div.group_grupoRotas.clearfix.grupoHolder.lista > div:nth-child(7) > div:nth-child(1) > div > input",
            "15081115"
        )
    )

    safe_action(doc, "Pesquisando Endereço", lambda: 
        wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            "#fmod_10089 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroViagem > div.catWrapper > div > div.cat_categoriaRotas.categoriaHolder > div.groupHolder.clearfix.grupo_grupoRotas > div.group_grupoRotas.clearfix.grupoHolder.lista > div:nth-child(7) > div:nth-child(1) > div > a"
        ))).click()
    )


    safe_action(doc, "Preenchendo Número", lambda: 
        preencher_campo_com_retry(
            driver, wait,
            "#fmod_10089 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroViagem > div.catWrapper > div > div.cat_categoriaRotas.categoriaHolder > div.groupHolder.clearfix.grupo_grupoRotas > div.group_grupoRotas.clearfix.grupoHolder.lista > div:nth-child(7) > div:nth-child(4) > input",
            "1735"
        )
    )



    safe_action(doc, "Preenchendo CEP de Destino", lambda: (
        driver.execute_script("""
            document.querySelector("#fmod_10089 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroViagem > div.catWrapper > div > div.cat_categoriaRotas.categoriaHolder > div.groupHolder.clearfix.grupo_grupoRotas > div.group_grupoRotas.clearfix.grupoHolder.lista > div:nth-child(9) > div:nth-child(1) > div > input").scrollIntoView({behavior: 'smooth', block: 'center'});
        """),
        preencher_campo_com_retry(
            driver, wait,
            "#fmod_10089 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroViagem > div.catWrapper > div > div.cat_categoriaRotas.categoriaHolder > div.groupHolder.clearfix.grupo_grupoRotas > div.group_grupoRotas.clearfix.grupoHolder.lista > div:nth-child(9) > div:nth-child(1) > div > input",
            "15081260"
        )
    ))


    safe_action(doc, "Pesquisando Endereço", lambda: 
        wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            "#fmod_10089 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroViagem > div.catWrapper > div > div.cat_categoriaRotas.categoriaHolder > div.groupHolder.clearfix.grupo_grupoRotas > div.group_grupoRotas.clearfix.grupoHolder.lista > div:nth-child(9) > div:nth-child(1) > div > a"
        ))).click()
    )


    safe_action(doc, "Rolando até o campo Número", lambda: (
        driver.execute_script("""
            document.querySelector("#fmod_10089 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroViagem > div.catWrapper > div > div.cat_categoriaRotas.categoriaHolder > div.groupHolder.clearfix.grupo_grupoRotas > div.group_grupoRotas.clearfix.grupoHolder.lista > div:nth-child(9) > div:nth-child(4) > input").scrollIntoView({behavior: 'smooth', block: 'center'});
        """),))

    safe_action(doc, "Preenchendo Número", lambda: 
        preencher_campo_com_retry(
            driver, wait,
            "#fmod_10089 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroViagem > div.catWrapper > div > div.cat_categoriaRotas.categoriaHolder > div.groupHolder.clearfix.grupo_grupoRotas > div.group_grupoRotas.clearfix.grupoHolder.lista > div:nth-child(9) > div:nth-child(4) > input",
            "85"
        )
    )




    safe_action(doc, "Rolando até o botão 'Adicionar'", lambda: (
        driver.execute_script("""
            document.querySelector("#fmod_10089 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroViagem > div.catWrapper > div > div.cat_categoriaRotas.categoriaHolder > div.groupHolder.clearfix.grupo_grupoRotas > div.btnListHolder > a.btAddGroup").scrollIntoView({behavior: 'smooth', block: 'center'});
        """),))


    safe_action(doc, "Adicionando Rota", lambda: 
        wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            "#fmod_10089 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroViagem > div.catWrapper > div > div.cat_categoriaRotas.categoriaHolder > div.groupHolder.clearfix.grupo_grupoRotas > div.btnListHolder > a.btAddGroup"
        ))).click()
    )

    time.sleep(5)

    safe_action(doc, "Salvando cadastro", lambda: driver.find_element(
        By.CSS_SELECTOR, "#fmod_10089 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroViagem > div.btnHolder > a.btModel.btGray.btsave"
    ).click())


    safe_action(doc, "Recusando o Cadastro da OS", lambda: (
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#BtNo"))).click()
    ))



    safe_action(doc, "Fechando modal após salvamento", lambda: wait.until(EC.element_to_be_clickable((
        By.CSS_SELECTOR, "#fmod_10089 > div.wdTop.ui-draggable-handle > div.wdClose > a"
        ))
    ).click())



    encontrar_mensagem_alerta()

except Exception as e:
    log(doc, f"❌ ERRO FATAL: {e}")
    take_screenshot(driver, doc, "erro_fatal")

finally:

    log(doc, "✅ Teste concluído com sucesso.")

    finalizar_relatorio()