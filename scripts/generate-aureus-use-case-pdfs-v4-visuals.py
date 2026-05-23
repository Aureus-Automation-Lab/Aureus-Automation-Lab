from __future__ import annotations

import runpy
from pathlib import Path

import fitz
from reportlab.lib import colors
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
BASE = runpy.run_path(str(ROOT / "scripts" / "generate-aureus-use-case-pdfs.py"))

EXPORT_DIR = ROOT / "exports"
PREVIEW_DIR = EXPORT_DIR / "preview_v4_visuals"
V4_PAGES = EXPORT_DIR / "v4_pages"
DESKTOP_DIR = Path.home() / "OneDrive" / "Počítač"

PAGE_W = BASE["PAGE_W"]
PAGE_H = BASE["PAGE_H"]
MARGIN = BASE["MARGIN"]
FONT = BASE["FONT"]
FONT_BOLD = BASE["FONT_BOLD"]

NAVY = BASE["NAVY"]
NAVY_2 = BASE["NAVY_2"]
INK = BASE["INK"]
MUTED = BASE["MUTED"]
LINE = BASE["LINE"]
WHITE = BASE["WHITE"]
GOLD = BASE["GOLD"]
TEAL = BASE["TEAL"]
BLUE = BASE["BLUE"]
GREEN = BASE["GREEN"]
PURPLE = BASE["PURPLE"]
RED = BASE["RED"]
CARD_DARK = BASE["CARD_DARK"]
CARD_LIGHT = BASE["CARD_LIGHT"]

draw_text = BASE["draw_text"]
draw_wrapped = BASE["draw_wrapped"]
round_rect = BASE["round_rect"]
chip = BASE["chip"]
footer = BASE["footer"]
flow_bar = BASE["flow_bar"]
bullets = BASE["bullets"]
sw = BASE["sw"]

EN = BASE["EN"]
SK = BASE["SK"]
USE_CASES_EN = BASE["USE_CASES_EN"]
USE_CASES_SK = BASE["USE_CASES_SK"]


def find_v4_pdf() -> Path:
    local = ROOT / "_input" / "Aureus_World_Class_Use_Case_Showcase_v4_final.pdf"
    if local.exists():
        return local
    for candidate in Path.home().rglob("Aureus_World_Class_Use_Case_Showcase_v4_final.pdf"):
        return candidate
    raise FileNotFoundError("Aureus_World_Class_Use_Case_Showcase_v4_final.pdf not found")


def render_v4_pages() -> None:
    src = find_v4_pdf()
    V4_PAGES.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(src)
    for i, page in enumerate(doc, 1):
        out = V4_PAGES / f"page_{i:02d}.png"
        if out.exists():
            continue
        pix = page.get_pixmap(matrix=fitz.Matrix(0.5, 0.5), alpha=False)
        pix.save(out)


def draw_bg(c: canvas.Canvas, page_no: int):
    bg = V4_PAGES / f"page_{page_no:02d}.png"
    c.drawImage(str(bg), 0, 0, width=PAGE_W, height=PAGE_H)


def cover(c: canvas.Canvas, x: float, y: float, w: float, h: float, fill=NAVY):
    c.setFillColor(fill)
    c.rect(x, y, w, h, fill=1, stroke=0)


def left_card(c, x, y, w, h, title, body, accent, dark=True):
    fill = colors.HexColor("#0f2233") if dark else WHITE
    stroke = colors.HexColor("#244259") if dark else LINE
    text = WHITE if dark else INK
    sub = colors.HexColor("#c5d2df") if dark else MUTED
    round_rect(c, x, y, w, h, fill, stroke, 10, 0.9)
    c.setFillColor(accent)
    c.rect(x, y, 4, h, fill=1, stroke=0)
    draw_text(c, title, x + 16, y + h - 22, 10.2, text, FONT_BOLD)
    draw_wrapped(c, body, x + 16, y + h - 42, w - 30, 8.5, sub, FONT, 10.8, 4)


