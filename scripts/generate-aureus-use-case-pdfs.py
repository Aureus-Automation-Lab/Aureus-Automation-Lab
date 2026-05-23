from __future__ import annotations

from pathlib import Path
from textwrap import wrap

import fitz
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
EXPORT_DIR = ROOT / "exports"
PREVIEW_DIR = EXPORT_DIR / "preview"
DESKTOP_DIR = Path.home() / "OneDrive" / "Počítač"

PAGE_W = 960
PAGE_H = 540
MARGIN = 36

NAVY = colors.HexColor("#07131d")
NAVY_2 = colors.HexColor("#0d1d2b")
INK = colors.HexColor("#111827")
MUTED = colors.HexColor("#5d6b7a")
LINE = colors.HexColor("#d7e0ea")
WHITE = colors.HexColor("#f8fafc")
GOLD = colors.HexColor("#e4b84f")
TEAL = colors.HexColor("#35d0c5")
BLUE = colors.HexColor("#6aa0ff")
GREEN = colors.HexColor("#54d68a")
PURPLE = colors.HexColor("#9b7cff")
RED = colors.HexColor("#ff7a63")
CARD_DARK = colors.HexColor("#0f2233")
CARD_LIGHT = colors.HexColor("#ffffff")


def register_fonts() -> tuple[str, str]:
    regular = Path("C:/Windows/Fonts/arial.ttf")
    bold = Path("C:/Windows/Fonts/arialbd.ttf")
    if regular.exists() and bold.exists():
        pdfmetrics.registerFont(TTFont("Aureus", str(regular)))
        pdfmetrics.registerFont(TTFont("Aureus-Bold", str(bold)))
        return "Aureus", "Aureus-Bold"
    return "Helvetica", "Helvetica-Bold"


FONT, FONT_BOLD = register_fonts()


def sw(text: str, size: float, font: str = FONT) -> float:
    return pdfmetrics.stringWidth(text, font, size)


def draw_text(c: canvas.Canvas, text: str, x: float, y: float, size: float, color=INK, font: str = FONT):
    c.setFillColor(color)
    c.setFont(font, size)
    c.drawString(x, y, text)


def draw_wrapped(
    c: canvas.Canvas,
    text: str,
    x: float,
    y: float,
    max_width: float,
    size: float = 12,
    color=INK,
    font: str = FONT,
    leading: float | None = None,
    max_lines: int | None = None,
) -> float:
    if leading is None:
        leading = size * 1.35
    words = text.replace("\n", " \n ").split()
    lines: list[str] = []
    current = ""
    for word in words:
        if word == "\n":
            if current:
                lines.append(current)
                current = ""
            continue
        candidate = word if not current else f"{current} {word}"
        if sw(candidate, size, font) <= max_width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    if max_lines is not None and len(lines) > max_lines:
        lines = lines[:max_lines]
        last = lines[-1]
        while sw(last + "...", size, font) > max_width and last:
            last = last.rsplit(" ", 1)[0] if " " in last else last[:-1]
        lines[-1] = last + "..."
    c.setFillColor(color)
    c.setFont(font, size)
    for idx, line in enumerate(lines):
        c.drawString(x, y - idx * leading, line)
    return y - len(lines) * leading


def round_rect(c, x, y, w, h, fill, stroke=None, radius=14, width=1):
    c.saveState()
    c.setFillColor(fill)
    c.setStrokeColor(stroke or fill)
    c.setLineWidth(width)
    c.roundRect(x, y, w, h, radius, fill=1, stroke=1 if stroke else 0)
    c.restoreState()


def chip(c, text, x, y, color, dark=True):
    size = 8.5
    pad_x = 9
    w = sw(text, size, FONT_BOLD) + pad_x * 2
    h = 17
    fill = colors.Color(color.red, color.green, color.blue, alpha=0.12 if not dark else 0.18)
    round_rect(c, x, y, w, h, fill, color, radius=8, width=0.8)
    draw_text(c, text, x + pad_x, y + 5, size, color, FONT_BOLD)
    return x + w + 7


def header(c, kicker, page, dark=True):
    color = colors.HexColor("#8ea0b4") if dark else colors.HexColor("#718094")
    draw_text(c, kicker, MARGIN, PAGE_H - 28, 8.5, color, FONT_BOLD)
    label = f"Use Case Showcase / {page:02d}"
    draw_text(c, label, PAGE_W - MARGIN - sw(label, 8.5, FONT_BOLD), PAGE_H - 28, 8.5, color, FONT_BOLD)
    c.setStrokeColor(colors.HexColor("#223449") if dark else LINE)
    c.setLineWidth(0.8)
    c.line(MARGIN, PAGE_H - 36, PAGE_W - MARGIN, PAGE_H - 36)


def footer(c, dark=True):
    color = colors.HexColor("#8ea0b4") if dark else colors.HexColor("#718094")
    draw_text(c, "Aureus Automation Lab - public-safe use-case system", MARGIN, 18, 8, color, FONT)


def bullets(c, items, x, y, max_width, color=INK, bullet_color=GOLD, size=10.5, gap=5):
    current_y = y
    for item in items:
        c.setFillColor(bullet_color)
        c.circle(x + 4, current_y + 3, 3.2, fill=1, stroke=0)
        current_y = draw_wrapped(c, item, x + 16, current_y, max_width - 16, size, color, FONT, size * 1.25)
        current_y -= gap
    return current_y


