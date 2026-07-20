# Public Portfolio Readiness Matrix

This matrix separates locally validated public artifacts from live GitHub readiness.

## Status Definitions

| Status | Meaning |
|---|---|
| `PASS` | Verified by current evidence |
| `REPAIR_REQUIRED` | A known safe-local gap remains |
| `APPROVAL_REQUIRED` | A reviewed owner or independent-review decision is required |
| `BLOCKED` | A required external prerequisite is unavailable or unverified |

## Readiness Gates

| Gate | Status | Required evidence |
|---|---|---|
| Canonical public identity | `PASS` locally | Exact repository, subject, manifest, policy, and phase binding |
| Portfolio information architecture | `PASS` locally | One company, one OS, clearly classified products and proofs |
| Public governance change | `APPROVAL_REQUIRED` | Green validation, distinct human review, protected merge, post-change audit |
| Standalone proof publication | `APPROVAL_REQUIRED` | Sanitized package, claim review, repository-specific promotion gate |
| CRM visual proof | `VISUAL_ASSET_BLOCKED_PENDING_SANITIZED_REVIEW` | A readable privacy-safe crop that passes visual and claim-safety review |
| Licensing | `APPROVAL_REQUIRED_LICENSE_DECISION` | Owner-selected boundaries for code, documentation, assets, and trademarks |
| Contact path and promotion | `BLOCKED_PENDING_CONTACT_PATH` | Owner-approved URL verified before `PROMOTION_READY` |
| Live attestation | `REPAIR_REQUIRED` until refreshed | Read-only audit with no identity, review, security, or evidence blockers |

## Promotion Decision

The public materials can be reviewed, but the system must not claim `PROMOTION_READY` while licensing, contact, independent-review, or live-attestation gates remain open. Public changes stay `APPROVAL_REQUIRED` and fail closed.

## Evidence Boundary

Public proof demonstrates architecture, workflow state, validation discipline, and limitations. It does not disclose private repositories, internal authorization topology, credentials, customer data, production logs, or sensitive operating state. No unsupported customer outcome, revenue, ROI, certification, accounting, trading, security, or production claim is permitted.

See the [Public GitHub Portfolio Standard](github-portfolio-standard.md), [portfolio manifest](../../public-proof/portfolio-manifest.json), and [governance review packet](../profile/github-governance-approval-packet.md).