def small_card(c, x, y, w, h, title, body, accent):
    round_rect(c, x, y, w, h, colors.HexColor("#0f2233"), colors.HexColor("#27435a"), 10, 0.8)
    c.setFillColor(accent)
    c.rect(x, y, 4, h, fill=1, stroke=0)
    draw_text(c, title, x + 14, y + h - 20, 10.5, WHITE, FONT_BOLD)
    draw_wrapped(c, body, x + 14, y + h - 39, w - 26, 7.6, colors.HexColor("#c5d2df"), FONT, 9.5, 3)


def status_chips(c, items, x, y, accent):
    current = x
    for item in items:
        current = chip(c, item, current, y, accent)


def draw_cover_v4(c, data, lang):
    draw_bg(c, 1)
    cover(c, 34, 38, 482, 462)
    cover(c, 520, 34, 394, 90)
    draw_wrapped(c, data["title"], MARGIN, 438, 430, 30, WHITE, FONT_BOLD, 37)
    draw_wrapped(c, data["subtitle"], MARGIN, 372, 420, 13.5, colors.HexColor("#cbd8e6"), FONT, 18, 4)
    x = MARGIN
    for label, color in data["chips"]:
        x = chip(c, label, x, 306, color)
    round_rect(c, MARGIN, 72, 420, 92, colors.HexColor("#0b1c2a"), colors.HexColor("#244259"), 14, 1)
    draw_text(c, data["rule_title"], MARGIN + 18, 126, 12.5, GOLD, FONT_BOLD)
    draw_wrapped(c, data["rule"], MARGIN + 18, 98, 382, 18, WHITE, FONT_BOLD, 23, 3)
    label = "What a buyer should understand" if lang == "en" else "Čo má kupujúci pochopiť"
    body = (
        "The problem, the safe AI role, the human review boundary, the evidence trail, and the first commercial next step."
        if lang == "en"
        else "Problém, bezpečnú rolu AI, hranicu ľudského schválenia, dôkazový záznam a prvý obchodný krok."
    )
    round_rect(c, 520, 42, 390, 70, colors.HexColor("#0f2233"), colors.HexColor("#244259"), 12, 0.9)
    draw_text(c, label, 535, 86, 12, TEAL, FONT_BOLD)
    draw_wrapped(c, body, 535, 68, 355, 8.5, colors.HexColor("#c5d2df"), FONT, 10.5, 3)
    footer(c, True)


def draw_model_v4(c, data):
    c.setFillColor(colors.HexColor("#f5f8fb"))
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    BASE["header"](c, data["kicker"], 2, False)
    draw_wrapped(c, data["title"], MARGIN, 445, 720, 26, INK, FONT_BOLD, 32)
    draw_wrapped(c, data["subtitle"], MARGIN, 395, 770, 12.5, MUTED, FONT, 17, 3)
    signals = data["signals"]
    for i, signal in enumerate(signals):
        x = MARGIN + (i % 3) * 295
        y = 287 if i < 3 else 205
        w = 270 if i < 3 else 420
        if i == 4:
            x = MARGIN + 450
        round_rect(c, x, y, w, 62, WHITE, LINE, 9, 0.8)
        draw_text(c, f"{i + 1:02d}", x + 14, y + 38, 14, [TEAL, GOLD, RED, BLUE, GREEN][i], FONT_BOLD)
        draw_wrapped(c, signal["title"], x + 50, y + 40, w - 65, 11, INK, FONT_BOLD, 13, 1)
        draw_wrapped(c, signal["copy"], x + 14, y + 20, w - 32, 8.4, MUTED, FONT, 10.5, 2)
    round_rect(c, MARGIN, 112, PAGE_W - MARGIN * 2, 78, WHITE, LINE, 11, 0.8)
    draw_text(c, data["flow_title"], MARGIN + 16, 160, 13.5, INK, FONT_BOLD)
    flow_bar(c, data["flow"], MARGIN + 20, 124, PAGE_W - MARGIN * 2 - 40, dark=False)
    round_rect(c, MARGIN, 52, PAGE_W - MARGIN * 2, 36, NAVY, NAVY, 10, 1)
    draw_text(c, data["bottom_rule_title"], MARGIN + 16, 65, 11.5, GOLD, FONT_BOLD)
    draw_wrapped(c, data["bottom_rule"], MARGIN + 110, 68, PAGE_W - MARGIN * 2 - 130, 8.8, WHITE, FONT, 11, 2)