def visual_panel(c, x, y, w, h, title, steps, accent=TEAL):
    round_rect(c, x, y, w, h, colors.HexColor("#0a1825"), colors.HexColor("#27435a"), 16, 1)
    draw_text(c, title, x + 18, y + h - 26, 12, WHITE, FONT_BOLD)
    rail_y = y + h * 0.48
    c.setStrokeColor(colors.HexColor("#36566f"))
    c.setLineWidth(2)
    c.line(x + 28, rail_y, x + w - 28, rail_y)
    usable = w - 80
    step_gap = usable / max(1, len(steps) - 1)
    for i, step in enumerate(steps):
        cx = x + 40 + i * step_gap
        c.setFillColor(accent if i % 2 == 0 else GOLD)
        c.circle(cx, rail_y, 8, fill=1, stroke=0)
        round_rect(c, cx - 36, rail_y - 58, 72, 30, colors.HexColor("#102638"), colors.HexColor("#29475f"), 8, 0.7)
        draw_wrapped(c, step, cx - 30, rail_y - 39, 60, 6.8, colors.HexColor("#cbd8e6"), FONT_BOLD, 8, max_lines=2)


def flow_bar(c, steps, x, y, w, dark=True):
    gap = 8
    box_w = (w - gap * (len(steps) - 1)) / len(steps)
    for i, step in enumerate(steps):
        bx = x + i * (box_w + gap)
        fill = CARD_DARK if dark else colors.HexColor("#edf4fb")
        stroke = [TEAL, GOLD, BLUE, GREEN, PURPLE, RED][i % 6]
        round_rect(c, bx, y, box_w, 42, fill, stroke, 10, 1)
        draw_wrapped(c, step, bx + 9, y + 26, box_w - 18, 8.2, WHITE if dark else INK, FONT_BOLD, 9, max_lines=2)


def draw_cover(c, data, lang):
    c.setFillColor(NAVY)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    header(c, "Aureus Automation Lab", 1, True)
    draw_wrapped(c, data["title"], MARGIN, 438, 440, 31, WHITE, FONT_BOLD, 38)
    draw_wrapped(c, data["subtitle"], MARGIN, 360, 455, 14, colors.HexColor("#cbd8e6"), FONT, 19)
    x = MARGIN
    for label, color in data["chips"]:
        x = chip(c, label, x, 306, color)
    round_rect(c, MARGIN, 72, 430, 86, colors.HexColor("#0b1c2a"), colors.HexColor("#244259"), 15, 1)
    draw_text(c, data["rule_title"], MARGIN + 20, 126, 13, GOLD, FONT_BOLD)
    draw_wrapped(c, data["rule"], MARGIN + 20, 100, 390, 18, WHITE, FONT_BOLD, 24)
    visual_panel(c, 520, 268, 390, 165, data["visual_title"], data["visual_steps"], TEAL)
    mini_y = 214
    for idx, case in enumerate(data["cases"]):
        col = idx % 2
        row = idx // 2
        bx = 520 + col * 200
        by = mini_y - row * 58
        round_rect(c, bx, by, 185, 42, colors.HexColor("#0f2233"), colors.HexColor("#27435a"), 10, 0.8)
        draw_wrapped(c, case, bx + 12, by + 25, 160, 8.8, colors.HexColor("#dce6f1"), FONT_BOLD, 10, 2)
    footer(c, True)


def draw_model(c, data):
    c.setFillColor(colors.HexColor("#f5f8fb"))
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    header(c, data["kicker"], 2, False)
    draw_wrapped(c, data["title"], MARGIN, 438, 680, 27, INK, FONT_BOLD, 33)
    draw_wrapped(c, data["subtitle"], MARGIN, 388, 740, 13, MUTED, FONT, 18)
    x0 = MARGIN
    for i, signal in enumerate(data["signals"]):
        x = x0 + i * 176
        round_rect(c, x, 236, 160, 108, CARD_LIGHT, LINE, 13, 0.9)
        draw_text(c, f"{i + 1}", x + 14, 314, 14, [TEAL, GOLD, BLUE, GREEN, PURPLE][i], FONT_BOLD)
        draw_wrapped(c, signal["title"], x + 36, 315, 100, 11.5, INK, FONT_BOLD, 14, 2)
        draw_wrapped(c, signal["copy"], x + 14, 276, 130, 8.8, MUTED, FONT, 11, 4)
    draw_text(c, data["flow_title"], MARGIN, 181, 15, INK, FONT_BOLD)
    flow_bar(c, data["flow"], MARGIN, 122, PAGE_W - MARGIN * 2, dark=False)
    round_rect(c, MARGIN, 58, PAGE_W - MARGIN * 2, 42, NAVY, NAVY, 12, 1)
    draw_text(c, data["bottom_rule_title"], MARGIN + 18, 74, 13, GOLD, FONT_BOLD)
    draw_wrapped(c, data["bottom_rule"], MARGIN + 148, 76, PAGE_W - MARGIN * 2 - 170, 10.5, WHITE, FONT, 13, 2)
    footer(c, False)


