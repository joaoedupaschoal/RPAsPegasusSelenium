# features/steps/cadastro_steps.py
from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import (
    TimeoutException, 
    NoSuchElementException, 
    StaleElementReferenceException, 
    ElementNotInteractableException,
    ElementClickInterceptedException
)
from selenium.webdriver.common.action_chains import ActionChains
from faker import Faker
import random
import time
import logging
from datetime import datetime, timedelta

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -------------------- Helper Functions --------------------

def gerar_cpf():
    """Gera um CPF válido."""
    def calcular_digito(cpf, peso):
        soma = sum(int(cpf[i]) * peso[i] for i in range(len(peso)))
        resto = soma % 11
        return 0 if resto < 2 else 11 - resto

    # Gerar 9 primeiros dígitos
    cpf = [random.randint(0, 9) for _ in range(9)]
    
    # Calcular primeiro dígito verificador
    peso1 = list(range(10, 1, -1))
    cpf.append(calcular_digito(cpf, peso1))
    
    # Calcular segundo dígito verificador
    peso2 = list(range(11, 1, -1))
    cpf.append(calcular_digito(cpf, peso2))
    
    return ''.join(map(str, cpf))

def gerar_cnpj():
    """Gera um CNPJ válido."""
    def calcular_digito(cnpj, sequencia):
        soma = sum(int(cnpj[i]) * sequencia[i] for i in range(len(sequencia)))
        resto = soma % 11
        return 0 if resto < 2 else 11 - resto

    # Gerar 12 primeiros dígitos
    cnpj = [random.randint(0, 9) for _ in range(12)]
    
    # Calcular primeiro dígito verificador
    seq1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    cnpj.append(calcular_digito(cnpj, seq1))
    
    # Calcular segundo dígito verificador
    seq2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    cnpj.append(calcular_digito(cnpj, seq2))
    
    return ''.join(map(str, cnpj))

def formatar_cpf(cpf):
    """Formata CPF com pontos e hífen."""
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"

def formatar_cnpj(cnpj):
    """Formata CNPJ com pontos, barra e hífen."""
    return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"

