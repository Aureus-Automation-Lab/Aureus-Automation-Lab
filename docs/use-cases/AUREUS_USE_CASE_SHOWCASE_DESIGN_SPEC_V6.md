# Aureus Use Case Showcase Design Spec V6

V6 is the preferred pro-tier PDF format for client conversations.

## Core Direction

The deck should feel like a premium AI automation architecture portfolio, not a raw documentation export.

The visual system follows this story:

```text
manual business chaos -> controlled AI workflow -> human approval -> evidence -> next decision
```

## Layout Rules

- 16:9 landscape.
- Fixed margins on every page.
- One primary headline per page.
- One dominant visual panel only where it adds meaning.
- No floating text over busy images.
- No random decorative boxes.
- Every use-case page uses the same grid:
  - left: problem, workflow, client receives,
  - right: visual, AI prepares, people approve, evidence, proof status,
  - bottom: best first step.

## Typography Rules

- Large page titles.
- Short card titles.
- Client-readable body copy.
- No dense paragraphs on visual pages.
- Slovak version must use correct diacritics and natural local wording.

## Visual Rules

- Use conceptual visuals as supporting panels, not fake screenshots.
- Do not depend on tiny text inside generated visuals.
- The reader must understand the page even if they ignore the image.
- Dark pages use high-contrast white / soft gray text.
- Light pages use a clean consulting-style table or card layout.

## Content Rules

Every use case must answer:

1. What business problem does this solve?
2. What does AI prepare?
3. What do people approve?
4. What evidence remains?
5. What does the client receive?
6. What is the safe first step?

## Proof Status Chips

Use proof status chips carefully:

- First purchase
- Pilot-ready
- Setup-gated
- Public-safe
- No blind send
- Internal E2E passed
- Accountant validation pending

Do not use unsupported claim language such as:

- claims that production use is already verified when it is not,
- ROI guarantees,
- claims that accounting correctness is already professionally confirmed,
- replaces accountant,
- certified.

## Preferred Generator

```powershell
python scripts\generate-aureus-use-case-pdfs-v6-pro.py
```

This creates:

- `exports/Aureus_Use_Case_Showcase_Pro_Tier_V6_EN.pdf`
- `exports/Aureus_Use_Case_Showcase_Pro_Tier_V6_SK.pdf`

The files are also copied to the OneDrive desktop folder when available.
