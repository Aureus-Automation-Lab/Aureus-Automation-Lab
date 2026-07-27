# Contributing to Aureus Automation Lab

Thanks for helping improve this public portfolio and reference repository. The goal is clear, useful, and safely shareable material about controlled AI automation.

## Before you start

1. Read the [public-safe architecture overview](docs/PUBLIC_SAFE_ARCHITECTURE_OVERVIEW.md) and the [public boundary](docs/portfolio/public-boundary.md).
2. Open an issue for a material change so the intent and scope can be reviewed early.
3. Work from a focused branch and keep each pull request limited to one coherent improvement.

## Public-safety rules

Only contribute material that is safe to publish. Do not add:

- customer, employee, or personal data;
- credentials, access details, tokens, configuration values, or internal URLs;
- raw private workflow exports, internal logs, or operating-environment details;
- unverified performance, revenue, compliance, or security claims.

Use fictional or synthetic examples whenever an example needs business data. If you are unsure whether material is public-safe, do not post it; request maintainer guidance with a minimal description.

## Pull request checklist

- Explain the user value and the evidence or source behind the change.
- Keep public claims precise and avoid implying results that are not demonstrated.
- Run the repository check:

  ```powershell
  python scripts/validate-public-portfolio.py
  ```

- Run `git diff --check` and confirm links and Markdown render clearly.
- Use the pull-request template and note any remaining limitation or reviewer decision.

## Review and merge

Maintainers review correctness, public-safety boundaries, wording, and maintainability. A pull request may be asked to narrow its scope, replace details with a synthetic example, or add clearer evidence before it can merge.