def draw_use_case(c, data, page_no):
    c.setFillColor(NAVY)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    header(c, "Aureus use case", page_no, True)
    chip(c, data["case"], MARGIN, 410, data["accent"])
    draw_wrapped(c, data["title"], MARGIN, 375, 410, 26, WHITE, FONT_BOLD, 31, 2)
    draw_wrapped(c, data["promise"], MARGIN, 324, 420, 12.5, colors.HexColor("#cbd8e6"), FONT, 17, 3)
    card_y = 238
    card_h = 68
    sections = [
        ("Buyer problem", data["problem"]),
        ("AI prepares", data["ai"]),
        ("People approve", data["approve"]),
    ]
    for label, copy in sections:
        round_rect(c, MARGIN, card_y, 370, card_h, CARD_DARK, colors.HexColor("#234158"), 12, 0.8)
        c.setFillColor(data["accent"])
        c.rect(MARGIN, card_y, 4, card_h, fill=1, stroke=0)
        draw_text(c, label, MARGIN + 16, card_y + card_h - 22, 12, WHITE, FONT_BOLD)
        draw_wrapped(c, copy, MARGIN + 16, card_y + card_h - 43, 330, 9.2, colors.HexColor("#b9c7d7"), FONT, 11.5, 3)
        card_y -= 82
    visual_panel(c, 470, 292, 430, 150, data["visual_title"], data["workflow"], data["accent"])
    round_rect(c, 470, 184, 205, 86, colors.Color(0.05, 0.12, 0.18, alpha=0.88), colors.HexColor("#28455d"), 12, 0.8)
    draw_text(c, "Evidence remains", 486, 244, 12, WHITE, FONT_BOLD)
    draw_wrapped(c, data["evidence"], 486, 222, 174, 8.7, colors.HexColor("#cbd8e6"), FONT, 10.5, 4)
    round_rect(c, 695, 184, 205, 86, colors.Color(0.05, 0.12, 0.18, alpha=0.88), colors.HexColor("#28455d"), 12, 0.8)
    draw_text(c, "Client receives", 711, 244, 12, WHITE, FONT_BOLD)
    bullets(c, data["receives"], 711, 221, 174, colors.HexColor("#cbd8e6"), data["accent"], 8.4, 2)
    round_rect(c, 470, 82, 430, 76, colors.HexColor("#0f2233"), colors.HexColor("#27435a"), 12, 0.8)
    draw_text(c, "Proof status", 486, 132, 10.5, GOLD, FONT_BOLD)
    x = 486
    for status in data["status"]:
        x = chip(c, status, x, 104, data["accent"])
    draw_wrapped(c, data["boundary"], 486, 92, 390, 8.2, colors.HexColor("#9fb0c2"), FONT, 10, 2)
    footer(c, True)


def draw_scorecard(c, data):
    c.setFillColor(colors.HexColor("#f5f8fb"))
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    header(c, data["kicker"], 9, False)
    draw_wrapped(c, data["title"], MARGIN, 438, 760, 27, INK, FONT_BOLD, 34)
    draw_wrapped(c, data["subtitle"], MARGIN, 388, 780, 13, MUTED, FONT, 17)
    cols = data["columns"]
    rows = data["rows"]
    x = MARGIN
    y = 322
    widths = [210, 96, 96, 108, 108, 160]
    for idx, col in enumerate(cols):
        round_rect(c, x, y, widths[idx], 28, NAVY, NAVY, 7, 1)
        draw_wrapped(c, col, x + 9, y + 18, widths[idx] - 18, 8.2, WHITE, FONT_BOLD, 9, 2)
        x += widths[idx] + 7
    y -= 38
    for r, row in enumerate(rows):
        x = MARGIN
        fill = CARD_LIGHT if r % 2 == 0 else colors.HexColor("#eaf1f8")
        for idx, cell in enumerate(row):
            round_rect(c, x, y, widths[idx], 28, fill, LINE, 7, 0.6)
            draw_wrapped(c, cell, x + 9, y + 18, widths[idx] - 18, 8.8, INK, FONT_BOLD if idx == 0 else FONT, 9.5, 2)
            x += widths[idx] + 7
        y -= 34
    round_rect(c, MARGIN, 46, PAGE_W - MARGIN * 2, 42, NAVY, NAVY, 12, 1)
    draw_text(c, data["rule_label"], MARGIN + 18, 62, 13, GOLD, FONT_BOLD)
    draw_wrapped(c, data["rule"], MARGIN + 170, 64, PAGE_W - MARGIN * 2 - 195, 9.8, WHITE, FONT, 12, 2)
    footer(c, False)


def draw_pilot(c, data):
    c.setFillColor(NAVY)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    header(c, data["kicker"], 10, True)
    draw_wrapped(c, data["title"], MARGIN, 430, 780, 27, WHITE, FONT_BOLD, 34)
    draw_wrapped(c, data["subtitle"], MARGIN, 382, 780, 13, colors.HexColor("#cbd8e6"), FONT, 17)
    x = MARGIN
    for i, week in enumerate(data["weeks"]):
        w = 206
        round_rect(c, x, 206, w, 154, CARD_DARK, colors.HexColor("#27435a"), 16, 0.9)
        draw_text(c, week["week"], x + 16, 322, 14, [TEAL, GOLD, PURPLE, GREEN][i], FONT_BOLD)
        draw_wrapped(c, week["title"], x + 16, 292, 165, 18, WHITE, FONT_BOLD, 23, 2)
        draw_wrapped(c, week["copy"], x + 16, 250, 168, 9.5, colors.HexColor("#b9c7d7"), FONT, 12, 4)
        x += w + 24
    round_rect(c, MARGIN, 82, PAGE_W - MARGIN * 2, 58, WHITE, WHITE, 14, 1)
    draw_text(c, data["promise_label"], MARGIN + 18, 105, 15, INK, FONT_BOLD)
    draw_wrapped(c, data["promise"], MARGIN + 210, 108, PAGE_W - MARGIN * 2 - 235, 10.4, MUTED, FONT, 13, 2)
    footer(c, True)


