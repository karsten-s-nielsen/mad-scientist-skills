"""Guard: the equivalence discipline is wired across peer skills — MBO points to
the equivalence template for an output snapshot; unbiased-review and final-review
verify a byte-identical/no-flip optimization claim at production scale.
"""
from pathlib import Path

SKILLS = Path(__file__).resolve().parents[3] / "plugins/mad-scientist-skills/skills"
MBO = SKILLS / "measure-before-optimize/SKILL.md"
UR = SKILLS / "unbiased-review/SKILL.md"
FR = SKILLS / "final-review/SKILL.md"


def test_mbo_points_to_equivalence():
    t = MBO.read_text(encoding="utf-8")
    assert "equivalence-verification.md" in t
    assert "output snapshot" in t.lower() or "output-snapshot" in t.lower()


def test_unbiased_review_has_parity_mirror():
    t = UR.read_text(encoding="utf-8").lower()
    assert "production scale" in t
    assert "byte-identical" in t or "no-flip" in t or "parity" in t


def test_final_review_has_parity_mirror():
    t = FR.read_text(encoding="utf-8").lower()
    assert "production scale" in t
    assert "byte-identical" in t or "no-flip" in t or "parity" in t
