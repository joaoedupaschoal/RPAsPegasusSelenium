
# força coleta no build do PyInstaller
# força coleta no build do PyInstaller
# força coleta no build do PyInstaller (ajuda a embutir libs usadas nos cenários)
try:
    import selenium, selenium.webdriver                  # noqa
    import webdriver_manager, webdriver_manager.chrome   # noqa
    import requests, urllib3, certifi                    # noqa
    import dotenv                                        # noqa
    import docx                                          # noqa  (python-docx)
    import lxml, lxml.etree                              # noqa
    import pyautogui, pyperclip, pyscreeze, pygetwindow, pymsgbox, pyrect  # noqa
    import faker                                         # noqa  (Faker)
    import validate_docbr                                # noqa
    import trio, trio_websocket, wsproto, websocket      # noqa  (websocket-client = módulo 'websocket')
    import faker_vehicle

except Exception:
    pass


import os
import sys
import time
import threading
import subprocess
from pathlib import Path
# ========== CONFIGURAÇÕES ==========
# Senha fixa (Windows)
SENHA_FIXA = "071999gs"  # <- ajuste aqui a sua senha
MAX_TENTATIVAS = 3

from pathlib import Path
import sys

def get_base_scripts_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys._MEIPASS) / "cenariostestespegasus"
    return Path(__file__).parent.parent / "cenariostestespegasus"

