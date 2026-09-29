"""Guard: the numeric-reproducibility template exists, covers the hazards, and is
loaded by the conditional Phase 11.5.
"""
from pathlib import Path

ROOT = (
    Path(__file__).resolve().parents[3]
    / "plugins/mad-scientist-skills/skills/optimization-audit"
)
TEMPLATE = ROOT / "templates/numeric-reproducibility.md"
SKILL = ROOT / "SKILL.md"

REQUIRED = ["reduction-order", "FMA", "BLAS", "version-fence", "redefine", "conditioning"]


def test_template_exists_and_covers_hazards():
    t = TEMPLATE.read_text(encoding="utf-8").lower()
    missing = [k for k in REQUIRED if k.lower() not in t]
    assert not missing, f"numeric-reproducibility.md missing: {missing}"


def test_phase_11_5_loads_the_template():
    s = SKILL.read_text(encoding="utf-8")
    body = s.split("### Phase 11.5:", 1)[1].split("###", 1)[0]
    assert "templates/numeric-reproducibility.md" in body
