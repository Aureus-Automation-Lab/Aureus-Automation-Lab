from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import fitz
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
EXPORT_DIR = ROOT / "exports"
PREVIEW_DIR = EXPORT_DIR / "preview_v6_pro"
CROP_DIR = EXPORT_DIR / "v6_visual_crops"

PAGE_W = 1920
PAGE_H = 1080
MARGIN = 78

BG = colors.HexColor("#07131d")
BG_2 = colors.HexColor("#0b1b29")
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
        pdfmetrics.registerFont(TTFont("Aureus", str(regular)))
        pdfmetrics.registerFont(TTFont("Aureus-Bold", str(bold)))
        return "Aureus", "Aureus-Bold"
    return "Helvetica", "Helvetica-Bold"


FONT, FONT_BOLD = register_fonts()


def sw(text: str, size: float, font: str = FONT) -> float:
    return pdfmetrics.stringWidth(text, font, size)


def txt(c: canvas.Canvas, text: str, x: float, y: float, size: float, color=INK, font: str = FONT):
    c.setFillColor(color)
    c.setFont(font, size)
    c.drawString(x, y, text)


def wrap_text(text: str, max_width: float, size: float, font: str = FONT) -> list[str]:
    lines: list[str] = []
    for para in text.split("\n"):
        words = para.split()
        if not words:
            lines.append("")
            continue
        current = ""
        for word in words:
            candidate = word if not current else f"{current} {word}"
            if sw(candidate, size, font) <= max_width:
                current = candidate
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)
    return lines


