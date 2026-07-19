# Aureus Use Case Git Proof Map

This map connects each client-facing use case to source-backed evidence without exposing private implementation.

Public-safe status values:

- **Public** - visible in this public profile repo.
- **Internal source** - known from internal/source-of-truth repositories, summarized without private details.
- **Private implementation** - exists behind safety boundaries and is not exposed publicly.

## Automation Audit

| Source | What it proves | What it does not prove | Public-safe status |
| --- | --- | --- | --- |
| `docs/portfolio/offer-menu.md` | Automation Audit is the recommended first purchase. | Does not prove customer outcome or ROI. | Public |
| `docs/portfolio/public-demo-flow.md` | Shows how manual process work becomes controlled workflow direction. | Does not expose private implementation. | Public |
| `docs/portfolio/synthetic-demo-case.md` | Gives a fictional invoice-review example. | Does not claim real client result. | Public |
| `docs/use-cases/AUREUS_CLIENT_USE_CASE_OFFER_SHEET.md` | Converts the audit into a client follow-up offer sheet. | Does not set price or guarantee outcome. | Public |

## n8n Workflow Review + Build

| Source | What it proves | What it does not prove | Public-safe status |
| --- | --- | --- | --- |
| `docs/portfolio/offer-menu.md` | n8n review and build are defined as client offers. | Does not expose raw workflow exports. | Public |
| `docs/portfolio/solution-architecture.md` | Shows review, validation, evidence, and handoff model. | Does not prove live activation. | Public |
| `AureusAutomationLab/n8n-workflows:scripts/aureus-n8n-finecon-excellence.py` | Internal source has workflow excellence tooling. | Does not expose private workflow data publicly. | Internal source |
| `AureusAutomationLab/n8n-workflows:scripts/check-finecon-ops-signals.ps1` | Internal source has operational signal checks. | Does not prove customer production operation. | Internal source |

## FinEcon Pocket / Bridge

| Source | What it proves | What it does not prove | Public-safe status |
| --- | --- | --- | --- |
| `public-proof/finecon/README.md` | Public-safe FinEcon proof story exists. | Does not expose private routes, payloads, IDs, credentials, or real documents. | Public |
| `public-proof/finecon/invoice-review-flow.md` | Shows reviewed document flow. | Does not claim accounting correctness. | Public |
| `public-proof/finecon/review-boundary.md` | Shows accountant/professional review boundary. | Does not replace professional review. | Public |
| `docs/proof/finecon-source-backed-status.md` | Summarizes source-backed FinEcon status safely. | Does not expose internal workflow exports. | Public |
| `AureusAutomationLab/n8n-workflows:workflows/finecon/*.json` | 19 FinEcon source-of-truth workflow exports exist, including Pocket, Bridge, and Proof Pack Publisher workflows. | Does not make the JSON public or expose private runtime details. | Internal source |
| `AureusAutomationLab/n8n-workflows:docs/finecon_bridge/FINECON_PRODUCT_STATUS.md` | Core E2E, Pocket to POHODA, live import, proof storage, and accountant boundary status are tracked. | Does not close accountant validation. | Internal source |
| `AureusAutomationLab/n8n-workflows:docs/finecon_bridge/FINECON_WORKFLOW_SOURCE_OF_TRUTH.md` | The FinEcon workflow family is documented as source of truth. | Does not allow copying private IDs or route details to public docs. | Internal source |
| `AureusAutomationLab/n8n-workflows:docs/finecon_bridge/ACCOUNTANT_VALIDATION_CHECKLIST.md` | Accountant validation boundary is explicit. | Does not validate accounting correctness by itself. | Internal source |
| `AureusAutomationLab/n8n-workflows:docs/finecon_bridge/POHODA_LIVE_IMPORT_VALIDATION_REPORT.md` | Controlled live-import evidence exists internally. | Does not become public customer proof. | Internal source |
| `AureusAutomationLab/n8n-workflows:docs/finecon_bridge/POHODA_MAPPING_DIFF_REPORT.md` | Mapping gaps and accountant validation needs are documented. | Does not claim final mapping correctness. | Internal source |
| `AureusAutomationLab/n8n-workflows:scripts/finecon-e2e-preflight.ps1` | E2E preflight coverage exists internally. | Does not run live workflows from this public profile. | Internal source |
| `AureusAutomationLab/FinEcon:finecon-pocket.html` | FinEcon Pocket is represented in the site layer. | Does not expose app internals. | Internal source |
| `AureusAutomationLab/FinEcon:efakturacia-2027.html` | Public-facing FinEcon site copy explains Pocket, folders, UBL, and POHODA output direction with boundaries. | Does not provide legal/accounting advice. | Internal source |

## Approval-Safe Sales Machine

| Source | What it proves | What it does not prove | Public-safe status |
| --- | --- | --- | --- |
| `public-proof/sales-machine/README.md` | Public-safe sales automation proof package exists. | Does not claim sent campaigns or customer results. | Public |
| `public-proof/sales-machine/workflow-map.md` | Shows lead source to reporting flow. | Does not expose private lead lists or inbox data. | Public |
| `public-proof/sales-machine/safe-state-model.md` | Shows no blind-send state model. | Does not prove live outreach. | Public |
| `public-proof/sales-machine/buyer-example.md` | Gives a fictional buyer example. | Does not claim real customer proof. | Public |

## Aureus OS

| Source | What it proves | What it does not prove | Public-safe status |
| --- | --- | --- | --- |
| `public-proof/aureus-os/README.md` | Public-safe Aureus OS operating-model proof exists. | Does not expose internal control plane implementation. | Public |
| `public-proof/aureus-os/operating-model.md` | Shows mission to handoff flow. | Does not claim AI can run the company alone. | Public |
| `public-proof/aureus-os/action-gates.md` | Shows approval-gated actions. | Does not authorize live actions. | Public |
| `docs/portfolio/solution-architecture.md` | Explains architecture layers and boundaries. | Does not expose private runtime state. | Public |
| `docs/proof/source-truth-map.md` | Maps public claims to source-truth families. | Does not publish private source repositories. | Public |

## Public Proof Website + Automation

| Source | What it proves | What it does not prove | Public-safe status |
| --- | --- | --- | --- |
| `README.md` | Public profile is a portfolio front door. | Does not claim client results. | Public |
| `public-proof/README.md` | Public proof showroom exists. | Does not expose private implementation. | Public |
| `docs/portfolio/public-boundary.md` | Public/private boundary is explicit. | Does not certify compliance. | Public |
| `docs/portfolio/review-guide.md` | Different audiences have review paths. | Does not replace a live sales process. | Public |
| `AureusAutomationLab/FinEcon:*.html` | FinEcon site has product/story pages and SEO surfaces. | Does not prove production customer adoption. | Internal source |

## Rule

Use source-backed evidence to strengthen clarity. Do not convert private implementation into public exposure.
