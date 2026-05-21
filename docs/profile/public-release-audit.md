# Public Release Audit

Use this checklist before switching the profile repository from private to public.

## Hard Warning

Do not switch visibility to public until the repository name equals the current GitHub username.

Current detected username:

```text
Aureus-Automation-Lab
```

Current repository:

```text
Aureus-Automation-Lab/robertkolesar
```

Required profile repository:

```text
Aureus-Automation-Lab/Aureus-Automation-Lab
```

## Repository Visibility

The profile works publicly only when:

- the repository owner is the GitHub account,
- the repository name equals the current GitHub username,
- the repository is public,
- the root `README.md` exists,
- the root `README.md` has useful content.

## Identity And Naming Checks

Confirm:

- Current username is detected and documented.
- Repository name equals current username.
- GitHub display name is `Róbert Kolesár`.
- README presents `Róbert Kolesár / robertkolesar` as the founder identity.
- Repository About description is public-safe.
- Repository About description no longer says `Private draft profile`.
- Repository About topics are public-safe and aligned with Aureus.
- The manual sequence in [GitHub identity transition](github-identity-transition.md) has been reviewed.
- The final naming gate in [Final public switch checklist](final-public-switch-checklist.md) has been reviewed.
- The recommended settings in [GitHub About settings](github-about-settings.md) have been applied or consciously deferred.

## Final Content Checks

| Check | Required state |
| --- | --- |
| README first screen | clear who Aureus is and what it does |
| Non-technical clarity | a business reader understands the profile in 30 seconds |
| Offers | first project options are clear |
| Aureus pillars | Automation Lab, FinEcon, and Aureus OS are easy to understand |
| Public proof | proof paths are visible and public-safe |
| Public proof showroom | `public-proof/README.md` opens and all three proof packages open |
| Internal links | all linked local docs open |
| Images | README images load |
| Public pages | public websites open |
| Private context | private repos are not required to understand the story |

## Public-Proof Checks

Confirm:

- [Public proof showroom](../../public-proof/README.md) opens.
- [Sales Machine proof package](../../public-proof/sales-machine/README.md) opens.
- [FinEcon proof package](../../public-proof/finecon/README.md) opens.
- [Aureus OS proof package](../../public-proof/aureus-os/README.md) opens.
- No proof artifact includes private implementation, raw workflow exports, private endpoints, real invoices, real leads, private prompts, logs, or unsupported claims.

## Safety Checks

The public repo must not include:

- secrets,
- API keys,
- credentials,
- webhook URLs,
- private endpoints,
- raw n8n workflow exports,
- private workflow IDs,
- POHODA access details,
- real invoices,
- real leads,
- real inbox data,
- client-like data,
- production logs,
- private screenshots,
- private prompts,
- fake testimonials,
- unsupported customer, ROI, certification, accounting, tax, legal, trading, or enterprise-compliance claims.

## Identity Reference Checks

Confirm:

- no old nickname appears as current public identity,
- no old private-draft About wording remains in GitHub About,
- no public-facing page claims unsupported production results,
- no private implementation appears.

## External Viewer Test

After switching to public, open the profile in a signed-out or incognito browser.

Confirm:

1. README renders on the profile page.
2. Hero image loads.
3. Public proof links open.
4. Public websites open.
5. The visitor understands Aureus without access to private repos.
6. No private or unsupported claim appears.
7. The profile feels like a serious company/studio front door.

## Local Audit Command

Before publishing, run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\public_profile_audit.ps1
```

Then review the output manually before changing repository visibility.
