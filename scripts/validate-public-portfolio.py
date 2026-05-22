from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def marker(*parts: str) -> str:
    return "".join(parts)


REQUIRED_FILES = [
    "README.md",
    "PUBLIC_DEMO_FLOW.md",
    "OFFER_MENU.md",
    "PUBLIC_PORTFOLIO_SCORECARD.md",
    "assets/public-ai-automation-operating-flow.svg",
]

README_REQUIRED = [
    "AI Automation Solution Architect",
    "controlled AI automation systems",
    "PUBLIC_DEMO_FLOW.md",
    "OFFER_MENU.md",
]

FORBIDDEN_PHRASES = [
    marker("guaranteed", " ROI"),
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


def iter_text_files():
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if ".git" in path.parts:
            continue
        if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico"}:
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

    if errors:
        print("PUBLIC_PORTFOLIO_VALIDATION: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PUBLIC_PORTFOLIO_VALIDATION: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
