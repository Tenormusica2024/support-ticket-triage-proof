from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from triage_engine import build_report, load_json, render_markdown  # noqa: E402


def main() -> int:
    tickets = ROOT / "samples" / "tickets.json"
    rules = ROOT / "samples" / "triage_rules.json"
    output_dir = ROOT / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    report = build_report(load_json(tickets), load_json(rules))
    report_md = output_dir / "triage_report.md"
    report_json = output_dir / "triage_report.json"

    report_md.write_text(render_markdown(report), encoding="utf-8", newline="\n")
    report_json.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")

    print(f"wrote {report_md.relative_to(ROOT)}")
    print(f"wrote {report_json.relative_to(ROOT)}")
    print("safety: sample-first / draft-only / no-ticket-update / confirmation-required")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
