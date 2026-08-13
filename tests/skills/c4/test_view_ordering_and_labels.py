"""Tab ordering, tab labelling, and the view-density warning.

Covers three assembler behaviours that decide what the tab row looks like and
whether an over-dense view gets flagged:

* `detect_views` ordering project-specific views by their position in the DSL's
  `views` block instead of by filename.
* An explicit `--views` label outranking the DSL-derived container display name.
* The advisory warning when a view exceeds MAX_ELEMENTS_PER_VIEW.
"""

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import c4_assemble

_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))
SCRIPT = os.path.join(_REPO_ROOT, "plugins", "mad-scientist-skills",
                      "skills", "c4", "c4_assemble.py")


def _entity_svg(n):
    """An SVG carrying n `<g class="entity">` nodes."""
    return ('<svg xmlns="http://www.w3.org/2000/svg">%s</svg>'
            % ''.join('<g class="entity" data-qualified-name="E%d">'
                      '<rect width="10" height="10"/></g>' % i for i in range(n)))


class DetectViewsOrderingTest(unittest.TestCase):
    def _dir(self, filenames):
        d = tempfile.mkdtemp()
        for fn in filenames:
            with open(os.path.join(d, fn), "w", encoding="utf-8") as fh:
                fh.write("<svg></svg>")
        return Path(d)

    # Named so the alphabetical fallback and the DSL order disagree.
    FILES = ["structurizr-Containers_Zebra.svg",
             "structurizr-Containers_Alpha.svg",
             "structurizr-Containers_Mango.svg"]

    def test_falls_back_to_filename_order_without_dsl_order(self):
        views = c4_assemble.detect_views(self._dir(self.FILES))
        self.assertEqual([v[3] for v in views],
                         ["Containers_Alpha", "Containers_Mango", "Containers_Zebra"])

    def test_follows_dsl_declaration_order(self):
        views = c4_assemble.detect_views(
            self._dir(self.FILES),
            dsl_order=["Containers_Zebra", "Containers_Mango", "Containers_Alpha"])
        self.assertEqual([v[3] for v in views],
                         ["Containers_Zebra", "Containers_Mango", "Containers_Alpha"])

    def test_keys_absent_from_the_dsl_sort_last_alphabetically(self):
        # A rendered SVG with no matching DSL declaration still has to land
        # somewhere deterministic rather than jumping around between builds.
        views = c4_assemble.detect_views(
            self._dir(self.FILES), dsl_order=["Containers_Zebra"])
        self.assertEqual([v[3] for v in views],
                         ["Containers_Zebra", "Containers_Alpha", "Containers_Mango"])

    def test_known_views_keep_their_fixed_order_ahead_of_the_rest(self):
        d = self._dir(self.FILES + ["structurizr-SystemContext.svg"])
        views = c4_assemble.detect_views(d, dsl_order=["Containers_Zebra",
                                                       "SystemContext"])
        self.assertEqual(views[0][3], "SystemContext")


class ExplicitViewLabelTest(unittest.TestCase):
    """An explicit --views label is the author speaking directly and must win."""

    DSL = ('workspace "Sys" {\n  model {\n'
           '    s = softwareSystem "Sys" "d" {\n'
           '      api = container "Analytics & SAM" "d"\n'
           '    }\n  }\n'
           '  views {\n'
           '    systemContext s "SystemContext" { include * }\n'
           '    component api "Component_api" { include * }\n'
           '  }\n}\n')

    def _run(self, d, views_spec, svg_name):
        dsl_path = os.path.join(d, "architecture.dsl")
        with open(dsl_path, "w", encoding="utf-8") as fh:
            fh.write(self.DSL)
        svg_dir = os.path.join(d, "svgs")
        os.makedirs(svg_dir, exist_ok=True)
        for fn in svg_name:
            with open(os.path.join(svg_dir, fn), "w", encoding="utf-8") as fh:
                fh.write(_entity_svg(1))
        out = os.path.join(d, "architecture.html")
        cmd = [sys.executable, SCRIPT, d, "--dsl-path", dsl_path,
               "--svg-dir", svg_dir, "--system-name", "Sys", "--output", out]
        if views_spec:
            cmd += ["--views"] + views_spec
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        with open(out, encoding="utf-8") as fh:
            return fh.read()

    FILES = ["structurizr-Component_api.svg", "structurizr-Component_other.svg"]

    def test_explicit_label_overrides_dsl_container_name(self):
        with tempfile.TemporaryDirectory() as d:
            html = self._run(d, [
                "Component_api:Provider Slice:structurizr-Component_api.svg",
                "Component_other:Other Slice:structurizr-Component_other.svg",
            ], self.FILES)
            self.assertIn("Provider Slice", html)

    def test_autodetect_still_uses_the_dsl_container_name(self):
        # Regression guard: detect_views synthesizes a label from the view key, so
        # letting labels win unconditionally would drop "Analytics & SAM" back to
        # the bare suffix "api".
        with tempfile.TemporaryDirectory() as d:
            html = self._run(d, None, self.FILES)
            self.assertIn("Analytics &amp; SAM", html)


class ViewDensityWarningTest(unittest.TestCase):
    """MAX_ELEMENTS_PER_VIEW was defined but nothing acted on it, so a view could
    drift well past the guideline unnoticed. The check is advisory: warn, never
    fail — a legitimately flat system may exceed it."""

    DSL = ('workspace "Sys" {\n  model {\n    s = softwareSystem "Sys" "d"\n  }\n'
           '  views {\n    systemContext s "SystemContext" { include * }\n  }\n}\n')

    def _run(self, d, n_entities):
        dsl_path = os.path.join(d, "architecture.dsl")
        with open(dsl_path, "w", encoding="utf-8") as fh:
            fh.write(self.DSL)
        svg_dir = os.path.join(d, "svgs")
        os.makedirs(svg_dir, exist_ok=True)
        with open(os.path.join(svg_dir, "structurizr-SystemContext.svg"),
                  "w", encoding="utf-8") as fh:
            fh.write(_entity_svg(n_entities))
        out = os.path.join(d, "architecture.html")
        return subprocess.run(
            [sys.executable, SCRIPT, d, "--dsl-path", dsl_path, "--svg-dir", svg_dir,
             "--system-name", "Sys", "--output", out],
            capture_output=True, text=True, timeout=60)

    def test_warns_above_the_guideline_without_failing(self):
        with tempfile.TemporaryDirectory() as d:
            r = self._run(d, c4_assemble.MAX_ELEMENTS_PER_VIEW + 1)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            self.assertIn("WARN", r.stderr)
            self.assertIn(str(c4_assemble.MAX_ELEMENTS_PER_VIEW), r.stderr)

    def test_silent_at_the_guideline(self):
        with tempfile.TemporaryDirectory() as d:
            r = self._run(d, c4_assemble.MAX_ELEMENTS_PER_VIEW)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            self.assertNotIn("readability guideline", r.stderr)


if __name__ == "__main__":
    unittest.main()
