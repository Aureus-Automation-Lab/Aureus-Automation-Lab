# Aureus Use Case Showcase Design Spec V5

This spec turns the V5 copy into a polished PDF, LinkedIn carousel, or presentation deck.

## Design Direction

- Premium dark/light alternating style.
- Strong page title and short subtitle on every page.
- One clear hero visual or diagram per use-case page.
- Large text blocks that remain readable on LinkedIn/mobile.
- No tiny text inside generated images.
- No fake screenshots.
- Conceptual visuals must be labeled as conceptual if they are not real UI.
- Use proof status chips to avoid overclaiming.

## Visual Language

| Element | Direction |
| --- | --- |
| Background | dark navy / graphite for system pages; clean off-white for scorecard and process pages |
| Accent colors | gold for evidence, teal for AI preparation, blue for validation, green for reviewed output |
| Typography | large headings, short paragraphs, no dense walls of text |
| Cards | use 3-4 cards maximum per page, aligned to a grid |
| Images | cinematic but relevant; visual supports the story, text carries the facts |
| Footer | page number, public-safe label, proof status |

## Required Blocks On Use-Case Pages

Every use-case page should include:

- buyer problem,
- what AI prepares,
- what people approve,
- evidence kept,
- client receives,
- proof status chip,
- best first step.

## Proof Status Chips

Use these labels:

- Public-safe concept,
- Internal E2E passed,
- Accountant validation pending,
- Setup-gated,
- Pilot-ready.

## Page Notes

| Page | Design requirement |
| --- | --- |
| 1. Portfolio overview | Balanced grid: left message, right visual collage. Do not let images cover the title or rule card. |
| 2. Discovery model | Use a clean decision model: repeated work, skill bottleneck, ownership/review, evidence readiness, bounded pilot. |
| 3. Automation Audit | Show impact/effort map and pilot brief. Client receives block must be visible. |
| 4. n8n Review + Build | Show trigger, validation, approval, evidence, handoff. Avoid raw n8n screenshots. |
| 5. FinEcon Pocket / Bridge | Make Pocket, review, Bridge, POHODA handoff, proof pack, and accountant boundary visible as separate steps. |
| 6. Sales Machine | Show no-blind-send approval gate and do-not-contact boundary. |
| 7. Aureus OS / AOP | Show mission, validation, action gate, evidence, handoff. AOP is internal engine/control plane. |
| 8. Public Proof Website + Automation | Show public page, intake, review, follow-up, handoff. |
| 9. Scorecard | Keep table spacious. Add recommendation strip at bottom. |
| 10. 30-Day Pilot | Use four week cards with client outputs. |
| 11. How To Use | Show six use channels and safety rules. |
| 12. Best First Step | Strong CTA: Start with Automation Audit. Show buyer action clearly. |

## Export Settings

- PDF: 16:9 landscape or A4 landscape, depending on use.
- LinkedIn carousel: 1080x1350 or 1600x2000 vertical pages.
- Keep margins generous.
- Avoid page content within 48 px of edges.
- Export images at high quality, but keep final file size reasonable.

## Safety Notes

- Do not include private workflow exports, credentials, route details, real invoices, private screenshots, local paths, runtime logs, or client records.
- Do not present conceptual visuals as real client/customer proof.
- Do not claim accounting correctness until accountant validation is complete.
