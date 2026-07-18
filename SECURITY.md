# Security Policy

## Reporting A Vulnerability

Do not open a public issue for vulnerabilities, leaked credentials, private
data, or production access details.

Use the repository Security tab's private vulnerability reporting flow when it
is available. If that flow is unavailable, contact the repository owner
through an existing private contact route shown on the GitHub profile. Include
the affected path, impact, safe reproduction steps, and any known exposure
window without including secret values.

## Supported Surface

The current `main` branch is the only supported public profile state. Historical
branches and migration snapshots are retained for review and are not release
claims.

## Sensitive Material

Never commit API keys, tokens, cookies, `.env` files, browser profiles,
credential exports, runtime databases, private workflow payloads, customer
data, or raw webhook URLs. If sensitive material is exposed, rotate or revoke
it first and coordinate remediation privately.

Security reports are assessed case by case. This policy does not promise a
specific response or remediation time.
