"""Pytest path setup for skill test suites.

Skill directories ship verbatim when a user installs the plugin, so only runtime
files belong under `plugins/<plugin>/skills/<skill>/`; their tests live under
`tests/skills/<skill>/` instead. That split means a test module cannot import the
module under test as a sibling, so make each skill directory importable here
rather than repeating a `sys.path` insert in every test module.
"""
import os
import sys

_SKILLS_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "plugins", "mad-scientist-skills", "skills")

# Every skill directory that ships an importable Python module. Each entry goes on
# sys.path in its own right, so two skills shipping the same module name would
# shadow each other silently — give runtime modules skill-specific names (as
# `c4_assemble.py` already is) rather than relying on insertion order.
for _skill in ("c4",):
    _path = os.path.join(_SKILLS_DIR, _skill)
    if _path not in sys.path:
        sys.path.insert(0, _path)
