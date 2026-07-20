# Founder, Organization, And Proof Publication Guide

![Aureus profile completeness map](../../assets/aureus-public-boundary.gif)

The current profile repository is public. Future work is a staged GitHub architecture rollout, not a visibility launch.

## Surface Roles

| Surface | Role | Publication rule |
| --- | --- | --- |
| Founder profile | Human identity, contribution story, role, selected work, company link | Keep concise and personal; username migration requires reference audit |
| Company organization profile | Company promise, portfolio map, evidence boundary, contact path | Publish from `AureusAutomationLab/.github` only after content and settings review |
| Public proof repository | Independently useful product proof or reference | Publish one at a time after lineage, license, CI, security, claim, and signed-out gates |
| Private source repository | Implementation, runtime, client work, and private evidence | Never expose merely to create portfolio volume |

## Staged Publication

1. merge governance into the existing public profile through independent review;
2. publish the local follow-up through a separate reviewed PR;
3. harden live branch, merge, feature, and security settings;
4. establish the organization profile;
5. extract and publish Aureus CRM Operations as the first standalone proof;
6. repeat the same gate for Aureus OS, FinEcon, and Trading references;
7. pin only passed artifacts;
8. decide founder username migration last.

## Public Proof Extraction Rule

A sanitized package is a candidate, not an automatic new repository. Before extraction, verify source lineage, remove private dependencies, choose a license intentionally, give the artifact its own README and CI, run claim/security checks, and prove it works without access to private GitHub.

## External Viewer Check

Open every changed public surface signed-out and confirm the accountable identity, artifact type, maturity, limitations, primary links, images, and validation path. Capture evidence; do not rely on an authenticated owner view.

Official references:

- [Managing a profile README](https://docs.github.com/en/account-and-profile/how-tos/profile-customization/managing-your-profile-readme)
- [Customizing an organization profile](https://docs.github.com/en/organizations/collaborating-with-groups-in-organizations/customizing-your-organizations-profile)
- [Pinning items to a profile](https://docs.github.com/en/account-and-profile/how-tos/profile-customization/pinning-items-to-your-profile)

The exact live stages and rollback paths are in the [approval packet](github-governance-approval-packet.md).
