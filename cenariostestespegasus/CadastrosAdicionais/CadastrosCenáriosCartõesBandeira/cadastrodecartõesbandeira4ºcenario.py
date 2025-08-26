#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import re
import time
import threading
import subprocess
from pathlib import Path

# ================== CONFIG ==================
ENV_PASSWORD_KEY = "APP_PASS"        # defina a senha via variável de ambiente
MAX_TRIES = 3

# Ajuste para a sua estrutura mostrada no print:
BASE_SCRIPTS = Path(__file__).parent / "cenariostestespegasus"

DIR_CAD_ADIC = BASE_SCRIPTS / "CadastrosAdicionais"
DIR_CAD_PRIN = BASE_SCRIPTS / "CadastrosPrincipais"    # se existir
DIR_PROCESSOS = BASE_SCRIPTS / "Processos"             # se existir

# Descrições especiais (opcional): por nome da pasta (sem prefixo)
SPECIAL_SCENARIO_TEXT = {
    # exemplo para "Agenda de Compromissos" se sua pasta se chamar "CadastrosCenáriosAgendaDeCompromissos"
    "AgendaDeCompromissos": {
        1: 'Cenário 1: Nesse teste, serão preenchidos todos os campos do cadastro, e clicará em "Salvar".',
        2: 'Cenário 2: Nesse teste, serão preenchidos todos os campos do cadastro, e clicará em "Cancelar".',
        3: 'Cenário 3: Nesse teste, serão preenchidos APENAS os campos obrigatórios, e clicará em "Salvar".',
        4: 'Cenário 4: Nesse teste, serão preenchidos APENAS os campos NÃO obrigatórios, e clicará em "Salvar", para o teste de disparo de mensagens de alerta no sistema.',
    }
}

# ================== TERMINAL / TECLAS ==================
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

def _read_key_win_blocking():
    """
    Retorna tuplas:
      ('ENTER', None) | ('BACKSPACE', None) | ('LEFT', None)
      ('CTRL_V', None) | ('SHIFT_INSERT', None)
      ('CHAR', ch) | ('OTHER', None)
    """
    ch = msvcrt.getwch()

    if ch in ("\r", "\n"):
        return ("ENTER", None)
    if ch == "\x08":
        return ("BACKSPACE", None)
    if ch == "\x16":     # Ctrl+V
        return ("CTRL_V", None)
    if ch in ("\x00", "\xe0"):
        ch2 = msvcrt.getwch()
        if ch2.upper() == "K":  # Left
            # exigimos SHIFT? opcional; aqui aceitamos Left e, se possível, checamos SHIFT
            if _is_shift_pressed_windows():
                return ("LEFT", None)
            else:
                return ("LEFT", None)
        if ch2.upper() == "R":  # Insert
            if _is_shift_pressed_windows():
                return ("SHIFT_INSERT", None)
        return ("OTHER", None)
    return ("CHAR", ch)

def read_masked_password(prompt: str) -> str:
    """Lê senha mostrando * e ignorando colar (Windows)."""
    sys.stdout.write(prompt)
    sys.stdout.flush()
    buf = []
    if IS_WIN:
        while True:
            t, val = _read_key_win_blocking()
            if t == "ENTER":
                print()
                return "".join(buf)
            if t == "BACKSPACE":
                if buf:
                    buf.pop()
                    sys.stdout.write("\b \b")
                    sys.stdout.flush()
                continue
            if t in ("CTRL_V", "SHIFT_INSERT"):
                # ignora tentativa de colar
                continue
            if t == "CHAR":
                buf.append(val)
                sys.stdout.write("*")
                sys.stdout.flush()
            # demais teclas: ignora
    else:
        import termios, tty
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            while True:
                ch = sys.stdin.read(1)
                if ch in ("\r", "\n"):
                    print()
                    return "".join(buf)
                if ch in ("\x7f", "\b"):
                    if buf:
                        buf.pop()
                        sys.stdout.write("\b \b")
                        sys.stdout.flush()
                    continue
                if ch == "\x16":  # Ctrl+V
                    continue
                buf.append(ch)
                sys.stdout.write("*")
                sys.stdout.flush()
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)

