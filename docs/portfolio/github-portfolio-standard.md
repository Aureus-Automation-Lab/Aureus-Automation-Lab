# Public GitHub Portfolio Standard

This standard defines the public GitHub quality bar for Aureus Automation Lab. It describes the desired public outcome without publishing private repositories, internal authorization topology, rollout identifiers, credentials, or live security posture.

## Identity Architecture

- **Company:** Aureus Automation Lab
- **Current public profile subject:** `Aureus-Automation-Lab`
- **Current public profile repository:** `Aureus-Automation-Lab/Aureus-Automation-Lab`
- **Company namespace:** `AureusAutomationLab`
- **Operating layer:** Aureus OS

The exact current profile account and repository are fail-closed identity pins. A different account, repository, rollout phase, or cross-file identity is a blocker until the policy and evidence are deliberately reviewed together.

Products, modules, workflows, agents, validators, and historical labels remain subordinate to Aureus OS. Public proof and private implementation are separate trust surfaces: a public artifact must be useful on its own and must not imply access to the complete private system.

## Repository Classes

| Class | Public role | Required boundary |
| --- | --- | --- |
| Profile repository | Company and founder front door | Identity, proof map, governance, and limitations |
| Product proof | Sanitized implementation or synthetic demonstrator | Explicit maturity, validation, and non-production boundary |
| Reference repository | Architecture, contracts, examples, and evidence | No implication that private source is included |
| Template | Reusable starting point | Maintained, versioned, and independently reviewed before publication |
| Archived history | Traceability | Clearly archived and excluded from current recommendations |

An empty repository, copied documentation dump, or artifact that needs undisclosed context is not eligible for promotion or pinning.

## Public Repository Contract

Every standalone public repository must provide:

1. a concise README for the intended reader, problem, artifact type, maturity, and next review path;
2. visible limitations, data boundaries, and claim boundaries;
3. an architecture, workflow, or product visual when it materially improves understanding;
4. reproducible validation and a required green check;
5. security reporting, contribution, support, ownership, and pull-request guidance;
6. an explicit licensing decision covering code, documentation, assets, and trademarks;
7. least-privilege automation with immutable action references, timeouts, and failure visibility;
8. versioning and release evidence when consumers can depend on an artifact;
9. no credentials, private endpoints, customer data, private workflow exports, or unsupported outcomes; and
10. signed-out browser verification before promotion or pinning.

The present licensing state is `APPROVAL_REQUIRED_LICENSE_DECISION`. No license grant may be inferred from public visibility or repository contents.

## Branch And Merge Baseline

- Changes to the protected default branch use pull requests.
- A distinct human reviewer is required; the founder cannot act as the independent reviewer, including through a case variant, bot, or second self-controlled identity.
- Review is fail-closed until reviewer identity, access, and effective ownership rules are verified.
- Required checks must be bound to the intended trusted application, not only to a matching display name.
- Force pushes, deletion of protected history, hidden bypass, unresolved review conversations, and unreviewed history rewrites are prohibited.
- Squash merge and linear, signed history are the public baseline.
- Overlapping enforcement mechanisms are migrated with an approved rollback plan and post-change attestation.

The public policy records desired state. It does not prove that a live control is enabled. Current live drift can be established only by a fresh read-only audit.

## Security And Automation Baseline

- Enable the relevant repository security capabilities where supported.
- Default workflow permissions to read-only and elevate only the job that needs more.
- Pin third-party actions immutably and review dependency updates.
- Never give untrusted pull-request content write credentials or secrets.
- Apply code scanning, dependency review, artifact provenance, and SBOM generation when the shipped artifact makes those controls useful.
- Keep credentials, private payloads, customer data, production evidence, and internal execution contracts outside the public repository.

Sensitive execution remains private. The public `change_control` contract states only that changes are review-required, least-privilege, fail-closed, rollback-evidenced, and post-change-attested.

## Objective Status Model

| Status | Meaning |
| --- | --- |
| `PASS` | The exact public artifact or control was validated from current evidence. |
| `REPAIR_REQUIRED` | A safe repository-local correction is needed. |
| `APPROVAL_REQUIRED` | The next step changes live GitHub state, publishes content, or changes identity. |
| `BLOCKED` | A prerequisite such as an independent reviewer, licensing decision, verified contact path, or supported control is missing. |

`review_governance.current_status` accepts only `APPROVAL_REQUIRED` or `VERIFIED`; `PASS` is not a valid reviewer-governance shortcut.

## Promotion Gate

A repository may be promoted or pinned only when:

- source lineage and sanitization are documented;
- its README and proof are understandable without private context;
- local validation and CI pass;
- secret, privacy, dependency, and claim-safety reviews pass;
- naming and metadata match the canonical identity;
- governance blockers are resolved or explicitly recorded;
- an independent signed-out viewer test passes;
- licensing has an owner-approved decision;
- a verified owner-approved contact URL exists; and
- publication and pinning have their required approval evidence.

Until the licensing and contact-path decisions are resolved, the overall public promotion result remains blocked. No contact address or URL may be invented.

## Policy As Code And Drift Detection

- [Public policy as code](../../.github/governance/public-profile-policy.json)
- [Portfolio manifest](../../public-proof/portfolio-manifest.json)
- [Governance approval packet](../profile/github-governance-approval-packet.md)

```powershell
python scripts/validate-local-json-schema.py --schema .github/governance/public-profile-policy.schema.json --instance .github/governance/public-profile-policy.json
python scripts/test-audit-public-github-state.py
python scripts/validate-public-portfolio.py
python scripts/audit-public-github-state.py --json
```

The audit is read-only. Any live repair remains `APPROVAL_REQUIRED` and must use the private sensitive-execution contract.
