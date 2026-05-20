# Profile Publication Guide

![Aureus profile completeness map](assets/completeness-check-map.svg)

This task does not change repository visibility automatically. GitHub profile README appears publicly only when the special profile repository `KimiAoki/KimiAoki` is public.

## Correct GitHub Target

GitHub profile READMEs are rendered from a repository whose name exactly matches the account login. For this account, the public profile target is:

| Item | Value |
| --- | --- |
| GitHub login | `KimiAoki` |
| Display identity | Robert Kolesár / KimiAoki |
| Profile repository | `KimiAoki/KimiAoki` |
| Branch to verify | `main` |

## Before Making The Profile Public

| Check | Required state |
| --- | --- |
| Identity | Robert Kolesár / KimiAoki is clear in the first screen |
| Positioning | Founder, Aureus Automation Lab; AI Product Systems Architect; Builder of Aureus AOP |
| Public boundary | Private systems, credentials, endpoints, POHODA internals, and private screenshots are not exposed |
| Visuals | README and key docs include public-safe SVG visuals |
| Claims | No fake customers, revenue, certifications, accounting correctness, trading performance, or production client results |
| Links | Public links and internal review links are intentional |
| Launch review | [PUBLIC_LAUNCH_READINESS.md](PUBLIC_LAUNCH_READINESS.md) is reviewed |

## Manual Steps To Make The Profile Repo Public

1. Open GitHub repository settings for `KimiAoki/KimiAoki`.
2. Go to the danger zone visibility section.
3. Change visibility from private to public only after [PUBLIC_LAUNCH_READINESS.md](PUBLIC_LAUNCH_READINESS.md) is complete.
4. Confirm the repository name remains exactly `KimiAoki/KimiAoki`.
5. Open the public GitHub profile in a signed-out or private browser session.

## Manual Steps To Pin Repos Or Gists

1. Open the GitHub profile page.
2. Use the profile customization / pinned repositories section.
3. Pin only public-safe, polished repos or gists.
4. Recommended order:

| Priority | Pin |
| --- | --- |
| 1 | `KimiAoki/KimiAoki` |
| 2 | Aureus AOP architecture gist/demo |
| 3 | Automation Audit process map gist/demo |
| 4 | Invoice / FineCon public-safe workflow gist/demo |
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
