#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# força coleta no build do PyInstaller
try:
    import selenium, selenium.webdriver  # noqa
    import urllib3, certifi, requests    # noqa
except Exception:
    pass


import os
import sys
import time
import threading
import subprocess
from pathlib import Path
# ========== CONFIGURAÇÕES ==========
ENV_PASSWORD_KEY = "j2e0j1p0#"
MAX_TRIES = 3

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
            # Exemplo de itens (adicione seus próprios caminhos depois)
            "1": {"label": "Cenários dos cadastros de Abastecimento", "scenarios": {}},
            "2": {"label": "Cenários dos cadastros de Áreas", "scenarios": {}},
            "3": {"label": "Cenários dos cadastros de Atendentes", "scenarios": {}},
            "4": {"label": "Cenários dos cadastros de Capelas", "scenarios": {}},
            "5": {"label": "Cenários dos cadastros de Carteira", "scenarios": {}},
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
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" /  "CadastrosCenáriosAgendaDeCompromissos" / "cadastrodeagendadecompromissos2ºcenario.py",
                    },
                    "3": {
                        "label": 'Cenário 3: Nesse teste, serão preenchidos APENAS os campos obrigatórios, e clicará em "Salvar".',
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" /  "CadastrosCenáriosAgendaDeCompromissos" / "cadastrodeagendadecompromissos3ºcenario.py",
                    },
                    "4": {
                        "label": 'Cenário 4: Nesse teste, serão preenchidos APENAS os campos NÃO obrigatórios, e clicará em "Salvar", para disparo de alertas.',
                        "file": BASE_SCRIPTS /"CadastrosPrincipais" /  "CadastrosCenáriosAgendaDeCompromissos" / "cadastrodeagendadecompromissos4ºcenario.py",
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
                }
            },
            
            "3": {
                "label": "Cenários dos cadastros de Cemitérios",
                "scenarios": {
                    "1": {
                        "label": "Cenário 1: TESTE CENARIO 1",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosCemitérios" / "cadastrodecemitérios1ºcenario.py",
                    },
                    "2": {
                        "label": "Cenário 2: TESTE CENARIO 2",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosCemitérios" / "cadastrodecemitérios2ºcenario.py",
                    },
                    "3": {
                        "label": "Cenário 3: TESTE CENARIO 3",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosCemitérios" / "cadastrodecemitérios3ºcenario.py",
                    "4": {
                        "label": "Cenário 4: TESTE CENARIO 4",
                        "file": BASE_SCRIPTS / "CadastrosPrincipais" / "CadastrosCenáriosCemitérios" / "cadastrodecemitérios4ºcenario.py",
                    },
                }
            },

            "4": {"label": "Cenários dos cadastros de Cesta Básica", "scenarios": {}},
            "5": {"label": "Cenários dos cadastros de Cobrador Teste", "scenarios": {}},
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
                    "file": BASE_SCRIPTS / "historico_falecidos" / "cenario_1.py",
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
}
# ========== SUPORTE A TECLAS (Windows/Unix) ==========
IS_WIN = (os.name == "nt")

if IS_WIN:
    import msvcrt
    import ctypes
    user32 = ctypes.windll.user32
    VK_SHIFT = 0x10
    VK_INSERT = 0x2D

def clear_screen():
    os.system("cls" if IS_WIN else "clear")

def _is_shift_pressed_windows() -> bool:
    if not IS_WIN:
        return False
    # bit mais significativo indica tecla pressionada
    return (user32.GetAsyncKeyState(VK_SHIFT) & 0x8000) != 0

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
    if ch == "\x16":  # 0x16 = 22
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

