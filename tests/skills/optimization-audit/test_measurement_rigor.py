"""Guard: Phase 12 carries the measurement-rigor cues (P9-P18, D4, D6) and the
algorithm-complexity template carries the P23/P24 guard-authoring guidance.
"""
from pathlib import Path

ROOT = (
    Path(__file__).resolve().parents[3]
    / "plugins/mad-scientist-skills/skills/optimization-audit"
)
ALG = ROOT / "templates/algorithm-complexity.md"


def test_phase_12_measurement_bullets_present():
    full = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    p12 = full.split("Profiling, Benchmarking & Equivalence Posture", 1)[1].split(
        "### Phase 13", 1
    )[0]
    for cue in [
        "fixed-cost",
        "count=0",
        "warm",
        "noise floor",
        "op-count",
        "shape inventory",
        "instrumentation",
        "known-broken shim",
    ]:
        assert cue.lower() in p12.lower(), f"missing measurement cue: {cue}"


def test_alg_template_has_guard_authoring_guidance():
    a = ALG.read_text(encoding="utf-8").lower()
    assert "threshold constant" in a and "size-ladder" in a
