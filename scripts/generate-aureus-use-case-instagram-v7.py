from __future__ import annotations

import importlib.util
import shutil
import sys
import zipfile
from pathlib import Path
from typing import Iterable

import fitz
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
EXPORT_DIR = ROOT / "exports"
OUT_ROOT = EXPORT_DIR / "instagram_carousel_v7"

PAGE_W = 1080
PAGE_H = 1350
MARGIN = 62

BG = colors.HexColor("#07131d")
BG_2 = colors.HexColor("#0a1a28")
PANEL = colors.HexColor("#0e2030")
PANEL_2 = colors.HexColor("#11283a")
INK = colors.HexColor("#111827")
MUTED = colors.HexColor("#5e6b7a")
LINE = colors.HexColor("#d9e2ec")
LINE_DARK = colors.HexColor("#284157")
WHITE = colors.HexColor("#f8fafc")
SOFT = colors.HexColor("#c8d4e1")
GOLD = colors.HexColor("#e5b84d")
TEAL = colors.HexColor("#33d0c4")
BLUE = colors.HexColor("#6b9dff")
GREEN = colors.HexColor("#51d38a")
PURPLE = colors.HexColor("#9a7cff")
RED = colors.HexColor("#ff7b64")


def register_fonts() -> tuple[str, str]:
    regular = Path("C:/Windows/Fonts/arial.ttf")
    bold = Path("C:/Windows/Fonts/arialbd.ttf")
    if regular.exists() and bold.exists():
        pdfmetrics.registerFont(TTFont("AureusIG", str(regular)))
        pdfmetrics.registerFont(TTFont("AureusIG-Bold", str(bold)))
        return "AureusIG", "AureusIG-Bold"
    return "Helvetica", "Helvetica-Bold"


FONT, FONT_BOLD = register_fonts()


