# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path
from PyInstaller.utils.hooks import collect_all, collect_submodules

# Raiz do projeto = pasta onde está este .spec
project_root = Path(__file__).parent

# Listas base usadas pelo Analysis
datas = []
binaries = []
hiddenimports = []

# -------------------------------------------------------------------
# PASTAS DO PROJETO (seus cenários e utils)
# -------------------------------------------------------------------
datas += [
    (str(project_root / "cenariostestespegasus"), "cenariostestespegasus"),
    (str(project_root / "utils"), "utils"),
]

# -------------------------------------------------------------------
# BIBLIOTECAS GRANDES (empacotar tudo: código + binários)
# -------------------------------------------------------------------
for pkg in [
    "selenium",
    "webdriver_manager",
    "docx",             # python-docx
    "lxml",
    "pyautogui",
    "pyrect",
    "trio",
    "trio_websocket",
    "websocket",        # websocket-client
]:
    try:
        c_datas, c_bins, c_hidden = collect_all(pkg)
        datas += c_datas
        binaries += c_bins
        hiddenimports += c_hidden
    except Exception:
        # Se não encontrar alguma, só ignora
        pass

# -------------------------------------------------------------------
# FAKER + DATEUTIL + COMPLEMENTOS (modo agressivo)
# -------------------------------------------------------------------
for pkg in [
    "faker",
    "faker.providers",          # providers dinâmicos
    "faker_vehicle",
    "validate_docbr",
    "dateutil",                 # pacote python-dateutil inteiro
]:
    try:
        hiddenimports += collect_submodules(pkg)
    except Exception:
        pass

# Garantia extra pros módulos mais chatos do dateutil
hiddenimports += [
    "dateutil",
    "dateutil.parser",
    "dateutil.relativedelta",
    "dateutil.tz",
]

block_cipher = None

a = Analysis(
    ['TesteAgenteAutomacoes.py'],     # seu script principal
    pathex=[str(project_root)],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher,
)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='TesteAgenteAutomacoes',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,              # mantém o console pra ver os logs
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
