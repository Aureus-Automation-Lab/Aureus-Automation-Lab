# Case Studies

These are public-safe case study directions. They show system thinking without exposing private implementation, customer data, production context, or unsupported claims. For the full exclusion list, see [public boundary](public-boundary.md).

The useful pattern is:

```text
Problem
-> System shape
-> AI role
-> Review boundary
-> Public-safe proof
-> What stays private
```

## 1. Manual Invoice / Document Work

| Step | Public-safe explanation |
| --- | --- |
| Problem | Documents arrive across email, folders, and manual processes. Review is slow, status is unclear, and downstream accounting-style handoff needs care. |
| System shape | Pocket-style intake, extraction draft, validation checks, exception queue, owner review decision, bridge-readiness guard, evidence note, downstream handoff direction. |
| AI role | Classify document type, extract draft fields, summarize context, flag missing or uncertain information. |
| Review boundary | A person reviews uncertain fields and approves downstream use. Accountant validation remains required for accounting-sensitive conclusions. |
| Public-safe proof | Source-backed FinEcon workflow-family summary, review-state model, Pocket/bridge/proof direction, evidence-note example. |
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

For the older detailed case-study library, see [case studies detail](../proof/case-studies.md).
