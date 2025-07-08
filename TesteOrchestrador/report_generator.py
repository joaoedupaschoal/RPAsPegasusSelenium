def gerar_relatorio(resultados):
    with open("relatorio.html", "w", encoding="utf-8") as f:
        f.write("<html><head><title>Relatório de Testes</title></head><body>")
        f.write("<h1>Relatório de Execução</h1><table border='1'>")
        f.write("<tr><th>Teste</th><th>Resultado</th><th>Tempo (s)</th></tr>")

        for teste, resultado, tempo in resultados:
            cor = "#90EE90" if "SUCESSO" in resultado else "#FF7F7F"
            f.write(f"<tr bgcolor='{cor}'><td>{teste}</td><td>{resultado}</td><td>{tempo}</td></tr>")

        f.write("</table></body></html>")