def draw_proof_status(c, x, y, w, h, title, statuses, boundary, accent):
    round_rect(c, x, y, w, h, colors.HexColor("#0f2233"), colors.HexColor("#27435a"), 10, 0.8)
    c.setFillColor(accent)
    c.rect(x, y, 4, h, fill=1, stroke=0)
    draw_text(c, title, x + 14, y + h - 20, 10.5, WHITE, FONT_BOLD)
    status_chips(c, statuses, x + 14, y + h - 44, accent)
    draw_wrapped(c, boundary, x + 14, y + 21, w - 26, 7.2, colors.HexColor("#c5d2df"), FONT, 8.8, 2)


def draw_use_case_v4(c, item, page_no, lang):
    draw_bg(c, page_no)
    cover(c, 34, 42, 420, 454)
    cover(c, 456, 40, 470, 205)
    accent = item["accent"]
    status = item["status"]
    # chip
    round_rect(c, MARGIN, 444, 72, 18, colors.Color(accent.red, accent.green, accent.blue, alpha=0.12), accent, 8, 0.8)
    draw_text(c, item["case"], MARGIN + 10, 450, 8.5, accent, FONT_BOLD)
    draw_wrapped(c, item["title"], MARGIN, 398, 390, 26, WHITE, FONT_BOLD, 31, 2)
    draw_wrapped(c, item["promise"], MARGIN, 350, 390, 12.3, colors.HexColor("#cbd8e6"), FONT, 16, 3)
    labels = {
        "problem": "Buyer problem" if lang == "en" else "Problém klienta",
        "workflow": "Controlled workflow" if lang == "en" else "Kontrolovaný workflow",
        "receives": "Client receives" if lang == "en" else "Čo klient dostane",
        "ai": "AI prepares" if lang == "en" else "AI pripraví",
        "approve": "People approve" if lang == "en" else "Ľudia schvaľujú",
        "evidence": "Evidence remains" if lang == "en" else "Dôkaz zostáva",
        "status": "Proof status" if lang == "en" else "Stav dôkazu",
    }
    left_card(c, MARGIN, 274, 390, 58, labels["problem"], item["problem"], accent)
    left_card(c, MARGIN, 190, 390, 70, labels["workflow"], " -> ".join(item["workflow"]), accent)
    left_card(c, MARGIN, 88, 390, 86, labels["receives"], ", ".join(item["receives"]) + ".", accent)
    small_card(c, 468, 166, 205, 67, labels["ai"], item["ai"], TEAL)
    small_card(c, 695, 166, 205, 67, labels["approve"], item["approve"], GOLD)
    small_card(c, 468, 72, 205, 78, labels["evidence"], item["evidence"], BLUE)
    draw_proof_status(c, 695, 72, 205, 78, labels["status"], status, item["boundary"], accent)
    footer(c, True)


