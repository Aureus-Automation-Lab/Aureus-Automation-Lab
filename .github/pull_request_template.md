## Summary

Explain what changed and why it improves the public profile.

Related issue:

## Public-Safe Scope

- [ ] Documentation or profile copy
- [ ] Public proof or use-case material
- [ ] Visual asset
- [ ] Validation or repository governance
- [ ] `public-proof/portfolio-manifest.json` updated, or confirmed not applicable

Source lineage and intended maturity:

## Validation

Commands run and results:

```powershell
python scripts/validate-public-portfolio.py
python scripts/validate-local-json-schema.py --schema .github/governance/public-profile-policy.schema.json --instance .github/governance/public-profile-policy.json
python scripts/test-audit-public-github-state.py
python scripts/validate-aureus-use-case-showcase.py
git diff --check
```

Visual proof, when visuals changed:

## Claim, Security, And Privacy Review

- [ ] No credentials, private data, local runtime state, or private endpoints
  are included.
- [ ] No unsupported customer, revenue, certification, accounting, security,
  trading, ROI, or production claim is introduced.
- [ ] Drafts, synthetic examples, and controlled proofs remain labeled.
- [ ] New links and media are public-safe and reviewable.
- [ ] Repository policy, manifest, README, and About metadata remain consistent.
- [ ] GitHub Actions use least privilege and immutable commit references.
- [ ] No production deploy, public campaign, or external message is part of
  this pull request.

## Release And Rollback

Risk level:

Rollback path:

Owner approval or repository-setting follow-up required:

Reviewed commit SHA:
