# GitHub Identity Consistency Standard

The canonical public profile subject is `Aureus-Automation-Lab`, and the matching public profile repository is `Aureus-Automation-Lab/Aureus-Automation-Lab`.

## Identity Invariant

Policy, schema, portfolio manifest, profile content, repository target, and read-only audit actor must resolve to that exact identity. A different repository owner, profile subject, rollout binding, or authenticated audit actor fails closed.

## Change Boundary

This document is not an account-rename, repository-transfer, or identity-migration runbook. Any future identity change requires a separate reviewed decision, impact assessment, rollback plan, cross-file update, validation, and explicit owner approval. Until then, the current canonical identity remains authoritative.

## Verification

- validate policy and manifest bindings locally;
- reject case-variant attempts to treat the founder as an independent reviewer;
- reject bot or application identities as human reviewers;
- require the authenticated read-only audit actor to match the profile subject;
- record identity mismatches as blocking findings.

Status: `APPROVAL_REQUIRED` for any live identity mutation.
