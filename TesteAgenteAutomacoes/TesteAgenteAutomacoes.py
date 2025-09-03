
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
    import getpass

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
SENHA_FIXA = "0701999gs"  # <- ajuste aqui a sua senha
MAX_TRIES = 03

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
            "01": {
                "label": "Cenários dos cadastros de Abastecimento",
                "scenarios": {
                    
                }
            },
            "02": {"label": "Cenários dos cadastros de Áreas", "scenarios": {}},
            "03": {"label": "Cenários dos cadastros de Atendentes", "scenarios": {}},
            "04": {"label": "Cenários dos cadastros de Capelas", "scenarios": {}},
            "05": {"label": "Cenários dos cadastros de Carteira", "scenarios": {}},
        },
        "principais": {
            "01": {
                "label": "Cenários dos cadastros de Agenda de Compromissos",
                "scenarios": {
                    "01": {
                        "label": 'Cenário 01: Nesse teste, serão preenchidos todos os campos do cadastro, e clicará em "Salvar".',
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosAgendaDeCompromissos" / "cadastrodeagendadecompromissos1ºcenario.py",
                    },
                    "02": {
                        "label": 'Cenário 02: Nesse teste, serão preenchidos todos os campos do cadastro, e clicará em "Cancelar".',
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosAgendaDeCompromissos" / "cadastrodeagendadecompromissos2ºcenario.py",
                    },
                    "03": {
                        "label": 'Cenário 03: Nesse teste, serão preenchidos APENAS os campos obrigatórios, e clicará em "Salvar".',
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosAgendaDeCompromissos" / "cadastrodeagendadecompromissos3ºcenario.py",
                    },
                    "004": {
                        "label": 'Cenário 004: Nesse teste, serão preenchidos APENAS os campos NÃO obrigatórios, e clicará em "Salvar", para disparo de alertas.',
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosAgendaDeCompromissos" / "cadastrodeagendadecompromissos4ºcenario.py",
                    },
                },
            },
            "02": {
                "label": "Cenários dos cadastros de Carteira de Cobrança",
                "scenarios": {
                    "01": {
                        "label": 'Cenário 01: Nesse teste, serão preenchidos todos os campos do cadastro, e clicará em "Salvar".',
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosCarteiraDeCobrança" / "cadastrodecarteiradecobrança1ºcenario.py",
                    },
                    "02": {
                        "label": 'Cenário 02: Nesse teste, serão preenchidos todos os campos do cadastro, e clicará em "Cancelar".',
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosCarteiraDeCobrança" / "cadastrodecarteiradecobrança2ºcenario.py",
                    },
                },
            },
            "03": {
                "label": "Cenários dos cadastros de Cemitérios",
                "scenarios": {
                    "01": {
                        "label": "Cenário 01: Nesse teste, serão preenchidos todos os campos do cadastro, e clicará em 'Salvar'.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosCemitérios" / "cadastrodecemitérios1ºcenario.py",
                    },
                    "02": {
                        "label": 'Cenário 02: Nesse teste, serão preenchidos todos os campos do cadastro, e clicará em "Cancelar".',
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosCemitérios" / "cadastrodecemitérios2ºcenario.py",
                    },
                    "03": {
                        "label": "Cenário 03: TESTE CENARIO 03",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosCemitérios" / "cadastrodecemitérios3ºcenario.py",
                    },
                    "004": {
                        "label": "Cenário 004: TESTE CENARIO 04",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosCemitérios" / "cadastrodecemitérios4ºcenario.py",
                    },
                },
            },
            "04": {
                "label": "Cenários dos cadastros de Cesta Básica",
                "scenarios": {
                    "01": {
                        "label": "Cenário 01: Nesse teste, o robô preencherá os todos campos e salvará o cadastro de uma nova Cesta Básica.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosCestaBásica" / "cadastrodecestabasica1ºcenario.py",
                    },
                    "02": {
                        "label": "Cenário 02: Nesse teste, o robô preencherá os todos campos e cancelará o cadastro de uma nova Cesta Básica.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosCestaBásica" / "cadastrodecestabasica2ºcenario.py",
                    },
                    "03": {
                        "label": "Cenário 03: Nesse teste, o robô preencherá os campos Não obrigatórios e salvará o cadastro de uma nova Cesta Básica.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosCestaBásica" / "cadastrodecestabasica3ºcenario.py",
                    },
                }
            },
            "05": {
                "label": "Cenários dos cadastros de Cobrador Teste", 
                "scenarios": {
                    "01": {
                        "label": "Cenário 01: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de um novo Cobrador.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosCobradorTeste" / "cadastrodecobradorteste1ºcenario.py",
                    },
                    "02": {
                        "label": "Cenário 02: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de um novo Cobrador.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosCobradorTeste" / "cadastrodecobradorteste2ºcenario.py",
                    },
                    "03": {
                        "label": "Cenário 03: Nesse teste, o robô preencherá os campos Não obrigatórios e salvará o cadastro de um novo Cobrador.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosCobradorTeste" / "cadastrodecobradorteste3ºcenario.py",
                    },
                }                
            },

            "06": {
                "label": "Cenários dos cadastros de Comissão", 
                "scenarios": {
                    "01": {
                        "label": "Cenário 01: Nesse teste, o robô preencherá os todos campos e salvará o cadastro de uma nova Comissão.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosComissão" / "cadastrodecomissao1ºcenario.py",
                    },
                    "02": {
                        "label": "Cenário 02: Nesse teste, o robô preencherá os campos e cancelará o cadastro de uma nova Comissão.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosComissão" / "cadastrodecomissao2ºcenario.py",
                    },
                    "03": {
                        "label": "Cenário 03: Nesse teste, o robô preencherá os campos NÃO obrigatórios e salvará o cadastro de uma nova Comissão.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosComissão" / "cadastrodecomissao3ºcenario.py",
                    },
                }                
            },
            "07": {
                "label": "Cenários dos cadastros de Comissão de Campanhas", 
                "scenarios": {
                    "01": {
                        "label": "Cenário 01: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de uma nova Comissão Campanha.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosComissãoDeCampanhas" / "cadastrodecomissaocampanhas1ºcenario.py",
                    },
                    "02": {
                        "label": "Cenário 02: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de uma nova Comissão Campanha.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosComissãoDeCampanhas" / "cadastrodecomissaocampanhas2ºcenario.py",
                    },
                    "03": {
                        "label": "Cenário 03: Nesse teste, o robô preencherá os campos NÃO obrigatórios e salvará o cadastro de uma nova Comissão Campanha, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosComissãoDeCampanhas" / "cadastrodecomissaocampanhas3ºcenario.py",
                    },
                }                
            },

            "08": {
                "label": "Cenários dos cadastros de Concessionárias De Energia", 
                "scenarios": {
                    "01": {
                        "label": "Cenário 01: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de uma nova Concessionária de Energia.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosConcessionáriasDeEnergia" / "cadastrodeconcessionariasdeenergia1ºcenario.py",
                    },
                    "02": {
                        "label": "Cenário 02: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de uma nova Concessionária de Energia.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosConcessionáriasDeEnergia" / "cadastrodeconcessionariasdeenergia2ºcenario.py",
                    },
                    "03": {
                        "label": "Cenário 03: Nesse teste, o robô preencherá os campos NÃO obrigatórios e salvará o cadastro de uma nova Concessionária de Energia, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosConcessionáriasDeEnergia" / "cadastrodeconcessionariasdeenergia3ºcenario.py",
                    },
                }                
            },
            "09": {
                "label": "Cenários dos cadastros de Conciliação Bancária", 
                "scenarios": {
                    "01": {
                        "label": "Cenário 01: Nesse teste, o robô preencherá todos os dados e salvará o cadastro de uma nova Conciliação Bancária.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosConciliaçãoBancária" / "cadastrodeconciliaçaobancaria1ºcenario.py",
                    },
                    "02": {
                        "label": "Cenário 02: Nesse teste, o robô preencherá todos os dados e cancelará o cadastro de uma nova Conciliação Bancária.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosConciliaçãoBancária" / "cadastrodeconciliaçaobancaria2ºcenario.py",
                    },
                    "03": {
                        "label": "Cenário 03: Nesse teste, o robô preencherá todos os dados NÃO obrigatórios e salvará o cadastro de uma nova Conciliação Bancária, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosConciliaçãoBancária" / "cadastrodeconciliaçaobancaria3ºcenario.py",
                    },

                }                
            },
            "10": {
                "label": "Cenários dos cadastros de Conta Bancária", 
                "scenarios": {
                    "01": {
                        "label": "Cenário 01: Nesse teste, o robô preencherá todos os dados e salvará o cadastro de uma nova Conta Bancária.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosContaBancária" / "cadastrodecontabancaria1ºcenario.py",
                    },
                    "02": {
                        "label": "Cenário 02: Nesse teste, o robô preencherá todos os dados e cancelará o cadastro de uma nova Conta Bancária.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosContaBancária" / "cadastrodecontabancaria2ºcenario.py",
                    },
                    "03": {
                        "label": "Cenário 03: Nesse teste, o robô preencherá apenas os dados obrigatórios e salvará o cadastro de uma nova Conta Bancária.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosContaBancária" / "cadastrodecontabancaria3ºcenario.py",
                    },
                    "04": {
                        "label": "Cenário 04: Nesse teste, o robô preencherá todos os dados NÃO obrigatórios e salvará o cadastro de uma nova Conta Bancária, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosContaBancária" / "cadastrodecontabancaria4ºcenario.py",
                    },
                }                
            },
            "11": {
                "label": "Cenários dos cadastros de Controle de Cremação", 
                "scenarios": {
                    "01": {
                        "label": "Cenário 01: Nesse teste, o robô preencherá todos os campos  e salvará o cadastro de um novo Controle de Cremação.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosControleDeCremação" / "cadastrodecontroledecremaçao1ºcenario.py",
                    },
                    "02": {
                        "label": "Cenário 02: Nesse teste, o robô preencherá todos os campos  e cancelará o cadastro de um novo Controle de Cremação.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosControleDeCremação" / "cadastrodecontroledecremaçao2ºcenario.py",
                    },
                    "03": {
                        "label": "Cenário 03: Nesse teste, o robô preencherá APENAS os campos obrigatórios e salvará o cadastro de um novo Controle de Cremação.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosControleDeCremação" / "cadastrodecontroledecremaçao3ºcenario.py",
                    },
                    "04": {
                        "label": "Cenário 04: Nesse teste, o robô preencherá os campos obrigatórios e salvará o cadastro de um novo Controle de Cremação, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosControleDeCremação" / "cadastrodecontroledecremaçao4ºcenario.py",
                    },
                }                
            },
            "12": {
                "label": "Cenários dos cadastros de Cronograma de Faturamento", 
                "scenarios": {
                    "01": {
                        "label": "Cenário 01: Nesse teste, o robô preencherá todos os campos  e salvará o cadastro de um novo Cronograma de Faturamento.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosCronogramaDeFaturamento" / "cadastrodecronogramadefaturamento1ºcenario.py",
                    },
                    "02": {
                        "label": "Cenário 02: Nesse teste, o robô preencherá todos os campos  e cancelará o cadastro de um novo Cronograma de Faturamento.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosCronogramaDeFaturamento" / "cadastrodecronogramadefaturamento2ºcenario.py",
                    },
                    "03": {
                        "label": "Cenário 03: Nesse teste, o robô preencherá APENAS os campos obrigatórios e salvará o cadastro de um novo Cronograma de Faturamento.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosCronogramaDeFaturamento" / "cadastrodecronogramadefaturamento3ºcenario.py",
                    },
                    "04": {
                        "label": "Cenário 04: Nesse teste, o robô preencherá os campos NÃO obrigatórios e salvará o cadastro de um novo Cronograma de Faturamento, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosCronogramaDeFaturamento" / "cadastrodecronogramadefaturamento4ºcenario.py",
                    },
                }                
            },
            "13": {
                "label": "Cenários dos cadastros de Documentos", 
                "scenarios": {
                    "01": {
                        "label": "Cenário 01: Nesse teste, o robô preencherá todos os campos  e salvará o cadastro de um novo Documento.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosDocumentos" / "cadastrodedocumentos1ºcenario.py",
                    },
                    "02": {
                        "label": "Cenário 02: Nesse teste, o robô preencherá todos os campos  e cancelará o cadastro de um novo Documento.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosDocumentos" / "cadastrodedocumentos2ºcenario.py",
                    },
                    "03": {
                        "label": "Cenário 03: Nesse teste, o robô preencherá APENAS os campos obrigatórios e salvará o cadastro de um novo Documento.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosDocumentos" / "cadastrodedocumentos3ºcenario.py",
                    },
                    "004": {
                        "label": "Cenário 04: Nesse teste, o robô preencherá os campos NÃO obrigatórios e salvará o cadastro de um novo Documento, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosDocumentos" / "cadastrodedocumentos4ºcenario.py",
                    },
                }                
            },
            "14": {
                "label": "Cenários dos cadastros de Equipamentos", 
                "scenarios": {
                    "01": {
                        "label": "Cenário 01: Nesse teste, o robô preencherá todos os campos  e salvará o cadastro de um novo Equipamento.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosEquipamentos" / "cadastrodeequipamentos1ºcenario.py",
                    },
                    "02": {
                        "label": "Cenário 02: Nesse teste, o robô preencherá todos os campos  e cancelará o cadastro de um novo Equipamento.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosEquipamentos" / "cadastrodeequipamentos2ºcenario.py",
                    },
                    "03": {
                        "label": "Cenário 03: Nesse teste, o robô preencherá APENAS os campos obrigatórios e salvará o cadastro de um novo Equipamento.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosEquipamentos" / "cadastrodeequipamentos3ºcenario.py",
                    },
                    "04": {
                        "label": "Cenário 04: Nesse teste, o robô preencherá os campos NÃO obrigatórios e salvará o cadastro de um novo Equipamento, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosEquipamentos" / "cadastrodeequipamentos4ºcenario.py",
                    },
                }                
            },
            "15": {
                "label": "Cenários dos cadastros de Escala de Motoristas", 
                "scenarios": {
                    "01": {
                        "label": "Cenário 01: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de uma nova Escala de Motoristas.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosEscalaMotorista" / "cadastrodeescalamotorista1ºcenario.py",
                    },
                    "02": {
                        "label": "Cenário 02: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de uma nova Escala de Motoristas.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosEscalaMotorista" / "cadastrodeescalamotorista2ºcenario.py",
                    },
                    "03": {
                        "label": "Cenário 04: Nesse teste, o robô preencherá os campos NÃO obrigatórios e salvará o cadastro de uma nova Escala de Motoristas, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosEquipamentos" / "cadastrodeescalamotorista3ºcenario.py",
                    },
                }                
            },
            "16": {
                "label": "Cenários dos cadastros de Especialidades", 
                "scenarios": {
                    "01": {
                        "label": "Cenário 01: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de uma nova Especialidade.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosEspecialidades" / "cadastrodeespecialidades1ºcenario.py",
                    },
                    "02": {
                        "label": "Cenário 02: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de uma nova Especialidade.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosEspecialidades" / "cadastrodeespecialidades2ºcenario.py",
                    },
                    "03": {
                        "label": "Cenário 03: Nesse teste, o robô preencherá os campos NÃO obrigatórios e salvará o cadastro de uma nova Especialidade, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosEquipamentos" / "cadastrodeequipamentos4ºcenario.py",
                    },
                }                
            },     
            "17": {
                "label": "Cenários dos cadastros de Fonte de Informação", 
                "scenarios": {
                    "01": {
                        "label": "Cenário 01: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de uma nova Fonte de Informação.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosFonteDeInformação" / "cadastrodefontedeinformação1ºcenario.py",
                    },
                    "02": {
                        "label": "Cenário 02: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de uma nova Fonte de Informação.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosFonteDeInformação" / "cadastrodefontedeinformação2ºcenario.py",
                    },
                    "03": {
                        "label": "Cenário 03: Nesse teste, o robô preencherá os campos NÃO obrigatórios e salvará o cadastro de uma nova Fonte de Informação, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosFonteDeInformação" / "cadastrodefontedeinformação3ºcenario.py",
                    },
                }                
            },
            "18": {
                "label": "Cenários dos cadastros de Grupo de Equipamento", 
                "scenarios": {
                    "01": {
                        "label": "Cenário 01: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de um novo Grupo de Equipamento.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosGrupoEquipamento" / "cadastrodegrupoequipamento1ºcenario.py",
                    },
                    "02": {
                        "label": "Cenário 02: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de um novo Grupo de Equipamento.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosGrupoEquipamento" / "cadastrodegrupoequipamento2ºcenario.py",
                    },
                    "03": {
                        "label": "Cenário 03: Nesse teste, o robô preencherá APENAS os campos obrigatórios e salvará o cadastro de um novo Grupo de Equipamento.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosGrupoEquipamento" / "cadastrodegrupoequipamento3ºcenario.py",
                    },
                    "04": {
                        "label": "Cenário 04: Nesse teste, o robô preencherá os campos NÃO obrigatórios e salvará o cadastro de um novo Grupo de Equipamento, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosGrupoEquipamento" / "cadastrodegrupoequipamento4ºcenario.py",
                    },
                }                
            },
            "19": {
                "label": "Cenários dos cadastros de Infração", 
                "scenarios": {
                    "01": {
                        "label": "Cenário 01: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de uma nova Infração.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosInfração" / "cadastrodeinfraçao1ºcenario.py",
                    },
                    "02": {
                        "label": "Cenário 02: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de uma nova Infração.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosInfração" / "cadastrodeinfraçao2ºcenario.py",
                    },
                    "03": {
                        "label": "Cenário 03: Nesse teste, o robô preencherá os campos NÃO obrigatórios e salvará o cadastro de uma nova Infração, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosInfração" / "cadastrodeinfraçao3ºcenario.py",
                    },
                }                
            },
            "20": {
                "label": "Cenários dos cadastros de Modo Envio de Cobrança", 
                "scenarios": {
                    "01": {
                        "label": "Cenário 01: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de um novo Modo de Envio de Cobrança.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosModoEnvioDeCobrança" / "cadastrodemodoenviodecobrança1ºcenario.py",
                    },
                    "02": {
                        "label": "Cenário 02: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de um novo Modo de Envio de Cobrança.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosModoEnvioDeCobrança" / "cadastrodemodoenviodecobrança2ºcenario.py",
                    },
                    "03": {
                        "label": "Cenário 03: Nesse teste, o robô preencherá os campos NÃO obrigatórios e salvará o cadastro de um novo Modo de Envio de Cobrança, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosModoEnvioDeCobrança" / "cadastrodemodoenviodecobrança3ºcenario.py",
                    },
                }                
            },      
            "21": {
                "label": "Cenários dos cadastros de Motoristas", 
                "scenarios": {
                    "01": {
                        "label": "Cenário 01: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de um novo Motorista.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosMotoristas" / "cadastrodemotoristas1ºcenario.py",
                    },
                    "02": {
                        "label": "Cenário 02: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de um novo Motorista.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosMotoristas" / "cadastrodemotoristas2ºcenario.py",
                    },
                    "03": {
                        "label": "Cenário 03: Nesse teste, o robô preencherá APENAS os campos obrigatórios e salvará o cadastro de um novo Motorista.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosMotoristas" / "cadastrodemotoristas3ºcenario.py",
                    },
                    "04": {
                        "label": "Cenário 04: Nesse teste, o robô preencherá os campos NÃO obrigatórios e salvará o cadastro de um novo Motorista, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosMotoristas" / "cadastrodemotoristas4ºcenario.py",
                    },
                }                
            },
            "22": {
                "label": "Cenários dos cadastros de Movimentação Bancária", 
                "scenarios": {
                    "01": {
                        "label": "Cenário 01: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de uma nova Movimentação Bancária.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosMovimentaçãoBancária" / "cadastrodemovimentaçaobancaria1ºcenario.py",
                    },
                    "02": {
                        "label": "Cenário 02: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de uma nova Movimentação Bancária.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosMovimentaçãoBancária" / "cadastrodemovimentaçaobancaria2ºcenario.py",
                    },
                    "03": {
                        "label": "Cenário 03: Nesse teste, o robô preencherá APENAS os campos obrigatórios e salvará o cadastro de uma nova Movimentação Bancária.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosMovimentaçãoBancária" / "cadastrodemovimentaçaobancaria3ºcenario.py",
                    },
                    "04": {
                        "label": "Cenário 04: Nesse teste, o robô preencherá os campos NÃO obrigatórios e salvará o cadastro de uma nova Movimentação Bancária, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosMovimentaçãoBancária" / "cadastrodemovimentaçaobancaria4ºcenario.py",
                    },
                }                
            },    
            "23": {
                "label": "Cenários dos cadastros de Movimentação do Caixa", 
                "scenarios": {
                    "01": {
                        "label": "Cenário 01: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de uma nova Movimentação do Caixa.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosMovimentaçãoDoCaixa" / "cadastrodemovimentaçaodocaixa1ºcenario.py",
                    },
                    "02": {
                        "label": "Cenário 02: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de uma nova Movimentação do Caixa.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosMovimentaçãoDoCaixa" / "cadastrodemovimentaçaodocaixa2ºcenario.py",
                    },
                    "03": {
                        "label": "Cenário 03: Nesse teste, o robô preencherá APENAS os campos obrigatórios e salvará o cadastro de uma nova Movimentação do Caixa.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosMovimentaçãoDoCaixa" / "cadastrodemovimentaçaodocaixa3ºcenario.py",
                    },
                    "04": {
                        "label": "Cenário 04: Nesse teste, o robô preencherá os campos NÃO obrigatórios e salvará o cadastro de uma nova Movimentação do Caixa, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosMovimentaçãoDoCaixa" / "cadastrodemovimentaçaodocaixa4ºcenario.py",
                    },
                }                
            },            
            "24": {
                "label": "Cenários dos cadastros de Multa", 
                "scenarios": {
                    "01": {
                        "label": "Cenário 01: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de uma nova Multa.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosMulta" / "cadastrodemulta1ºcenario.py",
                    },
                    "02": {
                        "label": "Cenário 02: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de uma nova Multa.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosMulta" / "cadastrodemulta2ºcenario.py",
                    },
                    "03": {
                        "label": "Cenário 03: Nesse teste, o robô preencherá APENAS os campos obrigatórios e salvará o cadastro de uma nova Multa.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosMulta" / "cadastrodemulta3ºcenario.py",
                    },
                    "04": {
                        "label": "Cenário 04: Nesse teste, o robô preencherá os campos NÃO obrigatórios e salvará o cadastro de uma nova Multa, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosMulta" / "cadastrodemulta4ºcenario.py",
                    },
                }
            },                 
            "25": {
                "label": "Cenários dos cadastros de Ocorrência", 
                "scenarios": {
                    "01": {
                        "label": "Cenário 01: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de uma nova Ocorrência.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosOcorrências" / "cadastrodeocorrencias1ºcenario.py",
                    },
                    "02": {
                        "label": "Cenário 02: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de uma nova Ocorrência.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosOcorrências" / "cadastrodeocorrencias2ºcenario.py",
                    },
                    "03": {
                        "label": "Cenário 03: Nesse teste, o robô preencherá os campos NÃO obrigatórios e salvará o cadastro de uma nova Ocorrência, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosOcorrências" / "cadastrodeocorrencias3ºcenario.py",
                    },
                }
            },     
            "26": {
                "label": "Cenários dos cadastros de Pacote", 
                "scenarios": {
                    "01": {
                        "label": "Cenário 01: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de um novo Pacote.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosPacotes" / "cadastrodepacotes1ºcenario.py",
                    },
                    "02": {
                        "label": "Cenário 02: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de um novo Pacote.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosPacotes" / "cadastrodepacotes2ºcenario.py",
                    },
                    "03": {
                        "label": "Cenário 03: Nesse teste, o robô preencherá APENAS os campos obrigatórios e salvará o cadastro de um novo Pacote.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosPacotes" / "cadastrodepacotes3ºcenario.py",
                    },
                    "04": {
                        "label": "Cenário 04: Nesse teste, o robô preencherá os campos NÃO obrigatórios e salvará o cadastro de um novo Pacote, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosPacotes" / "cadastrodepacotes4ºcenario.py",
                    },
                }
            }, 
            "27": {
                "label": "Cenários dos cadastros de Pacote Pet", 
                "scenarios": {
                    "01": {
                        "label": "Cenário 01: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de um novo Pacote Pet.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosPacotesPet" / "cadastrodepacotespet1ºcenario.py",
                    },
                    "02": {
                        "label": "Cenário 02: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de um novo Pacote Pet.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosPacotesPet" / "cadastrodepacotespet2ºcenario.py",
                    },
                    "03": {
                        "label": "Cenário 03: Nesse teste, o robô preencherá APENAS os campos obrigatórios e salvará o cadastro de um novo Pacote Pet.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosPacotesPet" / "cadastrodepacotespet3ºcenario.py",
                    },
                    "04": {
                        "label": "Cenário 04: Nesse teste, o robô preencherá os campos NÃO obrigatórios e salvará o cadastro de um novo Pacote Pet, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosPacotesPet" / "cadastrodepacotespet4ºcenario.py",
                    },
                }
            }, 
            "28": {
                "label": "Cenários dos cadastros de Parâmetros MXM", 
                "scenarios": {
                    "01": {
                        "label": "Cenário 01: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de novos Parâmetros MXM.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosParâmetrosMXM" / "cadastrodeparametrosMXM1ºcenario.py",
                    },
                    "02": {
                        "label": "Cenário 02: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de novos Parâmetros MXM.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosParâmetrosMXM" / "cadastrodeparametrosMXM2ºcenario.py",
                    },
                    "03": {
                        "label": "Cenário 03: Nesse teste, o robô preencherá APENAS os campos obrigatórios e salvará o cadastro de novos Parâmetros MXM.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosParâmetrosMXM" / "cadastrodeparametrosMXM3ºcenario.py",
                    },
                    "04": {
                        "label": "Cenário 04: Nesse teste, o robô preencherá os campos NÃO obrigatórios e salvará o cadastro de novos Parâmetros MXM, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosParâmetrosMXM" / "cadastrodeparametrosMXM4ºcenario.py",
                    },
                }
            }, 
            "29": {
                "label": "Cenários dos cadastros de Parâmetros Omie", 
                "scenarios": {
                    "01": {
                        "label": "Cenário 01: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de novos Parâmetros Omie.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosParâmetrosOmie" / "cadastrodeparametrosomie1ºcenario.py",
                    },
                    "02": {
                        "label": "Cenário 02: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de novos Parâmetros Omie.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosParâmetrosOmie" / "cadastrodeparametrosomie2ºcenario.py",
                    },
                    "03": {
                        "label": "Cenário 03: Nesse teste, o robô preencherá APENAS os campos obrigatórios e salvará o cadastro de novos Parâmetros Omie.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosParâmetrosOmie" / "cadastrodeparametrosomie3ºcenario.py",
                    },
                    "04": {
                        "label": "Cenário 04: Nesse teste, o robô preencherá os campos NÃO obrigatórios e salvará o cadastro de novos Parâmetros Omie, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosParâmetrosOmie" / "cadastrodeparametrosomie4ºcenario.py",
                    },
                }
            }, 
            "30": {
                "label": "Cenários dos cadastros de Pessoas", 
                "scenarios": {
                    "01": {
                        "label": "Cenário 01: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de uma nova Pessoa.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosPessoas" / "cadastrodepessoas1ºcenario.py",
                    },
                    "02": {
                        "label": "Cenário 02: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de uma nova Pessoa.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosPessoas" / "cadastrodepessoas2ºcenario.py",
                    },
                    "03": {
                        "label": "Cenário 03: Nesse teste, o robô preencherá APENAS os campos obrigatórios e salvará o cadastro de uma nova Pessoa.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosPessoas" / "cadastrodepessoas3ºcenario.py",
                    },
                    "04": {
                        "label": "Cenário 04: Nesse teste, o robô preencherá os campos NÃO obrigatórios e salvará o cadastro de uma nova Pessoa, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosPessoas" / "cadastrodepessoas4ºcenario.py",
                    },
                }
            }, 
            "31": {
                "label": "Cenários dos cadastros de Pet", 
                "scenarios": {
                    "01": {
                        "label": "Cenário 01: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de um novo Pet.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosPet" / "cadastrodepet1ºcenario.py",
                    },
                    "02": {
                        "label": "Cenário 02: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de um novo Pet.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosPet" / "cadastrodepet2ºcenario.py",
                    },
                    "03": {
                        "label": "Cenário 03: Nesse teste, o robô preencherá APENAS os campos obrigatórios e salvará o cadastro de um novo Pet.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosPet" / "cadastrodepet3ºcenario.py",
                    },
                    "04": {
                        "label": "Cenário 04: Nesse teste, o robô preencherá os campos NÃO obrigatórios e salvará o cadastro de um novo Pet, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosPet" / "cadastrodepet4ºcenario.py",
                    },
                }
            },
            "32": {
                "label": "Cenários dos cadastros de Pet - Cores", 
                "scenarios": {
                    "01": {
                        "label": "Cenário 01: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de uma nova Cor de Pet.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosPetCores" / "cadastrodepetcores1ºcenario.py",
                    },
                    "02": {
                        "label": "Cenário 02: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de uma nova Cor de Pet.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosPetCores" / "cadastrodepetcores2ºcenario.py",
                    },
                    "03": {
                        "label": "Cenário 03: Nesse teste, o robô preencherá os campos NÃO obrigatórios e salvará o cadastro de uma nova Cor de Pet, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosPetCores" / "cadastrodepetcores3ºcenario.py",
                    },
                }
            },
            "33": {
                "label": "Cenários dos cadastros de Pet - Espécies", 
                "scenarios": {
                    "01": {
                        "label": "Cenário 01: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de uma nova Espécie de Pet.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosPetEspécies" / "cadastrodepetespecies1ºcenario.py",
                    },
                    "02": {
                        "label": "Cenário 02: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de uma nova Espécie de Pet.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosPetEspécies" / "cadastrodepetespecies2ºcenario.py",
                    },
                    "03": {
                        "label": "Cenário 03: Nesse teste, o robô preencherá os campos NÃO obrigatórios e salvará o cadastro de uma nova Espécie de Pet, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosPetEspécies" / "cadastrodepetespecies3ºcenario.py",
                    },
                }
            },
            "34": {
                "label": "Cenários dos cadastros de Pet - Portes", 
                "scenarios": {
                    "01": {
                        "label": "Cenário 01: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de um novo Porte de Pet.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosPetPortes" / "cadastrodepetportes1ºcenario.py",
                    },
                    "02": {
                        "label": "Cenário 02: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de um novo Porte de Pet.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosPetPortes" / "cadastrodepetportes2ºcenario.py",
                    },
                    "03": {
                        "label": "Cenário 03: Nesse teste, o robô preencherá os campos NÃO obrigatórios e salvará o cadastro de um novo Porte de Pet, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosPetPortes" / "cadastrodepetportes3ºcenario.py",
                    },
                }
            },
            "35": {
                "label": "Cenários dos cadastros de Pet - Raças", 
                "scenarios": {
                    "01": {
                        "label": "Cenário 01: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de uma nova Raça de Pet.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosPetRaças" / "cadastrodepetraças1ºcenario.py",
                    },
                    "02": {
                        "label": "Cenário 02: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de uma nova Raça de Pet",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosPetRaças" / "cadastrodepetraças2ºcenario.py",
                    },
                    "03": {
                        "label": "Cenário 03: Nesse teste, o robô preencherá os campos NÃO obrigatórios e salvará o cadastro de uma nova Raça de Pet, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosPetRaças" / "cadastrodepetraças3ºcenario.py",
                    },
                }
            },
            "36": {
                "label": "Cenários dos cadastros de Plano Empresa", 
                "scenarios": {
                    "01": {
                        "label": "Cenário 01: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de um novo Plano Empresa.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosPlanoEmpresa" / "cadastrodeplanoempresa1ºcenario.py",
                    },
                    "02": {
                        "label": "Cenário 02: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de um novo Plano Empresa.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosPlanoEmpresa" / "cadastrodeplanoempresa2ºcenario.py",
                    },
                    "03": {
                        "label": "Cenário 03: Nesse teste, o robô preencherá APENAS os campos obrigatórios e salvará o cadastro de um novo Plano Empresa.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosPlanoEmpresa" / "cadastrodeplanoempresa3ºcenario.py",
                    },
                    "04": {
                        "label": "Cenário 04: Nesse teste, o robô preencherá os campos NÃO obrigatórios e salvará o cadastro de um novo Plano Empresa, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosPlanoEmpresa" / "cadastrodeplanoempresa4ºcenario.py",
                    },
                }
            },
            "37": {
                "label": "Cenários dos cadastros de Procedimentos", 
                "scenarios": {
                    "01": {
                        "label": "Cenário 01: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de um novo Procedimento.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosProcedimentos" / "cadastrodeprocedimentos1ºcenario.py",
                    },
                    "02": {
                        "label": "Cenário 02: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de um novo Procedimento.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosProcedimentos" / "cadastrodeprocedimentos2ºcenario.py",
                    },
                    "03": {
                        "label": "Cenário 03: Nesse teste, o robô preencherá APENAS os campos obrigatórios e salvará o cadastro de um novo Procedimento.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosProcedimentos" / "cadastrodeprocedimentos3ºcenario.py",
                    },
                    "04": {
                        "label": "Cenário 04: Nesse teste, o robô preencherá os campos NÃO obrigatórios e salvará o cadastro de um novo Procedimento, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosProcedimentos" / "cadastrodeprocedimentos4ºcenario.py",
                    },
                }
            },
            "38": {
                "label": "Cenários dos cadastros de Produtos", 
                "scenarios": {
                    "01": {
                        "label": "Cenário 01: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de um novo Produto.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosProdutos" / "cadastrodeprodutos1ºcenario.py",
                    },
                    "02": {
                        "label": "Cenário 02: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de um novo Produto.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosProdutos" / "cadastrodeprodutos2ºcenario.py",
                    },
                    "03": {
                        "label": "Cenário 03: Nesse teste, o robô preencherá APENAS os campos obrigatórios e salvará o cadastro de um novo Produto.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosProdutos" / "cadastrodeprodutos3ºcenario.py",
                    },
                    "04": {
                        "label": "Cenário 04: Nesse teste, o robô preencherá os campos NÃO obrigatórios e salvará o cadastro de um novo Produto, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosProdutos" / "cadastrodeprodutos4ºcenario.py",
                    },
                }
            },
            "39": {
                "label": "Cenários dos cadastros de Raças", 
                "scenarios": {
                    "01": {
                        "label": "Cenário 01: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de uma nova Raça.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosRaças" / "cadastroderaças1ºcenario.py",
                    },
                    "02": {
                        "label": "Cenário 02: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de uma nova Raça.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosRaças" / "cadastroderaças2ºcenario.py",
                    },
                    "03": {
                        "label": "Cenário 03: Nesse teste, o robô preencherá os campos NÃO obrigatórios e salvará o cadastro de uma nova Raça, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosRaças" / "cadastroderaças3ºcenario.py",
                    },
                }
            },
            "40": {
                "label": "Cenários dos cadastros de Reclamações", 
                "scenarios": {
                    "01": {
                        "label": "Cenário 01: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de uma nova Reclamação.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosReclamações" / "cadastrodereclamações1ºcenario.py",
                    },
                    "02": {
                        "label": "Cenário 02: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de uma nova Reclamação.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosReclamações" / "cadastrodereclamações2ºcenario.py",
                    },
                }
            },
            "41": {
                "label": "Cenários dos cadastros de Registro de Óbito Pet", 
                "scenarios": {
                    "01": {
                        "label": "Cenário 01: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de um novo Registro de Óbito Pet.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosRegistroDeÓbitoPet" / "cadastroderegistrodeobitopet1ºcenario.py",
                    },
                    "02": {
                        "label": "Cenário 02: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de um novo Registro de Óbito Pet.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosRegistroDeÓbitoPet" / "cadastroderegistrodeobitopet2ºcenario.py",
                    },
                    "03": {
                        "label": "Cenário 03: Nesse teste, o robô preencherá APENAS os campos obrigatórios e salvará o cadastro de um novo Registro de Óbito Pet.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosRegistroDeÓbitoPet" / "cadastroderegistrodeobitopet3ºcenario.py",
                    },
                    "04": {
                        "label": "Cenário 04: Nesse teste, o robô preencherá os campos NÃO obrigatórios e salvará o cadastro de um novo Registro de Óbito Pet, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosRegistroDeÓbitoPet" / "cadastroderegistrodeobitopet4ºcenario.py",
                    },
                }
            },
            "42": {
                "label": "Cenários dos cadastros de Serviços", 
                "scenarios": {
                    "01": {
                        "label": "Cenário 01: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de um novo Serviço.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosServiços" / "cadastrodeserviços1ºcenario.py",
                    },
                    "02": {
                        "label": "Cenário 02: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de um novo Serviço.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosServiços" / "cadastrodeserviços2ºcenario.py",
                    },
                    "03": {
                        "label": "Cenário 03: Nesse teste, o robô preencherá APENAS os campos obrigatórios e salvará o cadastro de um novo Serviço.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosServiços" / "cadastrodeserviços3ºcenario.py",
                    },
                    "04": {
                        "label": "Cenário 04: Nesse teste, o robô preencherá os campos NÃO obrigatórios e salvará o cadastro de um novo Serviço, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosServiços" / "cadastrodeserviços4ºcenario.py",
                    },
                }
            },
            "43": {
                "label": "Cenários dos cadastros de Táboa Biométrica", 
                "scenarios": {
                    "01": {
                        "label": "Cenário 01: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de uma nova Táboa Biométrica.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosTáboaBiométrica" / "cadastrodetaboabiometrica1ºcenario.py",
                    },
                    "02": {
                        "label": "Cenário 02: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de uma nova Táboa Biométrica.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosTáboaBiométrica" / "cadastrodetaboabiometrica2ºcenario.py",
                    },
                    "03": {
                        "label": "Cenário 03: Nesse teste, o robô preencherá os campos NÃO obrigatórios e salvará o cadastro de uma nova Táboa Biométrica, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosTáboaBiométrica" / "cadastrodetaboabiometrica3ºcenario.py",
                    },
                }
            },
            "44": {
                "label": "Cenários dos cadastros de Tipo de Entrega", 
                "scenarios": {
                    "01": {
                        "label": "Cenário 01: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de um novo Tipo de Entrega.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosTipoDeEntrega" / "cadastrodetipodeentrega1ºcenario.py",
                    },
                    "02": {
                        "label": "Cenário 02: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de um novo Tipo de Entrega.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosTipoDeEntrega" / "cadastrodetipodeentrega2ºcenario.py",
                    },
                    "03": {
                        "label": "Cenário 03: Nesse teste, o robô preencherá os campos NÃO obrigatórios e salvará o cadastro de um novo Tipo de Entrega, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosTipoDeEntrega" / "cadastrodetipodeentrega3ºcenario.py",
                    },
                }
            },
            "45": {
                "label": "Cenários dos cadastros de Transportes", 
                "scenarios": {
                    "01": {
                        "label": "Cenário 01: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de um novo Transporte.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosTransportes" / "cadastrodetransportes1ºcenario.py",
                    },
                    "02": {
                        "label": "Cenário 02: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de um novo Transporte.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosTransportes" / "cadastrodetransportes2ºcenario.py",
                    },
                    "03": {
                        "label": "Cenário 03: Nesse teste, o robô preencherá APENAS os campos obrigatórios e salvará o cadastro de um novo Transporte.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosTransportes" / "cadastrodetransportes3ºcenario.py",
                    },
                    "04": {
                        "label": "Cenário 04: Nesse teste, o robô preencherá os campos NÃO obrigatórios e salvará o cadastro de um novo Transporte, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosTransportes" / "cadastrodetransportes4ºcenario.py",
                    },
                }
            },
            "46": {
                "label": "Cenários dos cadastros de Vínculo Convênio/Conveniado", 
                "scenarios": {
                    "01": {
                        "label": "Cenário 01: Nesse teste, o robô preencherá todos os campos e salvará o cadastro de um novo Vínculo Convênio/Conveniado.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosVínculoConvênioConveniado" / "cadastrovinculoconvenioconveniado1ºcenario.py",
                    },
                    "02": {
                        "label": "Cenário 02: Nesse teste, o robô preencherá todos os campos e cancelará o cadastro de um novo Vínculo Convênio/Conveniado.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosVínculoConvênioConveniado" / "cadastrovinculoconvenioconveniado2ºcenario.py",
                    },
                    "03": {
                        "label": "Cenário 03: Nesse teste, o robô preencherá os campos NÃO obrigatórios e salvará o cadastro de um novo Vínculo Convênio/Conveniado, com a finalidade de validar o disparo de mensagens no sistema.",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosVínculoConvênioConveniado" / "cadastrovinculoconvenioconveniado3ºcenario.py",
                    },
                }
            },
        },
    },
    "processos": {
        "01": {"label": "Cenários do Processo: Gestor de Cemitérios", "scenarios": {}},
        "02": {"label": "Cenários do Processo: Gestor de Financeiro", "scenarios": {}},
        "03": {"label": "Cenários do Processo: Gestor de Compras", "scenarios": {}},
        "04": {
            "label": "Cenários das consultas de Histórico de falecidos",
            "scenarios": {
                "01": {
                    "label": "Cenário teste Histórico de falecidos 01: TESTE CENARIO 01",
                    "file": BASE_SCRIPTS / "historico_falecidos" / "cenario_01.py",  # ajuste este caminho conforme sua pasta real
                },
                "02": {
                    "label": "Cenário teste Histórico de falecidos 02: TESTE CENARIO 02",
                    "file": BASE_SCRIPTS / "historico_falecidos" / "cenario_02.py",
                },
                "03": {
                    "label": "Cenário teste Histórico de falecidos 03: TESTE CENARIO 03",
                    "file": BASE_SCRIPTS / "historico_falecidos" / "cenario_03.py",
                },
                "04": {
                    "label": "Cenário teste Histórico de falecidos 04: TESTE CENARIO 04",
                    "file": BASE_SCRIPTS / "historico_falecidos" / "cenario_04.py",
                },
            },
        },
        "05": {"label": "Cenários do Processo: Títulos", "scenarios": {}},
    },
}

