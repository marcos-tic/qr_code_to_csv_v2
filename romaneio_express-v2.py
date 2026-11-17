#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CSV Express - leitor de romaneios PDF e exportador CSV (PyQt6).
Suporta arrastar e soltar (drag & drop), processamento em lote,
pré-visualização com filtro, exportação CSV e modo linha de comando.
"""

import os
import sys
import re
import base64
import subprocess
from datetime import datetime
from pathlib import Path
from typing import List, Tuple, Optional, Dict

import pandas as pd
import pdfplumber

from PyQt6.QtCore import Qt, QThread, pyqtSignal, QByteArray, QRectF
from PyQt6.QtGui import QColor, QFont, QIcon, QPixmap, QPainter, QPen, QDragEnterEvent, QDropEvent
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFileDialog, QTableWidget, QTableWidgetItem,
    QHeaderView, QProgressBar, QMessageBox, QFrame, QLineEdit, QSplitter,
    QTabWidget, QScrollArea
)

# Logo LATAM embutido como fallback para a aba Manual
MANUAL_LOGO_B64 = (
    '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'
    'LrlvAAAAAElFTkSuQmCC'
)


def carregar_imagem_recurso(nome_arquivo: str) -> QPixmap:
    """Carrega uma imagem do código-fonte ou dos recursos empacotados."""
    diretorios = []
    pasta_embutida = getattr(sys, "_MEIPASS", None)
    if pasta_embutida:
        diretorios.append(Path(pasta_embutida))
    diretorios.extend((Path(__file__).resolve().parent, Path(sys.executable).resolve().parent))

    for diretorio in diretorios:
        arquivo = diretorio / nome_arquivo
        if arquivo.is_file():
            pixmap = QPixmap(str(arquivo))
            if not pixmap.isNull():
                return pixmap
    return QPixmap()


def obter_icone_aplicacao() -> QIcon:
    """Carrega o ícone próprio do Romaneio Express V2."""
    return QIcon(carregar_imagem_recurso("romaneio_express-v2.png"))


def obter_logo_manual() -> QIcon:
    """Carrega o logo LATAM exibido na aba Manual."""
    pixmap = carregar_imagem_recurso("icone.png")
    if pixmap.isNull():
        pixmap.loadFromData(QByteArray.fromBase64(MANUAL_LOGO_B64.encode("ascii")))
    return QIcon(pixmap)


def limpar_texto(texto: str) -> str:
    """Remove ruídos e normaliza espaços no texto extraído."""
    texto_limpo = texto.replace("|", " ")
    return re.sub(r'\s+', ' ', texto_limpo)


def extrair_dados_pdf(caminho_pdf: Path) -> Dict:
    """Extrai os dados gerais do romaneio, lotes e códigos de pacote."""
    texto_completo = ""
    with pdfplumber.open(caminho_pdf) as pdf:
        for pagina in pdf.pages:
            texto_completo += (pagina.extract_text() or "") + "\n"

    linhas = [re.sub(r"\s+", " ", linha).strip() for linha in texto_completo.splitlines()]
    texto = "\n".join(linhas)
    match_data = re.search(r"Emissão:\s*(\d{2}/\d{2}/\d{4})(?:\s+(\d{2}:\d{2}:\d{2}))?", texto, re.I)
    data = match_data.group(1) if match_data else ""
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
        elif lote_atual and re.match(r"\d{6}-\d{8,}", linha):
            lote_atual["pacotes"].extend(re.findall(r"\b\d{6}-\d{8,}\b", linha))
    pacotes = [{"lote": l["lote"], "codigo": c} for l in lotes for c in l["pacotes"]]
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


class ProcessadorThread(QThread):
    """Thread em segundo plano para extração sem travar a interface."""
    progresso = pyqtSignal(int, str)
    finalizado = pyqtSignal(list, list)

    def __init__(self, arquivos: List[Path]):
        super().__init__()
        self.arquivos = arquivos

    def run(self):
        resultados = []
        falhas = []
        total = len(self.arquivos)
        for i, arq in enumerate(self.arquivos):
            self.progresso.emit(int((i / total) * 100), f"Processando: {arq.name}...")
            try:
                dados = extrair_dados_pdf(arq)
                resultados.append({
                    "caminho": arq,
                    "nome": arq.name,
                    **dados,
                    "minutas": [p["codigo"] for p in dados["pacotes"]],
                    "total": len(dados["pacotes"])
                })
            except Exception as e:
                falhas.append({"nome": arq.name, "erro": str(e)})

        self.progresso.emit(100, "Concluído!")
        self.finalizado.emit(resultados, falhas)


class DropArea(QFrame):
    """Área para adicionar PDFs, compactada após a primeira carga."""
    arquivos_soltos = pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.tema_escuro = False
        self.compacta = False
        self.setAcceptDrops(True)
        self.setObjectName("dropArea")

        self.layout_conteudo = QVBoxLayout(self)
        self.layout_conteudo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout_conteudo.setSpacing(8)

        self.icone = QLabel("📥", self)
        self.icone.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.icone.setStyleSheet("font-size: 38px; background: transparent;")

        self.label_titulo = QLabel("Arraste e solte seus arquivos PDF aqui", self)
        self.label_titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label_sub = QLabel("ou clique no botão abaixo para selecionar do computador", self)
        self.label_sub.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_conteudo.addWidget(self.icone)
        self.layout_conteudo.addWidget(self.label_titulo)
        self.layout_conteudo.addWidget(self.label_sub)
        self.definir_compacta(False)

    def definir_compacta(self, compacta: bool):
        self.compacta = compacta
        self.icone.setVisible(not compacta)
        if compacta:
            self.label_titulo.setText("Arraste PDFs aqui para adicionar mais arquivos")
            self.label_sub.setText("ou use Selecionar PDF")
            self.layout_conteudo.setContentsMargins(12, 6, 12, 6)
            self.layout_conteudo.setSpacing(2)
            self.setMinimumHeight(66)
            self.setMaximumHeight(82)
        else:
            self.label_titulo.setText("Arraste e solte seus arquivos PDF aqui")
            self.label_sub.setText("ou clique no botão abaixo para selecionar do computador")
            self.layout_conteudo.setContentsMargins(20, 14, 20, 14)
            self.layout_conteudo.setSpacing(6)
            self.setMinimumHeight(130)
            self.setMaximumHeight(175)
        self.aplicar_tema(self.tema_escuro)

    def aplicar_tema(self, escuro: bool):
        self.tema_escuro = escuro
        fundo, borda, texto, secundario = (
            ("#1e293b", "#475569", "#f8fafc", "#94a3b8")
            if escuro else ("#ffffff", "#94a3b8", "#172033", "#526176")
        )
        padding = "8px" if self.compacta else "20px"
        self.setStyleSheet(
            f"#dropArea {{ background-color: {fundo}; border: 2px dashed {borda}; "
            f"border-radius: 14px; padding: {padding}; }}"
            f"#dropArea:hover {{ border-color: #2A0087; background-color: {fundo}; }}"
        )
        tamanho = 14 if self.compacta else 15
        self.label_titulo.setStyleSheet(f"font-size: {tamanho}px; font-weight: 600; color: {texto}; background: transparent;")
        self.label_sub.setStyleSheet(f"font-size: 12px; color: {secundario}; background: transparent;")

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if any(u.toLocalFile().lower().endswith(".pdf") for u in urls):
                event.acceptProposedAction()
                padding = "8px" if self.compacta else "20px"
                self.setStyleSheet(
                    f"#dropArea {{ background-color: #332080; border: 2px dashed #EE1750; "
                    f"border-radius: 14px; padding: {padding}; }}"
                )

    def dragLeaveEvent(self, event):
        self.aplicar_tema(self.tema_escuro)

    def dropEvent(self, event: QDropEvent):
        self.dragLeaveEvent(None)
        arquivos = []
        for url in event.mimeData().urls():
            caminho = Path(url.toLocalFile())
            if caminho.is_file() and caminho.suffix.lower() == ".pdf":
                arquivos.append(caminho)
        if arquivos:
            self.arquivos_soltos.emit(arquivos)


class ThemeSwitch(QWidget):
    """Interruptor visual compacto para alternar entre tema claro e escuro."""
    temaAlterado = pyqtSignal(bool)

    def __init__(self, escuro: bool = False, parent=None):
        super().__init__(parent)
        self.escuro = escuro
        self.setFixedSize(90, 44)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setAccessibleName("Alternar tema claro e escuro")
        self.atualizar_descricao()

    def atualizar_descricao(self):
        estado = "escuro" if self.escuro else "claro"
        self.setToolTip(f"Tema {estado}. Clique para alternar.")
        self.setAccessibleDescription(f"Tema atual: {estado}")

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.escuro = not self.escuro
            self.atualizar_descricao()
            self.update()
            self.temaAlterado.emit(self.escuro)
            event.accept()
            return
        super().mousePressEvent(event)

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key.Key_Space, Qt.Key.Key_Return, Qt.Key.Key_Enter):
            self.escuro = not self.escuro
            self.atualizar_descricao()
            self.update()
            self.temaAlterado.emit(self.escuro)
            event.accept()
            return
        super().keyPressEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        largura, altura = self.width(), self.height()
        cor_trilho = QColor("#2A0087" if self.escuro else "#b8b8b8")
        painter.setPen(QPen(QColor("#EE1750") if self.underMouse() else cor_trilho, 2))
        painter.setBrush(cor_trilho)
        painter.drawRoundedRect(QRectF(1, 1, largura - 2, altura - 2), altura / 2, altura / 2)

        diametro, margem = altura - 10, 5
        pos_knob = largura - diametro - margem if self.escuro else margem
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor("#ffffff"))
        painter.drawEllipse(QRectF(pos_knob, margem, diametro, diametro))

        centro_x = 22 if self.escuro else largura - 22
        centro_y = altura // 2
        painter.setPen(QPen(QColor("#ffffff"), 2, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        if self.escuro:
            painter.setBrush(QColor("#ffffff"))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(QRectF(centro_x - 7, centro_y - 7, 14, 14))
            painter.setBrush(cor_trilho)
            painter.drawEllipse(QRectF(centro_x - 1, centro_y - 10, 14, 14))
        else:
            painter.setBrush(QColor("#ffffff"))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(QRectF(centro_x - 4, centro_y - 4, 8, 8))
            painter.setPen(QPen(QColor("#ffffff"), 2, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
            for dx, dy in ((0, -1), (1, 0), (0, 1), (-1, 0), (1, -1), (1, 1), (-1, 1), (-1, -1)):
                inicio_x = centro_x + dx * 8
                inicio_y = centro_y + dy * 8
                fim_x = centro_x + dx * 12
                fim_y = centro_y + dy * 12
                painter.drawLine(inicio_x, inicio_y, fim_x, fim_y)
        painter.end()


class JanelaPrincipal(QMainWindow):
    """Janela principal da aplicação com tema Dark Moderno."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Romaneio Express V2")
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)
        self.setWindowIcon(obter_icone_aplicacao())
        self.resize(950, 800)
        self.setMinimumSize(800, 560)
        self.setFixedWidth(950)

        self.dados_carregados = []
        self.ultima_falhas = []
        self.ultimo_csv_gerado = None
        self.tema_escuro = False

        self.aplicar_estilos()
        self.construir_interface()

    def aplicar_estilos(self):
        """Aplica folha de estilos CSS moderna."""
        if self.tema_escuro:
            fundo, painel, texto, secundario = "#0f172a", "#1e293b", "#f8fafc", "#94a3b8"
            borda, destaque = "#334155", "#EE1750"
        else:
            fundo, painel, texto, secundario = "#f1f5f9", "#ffffff", "#172033", "#526176"
            borda, destaque = "#cbd5e1", "#2A0087"
        cinza_manual = "#334155" if self.tema_escuro else "#e5e7eb"
        self.setStyleSheet(f"""
            QMainWindow, QWidget {{
                background-color: {fundo};
                color: {texto};
                font-family: 'Segoe UI', 'Ubuntu', 'Inter', sans-serif;
            }}
            QFrame#cardStats {{
                background-color: {painel};
                border-radius: 12px;
                border: 1px solid {borda};
                padding: 12px;
            }}
            QFrame#manualTexto {{
                background-color: {cinza_manual};
                border-radius: 14px;
                border: 1px solid {borda};
            }}
            QLabel#manualTextoLabel {{ background-color: transparent; }}
            QLabel#metricNum {{
                font-size: 26px;
                font-weight: 700;
                color: {destaque};
            }}
            QLabel#metricLabel {{
                font-size: 12px;
                color: {secundario};
                font-weight: 500;
            }}
            QPushButton {{
                background-color: {painel};
                color: {texto};
                border: 1px solid {borda};
                border-radius: 8px;
                padding: 9px 18px;
                font-size: 13px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background-color: {borda};
            }}
            QPushButton#btnPrimary {{
                background-color: #2A0087;
                color: #ffffff;
                border: none;
            }}
            QPushButton#btnPrimary:hover {{
                background-color: #200066;
            }}
            QPushButton#btnSuccess {{
                background-color: #EE1750;
                color: #ffffff;
                border: none;
            }}
            QPushButton#btnSuccess:hover {{
                background-color: #C51243;
            }}
            QPushButton:disabled {{
                background-color: {fundo};
                color: {secundario};
                border-color: {borda};
            }}
            QLineEdit {{
                background-color: {painel};
                border: 1px solid {borda};
                border-radius: 8px;
                padding: 8px 12px;
                color: {texto};
                font-size: 13px;
            }}
            QLineEdit:focus {{
                border-color: {destaque};
            }}
            QTableWidget {{
                background-color: {painel};
                border: 1px solid {borda};
                border-radius: 10px;
                gridline-color: {borda};
                color: {texto};
                font-size: 13px;
            }}
            QTableWidget::item {{
                padding: 8px;
            }}
            QTableWidget::item:selected {{
                background-color: #2A0087;
                color: white;
            }}
            QLabel#emptyState {{
                background-color: {painel};
                border: 1px dashed {borda};
                border-radius: 14px;
                padding: 28px;
                color: {secundario};
                font-size: 15px;
            }}
            QHeaderView::section {{
                background-color: {fundo};
                color: {secundario};
                padding: 8px;
                font-weight: 600;
                font-size: 12px;
                border: none;
                border-bottom: 2px solid {borda};
            }}
            QProgressBar {{
                background-color: {painel};
                border: 1px solid {borda};
                border-radius: 6px;
                height: 12px;
                text-align: center;
                color: {texto};
                font-size: 10px;
            }}
            QProgressBar::chunk {{
                background-color: {destaque};
                border-radius: 5px;
            }}
            QTabWidget::pane {{
                border: 1px solid {borda};
                border-radius: 10px;
                background-color: {fundo};
                top: -1px;
            }}
            QTabBar::tab {{
                background-color: {painel};
                color: {secundario};
                padding: 10px 20px;
                margin-right: 6px;
                border: 1px solid {borda};
                border-top-left-radius: 9px;
                border-top-right-radius: 9px;
                min-width: 78px;
                font-size: 13px;
                font-weight: 600;
            }}
            QTabBar::tab:hover:!selected {{
                color: #EE1750;
                background-color: {fundo};
            }}
            QTabBar::tab:selected {{
                background-color: #2A0087;
                color: #ffffff;
                border: 1px solid #2A0087;
                border-bottom: 3px solid #EE1750;
            }}
        """)
        if hasattr(self, "drop_area"):
            self.drop_area.aplicar_tema(self.tema_escuro)
        self.atualizar_estilos_textuais()

    def alternar_tema(self, escuro: bool):
        self.tema_escuro = bool(escuro)
        self.aplicar_estilos()

    def atualizar_estilos_textuais(self):
        texto = "#f8fafc" if self.tema_escuro else "#172033"
        secundario = "#cbd5e1" if self.tema_escuro else "#526176"
        destaque = "#EE1750" if self.tema_escuro else "#2A0087"
        for widget in getattr(self, "textos_tema", []):
            widget.setStyleSheet(f"font-size: 20px; font-weight: 700; color: {texto};")
        for widget in getattr(self, "textos_secundarios_tema", []):
            widget.setStyleSheet(f"color: {secundario};")
        for widget in getattr(self, "titulos_tema", []):
            widget.setStyleSheet(f"font-size: 24px; font-weight: 700; color: {texto};")
        for widget in getattr(self, "destaques_tema", []):
            widget.setStyleSheet(f"font-size: 16px; font-weight: 700; color: {destaque};")
        if hasattr(self, "texto_manual"):
            self.texto_manual.setStyleSheet(f"font-size: 14px; color: {texto}; background-color: transparent;")

    def construir_interface(self):
        self.abas = QTabWidget()
        self.setCentralWidget(self.abas)

        container = QWidget()
        self.abas.addTab(container, obter_icone_aplicacao(), "Extrator")
        main_layout = QVBoxLayout(container)
        main_layout.setContentsMargins(24, 20, 24, 20)
        main_layout.setSpacing(16)

        # 1. Header
        header_layout = QHBoxLayout()
        header_text = QVBoxLayout()
        titulo = QLabel("Romaneio Express V2")
        titulo.setStyleSheet("font-size: 20px; font-weight: 700; color: #f8fafc;")
        self.textos_tema = [titulo]
        subtitulo = QLabel("Extração de romaneios, lotes e pacotes de arquivos PDF para CSV")
        subtitulo.setStyleSheet("font-size: 13px; color: #94a3b8;")
        self.textos_secundarios_tema = [subtitulo]
        header_text.addWidget(titulo)
        header_text.addWidget(subtitulo)
        header_layout.addLayout(header_text)
        header_layout.addStretch()

        self.btn_selecionar = QPushButton("📂 Selecionar PDF")
        self.btn_selecionar.setObjectName("btnPrimary")
        self.btn_selecionar.setToolTip("Escolha romaneios PDF para extrair dados, lotes e pacotes.")
        self.btn_selecionar.clicked.connect(self.abrir_seletor_arquivos)
        header_layout.addWidget(self.btn_selecionar)

        self.seletor_tema = ThemeSwitch(self.tema_escuro)
        self.seletor_tema.temaAlterado.connect(self.alternar_tema)
        header_layout.addWidget(self.seletor_tema)

        main_layout.addLayout(header_layout)

        # 2. Área de Drag and Drop
        self.drop_area = DropArea(self)
        self.drop_area.arquivos_soltos.connect(self.processar_arquivos)
        main_layout.addWidget(self.drop_area)

        # 3. Cards de Métricas
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(14)

        self.card_arquivos, self.val_arquivos = self.criar_card_stat("0", "ARQUIVOS PDF")
        self.card_minutas, self.val_minutas = self.criar_card_stat("0", "PACOTES EXTRAÍDOS")
        self.card_data, self.val_data = self.criar_card_stat("-", "DATA DO ROMANEIO")

        stats_layout.addWidget(self.card_arquivos)
        stats_layout.addWidget(self.card_minutas)
        stats_layout.addWidget(self.card_data)
        main_layout.addLayout(stats_layout)

        # 4. Barra de Filtro e Busca
        filtro_layout = QHBoxLayout()
        self.campo_busca = QLineEdit()
        self.campo_busca.setPlaceholderText("🔍 Filtrar pacote, lote ou romaneio...")
        self.campo_busca.textChanged.connect(self.filtrar_tabela)
        filtro_layout.addWidget(self.campo_busca)
        main_layout.addLayout(filtro_layout)

        # 5. Estado inicial e tabela de pré-visualização
        self.estado_vazio = QLabel(
            "📄\nAdicione PDFs para começar\nArraste arquivos para a área acima ou use Selecionar PDF."
        )
        self.estado_vazio.setObjectName("emptyState")
        self.estado_vazio.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.estado_vazio.setWordWrap(True)
        self.estado_vazio.setMinimumHeight(180)
        self.textos_secundarios_tema.append(self.estado_vazio)
        main_layout.addWidget(self.estado_vazio)

        self.tabela = QTableWidget()
        self.tabela.setColumnCount(7)
        self.tabela.setHorizontalHeaderLabels(["#", "Minuta", "Código do Pacote", "Lote", "Romaneio", "Arquivo de Origem", "Data"])
        self.tabela.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.tabela.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tabela.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.tabela.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        for coluna in range(1, 7):
            self.tabela.horizontalHeader().setSectionResizeMode(coluna, QHeaderView.ResizeMode.Stretch)
        self.tabela.verticalHeader().setVisible(False)
        self.tabela.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        self.tabela.verticalHeader().setDefaultSectionSize(38)
        self.tabela.verticalHeader().setMinimumSectionSize(38)
        self.tabela.verticalHeader().setMaximumSectionSize(38)
        self.tabela.setToolTip("Clique em uma linha para copiar a minuta.")
        self.tabela.cellClicked.connect(self.copiar_minuta_da_linha)
        self.tabela.hide()
        main_layout.addWidget(self.tabela)

        # 6. Barra de Progresso e Status
        progress_layout = QHBoxLayout()
        self.lbl_status = QLabel("Pronto para processar.")
        self.lbl_status.setStyleSheet("color: #94a3b8; font-size: 12px;")
        self.textos_secundarios_tema.append(self.lbl_status)
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)
        progress_layout.addWidget(self.lbl_status)
        progress_layout.addStretch()
        progress_layout.addWidget(self.progress_bar)
        main_layout.addLayout(progress_layout)

        # 7. Barra Inferior de Ações
        botoes_layout = QHBoxLayout()
        botoes_layout.setSpacing(12)

        self.btn_limpar = QPushButton("🗑️ Limpar Lista")
        self.btn_limpar.setToolTip("Remove os PDFs e resultados da sessão atual.")
        self.btn_limpar.clicked.connect(self.limpar_tudo)

        self.btn_abrir_pasta = QPushButton("📁 Abrir Pasta Destino")
        self.btn_abrir_pasta.setToolTip("Abre a pasta onde o último arquivo CSV foi salvo.")
        self.btn_abrir_pasta.setEnabled(False)
        self.btn_abrir_pasta.clicked.connect(self.abrir_pasta_destino)

        self.btn_exportar = QPushButton("💾 Exportar para CSV")
        self.btn_exportar.setObjectName("btnSuccess")
        self.btn_exportar.setToolTip("Salva dados do romaneio, lotes e pacotes em CSV compatível com Excel.")
        self.btn_exportar.setEnabled(False)
        self.btn_exportar.clicked.connect(self.exportar_csv)

        botoes_layout.addWidget(self.btn_limpar)
        botoes_layout.addStretch()
        botoes_layout.addWidget(self.btn_abrir_pasta)
        botoes_layout.addWidget(self.btn_exportar)

        main_layout.addLayout(botoes_layout)
        self.criar_aba_manual()
        self.aplicar_estilos()

    def criar_aba_manual(self):
        pagina = QWidget()
        layout_pagina = QVBoxLayout(pagina)
        layout_pagina.setContentsMargins(24, 20, 24, 20)

        rolagem = QScrollArea()
        rolagem.setWidgetResizable(True)
        rolagem.setFrameShape(QFrame.Shape.NoFrame)
        conteudo = QWidget()
        layout = QVBoxLayout(conteudo)
        layout.setSpacing(18)

        imagem = QLabel()
        imagem.setAlignment(Qt.AlignmentFlag.AlignCenter)
        imagem.setPixmap(obter_logo_manual().pixmap(104, 104))
        imagem.setStyleSheet("background-color: transparent;")
        layout.addWidget(imagem, 0, Qt.AlignmentFlag.AlignHCenter)

        bloco_texto = QFrame()
        bloco_texto.setObjectName("manualTexto")
        texto_layout = QVBoxLayout(bloco_texto)
        texto_layout.setContentsMargins(28, 24, 28, 24)

        secoes = [
            ("1. Adicionar PDF's", "Na aba Extrair, clique em Selecionar PDF ou arraste PDFs para a área indicada. É possível selecionar mais de um arquivo."),
            ("2. Conferir a extração", "Aguarde o processamento. A tabela mostra cada minuta encontrada, o nome do PDF de origem e a data do romaneio. Use o campo de busca para filtrar os resultados."),
            ("3. Exportar para CSV", "Clique em Exportar para CSV, escolha nome e local para o arquivo."),
            ("4. Depois de exportar", "Use Abrir Pasta Destino para localizar o arquivo. Clique em Limpar Lista para remover os resultados e processar outros PDFs."),
            ("Observação", "O aplicativo extrai informações em formato de texto já existente no PDF. Romaneios digitalizados como imagem não podem ser processados para extração."),
        ]
        blocos_texto = [
            "<span style='font-size:22px'><b>Manual de uso</b></span>",
            "Use o Romaneio Express para conferir os dados do romaneio e os pacotes associados a cada lote.",
        ]
        blocos_texto.extend(f"<b>{cabecalho}</b><br>{texto_secao}" for cabecalho, texto_secao in secoes)
        self.texto_manual = QLabel("<br><br>".join(blocos_texto))
        self.texto_manual.setObjectName("manualTextoLabel")
        self.texto_manual.setTextFormat(Qt.TextFormat.RichText)
        self.texto_manual.setWordWrap(True)
        texto_layout.addWidget(self.texto_manual)
        layout.addWidget(bloco_texto)
        layout.addStretch()

        self.titulos_tema = []
        self.destaques_tema = []
        self.textos_secundarios_tema.append(self.texto_manual)
        rolagem.setWidget(conteudo)
        layout_pagina.addWidget(rolagem)
        self.abas.addTab(pagina, "❔ Manual")

    def criar_card_stat(self, valor_inicial: str, rotulo: str):
        card = QFrame()
        card.setObjectName("cardStats")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(16, 10, 16, 10)
        layout.setSpacing(2)

        val_label = QLabel(valor_inicial)
        val_label.setObjectName("metricNum")
        rotulo_label = QLabel(rotulo)
        rotulo_label.setObjectName("metricLabel")

        layout.addWidget(val_label)
        layout.addWidget(rotulo_label)
        return card, val_label

    def abrir_seletor_arquivos(self):
        caminhos, _ = QFileDialog.getOpenFileNames(
            self,
            "Selecione arquivos PDF de Romaneio",
            str(Path.home()),
            "Arquivos PDF (*.pdf *.PDF)"
        )
        if caminhos:
            self.processar_arquivos([Path(c) for c in caminhos])

    def processar_arquivos(self, arquivos: List[Path]):
        if not arquivos:
            return

        self.ultima_falhas = []
        self.btn_selecionar.setEnabled(False)
        self.btn_exportar.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.lbl_status.setText("Iniciando leitura dos PDFs...")
        if not self.dados_carregados:
            self.estado_vazio.setText("⏳\nProcessando PDFs...\nA extração aparecerá aqui.")
            self.estado_vazio.show()
            self.tabela.hide()

        self.thread = ProcessadorThread(arquivos)
        self.thread.progresso.connect(self.atualizar_progresso)
        self.thread.finalizado.connect(self.finalizar_processamento)
        self.thread.start()

    def atualizar_progresso(self, valor: int, mensagem: str):
        self.progress_bar.setValue(valor)
        self.lbl_status.setText(mensagem)

    def exibir_resumo_falhas(self, falhas: list, total_arquivos: int):
        linhas = [f"Não foi possível processar {len(falhas)} de {total_arquivos} PDFs:"]
        for falha in falhas[:8]:
            erro = " ".join(falha["erro"].split())
            if len(erro) > 160:
                erro = erro[:157] + "..."
            linhas.append(f"• {falha['nome']}: {erro}")
        if len(falhas) > 8:
            linhas.append(f"• E mais {len(falhas) - 8} arquivo(s).")
        QMessageBox.warning(self, "Resumo do processamento", "\n".join(linhas))

    def finalizar_processamento(self, resultados: list, falhas: list):
        self.btn_selecionar.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.dados_carregados.extend(resultados)
        self.ultima_falhas = falhas
        self.atualizar_visualizacao()
        if falhas:
            self.exibir_resumo_falhas(falhas, len(resultados) + len(falhas))

    def copiar_minuta_da_linha(self, linha: int, coluna: int):
        item_codigo = self.tabela.item(linha, 1)
        if item_codigo:
            codigo = item_codigo.text()
            QApplication.clipboard().setText(codigo)
            self.lbl_status.setText(f"Pacote {codigo} copiado.")

    def atualizar_visualizacao(self):
        total_arquivos = len(self.dados_carregados)
        total_minutas = sum(len(d["pacotes"]) for d in self.dados_carregados)
        datas = set(d["data"] for d in self.dados_carregados if d["data"])
        datas_formatadas = [
            f"{data[0:2]}/{data[2:4]}/{data[4:8]}" if re.fullmatch(r"\d{8}", data) else data
            for data in sorted(datas)
        ]
        data_str = ", ".join(datas_formatadas) if datas_formatadas else "-"

        self.val_arquivos.setText(str(total_arquivos))
        self.val_minutas.setText(f"{total_minutas:,}".replace(",", "."))
        self.val_data.setText(data_str)

        todas_minutas = []
        for d in self.dados_carregados:
            for pacote in d["pacotes"]:
                todas_minutas.append((pacote["codigo"].partition("-")[2], pacote["codigo"], pacote["lote"], d["romaneio"], d["nome"], d["data"]))

        self.tabela.setRowCount(len(todas_minutas))
        for row, (minuta, codigo, lote, romaneio, arq_nome, data_doc) in enumerate(todas_minutas):
            self.tabela.setItem(row, 0, QTableWidgetItem(str(row + 1)))
            self.tabela.setItem(row, 1, QTableWidgetItem(minuta))
            self.tabela.setItem(row, 2, QTableWidgetItem(codigo))
            self.tabela.setItem(row, 3, QTableWidgetItem(lote))
            self.tabela.setItem(row, 4, QTableWidgetItem(romaneio))
            self.tabela.setItem(row, 5, QTableWidgetItem(arq_nome))
            self.tabela.setItem(row, 6, QTableWidgetItem(data_doc))

        tem_dados = total_minutas > 0
        self.drop_area.definir_compacta(total_arquivos > 0)
        if tem_dados:
            self.estado_vazio.hide()
            self.tabela.show()
        else:
            self.tabela.hide()
            if total_arquivos:
                self.estado_vazio.setText("📭\nNenhum pacote encontrado\nOs PDFs não continham códigos de pacote no formato esperado.")
            elif self.ultima_falhas:
                self.estado_vazio.setText("⚠️\nNão foi possível ler os PDFs\nConsulte o resumo do processamento para ver os detalhes.")
            else:
                self.estado_vazio.setText("📄\nAdicione PDFs para começar\nArraste arquivos para a área acima ou use Selecionar PDF.")
            self.estado_vazio.show()
        self.btn_exportar.setEnabled(tem_dados)
        if total_minutas:
            self.lbl_status.setText(f"✓ Pronto! {total_minutas} pacotes carregados.")
        elif total_arquivos:
            self.lbl_status.setText("Leitura concluída. Nenhum pacote foi encontrado.")

    def filtrar_tabela(self, texto: str):
        filtro = texto.strip().lower()
        for row in range(self.tabela.rowCount()):
            corresponde = any(filtro in self.tabela.item(row, col).text().lower() for col in range(1, 7))
            self.tabela.setRowHidden(row, not corresponde)

    def limpar_tudo(self):
        self.dados_carregados = []
        self.ultima_falhas = []
        self.val_arquivos.setText("0")
        self.val_minutas.setText("0")
        self.val_data.setText("-")
        self.tabela.setRowCount(0)
        self.tabela.hide()
        self.estado_vazio.setText("📄\nAdicione PDFs para começar\nArraste arquivos para a área acima ou use Selecionar PDF.")
        self.estado_vazio.show()
        self.drop_area.definir_compacta(False)
        self.btn_exportar.setEnabled(False)
        self.btn_abrir_pasta.setEnabled(False)
        self.campo_busca.clear()
        self.lbl_status.setText("Lista limpa. Pronto para processar.")

    def exportar_csv(self):
        todas_minutas = []
        for d in self.dados_carregados:
            todas_minutas.extend({
                "Minuta": p["codigo"].partition("-")[2],
                "Romaneio": d["romaneio"], "Data": d["data"], "Hora": d["hora"],
                "Origem": d["origem"], "Destino": d["destino"], "Motorista": d["motorista"],
                "Placa": d["placa"], "Recebedor": d["recebedor"], "Observações": d["observacoes"],
                "Total de lotes declarado": d["total_lotes_declarado"],
                "Total de pacotes declarado": d["total_pacotes_declarado"],
                "Lote": p["lote"], "Código do pacote": p["codigo"],
                "Pacotes declarados no lote": next((l["pacotes_declarados"] for l in d["lotes"] if l["lote"] == p["lote"]), ""),
            } for p in d["pacotes"])

        if not todas_minutas:
            QMessageBox.information(self, "Aviso", "Nenhuma minuta para exportar.")
            return

        datas = [d["data"] for d in self.dados_carregados if d["data"]]
        data_sugerida = datas[0] if datas else datetime.now().strftime("%d%m%Y")
        nome_sugerido = f"romaneios_extraidos_{data_sugerida}_qtd-{len(todas_minutas)}.csv"

        pasta_padrao = str(self.dados_carregados[0]["caminho"].parent)
        caminho_inicial = os.path.join(pasta_padrao, nome_sugerido)

        caminho_salvar, _ = QFileDialog.getSaveFileName(
            self,
            "Salvar Planilha de Minutas",
            caminho_inicial,
            "Planilha CSV (*.csv)"
        )

        if not caminho_salvar:
            return

        if not caminho_salvar.lower().endswith(".csv"):
            caminho_salvar += ".csv"

        df = pd.DataFrame(todas_minutas)
        df.to_csv(caminho_salvar, index=False, encoding="utf-8-sig")

        self.ultimo_csv_gerado = Path(caminho_salvar)
        self.btn_abrir_pasta.setEnabled(True)

        QMessageBox.information(
            self,
            "Exportação Concluída",
            f"✓ Sucesso total!\n\n"
            f"• Pacotes exportados: {len(todas_minutas)}\n"
            f"• Arquivo salvo em:\n{caminho_salvar}"
        )

    def abrir_pasta_destino(self):
        if self.ultimo_csv_gerado and self.ultimo_csv_gerado.exists():
            pasta = str(self.ultimo_csv_gerado.parent)
            try:
                if sys.platform == "win32":
                    os.startfile(pasta)
                elif sys.platform == "darwin":
                    subprocess.Popen(["open", pasta])
                else:
                    subprocess.Popen(["xdg-open", pasta])
            except Exception as e:
                QMessageBox.warning(self, "Erro", f"Não foi possível abrir o gerenciador: {e}")


