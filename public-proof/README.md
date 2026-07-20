# Public Proof Showroom

The machine-readable [portfolio manifest](portfolio-manifest.json) records which packages remain embedded scenarios, which are standalone repository candidates, their maturity, and their publication state. Candidate names are targets only; they are not live-repository claims.

This showroom is the evidence layer for Aureus Automation Lab. Each package answers four questions:

1. What system was designed?
2. What source-backed behavior can be reviewed?
3. What validation or operating controls exist?
4. What is explicitly not being claimed?

![Aureus public proof boundary](../assets/aureus-public-boundary.gif)

## Primary Proof Packages

| Package | Strongest signal | Status | Start here |
| --- | --- | --- | --- |
| **Aureus CRM Operations** | Full-stack UI/API/SQLite product with roles, operational state, audit, and tests | Source-backed synthetic demo | [Review](aureus-crm-operations/README.md) |
| **Aureus OS** | Mission control, agent/tool routing, action authority, validation, and evidence | Public architecture; private runtime | [Review](aureus-os/README.md) |
| **Aureus FinEcon** | Reviewed document intake, extraction, bridge handoff, and accountant boundary | Source-backed pilot direction | [Review](aureus-finecon/README.md) |
| **Aureus Trading Infrastructure** | Deterministic rails, isolated execution, runtime state, observability, and CI risk gates | Private paper-run architecture | [Review](aureus-trading-infrastructure/README.md) |

## Supporting Proof

| Package | What it adds |
| --- | --- |
| [Aureus Sales Workflow](aureus-sales-workflow/README.md) | Subordinate demonstration scenario for stateful qualification and approval-gated follow-up |
| [Credentials](../docs/portfolio/credentials.md) | Verified education record separated from product and customer evidence |
| [Case Studies](../docs/portfolio/case-studies.md) | Buyer problem, architecture, review boundary, evidence, and offer path |
| [Source Truth Map](../docs/proof/source-truth-map.md) | Public claim-to-private-source register and publication boundary |
| [Public Naming System](../docs/portfolio/naming-system.md) | Canonical hierarchy and legacy-alias register |

## Evidence Classes

| Class | Meaning |
| --- | --- |
| **Source-backed** | A claim maps to tracked implementation or a merged source receipt |
| **Validated** | Named checks were executed at the referenced source revision |
| **Synthetic** | Data and scenarios are fictional and safe for demonstration |
| **Architecture proof** | The system shape is evidenced; live operation or outcomes are not implied |
| **External outcome proof** | Requires separate customer, production, or independently verifiable evidence; not claimed here |

## What Stays Private

Credentials, private endpoints, raw workflow exports, strategy logic, client records, real invoices or leads, production settings, private logs, runtime screenshots, and sensitive proof receipts remain outside this repository.

## Review Rule

A stronger claim must have stronger evidence. If a statement cannot be mapped to source, validation, or independently reviewable evidence, it remains a capability or direction—not an outcome claim.
