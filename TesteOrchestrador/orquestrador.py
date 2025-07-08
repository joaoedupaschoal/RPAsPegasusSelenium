import importlib
import sys
import os
import time

import config
from utils.helpers import log, error, marcar_inicio, marcar_fim
import report_generator

# Ajuste de paths
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'testes')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'utils')))

testes = [
    "cadastrodeareas1ºcenario.py"
    "cadastrodeareas2ºcenario.py"
    "cadastrodeareas3ºcenario.py"
    "cadastrodeareas1ºcenario.py"
    "cadastrodeatendentes1ºcenario.py"
    "cadastrodeatendentes2ºcenario.py"
    "cadastrodeatendentes3ºcenario.py"
    "cadastrodecapelas1ºcenario.py"
    "cadastrodecapelas2ºcenario.py"
    "cadastrodecapelas3ºcenario.py"
    "cadastrodecapelas4ºcenario.py"
    "cadastrodecarteira1ºcenario.py"
    "cadastrodecarteira2ºcenario.py"
    "cadastrodecarteira3ºcenario.py"
    "cadastrodecartões1ºcenario.py"
    "cadastrodecartões2ºcenario.py"
    "cadastrodecartões3ºcenario.py"


]

resultados = []

for idx, teste in enumerate(testes, 1):
    log(f"🚀 Executando Teste {idx}: {teste}")
    inicio = marcar_inicio()

    try:
        modulo = importlib.import_module(teste)
        modulo.executar()
        tempo = marcar_fim(inicio)
        resultados.append((teste, "✅ SUCESSO", tempo))
    except Exception as e:
        tempo = marcar_fim(inicio)
        error(f"❌ Teste {teste} falhou: {e}")
        resultados.append((teste, f"❌ FALHOU: {e}", tempo))
        if not config.CONTINUAR_EM_ERRO:
            break
    time.sleep(1)

log("📊 RESUMO FINAL:")
for nome, resultado, tempo in resultados:
    print(f"{nome}: {resultado} ({tempo}s)")

report_generator.gerar_relatorio(resultados)
log("📄 Relatório HTML gerado com sucesso!")
