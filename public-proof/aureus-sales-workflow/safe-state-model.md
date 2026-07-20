# Aureus Sales Workflow Safe State Model

This state model shows how lead handling can stay controlled.

## States

| State | Meaning |
| --- | --- |
| `discovered` | A lead exists in the system. |
| `needs_review` | The lead requires human review before next action. |
| `approved` | A human approved the lead for the next safe step. |
| `qualified` | The lead appears to fit the selected criteria. |
| `not_fit` | The lead does not fit the selected criteria. |
| `draft_created` | AI prepared a message draft. |
| `waiting_approval` | A draft exists but cannot be sent yet. |
| `replied_positive` | The reply appears interested or open to next steps. |
| `replied_negative` | The reply appears negative or not interested. |
| `meeting_draft_created` | AI prepared a meeting or next-step draft. |
| `do_not_contact` | The lead must not be contacted. |

## Automatic Transitions

AI or automation may suggest transitions such as:

- `discovered` -> `needs_review`,
- `approved` -> `qualified`,
- `qualified` -> `draft_created`,
- reply received -> `replied_positive` or `replied_negative`,
- `replied_positive` -> `meeting_draft_created`.

These are suggestions or internal state updates, not blind external sends.

## Human Approval Required

Human approval is required before:

- sending first outreach,
- sending a follow-up,
- sending a booking response,
- changing a lead from blocked/not-fit to active,
- contacting anyone marked `do_not_contact`,
- using sensitive or uncertain context.

## What Blocks Outreach

Outreach is blocked when:

- state is `needs_review`,
- state is `not_fit`,
- state is `waiting_approval`,
- state is `do_not_contact`,
- required context is missing,
- the source is not approved,
- the message was not reviewed.

## Why No Blind Send Exists

Sales automation can damage trust if it sends too early.

The safe model is:

```text
AI prepares.
Human approves.
System records.
```
