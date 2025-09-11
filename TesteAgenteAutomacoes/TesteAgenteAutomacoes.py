# ===================== IMPORTS =====================
import os, sys, time, runpy, traceback, msvcrt
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any, List, Tuple

# ===================== BOAS-VINDAS =====================
def mostrar_boas_vindas():
    print("Carregando... Estamos preparando tudo pra você.")
    try:
        sys.stdout.flush()
    except Exception:
        pass
    time.sleep(0.8)

mostrar_boas_vindas()

# ===================== LIMPAR TELA =====================
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


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

# ===================== LOGO / CABEÇALHO =====================
def banner():
    print("\n===== AUTOMAÇÕES PEGASUS =====")

# ===================== PASSWORD (com asteriscos + 3 tentativas) =====================
def _read_password_masked(prompt: str = "Digite a senha para entrar: ") -> str:
    """Lê senha do teclado mostrando * (Windows / console)."""
    sys.stdout.write(prompt)
    sys.stdout.flush()
    buf: List[str] = []
    while True:
        ch = msvcrt.getwch()  # lê como wide char
        if ch in ('\r', '\n'):
            sys.stdout.write("\n")
            break
        if ch == '\x08':  # backspace
            if buf:
                buf.pop()
                sys.stdout.write("\b \b")  # apaga *
                sys.stdout.flush()
            continue
        if ch == '\x1b':  # ESC limpa tudo
            while buf:
                buf.pop()
                sys.stdout.write("\b \b")
            sys.stdout.flush()
            continue
        buf.append(ch)
        sys.stdout.write("*")
        sys.stdout.flush()
    return "".join(buf)

# Contadores globais de sucesso/falha
SUCCESS_COUNT = 0
FAIL_COUNT = 0

def check_password() -> bool:
    """
    Valida a senha inicial com até 3 tentativas.
    Defina a senha via variável de ambiente PEGASUS_PASSWORD (padrão: '071999gs').
    Registra (pass/fail) no relatório.
    """
    expected = os.getenv("PEGASUS_PASSWORD", "071999gs")
    banner()
    for tentativa in range(1, 4):
        pwd = _read_password_masked("Digite a senha para entrar: ")
        if pwd == expected:
            try:
                reporter.step_pass("Acesso ao Runner", f"Autenticação bem-sucedida na tentativa {tentativa}.")
            except Exception:
                pass
            clear_screen()  # entra com tela limpa
            return True
        else:
            print(f"[ERRO] Senha incorreta. Tentativa {tentativa}/3")
            try:
                reporter.step_fail("Acesso ao Runner", f"Senha incorreta (tentativa {tentativa}/3).")
            except Exception:
                pass
            if tentativa < 3:
                time.sleep(1)
    print("Número máximo de tentativas atingido. Encerrando...")
    try:
        reporter.step_fail("Acesso ao Runner", "Falha de autenticação após 3 tentativas. Execução abortada.")
    except Exception:
        pass
    return False

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

# ===================== QA REPORTER =====================
try:
    current_dir = Path(__file__).resolve().parent
    sys.path.insert(0, str(current_dir))
    from qa_reporter import QAReporter
except Exception as e:
    print("[ERRO] qa_reporter.py não encontrado ou inválido: ", e)
    sys.exit(1)

reporter: Optional[QAReporter] = QAReporter(reports_dir=DIR_REPORTS)
reporter.start()


# --- COMPATIBILIDADE COM qa_reporter ANTIGO/NOVO ---
# se não existir step_pass/step_fail, criamos "adapters" para não quebrar
if not hasattr(reporter, "step_pass"):
    def _step_pass(title: str, details: str | None = None):
        # tente usar uma API alternativa, senão apenas faça print
        if hasattr(reporter, "step"):            # ex: reporter.step(title, status, details)
            try:
                reporter.step(title, "PASS", details or "")
                return
            except Exception:
                pass
        print(f"[PASS] {title}" + (f" - {details}" if details else ""))
    reporter.step_pass = _step_pass  # type: ignore[attr-defined]

if not hasattr(reporter, "step_fail"):
    def _step_fail(title: str, details: str | None = None):
        if hasattr(reporter, "step"):
            try:
                reporter.step(title, "FAIL", details or "")
                return
            except Exception:
                pass
        print(f"[FAIL] {title}" + (f" - {details}" if details else ""))
    reporter.step_fail = _step_fail  # type: ignore[attr-defined]

# opcional: se não houver finish, evita quebrar no finally
if not hasattr(reporter, "finish"):
    def _finish(metadata=None):
        print("[INFO] Reporter.finish ausente — encerrando sem gerar arquivo.")
    reporter.finish = _finish  # type: ignore[attr-defined]
