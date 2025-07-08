import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCREENSHOT_DIR = os.path.join(BASE_DIR, "screenshots")
LOG_FILE = os.path.join(BASE_DIR, "orquestrador.log")
REPORT_FILE = os.path.join(BASE_DIR, "relatorio.html")

# Se True continua mesmo se algum teste falhar
CONTINUAR_EM_ERRO = False
