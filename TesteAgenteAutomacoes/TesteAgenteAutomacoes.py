# TesteAgenteAutomacoes.py — Versão consolidada e completa
# -----------------------------------------------------------------
# Gera relatórios DOCX ao final dos testes
# Suporta execução em modo .exe (PyInstaller), usando Python do sistema ou runpy
# -----------------------------------------------------------------

# ===================== IMPORTS =====================
import os, sys, time, threading, subprocess, contextlib, runpy, shutil, traceback, re
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional

# ===================== BOAS-VINDAS =====================
def mostrar_boas_vindas():
    print("Carregando... Estamos preparando tudo pra você.")
    try:
        sys.stdout.flush()
    except Exception:
        pass
    time.sleep(0.8)

mostrar_boas_vindas()

# ===================== WORKSPACE / SAÍDA =====================
RUN_ID = datetime.now().strftime("%Y%m%d_%H%M%S_") + os.urandom(3).hex()
DESKTOP = Path(os.path.expanduser("~/Desktop"))
OUT_BASE = DESKTOP / "AutomacoesPegasus" / f"RUN_{RUN_ID}"

DIR_REPORTS = OUT_BASE / "reports"
DIR_SHOTS   = OUT_BASE / "screenshots"
DIR_LOGS    = OUT_BASE / "logs"
DIR_DLS     = OUT_BASE / "downloads"
for d in (DIR_REPORTS, DIR_SHOTS, DIR_LOGS, DIR_DLS):
    d.mkdir(parents=True, exist_ok=True)
print(f"[RUN] Workspace: {OUT_BASE}")

# ===================== QA REPORTER =====================
try:
    from qa_reporter import QAReporter
except Exception as e:
    print("[ERRO] qa_reporter.py não encontrado ou inválido: ", e)
    sys.exit(1)

reporter: Optional[QAReporter] = QAReporter(reports_dir=DIR_REPORTS)
reporter.start()
_report_meta = {
    "ambiente": os.getenv("QA_AMBIENTE", "Homologação"),
    "versao":   os.getenv("QA_VERSAO", "-"),
}

# ===================== BASE DE CENÁRIOS =====================
BASE_SCRIPTS = Path(__file__).resolve().parent / "cenariostestespegasus"

