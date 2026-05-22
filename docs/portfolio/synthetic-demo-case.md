# Synthetic Demo Case: Manual Invoice Review Flow

## This Is Fictional And Public-Safe

This example uses fictional data only. It is not a real invoice, real company, VAT ID, email, person name, client record, production workflow, accounting result, or customer outcome.

## Before

A small operations team receives supplier invoices in several places. One person downloads files, copies fields into a spreadsheet, asks for missing context in chat, and later tries to remember which invoices were reviewed.

The problem is not effort. The problem is that the process has no reliable review trail.

## Input Example

```text
Document type: supplier invoice
Supplier label: Example Office Supplies
Amount label: 418.90 EUR
Date label: 2026-04-18
Missing context: approver, cost category, payment status
```

The example is deliberately synthetic and incomplete.

## Controlled Workflow

```text
document received
-> draft field extraction
-> validation checks
-> exception queue
-> owner review
-> evidence note
-> downstream handoff proposal
```

## AI-Assisted Step

AI may prepare draft fields, summarize missing information, classify the document type, and suggest review questions.

It does not approve payment, decide accounting treatment, replace professional review, or push data into a finance system without approval.

## Human Review Boundary

A person reviews uncertain fields before downstream use:

- supplier identity,
- amount and date,
- approver,
- cost category,
- exception notes,
- final handoff decision.

## Evidence / Proof Output

The workflow should leave a simple record:

- what document was reviewed,
- which fields were drafted,
- which fields were uncertain,
- what the owner approved,
- what still needs attention,
- what next step was proposed.

## Business Output

The output is a cleaner review queue and a next-step handoff proposal, not an automatic accounting decision.

## What This Demonstrates

- process mapping,
- AI-assisted extraction,
- validation thinking,
- human approval boundaries,
- evidence/proof-pack discipline,
- public-safe explanation of a private business workflow.

## What It Does Not Claim

This demo does not claim accounting correctness, tax/legal advice, production deployment, customer results, promised savings, or verified ROI.
