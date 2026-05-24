from __future__ import annotations

import shutil
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
    candidates = [
        ROOT / "_input" / "Aureus_World_Class_Use_Case_Showcase_v4_final.pdf",
        Path.home() / "OneDrive" / "Počítač" / "Aureus_World_Class_Use_Case_Showcase_v4_final.pdf",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    for candidate in Path.home().rglob("Aureus_World_Class_Use_Case_Showcase_v4_final.pdf"):
        return candidate
    return None


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


def desktop_dir() -> Path | None:
    candidates = [
        Path.home() / "OneDrive" / "Počítač",
        Path.home() / "OneDrive" / "Desktop",
        Path.home() / "Desktop",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


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


def en_pack() -> dict:
    return {
        "lang": "en",
        "cover_title": "Aureus Use Case Portfolio",
        "cover_subtitle": "Six controlled AI automation examples for companies that need useful work, human approval, and evidence they can review.",
        "cover_note": "Not chatbot demos. Not blind automation. Each use case starts with a business process, then adds AI only where review and evidence can stay visible.",
        "rule": "AI prepares. People approve. Evidence remains.",
        "model_title": "How We Choose The Right AI Use Case",
        "model_subtitle": "The best AI use cases are not the flashiest. They are repeated, bounded, reviewable, and close to a real business decision.",
        "signals": [
            ("Repeated work", "The task happens often enough to justify a system."),
            ("Skill bottleneck", "Expert time is spent sorting, checking, rewriting, or chasing."),
            ("Sensitive decision", "Ownership is unclear or the next step affects customers, money, records, or public claims."),
            ("Evidence-ready", "The workflow can keep a visible record of what happened and what was approved."),
            ("Bounded pilot", "The first version can be tested safely before scale."),
        ],
        "flow": ["Discover", "Score", "Design", "Build", "Review", "Scale"],
        "score_title": "Client Use-Case Scorecard",
        "score_subtitle": "A practical way to choose the first pilot: visible value, bounded effort, review sensitivity, proof readiness, and first-pilot fit.",
        "score_headers": ["Use case", "Best buyer signal", "Pilot fit", "Proof status", "Entry action"],
        "score_rows": [
            ["Automation Audit", "Work is manual, but the first build is unclear.", "High", "Public-safe / pilot-ready", "First purchase"],
            ["n8n Review + Build", "A workflow runs, but trust and handoff are weak.", "High", "Setup-gated", "Review existing workflow"],
            ["FinEcon Pilot", "Documents need reviewed intake and handoff.", "High", "Internal E2E / accountant pending", "Pick one document flow"],
            ["Sales Machine", "Follow-up depends on memory and risky drafts.", "Medium", "Approval-gated", "One lead source"],
            ["Aureus OS / AOP", "AI work is scattered across people and tools.", "Medium", "Operating model", "One team area"],
            ["Public Proof Site", "The offer is unclear and not connected to intake.", "High", "Public-safe", "One offer page"],
        ],
        "pilot_title": "30-Day Client Pilot Path",
        "pilot_subtitle": "The goal is not to automate everything. The goal is to prove one controlled workflow the client understands, approves, and can inspect.",
        "weeks": [
            ("Week 1", "Discovery", "Map the real process, owners, inputs, exceptions, and risk points."),
            ("Week 2", "Pilot design", "Define scope, AI role, review boundary, proof model, and acceptance criteria."),
            ("Week 3", "Build and test", "Build a controlled proof with synthetic or approved examples. Validate the handoff."),
            ("Week 4", "Review and handoff", "Review evidence, risks, operating notes, and the next decision."),
        ],
        "usage_title": "How To Use This Showcase",
        "usage_subtitle": "Use it as a client conversation tool. It explains what can be bought first and what remains approval-gated.",
        "usage": [
            ("First call", "Choose the use case that matches the buyer's real process."),
            ("Follow-up PDF", "Send the relevant page after a call to make the next step concrete."),
            ("LinkedIn carousel", "Use the shorter public-safe version for awareness and education."),
            ("GitHub portfolio", "Point technical reviewers to proof packages and boundaries."),
            ("Proposal appendix", "Attach the relevant use case and 30-day pilot path."),
            ("Sales follow-up", "Ask for one workflow, one document flow, or one repeated process."),
        ],
        "safety": "No private exports, no fake proof, no accounting authority claims, no blind automation, no customer-results claims without separate evidence, and no public claims without approval.",
        "cta_title": "Best First Step: Automation Audit",
        "cta_subtitle": "Start by finding the first useful workflow before spending money on a build.",
        "cta_action": "Send one workflow, document flow, or repeated process. We map what AI can prepare, what people must approve, and what evidence should remain.",
        "case_labels": {
            "problem": "Buyer problem",
            "ai": "AI prepares",
            "approve": "People approve",
            "evidence": "Evidence remains",
            "receives": "Client receives",
            "workflow": "Controlled workflow",
            "proof": "Proof status",
            "boundary": "Boundary",
            "first": "Best first step",
        },
    }


def sk_pack() -> dict:
    return {
        "lang": "sk",
        "cover_title": "Aureus Use Case Portfólio",
        "cover_subtitle": "Šesť príkladov kontrolovanej AI automatizácie pre firmy, ktoré potrebujú užitočnú prácu, ľudské schválenie a dôkazový záznam.",
        "cover_note": "Nie sú to chatbot demo ukážky. Nie je to slepá automatizácia. Každý use case začína firemným procesom a AI sa pridáva až tam, kde zostáva review a dôkaz.",
        "rule": "AI pripraví. Ľudia schvália. Dôkaz zostáva.",
        "model_title": "Ako vyberáme správny AI use case",
        "model_subtitle": "Najlepšie AI use cases nie sú najefektnejšie. Sú opakované, ohraničené, reviewovateľné a blízko k reálnemu firemnému rozhodnutiu.",
        "signals": [
            ("Opakovaná práca", "Úloha sa deje dosť často na to, aby dávalo zmysel vytvoriť systém."),
            ("Úzke miesto", "Odborný čas sa míňa na triedenie, kontrolu, prepisovanie alebo naháňanie."),
            ("Citlivé rozhodnutie", "Vlastník nie je jasný alebo ďalší krok ovplyvňuje klienta, peniaze, záznamy alebo verejné tvrdenia."),
            ("Pripravené na dôkaz", "Workflow vie uchovať viditeľný záznam o tom, čo sa stalo a čo bolo schválené."),
            ("Ohraničený pilot", "Prvá verzia sa dá bezpečne otestovať pred škálovaním."),
        ],
        "flow": ["Objaviť", "Ohodnotiť", "Navrhnúť", "Postaviť", "Skontrolovať", "Škálovať"],
        "score_title": "Scorecard pre klientsky rozhovor",
        "score_subtitle": "Praktický spôsob, ako vybrať prvý pilot: viditeľná hodnota, ohraničené úsilie, citlivosť review, pripravenosť dôkazu a vhodnosť prvého pilotu.",
        "score_headers": ["Use case", "Najlepší signál klienta", "Pilot fit", "Stav dôkazu", "Vstup"],
        "score_rows": [
            ["Automation Audit", "Práca je manuálna, ale prvá stavba nie je jasná.", "Vysoký", "Public-safe / pilot-ready", "Prvý nákup"],
            ["n8n Review + Build", "Workflow beží, ale dôvera a handoff sú slabé.", "Vysoký", "Setup-gated", "Review workflowu"],
            ["FinEcon Pilot", "Doklady potrebujú reviewovaný vstup a odovzdanie.", "Vysoký", "Interné E2E / čaká účtovník", "Jeden tok dokladov"],
            ["Sales Machine", "Follow-up stojí na pamäti a rizikových draftoch.", "Stredný", "Approval-gated", "Jeden lead source"],
            ["Aureus OS / AOP", "AI práca je roztrúsená cez ľudí a nástroje.", "Stredný", "Operating model", "Jedna tímová oblasť"],
            ["Public Proof Site", "Ponuka je nejasná a nie je napojená na intake.", "Vysoký", "Public-safe", "Jedna offer page"],
        ],
        "pilot_title": "30-dňový klientsky pilot",
        "pilot_subtitle": "Cieľ nie je automatizovať všetko. Cieľ je dokázať jeden kontrolovaný workflow, ktorý klient chápe, schvaľuje a vie skontrolovať.",
        "weeks": [
            ("Týždeň 1", "Discovery", "Zmapovať reálny proces, vlastníkov, vstupy, výnimky a rizikové body."),
            ("Týždeň 2", "Návrh pilotu", "Definovať scope, rolu AI, schvaľovaciu hranicu, dôkazový model a kritériá."),
            ("Týždeň 3", "Build a test", "Postaviť kontrolovaný proof na syntetických alebo schválených príkladoch. Overiť handoff."),
            ("Týždeň 4", "Review a handoff", "Prejsť dôkaz, riziká, prevádzkové poznámky a ďalšie rozhodnutie."),
        ],
        "usage_title": "Ako používať tento showcase",
        "usage_subtitle": "Používa sa ako klientsky rozhovorový materiál. Vysvetlí, čo sa dá kúpiť ako prvé a čo zostáva approval-gated.",
        "usage": [
            ("Prvý call", "Vybrať use case podľa reálneho procesu kupujúceho."),
            ("Follow-up PDF", "Poslať relevantnú stranu po calle, aby bol ďalší krok konkrétny."),
            ("LinkedIn carousel", "Použiť kratšiu public-safe verziu na edukáciu a dopyt."),
            ("GitHub portfólio", "Technických reviewerov poslať na proof packages a hranice."),
            ("Príloha k ponuke", "Pridať relevantný use case a 30-dňový pilot path."),
            ("Sales follow-up", "Požiadať o jeden workflow, tok dokladov alebo opakovaný proces."),
        ],
        "safety": "Žiadne private exporty, žiadny fake proof, žiadne tvrdenie o účtovnej autorite, žiadna slepá automatizácia, žiadne customer-results tvrdenia bez samostatného dôkazu a žiadne verejné claimy bez approval.",
        "cta_title": "Najlepší prvý krok: Automation Audit",
        "cta_subtitle": "Začnite tým, že nájdeme prvý užitočný workflow ešte predtým, než sa minú peniaze na stavbu.",
        "cta_action": "Pošlite jeden workflow, tok dokladov alebo opakovaný proces. Zmapujeme, čo môže pripraviť AI, čo musia schváliť ľudia a aký dôkaz má zostať.",
        "case_labels": {
            "problem": "Problém klienta",
            "ai": "AI pripraví",
            "approve": "Ľudia schvália",
            "evidence": "Dôkaz zostáva",
            "receives": "Čo klient dostane",
            "workflow": "Kontrolovaný workflow",
            "proof": "Stav dôkazu",
            "boundary": "Hranica",
            "first": "Najlepší prvý krok",
        },
    }


def en_cases() -> list[UseCase]:
    return [
        UseCase(
            "CASE 01",
            "Automation Audit",
            "Find the first useful AI automation before building.",
            "A company knows work is manual and messy, but the first useful automation is unclear.",
            "Summarizes process notes, clusters repeated work, drafts candidate workflows, and prepares an impact / effort view.",
            "The owner confirms which process matters, which actions are sensitive, and what a safe first pilot can include.",
            "Process map, candidate list, review boundary, risk list, pilot brief, and next-step recommendation.",
            ["Intake", "Process map", "Score", "Review boundary", "Pilot brief"],
            ["process map", "ranked candidates", "review boundary", "pilot recommendation"],
            ["First purchase", "Pilot-ready"],
            "No promise that every step should be automated. No promised savings.",
            "Send one repeated process that wastes time or creates avoidable mistakes.",
            GOLD,
            3,
        ),
        UseCase(
            "CASE 02",
            "n8n Workflow Review + Build",
            "Turn fragile automations into reviewable systems people can operate.",
            "A workflow may run, but the team cannot explain failure paths, ownership, credentials, retries, live actions, or handoff.",
            "Inspects workflow intent, drafts documentation, identifies weak boundaries, and prepares validation checklists.",
            "The owner approves credential handling, live activation, external sends, production changes, retry behavior, and failure handling.",
            "Risk scan, workflow map, failure-path notes, validation checklist, approval boundary, and handoff note.",
            ["Trigger", "Input contract", "AI assist", "Validation", "Approval", "Handoff"],
            ["workflow review notes", "failure map", "validation plan", "handoff documentation"],
            ["Setup-gated", "Pilot-ready"],
            "No live activation, credential change, external send, or production action without explicit approval.",
            "Share a sanitized workflow description and the failure you are most worried about.",
            BLUE,
            4,
        ),
        UseCase(
            "CASE 03",
            "FinEcon Pocket / Bridge",
            "Move documents from intake to reviewed POHODA handoff with proof.",
            "Invoices, receipts, and documents arrive through different channels. Context gets lost and the accounting-system handoff becomes hard to inspect.",
            "Extracts candidate fields, classifies document type, flags missing information, and prepares review notes and downstream handoff data.",
            "People review uncertain fields, accounting-sensitive interpretation, exceptions, Bridge readiness, and official-record handoff.",
            "Document status, review decision, Bridge readiness note, proof pack, exception list, and accountant checklist.",
            ["Pocket intake", "Status", "Review action", "Bridge start", "POHODA preflight", "Proof pack"],
            ["document intake path", "review queue direction", "POHODA handoff model", "proof pack", "accountant checklist"],
            ["Internal E2E passed", "Accountant validation pending"],
            "Not accounting authority. Not tax or legal advice. Accountant validation remains required.",
            "Choose one document flow and define what a person or accountant must approve.",
            TEAL,
            5,
        ),
        UseCase(
            "CASE 04",
            "Approval-Safe Sales Machine",
            "Prepare sales work without blind outreach.",
            "Leads and follow-ups depend on memory. Messages become inconsistent, claims can become risky, and no one knows what needs review.",
            "Researches public context, classifies fit, drafts outreach and follow-up, and classifies replies.",
            "People approve claims, external messages, sensitive personalization, do-not-contact decisions, and any send action.",
            "Lead state, qualification note, draft message, approval status, reply classification, follow-up plan, and daily report.",
            ["Lead source", "Qualification", "Draft", "Approval", "Reply", "Report"],
            ["lead state model", "approved-message workflow", "reply handling", "do-not-contact boundary"],
            ["No blind send", "Pilot-ready"],
            "No sending without approval. No unsupported claim generation.",
            "Start with one lead source and one approved offer message.",
            GREEN,
            6,
        ),
        UseCase(
            "CASE 05",
            "Aureus OS / AOP",
            "Control AI-assisted work with scope, validation, approval, evidence, and handoff.",
            "AI work is scattered across chats, docs, tasks, automations, and Git without a clear mission, owner, or evidence trail.",
            "Plans, researches, drafts, inspects, summarizes, validates, and prepares handoff artifacts.",
            "People approve scope, sensitive actions, public claims, production changes, external messages, financial handoffs, and deliverables.",
            "Mission brief, source references, validation notes, approval decisions, change summary, risk list, and handoff.",
            ["Mission", "Scope", "AI work", "Validation", "Action gate", "Handoff"],
            ["operating model", "review gates", "evidence format", "handoff discipline"],
            ["Setup-gated", "Pilot-ready"],
            "AOP is the internal control engine, not the first abstract product sold.",
            "Name one area where AI should help but should not act as final authority.",
            PURPLE,
            7,
        ),
        UseCase(
            "CASE 06",
            "Public Proof Website + Automation",
            "Turn a public offer into a proof-safe website and intake flow.",
            "The offer exists in the founder's head, but the website does not explain it clearly and does not start the next operational step.",
            "Drafts offer copy, page structure, intake questions, buyer context summaries, and follow-up materials.",
            "The owner approves claims, pricing, visuals, public pages, publishing, lead routing, and external messages.",
            "Claim register, page map, offer menu, intake record, handoff note, and follow-up path.",
            ["Offer", "Public page", "Intake", "Review", "Follow-up draft", "Handoff"],
            ["offer structure", "website copy direction", "intake path", "claim checklist"],
            ["Public-safe", "Pilot-ready"],
            "No fake proof. No unsupported claims. No publishing without owner approval.",
            "Send the offer, target buyer, and one client question the page must answer.",
            RED,
            8,
        ),
    ]


def sk_cases() -> list[UseCase]:
    return [
        UseCase(
            "CASE 01",
            "Automation Audit",
            "Nájsť prvú užitočnú AI automatizáciu ešte pred stavbou.",
            "Firma vie, že práca je manuálna a chaotická, ale nevie, čo automatizovať ako prvé.",
            "Zhrnie poznámky z procesu, zoskupí opakovanú prácu, pripraví kandidátov a impact / effort pohľad.",
            "Majiteľ potvrdí, ktorý proces je dôležitý, ktoré akcie sú citlivé a čo môže patriť do bezpečného pilotu.",
            "Mapa procesu, kandidáti, schvaľovacia hranica, risk list, pilot brief a odporúčanie ďalšieho kroku.",
            ["Intake", "Mapa procesu", "Skóre", "Schvaľovacia hranica", "Pilot brief"],
            ["mapa procesu", "zoradení kandidáti", "schvaľovacia hranica", "odporúčanie pilotu"],
            ["Prvý nákup", "Pilot-ready"],
            "Netvrdíme, že každý krok sa má automatizovať. Nesľubujeme úspory.",
            "Pošlite jeden opakovaný proces, ktorý míňa čas alebo vytvára chyby.",
            GOLD,
            3,
        ),
        UseCase(
            "CASE 02",
            "n8n Workflow Review + Build",
            "Zmeniť krehké automatizácie na reviewovateľné systémy.",
            "Workflow možno beží, ale tím nevie vysvetliť zlyhania, vlastníctvo, credentialy, retry, live akcie alebo handoff.",
            "Prečíta zámer workflowu, pripraví dokumentáciu, nájde slabé hranice a validačné checklisty.",
            "Majiteľ schvaľuje credential handling, live aktiváciu, externé odoslanie, produkčné zmeny, retry a failure handling.",
            "Risk scan, mapa workflowu, failure-path poznámky, validačný checklist, approval boundary a handoff note.",
            ["Trigger", "Input contract", "AI assist", "Validácia", "Approval", "Handoff"],
            ["review poznámky", "mapa zlyhaní", "validačný plán", "handoff dokumentácia"],
            ["Setup-gated", "Pilot-ready"],
            "Žiadna live aktivácia, zmena credentialov, externé odoslanie ani produkčná akcia bez schválenia.",
            "Pošlite sanitizovaný opis workflowu a zlyhanie, ktorého sa najviac obávate.",
            BLUE,
            4,
        ),
        UseCase(
            "CASE 03",
            "FinEcon Pocket / Bridge",
            "Presunúť doklady od vstupu po reviewované POHODA odovzdanie s dôkazom.",
            "Faktúry, bločky a doklady prichádzajú rôznymi kanálmi. Kontext sa stráca a odovzdanie do účtovníckeho systému sa ťažko kontroluje.",
            "Vytiahne kandidátske polia, klasifikuje typ dokladu, označí chýbajúce údaje a pripraví review aj handoff dáta.",
            "Ľudia kontrolujú neisté polia, účtovne citlivý výklad, výnimky, Bridge readiness a odovzdanie do oficiálnych záznamov.",
            "Stav dokladu, review rozhodnutie, Bridge readiness, proof pack, výnimky a checklist pre účtovníka.",
            ["Pocket intake", "Stav", "Review action", "Bridge start", "POHODA preflight", "Proof pack"],
            ["cesta vstupu dokladov", "review queue", "POHODA handoff model", "proof pack", "checklist účtovníka"],
            ["Interné E2E prešlo", "Čaká účtovnícke potvrdenie"],
            "Nie je účtovná autorita. Nie je daňové ani právne poradenstvo. Účtovnícke potvrdenie zostáva potrebné.",
            "Vyberte jeden tok dokladov a určite, čo musí schváliť človek alebo účtovník.",
            TEAL,
            5,
        ),
        UseCase(
            "CASE 04",
            "Approval-Safe Sales Machine",
            "Pripraviť sales prácu bez slepého outreachu.",
            "Leady a follow-up stoja na pamäti. Správy sú nekonzistentné, claimy môžu byť rizikové a nie je jasné, čo potrebuje review.",
            "Robí research verejného kontextu, klasifikuje fit, pripraví outreach, follow-up a reply classification.",
            "Ľudia schvaľujú claimy, externé správy, citlivú personalizáciu, do-not-contact a samotné odoslanie.",
            "Lead state, qualification note, draft správa, approval status, reply classification, follow-up plán a report.",
            ["Lead source", "Qualification", "Draft", "Approval", "Reply", "Report"],
            ["lead state model", "workflow schválených správ", "reply handling", "do-not-contact hranica"],
            ["No blind send", "Pilot-ready"],
            "Žiadne odoslanie bez approval. Žiadne generovanie nepodložených claimov.",
            "Začnite jedným lead source a jednou schválenou offer message.",
            GREEN,
            6,
        ),
        UseCase(
            "CASE 05",
            "Aureus OS / AOP",
            "Riadiť AI-asistovanú prácu cez scope, validáciu, approval, dôkaz a handoff.",
            "AI práca je roztrúsená v chatoch, dokumentoch, taskoch, automatizáciách a Gite bez jasnej misie, vlastníka alebo dôkazu.",
            "Plánuje, robí research, draftuje, kontroluje, sumarizuje, validuje a pripravuje handoff artefakty.",
            "Ľudia schvaľujú scope, citlivé akcie, verejné claimy, produkčné zmeny, externé správy, finančné handoffy a deliverables.",
            "Mission brief, zdroje, validačné poznámky, approval decisions, change summary, risk list a handoff.",
            ["Misia", "Scope", "AI práca", "Validácia", "Action gate", "Handoff"],
            ["operating model", "review gates", "formát dôkazu", "handoff disciplína"],
            ["Setup-gated", "Pilot-ready"],
            "AOP je interný control engine, nie prvý abstraktný produkt na predaj.",
            "Pomenujte jednu oblasť, kde má AI pomôcť, ale nemá byť finálnou autoritou.",
            PURPLE,
            7,
        ),
        UseCase(
            "CASE 06",
            "Public Proof Website + Automation",
            "Prepojiť verejnú ponuku s proof-safe webom a intake flow.",
            "Ponuka existuje v hlave foundera, ale web ju nevysvetľuje jasne a nespúšťa ďalší operatívny krok.",
            "Pripraví offer copy, štruktúru stránok, intake otázky, buyer context a follow-up materiály.",
            "Majiteľ schvaľuje claimy, pricing, vizuály, verejné stránky, publishing, routing leadov a externé správy.",
            "Claim register, page map, offer menu, intake record, handoff note a follow-up path.",
            ["Offer", "Verejná stránka", "Intake", "Review", "Follow-up draft", "Handoff"],
            ["štruktúra ponuky", "smer web copy", "intake path", "claim checklist"],
            ["Public-safe", "Pilot-ready"],
            "Žiadny fake proof. Žiadne nepodložené claimy. Žiadne publikovanie bez approval.",
            "Pošlite ponuku, cieľového kupujúceho a jednu otázku, ktorú má web zodpovedať.",
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
        ("Sales Machine", GREEN),
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
    txt(c, "Discovery flow" if data["lang"] == "en" else "Discovery flow", MARGIN, 260, 30, INK, FONT_BOLD)
    draw_flow(c, data["flow"], MARGIN, 155, PAGE_W - MARGIN * 2, 72, False)
    round_rect(c, MARGIN, 72, PAGE_W - MARGIN * 2, 62, BG, BG, 18, 1)
    txt(c, "Decision rule" if data["lang"] == "en" else "Pravidlo rozhodnutia", MARGIN + 26, 94, 22, GOLD, FONT_BOLD)
    rule = "Start where value is visible, effort is bounded, and review responsibility is clear."
    if data["lang"] == "sk":
        rule = "Začať tam, kde je hodnota viditeľná, úsilie ohraničené a zodpovednosť za review jasná."
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
    top_rule(c, "Client decision support" if data["lang"] == "en" else "Pomôcka pre rozhodnutie klienta", 9, False)
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
    recommendation = "Automation Audit first. Then choose n8n Review, FinEcon Pilot, Sales Machine, Aureus OS, or Public Proof Site based on the scorecard."
    if data["lang"] == "sk":
        recommendation = "Najprv Automation Audit. Potom podľa scorecardu vybrať n8n Review, FinEcon Pilot, Sales Machine, Aureus OS alebo Public Proof Site."
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
    txt(c, "By day 30" if data["lang"] == "en" else "Do 30. dňa", MARGIN + 34, 184, 32, INK, FONT_BOLD)
    out = "Process map, pilot spec, review boundary, evidence example, risk list, and next decision."
    if data["lang"] == "sk":
        out = "Mapa procesu, pilot spec, schvaľovacia hranica, príklad dôkazu, risk list a ďalšie rozhodnutie."
    wrapped(c, out, MARGIN + 270, 190, 1400, 24, MUTED, FONT, 31, 2)
    footer(c, True)


def draw_usage(c: canvas.Canvas, data: dict):
    light_page(c)
    top_rule(c, "Public-safe usage" if data["lang"] == "en" else "Verejne bezpečné použitie", 11, False)
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
    txt(c, "Safety boundary" if data["lang"] == "en" else "Bezpečnostná hranica", MARGIN + 30, 166, 24, GOLD, FONT_BOLD)
    wrapped(c, data["safety"], MARGIN + 30, 134, PAGE_W - MARGIN * 2 - 60, 20, WHITE, FONT, 27, 3)
    footer(c, False)


def draw_cta(c: canvas.Canvas, data: dict, crops: dict[int, Path]):
    dark_page(c)
    top_rule(c, "Best first step" if data["lang"] == "en" else "Najlepší prvý krok", 12, True)
    wrapped(c, data["cta_title"], MARGIN, 892, 900, 64, WHITE, FONT_BOLD, 72, 2)
    wrapped(c, data["cta_subtitle"], MARGIN, 790, 850, 30, SOFT, FONT, 40, 2)
    round_rect(c, MARGIN, 545, 760, 142, PANEL, GOLD, 26, 1.4)
    txt(c, "Why first?" if data["lang"] == "en" else "Prečo prvý?", MARGIN + 34, 628, 26, GOLD, FONT_BOLD)
    reason = "It maps the process, ranks automation candidates, defines review boundaries, and turns vague AI ideas into a scoped pilot decision."
    if data["lang"] == "sk":
        reason = "Zmapuje proces, zoradí kandidátov, definuje schvaľovacie hranice a zmení nejasné AI nápady na scoped pilot rozhodnutie."
    wrapped(c, reason, MARGIN + 34, 588, 690, 23, WHITE, FONT, 31, 3)
    path_title = "Choose the next path" if data["lang"] == "en" else "Potom vyberieme ďalšiu cestu"
    txt(c, path_title, MARGIN, 470, 30, WHITE, FONT_BOLD)
    paths = [
        ("FinEcon Pilot", TEAL),
        ("n8n Review + Build", BLUE),
        ("Sales Machine", GREEN),
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
    txt(c, "Buyer action" if data["lang"] == "en" else "Akcia pre klienta", 974, 236, 29, INK, FONT_BOLD)
    wrapped(c, data["cta_action"], 974, 195, 780, 23, MUTED, FONT, 31, 3)
    footer(c, True)


def generate(path: Path, data: dict, cases: list[UseCase], crops: dict[int, Path]):
    path.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(path), pagesize=(PAGE_W, PAGE_H))
    c.setTitle(f"Aureus Use Case Showcase Pro Tier V6 {data['lang'].upper()}")
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
    en_path = EXPORT_DIR / "Aureus_Use_Case_Showcase_Pro_Tier_V6_EN.pdf"
    sk_path = EXPORT_DIR / "Aureus_Use_Case_Showcase_Pro_Tier_V6_SK.pdf"
    generate(en_path, en_pack(), en_cases(), crops)
    generate(sk_path, sk_pack(), sk_cases(), crops)
    render_previews(en_path, "v6_en")
    render_previews(sk_path, "v6_sk")
    desktop = desktop_dir()
    if desktop:
        shutil.copy2(en_path, desktop / en_path.name)
        shutil.copy2(sk_path, desktop / sk_path.name)
    print(f"Generated: {en_path}")
    print(f"Generated: {sk_path}")
    if desktop:
        print(f"Copied to: {desktop}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