def read_menu_number(valid_options: set[str], show_prompt: str = ""):
    """
    Lê um número (1..N) com suporte a BACK (Shift+←). Aceita vários dígitos.
    No Windows: leitura tecla a tecla; no Unix: usa input().
    Retorna str do número, ou 'BACK'.
    """
    if show_prompt:
        print(show_prompt, end="", flush=True)

    if IS_WIN:
        buf = []
        while True:
            t, v = _read_key_win_blocking()
            if t == "LEFT":
                print()
                return "BACK"
            if t == "ENTER":
                num = "".join(buf).strip()
                if num in valid_options:
                    print(num)
                    return num
                if num:
                    print()  # quebra
                    print("Escolha um caractere presente na lista")
                    print("Voltar para aba anterior (Shift + Left Arrow)")
                buf = []
                if show_prompt:
                    print(show_prompt, end="", flush=True)
                continue
            if t == "BACKSPACE":
                if buf:
                    buf.pop()
                    sys.stdout.write("\b \b")
                    sys.stdout.flush()
                continue
            if t == "CHAR":
                if v.isdigit():
                    buf.append(v)
                    sys.stdout.write(v)
                    sys.stdout.flush()
                # ignora outros chars
    else:
        s = input().strip()
        if s.lower() == "b":
            return "BACK"
        return s if s in valid_options else None

def confirm_yn(question: str) -> bool:
    print(question)
    valid = {"y": True, "Y": True, "n": False, "N": False}
    if IS_WIN:
        while True:
            t, v = _read_key_win_blocking()
            if t == "CHAR" and v in valid:
                print(v)
                return valid[v]
    else:
        while True:
            s = input().strip()
            if s in valid:
                return valid[s]

# ================== AUTENTICAÇÃO ==================
def authenticate_or_exit():
    clear_screen()
    print("--- AUTOMAÇÕES PEGASUS ---")
    pwd_env = os.environ.get(ENV_PASSWORD_KEY, "")
    if not pwd_env:
        print(f"[ERRO] Defina a variável de ambiente {ENV_PASSWORD_KEY} com a senha.")
        if IS_WIN:
            print('Ex.: PowerShell ->  $env:APP_PASS="minha_senha_forte"')
        else:
            print('Ex.: bash ->  export APP_PASS="minha_senha_forte"')
        sys.exit(1)

    tries = 0
    while tries < MAX_TRIES:
        pwd = read_masked_password("Digite a senha de acesso para entrar: ")
        if pwd == pwd_env:
            return
        print("Senha incorreta, tente novamente.")
        tries += 1
    print("Acesso bloqueado.")
    sys.exit(1)

# ================== UTILS DE VARREDURA ==================
_CAMEL_SPLIT = re.compile(r"(?<!^)(?=[A-ZÁÉÍÓÚÂÊÎÔÛÃÕÇ])")

def pretty_from_folder(folder_name: str) -> str:
    """
    Remove prefixos 'CadastrosCenários'/'CadastrosCenarios' e quebra CamelCase.
    """
    base = folder_name
    base = base.replace("CadastrosCenários", "").replace("CadastrosCenarios", "")
    if base.startswith("_") or base.startswith("-"):
        base = base[1:]
    # separar CamelCase preservando De/Do/Da
    parts = _CAMEL_SPLIT.split(base)
    return " ".join(parts).replace("  ", " ").strip()

def natural_key(p: Path):
    """Ordena por número se existir, senão por nome."""
    m = re.findall(r"(\d+)", p.stem)
    if m:
        return [int(x) for x in m]
    return [p.stem.lower()]

def discover_categories(root_dir: Path):
    """
    Retorna lista de (codigo, label, dir_path).
    """
    if not root_dir.exists():
        return []
    subs = [p for p in root_dir.iterdir() if p.is_dir()]
    subs.sort(key=lambda p: pretty_from_folder(p.name).lower())

    items = []
    for i, p in enumerate(subs, start=1):
        label_name = pretty_from_folder(p.name)
        label = f"Cenários dos cadastros de {label_name}"
        items.append((str(i), label, p))
    return items

def discover_scenarios(dir_path: Path):
    """
    Retorna lista de (codigo, label, file_path).
    Usa textos especiais se definidos em SPECIAL_SCENARIO_TEXT.
    """
    files = [f for f in dir_path.glob("*.py") if f.is_file()]
    files.sort(key=natural_key)

    # nome-chave para textos especiais
    key = pretty_from_folder(dir_path.name).replace(" ", "")
    special = SPECIAL_SCENARIO_TEXT.get(key, {})

    items = []
    for i, f in enumerate(files, start=1):
        if i in special:
            label = special[i]
        else:
            label = f"Cenário {i}: {f.stem}"
        items.append((str(i), label, f))
    return items