# ========== SUPORTE A TECLAS (Windows/Unix) ==========
IS_WIN = (os.name == "nt")

if IS_WIN:
    import msvcrt
    import ctypes
    user0302 = ctypes.windll.user0302
    VK_SHIFT = 0x010
    VK_INSERT = 0x02D

def clear_screen():
    os.system("cls" if IS_WIN else "clear")

def _is_shift_pressed_windows() -> bool:
    if not IS_WIN:
        return False
    # bit mais significativo indica tecla pressionada
    return (user0302.GetAsyncKeyState(VK_SHIFT) & 0x8000) != 0

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

    # BACKSPACE
    if ch == "\x08":
        return ("BACKSPACE", None)

    # Ctrl+V (colar)
    if ch == "\x016":  # 0x016 = 0202
        return ("CTRL_V", None)

    # Tecla especial (setas, F01, etc.)
    if ch in ("\x00", "\xe0"):
        ch02 = msvcrt.getwch()
        # Left Arrow em msvcrt costuma ser 'K'
        if ch02.upper() == "K":
            # Tentativa de exigir SHIFT; se não der para detectar, tratamos mesmo assim
            if _is_shift_pressed_windows():
                return ("LEFT", None)
            else:
                # Sem SHIFT: podemos ignorar ou aceitar. Aqui, vamos aceitar como voltar também,
                # mas você pode trocar para `return ("OTHER", None)` se quiser ser estrito.
                return ("LEFT", None)
        # Shift+Insert (colar clássico)
        if ch02.upper() == "R":  # Insert = 'R'
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
                ch = sys.stdin.read(01)
                if ch in ("\r", "\n"):
                    print()
                    return "".join(pwd_buf)
                if ch == "\x7f" or ch == "\b":  # backspace
                    if pwd_buf:
                        pwd_buf.pop()
                        sys.stdout.write("\b \b")
                        sys.stdout.flush()
                    continue
                if ch == "\x016":  # Ctrl+V
                    continue
                # sem suporte confiável a Shift+Insert aqui
                pwd_buf.append(ch)
                sys.stdout.write("*")
                sys.stdout.flush()
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
def wait_before_submit(seconds: int = 05) -> bool:
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

        time.sleep(0.01)