# --- FIM DO BLOCO DE COMPATIBILIDADE ---


_report_meta = {
    "ambiente": os.getenv("QA_AMBIENTE", "Homologação"),
    "versao":   os.getenv("QA_VERSAO", "-"),
}

# ===================== ACESSO À BASE DE CENÁRIOS (SCRIPTS ausente de propósito) =====================
def _scripts() -> Dict[str, Any]:
    """
    Este runner espera que você defina SCRIPTS (e opcionalmente BASE_SCRIPTS) em outro ponto do arquivo
    ou importe de um módulo seu. Se não estiver definido, exibimos um erro amigável.
    """
    g = globals()
    if "SCRIPTS" not in g:
        print("[ERRO] SCRIPTS não definido. Insira sua BASE DE CENÁRIOS antes de usar os menus.")
        return {}
    return g["SCRIPTS"]

# ===================== EXECUÇÃO DE CENÁRIOS =====================
def run_script(path: Path) -> int:
    """Executa um .py como __main__, marca pass/fail no relatório e atualiza contadores."""
    global SUCCESS_COUNT, FAIL_COUNT
    print(f"\n[RUN] {path}")
    if not path.exists():
        print(f"[ERRO] Arquivo não encontrado: {path}")
        try:
            reporter.step_fail(f"{path.name}", "Arquivo não encontrado.")
        except Exception:
            pass
        FAIL_COUNT += 1
        return 1
    try:
        # Variáveis de saída úteis aos cenários
        os.environ.setdefault("QA_OUT_REPORTS", str(DIR_REPORTS))
        os.environ.setdefault("QA_OUT_SHOTS",   str(DIR_SHOTS))
        os.environ.setdefault("QA_OUT_LOGS",    str(DIR_LOGS))
        os.environ.setdefault("QA_OUT_DLS",     str(DIR_DLS))

        runpy.run_path(str(path), run_name="__main__")
        print(f"[OK]  {path.name}")
        reporter.step_pass(f"{path.name}")
        SUCCESS_COUNT += 1
        return 0
    except SystemExit as se:
        code = int(getattr(se, "code", 1) or 1)
        if code == 0:
            print(f"[OK]  {path.name} (SystemExit 0)")
            reporter.step_pass(f"{path.name}")
            SUCCESS_COUNT += 1
        else:
            print(f"[FAIL] {path.name} (SystemExit {code})")
            reporter.step_fail(f"{path.name}", f"SystemExit {code}")
            FAIL_COUNT += 1
        return code
    except Exception:
        print(f"[FAIL] {path.name}")
        traceback.print_exc()
        reporter.step_fail(f"{path.name}", traceback.format_exc())
        FAIL_COUNT += 1
        return 1

def run_chain(paths: List[Path]) -> int:
    """Executa vários .py em sequência; retorna o primeiro código de erro se houver."""
    code = 0
    for p in paths:
        c = run_script(p)
        if code == 0 and c != 0:
            code = c
    return code

# ===================== HELPERS DE NAVEGAÇÃO EM SCRIPTS =====================
def _collect_all_from(node: Dict[str, Any]) -> List[Path]:
    """Coleta todos os arquivos de 'scenarios' de um nó (recursivo)."""
    acc: List[Path] = []
    if not isinstance(node, dict):
        return acc
    scens = node.get("scenarios")
    if isinstance(scens, dict):
        for _, scen in sorted(scens.items(), key=lambda kv: kv[0]):
            p = scen.get("file")
            if isinstance(p, str): p = Path(p)
            if isinstance(p, Path): acc.append(p)
    for k, v in node.items():
        if k in ("label","scenarios"): 
            continue
        if isinstance(v, dict):
            acc.extend(_collect_all_from(v))
    return acc

def _pick_from(node: Dict[str, Any], key: str) -> Optional[Dict[str, Any]]:
    if isinstance(node, dict) and key in node and isinstance(node[key], dict):
        return node[key]
    return None

def _listar_grupos(grupo_raiz: Dict[str, Any]) -> List[Tuple[str, str, Dict[str, Any]]]:
    """
    Retorna [(codigo, label, node)] para cada subgrupo, por ex.:
    ("1", "Cenários dos cadastros de Abastecimento", {...})
    """
    itens: List[Tuple[str, str, Dict[str, Any]]] = []
    if not isinstance(grupo_raiz, dict):
        return itens
    for subkey, subnode in sorted(
        ((k, v) for k, v in grupo_raiz.items() if k not in ("label", "scenarios")), 
        key=lambda kv: kv[0]
    ):
        if isinstance(subnode, dict):
            itens.append((subkey, subnode.get("label", f"Grupo {subkey}"), subnode))
    return itens

