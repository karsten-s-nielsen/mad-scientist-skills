"""Guard: audit/review skills treat CLAUDE.md and AGENTS.md as a pair.

Two contracts (spec docs/plans/2026-09-25-agents-md-alignment-design.md §5):
  5.1  Every SKILL.md read-list line naming CLAUDE.md must also name AGENTS.md.
  5.2  Every line under plugins/**/*.md naming CLAUDE.md must also name AGENTS.md,
       except explicitly allow-listed lines.
"""
from __future__ import annotations

import re
from pathlib import Path

PLUGINS = Path(__file__).resolve().parent.parent / "plugins"
REPO_ROOT = PLUGINS.parent

# Read-list lines look like:  "- Read `CLAUDE.md`, `AGENTS.md`, `README.md`, ..."
READ_LIST_RE = re.compile(r"^\s*[-*]?\s*Read\b")

# (relative posix path, substring of the offending line) pairs that legitimately
# name only CLAUDE.md. EMPTY today — every CLAUDE.md line under plugins/ pairs with
# AGENTS.md. Each future entry MUST carry a comment explaining why the pairing does
# not apply to that line.
ALLOWLIST: set[tuple[str, str]] = set()


def _iter_lines(paths):
    for path in paths:
        rel = path.relative_to(REPO_ROOT).as_posix()
        for lineno, line in enumerate(
            path.read_text(encoding="utf-8").splitlines(), start=1
        ):
            yield rel, lineno, line


def test_read_list_skills_list_agents_md():
    offenders = [
        f"{rel}:{lineno}: {line.strip()}"
        for rel, lineno, line in _iter_lines(sorted(PLUGINS.rglob("SKILL.md")))
        if READ_LIST_RE.match(line) and "CLAUDE.md" in line and "AGENTS.md" not in line
    ]
    assert not offenders, (
        "Read-list lines naming CLAUDE.md must also name AGENTS.md "
        "(add `AGENTS.md` to the read list):\n" + "\n".join(offenders)
    )


def test_no_claude_md_without_agents_md():
    offenders = []
    for rel, lineno, line in _iter_lines(sorted(PLUGINS.rglob("*.md"))):
        if "CLAUDE.md" not in line or "AGENTS.md" in line:
            continue
        if any(a_rel == rel and sub in line for a_rel, sub in ALLOWLIST):
            continue
        offenders.append(f"{rel}:{lineno}: {line.strip()}")
    assert not offenders, (
        "Lines naming CLAUDE.md must also name AGENTS.md. Fix each by pairing it with "
        "AGENTS.md, or add (path, substring) to ALLOWLIST with a reason:\n"
        + "\n".join(offenders)
    )
