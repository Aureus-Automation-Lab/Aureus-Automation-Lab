# Aureus FinEcon — Pocket / Bridge modules Use Case One-Pager

FinEcon is a reviewed finance/document workflow direction. It helps move documents from intake to structured review, controlled handoff, proof notes, and accountant validation boundaries.

It does not replace accountants, provide tax/legal advice, or claim accounting correctness before professional review.

## What It Solves

Companies often receive invoices, receipts, and supporting documents through email, mobile photos, shared folders, chats, or delayed manual uploads.

The operational risk is not only extraction. The risk is that no one can clearly answer:

- where the document entered,
- who owns the next step,
- what was reviewed,
- what is ready for downstream handoff,
- what proof remains,
- what still needs accountant validation.

## How Pocket Works

FinEcon Pocket is the intake layer for documents at the source. It is useful when documents appear in the field, at a branch, from a client, or before the back office has clean context.

Pocket can support:

- document capture,
- company registration direction,
- status tracking,
- review actions,
- bridge-start direction,
- handoff visibility.

## How Folders / Intake Work

Pocket is not the only possible intake path.

FinEcon can also be described as taking documents from prepared folders when that is more natural for the company. The important point is that both paths should end in one governed intake layer:

```text
Pocket upload or prepared folder
-> document state
-> review queue
-> bridge readiness
-> proof record
```

## How Review Works

Review is the point where FinEcon stays safe.

AI may prepare candidate fields, context, classifications, and risk notes. A person still reviews uncertain information, accounting-sensitive interpretation, exceptions, and downstream actions.

## How Bridge Works

The Bridge layer is the controlled path between reviewed document work and POHODA handoff direction.

It includes readiness checks, reviewed handoff direction, post-import writeback direction, and proof-pack discipline.

## What Gets Handed To POHODA

Public-safe description:

- structured document context,
- reviewed handoff direction,
- readiness status,
- exception notes where needed,
- proof-pack / writeback direction.

Private implementation details, internal IDs, endpoint details, credentials, payloads, and real documents are not exposed.

## What Proof Remains

FinEcon proof can include:

- intake status,
- review decision,
- bridge readiness note,
- proof pack,
- exception list,
- downstream handoff note,
- accountant validation checklist.

## What Accountant Must Still Validate

The accountant or qualified professional must validate:

- accounting-sensitive interpretation,
- VAT / tax-sensitive treatment where relevant,
- accounting mapping,
- official record correctness,
- cleanup or correction decisions,
- whether a document is ready for official downstream use.

## What We Can Safely Claim

Public-safe claim:

```text
FinEcon has a source-backed Pocket + n8n + Bridge + proof-pack direction with internal controlled evidence through Pocket, Bridge, and POHODA handoff boundaries.
```

The source-backed workflow family includes:

- FinEcon 13 - Pocket Document Intake,
- FinEcon 14 - Pocket Status API,
- FinEcon 15 - Pocket Review Action,
- FinEcon 16 - Pocket Bridge Start,
- FinEcon 17 - Pocket Company Registration,
- FinEcon 09 - Bridge Review to POHODA,
- FinEcon 10 - Bridge Preflight & Runtime Readiness,
- FinEcon 11 - Bridge Live Import,
- FinEcon 12 - Bridge Post-Import Writeback & Proof Pack,
- FinEcon 19 - Proof Pack Drive Publisher.

Internal status evidence says:

- Core E2E passed,
- FinEcon Pocket to POHODA passed,
- POHODA live import passed across three configured mServer environments,
- proof storage local proof is OK and Drive Publisher is active/configured.

## What We Cannot Claim Yet

We cannot claim:

- accounting correctness,
- tax/legal advice,
- replacement of accountant review,
- customer production outcome,
- broad market adoption,
- promised financial result,
- unattended accounting authority.

Accounting correctness and cleanup remain pending accountant validation.

## Next Proof Needed

The next proof should be:

- accountant validation of mapping and review outcomes,
- broader benchmark on a larger document set,
- public-safe client demo packaging,
- final UX proof for a buyer-facing walkthrough,
- pilot scope with agreed review and evidence boundaries.