SCRIPTS: Dict[str, Dict[str, Dict[str, object]]] = {
    "cadastros": {
        "adicionais": {
            "1": {
                "label": "Cenários dos cadastros de Abastecimento",
                "scenarios": {
                    "1": {
                        "label": 'Cenário 1: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de um novo Abastecimento.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosAbastecimento" / "cadastrodeabastecimento1ºcenario.py",
                    },
                    "2": {
                        "label": 'Cenário 2: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de um novo Abastecimento.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosAbastecimento" / "cadastrodeabastecimento2ºcenario.py",
                    },
                    "3": {
                        "label": 'Cenário 3: Nesse teste, o robô preencherá APENAS os campos obrigatórios e salvará o cadastro de um novo Abastecimento.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosAbastecimento" / "cadastrodeabastecimento3ºcenario.py",
                    },
                    "4": {
                        "label": 'Cenário : Nesse teste, o robô preencherá os campos NÃO obrigatórios e salvará o cadastro de um novo Abastecimento, com a finalidade de validar o disparo de mensagens no sistema.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosAbastecimento" / "cadastrodeabastecimento4ºcenario.py",
                    },
                }
            },
            "2": {
                "label": "Cenários dos cadastros de Áreas",
                "scenarios": {
                    "1": {
                        "label": 'Cenário 1: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de uma nova Área.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosÁreas" / "cadastrodeareas1ºcenario.py",
                    },
                    "2": {
                        "label": 'Cenário 2: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de uma nova Área.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosÁreas" / "cadastrodeareas2ºcenario.py",
                    },
                    "3": {
                        "label": 'Cenário 3: Nesse teste, o robô preencherá os campos NÃO obrigatórios e salvará o cadastro de uma nova Área, com a finalidade de validar o disparo de mensagens no sistema.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosÁreas" / "cadastrodeareas3ºcenario.py",
                    },
                }
            },
            "3": {
                "label": "Cenários dos cadastros de Atendentes",
                "scenarios": {
                    "1": {
                        "label": 'Cenário 1: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de um novo Atendente.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosAtendentes" / "cadastrodeatendentes1ºcenario.py",
                    },
                    "2": {
                        "label": 'Cenário 2: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de um novo Atendente.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosAtendentes" / "cadastrodeatendentes2ºcenario.py",
                    },
                    "3": {
                        "label": 'Cenário 3: Nesse teste, o robô preencherá os campos NÃO obrigatórios e salvará o cadastro de um novo Atendente, com a finalidade de validar o disparo de mensagens no sistema.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosAtendentes" / "cadastrodeatendentes3ºcenario.py",
                    },
                }
            },
            "4": {
                "label": "Cenários dos cadastros de Capelas",
                "scenarios": {
                    "1": {
                        "label": 'Cenário 1: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de uma nova Capela.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosCapelas" / "cadastrodecapelas1ºcenario.py",
                    },
                    "2": {
                        "label": 'Cenário 2: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de uma nova Capela.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosCapelas" / "cadastrodecapelas2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 3: Nesse teste, o robô preencherá APENAS os dados obrigatórios e salvará o cadastro de uma nova Capela.",
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosCapelas" / "cadastrodecapelas3ºcenario.py",
                    },
                    "4": {
                        "label": "Cenário 4: Nesse teste, o robô preencherá todos os dados NÃO obrigatórios e salvará o cadastro de uma nova Capela, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosCapelas" / "cadastrodecapelas4ºcenario.py",
                    },
                }
            },
            "5": {
                "label": "Cenários dos cadastros de Carteira",
                "scenarios": {
                    "1": {
                        "label": 'Cenário 1: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de uma nova Carteira.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosCarteira" / "cadastrodecarteira1ºcenario.py",
                    },
                    "2": {
                        "label": 'Cenário 2: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de uma nova Carteira.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosCarteira" / "cadastrodecarteira2ºcenario.py",
                    },
                    "3": {
                        "label": 'Cenário 3: Nesse teste, o robô preencherá os campos NÃO obrigatórios e salvará o cadastro de uma nova Carteira, com a finalidade de validar o disparo de mensagens no sistema.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosCarteira" / "cadastrodecarteira3ºcenario.py",
                    },
                }
            },
        
            "6": {
                "label": "Cenários dos cadastros de Cartões",
                "scenarios": {
                    "1": {
                        "label": 'Cenário 1: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de um novo Cartão.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosCartões" / "cadastrodecartões1ºcenario.py",
                    },
                    "2": {
                        "label": 'Cenário 2: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de um novo Cartão.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosCartões" / "cadastrodecartões2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 3: Nesse teste, o robô preencherá APENAS os dados obrigatórios e salvará o cadastro de um novo Cartão.",
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosCartões" / "cadastrodecartões3ºcenario.py",
                    },
                    "4": {
                        "label": "Cenário 4: Nesse teste, o robô preencherá todos os dados NÃO obrigatórios e salvará o cadastro de um novo Cartão, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosCartões" / "cadastrodecartões4ºcenario.py",
                    },
                }
            },
            "7": {
                "label": "Cenários dos cadastros de Cartões - Bandeira",
                "scenarios": {
                    "1": {
                        "label": 'Cenário 1: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de uma nova Bandeira de Cartão.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosCartõesBandeira" / "cadastrodecartõesbandeira1ºcenario.py",
                    },
                    "2": {
                        "label": 'Cenário 2: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de uma nova Bandeira de Cartão.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosCartõesBandeira" / "cadastrodecartõesbandeira2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 3: Nesse teste, o robô preencherá APENAS os dados obrigatórios e salvará o cadastro de uma nova Bandeira de Cartão.",
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosCartõesBandeira" / "cadastrodecartõesbandeira3ºcenario.py",
                    },
                    "4": {
                        "label": "Cenário 4: Nesse teste, o robô preencherá todos os dados NÃO obrigatórios e salvará o cadastro de uma nova Bandeira de Cartão, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosCartõesBandeira" / "cadastrodecartõesbandeira4ºcenario.py",
                    },
                }
            },
           "8": {
                "label": "Cenários dos cadastros de Cartório",
                "scenarios": {
                    "1": {
                        "label": 'Cenário 1: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de um novo Cartório.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosCartórios" / "cadastrodecartorios1ºcenario.py",
                    },
                    "2": {
                        "label": 'Cenário 2: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de um novo Cartório.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosCartórios" / "cadastrodecartorios2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 3: Nesse teste, o robô preencherá todos os dados NÃO obrigatórios e salvará o cadastro de um novo Cartório, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosCartórios" / "cadastrodecartorios2ºcenario.py",
                    },
                }
            },
           "9": {
                "label": "Cenários dos cadastros de Cedente",
                "scenarios": {
                    "1": {
                        "label": 'Cenário 1: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de um novo Cedente.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosCedente" / "cadastrodecedente1ºcenario.py",
                    },
                    "2": {
                        "label": 'Cenário 2: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de um novo Cedente.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosCedente" / "cadastrodecedente2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 3: Nesse teste, o robô preencherá todos os dados NÃO obrigatórios e salvará o cadastro de um novo Cedente, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosCedente" / "cadastrodecedente3ºcenario.py",
                    },
                }
            },
            "10": {
                "label": "Cenários dos cadastros de Centro de Custo",
                "scenarios": {
                    "1": {
                        "label": 'Cenário 1: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de um novo Centro de Custo.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosCentrodeCusto" / "cadastrodecentrodecusto1ºcenario.py",
                    },
                    "2": {
                        "label": 'Cenário 2: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de um novo Centro de Custo.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosCentrodeCusto" / "cadastrodecentrodecusto2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 3: Nesse teste, o robô preencherá APENAS os dados obrigatórios e salvará o cadastro de um novo Centro de Custo.",
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosCentrodeCusto" / "cadastrodecentrodecusto3ºcenario.py",
                    },
                    "4": {
                        "label": "Cenário 4: Nesse teste, o robô preencherá todos os dados NÃO obrigatórios e salvará o cadastro de um novo Centro de Custo, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosCentrodeCusto" / "cadastrodecentrodecusto4ºcenario.py",
                    },
                }
            },
            "11": {
                "label": "Cenários dos cadastros de Cobrador", 
                "scenarios": {
                    "1": {
                        "label": "Cenário 1: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de um novo Cobrador.",
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosCobrador" / "cadastrodecobrador1ºcenario.py",
                    },
                    "2": {
                        "label": "Cenário 2: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de um novo Cobrador.",
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosCobrador" / "cadastrodecobrador2ºcenario.py",
                    },
                }
            },
           "12": {
                "label": "Cenários dos cadastros de Condição de Pagamento Faturamento MXM",
                "scenarios": {
                    "1": {
                        "label": 'Cenário 1: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de uma nova Condição de Pagamento Faturamento MXM.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosCondiçãoPagamentoFaturamentoMXM" / "cadastrodecondiçaopagamentofaturamentoMXM1ºcenario.py",
                    },
                    "2": {
                        "label": 'Cenário 2: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de uma nova Condição de Pagamento Faturamento MXM.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosCondiçãoPagamentoFaturamentoMXM" / "cadastrodecondiçaopagamentofaturamentoMXM2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 3: Nesse teste, o robô preencherá todos os dados NÃO obrigatórios e salvará o cadastro de uma nova Condição de Pagamento Faturamento MXM, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosCondiçãoPagamentoFaturamentoMXM" / "cadastrodecondiçaopagamentofaturamentoMXM3ºcenario.py",
                    },
                }
            },
            "13": {
                "label": "Cenários dos cadastros de Conveniado",
                "scenarios": {
                    "1": {
                        "label": 'Cenário 1: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de um novo Conveniado.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosConveniados" / "cadastrodeconveniados1ºcenario.py",
                    },
                    "2": {
                        "label": 'Cenário 2: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de um novo Conveniado.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosConveniados" / "cadastrodeconveniados2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 3: Nesse teste, o robô preencherá APENAS os dados obrigatórios e salvará o cadastro de um novo Conveniado.",
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosConveniados" / "cadastrodeconveniados3ºcenario.py",
                    },
                    "4": {
                        "label": "Cenário 4: Nesse teste, o robô preencherá todos os dados NÃO obrigatórios e salvará o cadastro de um novo Conveniado, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosConveniados" / "cadastrodeconveniados4ºcenario.py",
                    },
                }
            },
            "14": {
                "label": "Cenários dos cadastros de Convênio de Ordem de Serviço",
                "scenarios": {
                    "1": {
                        "label": 'Cenário 1: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de um novo Convênio de Ordem de Serviço.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosConvênioDaOrdemdeServiço" / "cadastrodeconvenioOS1ºcenario.py",
                    },
                    "2": {
                        "label": 'Cenário 2: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de um novo Convênio de Ordem de Serviço.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosConvênioDaOrdemdeServiço" / "cadastrodeconvenioOS2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 3: Nesse teste, o robô preencherá APENAS os dados obrigatórios e salvará o cadastro de um novo Convênio de Ordem de Serviço.",
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosConvênioDaOrdemdeServiço" / "cadastrodeconvenioOS3ºcenario.py",
                    },
                    "4": {
                        "label": "Cenário 4: Nesse teste, o robô preencherá todos os dados NÃO obrigatórios e salvará o cadastro de um novo Convênio de Ordem de Serviço, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosConvênioDaOrdemdeServiço" / "cadastrodeconvenioOS4ºcenario.py",
                    },
                }
            },
            "15": {
                "label": "Cenários dos cadastros de Convênio",
                "scenarios": {
                    "1": {
                        "label": 'Cenário 1: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de um novo Convênio.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosConvênios" / "cadastrodeconvenios1ºcenario.py",
                    },
                    "2": {
                        "label": 'Cenário 2: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de um novo Convênio.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosConvênios" / "cadastrodeconvenios2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 3: Nesse teste, o robô preencherá APENAS os dados obrigatórios e salvará o cadastro de um novo Convênio.",
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosConvênios" / "cadastrodeconvenios3ºcenario.py",
                    },
                    "4": {
                        "label": "Cenário 4: Nesse teste, o robô preencherá todos os dados NÃO obrigatórios e salvará o cadastro de um novo Convênio, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosConvênios" / "cadastrodeconvenios4ºcenario.py",
                    },
                }
            },
            "16": {
                "label": "Cenários dos cadastros de Coordenador",
                "scenarios": {
                    "1": {
                        "label": 'Cenário 1: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de um novo Coordenador',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosCoordenador" / "cadastrodecoordenador1ºcenario.py",
                    },
                    "2": {
                        "label": 'Cenário 2: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de um novo Coordenador',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosCoordenador" / "cadastrodecoordenador2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 3: Nesse teste, o robô preencherá APENAS os dados obrigatórios e salvará o cadastro de um novo Coordenador.",
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosCoordenador" / "cadastrodecoordenador3ºcenario.py",
                    },
                    "4": {
                        "label": "Cenário 4: Nesse teste, o robô preencherá todos os dados NÃO obrigatórios e salvará o cadastro de um novo Coordenador, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosCoordenador" / "cadastrodecoordenador4ºcenario.py",
                    },
                }
            },  
           "17": {
                "label": "Cenários dos cadastros de Cor",
                "scenarios": {
                    "1": {
                        "label": 'Cenário 1: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de uma nova Cor.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosCor" / "cadastrodecor1ºcenario.py",
                    },
                    "2": {
                        "label": 'Cenário 2: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de uma nova Cor.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosCor" / "cadastrodecor2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 3: Nesse teste, o robô preencherá todos os dados NÃO obrigatórios e salvará o cadastro de uma nova Cor, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosCor" / "cadastrodecor3ºcenario.py",
                    },
                }
            },
           "18": {
                "label": "Cenários dos cadastros de Duração da Gestação",
                "scenarios": {
                    "1": {
                        "label": 'Cenário 1: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de uma nova Duração da Gestação.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosDuraçãoDaGestação" / "cadastrodeduracaodagestaçao1ºcenario.py",
                    },
                    "2": {
                        "label": 'Cenário 2: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de uma nova Duração da Gestação.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosDuraçãoDaGestação" / "cadastrodeduracaodagestaçao2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 3: Nesse teste, o robô preencherá todos os dados NÃO obrigatórios e salvará o cadastro de uma nova Duração da Gestação, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosDuraçãoDaGestação" / "cadastrodeduracaodagestaçao3ºcenario.py",
                    },
                }
            },
            "19": {
                "label": "Cenários dos cadastros de Emitente de Nota Fiscal",
                "scenarios": {
                    "1": {
                        "label": 'Cenário 1: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de um novo Emitente de Nota Fiscal.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosEmitenteNotaFiscal" / "cadastrodeemitentenotafiscal1ºcenario.py",
                    },
                    "2": {
                        "label": 'Cenário 2: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de um novo Emitente de Nota Fiscal.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosEmitenteNotaFiscal" / "cadastrodeemitentenotafiscal2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 3: Nesse teste, o robô preencherá APENAS os dados obrigatórios e salvará o cadastro de um novo Emitente de Nota Fiscal.",
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosEmitenteNotaFiscal" / "cadastrodeemitentenotafiscal3ºcenario.py",
                    },
                    "4": {
                        "label": "Cenário 4: Nesse teste, o robô preencherá todos os dados NÃO obrigatórios e salvará o cadastro de um novo Emitente de Nota Fiscal, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosEmitenteNotaFiscal" / "cadastrodeemitentenotafiscal4ºcenario.py",
                    },
                }
            }, 
            "20": {
                "label": "Cenários dos cadastros de Forma de Pagamento MXM",
                "scenarios": {
                    "1": {
                        "label": 'Cenário 1: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de uma nova Forma de Pagamento MXM.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosFormasDePagamentoMXM" / "cadastrodeformasdepagamentoMXM1ºcenario.py",
                    },
                    "2": {
                        "label": 'Cenário 2: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de uma nova Forma de Pagamento MXM.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosFormasDePagamentoMXM" / "cadastrodeformasdepagamentoMXM2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 3: Nesse teste, o robô preencherá APENAS os dados obrigatórios e salvará o cadastro de uma nova Forma de Pagamento MXM.",
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosFormasDePagamentoMXM" / "cadastrodeformasdepagamentoMXM3ºcenario.py",
                    },
                    "4": {
                        "label": "Cenário 4: Nesse teste, o robô preencherá todos os dados NÃO obrigatórios e salvará o cadastro de uma nova Forma de Pagamento MXM, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosFormasDePagamentoMXM" / "cadastrodeformasdepagamentoMXM4ºcenario.py",
                    },
                }
            }, 
            "21": {
                "label": "Cenários dos cadastros de Formulário Digital",
                "scenarios": {
                    "1": {
                        "label": 'Cenário 1: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de um novo Formulário Digital.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosFormulárioDigital" / "cadastrodeformulariodigital1ºcenario.py",
                    },
                    "2": {
                        "label": 'Cenário 2: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de um novo Formulário Digital.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosFormulárioDigital" / "cadastrodeformulariodigital2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 3: Nesse teste, o robô preencherá APENAS os dados obrigatórios e salvará o cadastro de um novo Formulário Digital.",
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosFormulárioDigital" / "cadastrodeformulariodigital3ºcenario.py",
                    },
                    "4": {
                        "label": "Cenário 4: Nesse teste, o robô preencherá todos os dados NÃO obrigatórios e salvará o cadastro de um novo Formulário Digital, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosFormulárioDigital" / "cadastrodeformulariodigital4ºcenario.py",
                    },
                }
            }, 
           "22": {
                "label": "Cenários dos cadastros de Formulário Digital - Alternativa",
                "scenarios": {
                    "1": {
                        "label": 'Cenário 1: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de uma nova Alternativa de Formulário Digital.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosFormulárioDigitalAlternativa" / "cadastrodeformulariodigitalalternativa1ºcenario.py",
                    },
                    "2": {
                        "label": 'Cenário 2: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de uma nova Alternativa de Formulário Digital.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosFormulárioDigitalAlternativa" / "cadastrodeformulariodigitalalternativa2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 3: Nesse teste, o robô preencherá todos os dados NÃO obrigatórios e salvará o cadastro de uma nova Alternativa de Formulário Digital, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosFormulárioDigitalAlternativa" / "cadastrodeformulariodigitalalternativa3ºcenario.py",
                    },
                }
            },
            "23": {
                "label": "Cenários dos cadastros de Formulário Digital - Pergunta",
                "scenarios": {
                    "1": {
                        "label": 'Cenário 1: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de uma nova Pergunta de Formulário Digital.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosFormulárioDigital" / "cadastrodeformulariodigital1ºcenario.py",
                    },
                    "2": {
                        "label": 'Cenário 2: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de uma nova Pergunta de Formulário Digital.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosFormulárioDigital" / "cadastrodeformulariodigital2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 3: Nesse teste, o robô preencherá APENAS os dados obrigatórios e salvará o cadastro de uma nova Pergunta de Formulário Digital.",
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosFormulárioDigital" / "cadastrodeformulariodigital3ºcenario.py",
                    },
                    "4": {
                        "label": "Cenário 4: Nesse teste, o robô preencherá todos os dados NÃO obrigatórios e salvará o cadastro de uma nova Pergunta de Formulário Digital, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosFormulárioDigital" / "cadastrodeformulariodigital4ºcenario.py",
                    },
                }
            }, 
            "24": {
                "label": "Cenários dos cadastros de Funerária",
                "scenarios": {
                    "1": {
                        "label": 'Cenário 1: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de uma nova Funerária.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosFunerárias" / "cadastrodefunerarias1ºcenario.py",
                    },
                    "2": {
                        "label": 'Cenário 2: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de uma nova Funerária.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosFunerárias" / "cadastrodefunerarias2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 3: Nesse teste, o robô preencherá APENAS os dados obrigatórios e salvará o cadastro de uma nova Funerária.",
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosFunerárias" / "cadastrodefunerarias3ºcenario.py",
                    },
                    "4": {
                        "label": "Cenário 4: Nesse teste, o robô preencherá todos os dados NÃO obrigatórios e salvará o cadastro de uma nova Funerária, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosFunerárias" / "cadastrodefunerarias4ºcenario.py",
                    },
                }
            }, 
            "25": {
                "label": "Cenários dos cadastros de Grupo",
                "scenarios": {
                    "1": {
                        "label": 'Cenário 1: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de um novo Grupo.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosGrupos" / "cadastrodegrupo1ºcenario.py",
                    },
                    "2": {
                        "label": 'Cenário 2: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de um novo Grupo.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosGrupos" / "cadastrodegrupo2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 3: Nesse teste, o robô preencherá todos os dados NÃO obrigatórios e salvará o cadastro de um novo Grupo, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosGrupos" / "cadastrodegrupo3ºcenario.py",
                    },
                }
            },
            "26": {
                "label": "Cenários dos cadastros de Grupo de Óbito",
                "scenarios": {
                    "1": {
                        "label": 'Cenário 1: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de um novo Grupo de Óbito.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosGruposDeÓbito" / "cadastrodegruposdeobito1ºcenario.py",
                    },
                    "2": {
                        "label": 'Cenário 2: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de um novo Grupo de Óbito.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosGruposDeÓbito" / "cadastrodegruposdeobito2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 3: Nesse teste, o robô preencherá todos os dados NÃO obrigatórios e salvará o cadastro de um novo Grupo de Óbito, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosGruposDeÓbito" / "cadastrodegruposdeobito3ºcenario.py",
                    },
                }
            },
            "27": {
                "label": "Cenários dos cadastros de Grupo de Rateio",
                "scenarios": {
                    "1": {
                        "label": 'Cenário 1: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de um novo Grupo de Rateio.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosGruposDeRateio" / "cadastrodegrupoderateio1ºcenario.py",
                    },
                    "2": {
                        "label": 'Cenário 2: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de um novo Grupo de Rateio.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosGruposDeRateio" / "cadastrodegrupoderateio2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 3: Nesse teste, o robô preencherá APENAS os dados obrigatórios e salvará o cadastro de um novo Grupo de Rateio.",
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosGruposDeRateio" / "cadastrodegrupoderateio3ºcenario.py",
                    },
                    "4": {
                        "label": "Cenário 4: Nesse teste, o robô preencherá todos os dados NÃO obrigatórios e salvará o cadastro de um novo Grupo de Rateio, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosGruposDeRateio" / "cadastrodegrupoderateio4ºcenario.py",
                    },
                }
            }, 
            "28": {
                "label": "Cenários dos cadastros de Guia Médica",
                "scenarios": {
                    "1": {
                        "label": 'Cenário 1: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de uma nova Guia Médica.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosGuias" / "cadastrodeguias1ºcenario.py",
                    },
                    "2": {
                        "label": 'Cenário 2: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de uma nova Guia Médica.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosGuias" / "cadastrodeguias2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 3: Nesse teste, o robô preencherá APENAS os dados obrigatórios e salvará o cadastro de uma nova Guia Médica.",
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosGuias" / "cadastrodeguias3ºcenario.py",
                    },
                    "4": {
                        "label": "Cenário 4: Nesse teste, o robô preencherá todos os dados NÃO obrigatórios e salvará o cadastro de uma nova Guia Médica, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosGuias" / "cadastrodeguias4ºcenario.py",
                    },
                }
            }, 
            "29": {
                "label": "Cenários dos cadastros de Histórico Padrão",
                "scenarios": {
                    "1": {
                        "label": 'Cenário 1: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de um novo Histórico Padrão.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosHistóricoPadrão" / "cadastrodehistoricopadrao1ºcenario.py",
                    },
                    "2": {
                        "label": 'Cenário 2: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de um novo Histórico Padrão.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosHistóricoPadrão" / "cadastrodehistoricopadrao2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 3: Nesse teste, o robô preencherá todos os dados NÃO obrigatórios e salvará o cadastro de um novo Histórico Padrão, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosHistóricoPadrão" / "cadastrodehistoricopadrao3ºcenario.py",
                    },
                }
            },
            "30": {
                "label": "Cenários dos cadastros de Instruções de Boleto",
                "scenarios": {
                    "1": {
                        "label": 'Cenário 1: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de novas Instruções de Boleto.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosInstruçõesBoleto" / "cadastrodeinstruçoesboleto1ºcenario.py",
                    },
                    "2": {
                        "label": 'Cenário 2: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de novas Instruções de Boleto.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosInstruçõesBoleto" / "cadastrodeinstruçoesboleto2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 3: Nesse teste, o robô preencherá APENAS os dados obrigatórios e salvará o cadastro de novas Instruções de Boleto.",
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosInstruçõesBoleto" / "cadastrodeinstruçoesboleto3ºcenario.py",
                    },
                    "4": {
                        "label": "Cenário 4: Nesse teste, o robô preencherá todos os dados NÃO obrigatórios e salvará o cadastro de novas Instruções de Boleto, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosInstruçõesBoleto" / "cadastrodeinstruçoesboleto4ºcenario.py",
                    },
                }
            }, 
            "31": {
                "label": "Cenários dos cadastros de Jazigo",
                "scenarios": {
                    "1": {
                        "label": 'Cenário 1: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de um novo Jazigo.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosJazigos" / "CadastrosJazigosComum" / "cadastrodejazigo1ºcenario.py",
                    },
                    "2": {
                        "label": 'Cenário 2: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de um novo Jazigo.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosJazigos" / "CadastrosJazigosComum" / "cadastrodejazigo2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 3: Nesse teste, o robô preencherá APENAS os dados obrigatórios e salvará o cadastro de um novo Jazigo.",
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosJazigos" / "CadastrosJazigosComum" / "cadastrodejazigo3ºcenario.py",
                    },
                    "4": {
                        "label": "Cenário 4: Nesse teste, o robô preencherá todos os dados NÃO obrigatórios e salvará o cadastro de um novo Jazigo, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosJazigos" / "CadastrosJazigosComum" / "cadastrodejazigo4ºcenario.py",
                    },
                    "5": {
                        "label": "Cenário 5: Nesse teste, o robô preencherá todos os dados, excedendo o limite máximo de Jazigos de uma Quadra e clicará em Salvar, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosJazigos" / "CadastrosJazigosComum" / "cadastrodejazigo5ºcenario.py",
                    },
                }
            }, 
            "32": {
                "label": "Cenários dos cadastros de Jazigos em Lote",
                "scenarios": {
                    "1": {
                        "label": 'Cenário 1: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de novos Jazigos em Lote.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosJazigos" / "CadastrosJazigosLote" / "cadastrodejazigo1ºcenario.py",
                    },
                    "2": {
                        "label": 'Cenário 2: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de novos Jazigos em Lote.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosJazigos" / "CadastrosJazigosLote" / "cadastrodejazigo2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 3: Nesse teste, o robô preencherá APENAS os dados obrigatórios e salvará o cadastro de novos Jazigos em Lote.",
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosJazigos" / "CadastrosJazigosLote" / "cadastrodejazigo3ºcenario.py",
                    },
                    "4": {
                        "label": "Cenário 4: Nesse teste, o robô preencherá todos os dados NÃO obrigatórios e salvará o cadastro de novos Jazigos em Lote, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosJazigos" / "CadastrosJazigosLote" / "cadastrodejazigo4ºcenario.py",
                    },
                    "5": {
                        "label": "Cenário 5: Nesse teste, o robô preencherá todos os dados, excedendo o limite máximo de Jazigos de uma Quadra e clicará em Salvar, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosJazigos" / "CadastrosJazigosLote" / "cadastrodejazigo5ºcenario.py",
                    },
                }
            }, 
            "33": {
                "label": "Cenários dos cadastros de Local de Traslado",
                "scenarios": {
                    "1": {
                        "label": 'Cenário 1: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de um novo Local de Traslado.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosLocaisDeTraslado" / "cadastrodelocaisdetraslado1ºcenario.py",
                    },
                    "2": {
                        "label": 'Cenário 2: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de um novo Local de Traslado.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosLocaisDeTraslado" / "cadastrodelocaisdetraslado2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 3: Nesse teste, o robô preencherá todos os dados NÃO obrigatórios e salvará o cadastro de um novo Local de Traslado, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosLocaisDeTraslado" / "cadastrodelocaisdetraslado3ºcenario.py",
                    },
                }
            },
            "34": {
                "label": "Cenários dos cadastros de Manutenção de Veículos",
                "scenarios": {
                    "1": {
                        "label": 'Cenário 1: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de uma nova Manutenção de Veículo.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosManutençãoDeVeículos" / "cadastrodemanutençaodeveiculos1ºcenario.py",
                    },
                    "2": {
                        "label": 'Cenário 2: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de uma nova Manutenção de Veículo.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosManutençãoDeVeículos" / "cadastrodemanutençaodeveiculos2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 3: Nesse teste, o robô preencherá APENAS os dados obrigatórios e salvará o cadastro de uma nova Manutenção de Veículo.",
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosManutençãoDeVeículos" / "cadastrodemanutençaodeveiculos3ºcenario.py",
                    },
                    "4": {
                        "label": "Cenário 4: Nesse teste, o robô preencherá todos os dados NÃO obrigatórios e salvará o cadastro de uma nova Manutenção de Veículo, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosManutençãoDeVeículos" / "cadastrodemanutençaodeveiculos4ºcenario.py",
                    },
                }
            }, 
            "35": {
                "label": "Cenários dos cadastros de Médico",
                "scenarios": {
                    "1": {
                        "label": 'Cenário 1: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de um novo Médico.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosMédicos" / "cadastrodemedicos1ºcenario.py",
                    },
                    "2": {
                        "label": 'Cenário 2: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de um novo Médico.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosMédicos" / "cadastrodemedicos2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 3: Nesse teste, o robô preencherá APENAS os dados obrigatórios e salvará o cadastro de um novo Médico.",
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosMédicos" / "cadastrodemedicos3ºcenario.py",
                    },
                    "4": {
                        "label": "Cenário 4: Nesse teste, o robô preencherá todos os dados NÃO obrigatórios e salvará o cadastro de um novo Médico, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosMédicos" / "cadastrodemedicos4ºcenario.py",
                    },
                }
            }, 
            "36": {
                "label": "Cenários dos cadastros de Motivo",
                "scenarios": {
                    "1": {
                        "label": 'Cenário 1: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de um novo Motivo.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosMotivos" / "cadastrodemotivos1ºcenario.py",
                    },
                    "2": {
                        "label": 'Cenário 2: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de um novo Motivo.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosMotivos" / "cadastrodemotivos2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 3: Nesse teste, o robô preencherá APENAS os dados obrigatórios e salvará o cadastro de um novo Motivo.",
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosMotivos" / "cadastrodemotivos3ºcenario.py",
                    },
                    "4": {
                        "label": "Cenário 4: Nesse teste, o robô preencherá todos os dados NÃO obrigatórios e salvará o cadastro de um novo Motivo, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosMotivos" / "cadastrodemotivos4ºcenario.py",
                    },
                }
            }, 
            "37": {
                "label": "Cenários dos cadastros de Plano de Contas",
                "scenarios": {
                    "1": {
                        "label": 'Cenário 1: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de um novo Plano de Contas.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosPlanoDeContas" / "cadastrodeplanodecontas1ºcenario.py",
                    },
                    "2": {
                        "label": 'Cenário 2: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de um novo Plano de Contas.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosPlanoDeContas" / "cadastrodeplanodecontas2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 3: Nesse teste, o robô preencherá APENAS os dados obrigatórios e salvará o cadastro de um novo Plano de Contas.",
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosPlanoDeContas" / "cadastrodeplanodecontas3ºcenario.py",
                    },
                    "4": {
                        "label": "Cenário 4: Nesse teste, o robô preencherá todos os dados NÃO obrigatórios e salvará o cadastro de um novo Plano de Contas, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosPlanoDeContas" / "cadastrodeplanodecontas4ºcenario.py",
                    },
                }
            }, 
            "38": {
                "label": "Cenários dos cadastros de Procedimentos",
                "scenarios": {
                    "1": {
                        "label": 'Cenário 1: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de um novo Procedimento.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosProcedimentos" / "cadastrodeprocedimentos1ºcenario.py",
                    },
                    "2": {
                        "label": 'Cenário 2: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de um novo Procedimento.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosProcedimentos" / "cadastrodeprocedimentos2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 3: Nesse teste, o robô preencherá APENAS os dados obrigatórios e salvará o cadastro de um novo Procedimento.",
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosProcedimentos" / "cadastrodeprocedimentos3ºcenario.py",
                    },
                    "4": {
                        "label": "Cenário 4: Nesse teste, o robô preencherá todos os dados NÃO obrigatórios e salvará o cadastro de um novo Procedimento, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosProcedimentos" / "cadastrodeprocedimentos4ºcenario.py",
                    },
                }
            }, 
            "39": {
                "label": "Cenários dos cadastros de Profissão",
                "scenarios": {
                    "1": {
                        "label": 'Cenário 1: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de uma nova Profissão.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosProfissão" / "cadastrodeprofissao1ºcenario.py",
                    },
                    "2": {
                        "label": 'Cenário 2: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de uma nova Profissão.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosProfissão" / "cadastrodeprofissao2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 3: Nesse teste, o robô preencherá todos os dados NÃO obrigatórios e salvará o cadastro de uma nova Profissão, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosProfissão" / "cadastrodeprofissao3ºcenario.py",
                    },
                }
            },
            "40": {
                "label": "Cenários dos cadastros de Quadra",
                "scenarios": {
                    "1": {
                        "label": 'Cenário 1: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de uma nova Quadra.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosQuadras" / "cadastrodequadras1ºcenario.py",
                    },
                    "2": {
                        "label": 'Cenário 2: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de uma nova Quadra.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosQuadras" / "cadastrodequadras2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 3: Nesse teste, o robô preencherá APENAS os dados obrigatórios e salvará o cadastro de uma nova Quadra.",
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosQuadras" / "cadastrodequadras3ºcenario.py",
                    },
                    "4": {
                        "label": "Cenário 4: Nesse teste, o robô preencherá todos os dados NÃO obrigatórios e salvará o cadastro de uma nova Quadra, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosQuadras" / "cadastrodequadras4ºcenario.py",
                    },
                }
            }, 
            "41": {
                "label": "Cenários dos cadastros de Religião",
                "scenarios": {
                    "1": {
                        "label": 'Cenário 1: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de uma nova Religião.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosReligião" / "cadastrodereligiao1ºcenario.py",
                    },
                    "2": {
                        "label": 'Cenário 2: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de uma nova Religião.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosReligião" / "cadastrodereligiao2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 3: Nesse teste, o robô preencherá todos os dados NÃO obrigatórios e salvará o cadastro de uma nova Religião, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosReligião" / "cadastrodereligiao3ºcenario.py",
                    },
                }
            },
            "42": {
                "label": "Cenários dos cadastros de Sala",
                "scenarios": {
                    "1": {
                        "label": 'Cenário 1: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de uma nova Sala.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosSalas" / "cadastrodesalas1ºcenario.py",
                    },
                    "2": {
                        "label": 'Cenário 2: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de uma nova Sala.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosSalas" / "cadastrodesalas2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 3: Nesse teste, o robô preencherá APENAS os dados obrigatórios e salvará o cadastro de uma nova Sala.",
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosSalas" / "cadastrodesalas3ºcenario.py",
                    },
                    "4": {
                        "label": "Cenário 4: Nesse teste, o robô preencherá todos os dados NÃO obrigatórios e salvará o cadastro de uma nova Sala, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosSalas" / "cadastrodesalas4ºcenario.py",
                    },
                }
            }, 
            "43": {
                "label": "Cenários dos cadastros de Subgrupo",
                "scenarios": {
                    "1": {
                        "label": 'Cenário 1: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de um novo Subgrupo.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosSubgrupos" / "cadastrodesubgrupos1ºcenario.py",
                    },
                    "2": {
                        "label": 'Cenário 2: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de um novo Subgrupo.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosSubgrupos" / "cadastrodesubgrupos2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 3: Nesse teste, o robô preencherá todos os dados NÃO obrigatórios e salvará o cadastro de um novo Subgrupo, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosSubgrupos" / "cadastrodesubgrupos3ºcenario.py",
                    },
                }
            },
            "44": {
                "label": "Cenários dos cadastros de Supervisor",
                "scenarios": {
                    "1": {
                        "label": 'Cenário 1: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de um novo Supervisor.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosSupervisor" / "cadastrodesupervisor1ºcenario.py",
                    },
                    "2": {
                        "label": 'Cenário 2: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de um novo Supervisor.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosSupervisor" / "cadastrodesupervisor2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 3: Nesse teste, o robô preencherá APENAS os dados obrigatórios e salvará o cadastro de um novo Supervisor.",
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosSupervisor" / "cadastrodesupervisor3ºcenario.py",
                    },
                    "4": {
                        "label": "Cenário 4: Nesse teste, o robô preencherá todos os dados NÃO obrigatórios e salvará o cadastro de um novo Supervisor, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosSupervisor" / "cadastrodesupervisor4ºcenario.py",
                    },
                }
            }, 
            "45": {
                "label": "Cenários dos cadastros de Tipo de Mensalidade",
                "scenarios": {
                    "1": {
                        "label": 'Cenário 1: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de um novo Tipo de Mensalidade.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosTipoDeMensalidade" / "cadastrodetipodemensalidades1ºcenario.py",
                    },
                    "2": {
                        "label": 'Cenário 2: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de um novo Tipo de Mensalidade.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosTipoDeMensalidade" / "cadastrodetipodemensalidades2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 3: Nesse teste, o robô preencherá APENAS os dados obrigatórios e salvará o cadastro de um novo Tipo de Mensalidade.",
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosTipoDeMensalidade" / "cadastrodetipodemensalidades3ºcenario.py",
                    },
                    "4": {
                        "label": "Cenário 4: Nesse teste, o robô preencherá todos os dados NÃO obrigatórios e salvará o cadastro de um novo Tipo de Mensalidade, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosTipoDeMensalidade" / "cadastrodetipodemensalidades4ºcenario.py",
                    },
                }
            }, 
            "46": {
                "label": "Cenários dos cadastros de Tipo de Contrato",
                "scenarios": {
                    "1": {
                        "label": 'Cenário 1: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de um novo Tipo de Contrato.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosTiposDeContratos" / "cadastrodetiposdecontratos1ºcenario.py",
                    },
                    "2": {
                        "label": 'Cenário 2: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de um novo Tipo de Contrato.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosTiposDeContratos" / "cadastrodetiposdecontratos2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 3: Nesse teste, o robô preencherá APENAS os dados obrigatórios e salvará o cadastro de um novo Tipo de Contrato.",
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosTiposDeContratos" / "cadastrodetiposdecontratos3ºcenario.py",
                    },
                    "4": {
                        "label": "Cenário 4: Nesse teste, o robô preencherá todos os dados NÃO obrigatórios e salvará o cadastro de um novo Tipo de Contrato, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosTiposDeContratos" / "cadastrodetiposdecontratos4ºcenario.py",
                    },
                }
            }, 
            "47": {
                "label": "Cenários dos cadastros de Tipo de Documento",
                "scenarios": {
                    "1": {
                        "label": 'Cenário 1: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de um novo Tipo de Documento.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosTiposDeDocumento" / "cadastrodetiposdedocumento1ºcenario.py",
                    },
                    "2": {
                        "label": 'Cenário 2: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de um novo Tipo de Documento.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosTiposDeDocumento" / "cadastrodetiposdedocumento2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 3: Nesse teste, o robô preencherá todos os dados NÃO obrigatórios e salvará o cadastro de um novo Tipo de Documento, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosTiposDeDocumento" / "cadastrodetiposdedocumento3ºcenario.py",
                    },
                }
            },
            "48": {
                "label": "Cenários dos cadastros de Tipo de Gravidez",
                "scenarios": {
                    "1": {
                        "label": 'Cenário 1: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de um novo Tipo de Gravidez.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosTiposDeGravidez" / "cadastrodetiposdegravidez1ºcenario.py",
                    },
                    "2": {
                        "label": 'Cenário 2: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de um novo Tipo de Gravidez.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosTiposDeGravidez" / "cadastrodetiposdegravidez2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 3: Nesse teste, o robô preencherá todos os dados NÃO obrigatórios e salvará o cadastro de um novo Tipo de Gravidez, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosTiposDeGravidez" / "cadastrodetiposdegravidez3ºcenario.py",
                    },
                }
            },
            "49": {
                "label": "Cenários dos cadastros de Tipo de Venda",
                "scenarios": {
                    "1": {
                        "label": 'Cenário 1: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de um novo Tipo de Venda.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosTiposDeVenda" / "cadastrodetiposdevenda1ºcenario.py",
                    },
                    "2": {
                        "label": 'Cenário 2: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de um novo Tipo de Venda.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosTiposDeVenda" / "cadastrodetiposdevenda2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 3: Nesse teste, o robô preencherá todos os dados NÃO obrigatórios e salvará o cadastro de um novo Tipo de Venda, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosTiposDeVenda" / "cadastrodetiposdevenda3ºcenario.py",
                    },
                }
            },
            "50": {
                "label": "Cenários dos cadastros de Veículo",
                "scenarios": {
                    "1": {
                        "label": 'Cenário 1: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de um novo Veículo.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosVeículos" / "cadastrodeveiculos1ºcenario.py",
                    },
                    "2": {
                        "label": 'Cenário 2: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de um novo Veículo.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosVeículos" / "cadastrodeveiculos2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 3: Nesse teste, o robô preencherá APENAS os dados obrigatórios e salvará o cadastro de um novo Veículo.",
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosVeículos" / "cadastrodeveiculos3ºcenario.py",
                    },
                    "4": {
                        "label": "Cenário 4: Nesse teste, o robô preencherá todos os dados NÃO obrigatórios e salvará o cadastro de um novo Veículo, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosVeículos" / "cadastrodeveiculos4ºcenario.py",
                    },
                }
            }, 
            "51": {
                "label": "Cenários dos cadastros de Velório",
                "scenarios": {
                    "1": {
                        "label": 'Cenário 1: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de um novo Velório.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosVelórios" / "cadastrodevelorios1ºcenario.py",
                    },
                    "2": {
                        "label": 'Cenário 2: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de um novo Velório.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosVelórios" / "cadastrodevelorios2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 3: Nesse teste, o robô preencherá todos os dados NÃO obrigatórios e salvará o cadastro de um novo Velório, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosVelórios" / "cadastrodevelorios3ºcenario.py",
                    },
                }
            },
            "52": {
                "label": "Cenários dos cadastros de Vendedor",
                "scenarios": {
                    "1": {
                        "label": 'Cenário 1: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de um novo Vendedor.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosVendedor" / "cadastrodevendedor1ºcenario.py",
                    },
                    "2": {
                        "label": 'Cenário 2: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de um novo Vendedor.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosVendedor" / "cadastrodevendedor2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 3: Nesse teste, o robô preencherá APENAS os dados obrigatórios e salvará o cadastro de um novo Vendedor.",
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosVendedor" / "cadastrodevendedor3ºcenario.py",
                    },
                    "4": {
                        "label": "Cenário 4: Nesse teste, o robô preencherá todos os dados NÃO obrigatórios e salvará o cadastro de um novo Vendedor, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosVendedor" / "cadastrodevendedor4ºcenario.py",
                    },
                }
            }, 
            "53": {
                "label": "Cenários dos cadastros de Viagem",
                "scenarios": {
                    "1": {
                        "label": 'Cenário 1: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de uma nova Viagem.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosViagem" / "cadastrodeviagem1ºcenario.py",
                    },
                    "2": {
                        "label": 'Cenário 2: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro uma nova Viagem.',
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosViagem" / "cadastrodeviagem2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 3: Nesse teste, o robô preencherá APENAS os dados obrigatórios e salvará o cadastro de uma nova Viagem.",
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosViagem" / "cadastrodeviagem3ºcenario.py",
                    },
                    "4": {
                        "label": "Cenário 4: Nesse teste, o robô preencherá todos os dados NÃO obrigatórios e salvará o cadastro de uma nova Viagem, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosAdicionais" / "CadastrosCenáriosViagem" / "cadastrodeviagem4ºcenario.py",
                    },
                }
            }, 
        },
        "principais": {
            "1": {
                "label": "Cenários dos cadastros de Agenda de Compromissos",
                "scenarios": {
                    "1": {
                        "label": 'Cenário 1: Nesse teste, serão preenchidos todos os campos do cadastro, e clicará em "Salvar".',
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosAgendaDeCompromissos" / "cadastrodeagendadecompromissos1ºcenario.py",
                    },
                    "2": {
                        "label": 'Cenário 2: Nesse teste, serão preenchidos todos os campos do cadastro, e clicará em "Cancelar".',
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosAgendaDeCompromissos" / "cadastrodeagendadecompromissos2ºcenario.py",
                    },
                    "3": {
                        "label": 'Cenário 3: Nesse teste, serão preenchidos APENAS os campos obrigatórios, e clicará em "Salvar".',
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosAgendaDeCompromissos" / "cadastrodeagendadecompromissos3ºcenario.py",
                    },
                    "4": {
                        "label": 'Cenário : Nesse teste, serão preenchidos APENAS os campos NÃO obrigatórios, e clicará em "Salvar", para disparo de alertas.',
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosAgendaDeCompromissos" / "cadastrodeagendadecompromissos4ºcenario.py",
                    },
                },
            },
            "2": {
                "label": "Cenários dos cadastros de Cemitérios",
                "scenarios": {
                    "1": {
                        "label": "Cenário 1: Nesse teste, serão preenchidos todos os campos do cadastro, e clicará em 'Salvar'.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosCemitérios" / "cadastrodecemiterios1ºcenario.py",
                    },
                    "2": {
                        "label": 'Cenário 2: Nesse teste, serão preenchidos todos os campos do cadastro, e clicará em "Cancelar".',
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosCemitérios" / "cadastrodecemiterios2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 3: TESTE CENARIO 3",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosCemitérios" / "cadastrodecemiterios3ºcenario.py",
                    },
                    "4": {
                        "label": "Cenário : TESTE CENARIO 4",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosCemitérios" / "cadastrodecemiterios4ºcenario.py",
                    },
                },
            },
            "3": {
                "label": "Cenários dos cadastros de Cesta Básica",
                "scenarios": {
                    "1": {
                        "label": "Cenário 1: Nesse teste, o robô preencherá os todos campos e salvará o cadastro de uma nova Cesta Básica.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosCestaBásica" / "cadastrodecestabasica1ºcenario.py",
                    },
                    "2": {
                        "label": "Cenário 2: Nesse teste, o robô preencherá os todos campos e cancelará o cadastro de uma nova Cesta Básica.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosCestaBásica" / "cadastrodecestabasica2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 3: Nesse teste, o robô preencherá os campos Não obrigatórios e salvará o cadastro de uma nova Cesta Básica.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosCestaBásica" / "cadastrodecestabasica3ºcenario.py",
                    },
                }
            },
            "4": {
                "label": "Cenários dos cadastros de Cobrador Teste", 
                "scenarios": {
                    "1": {
                        "label": "Cenário 1: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de um novo Cobrador.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosCobradorTeste" / "cadastrodecobradorteste1ºcenario.py",
                    },
                    "2": {
                        "label": "Cenário 2: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de um novo Cobrador.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosCobradorTeste" / "cadastrodecobradorteste2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 3: Nesse teste, o robô preencherá os campos Não obrigatórios e salvará o cadastro de um novo Cobrador.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosCobradorTeste" / "cadastrodecobradorteste3ºcenario.py",
                    },
                }                
            },

            "5": {
                "label": "Cenários dos cadastros de Comissão", 
                "scenarios": {
                    "1": {
                        "label": "Cenário 1: Nesse teste, o robô preencherá os todos campos e salvará o cadastro de uma nova Comissão.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosComissão" / "cadastrodecomissao1ºcenario.py",
                    },
                    "2": {
                        "label": "Cenário 2: Nesse teste, o robô preencherá os campos e cancelará o cadastro de uma nova Comissão.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosComissão" / "cadastrodecomissao2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 3: Nesse teste, o robô preencherá os campos NÃO obrigatórios e salvará o cadastro de uma nova Comissão.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosComissão" / "cadastrodecomissao3ºcenario.py",
                    },
                }                
            },
            "6": {
                "label": "Cenários dos cadastros de Comissão de Campanhas", 
                "scenarios": {
                    "1": {
                        "label": "Cenário 1: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de uma nova Comissão Campanha.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosComissãoDeCampanhas" / "cadastrodecomissaocampanhas1ºcenario.py",
                    },
                    "2": {
                        "label": "Cenário 2: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de uma nova Comissão Campanha.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosComissãoDeCampanhas" / "cadastrodecomissaocampanhas2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 3: Nesse teste, o robô preencherá os campos NÃO obrigatórios e salvará o cadastro de uma nova Comissão Campanha, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosComissãoDeCampanhas" / "cadastrodecomissaocampanhas3ºcenario.py",
                    },
                }                
            },

            "7": {
                "label": "Cenários dos cadastros de Concessionárias De Energia", 
                "scenarios": {
                    "1": {
                        "label": "Cenário 1: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de uma nova Concessionária de Energia.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosConcessionáriasDeEnergia" / "cadastrodeconcessionariasdeenergia1ºcenario.py",
                    },
                    "2": {
                        "label": "Cenário 2: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de uma nova Concessionária de Energia.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosConcessionáriasDeEnergia" / "cadastrodeconcessionariasdeenergia2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 3: Nesse teste, o robô preencherá os campos NÃO obrigatórios e salvará o cadastro de uma nova Concessionária de Energia, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosConcessionáriasDeEnergia" / "cadastrodeconcessionariasdeenergia3ºcenario.py",
                    },
                }                
            },
            "8": {
                "label": "Cenários dos cadastros de Conciliação Bancária", 
                "scenarios": {
                    "1": {
                        "label": "Cenário 1: Nesse teste, o robô preencherá todos os dados e salvará o cadastro de uma nova Conciliação Bancária.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosConciliaçãoBancária" / "cadastrodeconciliaçaobancaria1ºcenario.py",
                    },
                    "2": {
                        "label": "Cenário 2: Nesse teste, o robô preencherá todos os dados e cancelará o cadastro de uma nova Conciliação Bancária.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosConciliaçãoBancária" / "cadastrodeconciliaçaobancaria2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 3: Nesse teste, o robô preencherá todos os dados NÃO obrigatórios e salvará o cadastro de uma nova Conciliação Bancária, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosConciliaçãoBancária" / "cadastrodeconciliaçaobancaria3ºcenario.py",
                    },

                }                
            },
            "9": {
                "label": "Cenários dos cadastros de Conta Bancária", 
                "scenarios": {
                    "1": {
                        "label": "Cenário 1: Nesse teste, o robô preencherá todos os dados e salvará o cadastro de uma nova Conta Bancária.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosContaBancária" / "cadastrodecontabancaria1ºcenario.py",
                    },
                    "2": {
                        "label": "Cenário 2: Nesse teste, o robô preencherá todos os dados e cancelará o cadastro de uma nova Conta Bancária.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosContaBancária" / "cadastrodecontabancaria2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 3: Nesse teste, o robô preencherá APENAS os dados obrigatórios e salvará o cadastro de uma nova Conta Bancária.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosContaBancária" / "cadastrodecontabancaria3ºcenario.py",
                    },
                    "4": {
                        "label": "Cenário 4: Nesse teste, o robô preencherá todos os dados NÃO obrigatórios e salvará o cadastro de uma nova Conta Bancária, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosContaBancária" / "cadastrodecontabancaria4ºcenario.py",
                    },
                }                
            },
            "10": {
                "label": "Cenários dos cadastros de Controle de Cremação", 
                "scenarios": {
                    "1": {
                        "label": "Cenário 1: Nesse teste, o robô preencherá todos os campos  e salvará o cadastro de um novo Controle de Cremação.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosControleDeCremação" / "cadastrodecontroledecremaçao1ºcenario.py",
                    },
                    "2": {
                        "label": "Cenário 2: Nesse teste, o robô preencherá todos os campos  e cancelará o cadastro de um novo Controle de Cremação.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosControleDeCremação" / "cadastrodecontroledecremaçao2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 3: Nesse teste, o robô preencherá APENAS os campos obrigatórios e salvará o cadastro de um novo Controle de Cremação.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosControleDeCremação" / "cadastrodecontroledecremaçao3ºcenario.py",
                    },
                    "4": {
                        "label": "Cenário 4: Nesse teste, o robô preencherá os campos obrigatórios e salvará o cadastro de um novo Controle de Cremação, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosControleDeCremação" / "cadastrodecontroledecremaçao4ºcenario.py",
                    },
                }                
            },
            "11": {
                "label": "Cenários dos cadastros de Cronograma de Faturamento", 
                "scenarios": {
                    "1": {
                        "label": "Cenário 1: Nesse teste, o robô preencherá todos os campos  e salvará o cadastro de um novo Cronograma de Faturamento.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosCronogramaDeFaturamento" / "cadastrodecronogramadefaturamento1ºcenario.py",
                    },
                    "2": {
                        "label": "Cenário 2: Nesse teste, o robô preencherá todos os campos  e cancelará o cadastro de um novo Cronograma de Faturamento.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosCronogramaDeFaturamento" / "cadastrodecronogramadefaturamento2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 3: Nesse teste, o robô preencherá APENAS os campos obrigatórios e salvará o cadastro de um novo Cronograma de Faturamento.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosCronogramaDeFaturamento" / "cadastrodecronogramadefaturamento3ºcenario.py",
                    },
                    "4": {
                        "label": "Cenário 4: Nesse teste, o robô preencherá os campos NÃO obrigatórios e salvará o cadastro de um novo Cronograma de Faturamento, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosCronogramaDeFaturamento" / "cadastrodecronogramadefaturamento4ºcenario.py",
                    },
                }                
            },
            "12": {
                "label": "Cenários dos cadastros de Documentos", 
                "scenarios": {
                    "1": {
                        "label": "Cenário 1: Nesse teste, o robô preencherá todos os campos  e salvará o cadastro de um novo Documento.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosDocumentos" / "cadastrodedocumentos1ºcenario.py",
                    },
                    "2": {
                        "label": "Cenário 2: Nesse teste, o robô preencherá todos os campos  e cancelará o cadastro de um novo Documento.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosDocumentos" / "cadastrodedocumentos2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 3: Nesse teste, o robô preencherá APENAS os campos obrigatórios e salvará o cadastro de um novo Documento.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosDocumentos" / "cadastrodedocumentos3ºcenario.py",
                    },
                    "4": {
                        "label": "Cenário 4: Nesse teste, o robô preencherá os campos NÃO obrigatórios e salvará o cadastro de um novo Documento, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosDocumentos" / "cadastrodedocumentos4ºcenario.py",
                    },
                }                
            },
            "13": {
                "label": "Cenários dos cadastros de Equipamentos", 
                "scenarios": {
                    "1": {
                        "label": "Cenário 1: Nesse teste, o robô preencherá todos os campos  e salvará o cadastro de um novo Equipamento.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosEquipamentos" / "cadastrodeequipamentos1ºcenario.py",
                    },
                    "2": {
                        "label": "Cenário 2: Nesse teste, o robô preencherá todos os campos  e cancelará o cadastro de um novo Equipamento.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosEquipamentos" / "cadastrodeequipamentos2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 3: Nesse teste, o robô preencherá APENAS os campos obrigatórios e salvará o cadastro de um novo Equipamento.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosEquipamentos" / "cadastrodeequipamentos3ºcenario.py",
                    },
                    "4": {
                        "label": "Cenário 4: Nesse teste, o robô preencherá os campos NÃO obrigatórios e salvará o cadastro de um novo Equipamento, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosEquipamentos" / "cadastrodeequipamentos4ºcenario.py",
                    },
                }                
            },
            "14": {
                "label": "Cenários dos cadastros de Escala de Motoristas", 
                "scenarios": {
                    "1": {
                        "label": "Cenário 1: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de uma nova Escala de Motoristas.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosEscalaMotorista" / "cadastrodeescalamotorista1ºcenario.py",
                    },
                    "2": {
                        "label": "Cenário 2: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de uma nova Escala de Motoristas.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosEscalaMotorista" / "cadastrodeescalamotorista2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 4: Nesse teste, o robô preencherá os campos NÃO obrigatórios e salvará o cadastro de uma nova Escala de Motoristas, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosEscalaMotorista" / "cadastrodeescalamotorista3ºcenario.py",
                    },
                }                
            },
            "15": {
                "label": "Cenários dos cadastros de Especialidades", 
                "scenarios": {
                    "1": {
                        "label": "Cenário 1: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de uma nova Especialidade.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosEspecialidades" / "cadastrodeespecialidades1ºcenario.py",
                    },
                    "2": {
                        "label": "Cenário 2: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de uma nova Especialidade.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosEspecialidades" / "cadastrodeespecialidades2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 3: Nesse teste, o robô preencherá os campos NÃO obrigatórios e salvará o cadastro de uma nova Especialidade, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosEspecialidades" / "cadastrodeespecialidades3ºcenario.py",
                    },
                }                
            },     
            "16": {
                "label": "Cenários dos cadastros de Fonte de Informação", 
                "scenarios": {
                    "1": {
                        "label": "Cenário 1: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de uma nova Fonte de Informação.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosFonteDeInformação" / "cadastrodefontedeinformação1ºcenario.py",
                    },
                    "2": {
                        "label": "Cenário 2: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de uma nova Fonte de Informação.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosFonteDeInformação" / "cadastrodefontedeinformação2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 3: Nesse teste, o robô preencherá os campos NÃO obrigatórios e salvará o cadastro de uma nova Fonte de Informação, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosFonteDeInformação" / "cadastrodefontedeinformação3ºcenario.py",
                    },
                }                
            },
            "17": {
                "label": "Cenários dos cadastros de Grupo de Equipamento", 
                "scenarios": {
                    "1": {
                        "label": "Cenário 1: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de um novo Grupo de Equipamento.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosGrupoEquipamento" / "cadastrodegrupoequipamento1ºcenario.py",
                    },
                    "2": {
                        "label": "Cenário 2: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de um novo Grupo de Equipamento.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosGrupoEquipamento" / "cadastrodegrupoequipamento2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 3: Nesse teste, o robô preencherá APENAS os campos obrigatórios e salvará o cadastro de um novo Grupo de Equipamento.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosGrupoEquipamento" / "cadastrodegrupoequipamento3ºcenario.py",
                    },
                    "4": {
                        "label": "Cenário 4: Nesse teste, o robô preencherá os campos NÃO obrigatórios e salvará o cadastro de um novo Grupo de Equipamento, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosGrupoEquipamento" / "cadastrodegrupoequipamento4ºcenario.py",
                    },
                }                
            },
            "18": {
                "label": "Cenários dos cadastros de Infração", 
                "scenarios": {
                    "1": {
                        "label": "Cenário 1: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de uma nova Infração.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosInfração" / "cadastrodeinfraçao1ºcenario.py",
                    },
                    "2": {
                        "label": "Cenário 2: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de uma nova Infração.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosInfração" / "cadastrodeinfraçao2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 3: Nesse teste, o robô preencherá os campos NÃO obrigatórios e salvará o cadastro de uma nova Infração, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosInfração" / "cadastrodeinfraçao3ºcenario.py",
                    },
                }                
            },
            "19": {
                "label": "Cenários dos cadastros de Modo Envio de Cobrança", 
                "scenarios": {
                    "1": {
                        "label": "Cenário 1: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de um novo Modo de Envio de Cobrança.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosModoEnvioDeCobrança" / "cadastrodemodoenviodecobrança1ºcenario.py",
                    },
                    "2": {
                        "label": "Cenário 2: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de um novo Modo de Envio de Cobrança.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosModoEnvioDeCobrança" / "cadastrodemodoenviodecobrança2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 3: Nesse teste, o robô preencherá os campos NÃO obrigatórios e salvará o cadastro de um novo Modo de Envio de Cobrança, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosModoEnvioDeCobrança" / "cadastrodemodoenviodecobrança3ºcenario.py",
                    },
                }                
            },      
            "20": {
                "label": "Cenários dos cadastros de Motoristas", 
                "scenarios": {
                    "1": {
                        "label": "Cenário 1: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de um novo Motorista.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosMotoristas" / "cadastrodemotoristas1ºcenario.py",
                    },
                    "2": {
                        "label": "Cenário 2: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de um novo Motorista.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosMotoristas" / "cadastrodemotoristas2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 3: Nesse teste, o robô preencherá APENAS os campos obrigatórios e salvará o cadastro de um novo Motorista.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosMotoristas" / "cadastrodemotoristas3ºcenario.py",
                    },
                    "4": {
                        "label": "Cenário 4: Nesse teste, o robô preencherá os campos NÃO obrigatórios e salvará o cadastro de um novo Motorista, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosMotoristas" / "cadastrodemotoristas4ºcenario.py",
                    },
                }                
            },
            "21": {
                "label": "Cenários dos cadastros de Movimentação Bancária", 
                "scenarios": {
                    "1": {
                        "label": "Cenário 1: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de uma nova Movimentação Bancária.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosMovimentaçãoBancária" / "cadastrodemovimentaçaobancaria1ºcenario.py",
                    },
                    "2": {
                        "label": "Cenário 2: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de uma nova Movimentação Bancária.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosMovimentaçãoBancária" / "cadastrodemovimentaçaobancaria2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 3: Nesse teste, o robô preencherá APENAS os campos obrigatórios e salvará o cadastro de uma nova Movimentação Bancária.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosMovimentaçãoBancária" / "cadastrodemovimentaçaobancaria3ºcenario.py",
                    },
                    "4": {
                        "label": "Cenário 4: Nesse teste, o robô preencherá os campos NÃO obrigatórios e salvará o cadastro de uma nova Movimentação Bancária, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosMovimentaçãoBancária" / "cadastrodemovimentaçaobancaria4ºcenario.py",
                    },
                }                
            },    
            "22": {
                "label": "Cenários dos cadastros de Movimentação do Caixa", 
                "scenarios": {
                    "1": {
                        "label": "Cenário 1: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de uma nova Movimentação do Caixa.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosMovimentaçãoDoCaixa" / "cadastrodemovimentaçaodocaixa1ºcenario.py",
                    },
                    "2": {
                        "label": "Cenário 2: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de uma nova Movimentação do Caixa.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosMovimentaçãoDoCaixa" / "cadastrodemovimentaçaodocaixa2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 3: Nesse teste, o robô preencherá APENAS os campos obrigatórios e salvará o cadastro de uma nova Movimentação do Caixa.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosMovimentaçãoDoCaixa" / "cadastrodemovimentaçaodocaixa3ºcenario.py",
                    },
                    "4": {
                        "label": "Cenário 4: Nesse teste, o robô preencherá os campos NÃO obrigatórios e salvará o cadastro de uma nova Movimentação do Caixa, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosMovimentaçãoDoCaixa" / "cadastrodemovimentaçaodocaixa4ºcenario.py",
                    },
                }                
            },            
            "23": {
                "label": "Cenários dos cadastros de Multa", 
                "scenarios": {
                    "1": {
                        "label": "Cenário 1: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de uma nova Multa.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosMulta" / "cadastrodemulta1ºcenario.py",
                    },
                    "2": {
                        "label": "Cenário 2: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de uma nova Multa.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosMulta" / "cadastrodemulta2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 3: Nesse teste, o robô preencherá APENAS os campos obrigatórios e salvará o cadastro de uma nova Multa.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosMulta" / "cadastrodemulta3ºcenario.py",
                    },
                    "4": {
                        "label": "Cenário 4: Nesse teste, o robô preencherá os campos NÃO obrigatórios e salvará o cadastro de uma nova Multa, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosMulta" / "cadastrodemulta4ºcenario.py",
                    },
                }
            },                 
            "24": {
                "label": "Cenários dos cadastros de Ocorrência", 
                "scenarios": {
                    "1": {
                        "label": "Cenário 1: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de uma nova Ocorrência.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosOcorrências" / "cadastrodeocorrencias1ºcenario.py",
                    },
                    "2": {
                        "label": "Cenário 2: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de uma nova Ocorrência.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosOcorrências" / "cadastrodeocorrencias2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 3: Nesse teste, o robô preencherá os campos NÃO obrigatórios e salvará o cadastro de uma nova Ocorrência, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosOcorrências" / "cadastrodeocorrencias3ºcenario.py",
                    },
                }
            },     
            "25": {
                "label": "Cenários dos cadastros de Pacote", 
                "scenarios": {
                    "1": {
                        "label": "Cenário 1: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de um novo Pacote.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosPacotes" / "cadastrodepacotes1ºcenario.py",
                    },
                    "2": {
                        "label": "Cenário 2: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de um novo Pacote.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosPacotes" / "cadastrodepacotes2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 3: Nesse teste, o robô preencherá APENAS os campos obrigatórios e salvará o cadastro de um novo Pacote.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosPacotes" / "cadastrodepacotes3ºcenario.py",
                    },
                    "4": {
                        "label": "Cenário 4: Nesse teste, o robô preencherá os campos NÃO obrigatórios e salvará o cadastro de um novo Pacote, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosPacotes" / "cadastrodepacotes4ºcenario.py",
                    },
                }
            }, 
            "26": {
                "label": "Cenários dos cadastros de Pacote Pet", 
                "scenarios": {
                    "1": {
                        "label": "Cenário 1: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de um novo Pacote Pet.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosPacotesPet" / "cadastrodepacotespet1ºcenario.py",
                    },
                    "2": {
                        "label": "Cenário 2: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de um novo Pacote Pet.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosPacotesPet" / "cadastrodepacotespet2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 3: Nesse teste, o robô preencherá APENAS os campos obrigatórios e salvará o cadastro de um novo Pacote Pet.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosPacotesPet" / "cadastrodepacotespet3ºcenario.py",
                    },
                    "4": {
                        "label": "Cenário 4: Nesse teste, o robô preencherá os campos NÃO obrigatórios e salvará o cadastro de um novo Pacote Pet, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosPacotesPet" / "cadastrodepacotespet4ºcenario.py",
                    },
                }
            }, 
            "27": {
                "label": "Cenários dos cadastros de Parâmetros MXM", 
                "scenarios": {
                    "1": {
                        "label": "Cenário 1: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de novos Parâmetros MXM.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosParâmetrosMXM" / "cadastrodeparametrosMXM1ºcenario.py",
                    },
                    "2": {
                        "label": "Cenário 2: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de novos Parâmetros MXM.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosParâmetrosMXM" / "cadastrodeparametrosMXM2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 3: Nesse teste, o robô preencherá APENAS os campos obrigatórios e salvará o cadastro de novos Parâmetros MXM.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosParâmetrosMXM" / "cadastrodeparametrosMXM3ºcenario.py",
                    },
                    "4": {
                        "label": "Cenário 4: Nesse teste, o robô preencherá os campos NÃO obrigatórios e salvará o cadastro de novos Parâmetros MXM, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosParâmetrosMXM" / "cadastrodeparametrosMXM4ºcenario.py",
                    },
                }
            }, 
            "28": {
                "label": "Cenários dos cadastros de Parâmetros Omie", 
                "scenarios": {
                    "1": {
                        "label": "Cenário 1: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de novos Parâmetros Omie.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosParâmetrosOmie" / "cadastrodeparametrosomie1ºcenario.py",
                    },
                    "2": {
                        "label": "Cenário 2: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de novos Parâmetros Omie.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosParâmetrosOmie" / "cadastrodeparametrosomie2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 3: Nesse teste, o robô preencherá APENAS os campos obrigatórios e salvará o cadastro de novos Parâmetros Omie.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosParâmetrosOmie" / "cadastrodeparametrosomie3ºcenario.py",
                    },
                    "4": {
                        "label": "Cenário 4: Nesse teste, o robô preencherá os campos NÃO obrigatórios e salvará o cadastro de novos Parâmetros Omie, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosParâmetrosOmie" / "cadastrodeparametrosomie4ºcenario.py",
                    },
                }
            }, 
            "29": {
                "label": "Cenários dos cadastros de Pessoas", 
                "scenarios": {
                    "1": {
                        "label": "Cenário 1: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de uma nova Pessoa.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosPessoas" / "cadastrodepessoas1ºcenario.py",
                    },
                    "2": {
                        "label": "Cenário 2: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de uma nova Pessoa.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosPessoas" / "cadastrodepessoas2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 3: Nesse teste, o robô preencherá APENAS os campos obrigatórios e salvará o cadastro de uma nova Pessoa.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosPessoas" / "cadastrodepessoas3ºcenario.py",
                    },
                    "4": {
                        "label": "Cenário 4: Nesse teste, o robô preencherá os campos NÃO obrigatórios e salvará o cadastro de uma nova Pessoa, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosPessoas" / "cadastrodepessoas4ºcenario.py",
                    },
                }
            }, 
            "30": {
                "label": "Cenários dos cadastros de Pet", 
                "scenarios": {
                    "1": {
                        "label": "Cenário 1: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de um novo Pet.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosPet" / "cadastrodepet1ºcenario.py",
                    },
                    "2": {
                        "label": "Cenário 2: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de um novo Pet.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosPet" / "cadastrodepet2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 3: Nesse teste, o robô preencherá APENAS os campos obrigatórios e salvará o cadastro de um novo Pet.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosPet" / "cadastrodepet3ºcenario.py",
                    },
                    "4": {
                        "label": "Cenário 4: Nesse teste, o robô preencherá os campos NÃO obrigatórios e salvará o cadastro de um novo Pet, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosPet" / "cadastrodepet4ºcenario.py",
                    },
                }
            },
            "31": {
                "label": "Cenários dos cadastros de Pet - Cores", 
                "scenarios": {
                    "1": {
                        "label": "Cenário 1: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de uma nova Cor de Pet.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosPetCores" / "cadastrodepetcores1ºcenario.py",
                    },
                    "2": {
                        "label": "Cenário 2: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de uma nova Cor de Pet.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosPetCores" / "cadastrodepetcores2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 3: Nesse teste, o robô preencherá os campos NÃO obrigatórios e salvará o cadastro de uma nova Cor de Pet, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosPetCores" / "cadastrodepetcores3ºcenario.py",
                    },
                }
            },
            "32": {
                "label": "Cenários dos cadastros de Pet - Espécies", 
                "scenarios": {
                    "1": {
                        "label": "Cenário 1: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de uma nova Espécie de Pet.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosPetEspécies" / "cadastrodepetespecies1ºcenario.py",
                    },
                    "2": {
                        "label": "Cenário 2: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de uma nova Espécie de Pet.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosPetEspécies" / "cadastrodepetespecies2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 3: Nesse teste, o robô preencherá os campos NÃO obrigatórios e salvará o cadastro de uma nova Espécie de Pet, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosPetEspécies" / "cadastrodepetespecies3ºcenario.py",
                    },
                }
            },
            "33": {
                "label": "Cenários dos cadastros de Pet - Portes", 
                "scenarios": {
                    "1": {
                        "label": "Cenário 1: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de um novo Porte de Pet.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosPetPortes" / "cadastrodepetportes1ºcenario.py",
                    },
                    "2": {
                        "label": "Cenário 2: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de um novo Porte de Pet.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosPetPortes" / "cadastrodepetportes2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 3: Nesse teste, o robô preencherá os campos NÃO obrigatórios e salvará o cadastro de um novo Porte de Pet, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosPetPortes" / "cadastrodepetportes3ºcenario.py",
                    },
                }
            },
            "34": {
                "label": "Cenários dos cadastros de Pet - Raças", 
                "scenarios": {
                    "1": {
                        "label": "Cenário 1: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de uma nova Raça de Pet.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosPetRaças" / "cadastrodepetraças1ºcenario.py",
                    },
                    "2": {
                        "label": "Cenário 2: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de uma nova Raça de Pet",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosPetRaças" / "cadastrodepetraças2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 3: Nesse teste, o robô preencherá os campos NÃO obrigatórios e salvará o cadastro de uma nova Raça de Pet, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosPetRaças" / "cadastrodepetraças3ºcenario.py",
                    },
                }
            },
            "35": {
                "label": "Cenários dos cadastros de Plano Empresa", 
                "scenarios": {
                    "1": {
                        "label": "Cenário 1: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de um novo Plano Empresa.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosPlanoEmpresa" / "cadastrodeplanoempresa1ºcenario.py",
                    },
                    "2": {
                        "label": "Cenário 2: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de um novo Plano Empresa.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosPlanoEmpresa" / "cadastrodeplanoempresa2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 3: Nesse teste, o robô preencherá APENAS os campos obrigatórios e salvará o cadastro de um novo Plano Empresa.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosPlanoEmpresa" / "cadastrodeplanoempresa3ºcenario.py",
                    },
                    "4": {
                        "label": "Cenário 4: Nesse teste, o robô preencherá os campos NÃO obrigatórios e salvará o cadastro de um novo Plano Empresa, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosPlanoEmpresa" / "cadastrodeplanoempresa4ºcenario.py",
                    },
                }
            },
            "36": {
                "label": "Cenários dos cadastros de Procedimentos", 
                "scenarios": {
                    "1": {
                        "label": "Cenário 1: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de um novo Procedimento.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosProcedimentos" / "cadastrodeprocedimentos1ºcenario.py",
                    },
                    "2": {
                        "label": "Cenário 2: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de um novo Procedimento.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosProcedimentos" / "cadastrodeprocedimentos2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 3: Nesse teste, o robô preencherá APENAS os campos obrigatórios e salvará o cadastro de um novo Procedimento.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosProcedimentos" / "cadastrodeprocedimentos3ºcenario.py",
                    },
                    "4": {
                        "label": "Cenário 4: Nesse teste, o robô preencherá os campos NÃO obrigatórios e salvará o cadastro de um novo Procedimento, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosProcedimentos" / "cadastrodeprocedimentos4ºcenario.py",
                    },
                }
            },
            "37": {
                "label": "Cenários dos cadastros de Produtos", 
                "scenarios": {
                    "1": {
                        "label": "Cenário 1: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de um novo Produto.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosProdutos" / "cadastrodeprodutos1ºcenario.py",
                    },
                    "2": {
                        "label": "Cenário 2: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de um novo Produto.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosProdutos" / "cadastrodeprodutos2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 3: Nesse teste, o robô preencherá APENAS os campos obrigatórios e salvará o cadastro de um novo Produto.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosProdutos" / "cadastrodeprodutos3ºcenario.py",
                    },
                    "4": {
                        "label": "Cenário 4: Nesse teste, o robô preencherá os campos NÃO obrigatórios e salvará o cadastro de um novo Produto, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosProdutos" / "cadastrodeprodutos4ºcenario.py",
                    },
                }
            },
            "38": {
                "label": "Cenários dos cadastros de Raças", 
                "scenarios": {
                    "1": {
                        "label": "Cenário 1: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de uma nova Raça.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosRaças" / "cadastroderaças1ºcenario.py",
                    },
                    "2": {
                        "label": "Cenário 2: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de uma nova Raça.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosRaças" / "cadastroderaças2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 3: Nesse teste, o robô preencherá os campos NÃO obrigatórios e salvará o cadastro de uma nova Raça, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosRaças" / "cadastroderaças3ºcenario.py",
                    },
                }
            },
            "39": {
                "label": "Cenários dos cadastros de Reclamações", 
                "scenarios": {
                    "1": {
                        "label": "Cenário 1: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de uma nova Reclamação.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosReclamações" / "cadastrodereclamações1ºcenario.py",
                    },
                    "2": {
                        "label": "Cenário 2: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de uma nova Reclamação.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosReclamações" / "cadastrodereclamações2ºcenario.py",
                    },
                }
            },
            "40": {
                "label": "Cenários dos cadastros de Registro de Óbito Pet", 
                "scenarios": {
                    "1": {
                        "label": "Cenário 1: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de um novo Registro de Óbito Pet.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosRegistroDeÓbitoPet" / "cadastroderegistrodeobitopet1ºcenario.py",
                    },
                    "2": {
                        "label": "Cenário 2: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de um novo Registro de Óbito Pet.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosRegistroDeÓbitoPet" / "cadastroderegistrodeobitopet2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 3: Nesse teste, o robô preencherá APENAS os campos obrigatórios e salvará o cadastro de um novo Registro de Óbito Pet.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosRegistroDeÓbitoPet" / "cadastroderegistrodeobitopet3ºcenario.py",
                    },
                    "4": {
                        "label": "Cenário 4: Nesse teste, o robô preencherá os campos NÃO obrigatórios e salvará o cadastro de um novo Registro de Óbito Pet, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosRegistroDeÓbitoPet" / "cadastroderegistrodeobitopet4ºcenario.py",
                    },
                }
            },
            "41": {
                "label": "Cenários dos cadastros de Serviços", 
                "scenarios": {
                    "1": {
                        "label": "Cenário 1: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de um novo Serviço.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosServiços" / "cadastrodeserviços1ºcenario.py",
                    },
                    "2": {
                        "label": "Cenário 2: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de um novo Serviço.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosServiços" / "cadastrodeserviços2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 3: Nesse teste, o robô preencherá APENAS os campos obrigatórios e salvará o cadastro de um novo Serviço.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosServiços" / "cadastrodeserviços3ºcenario.py",
                    },
                    "4": {
                        "label": "Cenário 4: Nesse teste, o robô preencherá os campos NÃO obrigatórios e salvará o cadastro de um novo Serviço, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosServiços" / "cadastrodeserviços4ºcenario.py",
                    },
                }
            },
            "42": {
                "label": "Cenários dos cadastros de Táboa Biométrica", 
                "scenarios": {
                    "1": {
                        "label": "Cenário 1: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de uma nova Táboa Biométrica.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosTáboaBiométrica" / "cadastrodetaboabiometrica1ºcenario.py",
                    },
                    "2": {
                        "label": "Cenário 2: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de uma nova Táboa Biométrica.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosTáboaBiométrica" / "cadastrodetaboabiometrica2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 3: Nesse teste, o robô preencherá os campos NÃO obrigatórios e salvará o cadastro de uma nova Táboa Biométrica, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosTáboaBiométrica" / "cadastrodetaboabiometrica3ºcenario.py",
                    },
                }
            },
            "43": {
                "label": "Cenários dos cadastros de Tipo de Entrega", 
                "scenarios": {
                    "1": {
                        "label": "Cenário 1: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de um novo Tipo de Entrega.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosTipoDeEntrega" / "cadastrodetipodeentrega1ºcenario.py",
                    },
                    "2": {
                        "label": "Cenário 2: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de um novo Tipo de Entrega.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosTipoDeEntrega" / "cadastrodetipodeentrega2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 3: Nesse teste, o robô preencherá os campos NÃO obrigatórios e salvará o cadastro de um novo Tipo de Entrega, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosTipoDeEntrega" / "cadastrodetipodeentrega3ºcenario.py",
                    },
                }
            },
            "44": {
                "label": "Cenários dos cadastros de Transportes", 
                "scenarios": {
                    "1": {
                        "label": "Cenário 1: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de um novo Transporte.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosTransportes" / "cadastrodetransportes1ºcenario.py",
                    },
                    "2": {
                        "label": "Cenário 2: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de um novo Transporte.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosTransportes" / "cadastrodetransportes2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 3: Nesse teste, o robô preencherá APENAS os campos obrigatórios e salvará o cadastro de um novo Transporte.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosTransportes" / "cadastrodetransportes3ºcenario.py",
                    },
                    "4": {
                        "label": "Cenário 4: Nesse teste, o robô preencherá os campos NÃO obrigatórios e salvará o cadastro de um novo Transporte, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosTransportes" / "cadastrodetransportes4ºcenario.py",
                    },
                }
            },
            "45": {
                "label": "Cenários dos cadastros de Vínculo Convênio/Conveniado", 
                "scenarios": {
                    "1": {
                        "label": "Cenário 1: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de um novo Vínculo Convênio/Conveniado.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosVínculoConvênioConveniado" / "cadastrovinculoconvenioconveniado1ºcenario.py",
                    },
                    "2": {
                        "label": "Cenário 2: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de um novo Vínculo Convênio/Conveniado.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosVínculoConvênioConveniado" / "cadastrovinculoconvenioconveniado2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 3: Nesse teste, o robô preencherá os campos NÃO obrigatórios e salvará o cadastro de um novo Vínculo Convênio/Conveniado, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosVínculoConvênioConveniado" / "cadastrovinculoconvenioconveniado3ºcenario.py",
                    },
                }
            },
        },
    },
    "processos": {
        "1": {"label": "Cenários do Processo: Gestor de Cemitérios", "scenarios": {}},
        "2": {"label": "Cenários do Processo: Gestor de Financeiro", "scenarios": {}},
        "3": {"label": "Cenários do Processo: Gestor de Compras", "scenarios": {}},
        "4": {
            "label": "Cenários das consultas de Histórico de falecidos",
            "scenarios": {
                "1": {
                    "label": "Cenário teste Histórico de falecidos 1: TESTE CENARIO 1",
                    "file": BASE_SCRIPTS / "historico_falecidos" / "cenario_1.py",  # ajuste este caminho conforme sua pasta real
                },
                "2": {
                    "label": "Cenário teste Histórico de falecidos 2: TESTE CENARIO 2",
                    "file": BASE_SCRIPTS / "historico_falecidos" / "cenario_2.py",
                },
                "3": {
                    "label": "Cenário teste Histórico de falecidos 3: TESTE CENARIO 3",
                    "file": BASE_SCRIPTS / "historico_falecidos" / "cenario_3.py",
                },
                "4": {
                    "label": "Cenário teste Histórico de falecidos 4: TESTE CENARIO 4",
                    "file": BASE_SCRIPTS / "historico_falecidos" / "cenario_4.py",
                },
            },
        },
        "5": {"label": "Cenários do Processo: Títulos", "scenarios": {}},
    },
}



