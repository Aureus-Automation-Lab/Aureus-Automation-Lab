# Aureus OS Operating Model

This is a public-safe operating model. It does not include private prompts, private repos, workflow IDs, endpoints, or production logs.

```mermaid
flowchart LR
    A[Mission / task] --> B[Scope and constraints]
    B --> C[AI-assisted work]
    C --> D[Source-controlled delivery]
    D --> E[Validation]
    E --> F[Action gate]
    F --> G[Evidence]
    G --> H[Handoff]
```

## Layer Explanation

| Layer | Plain-language meaning |
| --- | --- |
| Mission / task | Define what needs to happen and why it matters. |
| Scope and constraints | Decide what is in scope, out of scope, risky, or owner-controlled. |
| AI-assisted work | AI drafts, classifies, summarizes, reasons, or proposes next actions inside boundaries. |
| Source-controlled delivery | Important work is kept reviewable through files, docs, commits, or structured artifacts where appropriate. |
| Validation | Outputs are checked before they are trusted. |
| Action gate | Sensitive next actions stop until a human approves. |
| Evidence | The system records what was checked, approved, blocked, or still uncertain. |
| Handoff | The next person can understand the work without relying on hidden memory. |

## Why This Matters

AI can make work faster. Aureus OS is about making it reviewable, safe, and handoff-ready.
