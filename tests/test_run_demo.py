from __future__ import annotations

from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def test_run_demo_generates_reports():
    result = subprocess.run([sys.executable, "-X", "utf8", "run_demo.py"], cwd=ROOT, text=True, capture_output=True)

    assert result.returncode == 0, result.stderr
    assert "safety: sample-first" in result.stdout
    assert (ROOT / "outputs" / "triage_report.md").exists()
    assert (ROOT / "outputs" / "triage_report.json").exists()