def draw_scorecards_v4(c, data, lang):
    c.setFillColor(colors.HexColor("#f5f8fb"))
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    BASE["header"](c, data["kicker"], 9, False)
    draw_wrapped(c, data["title"], MARGIN, 438, 760, 27, INK, FONT_BOLD, 33)
    draw_wrapped(c, data["subtitle"], MARGIN, 390, 780, 12.5, MUTED, FONT, 16, 2)
    rows = data["rows"]
    accents = [GOLD, BLUE, TEAL, GREEN, PURPLE, RED]
    for i, row in enumerate(rows):
        col = i % 3
        r = i // 3
        x = MARGIN + col * 304
        y = 255 - r * 128
        round_rect(c, x, y, 270, 96, WHITE, LINE, 9, 0.8)
        c.setFillColor(accents[i])
        c.rect(x, y, 4, 96, fill=1, stroke=0)
        draw_text(c, row[0], x + 14, y + 70, 14, INK, FONT_BOLD)
        chip(c, row[5], x + 14, y + 47, accents[i], dark=False)
        if lang == "en":
            headline = f"{row[1]} value / {row[2].lower()} effort"
            meta = f"Review: {row[3]}. Proof: {row[4]}."
        else:
            headline = f"Hodnota: {row[1]} / úsilie: {row[2].lower()}"
            meta = f"Review: {row[3]}. Dôkaz: {row[4]}."
        draw_text(c, headline, x + 14, y + 31, 10.2, INK, FONT_BOLD)
        draw_wrapped(c, meta, x + 14, y + 17, 225, 8.2, MUTED, FONT, 9.8, 2)
    round_rect(c, MARGIN, 48, PAGE_W - MARGIN * 2, 40, NAVY, NAVY, 10, 1)
    draw_text(c, data["rule_label"], MARGIN + 16, 62, 12.5, GOLD, FONT_BOLD)
    draw_wrapped(c, data["rule"], MARGIN + 136, 65, PAGE_W - MARGIN * 2 - 155, 9.2, WHITE, FONT, 11.5, 2)
    footer(c, False)


def draw_pilot_v4(c, data):
    c.setFillColor(NAVY)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    BASE["header"](c, data["kicker"], 10, True)
    draw_wrapped(c, data["title"], MARGIN, 436, 720, 27, WHITE, FONT_BOLD, 33)
    draw_wrapped(c, data["subtitle"], MARGIN, 390, 800, 12.5, colors.HexColor("#cbd8e6"), FONT, 16, 3)
    for i, week in enumerate(data["weeks"]):
        x = MARGIN + i * 232
        round_rect(c, x, 206, 194, 150, CARD_DARK, colors.HexColor("#27435a"), 12, 0.8)
        draw_text(c, week["week"], x + 14, 319, 13.5, [TEAL, GOLD, PURPLE, GREEN][i], FONT_BOLD)
        draw_wrapped(c, week["title"], x + 14, 288, 160, 17, WHITE, FONT_BOLD, 21, 2)
        draw_wrapped(c, week["copy"], x + 14, 250, 154, 9, colors.HexColor("#b9c7d7"), FONT, 11.5, 4)
    round_rect(c, MARGIN, 80, PAGE_W - MARGIN * 2, 58, WHITE, WHITE, 12, 1)
    draw_text(c, data["promise_label"], MARGIN + 18, 104, 14, INK, FONT_BOLD)
    draw_wrapped(c, data["promise"], MARGIN + 150, 108, PAGE_W - MARGIN * 2 - 174, 9.5, MUTED, FONT, 12, 2)
    footer(c, True)


def draw_usage_v4(c, data):
    c.setFillColor(colors.HexColor("#f5f8fb"))
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    BASE["header"](c, data["kicker"], 11, False)
    draw_wrapped(c, data["title"], MARGIN, 438, 760, 26, INK, FONT_BOLD, 32)
    draw_wrapped(c, data["subtitle"], MARGIN, 395, 790, 12.5, MUTED, FONT, 16, 2)
    uses = data["uses"]
    for i, item in enumerate(uses):
        col = i % 2
        row = i // 2
        x = MARGIN + col * 470
        y = 314 - row * 76
        accent = [TEAL, RED, BLUE, PURPLE, GOLD, GREEN][i]
        round_rect(c, x, y, 430, 52, WHITE, LINE, 9, 0.7)
        c.setFillColor(accent)
        c.rect(x, y, 4, 52, fill=1, stroke=0)
        draw_text(c, item["title"], x + 14, y + 32, 10.5, INK, FONT_BOLD)
        draw_wrapped(c, item["copy"], x + 14, y + 17, 370, 8.2, MUTED, FONT, 9.8, 2)
    round_rect(c, MARGIN, 46, PAGE_W - MARGIN * 2, 38, NAVY, NAVY, 9, 1)
    draw_text(c, data["safety_title"], MARGIN + 16, 59, 11.5, GOLD, FONT_BOLD)
    draw_wrapped(c, data["safety"], MARGIN + 128, 62, PAGE_W - MARGIN * 2 - 150, 8.5, WHITE, FONT, 10.8, 2)
    footer(c, False)


