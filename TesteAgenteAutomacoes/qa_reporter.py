# qa_reporter.py
from __future__ import annotations
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Any
import csv, json, atexit, traceback

# Dependências opcionais
_HAS_MPL = False
_HAS_DOCX = False
try:
    import matplotlib
    matplotlib.use("Agg")  # headless
    import matplotlib.pyplot as plt
    _HAS_MPL = True
except Exception:
    _HAS_MPL = False

try:
    from docx import Document
    from docx.shared import Inches
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.shared import RGBColor
    _HAS_DOCX = True
except Exception:
    _HAS_DOCX = False


# ================== MODELOS ==================
@dataclass
class ScenarioResult:
    name: str
    status: str                  # SUCCESS | ERROR | ALERT
    started_at: datetime
    ended_at: datetime
    duration_ms: int
    test_type: str = "SCENARIO"  # SCENARIO | CADASTRO
    error_message: Optional[str] = None
    screenshots: Optional[List[str]] = None
    extra: Optional[Dict[str, Any]] = None


# ================== ESTADO GLOBAL DO REPORTER ==================
class QAReporter:
    def __init__(self, out_dir: str | Path = "reports", auto_register_atexit: bool = True,
                 environment: str = "localhost:8080/gs/login.xhtml",
                 username: str = "João Eduardo",
                 password: str = "071999gs"):
        self.out_dir = Path(out_dir)
        self.out_dir.mkdir(parents=True, exist_ok=True)
        self._stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        self._results: List[ScenarioResult] = []
        self._run_started_at: Optional[datetime] = None
        self._run_ended_at: Optional[datetime] = None
        self._closed: bool = False
        
        # Informações do ambiente de teste
        self.environment = environment
        self.username = username
        self.password = password
        
        if auto_register_atexit:
            atexit.register(self._safe_finalize_if_needed)

    # -------- ciclo da execução inteira --------
    def start_run(self):
        self._run_started_at = datetime.now()

    def end_run(self):
        self._run_ended_at = datetime.now()

    # -------- registro de cenários e cadastros --------
    def start_scenario(self, name: str, test_type: str = "SCENARIO") -> Dict[str, Any]:
        return {"name": name, "started_at": datetime.now(), "test_type": test_type}

    def start_cadastro(self, name: str) -> Dict[str, Any]:
        return self.start_scenario(name, "CADASTRO")

    def finish_scenario(self, handle: Dict[str, Any], status: str,
                        error_message: Optional[str] = None,
                        screenshots: Optional[List[str]] = None,
                        extra: Optional[Dict[str, Any]] = None):
        name = handle["name"]
        started_at = handle["started_at"]
        test_type = handle.get("test_type", "SCENARIO")
        ended_at = datetime.now()
        duration_ms = max(0, int((ended_at - started_at).total_seconds() * 1000))
        self._results.append(ScenarioResult(
            name=name,
            status=status.upper(),
            started_at=started_at,
            ended_at=ended_at,
            duration_ms=duration_ms,
            test_type=test_type,
            error_message=(error_message or "").strip() if error_message else None,
            screenshots=screenshots or [],
            extra=extra or {}
        ))

    # Helpers prontos para cenários
    def success(self, name: str, started_at: datetime, test_type: str = "SCENARIO", screenshots: Optional[List[str]] = None, extra: Optional[Dict[str, Any]] = None):
        self.finish_scenario({"name": name, "started_at": started_at, "test_type": test_type}, "SUCCESS", None, screenshots, extra)

    def error(self, name: str, started_at: datetime, error_message: str, test_type: str = "SCENARIO", screenshots: Optional[List[str]] = None, extra: Optional[Dict[str, Any]] = None):
        self.finish_scenario({"name": name, "started_at": started_at, "test_type": test_type}, "ERROR", error_message, screenshots, extra)

    def alert(self, name: str, started_at: datetime, message: str, test_type: str = "SCENARIO", screenshots: Optional[List[str]] = None, extra: Optional[Dict[str, Any]] = None):
        self.finish_scenario({"name": name, "started_at": started_at, "test_type": test_type}, "ALERT", message, screenshots, extra)

    # Helpers específicos para cadastros
    def cadastro_success(self, name: str, started_at: datetime, screenshots: Optional[List[str]] = None, extra: Optional[Dict[str, Any]] = None):
        self.success(name, started_at, "CADASTRO", screenshots, extra)

    def cadastro_error(self, name: str, started_at: datetime, error_message: str, screenshots: Optional[List[str]] = None, extra: Optional[Dict[str, Any]] = None):
        self.error(name, started_at, error_message, "CADASTRO", screenshots, extra)

    def cadastro_alert(self, name: str, started_at: datetime, message: str, screenshots: Optional[List[str]] = None, extra: Optional[Dict[str, Any]] = None):
        self.alert(name, started_at, message, "CADASTRO", screenshots, extra)

    # Context manager prático
    def scenario(self, name: str, test_type: str = "SCENARIO"):
        class _Ctx:
            def __init__(self, outer, name, test_type):
                self.outer = outer
                self.name = name
                self.test_type = test_type
                self.handle = None
                self._screens = []
                self._extra = {}
                self._status = "SUCCESS"
                self._err = None
            def attach_screenshot(self, path: str):
                self._screens.append(path)
            def set_extra(self, **kwargs):
                self._extra.update(kwargs)
            def __enter__(self):
                self.handle = self.outer.start_scenario(self.name, self.test_type)
                return self
            def __exit__(self, exc_type, exc, tb):
                if exc:
                    # Se houve exceção, marca como ERROR e registra traceback
                    self._status = "ERROR"
                    msg = f"{exc}\n{''.join(traceback.format_exception(exc_type, exc, tb))}"
                    self._err = msg
                self.outer.finish_scenario(self.handle, self._status, self._err, self._screens, self._extra)
                # Não suprime a exceção; deixe-a subir se necessário
                return False
        return _Ctx(self, name, test_type)

    def cadastro(self, name: str):
        return self.scenario(name, "CADASTRO")

    # -------- geração de métricas e arquivos --------
    def _metrics(self) -> Dict[str, Any]:
        # Métricas gerais
        total = len(self._results)
        ok = sum(1 for r in self._results if r.status == "SUCCESS")
        err = sum(1 for r in self._results if r.status == "ERROR")
        alt = sum(1 for r in self._results if r.status == "ALERT")
        pass_rate = (ok / total * 100.0) if total else 0.0
        efficiency = ((ok + 0.5 * alt) / total * 100.0) if total else 0.0
        
        # Métricas por tipo de teste
        cadastros = [r for r in self._results if r.test_type == "CADASTRO"]
        cenarios = [r for r in self._results if r.test_type == "SCENARIO"]
        
        # Cadastros
        cadastros_total = len(cadastros)
        cadastros_ok = sum(1 for r in cadastros if r.status == "SUCCESS")
        cadastros_err = sum(1 for r in cadastros if r.status == "ERROR")
        cadastros_alt = sum(1 for r in cadastros if r.status == "ALERT")
        cadastros_pass_rate = (cadastros_ok / cadastros_total * 100.0) if cadastros_total else 0.0
        cadastros_efficiency = ((cadastros_ok + 0.5 * cadastros_alt) / cadastros_total * 100.0) if cadastros_total else 0.0
        
        # Cenários
        cenarios_total = len(cenarios)
        cenarios_ok = sum(1 for r in cenarios if r.status == "SUCCESS")
        cenarios_err = sum(1 for r in cenarios if r.status == "ERROR")
        cenarios_alt = sum(1 for r in cenarios if r.status == "ALERT")
        cenarios_pass_rate = (cenarios_ok / cenarios_total * 100.0) if cenarios_total else 0.0
        cenarios_efficiency = ((cenarios_ok + 0.5 * cenarios_alt) / cenarios_total * 100.0) if cenarios_total else 0.0
        
        # Duração
        dur_total_ms = sum(r.duration_ms for r in self._results)
        dur_avg_ms = int(dur_total_ms / total) if total else 0

        # janela de execução
        t0 = min((r.started_at for r in self._results), default=self._run_started_at)
        tf = max((r.ended_at for r in self._results), default=self._run_ended_at)
        w_total_ms = int((tf - t0).total_seconds() * 1000) if (t0 and tf) else 0

        # Screenshots de erro
        error_screenshots = []
        for r in self._results:
            if r.status == "ERROR" and r.screenshots:
                for screenshot in r.screenshots:
                    error_screenshots.append({
                        "test_name": r.name,
                        "screenshot": screenshot,
                        "error_message": r.error_message
                    })

        return {
            "total": total,
            "success": ok,
            "error": err,
            "alert": alt,
            "pass_rate_pct": round(pass_rate, 2),
            "efficiency_pct": round(efficiency, 2),
            "duration_total_ms": dur_total_ms,
            "duration_avg_ms": dur_avg_ms,
            "window_started_at": _fmt_dt(t0) if t0 else "",
            "window_ended_at": _fmt_dt(tf) if tf else "",
            "window_total_ms": w_total_ms,
            
            # Métricas de cadastros
            "cadastros_total": cadastros_total,
            "cadastros_success": cadastros_ok,
            "cadastros_error": cadastros_err,
            "cadastros_alert": cadastros_alt,
            "cadastros_pass_rate_pct": round(cadastros_pass_rate, 2),
            "cadastros_efficiency_pct": round(cadastros_efficiency, 2),
            
            # Métricas de cenários
            "cenarios_total": cenarios_total,
            "cenarios_success": cenarios_ok,
            "cenarios_error": cenarios_err,
            "cenarios_alert": cenarios_alt,
            "cenarios_pass_rate_pct": round(cenarios_pass_rate, 2),
            "cenarios_efficiency_pct": round(cenarios_efficiency, 2),
            
            # Screenshots de erro
            "error_screenshots": error_screenshots,
        }

    def _save_csv(self) -> Path:
        p = self.out_dir / f"executions-{self._stamp}.csv"
        with open(p, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f, delimiter=";")
            w.writerow(["Execução", "Tipo", "Status", "Início", "Fim", "Duração(ms)", "Erro", "Screenshots"])
            for r in self._results:
                w.writerow([
                    r.name, r.test_type, r.status, _fmt_dt(r.started_at), _fmt_dt(r.ended_at),
                    r.duration_ms,
                    (r.error_message or "").replace("\n", " ").strip(),
                    " | ".join(r.screenshots or [])
                ])
        return p

    def _save_json(self, metrics: Dict[str, Any]) -> Path:
        p = self.out_dir / f"executions-{self._stamp}.json"
        payload = {
            "generated_at": _fmt_dt(datetime.now()),
            "environment": self.environment,
            "username": self.username,
            "password": self.password,
            "metrics": metrics,
            "executions": [asdict(r) | {
                "started_at": _fmt_dt(r.started_at),
                "ended_at": _fmt_dt(r.ended_at)
            } for r in self._results],
        }
        with open(p, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        return p

    def _save_charts(self, metrics: Dict[str, Any]) -> Dict[str, Optional[Path]]:
        if not _HAS_MPL:
            print("⚠️ matplotlib não encontrado — pulando gráficos (pip install matplotlib).")
            return {}
        
        charts = {}
        
        # 1. Gráfico de pizza geral
        counts = {
            "SUCCESS": metrics["success"],
            "ERROR": metrics["error"],
            "ALERT": metrics["alert"],
        }
        labels, sizes, colors = [], [], []
        color_map = {"SUCCESS": "#4CAF50", "ERROR": "#F44336", "ALERT": "#FF9800"}
        for k in ("SUCCESS", "ERROR", "ALERT"):
            if counts[k] > 0:
                labels.append(f"{k} ({counts[k]})")
                sizes.append(counts[k])
                colors.append(color_map[k])
        if sizes:
            fig = plt.figure(figsize=(8, 6))
            plt.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90, colors=colors)
            plt.title("Distribuição Geral de Resultados")
            plt.tight_layout()
            out = self.out_dir / f"executions-{self._stamp}-pie-geral.png"
            fig.savefig(out, dpi=120, bbox_inches='tight')
            plt.close(fig)
            charts["pie_geral"] = out
        
        # 2. Gráfico de cadastros
        if metrics["cadastros_total"] > 0:
            fig = plt.figure(figsize=(8, 6))
            labels = []
            sizes = []
            colors = []
            for status, count in [("SUCCESS", metrics["cadastros_success"]), 
                                ("ERROR", metrics["cadastros_error"]), 
                                ("ALERT", metrics["cadastros_alert"])]:
                if count > 0:
                    labels.append(f"{status} ({count})")
                    sizes.append(count)
                    colors.append(color_map[status])
            if sizes:
                plt.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90, colors=colors)
                plt.title("Distribuição de Resultados - Cadastros")
                plt.tight_layout()
                out = self.out_dir / f"executions-{self._stamp}-pie-cadastros.png"
                fig.savefig(out, dpi=120, bbox_inches='tight')
                plt.close(fig)
                charts["pie_cadastros"] = out
        
        # 3. Gráfico de cenários
        if metrics["cenarios_total"] > 0:
            fig = plt.figure(figsize=(8, 6))
            labels = []
            sizes = []
            colors = []
            for status, count in [("SUCCESS", metrics["cenarios_success"]), 
                                ("ERROR", metrics["cenarios_error"]), 
                                ("ALERT", metrics["cenarios_alert"])]:
                if count > 0:
                    labels.append(f"{status} ({count})")
                    sizes.append(count)
                    colors.append(color_map[status])
            if sizes:
                plt.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90, colors=colors)
                plt.title("Distribuição de Resultados - Cenários")
                plt.tight_layout()
                out = self.out_dir / f"executions-{self._stamp}-pie-cenarios.png"
                fig.savefig(out, dpi=120, bbox_inches='tight')
                plt.close(fig)
                charts["pie_cenarios"] = out
        
        # 4. Gráfico de eficiência
        fig, ax = plt.subplots(figsize=(10, 6))
        categories = ['Geral', 'Cadastros', 'Cenários']
        efficiencies = [metrics["efficiency_pct"], metrics["cadastros_efficiency_pct"], metrics["cenarios_efficiency_pct"]]
        bars = ax.bar(categories, efficiencies, color=['#2196F3', '#4CAF50', '#FF9800'])
        ax.set_ylabel('Eficiência (%)')
        ax.set_title('Eficiência do Sistema por Categoria')
        ax.set_ylim(0, 100)
        
        # Adicionar valores nas barras
        for bar, efficiency in zip(bars, efficiencies):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                   f'{efficiency:.1f}%', ha='center', va='bottom')
        
        plt.tight_layout()
        out = self.out_dir / f"executions-{self._stamp}-efficiency.png"
        fig.savefig(out, dpi=120, bbox_inches='tight')
        plt.close(fig)
        charts["efficiency"] = out
        
        return charts

    def _save_html(self, metrics: Dict[str, Any], charts: Dict[str, Optional[Path]]) -> Path:
        p = self.out_dir / f"executions-{self._stamp}.html"
        def esc(x: str) -> str:
            return (x or "").replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
        rows = []
        for r in self._results:
            rows.append(f"""
<tr>
  <td>{esc(r.name)}</td>
  <td>{esc(r.test_type)}</td>
  <td>{esc(r.status)}</td>
  <td>{_fmt_dt(r.started_at)}</td>
  <td>{_fmt_dt(r.ended_at)}</td>
  <td>{_ms_to_hhmmss(r.duration_ms)} ({r.duration_ms} ms)</td>
  <td>{esc(r.error_message or "")}</td>
  <td>{esc(" | ".join(r.screenshots or []))}</td>
</tr>""")
        
        charts_html = ""
        for chart_name, chart_path in charts.items():
            if chart_path:
                charts_html += f"<img src='{chart_path.name}' alt='Gráfico {chart_name}' style='max-width:100%;height:auto;margin:10px;border:1px solid #eee'/>"
        
        html = f"""<!doctype html>
<html lang="pt-br"><head><meta charset="utf-8"/>
<title>Relatório de Execuções - {self._stamp}</title>
<style>
body{{font-family:Arial, sans-serif; margin:24px}}
h1,h2{{margin:0 0 12px}}
.grid{{display:grid; grid-template-columns:1fr 1fr; gap:16px}}
table{{width:100%; border-collapse:collapse; margin-top:16px}}
th,td{{border:1px solid #ddd; padding:8px; font-size:14px}}
th{{background:#f6f6f6; text-align:left}}
.kpi{{background:#fafafa; padding:12px; border:1px solid #eee; border-radius:8px}}
.muted{{color:#666}}
</style></head><body>
<h1>Relatório de Execuções</h1>
<div class="muted">Gerado em: {_fmt_dt(datetime.now())} · Janela: {metrics["window_started_at"]} → {metrics["window_ended_at"]}</div>
<div class="muted">Ambiente: {self.environment} · Usuário: {self.username}</div>
<div class="grid">
  <div class="kpi">
    <h2>KPIs Gerais</h2>
    <p><b>Total:</b> {metrics["total"]}</p>
    <p><b>SUCCESS:</b> {metrics["success"]} · <b>ERROR:</b> {metrics["error"]} · <b>ALERT:</b> {metrics["alert"]}</p>
    <p><b>Pass rate:</b> {metrics["pass_rate_pct"]}%</p>
    <p><b>Eficiência:</b> {metrics["efficiency_pct"]}%</p>
  </div>
  <div class="kpi">
    <h2>Cadastros</h2>
    <p><b>Total:</b> {metrics["cadastros_total"]}</p>
    <p><b>SUCCESS:</b> {metrics["cadastros_success"]} · <b>ERROR:</b> {metrics["cadastros_error"]} · <b>ALERT:</b> {metrics["cadastros_alert"]}</p>
    <p><b>Pass rate:</b> {metrics["cadastros_pass_rate_pct"]}%</p>
    <p><b>Eficiência:</b> {metrics["cadastros_efficiency_pct"]}%</p>
  </div>
</div>
<div style="text-align:center; margin:20px 0;">
{charts_html}
</div>
<table>
<thead><tr><th>Execução</th><th>Tipo</th><th>Status</th><th>Início</th><th>Fim</th><th>Duração</th><th>Erro</th><th>Screenshots</th></tr></thead>
<tbody>
{''.join(rows)}
</tbody></table>
</body></html>"""
        with open(p, "w", encoding="utf-8") as f:
            f.write(html)
        return p

    def _save_docx(self, metrics: Dict[str, Any], charts: Dict[str, Optional[Path]]) -> Optional[Path]:
        if not _HAS_DOCX:
            print("⚠️ python-docx não encontrado — pulando DOCX (pip install python-docx).")
            return None
        
        p = self.out_dir / f"executions-{self._stamp}.docx"
        doc = Document()
        
        # Título principal
        title = doc.add_heading("Relatório de Testes de QA", 0)
        title.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        # Informações básicas
        doc.add_paragraph(f"Gerado em: {_fmt_dt(datetime.now())}")
        doc.add_paragraph(f"Período de execução: {metrics['window_started_at']} → {metrics['window_ended_at']}")
        doc.add_paragraph(f"Tempo total de execução: {_ms_to_hhmmss(metrics['window_total_ms'])}")
        
        # Informações do ambiente
        doc.add_heading("Informações do Ambiente de Teste", level=1)
        env_table = doc.add_table(rows=3, cols=2)
        env_table.style = 'Table Grid'
        env_table.rows[0].cells[0].text = "Ambiente Testado"
        env_table.rows[0].cells[1].text = self.environment
        env_table.rows[1].cells[0].text = "Usuário"
        env_table.rows[1].cells[1].text = self.username
        env_table.rows[2].cells[0].text = "Senha"
        env_table.rows[2].cells[1].text = self.password
        
        # Resumo executivo
        doc.add_heading("Resumo Executivo", level=1)
        summary_table = doc.add_table(rows=8, cols=4)
        summary_table.style = 'Table Grid'
        
        # Cabeçalhos
        headers = summary_table.rows[0].cells
        headers[0].text = "Métrica"
        headers[1].text = "Geral"
        headers[2].text = "Cadastros"
        headers[3].text = "Cenários"
        
        # Dados
        data_rows = [
            ("Total de Testes", str(metrics["total"]), str(metrics["cadastros_total"]), str(metrics["cenarios_total"])),
            ("Sucessos", str(metrics["success"]), str(metrics["cadastros_success"]), str(metrics["cenarios_success"])),
            ("Erros", str(metrics["error"]), str(metrics["cadastros_error"]), str(metrics["cenarios_error"])),
            ("Alertas", str(metrics["alert"]), str(metrics["cadastros_alert"]), str(metrics["cenarios_alert"])),
            ("Taxa de Sucesso (%)", f"{metrics['pass_rate_pct']}%", f"{metrics['cadastros_pass_rate_pct']}%", f"{metrics['cenarios_pass_rate_pct']}%"),
            ("Eficiência do Sistema (%)", f"{metrics['efficiency_pct']}%", f"{metrics['cadastros_efficiency_pct']}%", f"{metrics['cenarios_efficiency_pct']}%"),
            ("Tempo Total", _ms_to_hhmmss(metrics["duration_total_ms"]), "-", "-"),
            ("Tempo Médio", _ms_to_hhmmss(metrics["duration_avg_ms"]), "-", "-")
        ]
        
        for i, row_data in enumerate(data_rows, 1):
            cells = summary_table.rows[i].cells
            for j, cell_data in enumerate(row_data):
                cells[j].text = cell_data
        
        # Gráficos
        if charts:
            doc.add_heading("Análise Gráfica", level=1)
            
            # Gráfico geral
            if charts.get("pie_geral") and charts["pie_geral"].exists():
                doc.add_heading("Distribuição Geral de Resultados", level=2)
                try:
                    doc.add_picture(str(charts["pie_geral"]), width=Inches(5))
                    last_paragraph = doc.paragraphs[-1]
                    last_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
                except Exception as e:
                    doc.add_paragraph(f"Erro ao carregar gráfico: {e}")
            
            # Gráfico de cadastros
            if charts.get("pie_cadastros") and charts["pie_cadastros"].exists():
                doc.add_heading("Distribuição de Resultados - Cadastros", level=2)
                try:
                    doc.add_picture(str(charts["pie_cadastros"]), width=Inches(5))
                    last_paragraph = doc.paragraphs[-1]
                    last_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
                except Exception as e:
                    doc.add_paragraph(f"Erro ao carregar gráfico: {e}")
            
            # Gráfico de cenários
            if charts.get("pie_cenarios") and charts["pie_cenarios"].exists():
                doc.add_heading("Distribuição de Resultados - Cenários", level=2)
                try:
                    doc.add_picture(str(charts["pie_cenarios"]), width=Inches(5))
                    last_paragraph = doc.paragraphs[-1]
                    last_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
                except Exception as e:
                    doc.add_paragraph(f"Erro ao carregar gráfico: {e}")
            
            # Gráfico de eficiência
            if charts.get("efficiency") and charts["efficiency"].exists():
                doc.add_heading("Eficiência do Sistema", level=2)
                try:
                    doc.add_picture(str(charts["efficiency"]), width=Inches(6))
                    last_paragraph = doc.paragraphs[-1]
                    last_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
                except Exception as e:
                    doc.add_paragraph(f"Erro ao carregar gráfico: {e}")
        
        # Screenshots de erro
        if metrics["error_screenshots"]:
            doc.add_heading("Screenshots de Erros", level=1)
            for i, error_info in enumerate(metrics["error_screenshots"], 1):
                doc.add_heading(f"Erro {i}: {error_info['test_name']}", level=2)
                if error_info["error_message"]:
                    doc.add_paragraph(f"Mensagem de erro: {error_info['error_message']}")
                doc.add_paragraph(f"Screenshot: {error_info['screenshot']}")
        
        # Detalhes das execuções
        doc.add_heading("Detalhes das Execuções", level=1)
        table = doc.add_table(rows=1, cols=8)
        table.style = 'Table Grid'
        
        # Cabeçalhos
        hdr = table.rows[0].cells
        hdr[0].text = "Execução"
        hdr[1].text = "Tipo"
        hdr[2].text = "Status"
        hdr[3].text = "Início"
        hdr[4].text = "Fim"
        hdr[5].text = "Duração"
        hdr[6].text = "Erro"
        hdr[7].text = "Screenshots"
        
        # Dados das execuções
        for r in self._results:
            row = table.add_row().cells
            row[0].text = r.name
            row[1].text = r.test_type
            row[2].text = r.status
            row[3].text = _fmt_dt(r.started_at)
            row[4].text = _fmt_dt(r.ended_at)
            row[5].text = f"{_ms_to_hhmmss(r.duration_ms)} ({r.duration_ms} ms)"
            row[6].text = (r.error_message or "")[:200] + ("..." if r.error_message and len(r.error_message) > 200 else "")
            row[7].text = " | ".join(r.screenshots or [])
        
        # Conclusões
        doc.add_heading("Conclusões", level=1)
        
        if metrics["efficiency_pct"] >= 90:
            doc.add_paragraph("✅ Excelente: O sistema apresentou eficiência superior a 90%.")
        elif metrics["efficiency_pct"] >= 80:
            doc.add_paragraph("✅ Bom: O sistema apresentou eficiência satisfatória (80-90%).")
        elif metrics["efficiency_pct"] >= 70:
            doc.add_paragraph("⚠️ Atenção: O sistema apresentou eficiência moderada (70-80%). Recomenda-se investigação.")
        else:
            doc.add_paragraph("❌ Crítico: O sistema apresentou eficiência baixa (<70%). Ação imediata necessária.")
        
        doc.add_paragraph(f"• Total de testes executados: {metrics['total']}")
        doc.add_paragraph(f"• Taxa de sucesso geral: {metrics['pass_rate_pct']}%")
        doc.add_paragraph(f"• Eficiência do sistema: {metrics['efficiency_pct']}%")
        
        if metrics["error"] > 0:
            doc.add_paragraph(f"• Foram identificados {metrics['error']} erros que necessitam correção.")
        
        if metrics["alert"] > 0:
            doc.add_paragraph(f"• Há {metrics['alert']} alertas que requerem atenção.")
        
        try:
            doc.save(p)
            return p
        except Exception as e:
            print(f"Erro ao salvar DOCX: {e}")
            return None

    def finalize_reports(self) -> Dict[str, Optional[Path]]:
        if self._closed:
            return {}
        self._closed = True
        if self._run_ended_at is None:
            self.end_run()
        
        metrics = self._metrics()
        out = {}
        
        try:
            charts = self._save_charts(metrics)
            out["csv"] = self._save_csv()
            out["json"] = self._save_json(metrics)
            out["html"] = self._save_html(metrics, charts)
            out["docx"] = self._save_docx(metrics, charts)
            out.update(charts)
            
            # Confirmação:
            print("✅ Relatórios gerados em:", self.out_dir.resolve())
            for k, v in out.items():
                if v and v.exists(): 
                    print(f" - {k}: {Path(v).name}")
        except Exception as e:
            print(f"❌ Falha ao gerar relatórios: {e}")
            traceback.print_exc()
        return out

    def _safe_finalize_if_needed(self):
        # garante geração mesmo se esquecer de chamar finalize_reports()
        try:
            if not self._closed and self._results:
                self.finalize_reports()
        except Exception:
            pass


