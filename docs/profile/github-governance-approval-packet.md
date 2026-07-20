# Public GitHub Governance Review Packet

Status: `APPROVAL_REQUIRED`

This packet describes the public desired state. It does not expose or authorize the sensitive execution contract, which remains private.

The sensitive execution contract remains private.

## Public Governance Baseline

The canonical public identity is `Aureus-Automation-Lab/Aureus-Automation-Lab`, with `Aureus-Automation-Lab` as the profile subject. The repository is governed through review-first changes, a protected default branch, least privilege, narrowly scoped automation permissions, claim-safe public evidence, and fail-closed validation.

Observed live state is evidence only after the read-only auditor completes successfully. An unavailable API, incomplete response, identity mismatch, or unverified reviewer blocks a readiness claim.

## Desired-State Controls

| Area | Required outcome | Public status |
|---|---|---|
| Identity | Repository, profile subject, policy, manifest, and audit actor agree exactly | Validated locally; live attestation required |
| Review | A distinct human reviewer approves the reviewed change | `APPROVAL_REQUIRED` |
| Merge | Protected `main`, squash-only history, required checks, no bypass | Desired state; verify live before merge |
| Security | Least privilege, secret scanning, dependency review, private vulnerability reporting | Desired state; verify availability live |
| Evidence | Read-only before/after audit, rollback evidence, and post-change attestation | Required |
| Licensing | Owner decides boundaries for code, documentation, assets, and trademarks | `APPROVAL_REQUIRED_LICENSE_DECISION` |
| Contact path | Owner approves a concrete URL and it is verified before promotion | `BLOCKED_PENDING_CONTACT_PATH` |

## Change-Control Boundary

The public policy intentionally contains only a minimal `change_control` declaration: review required, least privilege, fail closed, rollback evidence required, post-change attestation required, and a private sensitive execution contract. Internal authorization topology, credentials, repository inventory, incident procedures, and live mutation details do not belong in this public repository.

No live GitHub setting, access grant, identity change, repository publication, visibility change, external message, or public promotion is authorized by this document.

## Recommended Rollout

1. Validate the exact public identity, policy, schema, manifest, documentation, tests, and workflow locally.
2. Review the proposed change set and its public disclosure boundary.
3. Obtain approval from a distinct human reviewer; the founder account can never satisfy that role.
4. Merge through the protected default branch only after all required checks and review gates pass.
5. Run a fresh read-only audit and capture the post-change attestation.
6. Keep promotion blocked until the owner approves and the audit verifies a safe contact URL.

## Required Evidence

- green repository validation and adversarial governance tests;
- exact repository and profile-subject binding;
- distinct human reviewer identity and effective access proof;
- protected-branch merge evidence with no bypass;
- before/after control attestation;
- rollback evidence for each approved live change;
- no-secret audit output;
- explicit owner licensing decision before any license grant;
- owner-approved, verified contact URL before `PROMOTION_READY`.

## Approval Boundary

`APPROVAL_REQUIRED` is a blocker, not permission. If a live audit cannot prove actor/profile identity, reviewer independence, required controls, or post-change evidence, the result remains blocked. Actor/profile mismatch is always a blocking finding, never a passive observation.

The repository currently grants no license. Reuse rights for code, documentation, assets, and trademarks remain undecided until the owner makes an explicit legal choice. The contact path is pending owner approval and verification, so the repository must not claim `PROMOTION_READY`.