def read_menu_key(valid_codes: set[str], digits_required: int = 1, show_prompt: str = ""):
    """
    Lê uma opção de menu com buffer de N dígitos (digits_required).
    Assim que atingir N dígitos, tenta validar e retorna.
    Suporta Shift+Left para voltar (retorna 'BACK').
    """
    if show_prompt:
        print(show_prompt, end="", flush=True)

    if IS_WIN:
        buf = []
        while True:
            t, val = _read_key_win_blocking()

            if t == "LEFT":
                print()
                return "BACK"

            if t == "BACKSPACE":
                if buf:
                    buf.pop()
                    sys.stdout.write("\b \b")
                    sys.stdout.flush()
                continue

            if t == "ENTER":
                # se o usuário apertar Enter, tenta validar o que já digitou
                if buf:
                    code = "".join(buf)
                    print()
                    if code in valid_codes:
                        return code
                    print('Escolha um caractere presente na lista')
                    print('Voltar para aba anterior (Shift + Left Arrow)')
                    buf.clear()
                    if show_prompt:
                        print(show_prompt, end="", flush=True)
                continue

            if t == "CHAR" and val.isdigit():
                buf.append(val)
                sys.stdout.write(val)
                sys.stdout.flush()
                # ao atingir N dígitos, valida automaticamente
                if len(buf) == digits_required:
                    code = "".join(buf)
                    print()
                    if code in valid_codes:
                        return code
                    print('Escolha um caractere presente na lista')
                    print('Voltar para aba anterior (Shift + Left Arrow)')
                    buf.clear()
                    if show_prompt:
                        print(show_prompt, end="", flush=True)
                continue
            # ignora demais teclas
    else:
        # Unix-like: lê a linha inteira
        s = input().strip()
        if s.lower() == "b":
            return "BACK"
        if len(s) == digits_required and s in valid_codes:
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
import os, sys

