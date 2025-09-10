# qa_reporter.py
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict
from statistics import mean
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH

@dataclass
class TestFailure:
    cadastro: str
    referencia: Optional[str] = None   # ex: ID interno, código, contrato, etc.
    erro: str = ""
    evidencias: Dict[str, str] = field(default_factory=dict)  # {"screenshot": "...", "log": "..."}

class QAReporter:
    def __init__(self, reports_dir: Path):
        self.reports_dir = Path(reports_dir)
        self.inicio = None
        self.fim = None
        self.sucessos = 0
        self.erros = 0
        self.alertas = 0  # NÃO entra no cálculo, apenas informativo
        self.execucoes: List[Dict] = []  # [{ "cadastro": ..., "status": "success|error|alert", "duracao_s": float }]
        self.falhas: List[TestFailure] = []

    # marque o início e o fim do run
    def start(self):
        self.inicio = datetime.now()

    def stop(self):
        self.fim = datetime.now()

    # registre cada cadastro executado
    def record(self, cadastro: str, status: str, duracao_s: float, 
               referencia: Optional[str] = None, erro: Optional[str] = None,
               evidencias: Optional[Dict[str, str]] = None):
        status = status.lower().strip()
        self.execucoes.append({
            "cadastro": cadastro,
            "status": status,
            "duracao_s": duracao_s,
            "referencia": referencia,
            "erro": erro,
            "evidencias": evidencias or {}
        })
        if status == "success":
            self.sucessos += 1
        elif status == "error":
            self.erros += 1
            self.falhas.append(TestFailure(
                cadastro=cadastro,
                referencia=referencia,
                erro=(erro or "").strip(),
                evidencias=(evidencias or {})
            ))
        elif status == "alert":
            self.alertas += 1  # não conta como sucesso/erro

    def _pct(self, parte: int, total: int) -> str:
        return f"{(parte/total*100):.2f}%" if total > 0 else "0.00%"

    def save_docx(self, nome_arquivo: Optional[str] = None, 
                  ambiente: str = "-", versao: str = "-", out_base: Optional[Path] = None) -> Path:
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        dt_fmt = "%d/%m/%Y %H:%M:%S"
        inicio_s = self.inicio.strftime(dt_fmt) if self.inicio else "-"
        fim_s    = self.fim.strftime(dt_fmt) if self.fim else "-"
        duracao_total_s = (self.fim - self.inicio).total_seconds() if (self.inicio and self.fim) else 0

        total_exec = self.sucessos + self.erros  # ALERTA não entra
        media_por_cadastro = (mean([e["duracao_s"] for e in self.execucoes if e["status"] in ("success","error")])
                              if total_exec > 0 else 0.0)

        pct_ok = self._pct(self.sucessos, total_exec)
        pct_err = self._pct(self.erros, total_exec)

        # monta DOCX
        doc = Document()
        title = doc.add_heading('Relatório de Eficiência do Sistema — Execução de Testes', 0)
        title.alignment = WD_ALIGN_PARAGRAPH.CENTER

        p = doc.add_paragraph()
        p.add_run('Início do Teste: ').bold = True; p.add_run(inicio_s)
        p = doc.add_paragraph()
        p.add_run('Fim do Teste: ').bold = True; p.add_run(fim_s)

        doc.add_heading('Resumo da Execução', level=1)
        table = doc.add_table(rows=6, cols=3)
        hdr = table.rows[0].cells
        hdr[0].text, hdr[1].text, hdr[2].text = 'Métrica', 'Quantidade', 'Percentual'
        linhas = [
            ('Cadastros com Sucesso', str(self.sucessos), pct_ok),
            ('Falhas (Erro)', str(self.erros), pct_err),
            ('Total de Cadastros Executados', str(total_exec), '—'),
            ('Tempo Total de Execução', f'{int(duracao_total_s)}s', '—'),
            ('Média por Cadastro', f'{media_por_cadastro:.2f}s', '—')
        ]
        for i, (m, q, pct) in enumerate(linhas, start=1):
            row = table.rows[i].cells
            row[0].text, row[1].text, row[2].text = m, q, pct

        doc.add_paragraph(f'Alertas informativos (não contabilizam no total): {self.alertas}')

        doc.add_heading('Cadastros com Falha (para análise)', level=1)
        if not self.falhas:
            doc.add_paragraph('Nenhuma falha registrada.')
        else:
            for f in self.falhas:
                para = doc.add_paragraph()
                para.add_run('Cadastro: ').bold = True; para.add_run(f.cadastro)
                if f.referencia:
                    para.add_run(' | Referência: ').bold = True; para.add_run(str(f.referencia))
                if f.erro:
                    doc.add_paragraph(f'Erro: {f.erro}')
                if f.evidencias:
                    evid = ', '.join([f'{k}: {v}' for k, v in f.evidencias.items()])
                    doc.add_paragraph(f'Evidências: {evid}')

        doc.add_heading('Detalhes Técnicos', level=1)
        doc.add_paragraph(f'Ambiente utilizado para o Teste: {ambiente}')
        doc.add_paragraph(f'Versão do Sistema: {versao}')
        if out_base:
            doc.add_paragraph(f'Caminho do diretório de saída: {out_base}')

        # nome do arquivo
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome = nome_arquivo or f"Relatorio_QA_{stamp}.docx"
        destino = self.reports_dir / nome
        doc.save(destino)
        return destino
