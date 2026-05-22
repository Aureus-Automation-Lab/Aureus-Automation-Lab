# Public Demo Flow

This is a public-safe demo flow. It explains the work pattern without exposing private workflows, endpoints, credentials, customer data, invoices, logs, or production context.

## Scenario: Manual Business Process

A company handles invoices, requests, approvals, and follow-ups across email, spreadsheets, shared folders, chat messages, and memory.

The work is not broken because people are careless. It is broken because the process has no reliable operating layer.

## Before

- Inputs arrive from multiple places.
- A person copies or retypes information.
- The next step depends on memory.
- Unclear items wait in someone else's inbox.
- Nobody can quickly explain what happened later.

## Controlled AI Workflow

```text
business signal
-> process map
-> structured workflow logic
-> AI-assisted draft / extraction / classification
-> review queue
-> evidence note
-> next-step proposal
```

AI may help prepare the work. It can classify a request, extract draft fields, summarize context, flag missing information, or suggest the next step.

## Review Boundary

Important actions stay human-approved.

Examples:

- sending an external message,
- approving a finance/document handoff,
- changing a production workflow,
- making a public claim,
- accepting uncertain extracted data.

## Evidence / Proof Output

Each important flow should leave a useful record:

- what entered the system,
- what AI prepared,
- what needed review,
- who or what approved the next step,
- what changed,
- where the output went.

## Business Output

The output is not just an automation run.

The useful output is a clearer business step: a reviewed document queue, a follow-up draft ready for approval, an exception list, a report, a handoff note, or a scoped proposal for the next automation block.

## What Stays Private

Private implementation stays private:

- workflow exports,
- credentials,
- endpoints,
- webhook URLs,
- real invoices,
- real leads,
- customer-like records,
- production logs,
- private prompts,
- internal screenshots.

## Why It Matters

The system does not ask the company to trust AI blindly.

It creates a controlled path from manual work to reviewed output, with enough evidence for a person to understand what happened and decide what should happen next.