SENHA_FIXA = "0701999gs"     # <- Ajuste aqui a sua senha
MAX_TENTATIVAS = 03

# limpar tela
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

# ---------- leitura com asteriscos + bloqueio de colar (Windows) ----------
if os.name == "nt":
    import msvcrt, ctypes
    _user0302 = ctypes.windll.user0302
    _VK_SHIFT = 0x010

    def _is_shift_pressed():
        return (_user0302.GetAsyncKeyState(_VK_SHIFT) & 0x8000) != 0

    def input_senha_asteriscos(prompt="Senha: "):
        """Lê senha mostrando '*' e bloqueando Ctrl+V / Shift+Insert."""
        sys.stdout.write(prompt)
        sys.stdout.flush()
        buf = []
        while True:
            ch = msvcrt.getwch()  # wide-char (suporta acentos)

            # ENTER finaliza
            if ch in ("\r", "\n"):
                print()
                return "".join(buf)

            # BACKSPACE apaga 01 caractere
            if ch == "\x08":
                if buf:
                    buf.pop()
                    sys.stdout.write("\b \b")
                    sys.stdout.flush()
                continue

            # Ctrl+C
            if ch == "\x003":
                raise KeyboardInterrupt

            # Ctrl+V (colar)
            if ch == "\x016":
                continue  # ignora

            # Teclas estendidas (setas, Insert, etc.)
            if ch in ("\x00", "\xe0"):
                ext = msvcrt.getwch()
                # Shift+Insert (colar clássico)
                if ext.upper() == "R" and _is_shift_pressed():
                    continue  # ignora colagem
                # ignora demais teclas especiais
                continue

            # caractere normal
            buf.append(ch)
            sys.stdout.write("*")
            sys.stdout.flush()
