"""Content guard for the research-discipline skill.

Machine-locks the load-bearing invariants Karsten ruled on (spec §8): the E1-E7
headline is present and one-line each, the validity ladder and multi-pass protocol
are present, the seven reference files exist, the sources + NOTICE attribution are
in place, and the skill is public-cite-safe (the S3 softening left no bare
percentage behind). Per-Part 1:1 faithfulness is NOT machine-checked here — that is
the manual source-diff in the plan's Task 9.2 / spec §6.

This directory has NO __init__.py on purpose: ``research-discipline`` is not a valid
Python package name (hyphen), so pytest loads this module by path (prepend mode),
exactly as it does for the sibling ``optimization-audit`` guards.
"""
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
SKILL_DIR = REPO_ROOT / "plugins/mad-scientist-skills/skills/research-discipline"
SKILL_MD = SKILL_DIR / "SKILL.md"
REFERENCES_DIR = SKILL_DIR / "references"
NOTICE_MD = REPO_ROOT / "NOTICE.md"

REFERENCE_FILES = (
    "validity-ladder.md",
    "attribution.md",
    "data-preflight.md",
    "reproducibility.md",
    "reviewing.md",
    "defect-smell-test.md",
    "sources.md",
)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _shipped_files() -> list[Path]:
    """SKILL.md plus every reference file — the files that ship to users."""
    return [SKILL_MD] + [REFERENCES_DIR / name for name in REFERENCE_FILES]


def _frontmatter(text: str) -> str:
    match = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    assert match is not None, "SKILL.md has no YAML frontmatter block"
    return match.group(1)


def test_frontmatter_names_the_skill_with_specific_triggers():
    fm = _frontmatter(_read(SKILL_MD))
    name = re.search(r"(?m)^name:\s*(.+?)\s*$", fm)
    desc = re.search(r"(?m)^description:\s*(.+?)\s*$", fm)
    assert name and name.group(1) == "research-discipline", "frontmatter name must be research-discipline"
    assert desc and desc.group(1), "frontmatter description must be non-empty"
    lowered = desc.group(1).lower()
    assert "metric" in lowered and ("design" in lowered or "validat" in lowered), (
        "description must carry the specific design/validate triggers (bare 'review' collides — spec §8 S9)"
    )


def test_e1_through_e7_present_each_on_one_line():
    # Faithful to the source, E1-E7 are bulleted list items ("- **E1 — ..."), so the
    # header anchors at "- **E<n> ". The [1-7] digit class still excludes a bold bullet
    # like "- **Efficacy ..." (its first char after "E" is not a digit).
    numbers = re.findall(r"(?m)^- \*\*E([1-7]) ", _read(SKILL_MD))
    assert sorted(numbers) == ["1", "2", "3", "4", "5", "6", "7"], (
        f"expected E1-E7 as one-bullet '- **E<n> ' headers, got {numbers}"
    )


def test_part_a_preamble_present():
    # Source :21 — a proposal must clear all seven before it is called validated.
    assert "clear all seven" in _read(SKILL_MD), "the Part-A preamble (source :21) is missing from SKILL.md"


def test_validity_ladder_and_multipass_sections_present():
    skill = _read(SKILL_MD).lower()
    assert "validity ladder" in skill, "the compact validity ladder section is missing from SKILL.md"
    assert "multi-pass" in skill, "the compact multi-pass review protocol section is missing from SKILL.md"


def test_all_seven_reference_files_exist():
    missing = [name for name in REFERENCE_FILES if not (REFERENCES_DIR / name).is_file()]
    assert not missing, f"missing reference files: {missing}"


def test_sources_cite_rahimian_and_landis_koch():
    sources = _read(REFERENCES_DIR / "sources.md")
    for token in ("Rahimian", "Landis", "Koch"):
        assert token in sources, f"sources.md must cite {token!r}"


def test_notice_has_a_research_discipline_section():
    assert "## research-discipline" in _read(NOTICE_MD), (
        "NOTICE.md must carry a '## research-discipline' section (the single citation home)"
    )


def test_no_bare_percentage_anywhere_in_the_shipped_skill():
    # The S3 ruling dropped the only figure (the >=17% in Part F); nothing legitimate
    # (CI, significance, percentile) survives, so a bare \d+% is a cite-safety leak.
    offenders = {
        path.name: re.findall(r"\d+%", _read(path))
        for path in _shipped_files()
        if re.search(r"\d+%", _read(path))
    }
    assert not offenders, f"bare percentage(s) found (cite-safety leak, spec §8 S3): {offenders}"


def test_no_claude_md_without_agents_md_in_shipped_files():
    offenders = []
    for path in _shipped_files():
        for lineno, line in enumerate(_read(path).splitlines(), 1):
            if "CLAUDE.md" in line and "AGENTS.md" not in line:
                offenders.append(f"{path.name}:{lineno}")
    assert not offenders, f"shipped file names CLAUDE.md without AGENTS.md: {offenders}"