# ================== HELPERS ==================
def _fmt_dt(dt: Optional[datetime]) -> str:
    return dt.strftime("%Y-%m-%d %H:%M:%S") if dt else ""

def _ms_to_hhmmss(ms: int) -> str:
    s = ms / 1000.0
    h = int(s // 3600); s -= h * 3600
    m = int(s // 60); s -= m * 60
    return f"{h:02d}:{m:02d}:{int(s):02d}"


# ================== EXEMPLO DE USO ==================
def exemplo_de_uso():
    """Exemplo prático de como usar o QAReporter"""
    
    # Inicializa o reporter com configurações personalizadas
    reporter = QAReporter(
        out_dir="relatorios_qa",
        environment="https://meuapp.com.br/login",
        username="teste.qa@empresa.com",
        password="minhasenha123"
    )
    
    # Inicia a execução
    reporter.start_run()
    
    # Exemplo 1: Usando context manager para cadastros
    with reporter.cadastro("Cadastro de Cliente - João Silva") as ctx:
        # Simula teste de cadastro
        import time
        time.sleep(1)  # Simula tempo de execução
        ctx.attach_screenshot("screenshot_cadastro_joao.png")
        ctx.set_extra(cliente_id=12345, email="joao@email.com")
        # Se tudo correu bem, será marcado como SUCCESS automaticamente
    
    # Exemplo 2: Cadastro com erro
    with reporter.cadastro("Cadastro de Cliente - CPF Inválido") as ctx:
        import time
        time.sleep(0.5)
        ctx.attach_screenshot("screenshot_erro_cpf.png")
        # Simula um erro
        raise ValueError("CPF 123.456.789-00 é inválido")
    
    # Exemplo 3: Usando métodos diretos para cenários
    inicio = datetime.now()
    try:
        # Simula teste de cenário
        import time
        time.sleep(2)
        reporter.success("Login com credenciais válidas", inicio, "SCENARIO", 
                        screenshots=["login_success.png"])
    except Exception as e:
        reporter.error("Login com credenciais válidas", inicio, str(e), "SCENARIO",
                      screenshots=["login_error.png"])
    
    # Exemplo 4: Cenário com alerta
    inicio = datetime.now()
    import time
    time.sleep(1)
    reporter.alert("Validação de performance - tempo limite", inicio, 
                   "Login demorou mais que 3 segundos (4.2s)", "SCENARIO")
    
    # Finaliza e gera relatórios
    reporter.end_run()
    arquivos = reporter.finalize_reports()
    
    print("\n" + "="*50)
    print("RELATÓRIOS GERADOS:")
    print("="*50)
    for tipo, caminho in arquivos.items():
        if caminho and caminho.exists():
            print(f"{tipo.upper()}: {caminho}")


if __name__ == "__main__":
    # Executa o exemplo se o arquivo for rodado diretamente
    exemplo_de_uso()