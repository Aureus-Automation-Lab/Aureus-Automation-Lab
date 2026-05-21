# Public Proof Index

This page explains how to evaluate the public Aureus GitHub profile.

The profile is intentionally public-safe. It does not expose raw private implementation or customer-like data. It shows architecture, operating discipline, safety boundaries, and proof direction.

## Primary Public Proof Artifacts

The `docs/proof` pages explain the proof philosophy. The `public-proof` packages show concrete public-safe proof objects that can later be converted into pinned gists or public mini-repos.

| Proof package | What it contains |
| --- | --- |
| [Sales Machine proof package](../../public-proof/sales-machine/README.md) | workflow map, safe lead state model, fictional buyer example |
| [FinEcon proof package](../../public-proof/finecon/README.md) | invoice review flow, review boundary, fictional buyer example |
| [Aureus OS proof package](../../public-proof/aureus-os/README.md) | operating model, action gates, fictional buyer example |

## What This Repository Is Meant To Prove

| Signal | What to look for |
| --- | --- |
| **Clear positioning** | Aureus builds AI automation, FinEcon, and Aureus OS / AOP |
| **Architecture thinking** | business process -> workflow -> AI role -> review -> validation -> handoff |
| **Safety discipline** | no blind external actions, no public secrets, no unsupported claims |
| **Workflow maturity** | workflow-as-source, n8n governance, validation gates |
| **Finance boundary awareness** | FinEcon supports insight and reviewed handoff, not unsupported accounting guarantees |
| **Public/private separation** | public proof without leaking private implementation |

## Best Reading Order

1. [README.md](../../README.md) - understand the whole profile in one page.
2. [Start here](../overview/start-here.md) - read the simplest non-technical explanation.
3. [One-page profile](../overview/one-pager.md) - use this as the short external-safe summary.
4. [Build menu](../services/build-menu.md) - see where a first project can start.
5. [Public proof showroom](../../public-proof/README.md) - review concrete public-safe proof objects.
6. [Sales Machine proof package](../../public-proof/sales-machine/README.md) - review sales workflow map and state model.
7. [FinEcon proof package](../../public-proof/finecon/README.md) - review invoice/document flow and review boundary.
8. [Aureus OS proof package](../../public-proof/aureus-os/README.md) - review operating model and action gates.
9. [Automation Lab](../services/automation-lab.md) - review automation capabilities and Sales Machine direction.
10. [Solution architecture](../system/solution-architecture.md) - review deeper architecture and decision boundaries.
11. [Source truth map](source-truth-map.md) - see which public claims are backed by Aureus Git source.
12. [Public boundary](public-boundary.md) - understand what stays private and why.

## Proof Types Shown Here

| Proof type | Public artifact |
| --- | --- |
| **Architecture proof** | diagrams, workflow maps, layer descriptions |
| **Process proof** | intake, review, approval, handoff patterns |
| **Safety proof** | public/private boundary, unsupported-claims discipline |
| **Automation proof** | n8n workflow governance and Sales Machine direction |
| **Financial workflow proof** | FinEcon, invoice/document review, POHODA/UBL boundary |
| **Operating-system proof** | Aureus OS scope, review, validation, action gate, evidence, and handoff |
| **Source-truth proof** | public claim register mapped to private Aureus Git artifact families |
| **Delivery proof** | GitHub/Codex, validation, evidence, handoff notes |

## What This Repository Does Not Claim

This profile does not claim official Azure certification, enterprise compliance certification, guaranteed ROI, paying customer results, production client outcomes, accounting correctness, tax/legal advice, trading performance, or public exposure of private systems.

Those claims require separate evidence and should not be implied from a public-safe architecture profile.

## One-Line External Summary

**Aureus Automation Lab builds controlled AI workflow systems for automation, finance intelligence, and internal execution with review gates, validation, evidence, and public/private safety boundaries.**
