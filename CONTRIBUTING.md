# Contributing

This public profile repository uses a PR-first workflow. Contributions should
improve the public portfolio, proof-safe documentation, visuals, or validation
without exposing private Aureus implementation.

## Before You Start

Open a public-profile feedback issue for a material proposal. Keep security
reports and sensitive context out of public issues; follow [SECURITY.md](SECURITY.md)
instead.

## Pull Requests

- Base work on the current `main` branch.
- Use one branch and one coherent purpose per pull request.
- Explain the public benefit, changed files, validation, claim-safety impact,
  and rollback path.
- Keep customer data, private workflow exports, credentials, endpoints,
  production details, and unsupported performance claims out of the repo.
- Do not represent a draft, mockup, or controlled proof as a live production
  result.

## Validation

Run the public-safe checks before requesting review:

```powershell
python scripts/validate-public-portfolio.py
python scripts/validate-aureus-use-case-showcase.py
powershell -NoProfile -File scripts/public_profile_audit.ps1
git diff --check
```

The PowerShell audit is intentionally read-only. Review its identity and
suspicious-text findings rather than treating every text match as a leak.

## Review Boundary

A pull request is not public-ready until the repository validators pass, the
diff has been reviewed, conversations are resolved, and a maintainer confirms
that claims and media remain public-safe.
