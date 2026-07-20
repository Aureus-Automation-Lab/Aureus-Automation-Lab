# Aureus Use Case Showcase Evidence Audit

This audit reviews the 12-page showcase against observable gates. It does not assign subjective quality scores or certify client readiness.

## Status Model

| Status | Meaning |
| --- | --- |
| `PASS` | The page already contains the required buyer, proof, and safety signal. |
| `REPAIR_REQUIRED` | A concrete content or evidence gap remains. |
| `VISUAL_QA_REQUIRED` | Copy may be usable, but rendered desktop and mobile proof is still required. |
| `APPROVAL_REQUIRED` | Publishing or using the artifact externally needs the applicable live approval. |

The shared message remains:

```text
AI prepares. People approve. Evidence remains.
```

## Page-By-Page Gate Matrix

| Page | Current gate | Evidence or gap | Required next action |
| --- | --- | --- | --- |
| Portfolio overview | `REPAIR_REQUIRED` | The six examples are present, but the opening promise and visual density still need rendered review. | Tighten the promise and verify the first page at mobile and PDF sizes. |
| Use-case discovery model | `REPAIR_REQUIRED` | The intended path exists but can still read as generic methodology. | Express the path as discover, assess, design, build, review, and scale. |
| Automation Audit | `PASS` | It is identified as the recommended first purchase with a concrete buyer outcome. | Preserve the explicit client-receives block. |
| n8n Workflow Review + Build | `PASS` | Failure paths, credentials, ownership, validation, and handoff are in scope. | Keep all live actions behind the stated approval boundary. |
| Aureus FinEcon — Pocket / Bridge modules | `REPAIR_REQUIRED` | Source-backed components are described, while accountant validation remains pending. | Keep Pocket, Bridge, proof publishing, and the accountant boundary separate. |
| Aureus Sales Workflow | `PASS` | Message and claim approval are explicit; blind outreach is excluded. | Preserve the fictional-data and no-live-outreach labels. |
| Aureus OS | `REPAIR_REQUIRED` | The control-layer role is present but can be mistaken for the first product sold. | Keep Aureus OS as the operating layer and make the first commercial step concrete. |
| Public Proof Website + Automation | `REPAIR_REQUIRED` | The offer-to-operation path exists but needs a clearer handoff and evidence map. | Connect offer, intake, owner review, proof-safe claim, and handoff. |
| Client Use-Case Decision Matrix | `PASS` | Buyer situations map to a recommended first pilot. | Keep recommendations tied to observable buyer constraints. |
| 30-Day Client Pilot Path | `REPAIR_REQUIRED` | Weekly stages exist; acceptance evidence by day 30 needs to remain explicit. | Define the artifact, validation, owner decision, and handoff for each week. |
| How To Use This Showcase | `PASS` | Sales call, PDF, carousel, GitHub, and proposal contexts are identified. | Use only the channel-specific approved export. |
| Best First Step | `PASS` | Automation Audit is the default call to action and the requested input is bounded. | Preserve one clear next action. |

## Cross-Artifact Gates

| Gate | Current status | Acceptance evidence |
| --- | --- | --- |
| Buyer clarity | `REPAIR_REQUIRED` | Every page names the buyer problem, delivered artifact, and next decision. |
| Claim safety | `PASS` | No guaranteed outcome, customer, certification, or production claim is required to understand the offer. |
| Public/private boundary | `PASS` | Private implementation, credentials, endpoints, payloads, and production evidence remain excluded. |
| Source alignment | `REPAIR_REQUIRED` | Every source-backed statement maps to the public proof index or an explicit limitation. |
| Accessibility and legibility | `VISUAL_QA_REQUIRED` | Rendered desktop, PDF, and mobile screenshots show readable text, hierarchy, contrast, and safe cropping. |
| External use | `APPROVAL_REQUIRED` | The exact export, channel, claim review, and approval receipt are recorded before publication or sending. |

## Promotion Rule

The showcase is eligible for an external channel only when all `REPAIR_REQUIRED` and `VISUAL_QA_REQUIRED` gates for that exact export are closed, the public/private boundary remains clean, and the channel has its required approval receipt. A Markdown file, generated PDF, or internal review alone is not evidence that the visual artifact is client-ready.
