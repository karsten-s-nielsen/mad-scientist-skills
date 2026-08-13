"""Page-size reduction for the per-word <text> elements PlantUML emits.

Two independent passes are covered here:

* `clean_svg` dropping `lengthAdjust="spacing"` — redundant because "spacing" is
  the SVG initial value.
* `hoist_text_styles` moving CSS-inheritable presentation attributes into shared
  `.c4tN` classes.

Both must be RENDER-IDENTICAL, so the tests assert on what the browser resolves,
not merely on byte count: geometry attributes survive untouched, text content is
unchanged, and non-default values are never rewritten.
"""

import re
import unittest

import c4_assemble


TEXT_OPEN = re.compile(r"<text\b([^>]*)>")
ATTR = re.compile(r'([a-zA-Z:\-]+)\s*=\s*"([^"]*)"')


def attrs_of(svg, n=0):
    return dict(ATTR.findall(TEXT_OPEN.findall(svg)[n]))


class DefaultLengthAdjustTest(unittest.TestCase):
    def test_drops_default_spacing(self):
        svg = ('<svg><g class="entity"><text fill="#FFF" lengthAdjust="spacing" '
               'textLength="53.34" x="40" y="148">Word</text></g></svg>')
        out = c4_assemble.clean_svg(svg)
        self.assertNotIn("lengthAdjust", out)

    def test_keeps_geometry_and_content_intact(self):
        svg = ('<svg><g class="entity"><text fill="#FFF" lengthAdjust="spacing" '
               'textLength="53.34" x="40" y="148">Word</text></g></svg>')
        a = attrs_of(c4_assemble.clean_svg(svg))
        self.assertEqual(a["textLength"], "53.34")
        self.assertEqual(a["x"], "40")
        self.assertEqual(a["y"], "148")
        self.assertIn(">Word</text>", c4_assemble.clean_svg(svg))

    def test_preserves_non_default_spacing_and_glyphs(self):
        # spacingAndGlyphs genuinely changes rendering — dropping it would be a bug.
        svg = ('<svg><text lengthAdjust="spacingAndGlyphs" textLength="53">W</text>'
               "</svg>")
        out = c4_assemble.clean_svg(svg)
        self.assertIn('lengthAdjust="spacingAndGlyphs"', out)


class HoistTextStylesTest(unittest.TestCase):
    def _svg(self, *texts):
        return "<svg>%s</svg>" % "".join(texts)

    def test_hoists_repeated_attributes_into_one_class(self):
        t = '<text fill="#FFFFFF" font-family="sans-serif" font-size="14" x="1" y="2">A</text>'
        svgs, css = c4_assemble.hoist_text_styles({"a": self._svg(t, t, t)})
        self.assertIn(".c4t0{", css)
        self.assertEqual(svgs["a"].count('class="c4t0"'), 3)
        self.assertNotIn('font-family="sans-serif"', svgs["a"])

    def test_font_size_gains_a_css_unit(self):
        # The SVG attribute is unitless user units; the CSS property needs a unit
        # or the declaration is invalid and the text silently falls back.
        t = '<text font-size="14" x="1" y="2">A</text>'
        _svgs, css = c4_assemble.hoist_text_styles({"a": self._svg(t)})
        self.assertIn("font-size:14px", css)

    def test_geometry_attributes_stay_inline(self):
        t = ('<text fill="#FFFFFF" font-size="14" textLength="53.34" x="40" '
             'y="148">Word</text>')
        svgs, _css = c4_assemble.hoist_text_styles({"a": self._svg(t)})
        a = attrs_of(svgs["a"])
        self.assertEqual(a["textLength"], "53.34")
        self.assertEqual(a["x"], "40")
        self.assertEqual(a["y"], "148")
        self.assertIn(">Word</text>", svgs["a"])

    def test_distinct_combinations_get_distinct_classes(self):
        a = '<text fill="#FFFFFF" font-size="14" x="1" y="2">A</text>'
        b = '<text fill="#666666" font-size="12" font-weight="bold" x="1" y="2">B</text>'
        svgs, css = c4_assemble.hoist_text_styles({"a": self._svg(a, b)})
        self.assertEqual(len(re.findall(r"\.c4t\d+\{", css)), 2)
        self.assertIn('class="c4t0"', svgs["a"])
        self.assertIn('class="c4t1"', svgs["a"])

    def test_class_namespace_is_shared_across_svgs(self):
        # Every SVG lands in ONE document, so identical styling in two different
        # panels must resolve to the SAME class — and differing styling must not
        # collide on a reused number.
        same = '<text fill="#FFFFFF" font-size="14" x="1" y="2">A</text>'
        other = '<text fill="#666666" font-size="12" x="1" y="2">B</text>'
        svgs, css = c4_assemble.hoist_text_styles(
            {"one": self._svg(same), "two": self._svg(same, other)})
        self.assertIn('class="c4t0"', svgs["one"])
        self.assertIn('class="c4t0"', svgs["two"])
        self.assertEqual(len(re.findall(r"\.c4t\d+\{", css)), 2)

    def test_ordering_is_deterministic_by_frequency(self):
        rare = '<text fill="#666666" font-size="12" x="1" y="2">B</text>'
        common = '<text fill="#FFFFFF" font-size="14" x="1" y="2">A</text>'
        _s1, css1 = c4_assemble.hoist_text_styles({"a": self._svg(rare, common, common)})
        _s2, css2 = c4_assemble.hoist_text_styles({"a": self._svg(common, common, rare)})
        self.assertEqual(css1, css2)          # same model -> same numbering
        self.assertTrue(css1.startswith(".c4t0{fill:#FFFFFF"))  # most frequent first

    def test_text_without_hoistable_attributes_is_untouched(self):
        t = '<text x="1" y="2">A</text>'
        svgs, css = c4_assemble.hoist_text_styles({"a": self._svg(t)})
        self.assertEqual(svgs["a"], self._svg(t))
        self.assertEqual(css, "")

    def test_no_text_elements_yields_no_css(self):
        svgs, css = c4_assemble.hoist_text_styles({"a": '<svg><rect x="1"/></svg>'})
        self.assertEqual(css, "")
        self.assertEqual(svgs["a"], '<svg><rect x="1"/></svg>')

    def test_hoisted_svg_still_passes_clean_verification(self):
        # verify_clean exits the process on failure; reaching the next line is the
        # assertion. Guards against the rewrite reintroducing active content.
        t = '<text fill="#FFF" font-size="14" x="1" y="2">A</text>'
        svgs, _css = c4_assemble.hoist_text_styles(
            {"a": '<svg><g class="entity">%s</g></svg>' % t})
        c4_assemble.verify_clean("hoisted", svgs["a"])

    def test_entity_count_survives_hoisting(self):
        # count_entities gates the placeholder-SVG check; the rewrite must not
        # disturb the <g class="entity"> prefix it keys on.
        svg = ('<svg><g class="entity"><text fill="#FFF" font-size="14">A</text></g>'
               '<g class="entity"><text fill="#FFF" font-size="14">B</text></g></svg>')
        self.assertEqual(c4_assemble.count_entities(svg), 2)
        svgs, _css = c4_assemble.hoist_text_styles({"a": svg})
        self.assertEqual(c4_assemble.count_entities(svgs["a"]), 2)

    def test_leaves_self_closing_text_alone(self):
        # Rebuilding the tag would drop the '/', turning an empty element into an
        # unclosed one and corrupting everything after it.
        svg = '<svg><text fill="#FFF" font-size="14" x="1"/></svg>'
        svgs, _css = c4_assemble.hoist_text_styles({"a": svg})
        self.assertEqual(svgs["a"], svg)

    def test_leaves_single_quoted_attributes_alone(self):
        # The attribute parser understands double quotes only; rewriting a tag it
        # only partly parsed would silently drop x=' 1' from the output.
        svg = "<svg><text fill=\"#FFF\" font-size=\"14\" x='1' y='2'>A</text></svg>"
        svgs, _css = c4_assemble.hoist_text_styles({"a": svg})
        self.assertEqual(svgs["a"], svg)

    def test_drill_wired_attributes_survive_hoisting(self):
        # Hoisting runs after wire_drilldown, so the injected handler must be
        # carried through untouched.
        svg = ('<svg><g class="entity" data-qualified-name="A" role="button" '
               'onclick="c4ShowTab(\'component-a\')">'
               '<text fill="#FFF" font-size="14">A</text></g></svg>')
        svgs, _css = c4_assemble.hoist_text_styles({"a": svg})
        self.assertIn("c4ShowTab('component-a')", svgs["a"])


