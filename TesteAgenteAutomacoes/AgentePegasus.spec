


# -*- mode: python ; coding: utf-8 -*-
from pathlib import Path
from PyInstaller.building.build_main import Analysis, PYZ, EXE, COLLECT
from PyInstaller.utils.hooks import collect_submodules
from PyInstaller.utils.hooks import collect_data_files
from PyInstaller.building.datastruct import Tree

project_dir = Path(__file__).resolve().parent
main_script = project_dir / "TesteAgenteAutomacoes" / "TesteAgenteAutomacoes.py"

# inclua aqui outros dados/binários se necessário (drivers, templates, etc.)
datas = [
    # embute TODOS os seus cenários dentro do exe
    Tree(str(project_dir / "cenariostestespegasus"), prefix="cenariostestespegasus"),
    # exemplos extras:
    # Tree(str(project_dir / "reports"), prefix="reports"),
    # (str(project_dir / "drivers" / "chromedriver.exe"), "drivers"),
]

binaries = [
    # exemplo: (str(project_dir / "drivers" / "chromedriver.exe"), "drivers")
]

hiddenimports = collect_submodules("")  # normalmente vazio; ajuste se usar libs dinâmicas

a = Analysis(
    [str(main_script)],
    pathex=[str(project_dir)],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    name="AgentePegasus",
    icon=None,  # opcional: str(project_dir / "icone.ico")
    debug=False,
    strip=False,
    upx=True,
    console=True,   # deixe True (console é útil p/ ver saídas e prompts)
)

# onefile: entregue apenas 1 exe
# (se preferir onefolder, troque por COLLECT abaixo)