# ================== EXECUÇÃO COM INTERRUPÇÃO ==================
class InterruptFlag:
    def __init__(self):
        self._flag = False
        self._lock = threading.Lock()
    def set(self, v: bool):
        with self._lock:
            self._flag = v
    def get(self) -> bool:
        with self._lock:
            return self._flag

def _watch_shift_left(interrupt_flag: InterruptFlag, stop_event: threading.Event):
    if not IS_WIN:
        return
    while not stop_event.is_set():
        if msvcrt.kbhit():
            t, _ = _read_key_win_blocking()
            if t == "LEFT":
                interrupt_flag.set(True)
        time.sleep(0.02)

def run_script_with_interrupt(py_file: Path):
    if not py_file.exists():
        print(f"[ERRO] Arquivo não encontrado: {py_file}")
        return

    if not confirm_yn('Deseja executar a automação selecionada? (y/n)'):
        print("Ação interrompida pelo usuário")
        return

    interrupt_flag = InterruptFlag()
    stop_event = threading.Event()
    watcher = threading.Thread(target=_watch_shift_left, args=(interrupt_flag, stop_event), daemon=True)
    watcher.start()

    try:
        if IS_WIN:
            CREATE_NEW_PROCESS_GROUP = 0x00000200
            proc = subprocess.Popen([sys.executable, str(py_file)], creationflags=CREATE_NEW_PROCESS_GROUP)
        else:
            proc = subprocess.Popen([sys.executable, str(py_file)])

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

# ================== TELAS/MENUS ==================
def tela_cenarios_genericos(titulo: str, dir_path: Path):
    clear_screen()
    print(titulo)
    print("\nEscolha seu cenário:\n")

    scenarios = discover_scenarios(dir_path)
    if not scenarios:
        print("Nenhum cenário encontrado nesta pasta.")
        time.sleep(1.2)
        return

    valid = set()
    for code, label, _ in scenarios:
        print(f"{label} (Digite {code})")
        valid.add(code)
    print("\nVoltar para aba anterior (Shift + Left Arrow)")

    while True:
        choice = read_menu_number(valid)
        if choice == "BACK":
            return
        if choice in valid:
            _, _, f = next(x for x in scenarios if x[0] == choice)
            run_script_with_interrupt(f)
            # volta para a mesma tela após finalizar
            clear_screen()
            print(titulo)
            print("\nEscolha seu cenário:\n")
            for code, label, _ in scenarios:
                print(f"{label} (Digite {code})")
            print("\nVoltar para aba anterior (Shift + Left Arrow)")
        else:
            if choice is not None:
                print("Escolha um caractere presente na lista")

def tela_cadastros_adicionais():
    clear_screen()
    print("\n--- CADASTROS ADICIONAIS ---\n")
    cats = discover_categories(DIR_CAD_ADIC)
    if not cats:
        print("Nenhuma pasta encontrada em:", DIR_CAD_ADIC)
        time.sleep(1.5)
        return

    valid = set()
    for code, label, _ in cats:
        print(f"- {label} (Digite {code})")
        valid.add(code)
    print("\nVoltar para aba anterior (Shift + Left Arrow)")

    while True:
        choice = read_menu_number(valid)
        if choice == "BACK":
            return
        if choice in valid:
            _, label, path = next(x for x in cats if x[0] == choice)
            # título “--- Cenários cadastros X ---”
            pretty = label.replace("Cenários dos cadastros de ", "").strip()
            titulo = f"--- Cenários cadastros {pretty} ---"
            tela_cenarios_genericos(titulo, path)
            clear_screen()
            print("\n--- CADASTROS ADICIONAIS ---\n")
            for code, label, _ in cats:
                print(f"- {label} (Digite {code})")
            print("\nVoltar para aba anterior (Shift + Left Arrow)")
        else:
            print("Escolha um caractere presente na lista")

