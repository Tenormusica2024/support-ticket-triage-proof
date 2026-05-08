# Privacy Boundary

This proof slice is sample-first and public-safe by default.

## Safe to publish

- Synthetic support ticket fixtures under `samples/`
- Generic triage rules
- Deterministic classification logic
- Confirmation queue examples
- Draft-only reply examples generated from synthetic data
- Markdown/JSON reports generated from synthetic data

## Do not publish

- Real ticket text
- Real customer names or contact details
- Real ticket IDs, thread IDs, or support portal URLs
- Private support logs or CRM records
- API tokens, OAuth credentials, local scheduler state
- Local absolute paths that reveal private environment details
- Private knowledge-base outputs

## Default safety model

The default demo is:

- no external API
- no ticket update
- no comment post
- no label change
- no email or notification send
- no automatic execution

The assistant recommends a decision; a human approves any external action.
