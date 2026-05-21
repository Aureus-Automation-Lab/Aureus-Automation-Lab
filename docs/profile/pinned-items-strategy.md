# GitHub Pinned Items Strategy

GitHub profile pins should show the clearest public-safe proof of Aureus.

Do not use pins as a dumping ground for old experiments. Use them as a small public showroom.

## Recommended Pins

| Priority | Pin | Format | Purpose |
| --- | --- | --- | --- |
| 1 | `robert-kolesar/robert-kolesar` | profile repo | main public front door |
| 2 | Sales Machine public workflow map | gist or repo based on `public-proof/sales-machine` | shows safe sales automation with human approval |
| 3 | FinEcon invoice review flow | gist or repo based on `public-proof/finecon` | shows finance/document workflow boundaries |
| 4 | Aureus OS public operating model | gist or repo based on `public-proof/aureus-os` | shows the operating model behind AI-assisted delivery |
| 5 | Public-safe web/product demo | repo, when ready | shows visual and product execution |
| 6 | Small utility/template repo | repo, when polished | shows technical hygiene without private context |

## Profile Repo Naming Rule

GitHub profile README rendering depends on the repository name matching the current username.

- If the GitHub username has not changed yet, the profile repository must keep matching the current username.
- If the GitHub username changes to `robert-kolesar`, the profile repository must be renamed to `robert-kolesar/robert-kolesar`.

## Public-Proof Source Packages

The three proof packages under [public-proof](../../public-proof/README.md) should be treated as the source material for future pinned artifacts:

- [Sales Machine](../../public-proof/sales-machine/README.md),
- [FinEcon](../../public-proof/finecon/README.md),
- [Aureus OS](../../public-proof/aureus-os/README.md).

Convert them into pinned gists or public mini-repos only after this profile repo is public, reviewed, and confirmed safe from a signed-out browser.

## Pin Rules

Only pin artifacts that are:

- public-safe,
- polished,
- understandable in under one minute,
- supported by a clear README,
- free of private context,
- free of credentials, endpoints, logs, and raw workflow exports,
- honest about what is proven and what is only a direction.

## Do Not Pin

Do not pin:

- random experiments,
- private-context repos,
- raw workflow exports,
- unfinished demos,
- repos with broken or unclear README files,
- anything with credentials, endpoints, private logs, client-like data, or unsupported claims.

## Recommended Public Story

The pinned section should tell this story:

```text
who we are
-> how we handle sales workflows
-> how we handle finance/document workflows
-> how Aureus OS controls AI-assisted work
-> what we can build visually/product-wise
-> small proof of implementation hygiene
```

## Relationship To Existing Pin Guides

This is the short executive strategy. For fuller detail, use the [profile pins guide](pins-guide.md) and [public pin candidates](public-pin-candidates.md).