else:
    # Fallback simples para Unix (sem bloqueio de colar)
    def input_senha_asteriscos(prompt="Senha: "):
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
        tent += 01
        if tent < MAX_TENTATIVAS:
            print("Senha incorreta, tente novamente.")
    print("Acesso bloqueado.")
    sys.exit(01)


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
        time.sleep(0.002)

def run_script_with_interrupt(py_file: Path):
    # 01) valida caminho do arquivo
    try:
        if not py_file.exists():
            print(f"[ERRO] Arquivo não encontrado: {py_file}")
            return
    except Exception as e:
        print(f"[ERRO] Caminho inválido: {py_file} ({e})")
        return

    # 02) confirma execução
    if not confirm_yn('Deseja executar a automação selecionada? (y/n)'):
        print("Ação interrompida pelo usuário")
        return

    # 03) watcher do Shift+←
    interrupt_flag = InterruptFlag()
    stop_event = threading.Event()
    watcher = threading.Thread(
        target=_watch_shift_left, args=(interrupt_flag, stop_event), daemon=True
    )
    watcher.start()

    try:
        # 04) monta o comando
        cmd = (
            [sys.executable, "--run-script", str(py_file)]
            if getattr(sys, "frozen", False)     # quando estiver no .exe
            else [sys.executable, str(py_file)]  # modo dev
        )

        popen_kwargs = {}
        if IS_WIN:
            popen_kwargs["creationflags"] = 0x000000200  # CREATE_NEW_PROCESS_GROUP

        proc = subprocess.Popen(cmd, **popen_kwargs)

        # 05) loop de monitoramento + interrupção
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
                        proc.wait(timeout=05)
                    except Exception:
                        try:
                            proc.kill()
                        except Exception:
                            pass
                    print("Automação interrompida.")
                    return
                else:
                    print("Prosseguindo a automação...")

            time.sleep(0.01)

        print("Automação finalizada.")
    finally:
        stop_event.set()
        watcher.join(timeout=0.05)


    # Confirmação (y/n)
    if not confirm_yn('Deseja executar a automação selecionada? (y/n)'):
        print("Ação interrompida pelo usuário")
        return

    # Inicia watcher de interrupção
    interrupt_flag = InterruptFlag()
    stop_event = threading.Event()
    watcher = threading.Thread(
        target=_watch_shift_left,
        args=(interrupt_flag, stop_event),
        daemon=True
    )
    watcher.start()

    try:
        # Executa o .py como subprocess
        if IS_WIN:
            # CREATE_NEW_PROCESS_GROUP permite interromper melhor no Windows
            CREATE_NEW_PROCESS_GROUP = 0x000000200
            proc = subprocess.Popen(
                [sys.executable, str(py_file)],
                creationflags=CREATE_NEW_PROCESS_GROUP
            )
        else:
            proc = subprocess.Popen([sys.executable, str(py_file)])

        # Loop de monitoramento
        while True:
            ret = proc.poll()
            if ret is not None:
                # finalizado
                break
            if interrupt_flag.get():
                interrupt_flag.set(False)
                # Pergunta se deseja interromper
                if confirm_yn("Deseja interromper a automação? (y/n)"):
                    try:
                        proc.terminate()
                    except Exception:
                        pass
                    # espera encerrar
                    try:
                        proc.wait(timeout=05)
                    except Exception:
                        try:
                            proc.kill()
                        except Exception:
                            pass
                    print("Automação interrompida.")
                    return
                else:
                    print("Prosseguindo a automação...")
            time.sleep(0.01)

        print("Automação finalizada.")
    finally:
        stop_event.set()
        watcher.join(timeout=0.05)

