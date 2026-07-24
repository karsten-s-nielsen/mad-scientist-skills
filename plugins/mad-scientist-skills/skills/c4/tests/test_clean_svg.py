import os
import sys
import unittest

# c4_assemble.py sits one directory up from tests/.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import c4_assemble  # noqa: E402


class CleanSvgTest(unittest.TestCase):
    def test_strips_plantuml_processing_instruction(self):
        svg = '<?plantuml version="1"?>\n<svg><rect/></svg>'
        out = c4_assemble.clean_svg(svg)
        self.assertNotIn("<?plantuml", out)
        self.assertIn("<rect/>", out)

    def test_strips_title_element(self):
        svg = "<svg><title>encoded title</title><rect/></svg>"
        out = c4_assemble.clean_svg(svg)
        self.assertNotIn("<title>", out)

    def test_strips_title_group_with_extra_attributes(self):
        # The opening tag carries attributes beyond class="title" — the regex
        # must match them or cleaning silently no-ops.
        svg = '<svg><g class="title" data-source-line="1"><text>T</text></g><rect/></svg>'
        out = c4_assemble.clean_svg(svg)
        self.assertNotIn('class="title"', out)
        self.assertIn("<rect/>", out)


class CleanSvgActiveContentTest(unittest.TestCase):
    """The cleaned SVG is embedded verbatim into architecture.html. The module
    bills itself as 'cleaning' the SVG, so it must also strip active content —
    <script>, <foreignObject>, on*= handlers, and javascript:/vbscript: hrefs —
    rather than shipping them. Legitimate PlantUML output (data:image icons,
    #fragment refs) must survive untouched."""

    def test_strips_script_element(self):
        svg = '<svg><script>alert(1)</script><rect/></svg>'
        out = c4_assemble.clean_svg(svg)
        self.assertNotIn("<script", out)
        self.assertNotIn("alert(1)", out)
        self.assertIn("<rect/>", out)

    def test_strips_script_with_attributes(self):
        svg = '<svg><script type="text/javascript">x()</script><rect/></svg>'
        out = c4_assemble.clean_svg(svg)
        self.assertNotIn("<script", out)
        self.assertNotIn("x()", out)

    def test_strips_foreign_object(self):
        svg = ('<svg><foreignObject width="10" height="10">'
               '<body xmlns="http://www.w3.org/1999/xhtml"><iframe/></body>'
               '</foreignObject><rect/></svg>')
        out = c4_assemble.clean_svg(svg)
        self.assertNotIn("foreignObject", out)
        self.assertNotIn("<iframe", out)
        self.assertIn("<rect/>", out)

    def test_strips_event_handler_attributes(self):
        svg = '<svg><rect onload="evil()" onclick="bad()" width="1"/></svg>'
        out = c4_assemble.clean_svg(svg)
        self.assertNotIn("onload", out)
        self.assertNotIn("onclick", out)
        self.assertNotIn("evil()", out)
        self.assertIn('width="1"', out)   # benign attribute preserved

    def test_neutralizes_javascript_href(self):
        svg = '<svg><a xlink:href="javascript:alert(1)"><rect/></a></svg>'
        out = c4_assemble.clean_svg(svg)
        self.assertNotIn("javascript:", out)

    def test_neutralizes_plain_javascript_href(self):
        svg = '<svg><a href="javascript:alert(1)"><rect/></a></svg>'
        out = c4_assemble.clean_svg(svg)
        self.assertNotIn("javascript:", out)

    def test_neutralizes_vbscript_href(self):
        svg = '<svg><a xlink:href="vbscript:msgbox(1)"><rect/></a></svg>'
        out = c4_assemble.clean_svg(svg)
        self.assertNotIn("vbscript:", out)

    def test_preserves_data_image_href(self):
        # PlantUML embeds icons via xlink:href="data:image/png;base64,..." —
        # the hardening must NOT strip these.
        svg = ('<svg><image xlink:href="data:image/png;base64,iVBORw0KGgo="'
               ' width="16" height="16"/><rect/></svg>')
        out = c4_assemble.clean_svg(svg)
        self.assertIn("data:image/png;base64,iVBORw0KGgo=", out)

    def test_preserves_fragment_href(self):
        svg = '<svg><a xlink:href="#node1"><rect/></a></svg>'
        out = c4_assemble.clean_svg(svg)
        self.assertIn('xlink:href="#node1"', out)

    def test_real_fixture_survives_and_keeps_icons(self):
        fixtures = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")
        with open(os.path.join(fixtures, "containers.svg"), encoding="utf-8") as fh:
            svg = fh.read()
        out = c4_assemble.clean_svg(svg)
        # Embedded PNG icons and entity nodes must be untouched by hardening.
        self.assertIn("data:image", out)
        self.assertEqual(c4_assemble.count_entities(out), 4)


