# Live GitHub Rollout Checklist

The profile repository is already public. This checklist governs reviewed changes to live public state without exposing the private execution contract.

## Before Every Live Change

- refresh the exact authenticated identity, repository, default branch, checks, and review state;
- require repository/profile/phase bindings to match the public policy;
- capture rollback evidence and confirm the approved scope;
- run local validation, secret/claim checks, and signed-out preview;
- stop if identity, reviewer, evidence, or target state changed.

## Ordered Gates

1. Obtain review from a distinct human who is not the founder or a bot.
2. Merge the reviewed change through protected `main` after green checks.
3. Run a fresh read-only audit and post-change attestation.
4. Publish standalone proof only after its own public-safety and promotion gate.
5. Make no license grant before `APPROVAL_REQUIRED_LICENSE_DECISION` is resolved.
6. Do not claim `PROMOTION_READY` before the owner-approved contact URL is verified.

## Post-Change Verification

Verify public rendering signed out, policy controls read only, exact identity, review independence, links, images, and maturity labels. Store evidence in the canonical mission output and report `PASS`, `REPAIR_REQUIRED`, `APPROVAL_REQUIRED`, or `BLOCKED`.

Use the [GitHub governance review packet](github-governance-approval-packet.md) for the public boundary.
