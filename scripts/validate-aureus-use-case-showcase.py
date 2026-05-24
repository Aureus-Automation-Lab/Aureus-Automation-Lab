from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def marker(*parts: str) -> str:
    return "".join(parts)


REQUIRED_FILES = [
    "docs/use-cases/AUREUS_USE_CASE_SHOWCASE_AUDIT.md",
    "docs/use-cases/AUREUS_USE_CASE_CONTENT_MODEL.md",
    "docs/use-cases/AUREUS_USE_CASE_SHOWCASE_COPY_V5.md",
    "docs/use-cases/AUREUS_USE_CASE_SHOWCASE_COPY_V5_SK.md",
    "docs/use-cases/FINECON_POCKET_BRIDGE_USE_CASE_ONE_PAGER.md",
    "docs/use-cases/AUREUS_CLIENT_USE_CASE_OFFER_SHEET.md",
    "docs/use-cases/AUREUS_USE_CASE_GIT_PROOF_MAP.md",
    "docs/use-cases/AUREUS_USE_CASE_SHOWCASE_DESIGN_SPEC_V5.md",
    "docs/use-cases/AUREUS_USE_CASE_SHOWCASE_DESIGN_SPEC_V6.md",
    "docs/use-cases/AUREUS_USE_CASE_SHOWCASE_TOP_TIER_REFERENCE_NOTES.md",
    "docs/use-cases/AUREUS_USE_CASE_LINKEDIN_CAROUSEL.md",
    "docs/use-cases/AUREUS_USE_CASE_INSTAGRAM_CAROUSEL_V7.md",
    "docs/use-cases/AUREUS_USE_CASE_SHOWCASE_V5_PDF_HANDOFF.md",
    "scripts/generate-aureus-use-case-pdfs-v6-pro.py",
    "scripts/generate-aureus-use-case-instagram-v7.py",
]

USE_CASES = [
    "Automation Audit",
    "n8n Workflow Review + Build",
    "FinEcon Pocket / Bridge",
    "Approval-Safe Sales Machine",
    "Aureus OS / AOP",
    "Public Proof Website + Automation",
]

FINECON_REQUIRED = [
    "Pocket Document Intake",
    "Pocket Status API",
    "Pocket Review Action",
    "Pocket Bridge Start",
    "Pocket Company Registration",
    "Bridge Review to POHODA",
    "Bridge Preflight",
    "Bridge Live Import",
    "Bridge Post-Import Writeback",
    "Proof Pack Drive Publisher",
    "accountant validation",
    "Accounting correctness",
]

SECRET_MARKERS = [
    marker("OPENAI", "_API_KEY"),
    marker("GITHUB", "_TOKEN"),
    marker("N8N", "_API_KEY"),
    marker("client", "_secret"),
    marker("refresh", "_token"),
    marker("access", "_token"),
    marker("ghp", "_"),
    marker("github", "_pat_"),
    marker("xoxb", "-"),
    marker("AK", "IA"),
    marker("AI", "za"),
]

FORBIDDEN_PHRASES = [
    marker("guar", "anteed", " ROI"),
    marker("production", " proven"),
    marker("accounting", " correctness", " confirmed"),
    marker("certified", " security"),
]

GENERIC_URL_PATTERN = re.compile(r"https?://[^\s)]+", re.IGNORECASE)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="ignore")


def iter_text_files():
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if ".git" in path.parts:
            continue
        if path.parts[-1] == "exports" or "exports" in path.parts:
            continue
        if path.name in {
            "public_profile_audit.ps1",
            "validate-aureus-use-case-showcase.py",
            "validate-public-portfolio.py",
        }:
            continue
        if path.suffix.lower() in {".gif", ".png", ".jpg", ".jpeg", ".webp", ".ico", ".pdf"}:
            continue
        yield path


