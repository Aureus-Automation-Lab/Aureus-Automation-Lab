from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def marker(*parts: str) -> str:
    return "".join(parts)


REQUIRED_FILES = [
    "README.md",
    "CODE_OF_CONDUCT.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "SUPPORT.md",
    ".github/CODEOWNERS",
    ".github/dependabot.yml",
    ".github/ISSUE_TEMPLATE/config.yml",
    ".github/ISSUE_TEMPLATE/public-profile-feedback.yml",
    ".github/pull_request_template.md",
    ".github/workflows/public-profile-validation.yml",
    "docs/portfolio/public-demo-flow.md",
    "docs/portfolio/synthetic-demo-case.md",
    "docs/portfolio/cv-usage.md",
    "docs/portfolio/offer-menu.md",
    "docs/portfolio/capabilities.md",
    "docs/portfolio/case-studies.md",
    "docs/portfolio/project-map.md",
    "docs/portfolio/naming-system.md",
    "docs/portfolio/credentials.md",
    "docs/portfolio/review-guide.md",
    "docs/portfolio/public-portfolio-scorecard.md",
    "docs/proof/finecon-source-backed-status.md",
    "public-proof/crm-platform/README.md",
    "public-proof/crm-platform/architecture.md",
    "public-proof/crm-platform/state-and-audit-model.md",
    "public-proof/crm-platform/validation-boundary.md",
    "public-proof/finecon/README.md",
    "public-proof/sales-machine/README.md",
    "public-proof/trading-infrastructure/README.md",
    "public-proof/trading-infrastructure/risk-boundary.md",
    "assets/aureus-profile-hero.gif",
    "assets/aureus-offer-menu.gif",
    "assets/aureus-sales-machine.gif",
    "assets/aureus-finecon-flow.gif",
    "assets/aureus-os-model.gif",
    "assets/aureus-public-boundary.gif",
    "assets/aureus-capability-system.gif",
    "assets/aureus-collaboration-flow.gif",
    "assets/aureus-proof-pack.gif",
    "assets/aureus-readiness-check.gif",
    "assets/aureus-solution-architecture.gif",
]

README_REQUIRED = [
    "Founder & AI Automation Solution Architect",
    "AI Automation Solution Architect",
    "Controlled AI automation",
    "docs/portfolio/public-demo-flow.md",
    "docs/portfolio/synthetic-demo-case.md",
    "docs/portfolio/offer-menu.md",
    "docs/portfolio/cv-usage.md",
    "docs/portfolio/project-map.md",
    "docs/portfolio/naming-system.md",
    "docs/portfolio/credentials.md",
    "public-proof/crm-platform/README.md",
    "public-proof/trading-infrastructure/README.md",
]

FILE_REQUIRED = {
    "CODE_OF_CONDUCT.md": ["Our Standard", "Reporting And Enforcement"],
    "CONTRIBUTING.md": ["PR-first workflow", "validate-public-portfolio.py", "Review Boundary"],
    "SECURITY.md": ["Reporting A Vulnerability", "Do not open a public issue", "Sensitive Material"],
    "SUPPORT.md": ["public-profile feedback", "not a production support channel"],
    ".github/CODEOWNERS": ["@Aureus-Automation-Lab"],
    ".github/dependabot.yml": ["package-ecosystem: github-actions"],
    ".github/ISSUE_TEMPLATE/config.yml": ["blank_issues_enabled: false"],
    ".github/ISSUE_TEMPLATE/public-profile-feedback.yml": ["Public profile feedback", "Safety confirmation"],
    ".github/pull_request_template.md": ["Claim, Security, And Privacy Review", "Release And Rollback"],
    ".github/workflows/public-profile-validation.yml": [
        "permissions:",
        "contents: read",
        "Validate public profile",
        "validate-public-portfolio.py",
        "validate-aureus-use-case-showcase.py",
    ],
    "docs/portfolio/capabilities.md": [
        "Best-Fit Roles",
        "Aureus CRM Operations",
        "Aureus FinEcon",
        "Aureus Sales Workflow",
    ],
    "docs/portfolio/project-map.md": [
        "Aureus OS",
        "Aureus CRM Operations",
        "Aureus FinEcon",
        "Aureus Trading Infrastructure",
    ],
    "docs/portfolio/naming-system.md": [
        "Canonical Hierarchy",
        "Only Aureus OS is an operating system",
        "Legacy Alias Register",
        "Aureus CRM Operations",
        "Aureus FinEcon",
        "Aureus Sales Workflow",
        "Aureus Trading Infrastructure",
    ],
    "docs/portfolio/credentials.md": [
        "IBM AI Engineering Professional Certificate",
        "13 courses",
        "Professional, non-credit certificate",
    ],
    "docs/portfolio/case-studies.md": [
        "Pro-Tier Public Case Studies",
        "Automation Audit",
        "Aureus Sales Workflow",
        "Aureus FinEcon",
        "Git-Backed LinkedIn Content",
        "Monthly Automation Partner",
        "Aureus CRM Operations",
        "Aureus Trading Infrastructure",
    ],
    "docs/portfolio/review-guide.md": ["CV"],
    "docs/portfolio/offer-menu.md": ["Recommended first purchase"],
    "docs/proof/finecon-source-backed-status.md": [
        "Pocket document intake",
        "accountant validation",
        "does not claim",
    ],
    "public-proof/crm-platform/README.md": [
        "Aureus CRM Operations",
        "49 changed files",
        "21,472 added lines",
        "source-backed full-stack synthetic product proof",
    ],
    "public-proof/crm-platform/state-and-audit-model.md": [
        "ReservationsReleased",
        "Concrete Inventory Invariant",
    ],
    "public-proof/trading-infrastructure/README.md": [
        "paper-run",
        "isolated executor",
        "not financial advice",
    ],
    "public-proof/finecon/README.md": [
        "Aureus FinEcon Public Proof",
        "accounting review",
    ],
    "public-proof/sales-machine/README.md": [
        "Aureus Sales Workflow Public Proof",
        "historical alias",
    ],
}

