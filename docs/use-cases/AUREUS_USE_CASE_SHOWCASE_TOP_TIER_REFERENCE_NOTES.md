# Aureus Use Case Showcase Top-Tier Reference Notes

These notes explain the design direction behind the Pro Tier V6 export and the Client-Language V7 rewrite.

The goal is not to copy any external company. The goal is to use the same public-safe structure that strong enterprise AI and consulting materials use:

```text
business situation -> controlled solution -> review / proof -> business decision -> next step
```

## Reference Patterns Reviewed

| Source | Pattern used for Aureus |
| --- | --- |
| OpenAI business guide on identifying and scaling AI use cases | Start with the right use case, not with the model. Look for repeated work, bottlenecks, review sensitivity, available data/evidence, and a bounded pilot. |
| Microsoft Customer Stories | Make the buyer problem and operational outcome visible before technical detail. |
| IBM case studies | Use clear challenge / solution / proof language and keep the story understandable to non-technical readers. |
| Accenture case studies | Keep business value, transformation path, and next action easy to scan. |

## Design Decisions

- One dominant visual per use-case page.
- No text boxes placed on top of detailed image areas.
- Fixed two-column layout for every use-case page.
- Same content order on every use case:
  - buyer problem,
  - controlled workflow,
  - client receives,
  - AI prepares,
  - people approve,
  - evidence remains,
  - proof status,
  - best first step.
- Shorter copy inside cards to keep the page readable during screen share.
- More concrete FinEcon wording, with the accountant-validation boundary preserved.
- Clear scorecard and 30-day pilot path for sales conversations.

## What Changed From V5

V5 preserved the original v4 PDF as a full-page background and then redrew text on top. That kept the visual mood, but it could create alignment issues and old-text ghosting.

V6 uses the original visuals only as cropped conceptual panels. Client-Language V7 keeps the same grid, but rewrites the copy around plain buyer questions: what problem is being solved, what the system prepares, what a person approves, what record remains, and what the client should do next.

## Safety Boundary

The showcase remains public-safe:

- no private workflow exports,
- no private webhook URLs,
- no credentials,
- no real invoices,
- no client data,
- no customer-result claims,
- no accounting-correctness claim,
- no claim that FinEcon replaces an accountant.

FinEcon is described as internally validated through controlled proof, with accountant validation still pending for accounting correctness.
