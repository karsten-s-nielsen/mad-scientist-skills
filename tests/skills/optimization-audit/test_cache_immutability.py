"""Guard: the caching template covers immutability + identity-keyed-cache staleness
(P6), and Phase 6 references it.
"""
from pathlib import Path

ROOT = (
    Path(__file__).resolve().parents[3]
    / "plugins/mad-scientist-skills/skills/optimization-audit"
)
CACHE = ROOT / "templates/caching-strategies.md"
SKILL = ROOT / "SKILL.md"


def test_cache_template_covers_immutability_and_identity_key():
    t = CACHE.read_text(encoding="utf-8").lower()
    assert "immutable" in t or "defensive" in t or "read-only" in t, "P6 immutability missing"
    assert "identity" in t, "identity-keyed-cache staleness missing"


def test_phase_6_references_cache_immutability():
    s = SKILL.read_text(encoding="utf-8")
    p6 = s.split("### Phase 6:", 1)[1].split("### Phase 7", 1)[0]
    assert (
        "immutab" in p6.lower() or "read-only" in p6.lower() or "defensive" in p6.lower()
    ), "Phase 6 must reference cache immutability"
