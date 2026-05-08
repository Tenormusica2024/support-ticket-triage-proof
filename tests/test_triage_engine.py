from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from confirmation_queue import stable_queue_id
from triage_engine import build_report, classify_ticket, load_json


def sample_rules():
    return load_json(ROOT / "samples" / "triage_rules.json")


def test_urgent_external_update_goes_to_confirmation_queue():
    tickets = load_json(ROOT / "samples" / "tickets.json")
    report = build_report(tickets, sample_rules())

    urgent = [row for row in report["items"] if row["classification"]["category"] == "urgent"]
    queue_titles = {item["title"] for item in report["confirmation_queue"]}

    assert urgent
    assert "Cannot access monthly report" in queue_titles


def test_reply_drafts_are_draft_only():
    tickets = load_json(ROOT / "samples" / "tickets.json")
    report = build_report(tickets, sample_rules())

    assert report["reply_drafts"]
    assert all(draft["draft"]["draft_only"] is True for draft in report["reply_drafts"])
    assert all(draft["draft"]["send_ready"] is False for draft in report["reply_drafts"])


def test_blocked_item_is_not_classified_as_urgent_even_with_high_score():
    ticket = {
        "id": "ticket-x",
        "source": "support_portal",
        "title": "High impact but blocked",
        "urgency": 5,
        "impact": 5,
        "requires_reply": True,
        "requires_external_update": True,
        "blocked": True,
        "blocker_reason": "Approval missing.",
    }

    classification = classify_ticket(ticket, sample_rules())

    assert classification["category"] == "blocked"
    assert classification["recommended_action"] == "confirm_blocker_before_update"


def test_string_boolean_fields_are_not_treated_as_truthy_by_default():
    ticket = {
        "id": "ticket-y",
        "source": "support_portal",
        "title": "String booleans",
        "urgency": 1,
        "impact": 1,
        "requires_reply": "false",
        "requires_external_update": "false",
        "blocked": "false",
    }

    classification = classify_ticket(ticket, sample_rules())

    assert classification["category"] == "no_action"
    assert classification["reply_draft_candidate"] is False
    assert classification["requires_external_update"] is False


def test_confirmation_queue_id_is_stable():
    first = stable_queue_id("support_portal", "ticket-001", "Cannot access monthly report")
    second = stable_queue_id("support_portal", "ticket-001", "Cannot access monthly report")

    assert first == second
    assert len(first) == 12
