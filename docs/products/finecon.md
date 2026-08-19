# FinEcon

FinEcon is the Aureus finance and document intelligence direction.

It helps companies collect, structure, check, and prepare business documents before they move into an accounting application, accountant workflow, or owner review.

## What it helps with

FinEcon can support workflows around:

- receipts and small expense documents,
- supplier invoices,
- issued invoices,
- income and cost documents,
- supporting accounting records,
- missing-data checks,
- finance summaries,
- cashflow, cost, revenue, and reporting visibility,
- reviewed downstream handoff.

## Simple and double-entry accounting workflows

FinEcon can support document-preparation workflows for both simple accounting and double-entry accounting environments.

This does not mean FinEcon replaces an accountant. It means the system can help organize documents, extract candidate fields, mark missing information, prepare review notes, and make handoff into an accounting application or accountant workflow clearer.

## Workflow shape

```text
document / invoice intake
-> candidate field extraction
-> validation and missing-data checks
-> exception queue
-> owner or operator review
-> finance summary
-> reviewed handoff to accounting application or accountant
```

## Typical candidate fields

Depending on the document type, FinEcon may help prepare candidate fields such as supplier, customer, document number, issue date, due date, amount, VAT-related fields where applicable, payment status, category, note, and review status.

These fields are candidates for review, not final accounting truth.

## Accounting application handoff

FinEcon can prepare reviewed document data for downstream handoff into an accounting application or accountant workflow.

This can include document status, extracted candidate fields, missing-data notes, exception state, review state, and handoff notes.

## Professional boundary

FinEcon does not claim accounting correctness, tax advice, legal advice, or replacement of professional review.

Accounting-sensitive, tax-sensitive, legal, payment, or official record decisions require appropriate human and professional review.

## Public proof

Open the [FinEcon proof package](../../public-proof/finecon/README.md) for the public-safe invoice/document review flow.
