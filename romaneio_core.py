"""Lógica compartilhada de leitura e exportação dos aplicativos de romaneio."""
from __future__ import annotations

import csv
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

import pdfplumber


class PDFSemTextoError(ValueError):
    """PDF sem camada de texto extraível (por exemplo, documento digitalizado)."""


def extrair_texto_pdf(caminho_pdf: Path) -> str:
    with pdfplumber.open(caminho_pdf) as pdf:
        partes = [pagina.extract_text() or "" for pagina in pdf.pages]
    texto = "\n".join(partes).strip()
    if not texto:
        raise PDFSemTextoError("PDF sem texto extraível; pode ser um documento digitalizado.")
    return texto


def data_valida(valor: str) -> bool:
    try:
        datetime.strptime(valor, "%d/%m/%Y")
        return True
    except ValueError:
        return False


def extrair_minutas_pdf(caminho_pdf: Path) -> Tuple[List[str], str]:
    texto = extrair_texto_pdf(caminho_pdf)
    candidatas = re.findall(r"(?<!\d)(\d{2}/\d{2}/\d{4})(?!\d)", texto)
    data = next((d for d in candidatas if data_valida(d)), "")
    minutas = re.findall(r"\b\d{6}\s*[-–—]\s*(\d+)\b", re.sub(r"\|", " ", texto))
    if not minutas:
        raise ValueError("Nenhuma minuta encontrada no formato esperado (6 dígitos, hífen e número).")
    return minutas, data


def extrair_romaneio_pdf(caminho_pdf: Path) -> Dict:
    texto_completo = extrair_texto_pdf(caminho_pdf)
    linhas = [re.sub(r"\s+", " ", linha).strip() for linha in texto_completo.splitlines()]
    texto = "\n".join(linhas)
    match_data = re.search(r"Emissão:\s*(\d{2}/\d{2}/\d{4})(?:\s+(\d{2}:\d{2}:\d{2}))?", texto, re.I)
    data = match_data.group(1) if match_data and data_valida(match_data.group(1)) else ""
    hora = match_data.group(2) if match_data and match_data.group(2) else ""
    romaneio = re.search(r"Romaneio de Carga\s+([A-Z0-9]+)", texto, re.I)
    origem = re.search(r"Origem:\s*(.*?)\s+Destino:", texto, re.I)
    destino = re.search(r"Destino:\s*(.*?)\s+(?:Recebi em perfeita|Lotes Consolidados:)", texto, re.I | re.S)
    origem_texto = origem.group(1).strip() if origem else ""
    destino_texto = destino.group(1).strip() if destino else ""
    if origem_texto.endswith("(XD") and destino_texto.startswith("GRU)"):
        origem_texto = f"{origem_texto} GRU)"
        destino_texto = destino_texto[4:].strip()
    motorista = re.search(r"Motorista transportadora:\s*Nome:\s*(.*?)\s+Placa:\s*(\S+)", texto, re.I | re.S)
    recebedor = re.search(r"Colaborador Unidade Recebedora:\s*Nome:\s*(.*?)\s+Observações:", texto, re.I | re.S)
    observacoes = re.search(r"Observações:\s*(.*?)(?:Descrição de pacotes|$)", texto, re.I | re.S)
    lotes, lote_atual = [], None
    for linha in linhas:
        m = re.search(r"Lote:\s*([A-Z0-9]+)\s*-\s*Pacotes:\s*(\d+)", linha, re.I)
        if m:
            lote_atual = {"lote": m.group(1), "pacotes_declarados": int(m.group(2)), "pacotes": []}
            lotes.append(lote_atual)
        elif lote_atual:
            lote_atual["pacotes"].extend(re.findall(r"\b\d{6}-\d{8,}\b", linha))
    pacotes = [{"lote": lote["lote"], "codigo": codigo} for lote in lotes for codigo in lote["pacotes"]]
    if not pacotes:
        raise ValueError("Nenhum código de pacote foi encontrado no formato esperado.")
    totais = re.search(r"Total de Lotes:.*?Total de Pacotes:.*?(\d+)\s+(\d+)", texto, re.I | re.S)
    return {
        "romaneio": romaneio.group(1) if romaneio else "", "data": data, "hora": hora,
        "origem": origem_texto, "destino": destino_texto,
        "motorista": motorista.group(1).strip() if motorista else "", "placa": motorista.group(2).strip() if motorista else "",
        "recebedor": recebedor.group(1).strip() if recebedor else "", "observacoes": observacoes.group(1).strip() if observacoes else "",
        "total_lotes_declarado": int(totais.group(1)) if totais else len(lotes),
        "total_pacotes_declarado": int(totais.group(2)) if totais else len(pacotes),
        "lotes": lotes, "pacotes": pacotes,
    }


def linhas_csv_romaneio(registros: Sequence[Dict]) -> List[Dict]:
    linhas = []
    for registro in registros:
        for pacote in registro["pacotes"]:
            linhas.append({
                "Minuta": pacote["codigo"].partition("-")[2], "Arquivo de origem": registro["caminho"].name,
                "Romaneio": registro["romaneio"], "Data": registro["data"], "Hora": registro["hora"],
                "Origem": registro["origem"], "Destino": registro["destino"], "Motorista": registro["motorista"],
                "Placa": registro["placa"], "Recebedor": registro["recebedor"], "Observações": registro["observacoes"],
                "Total de lotes declarado": registro["total_lotes_declarado"],
                "Total de pacotes declarado": registro["total_pacotes_declarado"], "Lote": pacote["lote"],
                "Código do pacote": pacote["codigo"],
                "Pacotes declarados no lote": next((lote["pacotes_declarados"] for lote in registro["lotes"] if lote["lote"] == pacote["lote"]), ""),
            })
    return linhas


def exportar_csv_linhas(caminho: Path, linhas: Sequence[Dict]) -> None:
    if not linhas:
        raise ValueError("Não há linhas para exportar.")
    with caminho.open("w", newline="", encoding="utf-8-sig") as arquivo:
        writer = csv.DictWriter(arquivo, fieldnames=list(linhas[0].keys()))
        writer.writeheader()
        writer.writerows(linhas)


def abrir_pasta(caminho: Path) -> None:
    pasta = str(caminho)
    if sys.platform == "win32":
        import os
        os.startfile(pasta)
    elif sys.platform == "darwin":
        subprocess.Popen(["open", pasta])
    else:
        subprocess.Popen(["xdg-open", pasta])