def _listar_cenarios(node_de_grupo: Dict[str, Any]) -> List[Tuple[str, str, Path]]:
    """
    Retorna [(codigo, label, path)] com os cenários de um *subgrupo específico*.
    """
    itens: List[Tuple[str, str, Path]] = []
    scens = node_de_grupo.get("scenarios", {})
    if isinstance(scens, dict):
        for scen_id, scen in sorted(scens.items(), key=lambda kv: kv[0]):
            label = scen.get("label", f"Cenário {scen_id}")
            p = scen.get("file")
            if isinstance(p, str):
                p = Path(p)
            if isinstance(p, Path):
                itens.append((scen_id, label, p))
    return itens

# ===================== MENUS =====================
def _confirmar(qtd: int, titulo: str = "cenários") -> bool:
    print(f'\nDeseja iniciar a execução do teste de {qtd} {titulo}? (S/N)')
    return input('> ').strip().lower().startswith('s')

def menu_principal(tree: Dict[str, Any]) -> int:
    clear_screen()
    print('\nQual tipo automação você deseja rodar?\n')
    print('Cadastros (Digite 1)')
    print('Processos (Digite 2)')
    print('Cadastros e Processos (0)')
    opt = input('\n> ').strip()

    if opt == '0':
        paths = []
        if "cadastros" in tree: paths += _collect_all_from(tree["cadastros"])
        if "processos" in tree: paths += _collect_all_from(tree["processos"])
        if _confirmar(len(paths)):
            try:
                reporter.step_pass("Início da Execução em Cadeia", f"Iniciando execução de {len(paths)} cenário(s) - Cadastros e Processos.")
            except Exception:
                pass
            clear_screen()
            code = run_chain(paths)
            try:
                reporter.step_pass("Resumo Geral", f"Concluído: {SUCCESS_COUNT} sucesso(s), {FAIL_COUNT} falha(s). Código de saída: {code}.")
            except Exception:
                pass
            return code
        return 0

    if opt == '1':
        return menu_cadastros(tree.get("cadastros", {}))
    if opt == '2':
        return menu_processos(tree.get("processos", {}))

    print('[ERRO] Opção inválida.')
    return 4

def menu_cadastros(cadastros: Dict[str, Any]) -> int:
    clear_screen()
    print('\nQual tipo de cadastro você deseja rodar?\n')
    print('Cadastros Principais (Digite 1)')
    print('Cadastros Adicionais (Digite 2)')
    print('Todos os cadastros contidos no sistema (0)')

    opt = input('\n> ').strip()

    if opt == '0':
        paths = _collect_all_from(cadastros)
        if _confirmar(len(paths)):
            try:
                reporter.step_pass("Início da Execução em Cadeia", f"Iniciando execução de {len(paths)} cenário(s) - Todos os cadastros.")
            except Exception:
                pass
            clear_screen()
            code = run_chain(paths)
            try:
                reporter.step_pass("Resumo Geral", f"Concluído: {SUCCESS_COUNT} sucesso(s), {FAIL_COUNT} falha(s). Código de saída: {code}.")
            except Exception:
                pass
            return code
        return 0

    if opt == '1':
        grupo = _pick_from(cadastros, "principais")
        return menu_listar_grupos_e_escolher(grupo, "Cadastros Principais")
    if opt == '2':
        grupo = _pick_from(cadastros, "adicionais")
        return menu_listar_grupos_e_escolher(grupo, "Cadastros Adicionais")

    print('[ERRO] Opção inválida.')
    return 4

def menu_listar_grupos_e_escolher(grupo_raiz: Dict[str, Any], titulo: str) -> int:
    """
    1º nível dentro de Cadastros Principais/Adicionais:
    - Mostra todos os grupos (Abastecimento, Áreas, …)
    - 0 = roda todos os cenários de TODOS os grupos
    - número = entra no grupo para listar cenários
    """
    clear_screen()
    itens = _listar_grupos(grupo_raiz)
    if not itens:
        print(f"[ERRO] Nenhum grupo encontrado em {titulo}.")
        return 3

    print(f"\n{titulo}\n")
    print(f"Todos os {titulo.split()[-1]} (Digite 0)")
    for i, (code, label, _) in enumerate(itens, start=1):
        print(f"{label} (Digite {i})")

    opt = input("\n> ").strip()
    if opt == "0":
        paths = _collect_all_from(grupo_raiz)
        if _confirmar(len(paths)):
            try:
                reporter.step_pass("Início da Execução em Cadeia", f"Iniciando {len(paths)} cenário(s) - {titulo} (todos).")
            except Exception:
                pass
            clear_screen()
            code = run_chain(paths)
            try:
                reporter.step_pass("Resumo Geral", f"Concluído: {SUCCESS_COUNT} sucesso(s), {FAIL_COUNT} falha(s). Código de saída: {code}.")
            except Exception:
                pass
            return code
        return 0

    if opt.isdigit():
        n = int(opt)
        if n < 1 or n > len(itens):
            print("[ERRO] Opção fora de faixa.")
            return 4
        _, label_grupo, node_grupo = itens[n-1]
        return menu_listar_cenarios_de_um_grupo(node_grupo, label_grupo)

    print("[ERRO] Opção inválida.")
    return 4

