# Profile Publication Guide

![Aureus profile completeness map](../../assets/completeness-check-map.svg)

This task does not change repository visibility automatically. GitHub profile README appears publicly only when the special profile repository matches the current GitHub username and is public.

For the identity change sequence, use [GitHub identity transition](github-identity-transition.md). For repository About settings, use [GitHub About settings](github-about-settings.md).

GitHub reference:

- [Managing your profile README](https://docs.github.com/en/account-and-profile/how-tos/profile-customization/managing-your-profile-readme)
- [Pinning items to your profile](https://docs.github.com/en/account-and-profile/how-tos/profile-customization/pinning-items-to-your-profile)

## Before Making The Profile Public

| Check | Required state |
| --- | --- |
| Identity | Róbert Kolesár / robertkolesar is clear in the first screen |
| Positioning | Founder, Aureus Automation Lab; AI Product Systems Architect; Builder of Aureus AOP |
| Public boundary | Private systems, credentials, endpoints, POHODA internals, and private screenshots are not exposed |
| Source truth | Public claims are connected to the [source truth map](../proof/source-truth-map.md) |
| Visuals | README and key docs include public-safe SVG visuals |
| Claims | No fake customers, revenue, certifications, accounting correctness, trading performance, or production client results |
| Links | Public links and internal review links are intentional |

## Manual Steps To Make The Profile Repo Public

1. Open GitHub repository settings for `robertkolesar/robertkolesar`.
2. Go to the danger zone visibility section.
3. Change visibility from private to public only after the checklist above is complete.
4. Confirm the repository name remains exactly `robertkolesar/robertkolesar`.
5. Open the public GitHub profile in a signed-out or private browser session.

Before switching visibility, run the local public release audit:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\public_profile_audit.ps1
```

## Manual Steps To Pin Repos Or Gists

1. Open the GitHub profile page.
2. Use the profile customization / pinned repositories section.
3. Pin only public-safe, polished repos or gists.
4. Recommended order:

| Priority | Pin |
| --- | --- |
| 1 | `robertkolesar/robertkolesar` |
| 2 | Aureus OS architecture gist/demo |
| 3 | Sales Machine public-safe workflow map gist/demo |
| 4 | Invoice / FinEcon public-safe workflow map gist/demo |
| 5 | Web Studio / Figma-to-code public-safe demo when visually ready |
| 6 | Template or health demo repo if polished |

## External Viewer Check

Open the profile as an external viewer and confirm:

- the README renders,
- images render,
- links work,
- public pages open,
- private repos are not required to understand the story,
- no private or unsupported claim appears.