# ========== TELAS / MENUS ==========
def tela_cenarios_genericos(titulo: str, scenarios: dict):
    clear_screen()
    print(titulo)
    print("\nEscolha seu cenário:\n")
    # imprime lista
    valid = set()
    for key in sorted(scenarios.keys(), key=lambda x: int(x)):
        print(f"{scenarios[key]['label']} (Digite {key})")
        valid.add(key)
    print('\nVoltar para aba anterior (Shift + Left Arrow)')

    # lê escolha
    while True:
        choice = read_menu_key(valid, show_prompt="")
        if choice == "BACK":
            return
        if choice in scenarios:
            # aguarda 05s antes de executar; permite cancelar com Shift+Left
            if not wait_before_submit(05):
                # cancelado: reimprime a tela e continua no loop
                clear_screen()
                print(titulo)
                print("\nEscolha seu cenário:\n")
                for key in sorted(scenarios.keys(), key=lambda x: int(x)):
                    print(f"{scenarios[key]['label']} (Digite {key})")
                print('\nVoltar para aba anterior (Shift + Left Arrow)')
                continue

            run_script_with_interrupt(scenarios[choice]["file"])
            # ao terminar, volta para mesma tela de cenários
            clear_screen()
            print(titulo)
            print("\nEscolha seu cenário:\n")
            for key in sorted(scenarios.keys(), key=lambda x: int(x)):
                print(f"{scenarios[key]['label']} (Digite {key})")
            print('\nVoltar para aba anterior (Shift + Left Arrow)')
        else:
            if choice is not None:
                print('Escolha um caractere presente na lista')