def draw_cta_v4(c, data, lang):
    draw_bg(c, 12)
    cover(c, 34, 44, 430, 440)
    cover(c, 36, 20, 430, 45)
    draw_wrapped(c, data["title"], MARGIN, 430, 410, 27, WHITE, FONT_BOLD, 33)
    draw_wrapped(c, data["subtitle"], MARGIN, 372, 400, 13, colors.HexColor("#cbd8e6"), FONT, 17, 4)
    y = 236
    starts = [data["first_copy"], " -> ".join(data["paths"][:3]), data["action"]]
    labels = [data["first_label"], "Then choose" if lang == "en" else "Potom vyberte", data["action_label"]]
    acc = [GOLD, TEAL, PURPLE]
    for label, copy, color in zip(labels, starts, acc):
        round_rect(c, MARGIN, y, 405, 52, colors.HexColor("#0f2233"), colors.HexColor("#27435a"), 10, 0.8)
        draw_text(c, label, MARGIN + 14, y + 31, 9.2, color, FONT_BOLD)
        draw_wrapped(c, copy, MARGIN + 122, y + 34, 260, 8.5, colors.HexColor("#dce6f1"), FONT_BOLD if label == data["first_label"] else FONT, 10.5, 2)
        y -= 70
    round_rect(c, MARGIN, 30, 405, 34, WHITE, WHITE, 8, 1)
    draw_text(c, "Aureus Automation Lab - controlled AI automation systems", MARGIN + 12, 44, 8.5, MUTED, FONT_BOLD)


def generate_pdf(path: Path, data, use_cases, lang: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(path), pagesize=(PAGE_W, PAGE_H))
    c.setTitle(f"Aureus World Class Use Case Showcase V5 {lang.upper()}")
    draw_cover_v4(c, data["cover"], lang)
    c.showPage()
    draw_model_v4(c, data["model"])
    c.showPage()
    for page_no, item in enumerate(use_cases, 3):
        draw_use_case_v4(c, item, page_no, lang)
        c.showPage()
    draw_scorecards_v4(c, data["score"], lang)
    c.showPage()
    draw_pilot_v4(c, data["pilot"])
    c.showPage()
    draw_usage_v4(c, data["usage"])
    c.showPage()
    draw_cta_v4(c, data["cta"], lang)
    c.save()


def render_previews(pdf_path: Path, prefix: str):
    PREVIEW_DIR.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(pdf_path)
    for page_no in [0, 2, 4, 8, 11]:
        page = doc[page_no]
        pix = page.get_pixmap(matrix=fitz.Matrix(1.35, 1.35), alpha=False)
        pix.save(PREVIEW_DIR / f"{prefix}_page_{page_no + 1:02d}.png")


def main() -> int:
    render_v4_pages()
    en_path = EXPORT_DIR / "Aureus_World_Class_Use_Case_Showcase_V5_EN.pdf"
    sk_path = EXPORT_DIR / "Aureus_World_Class_Use_Case_Showcase_V5_SK.pdf"
    generate_pdf(en_path, EN, USE_CASES_EN, "en")
    generate_pdf(sk_path, SK, USE_CASES_SK, "sk")
    render_previews(en_path, "visual_en")
    render_previews(sk_path, "visual_sk")
    if DESKTOP_DIR.exists():
        for src in [en_path, sk_path]:
            (DESKTOP_DIR / src.name).write_bytes(src.read_bytes())
    print(f"Generated: {en_path}")
    print(f"Generated: {sk_path}")
    if DESKTOP_DIR.exists():
        print(f"Copied to: {DESKTOP_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
