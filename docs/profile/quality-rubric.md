# Public GitHub Trust Standard

Use this gate before promoting the profile, an organization page, or a standalone proof repository to clients, partners, collaborators, or public reviewers.

## Review Gates

| Gate | Pass condition |
| --- | --- |
| First-screen clarity | A visitor sees the accountable person or company, the work category, and one useful next path without decoding internal terminology. |
| Identity separation | Founder and company surfaces have distinct roles, consistent names, and no competing account identities. |
| Business understanding | A non-technical reviewer can identify the buyer problem, artifact type, maturity, and next conversation quickly. |
| Technical review | Architecture, state boundaries, validation commands, security controls, and limitations are easy to find. |
| Public-safe proof | Every claim maps to a public artifact or an explicitly described private-source boundary. |
| Claim safety | No unsupported customer, revenue, certification, accounting, security, trading, ROI, or production claim appears. |
| Repository hygiene | The repository has a focused README, owned navigation, no stale launch instructions, no broken links, and no confusing duplicates. |
| CI and review | Proven validation is required on protected `main`, with independent review and no force-push shortcut. |
| Security | Least-privilege workflows, immutable Action references, dependency alerts, secret scanning, push protection, and a private disclosure path are active where supported. |
| External review | A signed-out visitor can render the profile, open every primary link, understand the maturity, and find no private dependency. |

## Required Public Proof Contract

- clear canonical name and repository class;
- explicit maturity and status;
- problem, user, scope, architecture, validation, limitations, and next review path;
- public-safe visual when it improves comprehension;
- reproducible CI and security/claim checks;
- contribution, support, conduct, security, ownership, and release boundaries;
- a deliberate license decision;
- signed-out verification evidence.

## Automatic No-Go

Do not promote or pin an artifact that contains secrets, private endpoints, raw private workflow exports, real client-like data, private screenshots, unsupported claims, broken rendering, unknown ownership, an empty placeholder repository, or a maturity label stronger than its evidence.

## Result

Record exactly one result per gate: `PASS`, `REPAIR_REQUIRED`, `APPROVAL_REQUIRED`, or `BLOCKED`. Numeric self-ratings are not accepted as readiness evidence.

The complete implementation contract is the [Public GitHub Portfolio Standard](../portfolio/github-portfolio-standard.md).