class VerifyCleanActiveContentTest(unittest.TestCase):
    """verify_clean is the post-clean gate that aborts the build on a leak. It
    must fail (SystemExit) when active content survives, and pass on clean SVG."""

    def test_aborts_on_surviving_script(self):
        with self.assertRaises(SystemExit):
            c4_assemble.verify_clean("x", '<svg><script>alert(1)</script></svg>')

    def test_aborts_on_surviving_foreign_object(self):
        with self.assertRaises(SystemExit):
            c4_assemble.verify_clean("x", '<svg><foreignObject></foreignObject></svg>')

    def test_aborts_on_surviving_event_handler(self):
        with self.assertRaises(SystemExit):
            c4_assemble.verify_clean("x", '<svg><rect onload="x()"/></svg>')

    def test_aborts_on_surviving_javascript_href(self):
        with self.assertRaises(SystemExit):
            c4_assemble.verify_clean("x", '<svg><a href="javascript:x()"/></svg>')

    def test_passes_on_clean_svg_with_data_image(self):
        # Must NOT abort on legitimate embedded icons.
        try:
            c4_assemble.verify_clean(
                "x", '<svg><image href="data:image/png;base64,AAAA"/><rect/></svg>')
        except SystemExit:
            self.fail("verify_clean aborted on a clean SVG with a data:image icon")


class HandlerAnchoredToStartTagTest(unittest.TestCase):
    """The on*= handler match (clean_svg step 7 + verify_clean guard) must be
    anchored to an element START-TAG, mirroring where a handler can actually
    execute. Unanchored, the pattern also fires on `<text>` prose that happens
    to contain a word like 'online=' or 'only=', causing either a false build
    ABORT (verify_clean) or silent CORRUPTION (clean_svg's lazy strip eats
    everything up to the next quote, across tag boundaries). Genuine handlers
    live only inside a start tag: `<... on...="...">`."""

    # --- verify_clean: must NOT abort on benign text-node prose ---
    def test_verify_clean_passes_on_prose_online_equals(self):
        try:
            c4_assemble.verify_clean("x", '<svg><text>Sets online=true</text></svg>')
        except SystemExit:
            self.fail("verify_clean aborted on benign <text> prose 'online=true'")

    def test_verify_clean_passes_on_prose_read_only_quoted(self):
        # An on-word followed by a QUOTED token in prose (the corruption shape).
        try:
            c4_assemble.verify_clean(
                "x", '<svg><text>mode read only="30"</text></svg>')
        except SystemExit:
            self.fail("verify_clean aborted on benign <text> prose 'read only=\"30\"'")

    def test_verify_clean_passes_on_prose_onclick_spaced(self):
        try:
            c4_assemble.verify_clean(
                "x", '<svg><text>calls onClick = handler</text></svg>')
        except SystemExit:
            self.fail("verify_clean aborted on benign <text> prose 'onClick = handler'")

    # --- verify_clean: must STILL abort on real handlers (quoted + unquoted) ---
    def test_verify_clean_still_aborts_on_quoted_handler(self):
        with self.assertRaises(SystemExit):
            c4_assemble.verify_clean("x", '<svg><rect onload="x()"/></svg>')

    def test_verify_clean_still_aborts_on_unquoted_handler(self):
        # The deliberate fail-closed case: clean_svg can't safely strip an
        # unquoted handler, so verify_clean must still abort on it.
        with self.assertRaises(SystemExit):
            c4_assemble.verify_clean("x", '<svg><rect onclick=alert(1)/></svg>')

    def test_verify_clean_aborts_on_multiline_start_tag_handler(self):
        # [^>] must span newlines so a handler on a wrapped start tag is caught.
        with self.assertRaises(SystemExit):
            c4_assemble.verify_clean(
                "x", '<svg><rect\n  width="1"\n  onload="x()"/></svg>')

    # --- clean_svg: must NOT corrupt text-node prose ---
    def test_clean_svg_preserves_prose_with_handler_shaped_word(self):
        svg = '<svg><text>read only="30" limit</text><rect width="1"/></svg>'
        out = c4_assemble.clean_svg(svg)
        self.assertIn('read only="30" limit', out)
        self.assertIn('<rect width="1"/>', out)

    def test_clean_svg_does_not_delete_across_tag_boundary(self):
        # The lazy `[\s\S]*?"` in the old unanchored strip would delete real
        # markup up to the next quote in a following tag.
        svg = '<svg><text>only="x</text><rect fill="y"/></svg>'
        out = c4_assemble.clean_svg(svg)
        self.assertIn('<rect fill="y"/>', out)
        self.assertIn('<text>only="x</text>', out)

    # --- clean_svg: must STILL strip a real quoted handler ---
    def test_clean_svg_still_strips_real_quoted_handler(self):
        out = c4_assemble.clean_svg('<svg><rect onload="evil()" width="1"/></svg>')
        self.assertNotIn("onload", out)
        self.assertNotIn("evil()", out)
        self.assertIn('width="1"', out)