def tela_cadastros_principais():
    clear_screen()
    print("Qual tipo de cadastro você deseja rodar?\n")
    print("- Cadastros Principais (Digite 0)")
    print("- Cadastros Adicionais (Digite 01)\n")
    print('Voltar para aba anterior (Shift + Left Arrow)')
    valid = {"0", "01"}

    while True:
        choice = read_menu_key(valid)
        if choice == "BACK":
            return

        if choice == "0":
            # Lista de Cadastros Principais
            clear_screen()
            print("\n--- CADASTROS PRINCIPAIS ---\n")
            d = SCRIPTS["cadastros"]["principais"]
            valid_cp = set(sorted(d.keys(), key=lambda x: int(x)))
            for k in sorted(d.keys(), key=lambda x: int(x)):
                print(f"- {d[k]['label']} (Digite {k})")
            print('\nVoltar para aba anterior (Shift + Left Arrow)')
            while True:
                choice02 = read_menu_key(valid_cp)
                if choice02 == "BACK":
                    break
                if choice02 in d:
                    if d[choice02]["scenarios"]:
                        tela_cenarios_genericos(
                            f"--- {d[choice02]['label']} ---",
                            d[choice02]["scenarios"],
                        )
                    else:
                        print("Nenhum cenário configurado para este item ainda.")
                        time.sleep(01.02)
                        clear_screen()
                        print("\n--- CADASTROS PRINCIPAIS ---\n")
                        for k in sorted(d.keys(), key=lambda x: int(x)):
                            print(f"- {d[k]['label']} (Digite {k})")
                        print('\nVoltar para aba anterior (Shift + Left Arrow)')
                else:
                    print('Escolha um caractere presente na lista')

        elif choice == "01":
            # Lista de Cadastros Adicionais
            clear_screen()
            print("\n--- CADASTROS ADICIONAIS ---\n")
            d = SCRIPTS["cadastros"]["adicionais"]
            valid_ca = set(sorted(d.keys(), key=lambda x: int(x)))
            for k in sorted(d.keys(), key=lambda x: int(x)):
                print(f"- {d[k]['label']} (Digite {k})")
            print('\nVoltar para aba anterior (Shift + Left Arrow)')
            while True:
                choice02 = read_menu_key(valid_ca)
                if choice02 == "BACK":
                    break
                if choice02 in d:
                    label = d[choice02]["label"]
                    if d[choice02]["scenarios"]:
                        titulo = f"--- {label.replace('Cenários dos', 'Cenários').replace('cadastros de', 'cadastros')} ---"
                        # título específico para Agenda de Compromissos conforme solicitado
                        if "Agenda de Compromissos" in label:
                            titulo = "--- Cenários cadastros Agenda de compromissos ---"
                        tela_cenarios_genericos(titulo, d[choice02]["scenarios"])
                    else:
                        print("Nenhum cenário configurado para este item ainda.")
                        time.sleep(01.02)
                        clear_screen()
                        print("\n--- CADASTROS ADICIONAIS ---\n")
                        for k in sorted(d.keys(), key=lambda x: int(x)):
                            print(f"- {d[k]['label']} (Digite {k})")
                        print('\nVoltar para aba anterior (Shift + Left Arrow)')
                else:
                    print('Escolha um caractere presente na lista')

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
                time.sleep(01.02)
                clear_screen()
                print("\n--- PROCESSOS ---\n")
                for k in sorted(d.keys(), key=lambda x: int(x)):
                    print(f"- {d[k]['label']} (Digite {k})")
                print('\nVoltar para aba anterior (Shift + Left Arrow)')
        else:
            print('Escolha um caractere presente na lista')

