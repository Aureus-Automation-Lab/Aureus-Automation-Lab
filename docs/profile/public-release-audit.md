# Public Release Audit

Use this checklist before making `KimiAoki/KimiAoki` public.

## Repository Visibility

The profile README appears publicly only when the repository name matches the GitHub username, the repository is public, there is a root `README.md`, and the README contains content.

## Content Checks

| Check | Required state |
| --- | --- |
| First screen | clear who Aureus is and what it does |
| Language | understandable to non-technical people |
| Offers | clear enough for a buyer |
| Proof | public-safe proof paths exist |
| Safety | no unsupported claims |
| Links | internal links work |
| Images | visuals load and are public-safe |
| Private data | none exposed |

## Safety Checks

The repository must not include secrets, API keys, credentials, webhook URLs, private endpoints, real invoices, real client data, private workflow exports, POHODA access details, production logs, raw financial records, or unsupported ROI/revenue/customer claims.

## External Viewer Test

Open the profile in an incognito browser after making it public.

Confirm:

1. README renders.
2. Images render.
3. Public pages open.
4. Internal docs open.
5. Visitor understands Aureus without private repos.
6. No private or unsupported claim appears.
7. The profile feels like a serious company front door.

## Local Audit Command

Before publishing, run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\public_profile_audit.ps1
```