def wrapped(
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
    if leading is None:
        leading = size * 1.32
    lines = wrap_text(text, max_width, size, font)
    if max_lines is not None and len(lines) > max_lines:
        lines = lines[:max_lines]
        last = lines[-1]
        while last and sw(last + "...", size, font) > max_width:
            last = last.rsplit(" ", 1)[0] if " " in last else last[:-1]
        lines[-1] = (last or lines[-1][:8]) + "..."
    c.setFillColor(color)
    c.setFont(font, size)
    for i, line in enumerate(lines):
        c.drawString(x, y - i * leading, line)
    return y - len(lines) * leading


def round_rect(c: canvas.Canvas, x: float, y: float, w: float, h: float, fill, stroke=None, radius=22, width=1.2):
    c.saveState()
    c.setFillColor(fill)
    c.setStrokeColor(stroke or fill)
    c.setLineWidth(width)
    c.roundRect(x, y, w, h, radius, fill=1, stroke=1 if stroke else 0)
    c.restoreState()


def top_rule(c: canvas.Canvas, kicker: str, page: int, dark=True):
    color = colors.HexColor("#8fa2b7") if dark else colors.HexColor("#627386")
    txt(c, kicker, MARGIN, PAGE_H - 55, 16, color, FONT_BOLD)
    label = f"Use Case Showcase / {page:02d}"
    txt(c, label, PAGE_W - MARGIN - sw(label, 16, FONT_BOLD), PAGE_H - 55, 16, color, FONT_BOLD)
    c.setStrokeColor(colors.HexColor("#24384b") if dark else LINE)
    c.setLineWidth(1.2)
    c.line(MARGIN, PAGE_H - 74, PAGE_W - MARGIN, PAGE_H - 74)


def footer(c: canvas.Canvas, dark=True):
    color = colors.HexColor("#8fa2b7") if dark else colors.HexColor("#657588")
    txt(c, "Aureus Automation Lab - public-safe, client-ready use-case material", MARGIN, 36, 14, color)


def chip(c: canvas.Canvas, label: str, x: float, y: float, accent, dark=True) -> float:
    size = 15
    width = sw(label, size, FONT_BOLD) + 32
    fill = colors.Color(accent.red, accent.green, accent.blue, alpha=0.14 if dark else 0.10)
    round_rect(c, x, y, width, 34, fill, accent, radius=16, width=1.4)
    txt(c, label, x + 16, y + 10, size, accent, FONT_BOLD)
    return x + width + 14


def bullet_list(c: canvas.Canvas, items: list[str], x: float, y: float, w: float, color, accent, size=18, max_lines=2) -> float:
    current = y
    for item in items:
        c.setFillColor(accent)
        c.circle(x + 8, current + 5, 5.5, fill=1, stroke=0)
        current = wrapped(c, item, x + 25, current + 10, w - 25, size, color, FONT, size * 1.28, max_lines)
        current -= 10
    return current


def card(c: canvas.Canvas, x: float, y: float, w: float, h: float, title: str, body: str, accent, dark=True, max_lines=4):
    fill = PANEL if dark else colors.HexColor("#ffffff")
    stroke = LINE_DARK if dark else LINE
    title_color = WHITE if dark else INK
    body_color = SOFT if dark else MUTED
    round_rect(c, x, y, w, h, fill, stroke, radius=20, width=1.1)
    c.setFillColor(accent)
    c.rect(x, y, 8, h, fill=1, stroke=0)
    txt(c, title, x + 28, y + h - 42, 24, title_color, FONT_BOLD)
    wrapped(c, body, x + 28, y + h - 78, w - 52, 18.5, body_color, FONT, 24, max_lines)


def metric_card(c: canvas.Canvas, x: float, y: float, w: float, h: float, label: str, value: str, accent, dark=True):
    fill = PANEL if dark else colors.HexColor("#ffffff")
    stroke = LINE_DARK if dark else LINE
    round_rect(c, x, y, w, h, fill, stroke, radius=18, width=1)
    txt(c, label, x + 20, y + h - 30, 15, accent, FONT_BOLD)
    wrapped(c, value, x + 20, y + h - 62, w - 40, 20, WHITE if dark else INK, FONT_BOLD, 25, 2)


def image_frame(c: canvas.Canvas, img: Path, x: float, y: float, w: float, h: float, label: str | None = None):
    round_rect(c, x, y, w, h, colors.HexColor("#0a1622"), LINE_DARK, radius=24, width=1.2)
    c.saveState()
    p = c.beginPath()
    p.roundRect(x + 2, y + 2, w - 4, h - 4, 20)
    c.clipPath(p, stroke=0, fill=0)
    c.drawImage(str(img), x + 2, y + 2, width=w - 4, height=h - 4)
    c.restoreState()
    c.setFillColor(colors.Color(0, 0, 0, alpha=0.22))
    c.rect(x + 2, y + 2, w - 4, h - 4, fill=1, stroke=0)
    if label:
        round_rect(c, x + 22, y + h - 58, sw(label, 16, FONT_BOLD) + 34, 34, colors.Color(0.04, 0.09, 0.13, alpha=0.88), colors.HexColor("#3b5870"), 17, 0.8)
        txt(c, label, x + 39, y + h - 37, 16, WHITE, FONT_BOLD)


def fitz_crop_to_png(src_pdf: Path, page_no: int, clip: tuple[float, float, float, float], out: Path):
    doc = fitz.open(src_pdf)
    page = doc[page_no - 1]
    pix = page.get_pixmap(matrix=fitz.Matrix(1, 1), clip=fitz.Rect(*clip), alpha=False)
    out.parent.mkdir(parents=True, exist_ok=True)
    pix.save(out)


def find_v4_pdf() -> Path | None:
    candidate = ROOT / "_input" / "Aureus_World_Class_Use_Case_Showcase_v4_final.pdf"
    return candidate if candidate.exists() else None


def make_visual_crops() -> dict[int, Path]:
    src = find_v4_pdf()
    crops: dict[int, Path] = {}
    if not src:
        return crops
    # Coordinates use the source 1920x1080 PDF page grid.
    crop_map = {
        1: (1010, 105, 1810, 815),
        3: (1030, 95, 1815, 535),
        4: (955, 90, 1830, 535),
        5: (950, 88, 1830, 535),
        6: (955, 88, 1830, 535),
        7: (955, 88, 1830, 535),
        8: (955, 88, 1830, 535),
        12: (1030, 105, 1815, 760),
    }
    for page, clip in crop_map.items():
        out = CROP_DIR / f"page_{page:02d}_visual.png"
        fitz_crop_to_png(src, page, clip, out)
        crops[page] = out
    return crops


@dataclass(frozen=True)
class UseCase:
    case: str
    title: str
    promise: str
    problem: str
    ai: str
    approve: str
    evidence: str
    workflow: list[str]
    receives: list[str]
    proof: list[str]
    boundary: str
    first_step: str
    accent: object
    visual_page: int


# V7 client-language copy.
# The V6 deck was technically accurate, but too close to internal architecture language.
# These definitions intentionally replace the earlier pack/case definitions with simpler
# client-facing wording while preserving the same proof and approval boundaries.
def en_pack() -> dict:
    return {
        "lang": "en",
        "cover_title": "Aureus Use Case Portfolio",
        "cover_subtitle": "Six practical examples of how AI can remove manual work without removing human control.",
        "cover_note": "This is not a chatbot demo and not blind automation. Each example starts with a real business problem, shows what the system prepares, what a person approves, and what record remains for review.",
        "rule": "AI prepares the work. People make the decision. The record remains.",
        "model_title": "How We Choose The Right AI Use Case",
        "model_subtitle": "We do not start by asking which tool looks impressive. We start by finding work that is repeated, painful, reviewable, and useful enough to pilot safely.",
        "signals": [
            ("Repeated work", "The same task, check, rewrite, reminder, or handoff happens again and again."),
            ("Clear pain", "People lose time because information is scattered, approvals are unclear, or follow-up depends on memory."),
            ("Human decision needed", "The system can prepare the work, but a person should still approve sensitive steps."),
            ("Visible record", "The process can leave a simple record of what happened, who reviewed it, and what comes next."),
            ("Small safe pilot", "The first version can be tested on one process before it is expanded."),
        ],
        "flow": ["Find pain", "Choose first step", "Design safely", "Build pilot", "Review", "Decide next"],
        "discovery_label": "Decision flow",
        "decision_rule_label": "Decision rule",
        "decision_rule": "Start where the buyer can see the value, approve the risk, and understand the next step.",
        "score_kicker": "Client decision support",
        "score_title": "Use-Case Scorecard For Client Conversations",
        "score_subtitle": "This helps choose the first practical pilot: where the value is visible, the effort is bounded, the approval line is clear, and the next step is easy to explain.",
        "score_headers": ["Use case", "When it fits", "Pilot fit", "Proof status", "First step"],
        "score_rows": [
            ["Automation Audit", "You know work is manual, but not where to start.", "High", "Safe first step", "Map one process"],
            ["n8n Review + Build", "An automation exists, but nobody fully trusts it.", "High", "Setup-gated", "Review one workflow"],
            ["FinEcon Pilot", "Documents arrive from many places and need review.", "High", "Internal E2E / accountant pending", "Pick one document flow"],
            ["Aureus Sales Workflow", "Follow-up depends on memory and risky drafts.", "Medium", "Approval-gated", "One lead source"],
            ["Aureus OS", "AI work is scattered across people and tools.", "Medium", "Operating model", "One team area"],
            ["Public Proof Site", "The offer is hard to understand and not connected to intake.", "High", "Public-safe", "One offer page"],
        ],
        "pilot_title": "30-Day Client Pilot Path",
        "pilot_subtitle": "The goal is not to automate the whole company. The goal is to prove one useful workflow that the client understands, approves, and can inspect.",
        "weeks": [
            ("Week 1", "Understand the work", "Map the current process, who owns it, where it slows down, and what can go wrong."),
            ("Week 2", "Design the pilot", "Choose one safe workflow, define what AI prepares, and mark what must stay human-approved."),
            ("Week 3", "Build and test", "Build a controlled version with synthetic or approved examples and check the handoff."),
            ("Week 4", "Review and decide", "Review the evidence, risks, operating notes, and decide what should be built next."),
        ],
        "usage_title": "How To Use This Showcase",
        "usage_subtitle": "Use this as a client conversation tool. It explains what can be bought first, what the client receives, and what remains approval-gated.",
        "usage": [
            ("First call", "Pick the use case that sounds closest to the buyer's daily problem."),
            ("Follow-up PDF", "Send the matching page after a call so the next step feels concrete."),
            ("LinkedIn carousel", "Use the short version to teach the market what controlled AI automation means."),
            ("GitHub portfolio", "Send technical reviewers to the public proof pages and safety boundaries."),
            ("Proposal appendix", "Attach the use case, the 30-day pilot path, and the first action."),
            ("Sales follow-up", "Ask for one workflow, one document flow, or one repeated process to review."),
        ],
        "safety": "Private exports, credentials, real client data, blind sending, unsupported customer-result claims, and accounting authority claims stay out of the public material. Sensitive actions remain approval-gated.",
        "cta_title": "Best First Step: Automation Audit",
        "cta_subtitle": "Before building anything, find the first workflow that is useful, safe, and simple enough to test.",
        "cta_action": "Send one repeated process or existing workflow. We map what AI can prepare, what a person must approve, what record should remain, and which pilot makes sense.",
        "pilot_by_day_label": "By day 30",
        "pilot_out": "Process map, pilot scope, approval line, evidence example, risk list, and next decision.",
        "usage_kicker": "Public-safe usage",
        "safety_label": "Safety boundary",
        "cta_kicker": "Best first step",
        "why_label": "Why first?",
        "why_text": "It turns a vague AI idea into a clear process map, ranked options, approval line, and scoped pilot decision.",
        "path_title": "Choose the next path",
        "buyer_action_label": "Buyer action",
        "case_labels": {
            "problem": "Everyday problem",
            "ai": "What the system prepares",
            "approve": "What people approve",
            "evidence": "What stays recorded",
            "receives": "What the client gets",
            "workflow": "Simple workflow",
            "proof": "Proof and safety",
            "boundary": "Boundary",
            "first": "First action",
        },
    }


def sk_pack() -> dict:
    return {
        "lang": "sk",
        "cover_title": "Aureus Use Case Portfólio",
        "cover_subtitle": "Šesť praktických príkladov, ako môže AI odstrániť manuálnu prácu bez toho, aby zobrala kontrolu človeku.",
        "cover_note": "Nie je to chatbot demo ani slepá automatizácia. Každý príklad začína reálnym firemným problémom: čo systém pripraví, čo človek schváli a aký záznam ostane na kontrolu.",
        "rule": "AI pripraví podklady. Človek rozhodne. Záznam ostane.",
        "model_title": "Ako vyberáme správny AI use case",
        "model_subtitle": "Nezačíname otázkou, ktorý nástroj vyzerá efektne. Začíname prácou, ktorá sa opakuje, bolí firmu, dá sa skontrolovať a je vhodná na bezpečný pilot.",
        "signals": [
            ("Opakovaná práca", "Rovnaká úloha, kontrola, prepisovanie, pripomienka alebo odovzdanie sa deje stále dokola."),
            ("Jasná bolesť", "Ľudia strácajú čas, lebo informácie sú rozhádzané, schvaľovanie je nejasné alebo follow-up stojí na pamäti."),
            ("Rozhoduje človek", "Systém pripraví podklady, ale citlivý krok musí stále schváliť človek."),
            ("Viditeľný záznam", "Proces zanechá jednoduchý záznam o tom, čo sa stalo, kto to skontroloval a čo je ďalší krok."),
            ("Malý bezpečný pilot", "Prvá verzia sa otestuje na jednom procese skôr, než sa rozšíri ďalej."),
        ],
        "flow": ["Nájsť bolesť", "Vybrať prvý krok", "Navrhnúť bezpečne", "Postaviť pilot", "Skontrolovať", "Rozhodnúť ďalej"],
        "discovery_label": "Ako sa rozhodneme",
        "decision_rule_label": "Pravidlo rozhodnutia",
        "decision_rule": "Začať tam, kde klient vidí hodnotu, vie schváliť riziko a rozumie ďalšiemu kroku.",
        "score_kicker": "Pomôcka pre rozhodnutie klienta",
        "score_title": "Scorecard pre rozhovor s klientom",
        "score_subtitle": "Pomôcka na výber prvého praktického pilotu: kde je hodnota viditeľná, rozsah ohraničený, schvaľovanie jasné a ďalší krok ľahko vysvetliteľný.",
        "score_headers": ["Use case", "Kedy dáva zmysel", "Pilot fit", "Stav dôkazu", "Prvý krok"],
        "score_rows": [
            ["Automation Audit", "Viete, že práca je manuálna, ale neviete kde začať.", "Vysoký", "Bezpečný prvý krok", "Zmapovať jeden proces"],
            ["n8n Review + Build", "Automatizácia existuje, ale tím jej úplne neverí.", "Vysoký", "Setup-gated", "Skontrolovať jeden workflow"],
            ["FinEcon Pilot", "Doklady chodia z rôznych miest a potrebujú review.", "Vysoký", "Interné E2E / čaká účtovník", "Vybrať jeden tok dokladov"],
            ["Aureus Sales Workflow", "Follow-up stojí na pamäti a rizikových draftoch.", "Stredný", "Approval-gated", "Jeden zdroj leadov"],
            ["Aureus OS", "AI práca je rozhádzaná cez ľudí a nástroje.", "Stredný", "Operating model", "Jedna tímová oblasť"],
            ["Public Proof Site", "Ponuka je ťažko pochopiteľná a nenadväzuje na intake.", "Vysoký", "Public-safe", "Jedna stránka ponuky"],
        ],
        "pilot_title": "30-dňový klientsky pilot",
        "pilot_subtitle": "Cieľ nie je automatizovať celú firmu. Cieľ je dokázať jeden užitočný workflow, ktorý klient chápe, schvaľuje a vie skontrolovať.",
        "weeks": [
            ("Týždeň 1", "Pochopiť prácu", "Zmapujeme dnešný proces, kto ho vlastní, kde sa spomaľuje a čo sa môže pokaziť."),
            ("Týždeň 2", "Navrhnúť pilot", "Vyberieme jeden bezpečný workflow, určíme čo pripraví AI a čo musí zostať schválené človekom."),
            ("Týždeň 3", "Postaviť a otestovať", "Postavíme kontrolovanú verziu na syntetických alebo schválených príkladoch a overíme odovzdanie."),
            ("Týždeň 4", "Vyhodnotiť a rozhodnúť", "Prejdeme záznamy, riziká, prevádzkové poznámky a rozhodneme, čo má zmysel stavať ďalej."),
        ],
        "usage_title": "Ako používať tento showcase",
        "usage_subtitle": "Je to materiál na rozhovor s klientom. Vysvetľuje, čo sa dá kúpiť ako prvé, čo klient dostane a čo zostáva schvaľované človekom.",
        "usage": [
            ("Prvý call", "Vybrať use case, ktorý sa najviac podobá na denný problém klienta."),
            ("Follow-up PDF", "Po calle poslať konkrétnu stranu, aby bol ďalší krok jasný."),
            ("LinkedIn carousel", "Kratšou verziou vysvetliť trhu, čo znamená kontrolovaná AI automatizácia."),
            ("GitHub portfólio", "Technických reviewerov poslať na public proof stránky a bezpečnostné hranice."),
            ("Príloha k ponuke", "Pridať use case, 30-dňový pilot a prvú akciu."),
            ("Sales follow-up", "Požiadať o jeden workflow, tok dokladov alebo opakovaný proces na review."),
        ],
        "safety": "Private exporty, credentials, reálne klientské dáta, slepé odosielanie, nepodložené výsledky a tvrdenia o účtovnej autorite nepatria do verejného materiálu. Citlivé akcie zostávajú approval-gated.",
        "cta_title": "Najlepší prvý krok: Automation Audit",
        "cta_subtitle": "Pred stavbou nájdeme prvý workflow, ktorý je užitočný, bezpečný a dosť jednoduchý na otestovanie.",
        "cta_action": "Pošlite jeden proces alebo existujúci workflow. Zmapujeme, čo pripraví AI, čo schváli človek, aký záznam ostane a aký pilot dáva zmysel.",
        "pilot_by_day_label": "Do 30. dňa",
        "pilot_out": "Mapa procesu, rozsah pilotu, schvaľovacia hranica, príklad záznamu, risk list a ďalšie rozhodnutie.",
        "usage_kicker": "Verejne bezpečné použitie",
        "safety_label": "Bezpečnostná hranica",
        "cta_kicker": "Najlepší prvý krok",
        "why_label": "Prečo prvý?",
        "why_text": "Z nejasného AI nápadu vznikne mapa procesu, zoradené možnosti, schvaľovacia hranica a konkrétne rozhodnutie o pilote.",
        "path_title": "Potom vyberieme ďalšiu cestu",
        "buyer_action_label": "Akcia pre klienta",
        "case_labels": {
            "problem": "Bežný problém",
            "ai": "Čo systém pripraví",
            "approve": "Čo schváli človek",
            "evidence": "Čo ostane zaznamenané",
            "receives": "Čo klient dostane",
            "workflow": "Jednoduchý postup",
            "proof": "Dôkaz a bezpečnosť",
            "boundary": "Hranica",
            "first": "Prvý krok",
        },
    }


def en_cases() -> list[UseCase]:
    return [
        UseCase(
            "CASE 01",
            "Automation Audit",
            "Find the first useful automation before spending money on a build.",
            "The company knows some work is slow and manual, but it is not clear which process should be automated first.",
            "It sorts the current work into simple groups, finds repeated tasks, and prepares a shortlist of good automation candidates.",
            "The owner decides which process matters, which actions are sensitive, and what is safe to test first.",
            "A clear process map, candidate list, risk list, approval line, and first pilot recommendation.",
            ["Map the work", "Find repeats", "Score value", "Mark approvals", "Choose pilot"],
            ["one process map", "ranked automation ideas", "approval boundary", "pilot brief"],
            ["Safe first step", "Pilot-ready"],
            "We do not claim every task should be automated and we do not promise savings before the process is reviewed.",
            "Send one repeated process that wastes time or creates avoidable mistakes.",
            GOLD,
            3,
        ),
        UseCase(
            "CASE 02",
            "n8n Workflow Review + Build",
            "Make existing automations easier to trust, fix, and operate.",
            "A workflow may run today, but when it fails, the team does not know who owns it, what changed, or how to repair it safely.",
            "It explains the workflow in plain language, finds weak points, prepares checks, and suggests a cleaner version.",
            "The owner approves live activation, credentials, external sends, production changes, and failure handling.",
            "A review note, workflow map, failure plan, validation checklist, and handoff document.",
            ["Review flow", "Find weak points", "Define checks", "Repair/build", "Handoff"],
            ["workflow review", "failure map", "validation plan", "handoff notes"],
            ["Setup-gated", "Pilot-ready"],
            "No live activation, credential change, external send, or production action happens without approval.",
            "Share a sanitized workflow description and the failure you are most worried about.",
            BLUE,
            4,
        ),
        UseCase(
            "CASE 03",
            "Aureus FinEcon — Pocket / Bridge modules",
            "Turn messy document intake into reviewed handoff with proof.",
            "Invoices, receipts, and documents arrive in email, folders, or mobile upload. Context gets lost before accounting review.",
            "It prepares document fields, flags missing information, shows status, and prepares the Bridge handoff path.",
            "A person or accountant reviews uncertain fields, exceptions, sensitive accounting interpretation, and official handoff.",
            "Document status, review decision, Bridge readiness note, proof pack, exception list, and accountant checklist.",
            ["Pocket intake", "Status", "Review", "Bridge", "POHODA handoff", "Proof pack"],
            ["intake path", "review queue direction", "POHODA handoff model", "proof pack", "accountant checklist"],
            ["Internal E2E passed", "Accountant validation pending"],
            "FinEcon is not an accounting authority and does not provide tax or legal advice. Accountant review remains required.",
            "Choose one document flow and define what must be reviewed by a person or accountant.",
            TEAL,
            5,
        ),
        UseCase(
            "CASE 04",
            "Aureus Sales Workflow",
            "Prepare follow-up and outreach without sending blindly.",
            "Leads are forgotten, follow-ups are late, and messages become inconsistent or risky because there is no review step.",
            "It researches public context, classifies fit, drafts outreach, prepares follow-up, and summarizes replies.",
            "People approve claims, personalization, do-not-contact decisions, external messages, and every send action.",
            "Lead state, qualification note, approved draft, reply status, follow-up plan, and daily report.",
            ["Lead source", "Fit check", "Draft", "Approval", "Reply", "Report"],
            ["lead state model", "approved-message process", "reply handling", "do-not-contact boundary"],
            ["No blind send", "Pilot-ready"],
            "No message is sent without approval and no unsupported claim is generated as final truth.",
            "Start with one lead source and one approved offer message.",
            GREEN,
            6,
        ),
        UseCase(
            "CASE 05",
            "Aureus OS",
            "Make AI work organized, reviewed, and easier to hand off.",
            "AI work is spread across chats, documents, tasks, automations, and Git. Nobody has one clear mission trail.",
            "It prepares plans, research, drafts, checks, summaries, validation notes, and handoff material.",
            "People approve scope, public claims, sensitive actions, production changes, external messages, and deliverables.",
            "Mission brief, source notes, validation notes, decisions, risk list, change summary, and handoff.",
            ["Mission", "Scope", "AI work", "Validation", "Approval gate", "Handoff"],
            ["operating model", "review gates", "evidence format", "handoff discipline"],
            ["Setup-gated", "Pilot-ready"],
            "Aureus OS is the internal control engine. It is introduced when a team needs cross-tool control, not as an abstract first purchase.",
            "Name one area where AI should help but should not make the final decision.",
            PURPLE,
            7,
        ),
        UseCase(
            "CASE 06",
            "Public Proof Website + Automation",
            "Explain the offer clearly and connect it to the next action.",
            "The service exists, but the website does not explain the value clearly and does not start a useful intake process.",
            "It prepares offer copy, page structure, intake questions, buyer summaries, and follow-up material.",
            "The owner approves claims, visuals, pricing, publishing, lead routing, and external messages.",
            "Claim checklist, page map, offer menu, intake record, handoff note, and follow-up path.",
            ["Offer", "Page", "Intake", "Review", "Follow-up", "Handoff"],
            ["offer structure", "website copy direction", "intake path", "claim checklist"],
            ["Public-safe", "Pilot-ready"],
            "No fake proof, no unsupported public claims, and no publishing without approval.",
            "Send the offer, target buyer, and one question the page must answer.",
            RED,
            8,
        ),
    ]


def sk_cases() -> list[UseCase]:
    return [
        UseCase(
            "CASE 01",
            "Automation Audit",
            "Nájsť prvú užitočnú automatizáciu skôr, než sa minú peniaze na stavbu.",
            "Firma vie, že niektorá práca je pomalá a manuálna, ale nie je jasné, ktorý proces automatizovať ako prvý.",
            "Systém roztriedi dnešnú prácu, nájde opakujúce sa úlohy a pripraví krátky zoznam dobrých kandidátov.",
            "Majiteľ rozhodne, ktorý proces je dôležitý, ktoré kroky sú citlivé a čo je bezpečné otestovať ako prvé.",
            "Jasná mapa procesu, zoznam kandidátov, riziká, schvaľovacia hranica a odporúčanie prvého pilotu.",
            ["Zmapovať prácu", "Nájsť opakovania", "Ohodnotiť hodnotu", "Určiť schválenia", "Vybrať pilot"],
            ["mapa jedného procesu", "zoradené nápady", "schvaľovacia hranica", "pilot brief"],
            ["Bezpečný prvý krok", "Pilot-ready"],
            "Netvrdíme, že sa má automatizovať všetko, a nesľubujeme úspory pred tým, než proces skontrolujeme.",
            "Pošlite jeden opakovaný proces, ktorý berie čas alebo vytvára zbytočné chyby.",
            GOLD,
            3,
        ),
        UseCase(
            "CASE 02",
            "n8n Workflow Review + Build",
            "Spraviť existujúce automatizácie dôveryhodnejšie, opraviteľné a ľahšie na prevádzku.",
            "Workflow dnes možno beží, ale keď zlyhá, tím nevie, kto ho vlastní, čo sa zmenilo a ako ho bezpečne opraviť.",
            "Systém vysvetlí workflow jednoduchou rečou, nájde slabé miesta, pripraví kontroly a navrhne čistejšiu verziu.",
            "Majiteľ schvaľuje live aktiváciu, credentials, externé odosielanie, produkčné zmeny a postup pri zlyhaní.",
            "Review poznámka, mapa workflowu, plán zlyhaní, validačný checklist a handoff dokument.",
            ["Review flow", "Nájsť slabé miesta", "Určiť kontroly", "Opraviť/postaviť", "Handoff"],
            ["review workflowu", "mapa zlyhaní", "validačný plán", "handoff poznámky"],
            ["Setup-gated", "Pilot-ready"],
            "Bez schválenia sa nerobí live aktivácia, zmena credentialov, externé odoslanie ani produkčná akcia.",
            "Pošlite bezpečný opis workflowu a zlyhanie, ktorého sa najviac obávate.",
            BLUE,
            4,
        ),
        UseCase(
            "CASE 03",
            "Aureus FinEcon — Pocket / Bridge modules",
            "Zmeniť chaotický príjem dokladov na reviewované odovzdanie s dôkazom.",
            "Faktúry, bločky a dokumenty chodia cez e-mail, priečinky alebo mobil. Kontext sa stratí skôr, než príde účtovná kontrola.",
            "Systém pripraví polia dokladu, označí chýbajúce údaje, ukáže stav a pripraví cestu pre Bridge odovzdanie.",
            "Človek alebo účtovník kontroluje neisté polia, výnimky, citlivý účtovný výklad a oficiálne odovzdanie.",
            "Stav dokladu, review rozhodnutie, Bridge readiness poznámka, proof pack, zoznam výnimiek a checklist pre účtovníka.",
            ["Pocket intake", "Stav", "Review", "Bridge", "POHODA handoff", "Proof pack"],
            ["cesta príjmu dokladov", "smer review queue", "POHODA handoff model", "proof pack", "účtovnícky checklist"],
            ["Interné E2E prešlo", "Čaká účtovnícke potvrdenie"],
            "FinEcon nie je účtovná autorita a neposkytuje daňové ani právne poradenstvo. Účtovnícka kontrola zostáva potrebná.",
            "Vyberte jeden tok dokladov a určite, čo musí skontrolovať človek alebo účtovník.",
            TEAL,
            5,
        ),
        UseCase(
            "CASE 04",
            "Aureus Sales Workflow",
            "Pripraviť follow-up a outreach bez slepého odosielania.",
            "Leady sa zabúdajú, follow-up mešká a správy sú nekonzistentné alebo rizikové, lebo chýba review krok.",
            "Systém urobí research verejného kontextu, posúdi fit, pripraví outreach, follow-up a zhrnutie odpovedí.",
            "Ľudia schvaľujú claimy, personalizáciu, do-not-contact rozhodnutia, externé správy a každé odoslanie.",
            "Stav leadu, kvalifikačná poznámka, schválený draft, stav odpovede, follow-up plán a denný report.",
            ["Zdroj leadov", "Fit check", "Draft", "Approval", "Odpoveď", "Report"],
            ["lead state model", "proces schválených správ", "reply handling", "do-not-contact hranica"],
            ["Žiadne slepé odoslanie", "Pilot-ready"],
            "Žiadna správa sa neposiela bez schválenia a nepodložený claim sa nepovažuje za finálnu pravdu.",
            "Začnite jedným zdrojom leadov a jednou schválenou ponukovou správou.",
            GREEN,
            6,
        ),
        UseCase(
            "CASE 05",
            "Aureus OS",
            "Urobiť AI prácu organizovanú, reviewovanú a ľahšie odovzdateľnú.",
            "AI práca je rozhádzaná v chatoch, dokumentoch, taskoch, automatizáciách a Gite. Chýba jedna jasná stopa misie.",
            "Systém pripraví plán, research, drafty, kontroly, zhrnutia, validačné poznámky a handoff materiál.",
            "Ľudia schvaľujú scope, verejné claimy, citlivé akcie, produkčné zmeny, externé správy a deliverables.",
            "Mission brief, poznámky k zdrojom, validácia, rozhodnutia, riziká, change summary a handoff.",
            ["Misia", "Scope", "AI práca", "Validácia", "Approval gate", "Handoff"],
            ["operating model", "review gates", "formát dôkazu", "handoff disciplína"],
            ["Setup-gated", "Pilot-ready"],
            "Aureus OS je interný control engine. Dáva zmysel vtedy, keď tím potrebuje kontrolu naprieč nástrojmi.",
            "Pomenujte jednu oblasť, kde má AI pomáhať, ale nemá robiť finálne rozhodnutie.",
            PURPLE,
            7,
        ),
        UseCase(
            "CASE 06",
            "Public Proof Website + Automation",
            "Vysvetliť ponuku jasne a napojiť ju na ďalší krok.",
            "Služba existuje, ale web nevysvetľuje hodnotu jednoducho a nespúšťa užitočný intake proces.",
            "Systém pripraví text ponuky, štruktúru stránky, intake otázky, zhrnutie kupujúceho a follow-up materiál.",
            "Majiteľ schvaľuje claimy, vizuály, ceny, publikovanie, routing leadov a externé správy.",
            "Claim checklist, mapa stránky, offer menu, intake záznam, handoff poznámka a follow-up cesta.",
            ["Ponuka", "Stránka", "Intake", "Review", "Follow-up", "Handoff"],
            ["štruktúra ponuky", "smer textu webu", "intake cesta", "claim checklist"],
            ["Public-safe", "Pilot-ready"],
            "Žiadny fake proof, žiadne nepodložené verejné tvrdenia a žiadne publikovanie bez schválenia.",
            "Pošlite ponuku, cieľového kupujúceho a jednu otázku, ktorú má stránka zodpovedať.",
            RED,
            8,
        ),
    ]


def dark_page(c: canvas.Canvas):
    c.setFillColor(BG)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    c.setFillColor(colors.Color(0.02, 0.13, 0.18, alpha=0.7))
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)


