$ErrorActionPreference = "Stop"

Write-Host "== Git status =="
git status --short

Write-Host "`n== Whitespace check =="
git diff --check

Write-Host "`n== Markdown internal link check =="
$linkChecker = @'
from pathlib import Path
import re
import sys

root = Path(".").resolve()
errors = []

for path in root.rglob("*.md"):
    if ".git" in path.parts:
        continue
    text = path.read_text(encoding="utf-8")
    for match in re.finditer(r"\[[^\]]+\]\(([^)]+)\)", text):
        target = match.group(1).strip()
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        clean = target.split("#", 1)[0]
        if not clean:
            continue
        dest = (path.parent / clean).resolve()
        if not dest.exists():
            errors.append(f"{path.relative_to(root)} -> {target}")

if errors:
    print("BROKEN LINKS")
    print("\n".join(errors))
    sys.exit(1)

print("Markdown internal links OK")
'@
$linkChecker | python -

Write-Host "`n== Secret pattern scan =="
$secretScanner = @'
from pathlib import Path
import re
import sys

patterns = [
    re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"ghp_[A-Za-z0-9_]{20,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
    re.compile(r"xoxb-[A-Za-z0-9-]{20,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"AIza[0-9A-Za-z_-]{20,}"),
    re.compile(r"eyJ[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{20,}"),
    re.compile(r"(?i)(client_secret|refresh_token|access_token)\s*[:=]\s*[A-Za-z0-9_./+=-]{12,}"),
]

errors = []
for path in Path(".").rglob("*"):
    if path.is_dir() or ".git" in path.parts:
        continue
    if path.suffix.lower() not in {".md", ".svg", ".json", ".txt", ".yml", ".yaml", ".toml", ".ps1", ".editorconfig", ".gitattributes"}:
        continue
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        continue
    for pattern in patterns:
        if pattern.search(text):
            errors.append(str(path))
            break

if errors:
    print("POSSIBLE SECRET PATTERNS")
    print("\n".join(errors))
    sys.exit(1)

print("Secret pattern scan OK")
'@
$secretScanner | python -

Write-Host "`n== Encoding marker scan =="
$encodingScanner = @'
from pathlib import Path
import sys

markers = [
    chr(0xfffd),
    chr(0x00c3),
    chr(0x00c2),
    "".join(map(chr, [0x00e2, 0x20ac, 0x2122])),
    "".join(map(chr, [0x00e2, 0x20ac, 0x0153])),
    chr(0x0102),
]

bad = []
for path in Path(".").rglob("*.md"):
    if ".git" in path.parts:
        continue
    text = path.read_text(encoding="utf-8")
    for marker in markers:
        if marker in text:
            bad.append(str(path))
            break

if bad:
    print("ENCODING MARKERS")
    print("\n".join(bad))
    sys.exit(1)

print("Encoding marker scan OK")
'@
$encodingScanner | python -

Write-Host "`n== Large files over 5MB =="
$largeFiles = Get-ChildItem -Recurse -File |
  Where-Object { $_.Length -gt 5MB -and $_.FullName -notmatch "\\.git\\" }

if ($largeFiles) {
  $largeFiles | Select-Object FullName, @{Name="MB";Expression={[math]::Round($_.Length / 1MB, 2)}} | Format-Table -AutoSize
  throw "Large files found"
}

Write-Host "No large files over 5MB"
Write-Host "`nPublic profile audit OK"
