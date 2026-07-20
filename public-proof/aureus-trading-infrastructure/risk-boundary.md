# Trading Infrastructure Risk Boundary

## What The Architecture Is Designed To Control

| Risk | Control direction |
| --- | --- |
| Credential exposure | Only the isolated executor may hold exchange credentials; secrets remain outside Git |
| Unreviewed logic change | Risk-path files require manual review and are excluded from safe auto-merge |
| Server drift | Tracked source is Git-first and server changes are pull-only |
| Partial deployment | Smoke failure stops progress before a partial apply |
| Invisible runtime failure | Metrics, alerts, dashboards, and runbooks make operational state reviewable |
| Strategy ambiguity | Deterministic stages and explicit rails separate decision logic from execution |

## Evidence Boundary

The private repository supports the architecture claims above. Public proof intentionally excludes:

- strategy parameters and order logic,
- exchange keys and account information,
- hosts, endpoints, and operational credentials,
- private metrics, logs, and dashboards,
- live positions or orders,
- return, profitability, or risk-adjusted performance claims.

## Promotion Boundary

Moving from paper-run evidence toward live operation would require a separate, explicit decision with threat modeling, capital/risk limits, credential controls, rollback evidence, monitoring acceptance, and owner approval. The existence of architecture and CI does not grant that authority.