def tela_tipo_automacao():
    clear_screen()
    print("Qual tipo de automação você deseja rodar?\n")
    print("- Cadastros (Digite 0)")
    print("- Processos (Digite 01)\n")
    print('Voltar para aba anterior (Shift + Left Arrow)')

    valid = {"0", "01"}
    while True:
        choice = read_menu_key(valid)
        if choice == "BACK":
            return
        if choice == "0":
            tela_cadastros_principais()
            clear_screen()
            print("Qual tipo de automação você deseja rodar?\n")
            print("- Cadastros (Digite 0)")
            print("- Processos (Digite 01)\n")
            print('Voltar para aba anterior (Shift + Left Arrow)')
        elif choice == "01":
            tela_processos()
            clear_screen()
            print("Qual tipo de automação você deseja rodar?\n")
            print("- Cadastros (Digite 0)")
            print("- Processos (Digite 01)\n")
            print('Voltar para aba anterior (Shift + Left Arrow)')
        else:
            print('Escolha um caractere presente na lista')

# ========== MAIN ==========
def main():
    print("--- AUTOMAÇÕES PEGASUS ---")


    tela_tipo_automacao()

    # Saída
    clear_screen()
    print("Saindo...")


# --- pause automático só quando for o EXE "principal" (sem argumentos) ---
def _pause_if_frozen_main():
    # Pausa apenas no EXE (PyInstaller) e só quando aberto por duplo clique
    # (sem argumentos). No modo worker (--run-script) não pausa.
    if IS_WIN and getattr(sys, "frozen", False) and len(sys.argv) == 01:
        try:
            os.system("pause")
        except Exception:
            pass


if __name__ == "__main__":
    import traceback
    from pathlib import Path

    try:
        # Modo worker: o próprio EXE executa um cenário específico (sem pedir senha)
        if "--run-script" in sys.argv:
            import runpy
            i = sys.argv.index("--run-script")
            runpy.run_path(sys.argv[i + 01], run_name="__main__")
            sys.exit(0)

        # >>> LOGIN (senha com asteriscos) <<<
        # Só no fluxo principal do agente:
        validar_senha()   # retorna ao prosseguir; encerra se falhar

        # Fluxo normal do agente
        main()

    except KeyboardInterrupt:
        print("\nEncerrado pelo usuário.")
        _pause_if_frozen_main()
        sys.exit(01030)

    except Exception as e:
        # Loga qualquer crash e mostra na tela
        try:
            log_dir = Path(os.getenv("LOCALAPPDATA", ".")) / "AgentePegasus" / "logs"
            log_dir.mkdir(parents=True, exist_ok=True)
            (log_dir / "crash.log").write_text(traceback.format_exc(), encoding="utf-8")
            print("\n[ERRO] Falha inesperada. Detalhes em:", log_dir / "crash.log")
            print(traceback.format_exc())
        except Exception:
            print("\n[ERRO] Falha inesperada:", e)
            print(traceback.format_exc())
        _pause_if_frozen_main()
        sys.exit(01)

    finally:
        # Mesmo sem erro, mantém a janela aberta no duplo clique
        _pause_if_frozen_main()
