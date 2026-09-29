"""Shared fixtures for the optimization-audit skill guards.

NOTE: this directory has NO __init__.py on purpose — `optimization-audit` is not a
valid Python package name (hyphen). pytest loads conftest.py by path, so the
fixture is available without any import, and the test modules load via pytest's
default prepend mode.
"""
import re
from pathlib import Path

import pytest

SKILL_PATH = (
    Path(__file__).resolve().parents[3]
    / "plugins/mad-scientist-skills/skills/optimization-audit/SKILL.md"
)


@pytest.fixture
def extract_pattern():
    """Return a helper that compiles the regex from the Phase-0 table row containing row_key.

    row_key: a stable, unique substring of the row (its Issue column).
    col: the 0-based cell index of the Pattern column in that table.
    Splits on UNescaped '|' only (so a pattern's own '\\|' alternation survives),
    strips the wrapping backticks, then un-escapes '\\|' -> '|' before compiling.
    Raises StopIteration if the row is absent — the RED state before it is added.
    """

    def _extract(row_key: str, col: int) -> "re.Pattern":
        text = SKILL_PATH.read_text(encoding="utf-8")
        row = next(
            l
            for l in text.splitlines()
            if l.lstrip().startswith("|") and row_key in l
        )
        cells = [c.strip() for c in re.split(r"(?<!\\)\|", row.strip().strip("|"))]
        return re.compile(cells[col].strip("`").replace(r"\|", "|"))

    return _extract
