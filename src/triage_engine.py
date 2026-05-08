from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from confirmation_queue import build_confirmation_item
from reply_draft import build_reply_draft


def load_json(path: str | Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _number(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "y", "on"}
    return bool(value)


def score_ticket(ticket: dict[str, Any], rules: dict[str, Any]) -> int:
    weights = rules.get("score_weights") or {}
    urgency = _number(ticket.get("urgency"))
    impact = _number(ticket.get("impact"))
    return urgency * _number(weights.get("urgency"), 1) + impact * _number(weights.get("impact"), 1)


def classify_ticket(ticket: dict[str, Any], rules: dict[str, Any]) -> dict[str, Any]:
    score = score_ticket(ticket, rules)
    blocked = _bool(ticket.get("blocked"))
    requires_reply = _bool(ticket.get("requires_reply"))
    requires_external_update = _bool(ticket.get("requires_external_update"))

    if blocked:
        return {
            "category": "blocked",
            "severity": "blocked",
            "score": score,
            "reason": str(ticket.get("blocker_reason") or "Blocked until a reviewer confirms the missing information."),
            "recommended_action": "confirm_blocker_before_update",
            "reply_draft_candidate": requires_reply,
            "requires_external_update": requires_external_update,
        }

    if score >= _number(rules.get("urgent_threshold"), 16):
        return {
            "category": "urgent",
            "severity": "high",
            "score": score,
            "reason": f"score={score} meets urgent threshold",
            "recommended_action": "review_and_prepare_ticket_update",
            "reply_draft_candidate": requires_reply,
            "requires_external_update": requires_external_update,
        }

    if requires_reply:
        return {
            "category": "needs_reply",
            "severity": "medium",
            "score": score,
            "reason": "reply requested; draft only",
            "recommended_action": "review_draft_before_reply",
            "reply_draft_candidate": True,
            "requires_external_update": requires_external_update,
        }

    if score >= _number(rules.get("backlog_threshold"), 7):
        return {
            "category": "backlog",
            "severity": "low",
            "score": score,
            "reason": f"score={score} is useful but not urgent",
            "recommended_action": "add_to_backlog_after_review",
            "reply_draft_candidate": False,
            "requires_external_update": requires_external_update,
        }

    return {
        "category": "no_action",
        "severity": "none",
        "score": score,
        "reason": "low score and no reply requested",
        "recommended_action": "no_external_update",
        "reply_draft_candidate": False,
        "requires_external_update": False,
    }


def build_report(tickets: list[dict[str, Any]], rules: dict[str, Any]) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    queue: list[dict[str, Any]] = []
    drafts: list[dict[str, Any]] = []

    for ticket in tickets:
        classification = classify_ticket(ticket, rules)
        row = {
            "ticket": {
                "id": ticket.get("id"),
                "source": ticket.get("source"),
                "title": ticket.get("title"),
                "received_at": ticket.get("received_at"),
            },
            "classification": classification,
        }
        rows.append(row)

        if classification.get("requires_external_update") or classification["category"] in {"urgent", "blocked"}:
            queue.append(build_confirmation_item(ticket, classification))
        if classification.get("reply_draft_candidate"):
            drafts.append({
                "ticket_id": ticket.get("id"),
                "draft": build_reply_draft(ticket, classification),
            })

    counts: dict[str, int] = {}
    for row in rows:
        cat = row["classification"]["category"]
        counts[cat] = counts.get(cat, 0) + 1

    return {
        "summary": {
            "tickets_scanned": len(tickets),
            "counts": counts,
            "confirmation_queue_count": len(queue),
            "reply_draft_count": len(drafts),
            "safety": rules.get("safety", "sample-first / no-comment / no-label-change"),
        },
        "items": rows,
        "confirmation_queue": queue,
        "reply_drafts": drafts,
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Support Ticket Triage Proof Report",
        "",
        f"- scanned: `{report['summary']['tickets_scanned']}`",
        f"- safety: `{report['summary']['safety']}`",
        f"- confirmation queue: `{report['summary']['confirmation_queue_count']}`",
        f"- reply drafts: `{report['summary']['reply_draft_count']}`",
        "",
        "## Reviewer Highlights",
        "",
        "- Tickets are grouped before any external update.",
        "- Reply suggestions are draft-only and not send-ready.",
        "- Action-worthy items are represented as confirmation queue entries.",
        "- The report is generated from synthetic fixtures, not a live support system.",
        "",
        "## Items",
        "",
    ]
    for row in report["items"]:
        ticket = row["ticket"]
        cls = row["classification"]
        lines.extend([
            f"### {ticket.get('title')}",
            f"- source: `{ticket.get('source')}`",
            f"- category: `{cls.get('category')}` / severity: `{cls.get('severity')}` / score: `{cls.get('score')}`",
            f"- reason: {cls.get('reason')}",
            f"- recommended_action: `{cls.get('recommended_action')}`",
            "",
        ])

    lines.extend(["## Confirmation Queue", ""])
    for item in report["confirmation_queue"]:
        lines.append(f"- `{item['id']}` {item['title']} -> `{item['recommended_action']}`")
    if not report["confirmation_queue"]:
        lines.append("- none")

    lines.extend(["", "## Reply Drafts", ""])
    for draft in report["reply_drafts"]:
        lines.extend([
            f"### ticket `{draft['ticket_id']}`",
            f"- draft_only: `{draft['draft']['draft_only']}`",
            f"- title: {draft['draft']['title']}",
            "",
            draft["draft"]["body"],
            "",
        ])
    if not report["reply_drafts"]:
        lines.append("- none")

    return "\n".join(lines).rstrip() + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Sample-first support ticket triage proof")
    parser.add_argument("--tickets", required=True)
    parser.add_argument("--rules", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--json-out", required=True)
    args = parser.parse_args(argv)

    report = build_report(load_json(args.tickets), load_json(args.rules))
    out = Path(args.out)
    json_out = Path(args.json_out)
    out.parent.mkdir(parents=True, exist_ok=True)
    json_out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render_markdown(report), encoding="utf-8", newline="\n")
    json_out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"wrote {out}")
    print(f"wrote {json_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