def draw_usage(c, data):
    c.setFillColor(colors.HexColor("#f5f8fb"))
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    header(c, data["kicker"], 11, False)
    draw_wrapped(c, data["title"], MARGIN, 438, 760, 27, INK, FONT_BOLD, 34)
    draw_wrapped(c, data["subtitle"], MARGIN, 392, 770, 13, MUTED, FONT, 17)
    for i, item in enumerate(data["uses"]):
        col = i % 3
        row = i // 3
        x = MARGIN + col * 294
        y = 290 - row * 88
        round_rect(c, x, y, 265, 62, CARD_LIGHT, LINE, 12, 0.7)
        draw_text(c, item["title"], x + 15, y + 38, 12, INK, FONT_BOLD)
        draw_wrapped(c, item["copy"], x + 15, y + 20, 225, 8.6, MUTED, FONT, 10.5, 2)
    round_rect(c, MARGIN, 56, PAGE_W - MARGIN * 2, 64, NAVY, NAVY, 13, 1)
    draw_text(c, data["safety_title"], MARGIN + 18, 92, 13, GOLD, FONT_BOLD)
    draw_wrapped(c, data["safety"], MARGIN + 18, 72, PAGE_W - MARGIN * 2 - 36, 9.5, WHITE, FONT, 12, 3)
    footer(c, False)


def draw_cta(c, data):
    c.setFillColor(NAVY)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    header(c, data["kicker"], 12, True)
    draw_wrapped(c, data["title"], MARGIN, 420, 780, 30, WHITE, FONT_BOLD, 36)
    draw_wrapped(c, data["subtitle"], MARGIN, 362, 770, 14, colors.HexColor("#cbd8e6"), FONT, 18)
    round_rect(c, MARGIN, 238, 360, 82, colors.HexColor("#0f2233"), GOLD, 15, 1.2)
    draw_text(c, data["first_label"], MARGIN + 20, 288, 13, GOLD, FONT_BOLD)
    draw_wrapped(c, data["first_copy"], MARGIN + 20, 266, 315, 11.5, WHITE, FONT, 14, 3)
    x = 432
    y = 270
    for idx, path in enumerate(data["paths"]):
        round_rect(c, x, y, 218, 42, CARD_DARK, colors.HexColor("#27435a"), 10, 0.8)
        draw_text(c, path, x + 14, y + 17, 9.6, WHITE, FONT_BOLD)
        y -= 52
        if idx == 2:
            x = 674
            y = 270
    round_rect(c, MARGIN, 82, PAGE_W - MARGIN * 2, 78, WHITE, WHITE, 15, 1)
    draw_text(c, data["action_label"], MARGIN + 22, 122, 16, INK, FONT_BOLD)
    draw_wrapped(c, data["action"], MARGIN + 190, 124, PAGE_W - MARGIN * 2 - 220, 12, MUTED, FONT, 15, 3)
    footer(c, True)


EN = {
    "cover": {
        "title": "Aureus Use Case Portfolio",
        "subtitle": "Six controlled AI automation examples for companies that need useful work, human approval, and evidence they can review.",
        "chips": [("Automation Audit", GOLD), ("FinEcon", TEAL), ("n8n Build", BLUE), ("Sales Machine", GREEN), ("Aureus OS", PURPLE), ("Public Proof", RED)],
        "rule_title": "Core operating rule",
        "rule": "AI prepares. People approve. Evidence remains.",
        "visual_title": "Controlled AI Automation System",
        "visual_steps": ["Signal", "Mission", "Workflow", "Review", "Evidence", "Output"],
        "cases": ["Automation Audit", "n8n Workflow Review + Build", "FinEcon Pocket / Bridge", "Approval-Safe Sales Machine", "Aureus OS / AOP", "Public Proof Website + Automation"],
    },
    "model": {
        "kicker": "OpenAI-aligned discovery model",
        "title": "How We Choose The Right AI Use Case",
        "subtitle": "Good AI automation starts with a bounded business process, not with a model.",
        "signals": [
            {"title": "Repeated work", "copy": "The task happens often enough to justify a system."},
            {"title": "Skill bottleneck", "copy": "Expert time is spent sorting, checking, rewriting, or chasing."},
            {"title": "Review needed", "copy": "Ownership is unclear or the next step is sensitive."},
            {"title": "Evidence-ready", "copy": "The workflow can keep a visible record of what happened."},
            {"title": "Bounded pilot", "copy": "The first version can be tested safely before scale."},
        ],
        "flow_title": "Discovery flow",
        "flow": ["Discover", "Score", "Design", "Build", "Review", "Scale"],
        "bottom_rule_title": "Rule",
        "bottom_rule": "Start where value is visible, effort is bounded, and review responsibility is clear. Scale only after evidence exists.",
    },
    "score": {
        "kicker": "Client decision support",
        "title": "Use-Case Scorecard For Client Conversations",
        "subtitle": "We combine visible value, bounded effort, review sensitivity, proof readiness, and first-pilot fit.",
        "columns": ["Use case", "Value", "Effort", "Review", "Proof", "Best entry"],
        "rows": [
            ["Automation Audit", "High", "Low", "Low", "High", "First purchase"],
            ["n8n Review + Build", "High", "Medium", "Medium", "High", "Existing workflow"],
            ["FinEcon Pilot", "High", "Medium", "High", "Medium", "Document flow"],
            ["Sales Machine", "Medium", "Medium", "High", "High", "Lead follow-up"],
            ["Aureus OS / AOP", "High", "High", "High", "High", "Team control"],
            ["Public Proof Site", "Medium", "Medium", "Medium", "High", "Offer clarity"],
        ],
        "rule_label": "Recommendation",
        "rule": "Start with Automation Audit. Choose n8n Review for the fastest technical proof and FinEcon Pilot for finance/document workflows.",
    },
    "pilot": {
        "kicker": "Pilot path",
        "title": "30-Day Client Pilot Path",
        "subtitle": "The goal is not to automate everything. The goal is to prove one controlled workflow the client understands, approves, and can inspect.",
        "weeks": [
            {"week": "Week 1", "title": "Discovery", "copy": "Map the process, owners, inputs, exceptions, and risk points."},
            {"week": "Week 2", "title": "Design", "copy": "Define pilot scope, AI role, review boundary, and acceptance criteria."},
            {"week": "Week 3", "title": "Build + Test", "copy": "Build controlled proof with synthetic or approved examples."},
            {"week": "Week 4", "title": "Review + Handoff", "copy": "Review evidence, risk notes, handoff, and next decision."},
        ],
        "promise_label": "By day 30",
        "promise": "The client receives a process map, pilot spec, review boundary, evidence example, risk list, and next decision.",
    },
    "usage": {
        "kicker": "Public-safe usage",
        "title": "How To Use This Showcase",
        "subtitle": "Use it as a conversation tool, not as private implementation proof.",
        "uses": [
            {"title": "First call", "copy": "Choose the use case that matches the buyer's process."},
            {"title": "Follow-up PDF", "copy": "Send the relevant page after the call."},
            {"title": "LinkedIn carousel", "copy": "Publish the shorter public-safe version."},
            {"title": "GitHub portfolio", "copy": "Link to proof packages and boundaries."},
            {"title": "Proposal appendix", "copy": "Attach the use case and pilot path."},
            {"title": "Sales follow-up", "copy": "Ask for one workflow or document flow."},
        ],
        "safety_title": "Safety",
        "safety": "No private exports, no fake proof, no accounting authority claims, no blind automation, and no public claims without approval.",
    },
    "cta": {
        "kicker": "Best first step",
        "title": "Start With Automation Audit",
        "subtitle": "It is the safest first purchase because it finds the first useful workflow before building.",
        "first_label": "Why first?",
        "first_copy": "The audit maps the process, ranks candidates, defines review boundaries, and creates a pilot brief.",
        "paths": ["FinEcon Pilot", "n8n Review + Build", "Sales Machine", "Aureus OS Setup", "Public Proof Site"],
        "action_label": "Buyer action",
        "action": "Send one workflow, document flow, or repeated process you want reviewed. We will map what AI can prepare, what people approve, and what evidence remains.",
    },
}