def executar_cli(arquivos: List[Path]):
    """Modo linha de comando rápido."""
    print("Modo Linha de Comando:")
    for arq in arquivos:
        if not arq.exists():
            print(f"Arquivo não encontrado: {arq}")
            continue
        dados = extrair_dados_pdf(arq)
        qtd = len(dados["pacotes"])
        nome_csv = arq.parent / f"romaneios_extraidos_{dados['data'] or 'sem_data'}_qtd-{qtd}.csv"
        linhas = [{"Minuta": p["codigo"].partition("-")[2],
                   "Romaneio": dados["romaneio"], "Data": dados["data"], "Hora": dados["hora"],
                   "Origem": dados["origem"], "Destino": dados["destino"], "Motorista": dados["motorista"],
                   "Placa": dados["placa"], "Recebedor": dados["recebedor"], "Observações": dados["observacoes"],
                   "Total de lotes declarado": dados["total_lotes_declarado"], "Total de pacotes declarado": dados["total_pacotes_declarado"],
                   "Lote": p["lote"], "Código do pacote": p["codigo"]} for p in dados["pacotes"]]
        df = pd.DataFrame(linhas)
        df.to_csv(nome_csv, index=False, encoding='utf-8-sig')
        print(f"✓ {arq.name}: {qtd} pacotes salvos em {nome_csv}")


def main():
    if len(sys.argv) > 1 and not sys.argv[1].startswith("-"):
        arquivos = [Path(a) for a in sys.argv[1:] if Path(a).is_file()]
        if arquivos:
            executar_cli(arquivos)
            return

    app = QApplication(sys.argv)
    app.setApplicationName("Romaneio Express V2")
    app.setApplicationVersion("2.0")
    app.setWindowIcon(obter_icone_aplicacao())
    janela = JanelaPrincipal()
    janela.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