class VerifyCleanBypassRegressionTest(unittest.TestCase):
    """Fail-closed regression (Finding 1): active content that evades clean_svg's
    deliberately-conservative strip must still ABORT at the verify gate, not ship.

    Two evasion shapes the whitespace-only guards missed:
    - SLASH-separated handlers. HTML accepts `/` as an attribute separator, so
      `<svg/onload=...>` parses as `<svg onload=...>` and fires on load — no click,
      no whitespace before `on`. The guard must anchor on `[\\s/]`, not `\\s`.
    - OBFUSCATED dangerous schemes. Browsers HTML-decode an href and strip control
      chars from the scheme before resolving it, so `jav&#x61;script:` and
      `java\\tscript:` both become `javascript:`. A raw-substring scan misses them;
      the gate must normalize (unescape + strip control chars) before matching, and
      also reject `data:text/html`.

    clean_svg is not asked to surgically neutralize these hostile shapes (PlantUML
    never emits them) — the gate simply refuses to ship them."""

    def test_aborts_on_slash_separated_svg_onload(self):
        # <svg/onload=...> executes immediately on parse — the worst case.
        with self.assertRaises(SystemExit):
            c4_assemble.verify_clean("x", '<svg/onload="alert(1)"><rect/></svg>')

    def test_aborts_on_slash_separated_handler_on_child(self):
        with self.assertRaises(SystemExit):
            c4_assemble.verify_clean("x", '<g class="entity"/onclick="x()"></g>')

    def test_aborts_on_entity_obfuscated_javascript_href(self):
        # jav&#x61;script: -> javascript: after HTML-entity decoding.
        with self.assertRaises(SystemExit):
            c4_assemble.verify_clean(
                "x", '<a xlink:href="jav&#x61;script:alert(1)">x</a>')

    def test_aborts_on_control_char_obfuscated_javascript_href(self):
        # Embedded tab: browsers ignore control chars in the scheme.
        with self.assertRaises(SystemExit):
            c4_assemble.verify_clean(
                "x", '<a xlink:href="java\tscript:alert(1)">x</a>')

    def test_aborts_on_data_text_html_href(self):
        with self.assertRaises(SystemExit):
            c4_assemble.verify_clean(
                "x", '<a xlink:href="data:text/html,<b>x">y</a>')

    # --- must NOT over-abort on legitimate PlantUML output ---
    def test_passes_on_data_image_href(self):
        try:
            c4_assemble.verify_clean(
                "x", '<image xlink:href="data:image/png;base64,AAAA"/><rect/>')
        except SystemExit:
            self.fail("verify_clean aborted on a legitimate data:image icon")

    def test_passes_on_fragment_and_https_href(self):
        # #fragment refs and ordinary https links (entity-encoded `&` in the query
        # is normal) must survive the normalized scheme check.
        try:
            c4_assemble.verify_clean(
                "x", '<a xlink:href="#node1"><rect/></a>'
                     '<a href="https://example.com/x?a=1&amp;b=2">y</a>')
        except SystemExit:
            self.fail("verify_clean aborted on benign #fragment / https href")

    def test_passes_when_scheme_word_is_only_a_query_param(self):
        # 'javascript' inside a query value is not an executable scheme; the
        # anchored (start-of-value) match must not fire on it.
        try:
            c4_assemble.verify_clean(
                "x", '<a href="https://example.com/?next=javascript">y</a>')
        except SystemExit:
            self.fail("verify_clean aborted on a benign 'javascript' query value")

    def test_slash_handler_guard_ignores_prose_slash(self):
        # A `/` in <text> prose (not a start-tag attribute separator) must not
        # trip the guard — mirrors the existing online=true false-positive tests.
        try:
            c4_assemble.verify_clean("x", '<svg><text>a/b online=true</text></svg>')
        except SystemExit:
            self.fail("verify_clean aborted on benign prose containing a slash")


if __name__ == "__main__":
    unittest.main()