SK = {
    "cover": {
        "title": "Aureus Use Case Portfólio",
        "subtitle": "Šesť príkladov kontrolovanej AI automatizácie pre firmy, ktoré potrebujú užitočnú prácu, ľudské schvaľovanie a dôkazový záznam.",
        "chips": [("Automation Audit", GOLD), ("FinEcon", TEAL), ("n8n Build", BLUE), ("Sales Machine", GREEN), ("Aureus OS", PURPLE), ("Public Proof", RED)],
        "rule_title": "Základné pravidlo",
        "rule": "AI pripraví. Ľudia schvália. Dôkaz zostáva.",
        "visual_title": "Kontrolovaný AI automatizačný systém",
        "visual_steps": ["Signál", "Misia", "Workflow", "Review", "Dôkaz", "Výstup"],
        "cases": ["Automation Audit", "n8n Workflow Review + Build", "FinEcon Pocket / Bridge", "Approval-Safe Sales Machine", "Aureus OS / AOP", "Public Proof Website + Automation"],
    },
    "model": {
        "kicker": "Discovery model pre AI use cases",
        "title": "Ako vyberáme správny AI use case",
        "subtitle": "Dobrý AI use case nezačína modelom. Začína ohraničeným firemným procesom.",
        "signals": [
            {"title": "Opakovaná práca", "copy": "Úloha sa deje dosť často na to, aby dávalo zmysel vytvoriť systém."},
            {"title": "Úzke miesto", "copy": "Odborný čas sa míňa na triedenie, kontrolu, prepisovanie alebo naháňanie."},
            {"title": "Treba review", "copy": "Vlastníctvo je nejasné alebo ďalší krok je citlivý."},
            {"title": "Dôkaz pripravený", "copy": "Workflow vie uchovať záznam o tom, čo sa stalo."},
            {"title": "Ohraničený pilot", "copy": "Prvá verzia sa dá bezpečne otestovať pred škálovaním."},
        ],
        "flow_title": "Discovery flow",
        "flow": ["Objaviť", "Ohodnotiť", "Navrhnúť", "Postaviť", "Skontrolovať", "Škálovať"],
        "bottom_rule_title": "Pravidlo",
        "bottom_rule": "Začať tam, kde je hodnota viditeľná, úsilie ohraničené a zodpovednosť za review jasná.",
    },
    "score": {
        "kicker": "Pomôcka pre rozhodnutie klienta",
        "title": "Scorecard pre klientsky rozhovor",
        "subtitle": "Spájame viditeľnú hodnotu, ohraničené úsilie, citlivosť review, proof readiness a vhodnosť prvého pilotu.",
        "columns": ["Use case", "Hodnota", "Úsilie", "Review", "Proof", "Najlepší vstup"],
        "rows": [
            ["Automation Audit", "Vysoká", "Nízke", "Nízke", "Vysoká", "Prvý nákup"],
            ["n8n Review + Build", "Vysoká", "Stredné", "Stredné", "Vysoká", "Existujúci workflow"],
            ["FinEcon Pilot", "Vysoká", "Stredné", "Vysoká", "Stredná", "Tok dokladov"],
            ["Sales Machine", "Stredná", "Stredné", "Vysoká", "Vysoká", "Lead follow-up"],
            ["Aureus OS / AOP", "Vysoká", "Vysoké", "Vysoká", "Vysoká", "Team control"],
            ["Public Proof Site", "Stredná", "Stredné", "Stredná", "Vysoká", "Offer clarity"],
        ],
        "rule_label": "Odporúčanie",
        "rule": "Začať s Automation Audit. n8n Review je najrýchlejší technický dôkaz a FinEcon Pilot je najsilnejší pre doklady a finance workflow.",
    },
    "pilot": {
        "kicker": "Pilot path",
        "title": "30-Dňový Klientsky Pilot",
        "subtitle": "Cieľ nie je automatizovať všetko. Cieľ je dokázať jeden kontrolovaný workflow, ktorý klient chápe, schvaľuje a vie skontrolovať.",
        "weeks": [
            {"week": "Týždeň 1", "title": "Discovery", "copy": "Zmapovať proces, vlastníkov, vstupy, výnimky a riziká."},
            {"week": "Týždeň 2", "title": "Návrh", "copy": "Definovať scope pilotu, rolu AI, schvaľovaciu hranicu a kritériá."},
            {"week": "Týždeň 3", "title": "Build + Test", "copy": "Postaviť kontrolovaný proof na syntetických alebo schválených príkladoch."},
            {"week": "Týždeň 4", "title": "Review + Handoff", "copy": "Prejsť dôkaz, riziká, handoff a ďalšie rozhodnutie."},
        ],
        "promise_label": "Do 30 dní",
        "promise": "Klient dostane mapu procesu, pilot spec, schvaľovaciu hranicu, príklad dôkazu, risk list a ďalšie rozhodnutie.",
    },
    "usage": {
        "kicker": "Verejne bezpečné použitie",
        "title": "Ako Používať Tento Showcase",
        "subtitle": "Používajte ho ako konverzačný a predajný materiál, nie ako export súkromnej implementácie.",
        "uses": [
            {"title": "Prvý call", "copy": "Vybrať use case podľa procesu kupujúceho."},
            {"title": "Follow-up PDF", "copy": "Poslať relevantnú stranu po rozhovore."},
            {"title": "LinkedIn carousel", "copy": "Publikovať kratšiu verejne bezpečnú verziu."},
            {"title": "GitHub portfólio", "copy": "Linkovať proof packages a hranice."},
            {"title": "Príloha k ponuke", "copy": "Pridať use case a pilot path."},
            {"title": "Sales follow-up", "copy": "Požiadať o jeden workflow alebo tok dokladov."},
        ],
        "safety_title": "Bezpečnosť",
        "safety": "Žiadne private exporty, fake proof, účtovná autorita, slepá automatizácia ani verejné claimy bez schválenia.",
    },
    "cta": {
        "kicker": "Najlepší prvý krok",
        "title": "Začnite s Automation Audit",
        "subtitle": "Je to najbezpečnejší prvý nákup, pretože nájde prvý užitočný workflow predtým, než sa začne stavať.",
        "first_label": "Prečo prvý?",
        "first_copy": "Audit zmapuje proces, zoradí kandidátov, definuje schvaľovacie hranice a pripraví pilot brief.",
        "paths": ["FinEcon Pilot", "n8n Review + Build", "Sales Machine", "Aureus OS Setup", "Public Proof Site"],
        "action_label": "Akcia klienta",
        "action": "Pošlite jeden workflow, tok dokladov alebo opakovaný proces. Zmapujeme, čo AI pripraví, čo ľudia schvália a aký dôkaz zostane.",
    },
}


