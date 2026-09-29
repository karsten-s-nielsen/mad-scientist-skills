"""Guard: Phase 11.5 (conditional numeric phase) is declared consistently.

Locates each section by content/heading, never by line number, so it survives
line drift (the ADR-003 migration shifted anchors, and this feature shifts them
more).
"""
from pathlib import Path

SKILL = (
    Path(__file__).resolve().parents[3]
    / "plugins/mad-scientist-skills/skills/optimization-audit/SKILL.md"
)


def _text():
    return SKILL.read_text(encoding="utf-8")


def test_phase_11_5_in_phase_order_line():
    t = _text()
    line = next(l for l in t.splitlines() if l.startswith("**Phase order:**"))
    assert "11.5" in line, "phase-order line must include 11.5"


def test_phase_11_5_in_conditional_skip_list():
    t = _text()
    line = next(l for l in t.splitlines() if "Skip conditional phases" in l)
    assert "11.5" in line, "conditional-skip list must include 11.5"


def test_phase_11_5_in_important_rules_conditional_rule():
    t = _text()
    line = next(
        l for l in t.splitlines() if l.strip().startswith("- **Conditional phases.**")
    )
    assert "11.5" in line, "Important-Rules conditional-phases rule must name 11.5"


def test_phase_11_5_in_coverage_matrix():
    t = _text()
    matrix = t.split("### Phase Coverage Matrix", 1)[1]
    assert "11.5" in matrix, "Phase Coverage Matrix must have an 11.5 row"


def test_phase_count_prose_not_a_bare_14():
    t = _text()
    assert "run all 14 phases" not in t, "count prose must be reworded for 0.5 + 11.5"


def test_phase_11_5_section_exists_and_conditional():
    t = _text()
    assert "### Phase 11.5:" in t, "Phase 11.5 section heading must exist"
    head = t.split("### Phase 11.5:", 1)[1].split("###", 1)[0]
    assert "CONDITIONAL" in head, "Phase 11.5 must be marked CONDITIONAL"