def light_page(c: canvas.Canvas):
    c.setFillColor(colors.HexColor("#f5f8fb"))
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)


def draw_cover(c: canvas.Canvas, data: dict, cases: list[UseCase], crops: dict[int, Path]):
    dark_page(c)
    top_rule(c, "Aureus Automation Lab", 1, True)
    wrapped(c, data["cover_title"], MARGIN, 900, 780, 78, WHITE, FONT_BOLD, 86, 2)
    wrapped(c, data["cover_subtitle"], MARGIN, 755, 760, 30, SOFT, FONT, 39, 3)
    wrapped(c, data["cover_note"], MARGIN, 640, 760, 23, colors.HexColor("#9fb1c4"), FONT, 31, 3)
    x = MARGIN
    for label, accent in [
        ("Automation Audit", GOLD),
        ("FinEcon", TEAL),
        ("n8n Build", BLUE),
        ("Aureus Sales Workflow", GREEN),
        ("Aureus OS", PURPLE),
        ("Public Proof", RED),
    ]:
        x = chip(c, label, x, 505, accent, True)
    round_rect(c, MARGIN, 118, 770, 160, colors.HexColor("#0e2030"), LINE_DARK, 24, 1.2)
    txt(c, "Core operating rule" if data["lang"] == "en" else "Základné pravidlo", MARGIN + 34, 220, 26, GOLD, FONT_BOLD)
    wrapped(c, data["rule"], MARGIN + 34, 174, 700, 38, WHITE, FONT_BOLD, 46, 2)

    if 1 in crops:
        image_frame(c, crops[1], 1000, 550, 820, 380, "Controlled AI automation")
        mini_pages = [3, 5, 6, 7]
        for idx, page in enumerate(mini_pages):
            x0 = 1000 + (idx % 2) * 425
            y0 = 275 - (idx // 2) * 195
            image_frame(c, crops.get(page, crops[1]), x0, y0, 390, 165, cases[page - 3].title if page <= 8 else None)
    footer(c, True)


def draw_model(c: canvas.Canvas, data: dict):
    light_page(c)
    top_rule(c, "OpenAI-aligned discovery model" if data["lang"] == "en" else "Model výberu AI use case", 2, False)
    wrapped(c, data["model_title"], MARGIN, 900, 1180, 58, INK, FONT_BOLD, 66, 2)
    wrapped(c, data["model_subtitle"], MARGIN, 810, 1160, 28, MUTED, FONT, 38, 2)
    for i, (title, body) in enumerate(data["signals"]):
        x = MARGIN + (i % 3) * 590
        y = 540 if i < 3 else 330
        w = 520 if i < 3 else 810
        if i == 4:
            x = MARGIN + 860
        round_rect(c, x, y, w, 150, WHITE, LINE, 24, 1)
        txt(c, f"{i + 1:02d}", x + 28, y + 94, 34, [TEAL, GOLD, BLUE, GREEN, PURPLE][i], FONT_BOLD)
        wrapped(c, title, x + 92, y + 104, w - 120, 27, INK, FONT_BOLD, 33, 2)
        wrapped(c, body, x + 28, y + 58, w - 56, 19, MUTED, FONT, 26, 2)
    txt(c, data.get("discovery_label", "Decision flow"), MARGIN, 260, 30, INK, FONT_BOLD)
    draw_flow(c, data["flow"], MARGIN, 155, PAGE_W - MARGIN * 2, 72, False)
    round_rect(c, MARGIN, 72, PAGE_W - MARGIN * 2, 62, BG, BG, 18, 1)
    txt(c, data.get("decision_rule_label", "Decision rule"), MARGIN + 26, 94, 22, GOLD, FONT_BOLD)
    rule = data.get("decision_rule", "Start where value is visible, effort is bounded, and review responsibility is clear.")
    wrapped(c, rule, MARGIN + 245, 97, 1420, 22, WHITE, FONT, 28, 2)
    footer(c, False)


def draw_flow(c: canvas.Canvas, steps: list[str], x: float, y: float, w: float, h: float, dark=True):
    gap = 14
    box_w = (w - gap * (len(steps) - 1)) / len(steps)
    for i, step in enumerate(steps):
        bx = x + i * (box_w + gap)
        accent = [TEAL, GOLD, BLUE, GREEN, PURPLE, RED][i % 6]
        fill = PANEL if dark else WHITE
        stroke = accent
        round_rect(c, bx, y, box_w, h, fill, stroke, 18, 1.2)
        wrapped(c, step, bx + 22, y + h / 2 + 8, box_w - 44, 21, WHITE if dark else INK, FONT_BOLD, 24, 2)


def draw_use_case(c: canvas.Canvas, uc: UseCase, page: int, data: dict, crops: dict[int, Path]):
    dark_page(c)
    top_rule(c, "Aureus use case", page, True)
    labels = data["case_labels"]
    round_rect(c, MARGIN, 870, 125, 38, colors.Color(uc.accent.red, uc.accent.green, uc.accent.blue, alpha=0.12), uc.accent, 19, 1.2)
    txt(c, uc.case, MARGIN + 18, 883, 17, uc.accent, FONT_BOLD)
    title_size = 54 if len(uc.title) > 27 else 62
    title_leading = 60 if title_size < 62 else 68
    title_bottom = wrapped(c, uc.title, MARGIN, 782, 780, title_size, WHITE, FONT_BOLD, title_leading, 2)
    wrapped(c, uc.promise, MARGIN, min(704, title_bottom - 12), 760, 29, SOFT, FONT, 38, 2)

    card(c, MARGIN, 420, 760, 140, labels["problem"], uc.problem, uc.accent, True, 3)
    card(c, MARGIN, 245, 760, 145, labels["workflow"], " -> ".join(uc.workflow), uc.accent, True, 3)
    card(c, MARGIN, 70, 760, 145, labels["receives"], ", ".join(uc.receives) + ".", uc.accent, True, 4)

    if uc.visual_page in crops:
        image_frame(c, crops[uc.visual_page], 910, 610, 900, 345, uc.title)
    else:
        draw_flow(c, uc.workflow, 910, 700, 900, 82, True)

    card_w = 430
    card_h = 146
    card(c, 910, 420, card_w, card_h, labels["ai"], uc.ai, TEAL, True, 4)
    card(c, 1380, 420, card_w, card_h, labels["approve"], uc.approve, GOLD, True, 4)
    card(c, 910, 230, card_w, card_h, labels["evidence"], uc.evidence, BLUE, True, 4)
    round_rect(c, 1380, 230, card_w, card_h, PANEL, LINE_DARK, 20, 1.1)
    c.setFillColor(PURPLE)
    c.rect(1380, 230, 8, card_h, fill=1, stroke=0)
    txt(c, labels["proof"], 1408, 334, 22, WHITE, FONT_BOLD)
    x = 1408
    for item in uc.proof:
        x = chip(c, item, x, 292, uc.accent, True)
        if x > 1750:
            x = 1408
    wrapped(c, uc.boundary, 1408, 272, 360, 16.5, SOFT, FONT, 21, 3)
    round_rect(c, 910, 112, 900, 74, colors.HexColor("#f8fafc"), WHITE, 20, 1)
    txt(c, labels["first"], 938, 140, 22, INK, FONT_BOLD)
    wrapped(c, uc.first_step, 1145, 144, 625, 19, MUTED, FONT, 24, 2)
    footer(c, True)


def draw_scorecard(c: canvas.Canvas, data: dict):
    light_page(c)
    top_rule(c, data.get("score_kicker", "Client decision support"), 9, False)
    wrapped(c, data["score_title"], MARGIN, 900, 1200, 58, INK, FONT_BOLD, 66, 2)
    wrapped(c, data["score_subtitle"], MARGIN, 818, 1400, 27, MUTED, FONT, 36, 2)
    headers = data["score_headers"]
    widths = [300, 540, 175, 330, 285]
    x0 = MARGIN
    y = 702
    for header, width in zip(headers, widths):
        round_rect(c, x0, y, width, 62, BG, BG, 12, 1)
        wrapped(c, header, x0 + 18, y + 39, width - 36, 18, WHITE, FONT_BOLD, 22, 2)
        x0 += width + 12
    y -= 74
    for idx, row in enumerate(data["score_rows"]):
        x = MARGIN
        fill = WHITE if idx % 2 == 0 else colors.HexColor("#eaf1f8")
        for cell, width in zip(row, widths):
            round_rect(c, x, y, width, 58, fill, LINE, 12, 0.8)
            wrapped(c, cell, x + 18, y + 37, width - 36, 18, INK, FONT_BOLD if width == widths[0] else FONT, 22, 2)
            x += width + 12
        y -= 68
    round_rect(c, MARGIN, 78, PAGE_W - MARGIN * 2, 74, BG, BG, 18, 1)
    txt(c, "Recommended start" if data["lang"] == "en" else "Odporúčaný štart", MARGIN + 28, 106, 24, GOLD, FONT_BOLD)
    recommendation = "Automation Audit first. Then choose n8n Review, FinEcon Pilot, Aureus Sales Workflow, Aureus OS, or Public Proof Site based on the scorecard."
    if data["lang"] == "sk":
        recommendation = "Najprv Automation Audit. Potom podľa scorecardu vybrať n8n Review, FinEcon Pilot, Aureus Sales Workflow, Aureus OS alebo Public Proof Site."
    wrapped(c, recommendation, MARGIN + 305, 110, 1390, 22, WHITE, FONT, 28, 2)
    footer(c, False)


def draw_pilot(c: canvas.Canvas, data: dict):
    dark_page(c)
    top_rule(c, "Pilot path", 10, True)
    wrapped(c, data["pilot_title"], MARGIN, 892, 1200, 58, WHITE, FONT_BOLD, 66, 2)
    wrapped(c, data["pilot_subtitle"], MARGIN, 800, 1360, 28, SOFT, FONT, 38, 2)
    for i, (week, title, body) in enumerate(data["weeks"]):
        x = MARGIN + i * 455
        round_rect(c, x, 360, 395, 285, PANEL, LINE_DARK, 24, 1.1)
        txt(c, week, x + 30, 585, 26, [TEAL, GOLD, PURPLE, GREEN][i], FONT_BOLD)
        wrapped(c, title, x + 30, 525, 310, 42, WHITE, FONT_BOLD, 48, 2)
        wrapped(c, body, x + 30, 445, 320, 22, SOFT, FONT, 30, 4)
    round_rect(c, MARGIN, 142, PAGE_W - MARGIN * 2, 105, WHITE, WHITE, 24, 1)
    txt(c, data.get("pilot_by_day_label", "By day 30"), MARGIN + 34, 184, 32, INK, FONT_BOLD)
    out = data.get("pilot_out", "Process map, pilot scope, approval line, evidence example, risk list, and next decision.")
    wrapped(c, out, MARGIN + 270, 190, 1400, 24, MUTED, FONT, 31, 2)
    footer(c, True)


def draw_usage(c: canvas.Canvas, data: dict):
    light_page(c)
    top_rule(c, data.get("usage_kicker", "Public-safe usage"), 11, False)
    wrapped(c, data["usage_title"], MARGIN, 900, 1180, 58, INK, FONT_BOLD, 66, 2)
    wrapped(c, data["usage_subtitle"], MARGIN, 815, 1320, 27, MUTED, FONT, 36, 2)
    for i, (title, body) in enumerate(data["usage"]):
        x = MARGIN + (i % 3) * 590
        y = 600 - (i // 3) * 180
        accent = [TEAL, RED, BLUE, PURPLE, GOLD, GREEN][i]
        round_rect(c, x, y, 520, 130, WHITE, LINE, 22, 1)
        c.setFillColor(accent)
        c.rect(x, y, 8, 130, fill=1, stroke=0)
        txt(c, title, x + 28, y + 82, 25, INK, FONT_BOLD)
        wrapped(c, body, x + 28, y + 48, 455, 19, MUTED, FONT, 25, 3)
    round_rect(c, MARGIN, 96, PAGE_W - MARGIN * 2, 126, BG, BG, 22, 1)
    txt(c, data.get("safety_label", "Safety boundary"), MARGIN + 30, 166, 24, GOLD, FONT_BOLD)
    wrapped(c, data["safety"], MARGIN + 30, 134, PAGE_W - MARGIN * 2 - 60, 20, WHITE, FONT, 27, 3)
    footer(c, False)


def draw_cta(c: canvas.Canvas, data: dict, crops: dict[int, Path]):
    dark_page(c)
    top_rule(c, data.get("cta_kicker", "Best first step"), 12, True)
    wrapped(c, data["cta_title"], MARGIN, 892, 900, 64, WHITE, FONT_BOLD, 72, 2)
    wrapped(c, data["cta_subtitle"], MARGIN, 790, 850, 30, SOFT, FONT, 40, 2)
    round_rect(c, MARGIN, 545, 760, 142, PANEL, GOLD, 26, 1.4)
    txt(c, data.get("why_label", "Why first?"), MARGIN + 34, 628, 26, GOLD, FONT_BOLD)
    reason = data.get("why_text", "It maps the process, ranks automation candidates, defines review boundaries, and turns vague AI ideas into a scoped pilot decision.")
    wrapped(c, reason, MARGIN + 34, 588, 690, 23, WHITE, FONT, 31, 3)
    path_title = data.get("path_title", "Choose the next path")
    txt(c, path_title, MARGIN, 470, 30, WHITE, FONT_BOLD)
    paths = [
        ("FinEcon Pilot", TEAL),
        ("n8n Review + Build", BLUE),
        ("Aureus Sales Workflow", GREEN),
        ("Aureus OS Setup", PURPLE),
        ("Public Proof Site", RED),
    ]
    for i, (label, accent) in enumerate(paths):
        x = MARGIN + (i % 2) * 390
        y = 365 - (i // 2) * 92
        round_rect(c, x, y, 350, 62, PANEL, LINE_DARK, 18, 1)
        c.setFillColor(accent)
        c.circle(x + 30, y + 31, 8, fill=1, stroke=0)
        txt(c, label, x + 55, y + 22, 21, WHITE, FONT_BOLD)
    if 12 in crops:
        image_frame(c, crops[12], 940, 390, 860, 430, "Use case portfolio")
    round_rect(c, 940, 145, 860, 152, WHITE, WHITE, 26, 1)
    txt(c, data.get("buyer_action_label", "Buyer action"), 974, 236, 29, INK, FONT_BOLD)
    wrapped(c, data["cta_action"], 974, 195, 780, 23, MUTED, FONT, 31, 3)
    footer(c, True)


def generate(path: Path, data: dict, cases: list[UseCase], crops: dict[int, Path]):
    path.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(path), pagesize=(PAGE_W, PAGE_H))
    c.setTitle(f"Aureus Use Case Showcase Client Language V7 {data['lang'].upper()}")
    draw_cover(c, data, cases, crops)
    c.showPage()
    draw_model(c, data)
    c.showPage()
    for idx, uc in enumerate(cases, start=3):
        draw_use_case(c, uc, idx, data, crops)
        c.showPage()
    draw_scorecard(c, data)
    c.showPage()
    draw_pilot(c, data)
    c.showPage()
    draw_usage(c, data)
    c.showPage()
    draw_cta(c, data, crops)
    c.save()


def render_previews(pdf: Path, prefix: str):
    PREVIEW_DIR.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(pdf)
    for page_no in range(len(doc)):
        if page_no + 1 not in {1, 2, 3, 4, 5, 9, 10, 11, 12}:
            continue
        pix = doc[page_no].get_pixmap(matrix=fitz.Matrix(0.52, 0.52), alpha=False)
        pix.save(PREVIEW_DIR / f"{prefix}_page_{page_no + 1:02d}.png")


def main() -> int:
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    crops = make_visual_crops()
    en_path = EXPORT_DIR / "Aureus_Use_Case_Showcase_Client_Language_V7_EN.pdf"
    sk_path = EXPORT_DIR / "Aureus_Use_Case_Showcase_Client_Language_V7_SK.pdf"
    generate(en_path, en_pack(), en_cases(), crops)
    generate(sk_path, sk_pack(), sk_cases(), crops)
    render_previews(en_path, "v7_en")
    render_previews(sk_path, "v7_sk")
    print(f"Generated: {en_path}")
    print(f"Generated: {sk_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
