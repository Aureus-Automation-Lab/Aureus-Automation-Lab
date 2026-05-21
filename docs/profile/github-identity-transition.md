# GitHub Identity Transition

This guide records the final public-profile naming rule for Aureus Automation Lab.

It does not change repository visibility. The repository must remain private until the final owner review passes.

## Detected State

| Field | Current value |
| --- | --- |
| Current GitHub username | `Aureus-Automation-Lab` |
| Current repository path | `Aureus-Automation-Lab/Aureus-Automation-Lab` |
| Required profile repository path | `Aureus-Automation-Lab/Aureus-Automation-Lab` |
| Display name target | `Róbert Kolesár` |
| Founder identity inside profile | `Róbert Kolesár / robertkolesar` |
| Public role line | Founder of Aureus Automation Lab · AI Systems Architect · Builder of controlled AI operating systems for business execution |
| Public brand | Aureus Automation Lab |

This is the brand/account profile. Róbert Kolesár is the founder identity presented inside the profile.

## Why This Matters

GitHub profile README appears only when all of these are true:

- the repository owner is the GitHub account,
- the repository name exactly matches the current GitHub username,
- the repository is public,
- `README.md` exists in the repository root,
- `README.md` has content.

Because the current username is `Aureus-Automation-Lab`, the profile repository must be:

```text
Aureus-Automation-Lab/Aureus-Automation-Lab
```

That naming gate is now satisfied.

## If The Account Username Changes Later

If the GitHub username is later changed to `robertkolesar`, then the profile repository must be renamed to:

```text
robertkolesar/robertkolesar
```

Do not switch the repository to public unless the repository name matches the current GitHub username.

## Public Switch Steps

1. Confirm the repository name equals the current GitHub username.
2. Confirm the display name is `Róbert Kolesár`.
3. Confirm the About description is public-safe.
4. Run the public audit:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\public_profile_audit.ps1
```

5. Switch the repository to public only after the audit passes and the owner approves.
6. Open the profile in a signed-out or incognito browser.
7. Confirm the README appears on the GitHub profile page.
8. Confirm images render and all public-proof links open.

## Incognito Test

Open:

```text
https://github.com/Aureus-Automation-Lab
```

Confirm:

- the README appears on the profile,
- the first screen says Aureus Automation Lab,
- the founder line says `Róbert Kolesár / robertkolesar`,
- the public-proof showroom opens,
- no private implementation or unsupported claim appears.
