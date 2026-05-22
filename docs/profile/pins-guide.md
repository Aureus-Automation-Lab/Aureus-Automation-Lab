# Profile Pins Guide

![Aureus public proof pack](../../assets/aureus-proof-pack.gif)

| Page signal | What this guide prevents |
| --- | --- |
| Public proof | pinned items should be polished, understandable, and safe for external reviewers |
| Review path | pins should form a portfolio path, not a random repo list |
| Safety boundary | private/internal repos should not be pinned for public reviewers |

## Aureus-Aligned Pin Strategy

Pins should make the profile understandable in under 10 seconds. The order should show a buyer or reviewer what Aureus Automation Lab and Róbert Kolesár build before they see deeper technical artifacts.

For the final candidate list, use [PUBLIC_PIN_CANDIDATES.md](public-pin-candidates.md).

1. `Aureus-Automation-Lab/Aureus-Automation-Lab` - public front door for the portfolio.
2. FinEcon / invoice automation public-safe surface - reviewed document and invoice workflow direction.
3. Sanitized n8n workflow demo or review map - controlled workflow design with review and evidence boundaries.
4. AOP public architecture artifact - internal operating engine, sanitized for public review.
5. Public demo/proof repo - small polished example that shows build quality without private context.
6. Template or utility repo - simple technical hygiene signal if polished and safe.

If no public-safe implementation repo exists yet, create a sanitized demo repo instead of exposing private repos.

## Visual Quality For Pins

A pinned repo should have at least one meaningful visual or diagram near the top of the README. Prefer architecture visuals, workflow maps, proof-pack diagrams, or sanitized screenshots over generic badges.

Do not pin a repo that visually looks unfinished, even if the code is strong.

Do not pin private repos expecting public reviewers to see them. Do not pin unfinished or confusing repos without README/status.

GitHub profile pins are managed manually from the GitHub profile UI. Private repositories should not be pinned for public reviewers because they will not be visible to most visitors.

## Recommended Pin Captions

| Pin | Caption |
| --- | --- |
| Profile repo | AI automation architecture portfolio: controlled workflows, review boundaries, evidence, and public-safe proof paths. |
| FinEcon surface | Reviewed document and invoice workflow direction with human approval boundaries. |
| n8n workflow demo | Workflow-as-system thinking: review, validation, failure handling, and handoff. |
| AOP architecture | Internal operating engine for scoped AI-assisted work, action gates, evidence, and handoff. |
| Demo/proof repo | Small public-safe proof of implementation quality and clarity. |
| Template/utility | Focused technical hygiene without private context. |

## Recommended Pin Categories

1. Profile repo `Aureus-Automation-Lab/Aureus-Automation-Lab`.
2. Public/review-safe FinEcon or invoice automation surface if available.
3. Public demo or sanitized n8n workflow demo if available.
4. AOP public architecture artifact only if sanitized.
5. Template or small service repo if polished.
6. Case-study gist if no repo is public-safe.

## Recommended Pin Order

1. `Aureus-Automation-Lab/Aureus-Automation-Lab`.
2. Sanitized Aureus AOP architecture gist or demo repo.
3. Automation Audit public-safe process map gist/demo.
4. Invoice / FinEcon public-safe workflow gist/demo.
5. Web Studio / Figma-to-code public-safe demo if visually ready.
6. Template or health demo repo if public/review-safe.

If no public-safe implementation repo exists yet, create a sanitized demo repo instead of exposing private repos.

## Pinning Rules

- Do not pin private repos expecting public reviewers to see them.
- Do not pin unfinished or confusing repos without README/status.
- Do not pin repos that contain private workflow exports, endpoints, credentials, logs, client-like data, or unsupported claims.
- Prefer fewer polished pins over many unclear repos.

## Good Pin Signals

A good pinned repo or gist should have:

- clear purpose,
- public-safe README,
- honest status,
- no private data,
- obvious review path,
- visible architecture or implementation signal.
