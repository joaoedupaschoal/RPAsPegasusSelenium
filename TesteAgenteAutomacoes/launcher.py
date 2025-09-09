# launcher.py
import sys, os, time

def mostrar_boas_vindas():
    print("Carregando... Estamos preparando tudo pra você.")
    sys.stdout.flush()

def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")

def main():
    mostrar_boas_vindas()
    # opcional: manter a frase por 1–2s
    time.sleep(1)
    limpar_tela()

    # importa e roda seu app principal
    import TesteAgenteAutomacoes as app
    if hasattr(app, "main") and callable(getattr(app, "main")):
        app.main()  # se você tiver definido uma main()
    # se não tiver main(), só o import já dispara seu fluxo (conforme seu script)

if __name__ == "__main__":
    main()
