
# -*- coding: utf-8 -*-
"""
QA Reporter — Relatório DOCX (Word) com gráficos
------------------------------------------------
Uso básico:

from qa_reporter import QAReporter
from datetime import datetime

rep = QAReporter(out_dir="reports", environment="Homologação", executor="Runner CLI", system_version="v2025.09")
rep.start_run(summary="Execução em massa — Cadastros Adicionais")

h1 = rep.start_scenario("Cadastro de Cor — Cenário 1", test_type="CADASTRO")
# ... rodar o cenário ...
rep.finish_scenario(h1, status="SUCCESS", screenshots=["path/screen1.png"], extra={"area": "Cadastros/Cor"})

h2 = rep.start_scenario("Cadastro de Capela — Cenário 2 (cancelar)", test_type="CADASTRO")
# ... rodar o cenário ...
rep.finish_scenario(h2, status="ERROR", error_message="Timeout ao clicar em Salvar", severity="HIGH")

rep.end_run()
docx_path = rep.save_docx("Relatorio_QA")
print("Gerado:", docx_path)

Compatível com empacotamento (PyInstaller) pois usa backends headless (matplotlib Agg).
"""

from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Any
import os, traceback, platform
import io
import re
# Dependências opcionais (não travar execução caso ausentes)
_HAS_MPL = False
_HAS_DOCX = False
try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    _HAS_MPL = True
except Exception:
    _HAS_MPL = False

try:
    from docx import Document
    from docx.shared import Inches, Pt
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.enum.table import WD_TABLE_ALIGNMENT
    _HAS_DOCX = True
except Exception:
    _HAS_DOCX = False


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
    test_id: Optional[str] = None
    severity: str = "MEDIUM"     # LOW | MEDIUM | HIGH | CRITICAL


def _fmt_dt(dt: Optional[datetime]) -> str:
    if not dt:
        return ""
    # dd/MM/yyyy HH:mm:ss
    return dt.strftime("%d/%m/%Y %H:%M:%S")


def _ms_readable(ms: int) -> str:
    s = int(round(ms / 1000.0))
    h = s // 3600
    m = (s % 3600) // 60
    sec = s % 60
    parts = []
    if h:
        parts.append(f"{h}h")
    if m or (h and not m):
        parts.append(f"{m}m")
    parts.append(f"{sec}s")
    return " ".join(parts)


