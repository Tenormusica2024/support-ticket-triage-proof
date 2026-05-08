# Support Ticket Triage Proof Report

- scanned: `5`
- safety: `sample-first / no-comment / no-label-change / confirmation-required`
- confirmation queue: `2`
- reply drafts: `3`

## Reviewer Highlights

- Tickets are grouped before any external update.
- Reply suggestions are draft-only and not send-ready.
- Action-worthy items are represented as confirmation queue entries.
- The report is generated from synthetic fixtures, not a live support system.

## Items

### Cannot access monthly report
- source: `support_portal`
- category: `urgent` / severity: `high` / score: `22`
- reason: score=22 meets urgent threshold
- recommended_action: `review_and_prepare_ticket_update`

### Question about invoice format
- source: `support_portal`
- category: `needs_reply` / severity: `medium` / score: `15`
- reason: reply requested; draft only
- recommended_action: `review_draft_before_reply`

### Feature request: export saved filters
- source: `feedback_form`
- category: `backlog` / severity: `low` / score: `11`
- reason: score=11 is useful but not urgent
- recommended_action: `add_to_backlog_after_review`

### Migration request waiting for approval
- source: `support_portal`
- category: `blocked` / severity: `blocked` / score: `23`
- reason: Owner approval and maintenance window are required.
- recommended_action: `confirm_blocker_before_update`

### Weekly usage summary available
- source: `notification`
- category: `no_action` / severity: `none` / score: `5`
- reason: low score and no reply requested
- recommended_action: `no_external_update`

## Confirmation Queue

- `3eb004cc2395` Cannot access monthly report -> `review_and_prepare_ticket_update`
- `cebb3bbb6331` Migration request waiting for approval -> `confirm_blocker_before_update`

## Reply Drafts

### ticket `ticket-001`
- draft_only: `True`
- title: Re: Cannot access monthly report

Thank you for the report. We have flagged this for human review because it may affect active work.

Before any ticket update is posted, a reviewer should confirm the affected account, impact, and next action.

### ticket `ticket-002`
- draft_only: `True`
- title: Re: Question about invoice format

Thank you for the question. We have prepared this as a draft response for review.

A reviewer should confirm the details before replying or updating the ticket.

### ticket `ticket-004`
- draft_only: `True`
- title: Re: Migration request waiting for approval

Thank you for the request. This is currently blocked because additional approval or missing information is required.

A reviewer should confirm the blocker before any external update is made.
