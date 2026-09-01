# Aureus Automation Lab

**Controlled AI automation and financial workflow operating systems for companies that need work to be clearer, safer, and faster.**

Made by Róbert Kolesár and Patrik Trnavský

![Aureus controlled AI automation hero](assets/aureus-profile-hero.gif)

## What Aureus does

Aureus helps companies turn scattered manual work into controlled AI-assisted workflows.

A real business process is mapped, repeated steps are automated, uncertain steps are routed to a human reviewer, and the system maintains a complete, verifiable audit trail.

```text
AI prepares.
People approve.
The system keeps evidence.
```

## Products and Systems

| System | What it helps with | Architecture & Typical Output |
| :--- | :--- | :--- |
| **FinEcon Ecosystem**<br>*(Core, Pocket & ePoštár)* | End-to-end finance workflow: mobile expense capture, AI extraction, pre-accounting classification, POHODA ERP mServer bridge, and e-Faktúra 2026/2027 ePoštár/Peppol gateway. | • **FinEcon Pocket:** Flutter iOS/Android client<br>• **FinEcon Core:** n8n orchestration & accounting logic<br>• **POHODA Bridge:** Native XML (`PriFaktury`, `VydFaktury`, `Pokladna`)<br>• **ePoštár Gateway:** Peppol BIS Billing 3.0 & UBL 2.1 XML |
| **Aureus Automation Lab** | Sales follow-up, operations workflows, document routing, reporting, n8n automations, and review queues. | Workflow map, automated routing, approval flow, daily operations summary, and handoff notes. |
| **Aureus OS** | Scope, validation, action gates, evidence, and handoff governance for enterprise AI work. | Operating model, safety approval gates, evidence ledgers, and repeatable delivery pipelines. |

Open the dedicated product pages:

- [FinEcon Ecosystem (Core, Pocket, ePoštár)](docs/products/finecon.md)
- [Automation Lab](docs/products/automation-lab.md)
- [Aureus OS](docs/products/aureus-os.md)

## What you can start with

| Offer | Best when | What you get |
| :--- | :--- | :--- |
| **FinEcon Pilot** | Receipts, invoices, finance documents, or accounting handoff needs complete structure and automation. | Production-grade finance workflow connecting Pocket intake, AI pre-accounting, and POHODA/ePoštár integration. |
| **Automation Audit** | You know work is too manual, but not what to automate first. | Process map, risk points, automation candidates, and first high-ROI scope. |
| **n8n Workflow Review** | Existing workflows feel fragile, unmonitored, or unclear. | Review notes, failure points, retry/safety boundaries, and improvement plan. |
| **n8n Workflow Automation Build** | A repeated business process needs reliable, production-grade automation. | Workflow design, validation notes, approval boundaries, and handoff direction. |
| **Aureus OS Setup** | A team wants to deploy AI across real operations without losing governance. | Operating model for scope, ownership, review, validation, evidence, approvals, and handoff. |
| **Monthly Automation Partner** | You need ongoing improvement, monitoring, and infrastructure maintenance. | Practical monthly support for automation operations, new pipelines, and delivery maintenance. |

Open the full offer menu: [docs/products/offers.md](docs/products/offers.md)

## Public Proof Showroom

These are public-safe proof packages. They demonstrate architecture, data flow, and workflow governance without exposing private implementation or client data.

| Proof path | Visual | What it shows |
| :--- | :--- | :--- |
| [FinEcon Ecosystem](public-proof/finecon/README.md) | <img src="assets/aureus-finecon-flow.gif" width="220" alt="FinEcon review flow"> | Mobile capture (Pocket), AI parsing, accounting classification, POHODA mServer XML, and ePoštár Peppol gateway. |
| [Sales Machine](public-proof/sales-machine/README.md) | <img src="assets/aureus-sales-machine.gif" width="220" alt="Sales Machine flow"> | Sales follow-up with qualification, approval, reply handling, and reporting. |
| [Aureus OS](public-proof/aureus-os/README.md) | <img src="assets/aureus-os-model.gif" width="220" alt="Aureus OS operating model"> | How AI-assisted work becomes scoped, reviewed, validated, evidenced, and handed off. |

Open the showroom: [public-proof/README.md](public-proof/README.md)

## Why this is different

Most automation projects stop at “the workflow runs once.”

Aureus focuses on what a company actually needs in real daily operations:

- **Strict Human-in-the-Loop:** High-consequence decisions (accounting ledgers, payments) stop for explicit review.
- **Deep Accounting Intelligence:** Native understanding of Slovak/CEE accounting standards (predkontácie `518`/`501`/`602`/`604`, reverse-charge, CAR 50:50 / 80:20 fuel splits).
- **Future-Proof E-Invoicing:** Ready for the mandatory European and Slovak e-Faktúra 2026/2027 rollout via Peppol BIS 3.0 and ePoštár.
- **Tamper-Evident Evidence:** Cryptographic SHA-256 proof packs and state transition ledgers for every processed document.
- **Zero Unintended Side Effects:** Dry-run modes, preflight connection checks, and clean error recovery.

## Proof Without Exposure

![Aureus public/private boundary](assets/aureus-public-boundary.gif)

This profile showcases products, workflow architectures, proof packages, safety boundaries, and review models.

It does **not** expose private implementation secrets, real customer data, credentials, production tokens, local computer paths, or unsupported claims.

Read the public boundary: [docs/products/public-boundary.md](docs/products/public-boundary.md)

## Review Path

| If you are a... | Start here |
| :--- | :--- |
| **Finance / Accounting Reviewer** | [FinEcon Ecosystem](docs/products/finecon.md) and [FinEcon Proof Showroom](public-proof/finecon/README.md) |
| **Client / Partner** | [Offer Menu](docs/products/offers.md) |
| **Operations Reviewer** | [Automation Lab](docs/products/automation-lab.md) |
| **Technical Reviewer** | [Aureus OS](docs/products/aureus-os.md) and [Public Proof Showroom](public-proof/README.md) |

## Public Pages

- [Automation Lab](https://aureus.it.com/automationlab)
- [FinEcon Finance Direction](https://aureus.it.com/finecon)

## One Sentence

Aureus Automation Lab builds controlled, enterprise-grade AI automation and finance operating systems connecting mobile capture, intelligent workflows, ERPs, and electronic invoicing.
