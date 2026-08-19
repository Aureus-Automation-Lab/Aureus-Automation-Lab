# Aureus Sales Machine Public Proof

This package shows a public-safe sales workflow direction.

It is designed for a business owner who wants better follow-up without letting AI send messages blindly.

## Problem statement

Sales work often breaks between lead capture and follow-up:

- leads arrive from different places,
- qualification depends on memory,
- follow-ups are late or forgotten,
- replies are not classified,
- activity is hard to review,
- AI can become risky if it sends without approval.

## Who it helps

This direction helps companies that receive inquiries, referrals, form submissions, or prospect lists and need a safer way to review, qualify, draft, follow up, and report.

## Workflow summary

```text
lead source
-> discovery / import
-> qualification
-> draft outreach
-> manual approval
-> follow-up draft
-> reply classification
-> booking draft
-> daily report
-> audit log
```

Open the [workflow map](workflow-map.md) for the full public-safe flow.

## What AI may do

AI may classify leads, score fit, draft outreach, draft follow-ups, classify replies, prepare a booking response draft, and summarize daily activity.

## What humans approve

Humans approve which leads to contact, final outbound messages, sensitive replies, booking language, escalation decisions, and any external send unless a separate approved system exists.

## What evidence is kept

A safe system can keep source of lead, qualification status, draft history, approval state, reply category, next action, daily summary, and audit note.

## What stays private

Real lead lists, message data, draft IDs, workflow IDs, credentials, endpoints, message prompts, and private logs stay private.

## Package files

- [Workflow map](workflow-map.md)
- [Safe state model](safe-state-model.md)
- [Buyer example](buyer-example.md)
