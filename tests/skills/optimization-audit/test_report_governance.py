"""Guard: Phase 13 report carries the optimization-vs-scope classification and the
regressions/trade-offs section; Important Rules carry P1/P19/P20; the shared
findings-table schema note is untouched.
"""
from pathlib import Path

SKILL = (
    Path(__file__).resolve().parents[3]
    / "plugins/mad-scientist-skills/skills/optimization-audit/SKILL.md"
).read_text(encoding="utf-8")


def test_report_has_optimization_vs_scope_section():
    assert "Optimization vs Scope-Decision Classification" in SKILL


def test_report_has_regressions_tradeoffs_section():
    assert "Regressions / trade-offs accepted" in SKILL


def test_important_rules_have_governance_rules():
    rules = SKILL.split("## Important rules", 1)[1]
    assert "output-preserving" in rules.lower(), "P1 rule missing"
    assert "correctness fix" in rules.lower(), "P19 rule missing"
    assert "as-built" in rules.lower() or "approved plan" in rules.lower(), "P20 rule missing"


def test_shared_findings_schema_note_present():
    assert "base columns" in SKILL.lower(), "shared findings-table schema note must remain"
