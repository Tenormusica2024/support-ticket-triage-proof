# Public Export Checklist

Use this checklist before publishing or reusing this proof.

## Required checks

- The demo runs with only `samples/tickets.json` and `samples/triage_rules.json`.
- No real ticket, customer, email, CRM, or support log data is included.
- No private issue or support-ticket content is included.
- No private knowledge-base output is included.
- No token, credential, or local absolute path is required.
- Default behavior is no-comment / no-label-change / no-send / no-execute.
- Action-worthy items go to a confirmation queue instead of being executed.
- Category decisions are explainable from sample inputs.

## Pre-export commands

```powershell
python -m pytest tests -q
python -X utf8 run_demo.py
python scripts/check_public_boundary.py
```

## Public repository description draft

```text
Sample-first AI secretary proof for support ticket triage, draft-only replies, and human confirmation queues.
```
