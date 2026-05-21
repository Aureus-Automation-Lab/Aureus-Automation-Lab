# GitHub Identity Transition

This guide prepares the public GitHub identity transition for Róbert Kolesár and Aureus Automation Lab.

It does not change the GitHub username, repository name, repository visibility, or public profile automatically. Those are owner-controlled GitHub actions.

## Target Identity

| Field | Target |
| --- | --- |
| Display name | `Róbert Kolesár` |
| GitHub username | `robertkolesar` |
| Profile repository | `robertkolesar/robertkolesar` |
| Public brand | Aureus Automation Lab |
| Role line | Founder of Aureus Automation Lab · AI Systems Engineer · workflow automation architect |

## A. Before Username Change

1. Confirm the target username `robertkolesar` is available in GitHub account settings.
2. Confirm the local repository is clean.
3. Run the public audit:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\public_profile_audit.ps1
```

4. Review all identity references reported by the audit.
5. Do not make the repository public until the final owner review is complete.

## B. GitHub Account Update

In GitHub:

1. Open **Settings**.
2. Open **Account**.
3. Change the current GitHub username to `robertkolesar` if the username is available.
4. Open **Public profile**.
5. Set **Name** to `Róbert Kolesár`.

## C. Repository Rename

After the username change:

1. Open the profile repository settings.
2. Rename the profile repository to `robertkolesar`.
3. Confirm the final repository path is:

```text
robertkolesar/robertkolesar
```

## D. About Section

Recommended repository description:

```text
Public profile for Aureus Automation Lab — controlled AI workflow systems for sales, operations, finance, documents, reporting, and internal execution.
```

Recommended website:

```text
https://aureus.it.com/automationlab
```

Recommended topics:

- `aureus-automation-lab`
- `ai-automation`
- `workflow-automation`
- `n8n`
- `finecon`
- `aureus-os`
- `operations`
- `public-proof`

## E. Public Switch

1. Keep the repository private until the audit passes and the owner completes final review.
2. Switch the repository to public only after approval.
3. Open `https://github.com/robertkolesar` in an incognito or signed-out browser.
4. Confirm the README renders as the profile README.
5. Confirm images render.
6. Confirm public-proof links work.
7. Confirm no private implementation, unsupported claim, or old public identity appears.

## F. Pins

After the profile is public:

1. Pin the profile repository.
2. Later create and pin public-safe gists or mini-repos from:
   - `public-proof/sales-machine`
   - `public-proof/finecon`
   - `public-proof/aureus-os`

Do not pin raw workflow exports, private-context repositories, private screenshots, credentials, endpoints, logs, real invoices, real leads, or unsupported claims.

## Profile Repository Behavior

GitHub profile README appears only when the profile repository name matches the current GitHub username.

Therefore:

- if the username has not changed yet, the profile repository must keep matching the current username,
- if username becomes `robertkolesar`, the profile repository must be `robertkolesar/robertkolesar`.
