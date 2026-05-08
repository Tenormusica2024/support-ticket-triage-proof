from __future__ import annotations

from typing import Any


def build_reply_draft(ticket: dict[str, Any], classification: dict[str, Any]) -> dict[str, Any]:
    """Build a deterministic draft-only reply. This never sends a message."""
    title = str(ticket.get("title") or "")
    category = classification.get("category")

    if category == "urgent":
        body = (
            "Thank you for the report. We have flagged this for human review because it may affect active work.\n\n"
            "Before any ticket update is posted, a reviewer should confirm the affected account, impact, and next action."
        )
    elif category == "blocked":
        body = (
            "Thank you for the request. This is currently blocked because additional approval or missing information is required.\n\n"
            "A reviewer should confirm the blocker before any external update is made."
        )
    else:
        body = (
            "Thank you for the question. We have prepared this as a draft response for review.\n\n"
            "A reviewer should confirm the details before replying or updating the ticket."
        )

    return {
        "draft_only": True,
        "send_ready": False,
        "title": f"Re: {title}" if title and not title.lower().startswith("re:") else title,
        "body": body,
        "safety_note": "This is a draft-only suggestion. Review before any external update.",
    }