USE_CASES_EN = [
    {
        "case": "CASE 01",
        "title": "Automation Audit",
        "promise": "Find the first useful AI automation before building.",
        "problem": "The company knows work is manual and messy, but the first useful automation is unclear.",
        "ai": "Summarizes process notes, clusters repeated work, drafts candidate workflows, and prepares impact / effort mapping.",
        "approve": "Owner confirms the process that matters, sensitive actions, manual boundaries, and safe pilot scope.",
        "evidence": "Process map, candidate list, review-boundary table, risk list, first pilot brief.",
        "workflow": ["Intake", "Map", "Score", "Boundary", "Pilot"],
        "receives": ["process map", "ranked candidates", "pilot brief"],
        "status": ["First purchase", "Pilot-ready"],
        "boundary": "No promise that every step should be automated. No promised savings.",
        "accent": GOLD,
        "visual_title": "Automation Audit outcome",
    },
    {
        "case": "CASE 02",
        "title": "n8n Workflow Review + Build",
        "promise": "Turn fragile automations into reviewable systems.",
        "problem": "A workflow may run, but the team cannot explain failure paths, ownership, credentials, retries, or handoff.",
        "ai": "Inspects workflow intent, drafts documentation, identifies weak boundaries, and prepares validation checklists.",
        "approve": "Owner approves credentials, live activation, external sends, production changes, retry behavior, and failure handling.",
        "evidence": "Risk scan, workflow map, failure-path notes, validation checklist, approval boundary.",
        "workflow": ["Trigger", "Input", "AI assist", "Validate", "Approve", "Handoff"],
        "receives": ["review notes", "failure map", "handoff docs"],
        "status": ["Setup-gated", "Pilot-ready"],
        "boundary": "No live activation or production action without explicit approval.",
        "accent": BLUE,
        "visual_title": "Reviewable workflow system",
    },
    {
        "case": "CASE 03",
        "title": "FinEcon Pocket / Bridge",
        "promise": "Move documents from intake to reviewed handoff with proof.",
        "problem": "Invoices and receipts arrive through different channels. Context gets lost and POHODA handoff is hard to inspect.",
        "ai": "Extracts candidate fields, classifies document type, flags missing information, and prepares review notes.",
        "approve": "Humans review uncertain fields, accounting-sensitive interpretation, exceptions, bridge readiness, and downstream handoff.",
        "evidence": "Document status, review decision, bridge readiness note, proof pack, exception list, accountant checklist.",
        "workflow": ["Pocket", "Status", "Review", "Bridge", "POHODA", "Proof"],
        "receives": ["intake path", "handoff model", "proof pack"],
        "status": ["Internal E2E passed", "Accountant pending"],
        "boundary": "Not accounting authority. Accountant validation remains required.",
        "accent": TEAL,
        "visual_title": "Pocket to reviewed handoff",
    },
    {
        "case": "CASE 04",
        "title": "Approval-Safe Sales Machine",
        "promise": "Prepare sales work without blind outreach.",
        "problem": "Leads and follow-ups depend on memory. Messages become inconsistent and claims can become risky.",
        "ai": "Researches public context, classifies fit, drafts outreach, drafts follow-up, and classifies replies.",
        "approve": "People approve claims, external messages, sensitive personalization, do-not-contact decisions, and sends.",
        "evidence": "Lead state, qualification note, draft message, approval status, reply classification, daily report.",
        "workflow": ["Lead", "Qualify", "Draft", "Approve", "Reply", "Report"],
        "receives": ["lead model", "approval gate", "reporting"],
        "status": ["No blind send", "Pilot-ready"],
        "boundary": "No sending without approval. No unsupported claim generation.",
        "accent": GREEN,
        "visual_title": "Approval-safe sales flow",
    },
    {
        "case": "CASE 05",
        "title": "Aureus OS / AOP",
        "promise": "Control AI-assisted work with scope, validation, approvals, evidence, and handoff.",
        "problem": "AI work is scattered across chats, docs, tasks, automations, and Git without clear owner or evidence trail.",
        "ai": "Plans, researches, drafts, inspects, summarizes, validates, and prepares handoff artifacts.",
        "approve": "People approve scope, sensitive actions, public claims, production changes, external messages, and deliverables.",
        "evidence": "Mission brief, source references, validation notes, approval decisions, risk list, handoff.",
        "workflow": ["Mission", "Scope", "AI work", "Validate", "Gate", "Handoff"],
        "receives": ["operating model", "action gates", "evidence format"],
        "status": ["Setup-gated", "Pilot-ready"],
        "boundary": "AOP is the internal control engine, not the first abstract product sold.",
        "accent": PURPLE,
        "visual_title": "AI operating control plane",
    },
    {
        "case": "CASE 06",
        "title": "Public Proof Website + Automation",
        "promise": "Turn a public offer into a proof-safe website and intake flow.",
        "problem": "The offer exists in the founder's head, but the website does not explain it or start the next operational step.",
        "ai": "Drafts offer copy, page structure, intake questions, buyer context summary, and follow-up materials.",
        "approve": "Owner approves claims, pricing, visuals, public pages, publishing, lead routing, and external messages.",
        "evidence": "Claim register, page map, offer menu, intake record, handoff note, follow-up path.",
        "workflow": ["Offer", "Page", "Intake", "Review", "Draft", "Handoff"],
        "receives": ["offer structure", "intake path", "claim checklist"],
        "status": ["Public-safe", "Pilot-ready"],
        "boundary": "No fake proof. No publishing without owner approval.",
        "accent": RED,
        "visual_title": "Public proof into operations",
    },
]

