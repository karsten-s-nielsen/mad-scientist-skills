"""Guard: the detection catalog (D1, D3-D6) is present in SKILL.md, and the D3
grep extracted from its table cell discriminates waste from legitimate code.

D2 is a Phase 2 structural check (not a grep) — asserted in
test_discovery_and_structural.py.
"""
import re
from pathlib import Path

SKILL = (
    Path(__file__).resolve().parents[3]
    / "plugins/mad-scientist-skills/skills/optimization-audit/SKILL.md"
).read_text(encoding="utf-8")


def test_detection_cues_present():
    for n in ("D1", "D3", "D4", "D5", "D6"):
        assert re.search(rf"\b{n}\b", SKILL), f"detection cue {n} missing from SKILL.md"


# D3 — wide copy/select then narrow read; the guard extracts the ACTUAL table grep.
D3_WASTE = "wide = fetch(); df = wide.copy(); use(df['a'])"   # full copy, few fields
D3_OK = "df = fetch()[['a', 'b']]; use(df['a'])"              # narrowed at source


def test_d3_pattern_discriminates(extract_pattern):
    rx = extract_pattern(row_key="Wide copy then narrow read", col=1)
    assert rx.search(D3_WASTE)
    assert not rx.search(D3_OK)