# ===================== AJUSTES P/ 'Todos os cenários' =====================
def _derive_group_name(label: str) -> str:
    m = re.search(r"\bde\s+(.+)", label, flags=re.IGNORECASE)
    return m.group(1).strip() if m else (label or "")

def _already_has_all_item(scenarios: dict) -> bool:
    return any(scenarios[k].get("all") for k in scenarios)

def _append_all_item(grupo: dict):
    scenarios = grupo.get("scenarios", {})
    if not scenarios or _already_has_all_item(scenarios):
        return
    ordered_keys = sorted(scenarios.keys(), key=lambda x: int(x))
    files = [scenarios[k]["file"] for k in ordered_keys if isinstance(scenarios[k], dict) and "file" in scenarios[k]]
    next_key = str(len(ordered_keys) + 1)
    group_name = _derive_group_name(grupo.get("label", ""))
    scenarios[next_key] = {
        "label": f"Todos os cenários de {group_name} (Digite {next_key})",
        "all": True,
        "files": files,
    }

def augment_with_all_options():
    cad = SCRIPTS.get("cadastros") or {}
    for tipo in ("principais", "adicionais"):
        for _k, grupo in (cad.get(tipo) or {}).items():
            _append_all_item(grupo)
    for _k, grupo in (SCRIPTS.get("processos") or {}).items():
        _append_all_item(grupo)

