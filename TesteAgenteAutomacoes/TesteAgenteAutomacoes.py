#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Runner de automações Pegasus — fluxo com CAPA pós-autenticação
Menus específicos + breadcrumb de caminho atual (inclusive em cada cadastro)
"""
from __future__ import annotations
import os, sys, time, traceback, subprocess
from pathlib import Path
import shutil
import re
from datetime import datetime
from typing import Dict, Any, Tuple
from qa_reporter import QAReporter  # <-- usar o seu qa_reporter.py
from subprocess import Popen, PIPE

import sys
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


IS_WINDOWS = (os.name == "nt")
if IS_WINDOWS:
    import ctypes, msvcrt

FROZEN = getattr(sys, "frozen", False)
BASE_DIR = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent)) if FROZEN else Path(__file__).resolve().parent
BASE_SCRIPTS = BASE_DIR / "cenariostestespegasus"

RUN_ID = datetime.now().strftime("%Y%m%d_%H%M%S_") + os.urandom(3).hex()
DESKTOP = Path(os.path.expanduser("~/Desktop"))
OUT_BASE = DESKTOP / "AutomacoesPegasus" / f"RUN_{RUN_ID}"
DIR_REPORTS = OUT_BASE / "reports"
for d in (DIR_REPORTS,):
    d.mkdir(parents=True, exist_ok=True)

# ===== Helpers de execução/parse de logs =====
import re
from pathlib import Path
import subprocess

ERROR_TAG   = re.compile(r'(?i)mensagem\s*de\s*erro\s*:\s*(.+)')
TRACEBACK   = re.compile(r'Traceback \(most recent call last\):')
SUCCESS_TAG = re.compile(r'(?i)\b(realizad[ao]|concluíd[ao])\s+com\s+sucesso\b')

def parse_result(stdout_text: str, returncode: int):
    """
    Converte o texto do log + returncode em ('OK'|'FAIL', 'mensagem de erro'|'' )
    Regras:
      - Se achar 'Mensagem de Erro:' => FAIL
      - Se achar Traceback => FAIL
      - Se achar '... com sucesso' => OK
      - Caso contrário, usa o returncode
    """
    clean = re.sub(r'\S+\.(png|jpg|jpeg)', '[arquivo]', stdout_text)  # ruído
    m = ERROR_TAG.search(clean)
    if m:
        return 'FAIL', m.group(1).strip()
    if TRACEBACK.search(clean):
        return 'FAIL', 'Exceção (Traceback) detectada no log'
    if SUCCESS_TAG.search(clean):
        return 'OK', ''
    return ('FAIL', 'Falha sem mensagem') if returncode != 0 else ('OK', '')

def save_full_log(base_reports_dir: Path, scenario_label: str, text: str) -> Path:
    """Salva o log completo do cenário dentro de reports/logs/"""
    p = Path(base_reports_dir) / "logs"
    p.mkdir(parents=True, exist_ok=True)
    fp = p / f"{scenario_label}.log.txt"
    fp.write_text(text, encoding="utf-8", errors="replace")
    return fp

def execute_scenario(label_exec: str, cmd, cwd: Path | None, reports_dir: Path):
    """
    Executa o comando do cenário, captura stdout+stderr (UTF-8, sem cortar),
    salva o log e devolve (status, err_msg, log_path, rc, log_txt)
    """
    proc = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        shell=isinstance(cmd, str),
        cwd=str(cwd) if cwd else None,
    )
    stdout = proc.stdout or ""
    stderr = proc.stderr or ""
    log_txt = stdout + ("\n-- STDERR --\n" + stderr if stderr else "")
    status, err_msg = parse_result(log_txt, proc.returncode)
    log_path = save_full_log(reports_dir, label_exec, log_txt)
    return status, err_msg, log_path, proc.returncode, log_txt
# ===== Fim helpers =====


try:
    from qa_reporter import QAReporter
except Exception:
    QAReporter = None

def clear_screen():
    os.system("cls" if IS_WINDOWS else "clear")

def show_loading():
    clear_screen()
    print("Carregando... Estamos preparando tudo pra você.", end="", flush=True)
    for _ in range(10):  # ~1,2s
        time.sleep(0.12)
        print(".", end="", flush=True)
    time.sleep(0.2)
    clear_screen()

def log(doc, msg):
    try:
        print(msg)
    except UnicodeEncodeError:
        print(msg.encode("ascii", "ignore").decode("ascii"))
    doc.add_paragraph(msg)


# Por este (não mostra * à toa nos menus):
def read_input_with_hotkeys(prompt: str = "") -> str:
    return input(prompt)


# Substitua a função de senha por esta:
def read_password_masked(prompt: str = "Digite a senha para entrar: ") -> str:
    import sys
    if os.name != "nt":
        # Em Linux/macOS: mantém o getpass (sem * por padrão)
        import getpass
        return getpass.getpass(prompt)

    # Em Windows: exibe * enquanto digita
    import msvcrt
    sys.stdout.write(prompt)
    sys.stdout.flush()
    buf = []
    while True:
        ch = msvcrt.getwch()
        if ch in ("\r", "\n"):
            sys.stdout.write("\n")
            return "".join(buf)
        if ch == "\x08":  # backspace
            if buf:
                buf.pop()
                sys.stdout.write("\b \b")
                sys.stdout.flush()
            continue
        if ch == "\x1b":  # ESC limpa a linha
            while buf:
                buf.pop()
                sys.stdout.write("\b \b")
                sys.stdout.flush()
            continue
        # ignora teclas de função/setas (prefixos \x00 ou \xe0)
        if ch in ("\x00", "\xe0"):
            msvcrt.getwch()  # consome o segundo byte
            continue
        buf.append(ch)
        sys.stdout.write("*")
        sys.stdout.flush()


PEGASUS_PASSWORD = os.getenv("PEGASUS_PASSWORD", "071999gs")


def autenticar() -> bool:
    clear_screen()
    print("===== AUTOMAÇÕES PEGASUS =====\n")
    pwd = read_password_masked("Digite a senha para entrar: ")
    if not pwd:
        print("\n[ERRO] Senha vazia.")
        time.sleep(1.2)
        return False
    if pwd != PEGASUS_PASSWORD:
        print("\n[ERRO] Senha incorreta.")
        time.sleep(1.2)
        return False
    return True

def main():
    show_loading()                  # splash inicial
    if not autenticar():
        sys.exit(1)

    show_loading()                  # pós-login, preparando a capa
    root = {**SCRIPTS}
    menu_pos_login(root)


# ===================== BASE DE CENÁRIOS =====================

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
                        "label": 'Cenário 4: Nesse teste, o robô preencherá os campos NÃO obrigatórios e salvará o cadastro de um novo Abastecimento, com a finalidade de validar o disparo de mensagens no sistema.',
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
                        "label": 'Cenário 4: Nesse teste, serão preenchidos APENAS os campos NÃO obrigatórios, e clicará em "Salvar", para disparo de alertas.',
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
                        "label": "Cenário 4: TESTE CENARIO 4",
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


# ---------- helpers de execução ----------



FROZEN = getattr(sys, "frozen", False)

def _python_cmd():
    if getattr(sys, "frozen", False) is False and sys.executable:
        return [sys.executable]
    for name in ("py", "python", "python3"):
        p = shutil.which(name)
        if p:
            return [p]
    return ["python"]



ERROR_RX = re.compile(r'^.*Mensagem de Erro.*$', re.IGNORECASE | re.MULTILINE)

# Flag do Windows para não abrir console no processo-filho
CREATE_NO_WINDOW = 0x08000000 if os.name == "nt" else 0


def _run_cenario_and_classify(path: Path, idx: int | None = None, total: int | None = None):
    """
    Executa o cenário SEM console do filho (evita 'cls' limpar sua tela),
    captura stdout/stderr, e imprime o log ao final em bloco.
    Retorna: (returncode, status, error_snippet, full_log)
    """
    path = Path(path).resolve()
    header = f"\nExecutando {path}"
    if idx is not None and total is not None:
        header += f" [{idx}/{total}]"
    print(header)

    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"

    # opcional: deixa seu console em UTF-8
    if os.name == "nt":
        try:
            os.system("chcp 65001 >nul")
        except Exception:
            pass

    proc = Popen(
        _python_cmd() + ["-u", str(path)],
        cwd=str(path.parent),
        stdout=PIPE,
        stderr=PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=env,
        creationflags=CREATE_NO_WINDOW,  # <- impede o 'cls' do filho de limpar sua tela
    )

    out, err = proc.communicate()
    full_log = (out or "") + (err or "")
    rc = proc.returncode

    # imprime o log do cenário em bloco (sem risco de ser "limpo")
    print("\n─── LOG DO CENÁRIO ─────────────────────────────────────────")
    print(full_log.rstrip())
    print("\n─── FIM DO LOG ─────────────────────────────────────────────")

    # ERRO somente se houver a palavra "Mensagem de Erro" no log
    has_error_text = bool(ERROR_RX.search(full_log))
    is_error = has_error_text

    if is_error:
        m = ERROR_RX.search(full_log)
        snippet = ""
        if m:
            start = max(0, m.start() - 120)
            end   = min(len(full_log), m.end() + 200)
            snippet = full_log[start:end].strip()
        print("[FAIL] Erro detectado por log (palavra 'Mensagem de Erro')")
        return rc, "ERROR", (snippet or "Erro detectado no log."), full_log
    else:
        print("[OK]")
        return rc, "SUCCESS", None, full_log







def _executar_cenario(path, idx=None, total=None, pause=False):
    path = Path(path)
    msg = f"\nExecutando {path}"
    if idx is not None and total is not None:
        msg += f" [{idx}/{total}]"
    print(msg)

    try:
        # roda no MESMO console e no diretório do script
        rc = subprocess.run(
            _python_cmd() + ["-u", str(path)],
            cwd=str(path.parent),
            check=False
        ).returncode

        if rc != 0:
            print(f"[FAIL] Retorno do processo: {rc}")
        else:
            print("[OK]")
    except Exception as e:
        print(f"[ERRO] Falha ao executar '{path}': {e}")

    if pause:
        input("\nPressione Enter para voltar...")

def _iter_scenarios(node: dict):
    """Percorre o nó atual e todos os subnós coletando caminhos de cenários (campo 'file')."""
    # cenários diretamente no nó
    if "scenarios" in node:
        for _, scen in node["scenarios"].items():
            f = scen.get("file")
            if f:
                yield f

    # subgrupos explícitos
    if "groups" in node:
        for _, sub in node["groups"].items():
            if isinstance(sub, dict):
                yield from _iter_scenarios(sub)

    # itens numéricos (ex.: '45' -> dict com 'label' e possivelmente 'scenarios')
    for k, v in node.items():
        if isinstance(k, str) and k.isdigit() and isinstance(v, dict):
            yield from _iter_scenarios(v)


# ---------- QA Reporter: só para encadeado ----------

def _abrir_arquivo(p: Path):
    try:
        p = Path(p).resolve()
        if not p.exists():
            for _ in range(10):
                time.sleep(0.2)
                if p.exists():
                    break
        if os.name == "nt":
            os.startfile(str(p))  # type: ignore[attr-defined]
        elif sys.platform == "darwin":
            subprocess.run(["open", str(p)], check=False)
        else:
            subprocess.run(["xdg-open", str(p)], check=False)
        print(f"Abrindo relatório: {p}")
    except Exception as e:
        print(f"Não foi possível abrir automaticamente: {e}\nCaminho: {p}")

_QA_DOCX_RX = re.compile(r'(?i)^relatorio[-_ ]?qa.*\.docx$')  # ex.: Relatorio_QA_20250924-154210.docx

def _is_qa_docx(p: Path) -> bool:
    """Somente arquivos gerados pelo qa_reporter (pelo padrão de nome)."""
    return _QA_DOCX_RX.match(p.name) is not None

def _anunciar_docx_encadeado(before: set[Path], after: set[Path]):
    """
    Ao final do encadeado, identifica os .docx NOVOS gerados pelo qa_reporter
    e abre apenas o mais recente. Ignora relatórios de cenários individuais.
    """
    # considera apenas *.docx cujo nome parece do qa_reporter
    novos = sorted([p for p in (after - before) if _is_qa_docx(p)],
                   key=lambda p: p.stat().st_mtime, reverse=True)

    alvo: Path | None = None
    if novos:
        alvo = novos[0]
        print(f"\nRelatório QA (encadeado) gerado: {alvo}")
    else:
        # não houve diff visível; tenta achar o qa_reporter mais recente entre 'after'
        candidatos = [p for p in after if _is_qa_docx(p)]
        if candidatos:
            alvo = max(candidatos, key=lambda p: p.stat().st_mtime)
            print(f"\n(Relatório QA mais recente encontrado) {alvo}")
        else:
            print("\nNenhum relatório do qa_reporter encontrado nas pastas monitoradas.")
            alvo = None

    if alvo:
        _abrir_arquivo(alvo)

def _provaveis_raizes_relatorios(paths_cenarios: list[Path]) -> list[Path]:
    """Locais prováveis onde o qa_reporter salva .docx durante o encadeado."""
    roots = set()
    for p in paths_cenarios:
        p = Path(p).resolve()
        roots.add(p.parent)
        roots.add(p.parent / "reports")
    roots.add(Path.cwd())
    roots.add(Path.cwd() / "reports")
    try:
        if 'DIR_REPORTS' in globals() and DIR_REPORTS:
            roots.add(Path(DIR_REPORTS))
        if 'OUT_BASE' in globals() and OUT_BASE:
            roots.add(Path(OUT_BASE))
    except Exception:
        pass
    return [r for r in roots if r]

def _snap_docx(roots: list[Path]) -> set[Path]:
    """Snapshot recursivo de .docx nas raízes monitoradas."""
    files: set[Path] = set()
    for r in roots:
        try:
            r = Path(r)
            if r.exists():
                for p in r.rglob("*.docx"):
                    files.add(p.resolve())
        except Exception:
            pass
    return files

def _collect_scenarios(node: dict):
    out = []
    # cenários diretos (ordenar por código numérico)
    if "scenarios" in node and isinstance(node["scenarios"], dict):
        for code in sorted(node["scenarios"].keys(),
                           key=lambda k: int(k) if str(k).isdigit() else str(k)):
            scen = node["scenarios"][code]
            f = scen.get("file")
            if f:
                out.append((scen.get("label", Path(f).stem), Path(f)))
    # subgrupos
    if "groups" in node and isinstance(node["groups"], dict):
        for _, sub in sorted(node["groups"].items(), key=lambda kv: kv[1].get("label","")):
            if isinstance(sub, dict):
                out.extend(_collect_scenarios(sub))
    # itens numéricos (ex.: "24": {...})
    num_keys = [k for k in node.keys() if isinstance(k, str) and k.isdigit()]
    for key in sorted(num_keys, key=int):
        v = node[key]
        if isinstance(v, dict):
            out.extend(_collect_scenarios(v))
    return out



# ===================== menus =====================

def executar_menu_scripts(node: Any, breadcrumb: str = ""):
    while True:
        clear_screen()
        label = node.get("label", "")
        if label:
            print(f"----- {label.upper()} -----\n")
        if breadcrumb:
            print("===== CAMINHO ATUAL =====")
            print(breadcrumb)
            print("")

        itens = {}

        if "groups" in node:
            for code, sub in node["groups"].items():
                sub_label = sub.get("label", str(code))
                print(f"{sub_label} (Digite {code})")
                itens[str(code)] = (sub_label, sub)

        for key in sorted([k for k in node.keys() if isinstance(k, str) and k.isdigit()], key=int):
            item = node[key]
            if isinstance(item, dict) and "label" in item:
                print(f"{item['label']} (Digite {key})")
                itens[key] = (item['label'], item)

        if "scenarios" in node:
            for code, scen in node["scenarios"].items():
                print(f"{scen['label']} (Digite {code})")
                itens[code] = (scen['label'], scen)

        print("\nTodos os Cenários encadeados (Digite 0)")
        print("<--- Voltar (X + Enter)")

        opt = read_input_with_hotkeys("\nDigite a opção desejada: ").upper()

        if opt in ("X", "__BACK__"):
            return

        if opt == "0":
            scen_list = _collect_scenarios(node)
            total = len(scen_list)
            if total == 0:
                print("\n[AVISO] Não há cenários neste nível.")
                input("\nPressione Enter para voltar...")
                continue

            print(f"\n[EXECUTAR EM CADEIA] {total} cenário(s) encontrado(s).\n")
            print("Plano de execução:")
            for i, (lbl, pth) in enumerate(scen_list, 1):
                print(f"  [{i}/{total}] {lbl} -> {pth}")
            print("")

            reports_dir = Path.cwd() / "reports"
            try:
                username = os.getlogin()
            except Exception:
                username = "Runner"

            rep = QAReporter(
                out_dir=reports_dir,
                environment="Homologação",
                executor="Runner CLI",
                system_version="v2025.09",
                username=username
            )
            rep.start_run(summary=f"Execução em cadeia — {node.get('label','')}")

            for idx, (label_exec, path_exec) in enumerate(scen_list, 1):
                h = rep.start_scenario(label_exec, test_type="CADASTRO")
                try:
                    rc, status, err_msg, full_log = _run_cenario_and_classify(Path(path_exec), idx, total)
                except Exception as e:
                    rc, status, err_msg, full_log = (1, "ERROR", f"Falha no runner: {e}", "")

                try:
                    (reports_dir / "logs").mkdir(parents=True, exist_ok=True)
                    (reports_dir / "logs" / f"{Path(path_exec).stem}_{idx:02d}.log").write_text(
                        full_log, encoding="utf-8", errors="ignore"
                    )
                except Exception:
                    pass

               # --- salvar o log COMPLETO e guardar o caminho em uma variável ---
                    # --- salvar log completo em reports/logs ---
                    (reports_dir / "logs").mkdir(parents=True, exist_ok=True)
                    saved_log_path = reports_dir / "logs" / f"{Path(path_exec).stem}_{idx:02d}.log"
                    saved_log_path.write_text(full_log, encoding="utf-8", errors="ignore")

                    # --- finalizar o cenário no relatório, incluindo o caminho do log ---
                    rep.finish_scenario(
                            h,
                            status=status,
                            error_message=err_msg,
                            extra={
                                "path": str(path_exec),
                                "returncode": rc,
                                "file_name": Path(path_exec).name,
                                "logfile": str(saved_log_path)   # <<< adicionado
                            }
                        )
            rep.end_run()
            docx_path = rep.save_docx("Relatorio_QA")
            print(f"\nRelatório QA gerado: {docx_path}")
            _abrir_arquivo(docx_path)

            input("\nEncadeamento concluído. Pressione Enter para voltar...")
            continue



        if opt in itens:
            item_label, item_data = itens[opt]

            if isinstance(item_data, dict) and ("scenarios" in item_data or "groups" in item_data
                                                or any(isinstance(k, str) and k.isdigit() for k in item_data.keys())):
                executar_menu_scripts(item_data, f"{breadcrumb} > {item_label}")
                continue

            if isinstance(item_data, dict) and "file" in item_data:
                # unitário: executa sem anúncio de relatório
                _executar_cenario(item_data["file"], pause=True)
                continue

            print("\n[AVISO] Opção sem ação definida.")
            time.sleep(0.8)
            continue

        print("\nOpção inválida.")
        time.sleep(0.8)

def menu_cadastros_principais(root: dict):
    cad_principais = root.get("cadastros", {}).get("principais", {})
    if not cad_principais:
        clear_screen()
        print("[AVISO] Nenhum cadastro principal configurado.")
        input("\nPressione Enter para voltar...")
        return
    executar_menu_scripts({"label": "Cadastros Principais", **cad_principais}, "> Cadastros > Cadastros Principais")

def menu_cadastros_adicionais(root: dict):
    cad_adicionais = root.get("cadastros", {}).get("adicionais", {})
    if not cad_adicionais:
        clear_screen()
        print("[AVISO] Nenhum cadastro adicional configurado.")
        input("\nPressione Enter para voltar...")
        return
    executar_menu_scripts({"label": "Cadastros Adicionais", **cad_adicionais}, "> Cadastros > Cadastros Adicionais")

def menu_tipo_cadastro(root: dict):
    while True:
        clear_screen()
        print("Qual tipo de cadastro você deseja rodar?\n")
        print("Cadastros Principais (Digite 1)")
        print("Cadastros Adicionais (Digite 2)")
        print("Todos os cadastros contidos no sistema (Digite 0)\n")
        print("<--- Voltar (X + Enter)")

        opt = read_input_with_hotkeys("\nDigite a opção desejada: ").upper()
        if opt in ("X", "__BACK__"):
            return
        if opt == "0":
            node_tmp = {"label": "Todos os Cadastros", "groups": {}}
            cad_root = root.get("cadastros", {})
            if cad_root.get("principais"):
                node_tmp["groups"]["1"] = {**cad_root["principais"], "label": "Cadastros Principais"}
            if cad_root.get("adicionais"):
                node_tmp["groups"]["2"] = {**cad_root["adicionais"], "label": "Cadastros Adicionais"}
            executar_menu_scripts(node_tmp, "> Cadastros > Todos")
            continue
        if opt == "1":
            menu_cadastros_principais(root); continue
        if opt == "2":
            menu_cadastros_adicionais(root); continue

        print("\nOpção inválida.")
        time.sleep(0.8)

def menu_pos_login(root: dict):
    while True:
        clear_screen()
        print("Qual tipo de automação você deseja rodar?\n")
        print("Cadastros (Digite 1)")
        print("Processos (Digite 2)")
        print("Cadastros e Processos (Digite 0)\n")
        print("<--- Voltar (X + Enter)")

        opt = read_input_with_hotkeys("\nDigite a opção desejada: ").upper()
        if opt in ("X", "__BACK__"):
            clear_screen()
            print("Você está na raiz.\n")
            time.sleep(1)
            continue
        if opt == "0":
            cad_root = root.get("cadastros", {})
            executar_menu_scripts({"label": "Cadastros", **cad_root}, "> Cadastros")
            continue
        if opt == "1":
            menu_tipo_cadastro(root); continue
        if opt == "2":
            clear_screen()
            print("----- PROCESSOS -----\n")
            print("(Ainda vou configurar)")
            input("\nPressione Enter para voltar...")
            continue

        print("\nOpção inválida.")
        time.sleep(0.8)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nEncerrado pelo usuário.")