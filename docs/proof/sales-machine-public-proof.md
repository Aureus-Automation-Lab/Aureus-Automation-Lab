# Sales Machine Public Proof

This page explains the public-safe direction of Aureus Sales Machine.

It does not expose private workflow exports, credentials, endpoints, real leads, or private inbox data.

## What Problem It Solves

Companies lose revenue when leads and follow-ups are handled manually.

Common issues:

- leads are not qualified consistently,
- follow-ups are forgotten,
- replies are not classified,
- sales activity is not visible,
- nobody knows what happened yesterday,
- AI outreach can become risky if it sends without review.

## Safe Workflow Direction

```text
lead source
-> lead discovery / import
-> qualification
-> outreach draft
-> manual approval
-> follow-up draft
-> reply classification
-> booking draft
-> daily report
-> audit log
```

## Key Safety Boundary

```text
No blind auto-send.
No uncontrolled outreach.
No sensitive external action without review.
```

## What AI May Do

| AI role | Allowed |
| --- | --- |
| qualify lead | yes, with scoring and review |
| draft outreach | yes, as a draft |
| draft follow-up | yes, as a draft |
| classify reply | yes, with uncertainty handling |
| create booking response | yes, as a draft |
| send email automatically | no, unless explicitly approved by the owner in a separate controlled system |

## Public Proof Value

This demonstrates that Aureus understands sales automation as a controlled workflow, not as a spam machine.

## What Stays Private

Real lead lists, inbox data, Gmail draft IDs, workflow IDs, credentials, private prompts, webhook URLs, and private logs stay private.
