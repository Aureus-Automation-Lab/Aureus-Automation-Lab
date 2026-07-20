# Public Pin Candidates

| Priority | Candidate | Current state | Required next gate |
| --- | --- | --- | --- |
| 1 | `AureusAutomationLab/aureus-crm-operations` | Sanitized package in the profile repository | Extract lineage, choose license, add standalone CI/governance, review screenshots and claims, publish with approval |
| 2 | `AureusAutomationLab/aureus-os-reference` | Sanitized architecture package | Confirm public reference scope, remove private implementation dependencies, add standalone validation and limitations |
| 3 | `AureusAutomationLab/aureus-finecon-reference` | Sanitized workflow package | Preserve accountant, POHODA, real-document, and production boundaries; add standalone validation |
| 4 | `AureusAutomationLab/aureus-trading-infrastructure-reference` | Sanitized paper-run package | Exclude strategy, credentials, runtime data, and performance claims; add standalone validation |
| 5 | Reusable validator or maintained template | Not selected | Demonstrate real reuse, versioning, ownership, CI, and support before publication |

`Aureus Sales Workflow` remains an embedded scenario. It is not a separate top-level product or pin candidate unless future source and buyer evidence justify promotion through the naming and governance gate.

Creating repositories, changing visibility, publishing code or documentation, and pinning items are separate live GitHub mutations. Perform them only through the [approval packet](github-governance-approval-packet.md) with a signed-out verification receipt.

The machine-readable source for this list is [portfolio-manifest.json](../../public-proof/portfolio-manifest.json).
