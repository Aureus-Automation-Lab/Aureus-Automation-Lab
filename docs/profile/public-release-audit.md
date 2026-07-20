# Public GitHub Release Audit

This audit applies to the public profile and every future public proof repository.

## Local Validation

```powershell
python scripts/validate-public-portfolio.py
python scripts/validate-aureus-use-case-showcase.py
python scripts/test-audit-public-github-state.py
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/public_profile_audit.ps1
git diff --check
```

## Required Review

- exact public repository, profile subject, rollout phase, and manifest binding;
- distinct human reviewer who is not the founder or a bot;
- protected-branch change with required checks and no bypass;
- immutable automation references, least-privilege permissions, timeout, and concurrency;
- explicit maturity, privacy, source, licensing, and claim boundaries;
- no private repository inventory, internal execution topology, secrets, private IDs, client data, or unsupported claims;
- owner-approved and verified contact URL before promotion.

## Live Verification

After an approved merge or setting change, verify the affected public surface signed out, run the read-only auditor, and capture the post-change attestation and rollback evidence. An audit actor/profile mismatch is a blocking finding. An API failure or incomplete response cannot produce `PASS`.

## Result

Record `PASS`, `REPAIR_REQUIRED`, `APPROVAL_REQUIRED`, or `BLOCKED`, the exact next safe action, and whether owner action is required. Licensing remains `APPROVAL_REQUIRED_LICENSE_DECISION`; promotion remains `BLOCKED_PENDING_CONTACT_PATH` until the approved URL is verified.
