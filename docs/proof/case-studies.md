# Case Studies

These are public-safe case study directions. They show system thinking without exposing private implementation, workflow exports, credentials, endpoints, invoices, logs, client-like data, or unsupported claims.

The useful review pattern is:

```text
Problem
-> System shape
-> AI role
-> Review boundary
-> Public-safe proof
-> What stays private
```

For the premium root version, see [pro-tier public case studies](../portfolio/case-studies.md).

The portfolio version now covers Automation Audit, n8n Review, n8n Build, Sales Machine, FinEcon, Aureus OS, Premium AI Website + Automation, Git-backed LinkedIn content, and Monthly Automation Partner.

## 1. Manual Invoice / Document Work

| Step | Public-safe explanation |
| --- | --- |
| Problem | Documents arrive across email, folders, and manual processes. Review is slow and state is unclear. |
| System shape | Intake, extraction draft, validation checks, exception queue, owner review, evidence note, downstream handoff direction. |
| AI role | Classify document type, extract draft fields, summarize context, flag missing or uncertain information. |
| Review boundary | A person reviews uncertain fields and approves downstream use. |
| Public-safe proof | Sanitized workflow map, review-state model, evidence-note example. |
| What stays private | Real invoices, POHODA access details, accounting context, workflow exports, endpoints, logs, credentials. |

## 2. n8n Workflow Review

| Step | Public-safe explanation |
| --- | --- |
| Problem | Existing workflows run, but nobody can clearly explain failure handling, ownership, retries, or activation safety. |
| System shape | Workflow inventory, risk review, naming review, state map, failure path, validation checklist, handoff notes. |
| AI role | Help summarize workflow intent, identify missing documentation, draft test cases, and propose review questions. |
| Review boundary | No live import, activation, credential change, or external action without explicit approval. |
| Public-safe proof | Sanitized review checklist, workflow-as-source diagram, risk model. |
| What stays private | Raw n8n exports, workflow IDs, webhook paths, credentials, runtime state, private node details. |

## 3. Controlled Sales Workflow

| Step | Public-safe explanation |
| --- | --- |
| Problem | Leads or inquiries arrive, but qualification, follow-up, and next-step ownership are inconsistent. |
| System shape | Lead intake, qualification state, draft outreach, manual approval, follow-up draft, reply classification, report. |
| AI role | Classify intent, draft follow-up, summarize context, suggest next action. |
| Review boundary | No blind sending. Outreach and client-facing messages stay approved. |
| Public-safe proof | State model, workflow map, fictional buyer example. |
| What stays private | Real leads, inbox data, draft IDs, prompts, workflow IDs, messages, contact data. |

## 4. AI Operating System Setup

| Step | Public-safe explanation |
| --- | --- |
| Problem | AI work is scattered across chats, docs, automations, and people, making it hard to review and trust. |
| System shape | Mission intake, constraints, AI-assisted work, source-controlled delivery, validation, action gate, evidence, handoff. |
| AI role | Draft, classify, summarize, check, propose next steps, and prepare review material. |
| Review boundary | Public claims, financial handoffs, production actions, client-facing outputs, and external messages need approval. |
| Public-safe proof | Operating-model diagram, action-gate guide, fictional buyer example. |
| What stays private | Internal prompts, private repos, production context, customer-like data, logs, credentials. |

## Public Proof Packages

- [Sales Machine proof package](../../public-proof/sales-machine/README.md)
- [FinEcon proof package](../../public-proof/finecon/README.md)
- [Aureus OS proof package](../../public-proof/aureus-os/README.md)

## Boundary

These case studies are not claims of production deployments, revenue results, accounting correctness, trading performance, official compliance certification, or customer outcomes unless separately verified.
