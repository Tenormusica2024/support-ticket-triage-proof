from __future__ import annotations

from dataclasses import dataclass
from typing import Any
import hashlib


@dataclass(frozen=True)
class QueueItem:
    id: str
    source: str
    title: str
    reason: str
    recommended_action: str
    ticket_id: str | None = None


def stable_queue_id(source: str, ticket_id: str | None, title: str) -> str:
    raw = f"{source}|{ticket_id or ''}|{title}".lower().encode("utf-8")
    return hashlib.sha1(raw).hexdigest()[:12]


def build_confirmation_item(ticket: dict[str, Any], classification: dict[str, Any]) -> dict[str, Any]:
    title = str(ticket.get("title") or "Untitled ticket")
    ticket_id = str(ticket.get("id") or "") or None
    source = str(ticket.get("source") or "sample-ticket")
    reason = str(classification.get("reason") or "Needs human confirmation")
    action = str(classification.get("recommended_action") or "review")
    created_at = str(ticket.get("received_at") or "sample-fixture")
    item = QueueItem(
        id=stable_queue_id(source, ticket_id, title),
        source=source,
        title=title,
        reason=reason,
        recommended_action=action,
        ticket_id=ticket_id,
    )
    return {
        "id": item.id,
        "source": item.source,
        "ticket_id": item.ticket_id,
        "title": item.title,
        "reason": item.reason,
        "recommended_action": item.recommended_action,
        "created_at": created_at,
    }
