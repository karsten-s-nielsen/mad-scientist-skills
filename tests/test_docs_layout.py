"""Guard: design/research docs live in docs/specs/, never docs/plans/ (ADR-003).

Before ADR-003 the flat docs/plans/ held both -design.md and -plan.md, which let
a design doc (a spec) sit in a folder named "plans". This guard prevents that
bundling from recurring.
"""
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOCS = REPO_ROOT / "docs"

# The exact set the migration moves. Asserting the specific basenames (not just
# "some *-design.md exists") keeps the test genuinely red before the move — the
# lone untracked feature spec already in docs/specs/ must NOT be enough to pass it.
MIGRATED = {
    "2026-03-08-observability-audit-design.md",
    "2026-03-08-optimization-audit-design.md",
    "2026-03-08-optimization-audit-research.md",
    "2026-03-27-documentation-audit-design.md",
    "2026-08-28-unbiased-review-skill-design.md",
    "2026-09-25-agents-md-alignment-design.md",
}


def test_no_design_or_research_docs_in_plans():
    plans = DOCS / "plans"
    stray = sorted(
        p.name
        for p in plans.glob("*.md")
        if p.stem.endswith("-design") or p.stem.endswith("-research")
    )
    assert stray == [], (
        "design/research docs must live in docs/specs/, "
        f"found in docs/plans/: {stray}"
    )


def test_migrated_designs_live_in_specs():
    specs = DOCS / "specs"
    assert specs.is_dir(), "docs/specs/ must exist (ADR-003)"
    present = {p.name for p in specs.glob("*.md")}
    missing = sorted(MIGRATED - present)
    assert not missing, (
        f"migrated design/research docs missing from docs/specs/: {missing}"
    )