def main() -> int:
    errors: list[str] = []

    for rel in REQUIRED_FILES:
        if not (ROOT / rel).exists():
            errors.append(f"Missing required file: {rel}")

    copy_path = ROOT / "docs/use-cases/AUREUS_USE_CASE_SHOWCASE_COPY_V5.md"
    copy = read_text(copy_path) if copy_path.exists() else ""
    sk_path = ROOT / "docs/use-cases/AUREUS_USE_CASE_SHOWCASE_COPY_V5_SK.md"
    sk_copy = read_text(sk_path) if sk_path.exists() else ""
    one_pager_path = ROOT / "docs/use-cases/FINECON_POCKET_BRIDGE_USE_CASE_ONE_PAGER.md"
    one_pager = read_text(one_pager_path) if one_pager_path.exists() else ""

    for use_case in USE_CASES:
        if use_case not in copy:
            errors.append(f"English showcase missing use case: {use_case}")
        if use_case not in sk_copy:
            errors.append(f"Slovak showcase missing use case: {use_case}")

    if "AI prepares. People approve. Evidence remains." not in copy:
        errors.append("English showcase missing central rule")
    if "AI pripraví. Ľudia schvália. Dôkaz zostáva." not in sk_copy:
        errors.append("Slovak showcase missing central rule")

    for required in FINECON_REQUIRED:
        if required not in copy and required not in one_pager:
            errors.append(f"FinEcon proof copy missing required term: {required}")

    if "Start with **Automation Audit**" not in copy:
        errors.append("English showcase missing final CTA")
    if "Začnite s **Automation Audit**" not in sk_copy:
        errors.append("Slovak showcase missing final CTA")
    if not (ROOT / "docs/use-cases/AUREUS_USE_CASE_GIT_PROOF_MAP.md").exists():
        errors.append("Git proof map missing")
    if not (ROOT / "docs/use-cases/AUREUS_USE_CASE_SHOWCASE_DESIGN_SPEC_V5.md").exists():
        errors.append("Design spec missing")
    if not (ROOT / "docs/use-cases/AUREUS_USE_CASE_SHOWCASE_DESIGN_SPEC_V6.md").exists():
        errors.append("V6 design spec missing")
    if not (ROOT / "scripts/generate-aureus-use-case-pdfs-v6-pro.py").exists():
        errors.append("V6 pro PDF generator missing")
    if not (ROOT / "docs/use-cases/AUREUS_USE_CASE_LINKEDIN_CAROUSEL.md").exists():
        errors.append("LinkedIn carousel missing")
    if not (ROOT / "docs/use-cases/AUREUS_USE_CASE_INSTAGRAM_CAROUSEL_V7.md").exists():
        errors.append("Instagram carousel missing")
    instagram_generator = ROOT / "scripts/generate-aureus-use-case-instagram-v7.py"
    if instagram_generator.exists():
        instagram_text = read_text(instagram_generator)
        if "1080" not in instagram_text or "1350" not in instagram_text:
            errors.append("Instagram carousel generator missing 1080x1350 format")

    for path in iter_text_files():
        rel = path.relative_to(ROOT).as_posix()
        content = read_text(path)

        wrong_finecon = marker("Fine", "Con")
        if wrong_finecon in content:
            errors.append(f"Incorrect FinEcon spelling remains in {rel}")

        for secret_marker in SECRET_MARKERS:
            if secret_marker in content:
                errors.append(f"Secret-like marker '{secret_marker}' found in {rel}")

        for phrase in FORBIDDEN_PHRASES:
            if phrase.lower() in content.lower():
                errors.append(f"Forbidden or unsupported phrase '{phrase}' found in {rel}")

        for url in GENERIC_URL_PATTERN.findall(content):
            if "webhook" in url.lower():
                errors.append(f"Webhook URL-like text found in {rel}: {url}")

    if errors:
        print("AUREUS_USE_CASE_SHOWCASE_VALIDATION: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("AUREUS_USE_CASE_SHOWCASE_VALIDATION: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
