# Aureus Use Case Content Model

Every Aureus use case should use the same public-safe structure. This keeps the offer clear, comparable, and safe to reuse in PDF, LinkedIn, GitHub, and proposal formats.

## Canonical Structure

| Section | Purpose |
| --- | --- |
| 1. Title | Names the use case in buyer language. |
| 2. One-line promise | Explains the useful outcome without hype. |
| 3. Buyer problem | Describes the painful business situation before Aureus. |
| 4. What AI prepares | States what AI can safely draft, inspect, classify, summarize, or structure. |
| 5. What people approve | States the human review boundary before sensitive action. |
| 6. What evidence remains | Names the proof artifacts: map, note, checklist, status, log, handoff, or proof pack. |
| 7. Controlled workflow | Shows the ordered flow from input to reviewed business output. |
| 8. What client receives | Makes the deliverable concrete. |
| 9. Proof status | Labels the current proof level without overclaiming. |
| 10. Boundaries / what we do not claim | Prevents unsupported claims. |
| 11. Best first step | Tells the buyer what to send or approve next. |
| 12. Git-backed truth notes | Maps the public message to source-backed evidence without exposing private implementation. |

## Proof Status Chips

Use one or more chips per use case:

| Chip | Meaning |
| --- | --- |
| Public-safe concept | Safe to explain publicly, but not a customer outcome claim. |
| Internal E2E passed | Validated in controlled internal evidence. Not public customer proof. |
| Accountant validation pending | Finance/accounting-sensitive interpretation still needs professional review. |
| Setup-gated | Useful only after credentials, permissions, or owner approval are configured. |
| Pilot-ready | Suitable for a scoped paid pilot with review boundaries. |

## Core Rule

```text
AI prepares. People approve. Evidence remains.
```

This rule must appear in every format derived from the showcase.

## Claim Discipline

Use:

- "internal proof",
- "validated in controlled test",
- "public-safe concept",
- "reviewed handoff",
- "accountant validation boundary",
- "pilot direction".

Avoid:

- promised results,
- customer outcome claims,
- accounting correctness claims,
- tax/legal advice,
- blind automation,
- claims that AI replaces professional review.
