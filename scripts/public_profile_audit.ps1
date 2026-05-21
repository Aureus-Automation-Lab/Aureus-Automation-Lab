$ErrorActionPreference = "Stop"

Write-Host "== Public Profile Audit =="
Write-Host "This script reports public-release risks. It does not delete, rewrite, or generate files."

Write-Host "`n== Git status =="
git status --short

Write-Host "`n== Profile repo naming check =="
$remoteUrl = ""
$currentUsername = ""
$repoOwner = ""
$repoName = ""

try {
  $remoteUrl = (& git remote get-url origin 2>$null).Trim()
} catch {
  $remoteUrl = ""
}

if ($remoteUrl) {
  Write-Host "Current git remote: $remoteUrl"
  if ($remoteUrl -match "github\.com[:/](?<owner>[^/]+)/(?<repo>[^/.]+)(?:\.git)?$") {
    $repoOwner = $Matches.owner
    $repoName = $Matches.repo
    Write-Host "Current repository: $repoOwner/$repoName"
  } else {
    Write-Host "Current repository could not be parsed from remote. Verify manually."
  }
} else {
  Write-Host "Current git remote could not be detected. Verify manually."
}

try {
  $currentUsername = (& gh api user --jq .login 2>$null).Trim()
} catch {
  $currentUsername = ""
}

if ($currentUsername) {
  Write-Host "Detected GitHub username: $currentUsername"
  if ($repoName) {
    if ($repoName -eq $currentUsername) {
      Write-Host "Profile repo naming OK: repository name matches current username."
    } else {
      Write-Host "WARNING: Profile repo naming mismatch."
      Write-Host "Repository name: $repoName"
      Write-Host "Current username: $currentUsername"
      Write-Host "Required profile repository: $currentUsername/$currentUsername"
      Write-Host "Do not switch visibility to public until repository name equals current username."
    }
  }
} else {
  Write-Host "GitHub username could not be detected automatically. Verify manually that repository name matches username before public."
}

Write-Host "`n== Suspicious text scan =="
$patterns = @(
  ("BEGIN " + "PRIVATE KEY"),
  ("OPENAI_" + "API_KEY"),
  "api_key",
  "secret",
  "token",
  "password",
  "credential",
  "webhook",
  "ngrok",
  "localhost",
  "127.0.0.1",
  "pohoda",
  "mserver",
  "gmail",
  "client_secret",
  "refresh_token",
  "access_token",
  ("ghp" + "_"),
  ("github" + "_pat_"),
  "sk-",
  ("xoxb" + "-"),
  ("AK" + "IA"),
  ("AI" + "za")
)

foreach ($pattern in $patterns) {
  Write-Host "`n--- pattern: $pattern ---"
  $matches = & git grep -n -I --fixed-strings $pattern 2>$null
  if ($LASTEXITCODE -eq 0) {
    $matches | ForEach-Object { Write-Host $_ }
  } elseif ($LASTEXITCODE -eq 1) {
    Write-Host "No matches"
  } else {
    throw "git grep failed for pattern: $pattern"
  }
}

Write-Host "`n== Identity references to review =="
Write-Host "These are not automatic failures. Confirm they appear only in migration, audit, or owner-instruction docs."
$identityPatterns = @(
  ("Kimi" + "Aoki"),
  ("Kimi " + "Aoki"),
  ("github.com/" + "Kimi" + "Aoki"),
  ("Private draft " + "profile"),
  ("Kimi" + "Aoki/Kimi" + "Aoki"),
  ("Robert " + "Kolesar"),
  ("Robert Koles" + [char]0x00E1 + "r"),
  ("R" + [char]0x00F3 + "bert Kolesar")
)

foreach ($pattern in $identityPatterns) {
  Write-Host "`n--- identity pattern: $pattern ---"
  $matches = & git grep -n -I --fixed-strings $pattern 2>$null
  if ($LASTEXITCODE -eq 0) {
    $matches | ForEach-Object { Write-Host $_ }
  } elseif ($LASTEXITCODE -eq 1) {
    Write-Host "No matches"
  } else {
    throw "git grep failed for identity pattern: $pattern"
  }
}

Write-Host "`n== Large files over 5MB =="
$largeFiles = Get-ChildItem -Recurse -File |
  Where-Object { $_.Length -gt 5MB -and $_.FullName -notmatch "\\.git\\" }

if ($largeFiles) {
  $largeFiles |
    Select-Object FullName, @{Name="MB";Expression={[math]::Round($_.Length / 1MB, 2)}} |
    Format-Table -AutoSize
} else {
  Write-Host "No large files over 5MB"
}

Write-Host "`n== File inventory =="
Get-ChildItem -Recurse -File |
  Where-Object { $_.FullName -notmatch "\\.git\\" } |
  Sort-Object FullName |
  Select-Object @{Name="Path";Expression={$_.FullName.Replace((Get-Location).Path + "\", "")}}, @{Name="KB";Expression={[math]::Round($_.Length / 1KB, 1)}} |
  Format-Table -AutoSize

Write-Host "`n== Markdown link inventory =="
Get-ChildItem -Recurse -Filter *.md |
  Where-Object { $_.FullName -notmatch "\\.git\\" } |
  Sort-Object FullName |
  ForEach-Object {
    $file = $_.FullName.Replace((Get-Location).Path + "\", "")
    Select-String -Path $_.FullName -Pattern "\]\((.*?)\)" -AllMatches | ForEach-Object {
      foreach ($match in $_.Matches) {
        [PSCustomObject]@{
          File = $file
          Link = $match.Groups[1].Value
        }
      }
    }
  } | Format-Table -AutoSize

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

Write-Host "`n== Whitespace check =="
git diff --check

Write-Host "`n== Next steps =="
Write-Host "1. Review any suspicious text matches above."
Write-Host "2. Confirm large files are intentional and public-safe."
Write-Host "3. Open README.md and key docs in GitHub preview."
Write-Host "4. Open the repo/profile in a signed-out browser after making it public."
Write-Host "5. Do not publish if any private data, unsupported claim, or broken link is found."

Write-Host "`nAudit report complete."