class HoistFailsSafeTest(unittest.TestCase):
    """The hoist exists only to shrink the page, so a violated invariant must cost
    the size win, never the diagram."""

    def test_tag_structure_violation_falls_back_to_unhoisted(self):
        original = c4_assemble._TEXT_OPEN_RE

        class Corrupting:
            """Stands in for the rewrite losing a tag boundary."""
            def finditer(self, s):
                return original.finditer(s)

            def sub(self, _repl, s):
                return s.replace("</text>", "")   # drops two angle brackets

        svg = '<svg><text fill="#FFF" font-size="14">A</text></svg>'
        c4_assemble._TEXT_OPEN_RE = Corrupting()
        try:
            out, css = c4_assemble.hoist_text_styles({"a": svg})
        finally:
            c4_assemble._TEXT_OPEN_RE = original
        self.assertEqual(out["a"], svg)   # un-hoisted original, not the corruption
        self.assertEqual(css, "")

    def test_verify_clean_is_not_re_runnable_after_wiring(self):
        # Documents WHY the invariant check above exists rather than a second
        # verify_clean pass: drill-down wiring injects the on*= handlers that
        # verify_clean rejects, so re-verifying post-wiring would abort the build.
        svg = ('<svg><g class="entity" data-qualified-name="Sys.Api">'
               "<rect/></g></svg>")
        wired, n = c4_assemble.wire_drilldown(svg, {"Sys.Api": "Component_api"})
        self.assertEqual(n, 1)
        with self.assertRaises(SystemExit):
            c4_assemble.verify_clean("wired", wired)


class HoistedCssReachesThePageTest(unittest.TestCase):
    def test_build_html_embeds_the_generated_rules(self):
        views = [("f.svg", "containers", "Containers", "Containers")]
        html = c4_assemble.build_html(views, {"containers": "<svg/>"}, "dsl", "Sys",
                                      text_css=".c4t0{fill:#FFFFFF}")
        self.assertIn(".c4t0{fill:#FFFFFF}", html)
        # Must land inside the page's own <style> block, not loose in the body.
        self.assertLess(html.index(".c4t0{fill:#FFFFFF}"), html.index("</style>"))

    def test_text_css_is_optional(self):
        views = [("f.svg", "containers", "Containers", "Containers")]
        html = c4_assemble.build_html(views, {"containers": "<svg/>"}, "dsl", "Sys")
        self.assertIn("</style>", html)


if __name__ == "__main__":
    unittest.main()
