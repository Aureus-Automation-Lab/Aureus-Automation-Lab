# GitHub Pinned Items Strategy

GitHub supports up to six pinned repositories or gists. Aureus should use only the number of independently useful artifacts that pass the public promotion gate.

## Target Story

```text
full-stack product proof
→ operating-system reference
→ finance workflow reference
→ risk-first infrastructure reference
→ optional reusable engineering artifact
```

## Recommended Order After Publication

| Priority | Candidate | Why it earns a pin |
| --- | --- | --- |
| 1 | `AureusAutomationLab/aureus-crm-operations` | Most accessible end-to-end business product proof: UI, API, data, roles, workflow state, tests, and deployment boundary |
| 2 | `AureusAutomationLab/aureus-os-reference` | Explains the operating model, safe autonomy, action gates, validation, evidence, and handoff |
| 3 | `AureusAutomationLab/aureus-finecon-reference` | Shows domain workflow design with professional-review and live-integration boundaries |
| 4 | `AureusAutomationLab/aureus-trading-infrastructure-reference` | Shows risk, isolation, observability, CI, and paper-run controls without exposing strategy |
| 5 | Future maintained validator or template | Include only if it has real reuse value, documentation, CI, ownership, and versioning |

The profile README already acts as the front door. Once the standalone portfolio exists, a permanent pin for the profile repository is redundant. Until then, fewer or zero pins are more credible than placeholders.

## Acceptance Standard

- clear artifact class, maturity, limitation, and source boundary;
- independently understandable README and meaningful visual;
- reproducible green CI and required branch check;
- security, privacy, claim, and license decisions complete;
- no private dependency, raw private export, client-like data, or unsupported outcome claim;
- signed-out rendering and link verification captured;
- exact publication and pin approval recorded.

Do not create empty repositories merely to reserve pin positions. The candidate registry is [portfolio-manifest.json](../../public-proof/portfolio-manifest.json).
