import os
import subprocess
import sys
import tempfile
import unittest

import c4_assemble  # noqa: E402

# This module shells out to the script instead of only importing it, so it needs
# the shipped path, which conftest.py's sys.path entry does not provide.
# tests/skills/c4/ -> repo root is three levels up.
_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))

SCRIPT = os.path.join(_REPO_ROOT, "plugins", "mad-scientist-skills",
                      "skills", "c4", "c4_assemble.py")

# Minimal SVGs — count_entities keys on `<g class="entity"`.
SVG_ONE_ENTITY = ('<svg xmlns="http://www.w3.org/2000/svg">'
                  '<g class="entity" data-qualified-name="Sys">'
                  '<rect width="10" height="10"/></g></svg>')
SVG_ZERO_ENTITY = ('<svg xmlns="http://www.w3.org/2000/svg">'
                   '<text>Syntax Error</text></svg>')

VALID_DSL = ('workspace "Sys" {\n  model {\n'
             '    s = softwareSystem "Sys" "d"\n  }\n'
             '  views {\n    systemContext s "SystemContext" { include * }\n  }\n}\n')
# Unbalanced braces make parse_dsl_model raise IndexError; main()'s try/except
# must catch it and degrade to no drill-down rather than crash the build.
MALFORMED_DSL = '}}}{{{ = = softwareSystem\n'


def _run(project_dir, dsl_text, svg_name, svg_text, out_path, extra=None):
    """Invoke c4_assemble.py as main() would run from the CLI.

    Returns the completed process (returncode, stdout, stderr)."""
    dsl_path = os.path.join(project_dir, "architecture.dsl")
    with open(dsl_path, "w", encoding="utf-8") as fh:
        fh.write(dsl_text)
    svg_dir = os.path.join(project_dir, "svgs")
    os.makedirs(svg_dir, exist_ok=True)
    with open(os.path.join(svg_dir, svg_name), "w", encoding="utf-8") as fh:
        fh.write(svg_text)
    cmd = [sys.executable, SCRIPT, project_dir,
           "--dsl-path", dsl_path,
           "--svg-dir", svg_dir,
           "--views", "SystemContext:Context:" + svg_name,
           "--system-name", "Sys",
           "--output", out_path]
    if extra:
        cmd += extra
    return subprocess.run(cmd, capture_output=True, text=True, timeout=60)


class MainZeroEntityAbortTest(unittest.TestCase):
    """A placeholder SVG (Graphviz-missing / syntax-error) has 0 entity nodes.
    main() must abort (exit 1) rather than embed a non-diagram, and must NOT
    write the output file."""

    def test_zero_entity_svg_aborts_without_writing(self):
        with tempfile.TemporaryDirectory() as d:
            out = os.path.join(d, "architecture.html")
            r = _run(d, VALID_DSL, "structurizr-SystemContext.svg",
                     SVG_ZERO_ENTITY, out)
            self.assertNotEqual(r.returncode, 0, r.stdout + r.stderr)
            self.assertIn("0", r.stderr)
            self.assertFalse(os.path.exists(out), "output must not be written on abort")

    def test_one_entity_svg_succeeds(self):
        # Control: the same flow with a real diagram writes HTML and exits 0.
        with tempfile.TemporaryDirectory() as d:
            out = os.path.join(d, "architecture.html")
            r = _run(d, VALID_DSL, "structurizr-SystemContext.svg",
                     SVG_ONE_ENTITY, out)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            self.assertTrue(os.path.exists(out))


class MainParseFailureDegradationTest(unittest.TestCase):
    """parse_dsl_model can raise on malformed DSL (e.g. unbalanced braces ->
    IndexError). main()'s contract is 'parsing must never crash assembly —
    degrade to no drill-down': it must still write HTML and exit 0."""

    def test_malformed_dsl_still_writes_html(self):
        with tempfile.TemporaryDirectory() as d:
            out = os.path.join(d, "architecture.html")
            r = _run(d, MALFORMED_DSL, "structurizr-SystemContext.svg",
                     SVG_ONE_ENTITY, out)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            self.assertTrue(os.path.exists(out), "HTML must still be written")
            self.assertIn("parse failed", (r.stdout + r.stderr).lower())
            with open(out, encoding="utf-8") as fh:
                page = fh.read()
            self.assertIn("<!DOCTYPE html>", page)


class ParseViewSpecTest(unittest.TestCase):
    """parse_view_spec('key:label:filename') -> 4-tuple; anything not exactly
    three colon-separated parts aborts (a colon in the label breaks it)."""

    def test_valid_spec(self):
        self.assertEqual(
            c4_assemble.parse_view_spec("Component_api:API:structurizr-Component_api.svg"),
            ("structurizr-Component_api.svg", "component-api", "API",
             "Component_api"))

    def test_too_few_parts_aborts(self):
        with self.assertRaises(SystemExit):
            c4_assemble.parse_view_spec("key:label")

    def test_too_many_parts_aborts(self):
        # A colon inside the label yields 4 parts -> rejected.
        with self.assertRaises(SystemExit):
            c4_assemble.parse_view_spec("key:my:label:file.svg")

    def test_no_colon_aborts(self):
        with self.assertRaises(SystemExit):
            c4_assemble.parse_view_spec("justakey")


if __name__ == "__main__":
    unittest.main()