def read_menu_key(valid_digits: set[str], show_prompt=""):
    """
    Lê uma opção de menu (um dígito). Suporta Shift+Left para voltar (retorna 'BACK').
    """
    if show_prompt:
        print(show_prompt, end="", flush=True)

    if IS_WIN:
        while True:
            t, val = _read_key_win_blocking()
            if t == "LEFT":
                print()  # quebra linha
                return "BACK"
            if t == "ENTER":
                # ignora ENTER sem ter recebido dígito
                continue
            if t == "BACKSPACE":
                # ignora
                continue
            if t == "CHAR":
                if val in valid_digits:
                    print(val)  # ecoa seleção
                    return val
                else:
                    print()  # quebra
                    print('Escolha um caractere presente na lista')
                    print("Voltar para aba anterior (Shift + Left Arrow)")
                    # reimprime prompt se houver
                    if show_prompt:
                        print(show_prompt, end="", flush=True)
            # demais teclas: ignora
    else:
        # Unix-like fallback (sem seta): lê linha e trata 'b' como voltar
        s = input()
        s = s.strip()
        if s.lower() == "b":
            return "BACK"
        if s in valid_digits:
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

# ========== AUTENTICAÇÃO ==========
def authenticate_or_exit():
    clear_screen()
    print("--- AUTOMAÇÕES PEGASUS ---")
    pwd_env = os.environ.get(ENV_PASSWORD_KEY, "")

    # Se não houver APP_PASS, informa e mantém a janela aberta
    if not pwd_env:
        print(f"[ERRO] Defina a variável de ambiente {ENV_PASSWORD_KEY} com a senha.")
        if IS_WIN:
            print('Ex.: PowerShell ->  $env:APP_PASS="minha_senha_forte"')
            # mantém janela aberta no duplo clique
            try:
                os.system("pause")
            except Exception:
                pass
        else:
            try:
                input("Pressione Enter para sair...")
            except Exception:
                pass
        sys.exit(1)

    # Tentativas de senha
    tries = 0
    while tries < MAX_TRIES:
        pwd = read_masked_password("Digite a senha de acesso para entrar: ")
        if pwd == pwd_env:
            return
        print("Senha incorreta, tente novamente.")
        tries += 1

    print("Acesso bloqueado.")
    # também pausa aqui para o caso de duplo clique
    if IS_WIN:
        try:
            os.system("pause")
        except Exception:
            pass
    else:
        try:
            input("Pressione Enter para sair...")
        except Exception:
            pass
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
        time.sleep(0.02)

