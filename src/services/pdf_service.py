import io
import re
from typing import Any, Dict, List, Optional
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import (
    HRFlowable,
    KeepTogether,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Group


def _create_mind_map_drawing(destination: str, days: int, trip_type: str, profile: str) -> Drawing:
    """Gera um diagrama de mapa mental vetorial limpo e profissional."""
    d = Drawing(520, 140)

    # Cores executivas
    c_center = colors.HexColor("#0f172a")
    c_branch = colors.HexColor("#1e293b")
    c_border_center = colors.HexColor("#38bdf8")
    c_border_branch = colors.HexColor("#64748b")
    c_text_title = colors.white
    c_text_sub = colors.HexColor("#94a3b8")
    c_line = colors.HexColor("#475569")

    # Nó Central (Destino)
    cx, cy, cw, ch = 195, 45, 130, 50
    d.add(Rect(cx, cy, cw, ch, rx=8, ry=8, fillColor=c_center, strokeColor=c_border_center, strokeWidth=1.5))
    d.add(String(cx + 65, cy + 30, destination[:18], fontName="Helvetica-Bold", fontSize=10, fillColor=c_text_title, textAnchor="middle"))
    d.add(String(cx + 65, cy + 14, f"{days} dias · {trip_type.capitalize()}", fontName="Helvetica", fontSize=8, fillColor=c_text_sub, textAnchor="middle"))

    # Nó 1: Superior Esquerdo (Cronograma)
    n1_x, n1_y, n1_w, n1_h = 10, 80, 140, 42
    d.add(Line(n1_x + n1_w, n1_y + 21, cx, cy + 35, strokeColor=c_line, strokeWidth=1.2))
    d.add(Rect(n1_x, n1_y, n1_w, n1_h, rx=6, ry=6, fillColor=c_branch, strokeColor=c_border_branch, strokeWidth=1))
    d.add(String(n1_x + 70, n1_y + 24, "1. Roteiro Dia a Dia", fontName="Helvetica-Bold", fontSize=8.5, fillColor=c_text_title, textAnchor="middle"))
    d.add(String(n1_x + 70, n1_y + 11, "Manhã · Tarde · Noite", fontName="Helvetica", fontSize=7.5, fillColor=c_text_sub, textAnchor="middle"))

    # Nó 2: Inferior Esquerdo (Orçamento)
    n2_x, n2_y, n2_w, n2_h = 10, 18, 140, 42
    d.add(Line(n2_x + n2_w, n2_y + 21, cx, cy + 15, strokeColor=c_line, strokeWidth=1.2))
    d.add(Rect(n2_x, n2_y, n2_w, n2_h, rx=6, ry=6, fillColor=c_branch, strokeColor=c_border_branch, strokeWidth=1))
    d.add(String(n2_x + 70, n2_y + 24, "2. Orçamento Estimado", fontName="Helvetica-Bold", fontSize=8.5, fillColor=c_text_title, textAnchor="middle"))
    d.add(String(n2_x + 70, n2_y + 11, f"Perfil: {profile.capitalize()} (BRL)", fontName="Helvetica", fontSize=7.5, fillColor=c_text_sub, textAnchor="middle"))

    # Nó 3: Superior Direito (Bagagem & Clima)
    n3_x, n3_y, n3_w, n3_h = 370, 80, 140, 42
    d.add(Line(cx + cw, cy + 35, n3_x, n3_y + 21, strokeColor=c_line, strokeWidth=1.2))
    d.add(Rect(n3_x, n3_y, n3_w, n3_h, rx=6, ry=6, fillColor=c_branch, strokeColor=c_border_branch, strokeWidth=1))
    d.add(String(n3_x + 70, n3_y + 24, "3. Bagagem Inteligente", fontName="Helvetica-Bold", fontSize=8.5, fillColor=c_text_title, textAnchor="middle"))
    d.add(String(n3_x + 70, n3_y + 11, "Adaptada à Previsão do Clima", fontName="Helvetica", fontSize=7.5, fillColor=c_text_sub, textAnchor="middle"))

    # Nó 4: Inferior Direito (Dicas & Cultura)
    n4_x, n4_y, n4_w, n4_h = 370, 18, 140, 42
    d.add(Line(cx + cw, cy + 15, n4_x, n4_y + 21, strokeColor=c_line, strokeWidth=1.2))
    d.add(Rect(n4_x, n4_y, n4_w, n4_h, rx=6, ry=6, fillColor=c_branch, strokeColor=c_border_branch, strokeWidth=1))
    d.add(String(n4_x + 70, n4_y + 24, "4. Cultura & Segurança", fontName="Helvetica-Bold", fontSize=8.5, fillColor=c_text_title, textAnchor="middle"))
    d.add(String(n4_x + 70, n4_y + 11, "Gastronomia e Dicas Locais", fontName="Helvetica", fontSize=7.5, fillColor=c_text_sub, textAnchor="middle"))

    return d


def generate_itinerary_pdf(
    markdown_text: str,
    trip_info: Optional[Dict[str, Any]] = None,
) -> bytes:
    """Gera um documento PDF diagramado profissionalmente a partir do roteiro."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        leftMargin=40,
        rightMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()

    # Estilos customizados
    title_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#0f172a"),
        spaceAfter=4,
    )

    subtitle_style = ParagraphStyle(
        "DocSubTitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor("#64748b"),
        spaceAfter=12,
    )

    h1_style = ParagraphStyle(
        "SectionH1",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=12.5,
        leading=16,
        textColor=colors.HexColor("#0284c7"),
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True,
    )

    h2_style = ParagraphStyle(
        "SectionH2",
        parent=styles["Heading3"],
        fontName="Helvetica-Bold",
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor("#1e293b"),
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True,
    )

    body_style = ParagraphStyle(
        "BodyDark",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#334155"),
        spaceAfter=4,
    )

    bullet_style = ParagraphStyle(
        "BulletDark",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=12.5,
        leftIndent=14,
        textColor=colors.HexColor("#334155"),
        spaceAfter=2,
    )

    table_header_style = ParagraphStyle(
        "TableHeader",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8.5,
        textColor=colors.white,
        alignment=1,
    )

    table_cell_style = ParagraphStyle(
        "TableCell",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8,
        textColor=colors.HexColor("#1e293b"),
    )

    story = []

    # Cabeçalho Principal
    dest_name = trip_info.get("destino", "Planejamento de Viagem") if trip_info else "Planejamento de Viagem"
    days_count = trip_info.get("dias", 5) if trip_info else 5
    trip_type = trip_info.get("tipo", "Cidade") if trip_info else "Cidade"
    profile = trip_info.get("estilo", "Moderado") if trip_info else "Moderado"
    periodo_str = trip_info.get("periodo_str", "") if trip_info else ""

    story.append(Paragraph("TripMind AI — Relatório de Roteiro de Viagem", title_style))
    sub_text = f"Destino: <b>{dest_name}</b> | Duração: <b>{days_count} dia(s)</b>"
    if periodo_str:
        sub_text += f" ({periodo_str})"
    sub_text += f" | Perfil: <b>{profile.capitalize()}</b> | Estilo: <b>{trip_type.capitalize()}</b>"
    story.append(Paragraph(sub_text, subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#cbd5e1"), spaceAfter=10))

    # Esquema / Mapa Mental Visual
    story.append(Paragraph("Esquema Estrutural da Viagem (Mapa Mental)", h2_style))
    mind_map = _create_mind_map_drawing(dest_name, days_count, trip_type, profile)
    story.append(mind_map)
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#e2e8f0"), spaceAfter=10))

    # Parse do Markdown para elementos do PDF
    lines = markdown_text.split("\n")
    in_table = False
    table_rows = []

    for line in lines:
        stripped = line.strip()

        # Detecção e parsing de tabelas Markdown
        if stripped.startswith("|") and stripped.endswith("|"):
            if "---" in stripped:
                continue
            cells = [c.strip() for c in stripped.split("|")[1:-1]]
            if not in_table:
                in_table = True
                table_rows = []
            table_rows.append(cells)
            continue
        elif in_table:
            # Finaliza e renderiza a tabela acumulada
            in_table = False
            if table_rows:
                formatted_data = []
                for row_idx, row in enumerate(table_rows):
                    row_cells = []
                    for col_idx, cell in enumerate(row):
                        st_cell = table_header_style if row_idx == 0 else table_cell_style
                        # Limpa formatação markdown simples
                        clean_cell = cell.replace("**", "").replace("*", "")
                        row_cells.append(Paragraph(clean_cell, st_cell))
                    formatted_data.append(row_cells)

                t = Table(formatted_data, colWidths=None)
                t.setStyle(TableStyle([
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f172a")),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                    ("TOPPADDING", (0, 0), (-1, -1), 4),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
                    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#f8fafc"), colors.white]),
                ]))
                story.append(Spacer(1, 4))
                story.append(t)
                story.append(Spacer(1, 6))

        if not stripped:
            continue

        # Cabeçalhos
        if stripped.startswith("## "):
            header_title = stripped[3:].strip()
            story.append(Paragraph(header_title, h1_style))
        elif stripped.startswith("### "):
            sub_title = stripped[4:].strip()
            story.append(Paragraph(sub_title, h2_style))
        elif stripped.startswith("- ") or stripped.startswith("* "):
            bullet_text = stripped[2:].strip()
            # Formata negrito
            bullet_text = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", bullet_text)
            story.append(Paragraph(f"• {bullet_text}", bullet_style))
        else:
            p_text = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", stripped)
            story.append(Paragraph(p_text, body_style))

    # Rodapé da última página
    story.append(Spacer(1, 14))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#cbd5e1"), spaceAfter=6))
    story.append(Paragraph("Gerado automaticamente por TripMind AI — Planejamento Inteligente de Viagens.", subtitle_style))

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()