PRIMARY_NAMING_SURFACES = [
    "README.md",
    "docs/portfolio/project-map.md",
    "public-proof/README.md",
    "docs/proof/proof-index.md",
]

CANONICAL_PUBLIC_NAMES = [
    "Aureus OS",
    "Aureus CRM Operations",
    "Aureus FinEcon",
    "Aureus Trading Infrastructure",
]

FORBIDDEN_PHRASES = [
    marker("guar", "anteed", " ROI"),
    marker("proven", " revenue"),
    marker("world", "-class"),
    marker("best in", " the world"),
    marker("enterprise", "-grade"),
    marker("SOC 2", " certified"),
    marker("production", " proven"),
]

SECRET_MARKERS = [
    marker("OPENAI", "_API_KEY", "="),
    marker("GITHUB", "_TOKEN", "="),
    marker("N8N", "_API_KEY", "="),
    marker("password", "="),
    marker("secret", "="),
    marker("webhook", ".site"),
    marker("localhost", ":"),
    marker("127", ".0.0.1"),
]

MOJIBAKE_MARKERS = [
    "\u0102",
    "\u00e2\u20ac",
    "\ufffd",
]


def iter_text_files():
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if ".git" in path.parts:
            continue
        if "__pycache__" in path.parts:
            continue
        if "exports" in path.parts:
            continue
        if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".pyc"}:
            continue
        yield path


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="ignore")


def main() -> int:
    errors: list[str] = []

    for rel in REQUIRED_FILES:
        if not (ROOT / rel).exists():
            errors.append(f"Missing required file: {rel}")

    readme_path = ROOT / "README.md"
    readme = read_text(readme_path) if readme_path.exists() else ""
    for required in README_REQUIRED:
        if required not in readme:
            errors.append(f"README.md missing required text/link: {required}")

    if "Founder & AI Systems Architect" in readme:
        errors.append("README.md still contains old main hero phrase: Founder & AI Systems Architect")

    readme_lines = readme.splitlines()
    if len(readme_lines) > 180:
        errors.append(f"README.md is too long for a focused public front door: {len(readme_lines)} lines (max 180)")

    headings = [
        line.strip()
        for line in readme.splitlines()
        if line.startswith("#")
    ]
    duplicate_headings = sorted({heading for heading in headings if headings.count(heading) > 1})
    for heading in duplicate_headings:
        errors.append(f"README.md contains duplicate heading: {heading}")

    for rel, required_values in FILE_REQUIRED.items():
        path = ROOT / rel
        content = read_text(path) if path.exists() else ""
        for required in required_values:
            if required not in content:
                errors.append(f"{rel} missing required text: {required}")

    for rel in PRIMARY_NAMING_SURFACES:
        path = ROOT / rel
        content = read_text(path) if path.exists() else ""
        for canonical_name in CANONICAL_PUBLIC_NAMES:
            if canonical_name not in content:
                errors.append(f"{rel} missing canonical public name: {canonical_name}")

    for path in ROOT.rglob("*.md"):
        if ".git" in path.parts or "exports" in path.parts:
            continue
        content = read_text(path)
        for match in re.finditer(r"\[[^\]]+\]\(([^)]+)\)", content):
            target = match.group(1).strip()
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            clean = target.split("#", 1)[0].split("?", 1)[0]
            if clean and not (path.parent / clean).resolve().exists():
                rel = path.relative_to(ROOT).as_posix()
                errors.append(f"Broken Markdown link in {rel}: {target}")

    for path in iter_text_files():
        rel = path.relative_to(ROOT).as_posix()
        content = read_text(path)

        wrong_finecon = marker("Fine", "Con")
        if wrong_finecon in content:
            errors.append(f"Incorrect FinEcon spelling remains in {rel}")

        for phrase in FORBIDDEN_PHRASES:
            if phrase in content:
                errors.append(f"Forbidden hype phrase '{phrase}' found in {rel}")

        for secret_marker in SECRET_MARKERS:
            if secret_marker in content:
                errors.append(f"Obvious secret/local marker '{secret_marker}' found in {rel}")

        for mojibake_marker in MOJIBAKE_MARKERS:
            if mojibake_marker in content:
                errors.append(f"Likely encoding corruption found in {rel}: {ascii(mojibake_marker)}")

    if errors:
        print("PUBLIC_PORTFOLIO_VALIDATION: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PUBLIC_PORTFOLIO_VALIDATION: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