def tela_cadastros_principais_ou_adicionais():
    clear_screen()
    print("Qual tipo de cadastro você deseja rodar?\n")
    print("- Cadastros Principais (Digite 0)")
    print("- Cadastros Adicionais (Digite 1)\n")
    print("Voltar para aba anterior (Shift + Left Arrow)")

    valid = {"0", "1"}
    while True:
        choice = read_menu_number(valid)
        if choice == "BACK":
            return
        if choice == "0":
            # dinâmica para Principais se existir
            clear_screen()
            print("\n--- CADASTROS PRINCIPAIS ---\n")
            cats = discover_categories(DIR_CAD_PRIN)
            if not cats:
                print("Nenhum item configurado para Cadastros Principais.")
                time.sleep(1.5)
                return
            valid2 = set()
            for code, label, _ in cats:
                print(f"- {label} (Digite {code})")
                valid2.add(code)
            print("\nVoltar para aba anterior (Shift + Left Arrow)")
            while True:
                c2 = read_menu_number(valid2)
                if c2 == "BACK":
                    break
                if c2 in valid2:
                    _, label, path = next(x for x in cats if x[0] == c2)
                    titulo = f"--- {label} ---"
                    tela_cenarios_genericos(titulo, path)
                    clear_screen()
                    print("\n--- CADASTROS PRINCIPAIS ---\n")
                    for code, lab, _ in cats:
                        print(f"- {lab} (Digite {code})")
                    print("\nVoltar para aba anterior (Shift + Left Arrow)")
                else:
                    print("Escolha um caractere presente na lista")
        elif choice == "1":
            tela_cadastros_adicionais()
            clear_screen()
            print("Qual tipo de cadastro você deseja rodar?\n")
            print("- Cadastros Principais (Digite 0)")
            print("- Cadastros Adicionais (Digite 1)\n")
            print("Voltar para aba anterior (Shift + Left Arrow)")
        else:
            print("Escolha um caractere presente na lista")

def tela_processos():
    clear_screen()
    print("\n--- PROCESSOS ---\n")
    cats = discover_categories(DIR_PROCESSOS)
    if not cats:
        print("Nenhum processo encontrado em:", DIR_PROCESSOS)
        time.sleep(1.5)
        return

    # Ajusta rótulo para "Cenários do Processo: X" quando fizer sentido
    cats = [(code, f"Cenários do Processo: {pretty_from_folder(path.name)}", path)
            for (code, _, path) in cats]

    valid = set()
    for code, label, _ in cats:
        print(f"- {label} (Digite {code})")
        valid.add(code)
    print("\nVoltar para aba anterior (Shift + Left Arrow)")

    while True:
        choice = read_menu_number(valid)
        if choice == "BACK":
            return
        if choice in valid:
            _, label, path = next(x for x in cats if x[0] == choice)
            titulo = f"--- {label} ---"
            tela_cenarios_genericos(titulo, path)
            clear_screen()
            print("\n--- PROCESSOS ---\n")
            for code, lab, _ in cats:
                print(f"- {lab} (Digite {code})")
            print("\nVoltar para aba anterior (Shift + Left Arrow)")
        else:
            print("Escolha um caractere presente na lista")

def tela_tipo_automacao():
    clear_screen()
    print("Qual tipo de automação você deseja rodar?\n")
    print("- Cadastros (Digite 0)")
    print("- Processos (Digite 1)\n")
    print("Voltar para aba anterior (Shift + Left Arrow)")

    valid = {"0", "1"}
    while True:
        choice = read_menu_number(valid)
        if choice == "BACK":
            return
        if choice == "0":
            tela_cadastros_principais_ou_adicionais()
            clear_screen()
            print("Qual tipo de automação você deseja rodar?\n")
            print("- Cadastros (Digite 0)")
            print("- Processos (Digite 1)\n")
            print("Voltar para aba anterior (Shift + Left Arrow)")
        elif choice == "1":
            tela_processos()
            clear_screen()
            print("Qual tipo de automação você deseja rodar?\n")
            print("- Cadastros (Digite 0)")
            print("- Processos (Digite 1)\n")
            print("Voltar para aba anterior (Shift + Left Arrow)")
        else:
            print("Escolha um caractere presente na lista")

# ================== MAIN ==================
def main():
    print("--- AUTOMAÇÕES PEGASUS ---")
    authenticate_or_exit()
    # etapa 2
    tela_tipo_automacao()
    clear_screen()
    print("Saindo...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nSaindo...")