# ===================== TECLADO (Windows/Unix) =====================
IS_WIN = (os.name == "nt")
if IS_WIN:
    import msvcrt
    import ctypes
    user32 = ctypes.windll.user32
    VK_SHIFT = 0x10

def clear_screen():
    os.system("cls" if IS_WIN else "clear")

def _is_shift_pressed_windows() -> bool:
    if not IS_WIN:
        return False
    return (user32.GetAsyncKeyState(VK_SHIFT) & 0x8000) != 0

# ===================== SUPORTE PYTHON EM FROZEN =====================
def _pick_python_for_frozen() -> list[str] | None:
    forced = os.getenv("QA_PY")
    if forced and shutil.which(forced):
        return [forced]
    for candidate in ("py", "python", "python3"):
        path = shutil.which(candidate)
        if path:
            if os.name == "nt" and os.path.basename(path).lower() == "py.exe":
                return [path, "-3"]
            return [path]
    return None

# ===================== RAIZ DO PROJETO (CWD) =====================
from pathlib import Path as _PathAlias

def _resolve_project_root(default_start: _PathAlias) -> _PathAlias:
    """
    1) Se QA_PROJECT_ROOT estiver definido e contiver 'cenariostestespegasus', usa-o.
    2) Senão, tenta C:/RPASelenium/RPAsPegasusSelenium (layout padrão do seu repo).
    3) Senão, devolve 'default_start'.
    """
    env = os.getenv("QA_PROJECT_ROOT")
    if env:
        p = _PathAlias(env)
        if (p / "cenariostestespegasus").exists():
            return p

    p = _PathAlias("C:/RPASelenium/RPAsPegasusSelenium")
    if (p / "cenariostestespegasus").exists():
        return p

    return default_start