def load_source_module():
    source = ROOT / "scripts" / "generate-aureus-use-case-pdfs-v6-pro.py"
    spec = importlib.util.spec_from_file_location("aureus_use_case_v7_source", source)
    if not spec or not spec.loader:
        raise RuntimeError(f"Could not load source generator: {source}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def string_width(text: str, size: float, font: str = FONT) -> float:
    return pdfmetrics.stringWidth(text, font, size)


def draw_text(c: canvas.Canvas, text: str, x: float, y: float, size: float, color=INK, font: str = FONT) -> None:
    c.setFillColor(color)
    c.setFont(font, size)
    c.drawString(x, y, text)


def wrap_lines(text: str, max_width: float, size: float, font: str = FONT) -> list[str]:
    lines: list[str] = []
    for para in text.split("\n"):
        words = para.split()
        if not words:
            lines.append("")
            continue
        current = ""
        for word in words:
            candidate = word if not current else f"{current} {word}"
            if string_width(candidate, size, font) <= max_width:
                current = candidate
                continue
            if current:
                lines.append(current)
            current = word
        if current:
            lines.append(current)
    return lines


def draw_wrapped(
    c: canvas.Canvas,
    text: str,
    x: float,
    y: float,
    max_width: float,
    size: float,
    color=INK,
    font: str = FONT,
    leading: float | None = None,
    max_lines: int | None = None,
) -> float:
    leading = leading or size * 1.24
    lines = wrap_lines(text, max_width, size, font)
    if max_lines is not None and len(lines) > max_lines:
        lines = lines[:max_lines]
        last = lines[-1]
        while last and string_width(last + "...", size, font) > max_width:
            last = last.rsplit(" ", 1)[0] if " " in last else last[:-1]
        lines[-1] = (last or lines[-1][:8]) + "..."
    c.setFillColor(color)
    c.setFont(font, size)
    for index, line in enumerate(lines):
        c.drawString(x, y - index * leading, line)
    return y - len(lines) * leading


def rounded(c: canvas.Canvas, x: float, y: float, w: float, h: float, fill, stroke=None, radius=24, width=1.0) -> None:
    c.saveState()
    c.setFillColor(fill)
    c.setStrokeColor(stroke or fill)
    c.setLineWidth(width)
    c.roundRect(x, y, w, h, radius, fill=1, stroke=1 if stroke else 0)
    c.restoreState()


def page_bg(c: canvas.Canvas, dark: bool) -> None:
    c.setFillColor(BG if dark else colors.HexColor("#f5f8fb"))
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    if dark:
        c.setFillColor(colors.HexColor("#0b2030"))
        c.rect(0, 0, PAGE_W, 220, fill=1, stroke=0)


def header(c: canvas.Canvas, page: int, label: str, dark: bool) -> None:
    color = colors.HexColor("#8fa2b7") if dark else colors.HexColor("#617185")
    draw_text(c, "Aureus Automation Lab", MARGIN, PAGE_H - 54, 18, color, FONT_BOLD)
    right = f"{page:02d}/12"
    draw_text(c, right, PAGE_W - MARGIN - string_width(right, 18, FONT_BOLD), PAGE_H - 54, 18, color, FONT_BOLD)
    c.setStrokeColor(colors.HexColor("#24384b") if dark else LINE)
    c.setLineWidth(1)
    c.line(MARGIN, PAGE_H - 78, PAGE_W - MARGIN, PAGE_H - 78)
    if label:
        draw_text(c, label, MARGIN, PAGE_H - 100, 13, color, FONT_BOLD)


def footer(c: canvas.Canvas, dark: bool) -> None:
    color = colors.HexColor("#8fa2b7") if dark else colors.HexColor("#657588")
    draw_text(c, "Public-safe Instagram carousel", MARGIN, 34, 15, color, FONT)


def chip(c: canvas.Canvas, label: str, x: float, y: float, accent, dark: bool = True) -> float:
    size = 17
    width = string_width(label, size, FONT_BOLD) + 30
    fill = colors.Color(accent.red, accent.green, accent.blue, alpha=0.16 if dark else 0.10)
    rounded(c, x, y, width, 36, fill, accent, radius=18, width=1.2)
    draw_text(c, label, x + 15, y + 11, size, accent, FONT_BOLD)
    return x + width + 10


def draw_bullet_list(c: canvas.Canvas, items: Iterable[str], x: float, y: float, width: float, accent, color, size=22) -> float:
    current_y = y
    for item in items:
        c.setFillColor(accent)
        c.circle(x + 7, current_y + 6, 5, fill=1, stroke=0)
        current_y = draw_wrapped(c, item, x + 24, current_y, width - 24, size, color, FONT, size * 1.25, 2) - 7
    return current_y


def card(c: canvas.Canvas, x: float, y: float, w: float, h: float, title: str, body: str, accent, dark: bool, max_lines=4) -> None:
    fill = PANEL if dark else WHITE
    stroke = LINE_DARK if dark else LINE
    title_color = WHITE if dark else INK
    body_color = SOFT if dark else MUTED
    rounded(c, x, y, w, h, fill, stroke, radius=24, width=1)
    c.setFillColor(accent)
    c.rect(x, y, 7, h, fill=1, stroke=0)
    draw_text(c, title, x + 26, y + h - 42, 26, title_color, FONT_BOLD)
    draw_wrapped(c, body, x + 26, y + h - 82, w - 52, 22, body_color, FONT, 29, max_lines)


def image_frame(c: canvas.Canvas, img: Path, x: float, y: float, w: float, h: float, label: str | None = None) -> None:
    rounded(c, x, y, w, h, colors.HexColor("#0a1622"), LINE_DARK, radius=28, width=1.1)
    c.saveState()
    path = c.beginPath()
    path.roundRect(x + 2, y + 2, w - 4, h - 4, 24)
    c.clipPath(path, stroke=0, fill=0)
    c.drawImage(str(img), x + 2, y + 2, width=w - 4, height=h - 4, preserveAspectRatio=True, anchor="c")
    c.restoreState()
    c.setFillColor(colors.Color(0, 0, 0, alpha=0.18))
    c.roundRect(x + 2, y + 2, w - 4, h - 4, 24, fill=1, stroke=0)
    if label:
        badge_width = min(w - 44, string_width(label, 16, FONT_BOLD) + 34)
        rounded(c, x + 22, y + h - 58, badge_width, 34, colors.Color(0.04, 0.09, 0.13, alpha=0.88), colors.HexColor("#3b5870"), 17, 0.8)
        draw_wrapped(c, label, x + 38, y + h - 36, w - 75, 16, WHITE, FONT_BOLD, 18, 1)


def fallback_visual(c: canvas.Canvas, x: float, y: float, w: float, h: float, title: str, accent) -> None:
    rounded(c, x, y, w, h, colors.HexColor("#0a1622"), LINE_DARK, radius=28, width=1.1)
    draw_text(c, title, x + 34, y + h - 54, 28, WHITE, FONT_BOLD)
    step_w = (w - 90) / 5
    labels = ["Signal", "AI", "Review", "Evidence", "Output"]
    for i, label in enumerate(labels):
        sx = x + 34 + i * step_w
        rounded(c, sx, y + 90, step_w - 18, 82, colors.HexColor("#101f2b"), accent if i == 2 else LINE_DARK, 16, 1)
        draw_wrapped(c, label, sx + 14, y + 136, step_w - 46, 17, SOFT, FONT_BOLD, 20, 2)
        if i < len(labels) - 1:
            c.setStrokeColor(accent)
            c.setLineWidth(2)
            c.line(sx + step_w - 18, y + 132, sx + step_w + 6, y + 132)


def carousel_data(pack: dict, lang: str) -> dict:
    if lang == "sk":
        return {
            **pack,
            "cover_kicker": "6 klientskych use casov",
            "cover_title": "Aureus Use Case Portfólio",
            "cover_subtitle": "Ako zmeniť manuálnu firemnú prácu na kontrolované AI workflowy, ktoré človek vie schváliť a spätne skontrolovať.",
            "rule_label": "Základné pravidlo",
            "model_label": "Ako vyberáme správny use case",
            "case_labels": {
                "problem": "Problém klienta",
                "ai": "Čo pripraví AI",
                "receives": "Čo klient dostane",
                "first": "Prvý krok",
            },
            "score_title": "Ktorý pilot má zmysel ako prvý?",
            "score_subtitle": "Začíname tam, kde je hodnota viditeľná, riziko ohraničené a schvaľovanie jasné.",
            "pilot_title": "30-dňová pilotná cesta",
            "pilot_subtitle": "Cieľom nie je automatizovať všetko. Cieľom je dokázať jeden kontrolovaný workflow, ktorému klient rozumie.",
            "pilot_by_day_label": "Do 30 dní klient dostane",
            "pilot_out": "Mapa procesu, pilot brief, schvaľovacia hranica, príklad záznamu, risk list a ďalší krok.",
            "usage_title": "Ako tento carousel použiť",
            "usage_subtitle": "Materiál je pripravený na Instagram, follow-up po hovore a vysvetlenie ponuky bez odhalenia privátnej implementácie.",
            "usage": [
                ("Prvý hovor", "Použi ho na rýchle vysvetlenie, čo Aureus rieši a pre koho."),
                ("Follow-up", "Pošli carousel po stretnutí ako jednoduché zhrnutie možností."),
                ("Instagram", "Publikuj ako carousel: úvod, 6 use casov, scorecard, pilot, CTA."),
                ("Predaj", "Použi ho ako most medzi záujmom klienta a konkrétnym Automation Auditom."),
                ("Bezpečnosť", "Materiál neukazuje privátne workflowy, credentials ani reálne dáta."),
                ("Dôkaz", "Ukazuje model práce: AI pripraví, človek schváli, záznam ostane."),
            ],
            "safety_label": "Hranica",
            "safety": "Žiadne privátne exporty, žiadne falošné výsledky, žiadne slepé odosielanie a žiadne tvrdenie o účtovníckej správnosti bez potvrdenia.",
            "cta_kicker": "Najlepší prvý krok",
            "cta_title": "Začnite s Automation Auditom",
            "cta_subtitle": "Pošlite jeden proces, workflow alebo tok dokladov, ktorý dnes berie čas alebo vytvára neistotu.",
            "why_label": "Prečo takto",
            "why_text": "Najprv zmapujeme proces, nájdeme použiteľné miesto pre AI, nastavíme schvaľovaciu hranicu a ukážeme, aký dôkaz má ostať.",
            "buyer_action_label": "Akcia pre klienta",
            "cta_action": "Vyberte jeden opakovaný proces. Aureus z neho pripraví mapu, riziká, prvý pilot a jasný ďalší krok.",
        }
    return {
        **pack,
        "cover_kicker": "6 client-ready use cases",
        "cover_title": "Aureus Use Case Portfolio",
        "cover_subtitle": "How to turn manual business work into controlled AI workflows that people can approve and review.",
        "rule_label": "Core rule",
        "model_label": "How we choose the right use case",
        "case_labels": {
            "problem": "Client problem",
            "ai": "What AI prepares",
            "receives": "Client receives",
            "first": "First step",
        },
        "score_title": "Which pilot should start first?",
        "score_subtitle": "Start where value is visible, risk is bounded, and approval responsibility is clear.",
        "pilot_title": "30-Day Client Pilot Path",
        "pilot_subtitle": "The goal is not to automate everything. The goal is to prove one controlled workflow the client understands.",
        "pilot_by_day_label": "By day 30 the client receives",
        "pilot_out": "Process map, pilot brief, approval boundary, evidence example, risk list, and next step.",
        "usage_title": "How To Use This Carousel",
        "usage_subtitle": "Built for Instagram, follow-up after a call, and offer explanation without exposing private implementation.",
        "usage": [
            ("First call", "Use it to explain what Aureus solves and who it helps."),
            ("Follow-up", "Send it after a meeting as a simple summary of options."),
            ("Instagram", "Post as carousel: cover, 6 use cases, scorecard, pilot, CTA."),
            ("Sales", "Use it as a bridge between interest and a concrete Automation Audit."),
            ("Safety", "It does not show private workflows, credentials, or real data."),
            ("Proof", "It shows the operating model: AI prepares, people approve, evidence remains."),
        ],
        "safety_label": "Boundary",
        "safety": "No private exports, no fake proof, no blind sending, and no accounting correctness claim without validation.",
        "cta_kicker": "Best first step",
        "cta_title": "Start With Automation Audit",
        "cta_subtitle": "Send one process, workflow, or document flow that wastes time or creates uncertainty today.",
        "why_label": "Why this works",
        "why_text": "We map the process, find the useful AI entry point, define the approval boundary, and show what evidence should remain.",
        "buyer_action_label": "Client action",
        "cta_action": "Pick one repeated process. Aureus turns it into a process map, risk list, first pilot, and clear next step.",
    }


def draw_cover(c: canvas.Canvas, data: dict, crops: dict[int, Path]) -> None:
    page_bg(c, True)
    header(c, 1, "Instagram carousel", True)
    chip(c, data["cover_kicker"], MARGIN, 1138, GOLD, True)
    draw_wrapped(c, data["cover_title"], MARGIN, 1064, PAGE_W - MARGIN * 2, 61, WHITE, FONT_BOLD, 70, 2)
    draw_wrapped(c, data["cover_subtitle"], MARGIN, 910, PAGE_W - MARGIN * 2, 31, SOFT, FONT, 40, 3)
    if 1 in crops:
        image_frame(c, crops[1], MARGIN, 575, PAGE_W - MARGIN * 2, 272, "Controlled AI automation system")
    else:
        fallback_visual(c, MARGIN, 575, PAGE_W - MARGIN * 2, 272, "Controlled AI automation system", GOLD)
    rounded(c, MARGIN, 332, PAGE_W - MARGIN * 2, 166, PANEL, LINE_DARK, 28, 1)
    draw_text(c, data["rule_label"], MARGIN + 30, 430, 25, GOLD, FONT_BOLD)
    draw_wrapped(c, data["rule"], MARGIN + 30, 390, PAGE_W - MARGIN * 2 - 60, 38, WHITE, FONT_BOLD, 48, 3)
    x = MARGIN
    for label, accent in [("Audit", GOLD), ("FinEcon", TEAL), ("n8n", BLUE), ("Sales", GREEN), ("Aureus OS", PURPLE)]:
        x = chip(c, label, x, 244, accent, True)
    footer(c, True)


def draw_model(c: canvas.Canvas, data: dict) -> None:
    page_bg(c, False)
    header(c, 2, data["model_label"], False)
    draw_wrapped(c, data["model_title"], MARGIN, 1168, PAGE_W - MARGIN * 2, 52, INK, FONT_BOLD, 60, 2)
    draw_wrapped(c, data["model_subtitle"], MARGIN, 1040, PAGE_W - MARGIN * 2, 28, MUTED, FONT, 36, 3)
    y = 850
    for i, (title, body) in enumerate(data["signals"]):
        accent = [TEAL, GOLD, BLUE, GREEN, PURPLE][i]
        rounded(c, MARGIN, y, PAGE_W - MARGIN * 2, 118, WHITE, LINE, 22, 1)
        draw_text(c, f"{i + 1:02d}", MARGIN + 28, y + 67, 34, accent, FONT_BOLD)
        draw_text(c, title, MARGIN + 100, y + 73, 27, INK, FONT_BOLD)
        draw_wrapped(c, body, MARGIN + 100, y + 37, PAGE_W - MARGIN * 2 - 130, 21, MUTED, FONT, 27, 2)
        y -= 138
    rounded(c, MARGIN, 74, PAGE_W - MARGIN * 2, 92, BG, BG, 22, 1)
    draw_wrapped(c, data["decision_rule"], MARGIN + 26, 130, PAGE_W - MARGIN * 2 - 52, 23, WHITE, FONT_BOLD, 30, 2)
    footer(c, False)


def draw_use_case(c: canvas.Canvas, uc, data: dict, crops: dict[int, Path], page: int) -> None:
    page_bg(c, True)
    header(c, page, "Use case", True)
    accent = uc.accent
    chip(c, uc.case, MARGIN, 1178, accent, True)
    title_bottom = draw_wrapped(c, uc.title, MARGIN, 1118, PAGE_W - MARGIN * 2, 51, WHITE, FONT_BOLD, 58, 2)
    draw_wrapped(c, uc.promise, MARGIN, min(1002, title_bottom - 14), PAGE_W - MARGIN * 2, 29, SOFT, FONT, 37, 2)
    if uc.visual_page in crops:
        image_frame(c, crops[uc.visual_page], MARGIN, 720, PAGE_W - MARGIN * 2, 246, uc.title)
    else:
        fallback_visual(c, MARGIN, 720, PAGE_W - MARGIN * 2, 246, uc.title, accent)
    labels = data["case_labels"]
    card(c, MARGIN, 524, PAGE_W - MARGIN * 2, 148, labels["problem"], uc.problem, accent, True, 3)
    card(c, MARGIN, 350, PAGE_W - MARGIN * 2, 148, labels["ai"], uc.ai, TEAL, True, 3)
    card(c, MARGIN, 176, PAGE_W - MARGIN * 2, 148, labels["receives"], ", ".join(uc.receives) + ".", BLUE, True, 3)
    rounded(c, MARGIN, 76, PAGE_W - MARGIN * 2, 76, WHITE, WHITE, 22, 1)
    draw_text(c, labels["first"], MARGIN + 24, 105, 23, INK, FONT_BOLD)
    draw_wrapped(c, uc.first_step, MARGIN + 206, 110, PAGE_W - MARGIN * 2 - 230, 20, MUTED, FONT, 25, 2)
    footer(c, True)


def draw_scorecard(c: canvas.Canvas, data: dict) -> None:
    page_bg(c, False)
    header(c, 9, "Scorecard", False)
    draw_wrapped(c, data["score_title"], MARGIN, 1168, PAGE_W - MARGIN * 2, 50, INK, FONT_BOLD, 58, 2)
    draw_wrapped(c, data["score_subtitle"], MARGIN, 1048, PAGE_W - MARGIN * 2, 27, MUTED, FONT, 35, 3)
    y = 855
    for row in data["score_rows"]:
        name, signal, fit, _proof, first = row
        rounded(c, MARGIN, y, PAGE_W - MARGIN * 2, 112, WHITE, LINE, 22, 1)
        draw_text(c, name, MARGIN + 25, y + 66, 25, INK, FONT_BOLD)
        draw_wrapped(c, signal, MARGIN + 25, y + 34, 505, 18, MUTED, FONT, 23, 2)
        chip(c, fit, MARGIN + 585, y + 58, GREEN if fit in {"High", "Vysoký"} else GOLD, False)
        draw_wrapped(c, first, MARGIN + 585, y + 33, 350, 18, INK, FONT_BOLD, 23, 1)
        y -= 128
    footer(c, False)


def draw_pilot(c: canvas.Canvas, data: dict) -> None:
    page_bg(c, True)
    header(c, 10, "Pilot path", True)
    draw_wrapped(c, data["pilot_title"], MARGIN, 1168, PAGE_W - MARGIN * 2, 54, WHITE, FONT_BOLD, 62, 2)
    draw_wrapped(c, data["pilot_subtitle"], MARGIN, 1038, PAGE_W - MARGIN * 2, 29, SOFT, FONT, 38, 3)
    y = 828
    for i, (week, title, body) in enumerate(data["weeks"]):
        accent = [TEAL, GOLD, PURPLE, GREEN][i]
        rounded(c, MARGIN, y, PAGE_W - MARGIN * 2, 145, PANEL, LINE_DARK, 24, 1)
        draw_text(c, week, MARGIN + 26, y + 92, 24, accent, FONT_BOLD)
        draw_text(c, title, MARGIN + 220, y + 88, 34, WHITE, FONT_BOLD)
        draw_wrapped(c, body, MARGIN + 220, y + 48, PAGE_W - MARGIN * 2 - 250, 21, SOFT, FONT, 27, 2)
        y -= 168
    rounded(c, MARGIN, 84, PAGE_W - MARGIN * 2, 118, WHITE, WHITE, 26, 1)
    draw_text(c, data["pilot_by_day_label"], MARGIN + 28, 146, 25, INK, FONT_BOLD)
    draw_wrapped(c, data["pilot_out"], MARGIN + 28, 111, PAGE_W - MARGIN * 2 - 56, 21, MUTED, FONT, 27, 2)
    footer(c, True)


def draw_usage(c: canvas.Canvas, data: dict) -> None:
    page_bg(c, False)
    header(c, 11, "Use rules", False)
    draw_wrapped(c, data["usage_title"], MARGIN, 1168, PAGE_W - MARGIN * 2, 52, INK, FONT_BOLD, 60, 2)
    draw_wrapped(c, data["usage_subtitle"], MARGIN, 1048, PAGE_W - MARGIN * 2, 27, MUTED, FONT, 35, 3)
    y = 835
    for i, (title, body) in enumerate(data["usage"]):
        accent = [TEAL, RED, BLUE, PURPLE, GOLD, GREEN][i]
        rounded(c, MARGIN, y, PAGE_W - MARGIN * 2, 108, WHITE, LINE, 22, 1)
        c.setFillColor(accent)
        c.rect(MARGIN, y, 8, 108, fill=1, stroke=0)
        draw_text(c, title, MARGIN + 28, y + 63, 25, INK, FONT_BOLD)
        draw_wrapped(c, body, MARGIN + 28, y + 30, PAGE_W - MARGIN * 2 - 56, 19, MUTED, FONT, 24, 2)
        y -= 126
    rounded(c, MARGIN, 78, PAGE_W - MARGIN * 2, 126, BG, BG, 24, 1)
    draw_text(c, data["safety_label"], MARGIN + 26, 155, 22, GOLD, FONT_BOLD)
    draw_wrapped(c, data["safety"], MARGIN + 26, 120, PAGE_W - MARGIN * 2 - 52, 18, WHITE, FONT, 23, 3)
    footer(c, False)


def draw_cta(c: canvas.Canvas, data: dict, crops: dict[int, Path]) -> None:
    page_bg(c, True)
    header(c, 12, data["cta_kicker"], True)
    draw_wrapped(c, data["cta_title"], MARGIN, 1172, PAGE_W - MARGIN * 2, 58, WHITE, FONT_BOLD, 64, 2)
    draw_wrapped(c, data["cta_subtitle"], MARGIN, 1030, PAGE_W - MARGIN * 2, 30, SOFT, FONT, 39, 3)
    if 12 in crops:
        image_frame(c, crops[12], MARGIN, 704, PAGE_W - MARGIN * 2, 260, "Next path")
    else:
        fallback_visual(c, MARGIN, 704, PAGE_W - MARGIN * 2, 260, "Next path", GOLD)
    rounded(c, MARGIN, 486, PAGE_W - MARGIN * 2, 150, PANEL, GOLD, 26, 1.3)
    draw_text(c, data["why_label"], MARGIN + 28, 580, 26, GOLD, FONT_BOLD)
    draw_wrapped(c, data["why_text"], MARGIN + 28, 540, PAGE_W - MARGIN * 2 - 56, 22, WHITE, FONT, 29, 3)
    rounded(c, MARGIN, 254, PAGE_W - MARGIN * 2, 152, WHITE, WHITE, 26, 1)
    draw_text(c, data["buyer_action_label"], MARGIN + 28, 350, 27, INK, FONT_BOLD)
    draw_wrapped(c, data["cta_action"], MARGIN + 28, 310, PAGE_W - MARGIN * 2 - 56, 22, MUTED, FONT, 29, 3)
    footer(c, True)


def generate_pdf(pdf_path: Path, data: dict, cases: list, crops: dict[int, Path]) -> None:
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(pdf_path), pagesize=(PAGE_W, PAGE_H))
    c.setTitle(f"Aureus Use Case Instagram Carousel V7 {data['lang'].upper()}")
    draw_cover(c, data, crops)
    c.showPage()
    draw_model(c, data)
    c.showPage()
    for page, use_case in enumerate(cases, start=3):
        draw_use_case(c, use_case, data, crops, page)
        c.showPage()
    draw_scorecard(c, data)
    c.showPage()
    draw_pilot(c, data)
    c.showPage()
    draw_usage(c, data)
    c.showPage()
    draw_cta(c, data, crops)
    c.save()