def menu_listar_cenarios_de_um_grupo(node_grupo: Dict[str, Any], titulo_grupo: str) -> int:
    """
    2º nível: lista os CENÁRIOS do grupo escolhido (com 0 = rodar todos do grupo).
    """
    clear_screen()
    itens = _listar_cenarios(node_grupo)
    if not itens:
        print(f"[ERRO] Nenhum cenário encontrado em {titulo_grupo}.")
        return 3

    print(f"\n{titulo_grupo} - Selecione o que rodar:\n")
    print("0) Rodar TODOS deste grupo em cadeia")
    for i, (code, label, _) in enumerate(itens, start=1):
        print(f"{i}) {label}")

    opt = input("\n> ").strip()
    if opt == "0":
        paths = [p for _, _, p in itens]
        if _confirmar(len(paths)):
            try:
                reporter.step_pass("Início da Execução em Cadeia", f"Iniciando {len(paths)} cenário(s) - {titulo_grupo}.")
            except Exception:
                pass
            clear_screen()
            code = run_chain(paths)
            try:
                reporter.step_pass("Resumo Geral", f"Concluído: {SUCCESS_COUNT} sucesso(s), {FAIL_COUNT} falha(s). Código de saída: {code}.")
            except Exception:
                pass
            return code
        return 0

    if opt.isdigit():
        n = int(opt)
        if n < 1 or n > len(itens):
            print("[ERRO] Opção fora de faixa.")
            return 4
        _, label, p = itens[n-1]
        if _confirmar(1, "cenário"):
            clear_screen()
            return run_script(p)
        return 0

    print("[ERRO] Opção inválida.")
    return 4

def menu_processos(proc: Dict[str, Any]) -> int:
    """
    Se sua árvore de 'processos' tiver a mesma estrutura (grupos -> scenarios),
    use o mesmo padrão de listagem:
    """
    return menu_listar_grupos_e_escolher(proc, "Processos")

# ===================== CLI =====================
def main_cli():
    args = sys.argv[1:]

    # Atalhos por linha de comando (opcionais)
    if "--run" in args:
        idx = args.index("--run")
        target = args[idx + 1] if idx + 1 < len(args) else None
        if not target:
            print("[ERRO] Uso: --run <arquivo.py>")
            sys.exit(2)
        clear_screen()
        sys.exit(run_chain([Path(target)]))

    if "--chain" in args:
        idx = args.index("--chain")
        chain = args[idx + 1] if idx + 1 < len(args) else ""
        paths = [Path(p) for p in chain.split("|") if p.strip()]
        clear_screen()
        sys.exit(run_chain(paths))

    # Fluxo com senha + menus
    if not check_password():
        # senha inválida já foi logada; encerra com código 5
        try:
            reporter.step_fail("Encerramento", "Aplicação encerrada por falha de autenticação.")
        except Exception:
            pass
        sys.exit(5)

    tree = _scripts()
    if not tree:
        # Sem SCRIPTS definido
        try:
            reporter.step_fail("Encerramento", "SCRIPTS não definido. Nada a executar.")
        except Exception:
            pass
        sys.exit(3)

    code = menu_principal(tree)
    sys.exit(code)

if __name__ == "__main__":
    try:
        main_cli()
    finally:
        # Resumo final e fechamento do relatório
        try:
            reporter.step_pass("Resumo Final",
                               f"Total executado: {SUCCESS_COUNT + FAIL_COUNT} | "
                               f"Sucessos: {SUCCESS_COUNT} | Falhas: {FAIL_COUNT}")
            reporter.finish(metadata=_report_meta)
            print(f"[RELATÓRIO] Gerado em: {DIR_REPORTS}")
        except Exception as _e:
            print("[WARN] Falha ao finalizar relatório:", _e)