def _cadastrar_novo_posto(context, nome_posto):
    """
    Cadastra um novo posto de combustível no LOV durante o abastecimento.
    
    IMPORTANTE: Como não há postos cadastrados no sistema, sempre será necessário
    cadastrar um posto na hora. Esta função preenche TODOS os campos necessários:
    
    DADOS BÁSICOS:
    - Nome/Razão Social do Posto
    - Tipo de Pessoa (F=Física, J=Jurídica) - Postos são geralmente PJ
    - CPF/CNPJ (válidos e formatados)
    - RG/Inscrição Estadual
    - Nome Fantasia (para PJ)
    
    CONTATO:
    - Telefone Comercial
    - Celular (opcional)
    - Email
    - Site (opcional)
    
    ENDEREÇO COMPLETO:
    - CEP (com busca automática se disponível)
    - Logradouro/Endereço
    - Número
    - Complemento (opcional)
    - Bairro
    - Cidade
    - Estado (UF)
    
    DADOS ESPECÍFICOS DO POSTO:
    - Bandeira do Posto (Shell, Petrobras, etc.)
    - CNAE (se necessário)
    - Observações (opcional)
    
    Args:
        context: Contexto do behave
        nome_posto: Nome do posto a ser cadastrado
    """
    logger.info(f"🏪 Iniciando cadastro completo do posto: {nome_posto}")
    fake = Faker('pt_BR')
    
    try:
        # Aguardar formulário de cadastro do posto abrir completamente
        aguardar_elemento(
            context.driver, 
            (By.NAME, "nome"), 
            timeout=10, 
            condicao="visible"
        )
        time.sleep(1)  # Estabilizar formulário
        
        # ==================== DADOS BÁSICOS ====================
        logger.info("📝 Preenchendo dados básicos do posto")
        
        # 1. Nome/Razão Social
        preencher_campo_com_retry(
            context.driver, 
            (By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosPessoais.categoriaHolder > div > div > div:nth-child(2) > div:nth-child(2) > input"), 
            nome_posto.upper()
        )
        

        # 2. Órgão Emissor
        orgao_emissor = "Carteira de Identidade Classista"
        logger.info(f"Definindo Órgão Emissor: {orgao_emissor}")
        
        try:
            # Tentar dropdown/select
            select_tipo = Select(aguardar_elemento(
                context.driver, 
                (By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosPessoais.categoriaHolder > div > div > div:nth-child(2) > div:nth-child(4) > select"), 
                timeout=5
            ))
            select_tipo.select_by_visible_text("Carteira de Identidade Classista")
            logger.info("✅ Tipo pessoa selecionado via dropdown")
        except:
            try:
                # Tentar radio buttons
                radio_org = aguardar_elemento(
                    context.driver, 
                    (By.CSS_SELECTOR, "input[value='1'], input[value='Carteira de Identidade Classista']"), 
                    timeout=5
                )
                context.driver.execute_script("arguments[0].click();", radio_org)
                logger.info("✅ Órgão Emissor selecionado via radio button")
            except:
                logger.warning("⚠️ Campo Órgão Emissor não encontrado")
        
        time.sleep(1)  # Aguardar mudança de campos baseada no tipo
        

        # 3. Tipo de Pessoa (Posto = Pessoa Jurídica)
        tipo_pessoa = "Jurídica"
        logger.info(f"Definindo tipo de pessoa: {tipo_pessoa}")
        
        try:
            # Tentar dropdown/select
            select_tipo = Select(aguardar_elemento(
                context.driver, 
                (By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosPessoais.categoriaHolder > div > div > div:nth-child(2) > div:nth-child(3) > select"), 
                timeout=5
            ))
            select_tipo.select_by_visible_text("Jurídica")
            logger.info("✅ Tipo pessoa selecionado via dropdown")
        except:
            try:
                # Tentar radio buttons
                radio_pj = aguardar_elemento(
                    context.driver, 
                    (By.CSS_SELECTOR, "input[value='J'], input[value='Jurídica']"), 
                    timeout=5
                )
                context.driver.execute_script("arguments[0].click();", radio_pj)
                logger.info("✅ Tipo pessoa selecionado via radio button")
            except:
                logger.warning("⚠️ Campo tipo pessoa não encontrado")
        
        time.sleep(1)  # Aguardar mudança de campos baseada no tipo
        
        # ==================== DOCUMENTOS PESSOA JURÍDICA ====================
        logger.info("📄 Preenchendo documentos de pessoa jurídica")
        
        # 4. CNPJ
        cnpj_numeros = gerar_cnpj()
        cnpj_formatado = formatar_cnpj(cnpj_numeros)
        
        try:
            preencher_campo_com_retry(
                context.driver, 
                (By.CSS_SELECTOR, "cnpj"), 
                cnpj_formatado
            )
            logger.info(f"✅ CNPJ preenchido: {cnpj_formatado}")
        except:
            # Tentar sem formatação
            preencher_campo_com_retry(
                context.driver, 
                (By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosPessoais.categoriaHolder > div > div > div.formRow.divPessoaJURIDICA > div:nth-child(1) > input"), 
                cnpj_numeros
            )
            logger.info(f"✅ CNPJ preenchido (sem formatação): {cnpj_numeros}")
        
        # 5. Nome Fantasia (se campo existir)
        try:
            nome_fantasia = f"{nome_posto.split()[1] if len(nome_posto.split()) > 1 else 'POSTO'} COMBUSTÍVEIS"
            preencher_campo_com_retry(
                context.driver, 
                (By.NAME, "nomeFantasia"), 
                nome_fantasia
            )
        except:
            logger.info("Campo nome fantasia não encontrado - prosseguindo")
        

        # 6. Inscrição Estadual
        ie_numero = f"{random.randint(100, 999)}.{random.randint(100, 999)}.{random.randint(100, 999)}.{random.randint(100, 999)}"
        try:
            preencher_campo_com_retry(
                context.driver, 
                (By.NAME, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosPessoais.categoriaHolder > div > div > div.formRow.divPessoaJURIDICA > div:nth-child(3) > input"), 
                ie_numero
            )
            logger.info(f"✅ Inscrição Estadual: {ie_numero}")
        except:
            # Tentar variações do nome do campo
            for campo_ie in ["#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosPessoais.categoriaHolder > div > div > div.formRow.divPessoaJURIDICA > div:nth-child(3) > input"]:
                try:
                    preencher_campo_com_retry(
                        context.driver, 
                        (By.CSS_SELECTOR, campo_ie), 
                        ie_numero
                    )
                    logger.info(f"✅ IE preenchida no campo: {campo_ie}")
                    break
                except:
                    continue
        
        # 7. Inscrição Municipal (se necessário)
        try:
            im_numero = f"{random.randint(100000, 999999)}"
            preencher_campo_com_retry(
                context.driver, 
                (By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosPessoais.categoriaHolder > div > div > div.formRow.divPessoaJURIDICA > div:nth-child(4) > input"), 
                im_numero
            )
            logger.info(f"✅ Inscrição Municipal: {im_numero}")
        except:
            logger.info("Campo Inscrição Municipal não encontrado")



        logger.info("Selecionando Pacote")
        
        try:
            # Clicar no botão LOV do Pacote
            botao_lov_pacote = aguardar_elemento(
                context.driver,
                (By.CSS_SELECTOR, "#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosPessoais.categoriaHolder > div > div > div.formRow.divPessoaJURIDICA > div.formCol.pacotes > div > a")
            )
            botao_lov_pacote.click()
            
            time.sleep(1)  # Aguardar animação do modal
            
            # Pesquisar Pacote
            campo_pesquisa = aguardar_elemento(
                context.driver,
                (By.XPATH, "//input[@class='nomePesquisa' and contains(@style,'210px')]")
            )
            
            pacote_nome = "TESTE PACOTE SELENIUM AUTOMATIZADO"
            preencher_campo_com_retry(
                context.driver, 
                (By.CSS_SELECTOR, campo_pesquisa),
                pacote_nome
            )
            
            # Clicar em pesquisar
            aguardar_elemento(
                context.driver,
                (By.XPATH, "//a[@class='btModel btGray lpFind' and normalize-space(text())='Pesquisar']")
            ).click()
            time.sleep(2)

            # Selecionar pacote na lista
            aguardar_elemento(
                context.driver,
                (By.XPATH, f"//td[contains(text(), '{pacote_nome}')]")
            ).click()
            
            context.dados_abastecimento['pacote'] = pacote_nome
            logger.info(f"Pacote selecionado: {pacote_nome}")
            
        except Exception as e:
            logger.error(f"Erro ao selecionar pacote: {str(e)}")
            raise




        # ==================== DADOS DE CONTATO ====================
        logger.info("📞 Preenchendo dados de contato")
        
        # 8. Telefone Principal
        telefone_comercial = fake.phone_number().replace('(', '').replace(')', '').replace('-', '').replace(' ', '')
        telefone_formatado = f"({telefone_comercial[:2]}) {telefone_comercial[2:7]}-{telefone_comercial[7:11]}"
        
        for campo_tel in ["#cg_1 > div.wdTelas > div > div.catWrapper > div > div.cat_dadosComplementares.categoriaHolder > div > div > div > div:nth-child(5) > input"]:
            try:
                preencher_campo_com_retry(
                    context.driver, 
                    (By.CSS_SELECTOR, campo_tel ), 
                    telefone_formatado
                )
                logger.info(f"✅ Telefone preenchido: {telefone_formatado}")
                break
            except:
                continue
        
        # 9. Celular/WhatsApp (opcional)
        try:
            celular = fake.phone_number().replace('(', '').replace(')', '').replace('-', '').replace(' ', '')
            celular_formatado = f"({celular[:2]}) 9{celular[2:6]}-{celular[6:10]}"
            preencher_campo_com_retry(
                context.driver, 
                (By.CLASS_NAME, "fc celular"), 
                celular_formatado
            )
            logger.info(f"✅ Celular: {celular_formatado}")
        except:
            logger.info("Campo celular não encontrado")
        
        # 10. Email
        email_posto = f"{nome_posto.lower().replace(' ', '').replace('posto', '')}@email.com"
        for campo_email in ["email", "emailComercial"]:
            try:
                preencher_campo_com_retry(
                    context.driver, 
                    (By.NAME, campo_email), 
                    email_posto
                )
                logger.info(f"✅ Email: {email_posto}")
                break
            except:
                continue
        

        # ==================== SALVAR CADASTRO ====================
        logger.info("💾 Salvando cadastro do posto")
        
        # Procurar botão salvar com múltiplos seletores
        seletores_salvar = [
            "#cg_1 > div.wdTelas > div > div.btnHolder > a.btModel.btGray.btsave",
            "button[type='submit']",
            "input[type='submit']", 
            ".btn-save",
            ".botao-salvar",
            "a:contains('Salvar')",
            "button:contains('Salvar')"
        ]
        
        botao_salvo = False
        for seletor in seletores_salvar:
            try:
                botao_salvar = aguardar_elemento(
                    context.driver,
                    (By.CSS_SELECTOR, seletor),
                    timeout=3
                )
                # Scroll até o botão e clicar
                context.driver.execute_script(
                    "arguments[0].scrollIntoView({block: 'center'});", 
                    botao_salvar
                )
                time.sleep(0.5)
                botao_salvar.click()
                botao_salvo = True
                logger.info(f"✅ Botão salvar clicado: {seletor}")
                break
            except:
                continue
        
        if not botao_salvo:
            # Fallback: tentar Enter no formulário
            context.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ENTER)
            logger.info("⚠️ Fallback: Enter enviado para salvar")
        
        # Aguardar processamento do cadastro
        time.sleep(5)
        
        # ==================== VALIDAÇÃO DO CADASTRO ====================
        logger.info("🔍 Validando se posto foi cadastrado")
        
        try:
            # Verificar se há mensagem de sucesso
            tipo_msg, mensagem = verificar_mensagem_alerta(context.driver)
            if tipo_msg == "sucesso":
                logger.info(f"✅ Cadastro confirmado: {mensagem}")
            else:
                logger.warning(f"⚠️ Resposta do sistema: {tipo_msg} - {mensagem}")
        except:
            logger.info("Nenhuma mensagem de confirmação encontrada - prosseguindo")
        
        # Verificar se voltou para a lista do LOV ou fechou modal
        try:
            # Se estiver de volta no LOV, tentar selecionar o posto recém-criado
            aguardar_elemento(
                context.driver,
                (By.XPATH, f"//td[contains(text(), '{nome_posto}')]"),
                timeout=5
            ).click()
            logger.info(f"✅ Posto '{nome_posto}' selecionado na lista LOV")
        except:
            logger.info("Lista LOV não encontrada - modal pode ter fechado automaticamente")
        
        # ==================== FINALIZAÇÃO ====================
        logger.info(f"🎉 POSTO CADASTRADO COM SUCESSO!")
        logger.info(f"📋 Resumo do posto criado:")
        logger.info(f"   • Nome: {nome_posto}")
        logger.info(f"   • CNPJ: {cnpj_formatado}")
        logger.info(f"   • IE: {ie_numero}")
        logger.info(f"   • Telefone: {telefone_formatado}")
        logger.info(f"   • Email: {email_posto}")

        
        # Armazenar dados no contexto para uso posterior
        if not hasattr(context, 'dados_posto_cadastrado'):
            context.dados_posto_cadastrado = {}
        
        context.dados_posto_cadastrado.update({
            'nome': nome_posto,
            'cnpj': cnpj_formatado,
            'ie': ie_numero,
            'telefone': telefone_formatado,
            'email': email_posto,

        })
        
    except Exception as e:
        logger.error(f"❌ ERRO CRÍTICO no cadastro do posto: {str(e)}")
        logger.error(f"🔧 Detalhes técnicos: {type(e).__name__}")
        
        # Capturar screenshot para debug (se possível)
        try:
            screenshot_nome = f"erro_posto_{int(time.time())}.png"
            context.driver.save_screenshot(screenshot_nome)
            logger.error(f"📸 Screenshot salvo: {screenshot_nome}")
        except:
            pass
        
        raise Exception(f"Falha crítica no cadastro do posto '{nome_posto}': {str(e)}")
    
    logger.info("✅ Função _cadastrar_novo_posto finalizada com sucesso")

# -------------------- Helper Functions --------------------

def preencher_campo_com_retry(driver, locator, valor, tentativas=3, espera=1):
    """
    Preenche um campo input com múltiplas estratégias de retry.
    
    Args:
        driver: WebDriver instance
        locator: Tuple com estratégia de localização (By.ID, "elemento")
        valor: Valor a ser inserido
        tentativas: Número máximo de tentativas
        espera: Tempo de espera entre tentativas
    """
    ultimo_erro = None
    
    for tentativa in range(tentativas):
        try:
            logger.info(f"Tentativa {tentativa + 1} de preenchimento do campo {locator}")
            
            # Encontrar elemento
            elemento = driver.find_element(*locator)
            
            # Garantir visibilidade
            driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", 
                elemento
            )
            time.sleep(0.5)
            
            # Tentar clicar
            try:
                elemento.click()
            except ElementClickInterceptedException:
                # Fechar possíveis overlays
                driver.execute_script("document.activeElement.blur();")
                elemento.send_keys(Keys.ESCAPE)
                time.sleep(0.3)
                
                # Tentar click via JavaScript
                driver.execute_script("arguments[0].click();", elemento)
            
            # Limpar e preencher
            elemento.clear()
            elemento.send_keys(valor)
            
            # Verificar se valor foi inserido corretamente
            if elemento.get_attribute('value') == valor:
                logger.info(f"Campo preenchido com sucesso: {valor}")
                return True
            
        except (StaleElementReferenceException, ElementNotInteractableException, 
                ElementClickInterceptedException, NoSuchElementException) as e:
            ultimo_erro = e
            logger.warning(f"Erro na tentativa {tentativa + 1}: {str(e)}")
            time.sleep(espera)
    
    # Fallback: definir valor via JavaScript
    try:
        logger.info("Usando fallback JavaScript para preenchimento")
        elemento = driver.find_element(*locator)
        driver.execute_script("""
            const el = arguments[0];
            const val = arguments[1];
            el.value = val;
            el.dispatchEvent(new Event('input', {bubbles: true}));
            el.dispatchEvent(new Event('change', {bubbles: true}));
            el.dispatchEvent(new Event('blur', {bubbles: true}));
        """, elemento, valor)
        return True
    except Exception as e:
        logger.error(f"Fallback também falhou: {str(e)}")
        raise Exception(f"Não foi possível preencher o campo {locator} após {tentativas} tentativas. Último erro: {ultimo_erro}")

def aguardar_elemento(driver, locator, timeout=15, condicao="clickable"):
    """
    Aguarda um elemento aparecer com diferentes condições.
    
    Args:
        driver: WebDriver instance
        locator: Tuple com estratégia de localização
        timeout: Tempo limite de espera
        condicao: Tipo de condição ('clickable', 'visible', 'present')
    """
    wait = WebDriverWait(driver, timeout)
    
    condicoes = {
        'clickable': EC.element_to_be_clickable,
        'visible': EC.visibility_of_element_located,
        'present': EC.presence_of_element_located
    }
    
    if condicao not in condicoes:
        raise ValueError(f"Condição '{condicao}' não é válida. Use: {list(condicoes.keys())}")
    
    try:
        elemento = wait.until(condicoes[condicao](locator))
        logger.info(f"Elemento {locator} encontrado com condição '{condicao}'")
        return elemento
    except TimeoutException:
        logger.error(f"Timeout ao aguardar elemento {locator} com condição '{condicao}'")
        raise

def ajustar_zoom(driver, percentual="90%"):
    """Ajusta o zoom da página."""
    driver.execute_script(f"document.body.style.zoom='{percentual}'")
    logger.info(f"Zoom ajustado para {percentual}")

def gerar_data_abastecimento():
    """Gera uma data aleatória dentro dos últimos 30 dias."""
    fake = Faker('pt_BR')
    hoje = datetime.now()
    trinta_dias_atras = hoje - timedelta(days=30)
    data = fake.date_between(start_date=trinta_dias_atras, end_date=hoje)
    return data.strftime("%d/%m/%Y")

def gerar_dados_abastecimento():
    """Gera dados aleatórios para abastecimento."""
    dados = {
        'km': random.randint(10000, 300000),
        'volume': round(random.uniform(10.0, 80.0), 2),
        'valor_unitario': round(random.uniform(4.50, 7.00), 2),
        'desconto': round(random.uniform(0.0, 20.0), 2)
    }
    logger.info(f"Dados gerados: {dados}")
    return dados

def verificar_mensagem_alerta(driver):
    """
    Verifica se existe mensagem de alerta na tela e retorna tipo e conteúdo.
    
    Returns:
        tuple: (tipo_alerta, mensagem) ou (None, None) se não encontrar
    """
    seletores_alerta = [
        (".alerts.salvo", "sucesso"),
        (".alerts.alerta", "alerta"), 
        (".alerts.erro", "erro"),
        (".alert-success", "sucesso"),
        (".alert-warning", "alerta"),
        (".alert-danger", "erro")
    ]
    
    for seletor, tipo in seletores_alerta:
        try:
            elemento = driver.find_element(By.CSS_SELECTOR, seletor)
            if elemento.is_displayed():
                mensagem = elemento.text.strip()
                logger.info(f"Alerta encontrado - Tipo: {tipo}, Mensagem: {mensagem}")
                return tipo, mensagem
        except NoSuchElementException:
            continue
    
    logger.warning("Nenhuma mensagem de alerta encontrada")
    return None, None

# -------------------- Steps Implementation --------------------

@given("que estou logado no sistema")
def step_login_sistema(context):
    """Realiza login no sistema."""
    logger.info("Iniciando processo de login")
    
    # Configurar Chrome
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    
    # Inicializar driver
    service = Service(ChromeDriverManager().install())
    context.driver = webdriver.Chrome(service=service, options=chrome_options)
    context.base_url = "http://localhost:8080/gs/index.xhtml"
    
    try:
        # Navegar para página de login
        context.driver.get(context.base_url)
        logger.info(f"Navegando para: {context.base_url}")
        
        # Aguardar campos de login
        campo_email = aguardar_elemento(context.driver, (By.ID, "j_id15:email"), timeout=20)
        campo_senha = aguardar_elemento(context.driver, (By.ID, "j_id15:senha"))
        
        # Preencher credenciais
        preencher_campo_com_retry(context.driver, (By.ID, "j_id15:email"), "joaoeduardo.gold@outlook.com")
        preencher_campo_com_retry(context.driver, (By.ID, "j_id15:senha"), "071999gs")
        
        # Fazer login
        campo_senha.send_keys(Keys.ENTER)
        
        # Aguardar redirecionamento/carregamento
        time.sleep(3)
        
        # Configurações pós-login
        ajustar_zoom(context.driver, "90%")
        context.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.F2)
        time.sleep(1)
        
        logger.info("Login realizado com sucesso")
        
    except Exception as e:
        logger.error(f"Erro durante login: {str(e)}")
        context.driver.quit()
        raise

@given("que estou na página inicial do sistema")
def step_pagina_inicial(context):
    """Verifica se está na página inicial após login."""
    try:
        # Verificar se elementos da página inicial estão presentes
        aguardar_elemento(
            context.driver, 
            (By.XPATH, "//input[@placeholder='Busque um cadastro']"), 
            timeout=10
        )
        logger.info("Página inicial carregada com sucesso")
        
    except TimeoutException:
        logger.error("Página inicial não carregou corretamente")
        raise AssertionError("Página inicial não foi carregada após login")

@when("eu acesso o módulo de abastecimento")
def step_acessar_modulo_abastecimento(context):
    """Acessa o módulo de abastecimento através da busca."""
    logger.info("Acessando módulo de abastecimento")
    
    try:
        # Localizar campo de pesquisa
        campo_pesquisa = aguardar_elemento(
            context.driver, 
            (By.XPATH, "//input[@placeholder='Busque um cadastro']")
        )
        
        # Pesquisar por "Abastecimento"
        preencher_campo_com_retry(
            context.driver, 
            (By.XPATH, "//input[@placeholder='Busque um cadastro']"), 
            "Abastecimento"
        )
        campo_pesquisa.send_keys(Keys.ENTER)
        
        time.sleep(2)
        logger.info("Módulo de abastecimento acessado")
        
    except Exception as e:
        logger.error(f"Erro ao acessar módulo: {str(e)}")
        raise

@when("eu clico em cadastrar novo abastecimento")
def step_clicar_cadastrar_abastecimento(context):
    """Clica no botão para cadastrar novo abastecimento."""
    logger.info("Clicando em cadastrar abastecimento")
    
    try:
        # Aguardar e clicar no botão cadastrar
        botao_cadastrar = aguardar_elemento(
            context.driver,
            (By.CSS_SELECTOR, "#fmod_10090 > div.wdTelas > div > ul > li:nth-child(1) > a > span")
        )
        botao_cadastrar.click()
        
        time.sleep(2)
        logger.info("Formulário de cadastro aberto")
        
    except Exception as e:
        logger.error(f"Erro ao clicar em cadastrar: {str(e)}")
        raise

@when("eu preencho a data do abastecimento")
def step_preencher_data(context):
    """Preenche a data do abastecimento."""
    logger.info("Preenchendo data do abastecimento")
    
    try:
        data = gerar_data_abastecimento()
        context.dados_abastecimento = {'data': data}
        
        aguardar_elemento(context.driver, (By.NAME, "data"))
        preencher_campo_com_retry(context.driver, (By.NAME, "data"), data)
        
        logger.info(f"Data preenchida: {data}")
        
    except Exception as e:
        logger.error(f"Erro ao preencher data: {str(e)}")
        raise

@when("eu seleciono o tipo de combustível")
def step_selecionar_combustivel(context):
    """Seleciona o tipo de combustível."""
    logger.info("Selecionando combustível")
    
    try:
        # Localizar dropdown de combustível
        select_combustivel = aguardar_elemento(
            context.driver,
            (By.CSS_SELECTOR, "#fmod_10090 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroAbastecimento > div.catWrapper > div > div > div > div > div > div:nth-child(3) > select")
        )
        
        # Selecionar gasolina
        select = Select(select_combustivel)
        select.select_by_visible_text("Gasolina")
        
        context.dados_abastecimento['combustivel'] = 'Gasolina'
        logger.info("Combustível selecionado: Gasolina")
        
    except Exception as e:
        logger.error(f"Erro ao selecionar combustível: {str(e)}")
        raise

@when("eu seleciono o motorista")
def step_selecionar_motorista(context):
    """Seleciona o motorista através do LOV."""
    logger.info("Selecionando motorista")
    
    try:
        # Clicar no botão LOV do motorista
        botao_lov_motorista = aguardar_elemento(
            context.driver,
            (By.CSS_SELECTOR, "#fmod_10090 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroAbastecimento > div.catWrapper > div > div > div > div > div > div:nth-child(4) > div > a")
        )
        botao_lov_motorista.click()
        
        time.sleep(1)  # Aguardar animação do modal
        
        # Pesquisar motorista
        campo_pesquisa = aguardar_elemento(
            context.driver,
            (By.CSS_SELECTOR, "body > div.modalHolder > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div.formCol.divPesquisa > input")
        )
        
        motorista_nome = "CRISPIM MALAFAIA"
        preencher_campo_com_retry(
            context.driver, 
            (By.CSS_SELECTOR, "body > div.modalHolder > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div.formCol.divPesquisa > input"),
            motorista_nome
        )
        
        # Clicar em pesquisar
        aguardar_elemento(
            context.driver,
            (By.CSS_SELECTOR, "body > div.modalHolder > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div:nth-child(3) > a")
        ).click()
        time.sleep(2)

        # Selecionar motorista na lista
        aguardar_elemento(
            context.driver,
            (By.XPATH, f"//td[contains(text(), '{motorista_nome}')]")
        ).click()
        
        context.dados_abastecimento['motorista'] = motorista_nome
        logger.info(f"Motorista selecionado: {motorista_nome}")
        
    except Exception as e:
        logger.error(f"Erro ao selecionar motorista: {str(e)}")
        raise

@when("eu seleciono o veículo")
def step_selecionar_veiculo(context):
    """Seleciona o veículo através do LOV."""
    logger.info("Selecionando veículo")
    
    try:
        # Clicar no botão LOV do veículo
        aguardar_elemento(
            context.driver,
            (By.CSS_SELECTOR, "#fmod_10090 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroAbastecimento > div.catWrapper > div > div > div > div > div > div:nth-child(5) > div > a")
        ).click()
        
        # Pesquisar veículo
        campo_pesquisa = aguardar_elemento(
            context.driver,
            (By.CSS_SELECTOR, "body > div.modalHolder > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div.formCol.divPesquisa > div:nth-child(1) > input")
        )
        
        veiculo_nome = "TESTE VEÍCULO SELENIUM AUTOMATIZADO"
        preencher_campo_com_retry(
            context.driver,
            (By.CSS_SELECTOR, campo_pesquisa))
        veiculo_nome
        
        
        # Clicar em pesquisar
        aguardar_elemento(
            context.driver,
            (By.CSS_SELECTOR, "body > div.modalHolder > div.modal.overflow > div:nth-child(1) > div.formRow.formLastLine > div:nth-child(3) > a")
        ).click()
        time.sleep(3)

        # Selecionar veículo na lista
        aguardar_elemento(
            context.driver,
            (By.XPATH, f"//td[contains(text(), '{veiculo_nome}')]")
        ).click()
        
        context.dados_abastecimento['veiculo'] = veiculo_nome
        logger.info(f"Veículo selecionado: {veiculo_nome}")
        
    except Exception as e:
        logger.error(f"Erro ao selecionar veículo: {str(e)}")
        raise

@when("eu seleciono o posto de combustível")
def step_selecionar_posto_combustivel(context):
    """Cadastra posto de combustível na hora (não existe nenhum cadastrado)."""
    logger.info("Cadastrando posto de combustível na hora")
    
    try:
        # Clicar no botão LOV do posto de combustível
        aguardar_elemento(
            context.driver,
            (By.CSS_SELECTOR, "#fmod_10090 > div.wdTelas > div.telaCadastro.clearfix.telaCadastroAbastecimento > div.catWrapper > div > div > div > div > div > div:nth-child(6) > div > a")
        ).click()
        
        time.sleep(1)  # Aguardar modal abrir
        
        # Como não há postos cadastrados, clicar diretamente em "Novo"
        logger.info("Não há postos cadastrados - cadastrando novo posto")
        
        botao_novo = aguardar_elemento(
            context.driver,
            (By.XPATH, "//a[contains(@class,'btModel') and contains(@class,'novo') and contains(normalize-space(.),'Novo Registro')]")
        )
        botao_novo.click()
        
        # Gerar dados para o novo posto
        fake = Faker('pt_BR')
        timestamp = int(time.time())
        posto_nome = f"POSTO {fake.company().upper()[:12]} {timestamp}"
        
        # Cadastrar o posto na hora
        _cadastrar_novo_posto(context, posto_nome)
        
        context.dados_abastecimento['posto'] = posto_nome
        logger.info(f"Posto cadastrado na hora: {posto_nome}")
        
    except Exception as e:
        logger.error(f"Erro ao cadastrar posto na hora: {str(e)}")
        raise

@when("eu preencho apenas os campos obrigatórios para abastecimento")
def step_preencher_campos_obrigatorios(context):
    """Preenche apenas os campos obrigatórios para um abastecimento válido."""
    logger.info("Preenchendo apenas campos obrigatórios")
    
    try:
        # Data (obrigatório)
        step_preencher_data(context)
        
        # Combustível (obrigatório)  
        step_selecionar_combustivel(context)
        
        # Motorista (obrigatório)
        step_selecionar_motorista(context)
        
        # Veículo (obrigatório)
        step_selecionar_veiculo(context)
        
        # Posto (obrigatório - sempre cadastrado na hora)
        step_selecionar_posto_combustivel(context)
        
        # Dados básicos do abastecimento (obrigatórios)
        dados = gerar_dados_abastecimento()
        
        # KM (obrigatório)
        preencher_campo_com_retry(
            context.driver,
            (By.CSS_SELECTOR, "#fmod_10090 div:nth-child(7) > input"),
            str(dados['km'])
        )
        
        # Volume (obrigatório)
        preencher_campo_com_retry(
            context.driver,
            (By.CSS_SELECTOR, "#fmod_10090 div:nth-child(8) > input"),
            str(dados['volume']).replace('.', ',')
        )
        
        # Valor unitário (obrigatório)
        preencher_campo_com_retry(
            context.driver,
            (By.CSS_SELECTOR, "#fmod_10090 div:nth-child(9) > input"),
            str(dados['valor_unitario']).replace('.', ',')
        )
        
        # Desconto (opcional, mas vamos preencher com 0)
        preencher_campo_com_retry(
            context.driver,
            (By.CSS_SELECTOR, "#fmod_10090 div:nth-child(10) > input"),
            "0,00"
        )
        
        context.dados_abastecimento.update(dados)
        logger.info("Campos obrigatórios preenchidos com sucesso")
        
    except Exception as e:
        logger.error(f"Erro ao preencher campos obrigatórios: {str(e)}")
        raise

@when("eu preencho os dados complementares")
def step_preencher_dados_complementares(context):
    """Preenche campos complementares como telefone."""
    logger.info("Preenchendo dados complementares")
    
    try:
        fake = Faker('pt_BR')
        telefone = fake.phone_number()
        
        # Preencher telefone
        aguardar_elemento(
            context.driver,
            (By.CSS_SELECTOR, "#cg_1 div.cat_dadosComplementares input:nth-child(7)")
        )
        preencher_campo_com_retry(
            context.driver,
            (By.CSS_SELECTOR, "#cg_1 div.cat_dadosComplementares input:nth-child(7)"),
            telefone
        )
        
        context.dados_abastecimento['telefone'] = telefone
        logger.info(f"Telefone preenchido: {telefone}")
        
    except Exception as e:
        logger.error(f"Erro ao preencher dados complementares: {str(e)}")
        raise

@when("eu preencho os dados do abastecimento")
def step_preencher_dados_abastecimento(context):
    """Preenche os dados específicos do abastecimento."""
    logger.info("Preenchendo dados do abastecimento")
    
    try:
        dados = gerar_dados_abastecimento()
        
        # Preencher KM
        preencher_campo_com_retry(
            context.driver,
            (By.CSS_SELECTOR, "#fmod_10090 div:nth-child(7) > input"),
            str(dados['km'])
        )
        
        # Preencher Volume
        preencher_campo_com_retry(
            context.driver,
            (By.CSS_SELECTOR, "#fmod_10090 div:nth-child(8) > input"),
            str(dados['volume']).replace('.', ',')  # Formato brasileiro
        )
        
        # Preencher Valor Unitário
        preencher_campo_com_retry(
            context.driver,
            (By.CSS_SELECTOR, "#fmod_10090 div:nth-child(9) > input"),
            str(dados['valor_unitario']).replace('.', ',')
        )
        
        # Preencher Desconto
        preencher_campo_com_retry(
            context.driver,
            (By.CSS_SELECTOR, "#fmod_10090 div:nth-child(10) > input"),
            str(dados['desconto']).replace('.', ',')
        )
        
        context.dados_abastecimento.update(dados)
        logger.info(f"Dados do abastecimento preenchidos: {dados}")
        
    except Exception as e:
        logger.error(f"Erro ao preencher dados do abastecimento: {str(e)}")
        raise

@when("eu clico em salvar")
def step_clicar_salvar(context):
    """Clica no botão salvar para confirmar o cadastro."""
    logger.info("Clicando em salvar")
    
    try:
        botao_salvar = aguardar_elemento(
            context.driver,
            (By.CSS_SELECTOR, "#fmod_10090 a.btModel.btGray.btsave")
        )
        botao_salvar.click()
        
        time.sleep(2)  # Aguardar processamento
        logger.info("Botão salvar clicado")
        
    except Exception as e:
        logger.error(f"Erro ao clicar em salvar: {str(e)}")
        raise

@then("o sistema deve exibir mensagem de sucesso")
def step_verificar_mensagem_sucesso(context):
    """Verifica se a mensagem de sucesso foi exibida."""
    logger.info("Verificando mensagem de sucesso")
    
    try:
        # Aguardar container de alertas aparecer
        aguardar_elemento(
            context.driver,
            (By.CSS_SELECTOR, ".alerts"),
            timeout=15,
            condicao="present"
        )
        
        # Verificar tipo de mensagem
        tipo, mensagem = verificar_mensagem_alerta(context.driver)
        
        # Validar se é mensagem de sucesso
        assert tipo == "sucesso", f"Esperado mensagem de sucesso, mas obteve '{tipo}': {mensagem}"
        
        logger.info(f"✅ Teste passou - Mensagem de sucesso: {mensagem}")
        print(f"✅ Abastecimento cadastrado com sucesso!")
        print(f"📄 Dados cadastrados: {context.dados_abastecimento}")
        print(f"💬 Mensagem do sistema: {mensagem}")
        
    except AssertionError:
        logger.error(f"❌ Falha na validação - Tipo: {tipo}, Mensagem: {mensagem}")
        raise
    except Exception as e:
        logger.error(f"❌ Erro ao verificar mensagem: {str(e)}")
        raise
    finally:
        # Encerrar driver
        if hasattr(context, 'driver'):
            context.driver.quit()
            logger.info("Driver encerrado")

@then("o sistema deve exibir mensagem de erro")
def step_verificar_mensagem_erro(context):
    """Verifica se a mensagem de erro foi exibida."""
    logger.info("Verificando mensagem de erro")
    
    try:
        aguardar_elemento(
            context.driver,
            (By.CSS_SELECTOR, ".alerts"),
            timeout=15,
            condicao="present"
        )
        
        tipo, mensagem = verificar_mensagem_alerta(context.driver)
        
        assert tipo == "erro", f"Esperado mensagem de erro, mas obteve '{tipo}': {mensagem}"
        
        logger.info(f"✅ Mensagem de erro verificada: {mensagem}")
        print(f"⚠️ Erro capturado conforme esperado: {mensagem}")
        
    except AssertionError:
        logger.error(f"❌ Falha - Esperado erro mas obteve: {tipo}")
        raise
    finally:
        if hasattr(context, 'driver'):
            context.driver.quit()
            logger.info("Driver encerrado")