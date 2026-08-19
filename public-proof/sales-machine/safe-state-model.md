# Sales Machine Safe State Model

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

## Automatic transitions

AI or automation may suggest transitions such as:

- `discovered` -> `needs_review`,
- `approved` -> `qualified`,
- `qualified` -> `draft_created`,
- reply received -> `replied_positive` or `replied_negative`,
- `replied_positive` -> `meeting_draft_created`.

These are suggestions or internal state updates, not blind external sends.

## Human approval required

Human approval is required before sending first outreach, sending a follow-up, sending a booking response, changing a blocked lead to active, contacting anyone marked `do_not_contact`, or using sensitive or uncertain context.

## What blocks outreach

Outreach is blocked when state is `needs_review`, `not_fit`, `waiting_approval`, or `do_not_contact`, required context is missing, the source is not approved, or the message was not reviewed.

## Why no blind send exists

Sales automation can damage trust if it sends too early.

The safe model is:

```text
AI prepares.
Human approves.
System records.
```