def run_script_with_interrupt(py_file: Path):
    # 1) valida caminho do arquivo
    try:
        if not py_file.exists():
            print(f"[ERRO] Arquivo não encontrado: {py_file}")
            return
    except Exception as e:
        print(f"[ERRO] Caminho inválido: {py_file} ({e})")
        return

    # 2) confirma execução
    if not confirm_yn('Deseja executar a automação selecionada? (y/n)'):
        print("Ação interrompida pelo usuário")
        return

    # 3) watcher do Shift+←
    interrupt_flag = InterruptFlag()
    stop_event = threading.Event()
    watcher = threading.Thread(
        target=_watch_shift_left, args=(interrupt_flag, stop_event), daemon=True
    )
    watcher.start()

    try:
        # 4) monta o comando
        # - no exe (PyInstaller): chama a si próprio com --run-script
        # - no modo dev: chama o Python do sistema com o .py
        cmd = (
            [sys.executable, "--run-script", str(py_file)]
            if getattr(sys, "frozen", False)
            else [sys.executable, str(py_file)]
        )

        popen_kwargs = {}
        if IS_WIN:
            popen_kwargs["creationflags"] = 0x00000200  # CREATE_NEW_PROCESS_GROUP

        proc = subprocess.Popen(cmd, **popen_kwargs)

        # 5) loop de monitoramento + interrupção
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
            CREATE_NEW_PROCESS_GROUP = 0x00000200
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
    print("- Cadastros Adicionais (Digite 1)\n")
    print('Voltar para aba anterior (Shift + Left Arrow)')
    valid = {"0", "1"}

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
                choice2 = read_menu_key(valid_cp)
                if choice2 == "BACK":
                    break
                if choice2 in d:
                    if d[choice2]["scenarios"]:
                        tela_cenarios_genericos(
                            f"--- {d[choice2]['label']} ---",
                            d[choice2]["scenarios"],
                        )
                    else:
                        print("Nenhum cenário configurado para este item ainda.")
                        time.sleep(1.2)
                        clear_screen()
                        print("\n--- CADASTROS PRINCIPAIS ---\n")
                        for k in sorted(d.keys(), key=lambda x: int(x)):
                            print(f"- {d[k]['label']} (Digite {k})")
                        print('\nVoltar para aba anterior (Shift + Left Arrow)')
                else:
                    print('Escolha um caractere presente na lista')

        elif choice == "1":
            # Lista de Cadastros Adicionais
            clear_screen()
            print("\n--- CADASTROS ADICIONAIS ---\n")
            d = SCRIPTS["cadastros"]["adicionais"]
            valid_ca = set(sorted(d.keys(), key=lambda x: int(x)))
            for k in sorted(d.keys(), key=lambda x: int(x)):
                print(f"- {d[k]['label']} (Digite {k})")
            print('\nVoltar para aba anterior (Shift + Left Arrow)')
            while True:
                choice2 = read_menu_key(valid_ca)
                if choice2 == "BACK":
                    break
                if choice2 in d:
                    label = d[choice2]["label"]
                    if d[choice2]["scenarios"]:
                        titulo = f"--- {label.replace('Cenários dos', 'Cenários').replace('cadastros de', 'cadastros')} ---"
                        # título específico para Agenda de Compromissos conforme solicitado
                        if "Agenda de Compromissos" in label:
                            titulo = "--- Cenários cadastros Agenda de compromissos ---"
                        tela_cenarios_genericos(titulo, d[choice2]["scenarios"])
                    else:
                        print("Nenhum cenário configurado para este item ainda.")
                        time.sleep(1.2)
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
                time.sleep(1.2)
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
    print("- Processos (Digite 1)\n")
    print('Voltar para aba anterior (Shift + Left Arrow)')

    valid = {"0", "1"}
    while True:
        choice = read_menu_key(valid)
        if choice == "BACK":
            return
        if choice == "0":
            tela_cadastros_principais()
            clear_screen()
            print("Qual tipo de automação você deseja rodar?\n")
            print("- Cadastros (Digite 0)")
            print("- Processos (Digite 1)\n")
            print('Voltar para aba anterior (Shift + Left Arrow)')
        elif choice == "1":
            tela_processos()
            clear_screen()
            print("Qual tipo de automação você deseja rodar?\n")
            print("- Cadastros (Digite 0)")
            print("- Processos (Digite 1)\n")
            print('Voltar para aba anterior (Shift + Left Arrow)')
        else:
            print('Escolha um caractere presente na lista')

# ========== MAIN ==========
def main():
    # Banner + senha
    print("--- AUTOMAÇÕES PEGASUS ---")
    authenticate_or_exit()

    # Etapa 2
    tela_tipo_automacao()

    # Saída
    clear_screen()
    print("Saindo...")


# --- pause automático só quando for o EXE "principal" (sem argumentos) ---
def _pause_if_frozen_main():
    # Pausa apenas no EXE (PyInstaller) e só quando aberto por duplo clique
    # (sem argumentos). No modo worker (--run-script) não pausa.
    if IS_WIN and getattr(sys, "frozen", False) and len(sys.argv) == 1:
        try:
            os.system("pause")
        except Exception:
            pass


if __name__ == "__main__":
    import traceback
    from pathlib import Path

    try:
        # Modo worker: o próprio EXE executa um cenário específico
        if "--run-script" in sys.argv:
            import runpy
            i = sys.argv.index("--run-script")
            runpy.run_path(sys.argv[i + 1], run_name="__main__")
            sys.exit(0)

        # Fluxo normal do agente
        main()

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
        sys.exit(1)

    finally:
        # Mesmo sem erro, mantém a janela aberta no duplo clique
        _pause_if_frozen_main()