USE_CASES_SK = [
    {
        "case": "CASE 01",
        "title": "Automation Audit",
        "promise": "Nájsť prvú užitočnú AI automatizáciu pred stavbou.",
        "problem": "Firma vie, že práca je manuálna a chaotická, ale nevie, čo automatizovať ako prvé.",
        "ai": "Zhrnie poznámky z procesu, zoskupí opakovanú prácu, pripraví kandidátov a impact / effort mapu.",
        "approve": "Majiteľ potvrdí dôležitý proces, citlivé akcie, manuálne hranice a bezpečný scope pilotu.",
        "evidence": "Mapa procesu, kandidáti, schvaľovacia hranica, risk list, pilot brief.",
        "workflow": ["Intake", "Mapa", "Skóre", "Hranica", "Pilot"],
        "receives": ["mapa procesu", "kandidáti", "pilot brief"],
        "status": ["Prvý nákup", "Pilot-ready"],
        "boundary": "Netvrdíme, že každý krok sa má automatizovať. Nesľubujeme úspory.",
        "accent": GOLD,
        "visual_title": "Výstup Automation Audit",
    },
    {
        "case": "CASE 02",
        "title": "n8n Workflow Review + Build",
        "promise": "Zmeniť krehké automatizácie na reviewovateľné systémy.",
        "problem": "Workflow možno beží, ale tím nevie vysvetliť zlyhania, vlastníctvo, credentialy, retry ani handoff.",
        "ai": "Prečíta zámer workflowu, pripraví dokumentáciu, nájde slabé hranice a validačné checklisty.",
        "approve": "Majiteľ schvaľuje credentialy, live aktiváciu, externé odoslanie, produkčné zmeny a failure handling.",
        "evidence": "Risk scan, mapa workflowu, failure notes, validačný checklist, approval boundary.",
        "workflow": ["Trigger", "Input", "AI krok", "Validácia", "Approval", "Handoff"],
        "receives": ["review notes", "failure mapa", "handoff docs"],
        "status": ["Setup-gated", "Pilot-ready"],
        "boundary": "Žiadna live aktivácia ani produkčná akcia bez explicitného schválenia.",
        "accent": BLUE,
        "visual_title": "Reviewovateľný workflow systém",
    },
    {
        "case": "CASE 03",
        "title": "FinEcon Pocket / Bridge",
        "promise": "Presunúť doklady od vstupu po kontrolované odovzdanie s dôkazom.",
        "problem": "Faktúry a bločky prichádzajú rôznymi kanálmi. Kontext sa stráca a POHODA handoff sa ťažko kontroluje.",
        "ai": "Vytiahne kandidátske polia, klasifikuje doklad, označí chýbajúce údaje a pripraví review poznámky.",
        "approve": "Ľudia kontrolujú neisté polia, účtovne citlivý výklad, výnimky, Bridge readiness a downstream handoff.",
        "evidence": "Stav dokladu, review rozhodnutie, bridge readiness, proof pack, výnimky, checklist účtovníka.",
        "workflow": ["Pocket", "Stav", "Review", "Bridge", "POHODA", "Dôkaz"],
        "receives": ["intake path", "handoff model", "proof pack"],
        "status": ["Interné E2E prešlo", "Účtovník čaká"],
        "boundary": "Nie je účtovná autorita. Účtovnícke potvrdenie zostáva povinné.",
        "accent": TEAL,
        "visual_title": "Pocket po kontrolované odovzdanie",
    },
    {
        "case": "CASE 04",
        "title": "Approval-Safe Sales Machine",
        "promise": "Pripraviť predajnú prácu bez slepého outreachu.",
        "problem": "Leady a follow-up závisia od pamäte. Správy sú nekonzistentné a claimy môžu byť rizikové.",
        "ai": "Robí research, klasifikuje fit, pripraví outreach, follow-up a reply classification.",
        "approve": "Ľudia schvaľujú claimy, externé správy, personalizáciu, do-not-contact a samotné odoslanie.",
        "evidence": "Lead state, qualification note, draft správa, approval status, reply classification, report.",
        "workflow": ["Lead", "Fit", "Draft", "Approval", "Reply", "Report"],
        "receives": ["lead model", "approval gate", "reporting"],
        "status": ["No blind send", "Pilot-ready"],
        "boundary": "Žiadne odoslanie bez approval. Žiadne nepodložené claimy.",
        "accent": GREEN,
        "visual_title": "Approval-safe sales flow",
    },
    {
        "case": "CASE 05",
        "title": "Aureus OS / AOP",
        "promise": "Riadiť AI prácu cez scope, validáciu, approval, dôkaz a handoff.",
        "problem": "AI práca je roztrúsená v chatoch, dokumentoch, taskoch, automatizáciách a Gite bez vlastníka a dôkazu.",
        "ai": "Plánuje, robí research, draftuje, kontroluje, sumarizuje, validuje a pripravuje handoff.",
        "approve": "Ľudia schvaľujú scope, citlivé akcie, verejné claimy, produkčné zmeny, externé správy a deliverables.",
        "evidence": "Mission brief, zdroje, validačné notes, approval decisions, risk list, handoff.",
        "workflow": ["Misia", "Scope", "AI práca", "Validácia", "Gate", "Handoff"],
        "receives": ["operating model", "action gates", "dôkazový formát"],
        "status": ["Setup-gated", "Pilot-ready"],
        "boundary": "AOP je interný control engine, nie prvý abstraktný produkt na predaj.",
        "accent": PURPLE,
        "visual_title": "AI operating control plane",
    },
    {
        "case": "CASE 06",
        "title": "Public Proof Website + Automation",
        "promise": "Prepojiť verejnú ponuku s proof-safe webom a intake flow.",
        "problem": "Ponuka existuje v hlave foundera, ale web ju nevysvetľuje a nespúšťa ďalší operatívny krok.",
        "ai": "Pripraví offer copy, štruktúru stránok, intake otázky, buyer context a follow-up materiály.",
        "approve": "Majiteľ schvaľuje claimy, pricing, vizuály, verejné stránky, publishing, routing a externé správy.",
        "evidence": "Claim register, page map, offer menu, intake record, handoff note, follow-up path.",
        "workflow": ["Offer", "Page", "Intake", "Review", "Draft", "Handoff"],
        "receives": ["offer structure", "intake path", "claim checklist"],
        "status": ["Public-safe", "Pilot-ready"],
        "boundary": "Žiadny fake proof. Žiadne publikovanie bez approval vlastníka.",
        "accent": RED,
        "visual_title": "Public proof do operácie",
    },
]