def render_pdf_to_pngs(pdf_path: Path, out_dir: Path) -> list[Path]:
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(pdf_path)
    paths: list[Path] = []
    for page_no, page in enumerate(doc, start=1):
        pix = page.get_pixmap(matrix=fitz.Matrix(1, 1), alpha=False)
        out = out_dir / f"slide_{page_no:02d}.png"
        pix.save(out)
        paths.append(out)
    doc.close()
    return paths


def make_zip(paths: list[Path], zip_path: Path) -> None:
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in paths:
            archive.write(path, path.name)


def desktop_dir() -> Path | None:
    for candidate in [
        Path.home() / "OneDrive" / "Počítač",
        Path.home() / "OneDrive" / "Desktop",
        Path.home() / "Desktop",
    ]:
        if candidate.exists():
            return candidate
    return None


def copy_to_desktop(pngs: list[Path], folder_name: str, zip_path: Path) -> Path | None:
    desktop = desktop_dir()
    if not desktop:
        return None
    dest = desktop / folder_name
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True, exist_ok=True)
    for path in pngs:
        shutil.copy2(path, dest / path.name)
    shutil.copy2(zip_path, desktop / zip_path.name)
    return dest


def generate_pack(lang: str, data: dict, cases: list, crops: dict[int, Path]) -> tuple[Path, Path, Path, Path | None]:
    folder_name = f"Aureus_Use_Case_Instagram_Carousel_V7_{lang}"
    pdf_path = OUT_ROOT / f"{folder_name}.pdf"
    png_dir = OUT_ROOT / folder_name
    zip_path = OUT_ROOT / f"{folder_name}.zip"
    generate_pdf(pdf_path, data, cases, crops)
    pngs = render_pdf_to_pngs(pdf_path, png_dir)
    make_zip(pngs, zip_path)
    desktop = copy_to_desktop(pngs, folder_name, zip_path)
    return pdf_path, png_dir, zip_path, desktop


def main() -> int:
    source = load_source_module()
    crops = source.make_visual_crops()
    OUT_ROOT.mkdir(parents=True, exist_ok=True)

    packs = [
        ("SK", carousel_data(source.sk_pack(), "sk"), source.sk_cases()),
        ("EN", carousel_data(source.en_pack(), "en"), source.en_cases()),
    ]

    for lang, data, cases in packs:
        pdf_path, png_dir, zip_path, desktop = generate_pack(lang, data, cases, crops)
        print(f"{lang} PDF: {pdf_path}")
        print(f"{lang} PNG folder: {png_dir}")
        print(f"{lang} ZIP: {zip_path}")
        if desktop:
            print(f"{lang} copied to: {desktop}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