BASE_SCRIPTS = get_base_scripts_dir()
# Mapeie aqui os arquivos .py que cada cenário deve rodar:
SCRIPTS = {
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
                "label": "Cenários dos cadastros de Carteira de Cobrança",
                "scenarios": {
                    "1": {
                        "label": 'Cenário 1: Nesse teste, serão preenchidos todos os campos do cadastro, e clicará em "Salvar".',
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosCarteiraDeCobrança" / "cadastrodecarteiradecobrança1ºcenario.py",
                    },
                    "2": {
                        "label": 'Cenário 2: Nesse teste, serão preenchidos todos os campos do cadastro, e clicará em "Cancelar".',
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosCarteiraDeCobrança" / "cadastrodecarteiradecobrança2ºcenario.py",
                    },
                },
            },
            "3": {
                "label": "Cenários dos cadastros de Cemitérios",
                "scenarios": {
                    "1": {
                        "label": "Cenário 1: Nesse teste, serão preenchidos todos os campos do cadastro, e clicará em 'Salvar'.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosCemitérios" / "cadastrodecemitérios1ºcenario.py",
                    },
                    "2": {
                        "label": 'Cenário 2: Nesse teste, serão preenchidos todos os campos do cadastro, e clicará em "Cancelar".',
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosCemitérios" / "cadastrodecemitérios2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 3: TESTE CENARIO 3",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosCemitérios" / "cadastrodecemitérios3ºcenario.py",
                    },
                    "4": {
                        "label": "Cenário : TESTE CENARIO 4",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosCemitérios" / "cadastrodecemitérios4ºcenario.py",
                    },
                },
            },
            "4": {
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
            "5": {
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

            "6": {
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
            "7": {
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

            "8": {
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
            "9": {
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
            "10": {
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
            "11": {
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
            "12": {
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
            "13": {
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
            "14": {
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
            "15": {
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
            "16": {
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
            "17": {
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
            "18": {
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
            "19": {
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
            "20": {
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
            "21": {
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
            "22": {
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
            "23": {
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
            "24": {
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
            "25": {
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
            "26": {
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
            "27": {
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
            "28": {
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
            "29": {
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
            "30": {
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
            "31": {
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
            "32": {
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
            "33": {
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
            "34": {
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
            "35": {
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
            "36": {
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
            "37": {
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
            "38": {
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
            "39": {
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
            "40": {
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
            "41": {
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
            "42": {
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
            "43": {
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
            "44": {
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
            "45": {
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
            "46": {
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

import re

def _derive_group_name(label: str) -> str:
    m = re.search(r"\bde\s+(.+)", label, flags=re.IGNORECASE)
    return m.group(1).strip() if m else label

def _already_has_all_item(scenarios: dict) -> bool:
    return any(scenarios[k].get("all") for k in scenarios)

def _append_all_item(grupo: dict):
    scenarios = grupo.get("scenarios", {})
    if not scenarios or _already_has_all_item(scenarios):
        return
    ordered_keys = sorted(scenarios.keys(), key=lambda x: int(x))
    files = [scenarios[k]["file"] for k in ordered_keys if "file" in scenarios[k]]
    next_key = str(len(ordered_keys) + 1)  # <<< X dinâmico aqui
    group_name = _derive_group_name(grupo["label"])
    scenarios[next_key] = {
        "label": f"Todos os cenários de {group_name} (Digite {next_key})",
        "all": True,
        "files": files,
    }

def augment_with_all_options():
    # Cadastros (principais/adicionais)
    for tipo in ("principais", "adicionais"):
        for _k, grupo in SCRIPTS["cadastros"][tipo].items():
            _append_all_item(grupo)
    # Processos
    for _k, grupo in SCRIPTS["processos"].items():
        _append_all_item(grupo)

# Chame logo após montar completamente o SCRIPTS:
augment_with_all_options()


# ========== SUPORTE A TECLAS (Windows/Unix) ==========
IS_WIN = (os.name == "nt")

if IS_WIN:
    import msvcrt
    import ctypes
    user32 = ctypes.windll.user32
    VK_SHIFT = 0x1
    VK_INSERT = 0x2D

def clear_screen():
    os.system("cls" if IS_WIN else "clear")

def _is_shift_pressed_windows() -> bool:
    if not IS_WIN:
        return False
    # bit mais significativo indica tecla pressionada
    return (user32.GetAsyncKeyState(VK_SHIFT) & 0x8) != 0

def _read_key_win_blocking():
    """
    Lê uma tecla (Windows). Retorna:
      - ('CHAR', ch) para caracteres
      - ('LEFT', None) para seta esquerda
      - ('ENTER', None)
      - ('BACKSPACE', None)
      - ('CTRL_V', None) quando Ctrl+V
      - ('SHIFT_INSERT', None) quando Shift+Insert
    """
    ch = msvcrt.getwch()

    # ENTER
    if ch in ("\r", "\n"):
        return ("ENTER", None)

    # BACKSPACE - corrigido
    if ch == "\x08":  # era "\0x8"
        return ("BACKSPACE", None)

    # Ctrl+V (colar)
    if ch == "\x16":  # x16 = 22
        return ("CTRL_V", None)

    # Tecla especial (setas, F1, etc.)
    if ch in ("\x00", "\xe0"):
        ch2 = msvcrt.getwch()
        # Left Arrow em msvcrt costuma ser 'K'
        if ch2.upper() == "K":
            # Tentativa de exigir SHIFT; se não der para detectar, tratamos mesmo assim
            if _is_shift_pressed_windows():
                return ("LEFT", None)
            else:
                # Sem SHIFT: podemos ignorar ou aceitar. Aqui, vamos aceitar como voltar também,
                # mas você pode trocar para `return ("OTHER", None)` se quiser ser estrito.
                return ("LEFT", None)
        # Shift+Insert (colar clássico)
        if ch2.upper() == "R":  # Insert = 'R'
            if _is_shift_pressed_windows():
                return ("SHIFT_INSERT", None)
        return ("OTHER", None)

    # Caractere normal
    return ("CHAR", ch)

def read_masked_password(prompt: str) -> str:
    """
    Lê senha mostrando asteriscos, com tentativa de bloquear colar (Ctrl+V e Shift+Insert).
    """
    sys.stdout.write(prompt)
    sys.stdout.flush()

    pwd_buf = []
    if IS_WIN:
        while True:
            t, val = _read_key_win_blocking()
            if t == "ENTER":
                print()
                return "".join(pwd_buf)
            elif t == "BACKSPACE":
                if pwd_buf:
                    pwd_buf.pop()
                    # apaga o último *
                    sys.stdout.write("\b \b")
                    sys.stdout.flush()
            elif t in ("CTRL_V", "SHIFT_INSERT"):
                # ignora tentativa de colar
                continue
            elif t == "CHAR":
                # evita copiar: nunca exibimos a senha, só "*"
                pwd_buf.append(val)
                sys.stdout.write("*")
                sys.stdout.flush()
            else:
                # ignora teclas especiais
                continue
    else:
        # Unix-like: uso simples com termios para não ecoar; "*" visível
        import termios, tty
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            while True:
                ch = sys.stdin.read(1)
                if ch in ("\r", "\n"):
                    print()
                    return "".join(pwd_buf)
                if ch == "\x7f" or ch == "\b":  # backspace
                    if pwd_buf:
                        pwd_buf.pop()
                        sys.stdout.write("\b \b")
                        sys.stdout.flush()
                    continue
                if ch == "\x16":  # Ctrl+V
                    continue
                # sem suporte confiável a Shift+Insert aqui
                pwd_buf.append(ch)
                sys.stdout.write("*")
                sys.stdout.flush()
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def wait_before_submit(seconds: int = 5) -> bool:
    """
    Espera 'seconds' segundos com contagem regressiva.
    Retorna False se o usuário pressionar Shift + Left Arrow (cancelar), senão True.
    """
    print(f"\nPreparando para iniciar (aguarde {seconds}s)...")
    print("Voltar para aba anterior (Shift + Left Arrow)")
    end = time.time() + seconds
    last_shown = None

    while True:
        remain = int(end - time.time())
        if remain <= 0:
            sys.stdout.write("\rIniciando...           \n")
            sys.stdout.flush()
            return True

        if remain != last_shown:
            last_shown = remain
            sys.stdout.write(f"\rIniciando em {remain}s... ")
            sys.stdout.flush()

        # permitir cancelar com Shift+Left (Windows)
        if IS_WIN and msvcrt.kbhit():
            t, _ = _read_key_win_blocking()
            if t == "LEFT":
                print("\nAção cancelada. Voltando ao menu de cenários.")
                return False

        time.sleep(.1)

def read_menu_key(valid_codes: set[str], digits_required: int = 1, show_prompt: str = ""):
    """
    Lê uma opção de menu e SÓ valida ao pressionar ENTER.
    - Mantém Shift+Left para voltar (retorna 'BACK').
    - Mostra/edita o buffer (Backspace apaga).
    - Ignora colagens/teclas especiais.
    - 'digits_required' aqui serve APENAS como dica visual (limite opcional), não auto-envia mais.
    """
    if show_prompt:
        print(show_prompt, end="", flush=True)

    if IS_WIN:
        buf = []
        while True:
            t, val = _read_key_win_blocking()

            # Voltar
            if t == "LEFT":
                print()
                return "BACK"

            # Apagar
            if t == "BACKSPACE":
                if buf:
                    buf.pop()
                    sys.stdout.write("\b \b")
                    sys.stdout.flush()
                continue

            # Confirmar (somente aqui valida)
            if t == "ENTER":
                code = "".join(buf).strip()
                print()
                if code in valid_codes:
                    return code
                print('Escolha um caractere presente na lista')
                print('Voltar para aba anterior (Shift + Left Arrow)')
                buf.clear()
                if show_prompt:
                    print(show_prompt, end="", flush=True)
                continue

            # Digitação: aceita APENAS dígitos para menus numéricos
            if t == "CHAR" and val.isdigit():
                # se quiser limitar visualmente, descomente a linha abaixo:
                # if len(buf) >= digits_required: continue
                buf.append(val)
                sys.stdout.write(val)
                sys.stdout.flush()
                continue

            # Ignora outras teclas (CTRL_V, SHIFT_INSERT, F-teclas etc.)
            continue
    else:
        # Unix-like já exige ENTER por padrão
        s = input().strip()
        if s.lower() == "b":
            return "BACK"
        if s in valid_codes:
            return s
        print('Escolha um caractere presente na lista')
        return None

    
def confirm_yn(question: str) -> bool:
    print(question)
    valid = {"y": True, "Y": True, "n": False, "N": False}
    if IS_WIN:
        while True:
            t, val = _read_key_win_blocking()
            if t == "CHAR" and val in valid:
                print(val)
                return valid[val]
    else:
        while True:
            s = input().strip()
            if s in valid:
                return valid[s]

# =========================
# Login com senha fixa (Windows)
# =========================

def run_all_cadastros_principais():
    """Executa todos os cadastros principais em cadeia"""
    print("Iniciando execução de todos os cadastros principais...")

    all_scripts = []
    for categoria_key in SCRIPTS["cadastros"]["principais"]:
        categoria = SCRIPTS["cadastros"]["principais"][categoria_key]
        if categoria["scenarios"]:
            for scenario_key in categoria["scenarios"]:
                scenario = categoria["scenarios"][scenario_key]
                if "file" in scenario:  # ignora itens 'all'
                    all_scripts.append(scenario["file"])

    total_scripts = len(all_scripts)
    print(f"Total de {total_scripts} cenários principais para executar.")

    if total_scripts == 0:
        print("Nenhum cenário principal configurado para execução.")
        return

    if not confirm_yn(f'Deseja executar todos os {total_scripts} cenários principais? (y/n)'):
        print("Execução cancelada pelo usuário")
        return

    for i, script_file in enumerate(all_scripts, 1):
        try:
            print(f"\n[{i}/{total_scripts}] Executando: {script_file.name}")
            run_script_with_interrupt(script_file, ask_confirm=False)
        except Exception as e:
            print(f"Erro ao executar {script_file.name}: {e}")
            if not confirm_yn("Deseja continuar com os próximos cenários? (y/n)"):
                break

    print("Execução de todos os cadastros principais concluída.")


def input_senha_asteriscos(prompt="Senha: "):
    """Lê senha mostrando '*' e bloqueando Ctrl+V / Shift+Insert."""
    if IS_WIN:
        sys.stdout.write(prompt)
        sys.stdout.flush()
        buf = []
        while True:
            ch = msvcrt.getwch()  # wide-char (suporta acentos)

            # ENTER finaliza
            if ch in ("\r", "\n"):
                print()
                return "".join(buf)

            # BACKSPACE apaga 1 caractere - corrigido
            if ch == "\x08":  # era "\0x8"
                if buf:
                    buf.pop()
                    sys.stdout.write("\b \b")
                    sys.stdout.flush()
                continue

            # Ctrl+C
            if ch == "\x03":  # era "\0x3"
                raise KeyboardInterrupt

            # Ctrl+V (colar)
            if ch == "\x16":
                continue  # ignora

            # Teclas estendidas (setas, Insert, etc.)
            if ch in ("\x00", "\xe0"):  # era "\0x", "\0xe"
                ext = msvcrt.getwch()
                # Shift+Insert (colar clássico)
                if ext.upper() == "R" and _is_shift_pressed_windows():
                    continue  # ignora colagem
                # ignora demais teclas especiais
                continue

            # caractere normal
            buf.append(ch)
            sys.stdout.write("*")
            sys.stdout.flush()
    else:
        # Unix-like
        import getpass
        return getpass.getpass(prompt)

def validar_senha():
    """Mostra banner e valida a senha com até MAX_TENTATIVAS tentativas."""
    clear_screen()
    print("--- AUTOMAÇÕES PEGASUS ---")
    tent = 0
    while tent < MAX_TENTATIVAS:
        senha = input_senha_asteriscos("Digite a senha de acesso para entrar: ")
        if senha == SENHA_FIXA:
            return True
        tent += 1
        if tent < MAX_TENTATIVAS:
            print("Senha incorreta, tente novamente.")
    print("Acesso bloqueado.")
    sys.exit(1)

# ========== EXECUÇÃO DE SCRIPTS COM INTERRUPÇÃO ==========
class InterruptFlag:
    def __init__(self):
        self.flag = False
        self.lock = threading.Lock()
    
    def set(self, v: bool):
        with self.lock:
            self.flag = v
    
    def get(self) -> bool:
        with self.lock:
            return self.flag

def _watch_shift_left(interrupt_flag: InterruptFlag, stop_event: threading.Event):
    if not IS_WIN:
        return  # watcher somente Windows
    while not stop_event.is_set():
        if msvcrt.kbhit():
            t, _ = _read_key_win_blocking()
            if t == "LEFT":
                interrupt_flag.set(True)
        time.sleep(0.2)

import shutil, runpy

def _pick_python_for_frozen() -> list[str] | None:
    """
    Em ambiente congelado (.exe), tenta localizar um Python do sistema para
    rodar o script como novo processo. Retorna o comando base ou None.
    """
    # Windows: 'py' costuma existir; depois tenta 'python', 'python3'
    for candidate in ("py", "python", "python3"):
        path = shutil.which(candidate)
        if path:
            # no Windows, prefira 'py -3 script.py' quando possível
            if candidate == "py":
                return [path, "-3"]
            return [path]
    return None

import runpy, shutil, contextlib

def run_script_with_interrupt(py_file: Path, ask_confirm: bool = True, force_inprocess_when_frozen: bool = True):
    # 1) valida caminho do arquivo
    try:
        if not py_file.exists():
            print(f"[ERRO] Arquivo não encontrado: {py_file}")
            return
    except Exception as e:
        print(f"[ERRO] Caminho inválido: {py_file} ({e})")
        return

    # 2) confirma execução (APENAS se solicitado)
    if ask_confirm:
        if not confirm_yn('Deseja executar a automação selecionada? (y/n)'):
            print("Ação interrompida pelo usuário")
            return

    # 3) watcher do Shift+←
    interrupt_flag = InterruptFlag()
    stop_event = threading.Event()
    watcher = threading.Thread(target=_watch_shift_left, args=(interrupt_flag, stop_event), daemon=True)
    watcher.start()

    try:
        # ===== MODO CONGELADO: roda IN-PROCESS com runpy =====
        if getattr(sys, "frozen", False) and force_inprocess_when_frozen:
            print("[runner] executando in-process (runpy).")
            # Ajusta diretório de trabalho para o diretório do script
            old_cwd = Path.cwd()
            with contextlib.ExitStack() as stack:
                stack.callback(lambda: os.chdir(old_cwd))
                os.chdir(py_file.parent)

                # Executa o .py em thread para manter a capacidade de interrupção
                def _target():
                    try:
                        # opcional: ajustar argv visível pelo script
                        old_argv = sys.argv
                        sys.argv = [str(py_file)]
                        try:
                            runpy.run_path(str(py_file), run_name="__main__")
                        finally:
                            sys.argv = old_argv
                    except SystemExit:
                        pass
                    except Exception as e:
                        print(f"[ERRO] Execução in-process falhou: {e}")

                t = threading.Thread(target=_target, daemon=True)
                t.start()

                # loop de monitoramento/interrupção
                while t.is_alive():
                    if interrupt_flag.get():
                        interrupt_flag.set(False)
                        if confirm_yn("Deseja interromper a automação? (y/n)"):
                            print("Aviso: não é possível 'matar' com segurança em modo in-process; aguardando término…")
                        else:
                            print("Prosseguindo a automação...")
                    time.sleep(0.1)

            print("Automação finalizada.")
            return

        # ===== MODO DEV: subprocess com o mesmo Python =====
        cmd = [sys.executable, str(py_file)]
        print(f"[runner] usando interpretador atual: {' '.join(cmd)}")

        popen_kwargs = {}
        if IS_WIN:
            popen_kwargs["creationflags"] = 0x2  # CREATE_NEW_PROCESS_GROUP

        proc = subprocess.Popen(cmd, **popen_kwargs)

        # loop de monitoramento + interrupção
        while True:
            ret = proc.poll()
            if ret is not None:
                break

            if interrupt_flag.get():
                interrupt_flag.set(False)
                if confirm_yn("Deseja interromper a automação? (y/n)"):
                    try:
                        proc.terminate()
                    except Exception:
                        pass
                    try:
                        proc.wait(timeout=5)
                    except Exception:
                        try:
                            proc.kill()
                        except Exception:
                            pass
                    print("Automação interrompida.")
                    return
                else:
                    print("Prosseguindo a automação...")

            time.sleep(0.1)

        print("Automação finalizada.")
    finally:
        stop_event.set()
        watcher.join(timeout=0.5)

def run_all_cadastros():
    """Executa todos os cadastros principais e adicionais em cadeia"""
    print("Iniciando execução de todos os cadastros...")
    
    # Coleta todos os cenários de cadastros principais
    all_scripts = []
    for categoria_key in SCRIPTS["cadastros"]["principais"]:
        categoria = SCRIPTS["cadastros"]["principais"][categoria_key]
        if categoria["scenarios"]:  # Só adiciona se tiver cenários
            for scenario_key in categoria["scenarios"]:
                scenario = categoria["scenarios"][scenario_key]
                all_scripts.append(scenario["file"])
    
    # Coleta todos os cenários de cadastros adicionais
    for categoria_key in SCRIPTS["cadastros"]["adicionais"]:
        categoria = SCRIPTS["cadastros"]["adicionais"][categoria_key]
        if categoria["scenarios"]:  # Só adiciona se tiver cenários
            for scenario_key in categoria["scenarios"]:
                scenario = categoria["scenarios"][scenario_key]
                all_scripts.append(scenario["file"])
    
    total_scripts = len(all_scripts)
    print(f"Total de {total_scripts} cenários para executar.")
    
    if total_scripts == 0:
        print("Nenhum cenário configurado para execução.")
        return
    
    if not confirm_yn(f'Deseja executar todos os {total_scripts} cenários? (y/n)'):
        print("Execução cancelada pelo usuário")
        return
    
    for i, script_file in enumerate(all_scripts, 1):
        try:
            print(f"\n[{i}/{total_scripts}] Executando: {script_file.name}")
            run_script_with_interrupt(script_file, ask_confirm=False)
        except Exception as e:
            print(f"Erro ao executar {script_file.name}: {e}")
            if not confirm_yn("Deseja continuar com os próximos cenários? (y/n)"):
                break
    
    print("Execução de todos os cadastros concluída.")

# ========== TELAS / MENUS ==========
def tela_cenarios_genericos(titulo: str, scenarios: dict):
    clear_screen()
    print(titulo)
    print("Escolha seu cenário:")
    valid = set()
    ordered_keys = sorted(scenarios.keys(), key=lambda x: int(x))
    for key in ordered_keys:
        lbl = scenarios[key]['label']
        # evita duplicar "(Digite X)" se já estiver no label
        if "(Digite" in lbl:
            print(lbl)
        else:
            print(f"{lbl} (Digite {key})")
        valid.add(key)
    print('Voltar para aba anterior (Shift + Left Arrow)')

    while True:
        choice = read_menu_key(valid, show_prompt="Digite a opção e pressione ENTER: ")
        if choice == "BACK":
            return
        if choice in scenarios:
            # Item especial: "Todos os cenários ..."
            if scenarios[choice].get("all"):
                if not wait_before_submit(5):
                    clear_screen()
                    print(titulo)
                    print("Escolha seu cenário:")
                    for key in ordered_keys:
                        lbl = scenarios[key]['label']
                        print(lbl if "(Digite" in lbl else f"{lbl} (Digite {key})")
                    print('Voltar para aba anterior (Shift + Left Arrow)')
                    continue

                files = scenarios[choice].get("files", [])
                total = len(files)
                if total == 0:
                    print("Nenhum arquivo associado a este conjunto.")
                    time.sleep(1.2)
                else:
                    if not confirm_yn(f"Deseja executar todos os {total} cenários deste grupo? (y/n)"):
                        print("Ação interrompida pelo usuário")
                    else:
                        for i, f in enumerate(files, 1):
                            print(f"\n[{i}/{total}] Executando: {Path(f).name}")
                            run_script_with_interrupt(Path(f), ask_confirm=False)

                # Reexibe a tela
                clear_screen()
                print(titulo)
                print("Escolha seu cenário:")
                for key in ordered_keys:
                    lbl = scenarios[key]['label']
                    print(lbl if "(Digite" in lbl else f"{lbl} (Digite {key})")
                print('Voltar para aba anterior (Shift + Left Arrow)')
                continue

            # Cenário individual (como já era)
            if not wait_before_submit(5):
                clear_screen()
                print(titulo)
                print("Escolha seu cenário:")
                for key in ordered_keys:
                    lbl = scenarios[key]['label']
                    print(lbl if "(Digite" in lbl else f"{lbl} (Digite {key})")
                print('Voltar para aba anterior (Shift + Left Arrow)')
                continue

            run_script_with_interrupt(Path(scenarios[choice]["file"]))

            clear_screen()
            print(titulo)
            print("Escolha seu cenário:")
            for key in ordered_keys:
                lbl = scenarios[key]['label']
                print(lbl if "(Digite" in lbl else f"{lbl} (Digite {key})")
            print('Voltar para aba anterior (Shift + Left Arrow)')
        else:
            if choice is not None:
                print('Escolha um caractere presente na lista')

def _collect_all_files_from(group: dict) -> list[Path]:
    files = []
    for categoria_key in sorted(group.keys(), key=lambda x: int(x)):
        categoria = group[categoria_key]
        scenarios = categoria.get("scenarios", {})
        for scenario_key in sorted(scenarios.keys(), key=lambda x: int(x)):
            scenario = scenarios[scenario_key]
            if "file" in scenario:  # ignora itens 'all'
                files.append(Path(scenario["file"]))
    return files


def run_all_cadastros_principais():
    """Executa todos os cadastros PRINCIPAIS em cadeia."""
    print("Iniciando execução de todos os cadastros PRINCIPAIS...")

    all_scripts = _collect_all_files_from(SCRIPTS["cadastros"]["principais"])
    total = len(all_scripts)
    print(f"Total de {total} cenários PRINCIPAIS para executar.")

    if total == 0:
        print("Nenhum cenário PRINCIPAL configurado para execução.")
        return

    if not confirm_yn(f"Deseja executar todos os {total} cenários PRINCIPAIS? (y/n)"):
        print("Execução cancelada pelo usuário")
        return

    for i, script_file in enumerate(all_scripts, 1):
        try:
            print(f"\n[{i}/{total}] Executando: {script_file.name}")
            run_script_with_interrupt(script_file, ask_confirm=False)
        except Exception as e:
            print(f"Erro ao executar {script_file.name}: {e}")
            if not confirm_yn("Deseja continuar com os próximos cenários? (y/n)"):
                break

    print("Execução de todos os cadastros PRINCIPAIS concluída.")


def run_all_cadastros_adicionais():
    """Executa todos os cadastros ADICIONAIS em cadeia."""
    print("Iniciando execução de todos os cadastros ADICIONAIS...")

    all_scripts = _collect_all_files_from(SCRIPTS["cadastros"]["adicionais"])
    total = len(all_scripts)
    print(f"Total de {total} cenários ADICIONAIS para executar.")

    if total == 0:
        print("Nenhum cenário ADICIONAL configurado para execução.")
        return

    if not confirm_yn(f"Deseja executar todos os {total} cenários ADICIONAIS? (y/n)"):
        print("Execução cancelada pelo usuário")
        return

    for i, script_file in enumerate(all_scripts, 1):
        try:
            print(f"\n[{i}/{total}] Executando: {script_file.name}")
            run_script_with_interrupt(script_file, ask_confirm=False)
        except Exception as e:
            print(f"Erro ao executar {script_file.name}: {e}")
            if not confirm_yn("Deseja continuar com os próximos cenários? (y/n)"):
                break

    print("Execução de todos os cadastros ADICIONAIS concluída.")


def tela_cadastros():
    clear_screen()
    print("Qual tipo de cadastro você deseja rodar?")
    print("- Cadastros Principais (Digite 0)")
    print("- Cadastros Adicionais (Digite 1)")
    print("- Todos os cadastros contidos no sistema (Digite 2)")
    print('Voltar para aba anterior (Shift + Left Arrow)')
    valid = {"0", "1", "2"}

    while True:
        try:
            choice = read_menu_key(valid)
            if choice == "BACK":
                return

            if choice == "0":
                clear_screen()
                print("--- CADASTROS PRINCIPAIS ---")
                print("- Todos os cadastros principais (Digite 0)")
                d = SCRIPTS["cadastros"]["principais"]
                for k in sorted(d.keys(), key=lambda x: int(x)):
                    print(f"- {d[k]['label']} (Digite {k})")
                print('Voltar para aba anterior (Shift + Left Arrow)')

                valid_cp = {"0"} | set(sorted(d.keys(), key=lambda x: int(x)))
                sub = read_menu_key(valid_cp)
                if sub == "BACK":
                    clear_screen()
                    print("Qual tipo de cadastro você deseja rodar?")
                    print("- Cadastros Principais (Digite 0)")
                    print("- Cadastros Adicionais (Digite 1)")
                    print("- Todos os cadastros contidos no sistema (Digite 2)")
                    print('Voltar para aba anterior (Shift + Left Arrow)')
                    continue
                if sub == "0":
                    run_all_cadastros_principais()
                elif sub in d:
                    if d[sub]["scenarios"]:
                        tela_cenarios_genericos(f"--- {d[sub]['label']} ---", d[sub]["scenarios"])
                    else:
                        print("Nenhum cenário configurado para este cadastro ainda.")
                        time.sleep(1.2)

                clear_screen()
                print("Qual tipo de cadastro você deseja rodar?")
                print("- Cadastros Principais (Digite 0)")
                print("- Cadastros Adicionais (Digite 1)")
                print("- Todos os cadastros contidos no sistema (Digite 2)")
                print('Voltar para aba anterior (Shift + Left Arrow)')

            elif choice == "1":
                clear_screen()
                print("--- CADASTROS ADICIONAIS ---")
                print("- Todos os cadastros adicionais (Digite 0)")
                d = SCRIPTS["cadastros"]["adicionais"]
                for k in sorted(d.keys(), key=lambda x: int(x)):
                    print(f"- {d[k]['label']} (Digite {k})")
                print('Voltar para aba anterior (Shift + Left Arrow)')

                valid_ca = {"0"} | set(sorted(d.keys(), key=lambda x: int(x)))
                sub = read_menu_key(valid_ca)
                if sub == "BACK":
                    clear_screen()
                    print("Qual tipo de cadastro você deseja rodar?")
                    print("- Cadastros Principais (Digite 0)")
                    print("- Cadastros Adicionais (Digite 1)")
                    print("- Todos os cadastros contidos no sistema (Digite 2)")
                    print('Voltar para aba anterior (Shift + Left Arrow)')
                    continue
                if sub == "0":
                    run_all_cadastros_adicionais()
                elif sub in d:
                    if d[sub]["scenarios"]:
                        tela_cenarios_genericos(f"--- {d[sub]['label']} ---", d[sub]["scenarios"])
                    else:
                        print("Nenhum cenário configurado para este cadastro ainda.")
                        time.sleep(1.2)

                clear_screen()
                print("Qual tipo de cadastro você deseja rodar?")
                print("- Cadastros Principais (Digite 0)")
                print("- Cadastros Adicionais (Digite 1)")
                print("- Todos os cadastros contidos no sistema (Digite 2)")
                print('Voltar para aba anterior (Shift + Left Arrow)')

            elif choice == "2":
                run_all_cadastros()
                clear_screen()
                print("Qual tipo de cadastro você deseja rodar?")
                print("- Cadastros Principais (Digite 0)")
                print("- Cadastros Adicionais (Digite 1)")
                print("- Todos os cadastros contidos no sistema (Digite 2)")
                print('Voltar para aba anterior (Shift + Left Arrow)')

            else:
                print('Escolha um caractere presente na lista')

        except Exception as e:
            print(f"Erro na seleção: {e}")
            clear_screen()
            print("Qual tipo de cadastro você deseja rodar?")
            print("- Cadastros Principais (Digite 0)")
            print("- Cadastros Adicionais (Digite 1)")
            print("- Todos os cadastros contidos no sistema (Digite 2)")
            print('Voltar para aba anterior (Shift + Left Arrow)')
            continue


def tela_processos():
    clear_screen()
    print("\n--- PROCESSOS ---\n")
    d = SCRIPTS["processos"]
    valid_p = set(sorted(d.keys(), key=lambda x: int(x)))
    for k in sorted(d.keys(), key=lambda x: int(x)):
        print(f"- {d[k]['label']} (Digite {k})")
    print('\nVoltar para aba anterior (Shift + Left Arrow)')

    while True:
        choice = read_menu_key(valid_p)
        if choice == "BACK":
            return
        if choice in d:
            label = d[choice]["label"]
            if d[choice]["scenarios"]:
                tela_cenarios_genericos(f"--- {label} ---", d[choice]["scenarios"])
            else:
                print("Nenhum cenário configurado para este item ainda.")
                time.sleep(1.2)
            clear_screen()
            print("\n--- PROCESSOS ---\n")
            for k in sorted(d.keys(), key=lambda x: int(x)):
                print(f"- {d[k]['label']} (Digite {k})")
            print('\nVoltar para aba anterior (Shift + Left Arrow)')
        else:
            if choice is not None:
                print('Escolha um caractere presente na lista')

def tela_tipo_automacao():
    clear_screen()
    print("Qual tipo de automação você deseja rodar?\n")
    print("- Cadastros (Digite 0)")
    print("- Processos (Digite 1)")
    print("- Cadastros e Processos (Digite 2)\n")
    print('Voltar para aba anterior (Shift + Left Arrow)')

    valid = {"0", "1", "2"}
    while True:
        try:
            choice = read_menu_key(valid)
            if choice == "BACK":
                return
            if choice == "0":
                tela_cadastros()
            elif choice == "1":
                tela_processos()
            elif choice == "2":
                # Nova opção: Cadastros e Processos
                print("Executando todos os cadastros e processos...")
                run_all_cadastros()
                # Aqui você pode adicionar run_all_processos() quando implementar
                print("Execução completa de cadastros e processos concluída.")
            
            # Reexibe o menu após qualquer execução
            clear_screen()
            print("Qual tipo de automação você deseja rodar?\n")
            print("- Cadastros (Digite 0)")
            print("- Processos (Digite 1)")
            print("- Cadastros e Processos (Digite 2)\n")
            print('Voltar para aba anterior (Shift + Left Arrow)')
        except Exception as e:
            print(f"Erro na navegação: {e}")
            continue

# ========== MAIN E SUPORTE A EXE ==========

def main():
    print("--- AUTOMAÇÕES PEGASUS ---")
    tela_tipo_automacao()
    clear_screen()
    print("Saindo...")

def _pause_if_frozen_main():
    if IS_WIN and getattr(sys, "frozen", False) and len(sys.argv) == 1:
        try:
            os.system("pause")
        except Exception:
            pass

if __name__ == "__main__":
    import traceback
    try:
        if "--run-script" in sys.argv:
            import runpy
            i = sys.argv.index("--run-script")
            runpy.run_path(sys.argv[i + 1], run_name="__main__")
            sys.exit()

        validar_senha()
        main()

    except KeyboardInterrupt:
        print("Encerrado pelo usuário.")
        _pause_if_frozen_main()
        sys.exit(13)

    except Exception as e:
        try:
            log_dir = Path(os.getenv("LOCALAPPDATA", ".")) / "AgentePegasus" / "logs"
            log_dir.mkdir(parents=True, exist_ok=True)
            (log_dir / "crash.log").write_text(traceback.format_exc(), encoding="utf-8")
            print("[ERRO] Falha inesperada. Detalhes em:", log_dir / "crash.log")
            print(traceback.format_exc())
        except Exception:
            print("[ERRO] Falha inesperada:", e)
            print(traceback.format_exc())
        _pause_if_frozen_main()
        sys.exit(1)
    finally:
        _pause_if_frozen_main()