def generate_pdf(path: Path, data, use_cases, lang: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(path), pagesize=(PAGE_W, PAGE_H))
    c.setTitle(f"Aureus Use Case Showcase V5 {lang.upper()}")
    draw_cover(c, data["cover"], lang)
    c.showPage()
    draw_model(c, data["model"])
    c.showPage()
    for idx, use_case in enumerate(use_cases, start=3):
        draw_use_case(c, use_case, idx)
        c.showPage()
    draw_scorecard(c, data["score"])
    c.showPage()
    draw_pilot(c, data["pilot"])
    c.showPage()
    draw_usage(c, data["usage"])
    c.showPage()
    draw_cta(c, data["cta"])
    c.save()


def render_previews(pdf_path: Path, prefix: str):
    PREVIEW_DIR.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(pdf_path)
    for page_no in [0, 2, 4, 8, 11]:
        if page_no >= len(doc):
            continue
        page = doc[page_no]
        pix = page.get_pixmap(matrix=fitz.Matrix(1.35, 1.35), alpha=False)
        pix.save(PREVIEW_DIR / f"{prefix}_page_{page_no + 1:02d}.png")


def main() -> int:
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    en_path = EXPORT_DIR / "Aureus_Use_Case_Showcase_V5_EN.pdf"
    sk_path = EXPORT_DIR / "Aureus_Use_Case_Showcase_V5_SK.pdf"
    generate_pdf(en_path, EN, USE_CASES_EN, "en")
    generate_pdf(sk_path, SK, USE_CASES_SK, "sk")
    render_previews(en_path, "en")
    render_previews(sk_path, "sk")
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