class QAReporter:
    def __init__(self, out_dir: str | Path = "reports",
                 environment: str = "Produção",
                 executor: str = "Pipeline CI/CD",
                 system_version: str = "1.0.0",
                 username: str = "Robô de Testes"):
        self.out_dir = Path(out_dir)
        self.out_dir.mkdir(parents=True, exist_ok=True)
        self._results: List[ScenarioResult] = []
        self._run_started_at: Optional[datetime] = None
        self._run_ended_at: Optional[datetime] = None
        self.environment = environment
        self.executor = executor
        self.system_version = system_version
        self.username = username
        self.summary = ""
        self._stamp = datetime.now().strftime("%Y%m%d-%H%M%S")

    # ===== ciclo de execução =====
    def start_run(self, summary: str = ""):
        self._run_started_at = datetime.now()
        self.summary = summary or ""

    def end_run(self):
        self._run_ended_at = datetime.now()

    ERROR_PATTERNS = [
        r'^\s*\[\!\]\s*erro\b',             # ex.: [!] Erro: ...
        r'\berro:\s',                       # "Erro: ..."
        r'\bexception\b',                   # exception genérica
        r'\bexce(ç|c)ão\b',                 # "exceção"
        r'Traceback \(most recent call last\):',
    ]
    ERROR_RX = re.compile("|".join(ERROR_PATTERNS), re.IGNORECASE | re.MULTILINE)

    # opcional: marcador para forçar sucesso mesmo com "erro" no texto
    FORCE_OK_RX = re.compile(r'\[TESTE_OK\]', re.IGNORECASE)


    # ===== registrar cenários =====
    def start_scenario(self, name: str, test_type: str = "SCENARIO", test_id: str | None = None) -> Dict[str, Any]:
        return {
            "name": name,
            "test_type": test_type,
            "test_id": test_id or f"{test_type}_{len(self._results)+1:04d}",
            "started_at": datetime.now()
        }

    def finish_scenario(self, handle: Dict[str, Any], status: str,
                        error_message: Optional[str] = None,
                        screenshots: Optional[List[str]] = None,
                        extra: Optional[Dict[str, Any]] = None,
                        severity: str = "MEDIUM"):
        now = datetime.now()
        dur_ms = int((now - handle["started_at"]).total_seconds() * 1000)
        self._results.append(
            ScenarioResult(
                name=handle["name"],
                status=str(status or "SUCCESS").upper(),
                started_at=handle["started_at"],
                ended_at=now,
                duration_ms=max(0, dur_ms),
                test_type=handle.get("test_type", "SCENARIO"),
                error_message=(error_message or None),
                screenshots=screenshots or [],
                extra=extra or {},
                test_id=handle.get("test_id"),
                severity=str(severity or "MEDIUM").upper()
            )
        )

    # ===== métricas =====
    def _metrics(self) -> Dict[str, Any]:
        total = len(self._results)
        ok = sum(1 for r in self._results if r.status == "SUCCESS")
        err = sum(1 for r in self._results if r.status == "ERROR")
        alt = sum(1 for r in self._results if r.status == "ALERT")
        pass_rate = (ok / total * 100.0) if total else 0.0

        # janela/tempo
        started = self._run_started_at or (min((r.started_at for r in self._results), default=None))
        ended = self._run_ended_at or (max((r.ended_at for r in self._results), default=None))
        window_ms = int((ended - started).total_seconds() * 1000) if (started and ended) else 0
        dur_total_ms = sum(r.duration_ms for r in self._results)
        dur_avg_ms = int(dur_total_ms / total) if total else 0

        cad = [r for r in self._results if r.test_type == "CADASTRO"]
        cad_total = len(cad)
        cad_ok = sum(1 for r in cad if r.status == "SUCCESS")
        cad_err = sum(1 for r in cad if r.status == "ERROR")
        cad_alt = sum(1 for r in cad if r.status == "ALERT")
        cad_pass = (cad_ok / cad_total * 100.0) if cad_total else 0.0
        cad_dur_total = sum(r.duration_ms for r in cad)
        cad_dur_avg = int(cad_dur_total / cad_total) if cad_total else 0

        return {
            "total": total,
            "success": ok,
            "error": err,
            "alert": alt,
            "pass_rate_pct": round(pass_rate, 2),
            "started_at": started,
            "ended_at": ended,
            "window_ms": window_ms,
            "duration_total_ms": dur_total_ms,
            "duration_avg_ms": dur_avg_ms,
            "cad_total": cad_total,
            "cad_success": cad_ok,
            "cad_error": cad_err,
            "cad_alert": cad_alt,
            "cad_pass_rate_pct": round(cad_pass, 2),
            "cad_duration_total_ms": cad_dur_total,
            "cad_duration_avg_ms": cad_dur_avg,
            "failures": [r for r in self._results if r.status == "ERROR"],
            "system_info": {
                "platform": platform.platform(),
                "python": platform.python_version(),
                "hostname": platform.node(),
                "processor": platform.processor(),
            }
        }

    # ===== gráficos de pizza =====
    def _make_pie(self, ok: int, err: int, alt: int, title: str,
                size_in: float = 2.8, dpi: int = 180) -> Optional[Path]:
        if not _HAS_MPL:
            return None

        labels = ["Sucesso", "Erro", "Alerta"]
        sizes  = [ok, err, alt]

        if sum(sizes) == 0:
            return None

        # rótulos: não mostra para fatias com valor 0
        show_labels = [lbl if val > 0 else "" for lbl, val in zip(labels, sizes)]
        show_labels = [lbl if val > 0 else None for lbl, val in zip(labels, sizes)]

        # CORES FIXAS (mesma ordem dos labels acima)
        colors = [
            "#2ecc71",  # Sucesso  -> verde
            "#e74c3c",  # Erro     -> vermelho
            "#f1c40f",  # Alerta   -> amarelo
        ]

        def _autopct(pct: float) -> str:
            return f"{pct:.0f}%" if pct >= 1.0 else ""

        fig, ax = plt.subplots(figsize=(size_in, size_in), dpi=dpi)
        wedges, texts, autotexts = ax.pie(
            sizes,
            labels=show_labels,
            colors=colors,           # <--- fixa as cores
            autopct=_autopct,
            startangle=90,
            labeldistance=1.08,
            pctdistance=0.72,
            wedgeprops={"linewidth": 0.8, "edgecolor": "white"},
            textprops={"fontsize": 8}
        )
        ax.axis("equal")
        ax.set_title(title, fontsize=10)

        out = self.out_dir / f"chart_{title.replace(' ', '_').lower()}_{self._stamp}.png"
        fig.savefig(out, bbox_inches="tight")
        plt.close(fig)
        return out


    # ===== DOCX =====
    def save_docx(self, base_name: str = "Relatorio_QA") -> Path:
        if not _HAS_DOCX:
            raise RuntimeError("python-docx não encontrado. pip install python-docx")
        m = self._metrics()
        # gráficos
        chart_all = self._make_pie(m["success"], m["error"], m["alert"], "Geral")
        chart_cad = self._make_pie(m["cad_success"], m["cad_error"], m["cad_alert"], "Cadastros")

        doc = Document()
        # estilos gerais
        style = doc.styles["Normal"]
        style.font.name = "Arial"
        style.font.size = Pt(11)

        # título do relatório
        h = doc.add_heading("Relatório de Eficiência do Sistema — Execução de Testes", level=0)
        h.alignment = WD_ALIGN_PARAGRAPH.CENTER

        # data/hora e período
        doc.add_paragraph(f"Data/Hora do Relatório: {_fmt_dt(datetime.now())}")
        started = _fmt_dt(m["started_at"])
        ended = _fmt_dt(m["ended_at"])
        doc.add_paragraph(f"Período do Teste: {started} — {ended}")
        if self.summary:
            doc.add_paragraph(f"Resumo da Execução: {self.summary}")
        doc.add_paragraph("")

        # seção: resumo da execução
        doc.add_heading("Resumo da Execução", level=1)
        table = doc.add_table(rows=6, cols=3)
        table.style = "Table Grid"
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        hdr = table.rows[0].cells
        hdr[0].text = "Métrica"
        hdr[1].text = "Quantidade"
        hdr[2].text = "Percentual"
        for c in hdr:
            c.paragraphs[0].runs[0].bold = True

        data_rows = [
            ("Cadastros com Sucesso", str(m["cad_success"]), f"{m['cad_pass_rate_pct']:.2f}%"),
            ("Falhas (Erro)", str(m["cad_error"]), f"{(m['cad_error']/m['cad_total']*100.0 if m['cad_total'] else 0):.2f}%"),
            ("Total de Cadastros Executados", str(m["cad_total"]), "—"),
            ("Tempo Total de Execução", _ms_readable(m["cad_duration_total_ms"]), "—"),
            ("Média por Cadastro", _ms_readable(m["cad_duration_avg_ms"]), "—"),
        ]
        for i, (met, qtd, pct) in enumerate(data_rows, start=1):
            r = table.rows[i].cells
            r[0].text, r[1].text, r[2].text = met, qtd, pct

        doc.add_paragraph("")
        obs = doc.add_paragraph()
        obs.add_run("Obs.: ").bold = True
        obs.add_run('Registros com "alerta" não são contabilizados como sucesso ou erro; apenas informativos.')
        doc.add_paragraph("")

        CHART_WIDTH_IN = 2.8
       
        # gráficos (se existirem)
        if chart_all or chart_cad:
            doc.add_heading("Gráficos", level=1)
        if chart_all and Path(chart_all).exists():
            doc.add_paragraph("Distribuição Geral")
            doc.add_picture(str(chart_all), width=Inches(CHART_WIDTH_IN))
        if chart_cad and Path(chart_cad).exists():
            doc.add_paragraph("Distribuição — Cadastros")
            doc.add_picture(str(chart_cad), width=Inches(CHART_WIDTH_IN))
            doc.add_paragraph("")

        # falhas
        doc.add_heading("Cadastros com Falha (para análise)", level=1)
        fails = [f for f in m["failures"] if f.test_type == "CADASTRO"]
        if not fails:
            doc.add_paragraph("Nenhuma falha registrada nesta execução.")
        else:
            doc.add_paragraph(f"Foram encontradas {len(fails)} falhas que requerem análise:")
            doc.add_paragraph("")
            for idx, f in enumerate(fails, 1):
                p = doc.add_paragraph()
                p.add_run(f"Falha {idx}: ").bold = True
                p.add_run(f.name)
                if f.test_id:
                    doc.add_paragraph(f"• ID/Referência: {f.test_id}")
                if f.error_message:
                    # primeira linha do erro
                    first = f.error_message.strip().splitlines()[0][:250]
                    doc.add_paragraph(f"• Erro: {first}")
                if f.screenshots:
                    doc.add_paragraph("• Evidências: " + ", ".join(f.screenshots))
                doc.add_paragraph(f"• Timestamp: {_fmt_dt(f.started_at)}")
                doc.add_paragraph(f"• Severidade: {f.severity}")
                doc.add_paragraph("")

        # detalhes técnicos
        doc.add_heading("Detalhes Técnicos", level=1)
        doc.add_paragraph(f"• Ambiente: {self.environment}")
        doc.add_paragraph(f"• Executor: {self.executor}")
        doc.add_paragraph(f"• Versão do Sistema: {self.system_version}")
        doc.add_paragraph(f"• Plataforma: {m['system_info']['platform']}")
        doc.add_paragraph(f"• Hostname: {m['system_info']['hostname']}")
        doc.add_paragraph(f"• Python: {m['system_info']['python']}")
        doc.add_paragraph("")

        out = self.out_dir / f"{base_name}_{self._stamp}.docx"
        doc.save(str(out))
        return out
