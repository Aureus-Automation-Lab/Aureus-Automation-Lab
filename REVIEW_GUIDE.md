# Review Guide

![Aureus reviewer path map](assets/review-path-map.svg)

| Page signal | What to do first |
| --- | --- |
| 60-second scan | README, At A Glance, Architecture Cards, Public Boundary |
| Technical scan | Solution Architecture, Case Studies, Capabilities |
| Client scan | One-Pager, Build Menu, Collaboration, public pages |

## 60-Second Review

If you only have 60 seconds:

1. Read the hero and At A Glance in [README.md](README.md).
2. Check `What I Have Built` to understand the created systems and public-safe proof.
3. Check the Public Architecture Snapshot.
4. Review [Capabilities](CAPABILITIES.md) for role fit and system range.
5. Open [Case Studies](CASE_STUDIES.md) for public-safe examples.
6. Check [Public Boundary](PUBLIC_BOUNDARY.md) before asking for private material.

## What To Remember

| Signal | Meaning |
| --- | --- |
| Aureus Automation Lab | Robert is building an AI-native automation/product systems lab, not a generic freelancer page |
| Aureus AOP | The core idea is an operating platform around GitHub/Codex, n8n, validation, evidence, and handoff |
| n8n governance | Workflow automation is treated as source, review, approval, and evidence |
| Supervisor capability | AI review is framed as demonstrated integration capability, not official certification |
| Public-safe proof | The profile shows architecture and review discipline without leaking private systems |

## Reviewer Journey

```mermaid
flowchart TD
    A[README] --> B{Reviewer type}
    B --> C[Recruiter]
    B --> D[CTO / technical reviewer]
    B --> E[Client / partner]
    B --> F[Investor / founder reviewer]
    C --> G[Capabilities + Review Guide]
    D --> H[Solution Architecture + Case Studies]
    E --> I[One-Pager + Build Menu]
    F --> J[AOP story + public links]
```

## For Recruiters

Adjacent role signals include AI automation architecture, AI product engineering, workflow automation, internal tools, product operations, solutions engineering, and agentic workflow design.

Start with [README.md](README.md), then review [SOLUTION_ARCHITECTURE.md](SOLUTION_ARCHITECTURE.md) and [CASE_STUDIES.md](CASE_STUDIES.md). Many real automation repositories and workflow exports stay private because they can contain business logic, credentials, customer-like data, endpoints, and production context.

## For Technical Reviewers

Look for solution architecture thinking rather than only source volume:

- business process first,
- validation-first delivery,
- workflow and data boundaries,
- human review states,
- public-safe case study directions,
- evidence, QA, and handoff discipline.

The useful signal is whether the system shape is controlled, reviewable, and maintainable.

## For Clients / Partners

The best starting point is the business process: what happens today, what breaks, which tools are involved, what needs review, and what the first useful version should prove.

The collaboration model is designed around first useful scope, safety boundary, validation path, review/handoff, and practical next iteration.

## Suggested Review Path

1. [README.md](README.md)
2. [SOLUTION_ARCHITECTURE.md](SOLUTION_ARCHITECTURE.md)
3. [CASE_STUDIES.md](CASE_STUDIES.md)
4. [CAPABILITIES.md](CAPABILITIES.md)
5. [COLLABORATION.md](COLLABORATION.md)
6. [BUILD_MENU.md](BUILD_MENU.md)
7. [PUBLIC_BOUNDARY.md](PUBLIC_BOUNDARY.md)

## Reviewer Score Signals

| Signal | Where to look |
| --- | --- |
| Role clarity | [README.md](README.md) |
| Architecture thinking | [SOLUTION_ARCHITECTURE.md](SOLUTION_ARCHITECTURE.md) |
| Public-safe examples | [CASE_STUDIES.md](CASE_STUDIES.md) |
| Capability range | [CAPABILITIES.md](CAPABILITIES.md) |
| Collaboration style | [COLLABORATION.md](COLLABORATION.md) |
| Privacy discipline | [PUBLIC_BOUNDARY.md](PUBLIC_BOUNDARY.md) |
| Public launch readiness | [PUBLIC_LAUNCH_READINESS.md](PUBLIC_LAUNCH_READINESS.md) |

## What This Profile Is Not

It is not a source-code dump, raw workflow export, customer proof page, production system audit, or claim of private deployment results. It is a public-safe technical profile designed to show architecture thinking, workflow capability, and delivery discipline.
