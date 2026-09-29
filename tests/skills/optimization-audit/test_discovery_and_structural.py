"""Guard: Phase 1 has consumer-enumeration/blast-radius (P8); Phase 2 has the D2
same-transform-same-source structural check.
"""
import re
from pathlib import Path

SKILL = (
    Path(__file__).resolve().parents[3]
    / "plugins/mad-scientist-skills/skills/optimization-audit/SKILL.md"
).read_text(encoding="utf-8")


def test_phase_1_has_consumer_enumeration():
    p1 = SKILL.split("### Phase 1: Discovery", 1)[1].split("### Phase 2", 1)[0]
    assert "consumer" in p1.lower() and "blast radius" in p1.lower()


def test_phase_2_has_d2_structural_check():
    p2 = SKILL.split("### Phase 2:", 1)[1].split("### Phase 3", 1)[0]
    assert re.search(r"\bD2\b", p2), "D2 cue missing from Phase 2"
    assert "same transform" in p2.lower() and "same source" in p2.lower()