# ===================== LOGS =====================
def _paths_logs_for(py_file: Path) -> tuple[Path, Path]:
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    safe = f"{py_file.parent.name}__{py_file.stem}".replace(" ", "_")
    out_log = DIR_LOGS / f"{stamp}__{safe}__out.log"
    err_log = DIR_LOGS / f"{stamp}__{safe}__err.log"
    return out_log, err_log

# ===================== EXECUÇÃO DE SCRIPTS =====================
def run_script_with_interrupt(py_file: Path, ask_confirm: bool = True, force_inprocess_when_frozen: bool = False):
    if ask_confirm:
        resp = input(f"Deseja executar '{py_file.name}'? (y/n): ")
        if resp.strip().lower() != 'y':
            print("Ação interrompida pelo usuário"); return

    out_txt, err_txt, erro_msg = "", "", None
    t_ini = time.perf_counter()
    out_log, err_log = _paths_logs_for(py_file)

    try:
        project_cwd = _resolve_project_root(py_file.parent)
        print(f"[runner] cwd: {project_cwd}")

        if getattr(sys, "frozen", False):
            py_cmd = _pick_python_for_frozen()
            if py_cmd is None:
                print("[runner] Nenhum Python do sistema encontrado. Executando in-process (runpy).")
                try:
                    old_cwd = Path.cwd()
                    with contextlib.ExitStack() as stack:
                        stack.callback(lambda: os.chdir(old_cwd))
                        os.chdir(py_file.parent)
                        from io import StringIO
                        old_argv = sys.argv
                        sys.argv = [str(py_file)]
                        old_stdout, old_stderr = sys.stdout, sys.stderr
                        buf_out, buf_err = StringIO(), StringIO()
                        try:
                            sys.stdout, sys.stderr = buf_out, buf_err
                            runpy.run_path(str(py_file), run_name="__main__")
                        finally:
                            sys.stdout, sys.stderr = old_stdout, old_stderr
                            sys.argv = old_argv
                        out_txt, err_txt = buf_out.getvalue(), buf_err.getvalue()
                except Exception as e:
                    err_txt += f"\n[ERRO] Execução in-process falhou: {e}\n"
                    erro_msg = str(e)
            else:
                cmd = py_cmd + [str(py_file)]
                project_cwd = _resolve_project_root(py_file.parent)
                print(f"[runner] cwd: {project_cwd}")
                print(f"[runner] usando interpretador: {' '.join(cmd)}")

                proc = subprocess.Popen(cmd, cwd=str(project_cwd), stdout=..., stderr=..., text=True)
                o, e = proc.communicate()
                out_txt, err_txt = o or "", e or ""
        else:
            cmd = [sys.executable, str(py_file)]
            project_cwd = _resolve_project_root(py_file.parent)
            print(f"[runner] cwd: {project_cwd}")
            print(f"[runner] usando interpretador atual: {' '.join(cmd)}")

            proc = subprocess.Popen(cmd, cwd=str(project_cwd), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            o, e = proc.communicate()
            out_txt, err_txt = o or "", e or ""
    finally:
        dur_s = time.perf_counter() - t_ini
        reporter.record(
            cadastro=f"{py_file.parent.name}/{py_file.stem}",
            status="error" if err_txt else "success",
            duracao_s=dur_s,
            referencia=None,
            erro=erro_msg,
            evidencias={"log": str(err_log)}
        )
        out_log.write_text(out_txt, encoding="utf-8", errors="ignore")
        err_log.write_text(err_txt, encoding="utf-8", errors="ignore")
        print(f"Automação finalizada. -> Duração: {dur_s:.2f}s")

# ===================== MENUS (RESUMO) =====================
def tela_tipo_automacao():
    clear_screen()
    print("Qual tipo de automação você deseja rodar?\n")
    print("- Cadastros (Digite 0)")
    print("- Processos (Digite 1)")
    print("- Cadastros e Processos (Digite 2)\n")
    choice = input("Opção: ").strip()
    if choice == "0":
        print("[MENU] Cadastros")
    elif choice == "1":
        print("[MENU] Processos")
    elif choice == "2":
        print("[MENU] Todos")
        for categoria_key in SCRIPTS["cadastros"]["principais"]:
            categoria = SCRIPTS["cadastros"]["principais"][categoria_key]
            for scenario_key in categoria.get("scenarios", {}):
                run_script_with_interrupt(categoria["scenarios"][scenario_key]["file"], ask_confirm=False)

def main():
    tela_tipo_automacao()
    print("Saindo...")

# ===================== MAIN =====================
if __name__ == "__main__":
    exit_code = 0
    try:
        main()
    except KeyboardInterrupt:
        print("Encerrado pelo usuário."); exit_code = 13
    except Exception as e:
        exit_code = 1
        log_dir = Path(os.getenv("LOCALAPPDATA", ".")) / "AgentePegasus" / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        (log_dir / "crash.log").write_text(traceback.format_exc(), encoding="utf-8")
        print("[ERRO] Falha inesperada. Detalhes em:", log_dir / "crash.log")
        print(traceback.format_exc())
    finally:
        try:
            if reporter:
                reporter.stop()
                rel_path = reporter.save_docx(
                    nome_arquivo=None,
                    ambiente=_report_meta.get("ambiente"),
                    versao=_report_meta.get("versao"),
                    out_base=OUT_BASE
                )
                print(f"[REPORT] Relatório gerado: {rel_path}")
        except Exception as e:
            print(f"[ALERTA] Não foi possível gerar o relatório DOCX: {e}")
        sys.exit(exit_code)
