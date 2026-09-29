"""Guard: Phase 12 owns equivalence posture and loads the equivalence template,
which covers the oracle discipline.
"""
from pathlib import Path

ROOT = (
    Path(__file__).resolve().parents[3]
    / "plugins/mad-scientist-skills/skills/optimization-audit"
)
SKILL = ROOT / "SKILL.md"
TEMPLATE = ROOT / "templates/equivalence-verification.md"


def test_phase_12_renamed():
    s = SKILL.read_text(encoding="utf-8")
    assert "Profiling, Benchmarking & Equivalence Posture" in s


def test_equivalence_template_exists_and_covers_oracle_discipline():
    t = TEMPLATE.read_text(encoding="utf-8").lower()
    for k in ["oracle", "production scale", "mutation", "probe", "bitwise"]:
        assert k in t, f"equivalence-verification.md missing: {k}"


def test_phase_12_loads_equivalence_template():
    s = SKILL.read_text(encoding="utf-8")
    p12 = s.split("Profiling, Benchmarking & Equivalence Posture", 1)[1]
    assert "templates/equivalence-verification.md" in p12
