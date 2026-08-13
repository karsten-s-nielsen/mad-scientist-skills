"""Final-page verification of the embedded SVGs.

`verify_clean` guards each SVG as it leaves PlantUML, but two stages run after it
(`wire_drilldown` injects handlers, `hoist_text_styles` rewrites start tags) and
`verify_clean` cannot be re-run on the result — it rejects `on*=` handlers by
design and wiring adds them deliberately. This sweep closes that gap by checking
the SVGs in the exact form they ship, allowing precisely the handlers this
pipeline injects.

It replaced a check that scanned the whole page for two patterns and subtracted
their html-escaped count from their raw count. Raw and escaped forms are disjoint
strings, so that subtraction never removed a false positive — it only masked one
real violation per escaped mention in the DSL panel. That masking is pinned below.
"""

import unittest

import c4_assemble


def page_with(svg_inner):
    """A page shaped like the real output: chrome with its own <title> and
    <script>, plus one embedded SVG."""
    return ('<html><head><title>Sys &mdash; C4</title><style>.c4t0{fill:#FFF}</style>'
            "</head><body><script>function c4ShowTab(){}</script>"
            '<div class="svg-container"><svg xmlns="http://www.w3.org/2000/svg">'
            "%s</svg></div></body></html>" % svg_inner)


class ChromeIsNotFlaggedTest(unittest.TestCase):
    """The page's own head <title> and inline <script> runtime are legitimate.
    A whole-page scan for those would be permanently red, so the sweep is scoped
    to the <svg> regions."""

    def test_clean_page_passes(self):
        n = c4_assemble.verify_embedded_svgs(page_with('<g class="entity"><rect/></g>'))
        self.assertEqual(n, 1)

    def test_counts_every_svg_block(self):
        page = page_with("<rect/>").replace(
            "</body>", '<svg><circle r="1"/></svg></body>')
        self.assertEqual(c4_assemble.verify_embedded_svgs(page), 2)


class ForbiddenContentInEmbeddedSvgTest(unittest.TestCase):
    def _assert_aborts(self, svg_inner):
        with self.assertRaises(SystemExit):
            c4_assemble.verify_embedded_svgs(page_with(svg_inner))

    def test_title_group_inside_svg_aborts(self):
        self._assert_aborts('<g class="title"><text>T</text></g>')

    def test_title_element_inside_svg_aborts(self):
        self._assert_aborts("<title>encoded</title><rect/>")

    def test_processing_instruction_inside_svg_aborts(self):
        self._assert_aborts('<?plantuml version="1"?><rect/>')

    def test_script_inside_svg_aborts(self):
        self._assert_aborts("<script>alert(1)</script>")

    def test_foreign_object_inside_svg_aborts(self):
        self._assert_aborts("<foreignObject><iframe/></foreignObject>")

    def test_javascript_href_inside_svg_aborts(self):
        self._assert_aborts('<a xlink:href="javascript:alert(1)"><rect/></a>')

    def test_entity_obfuscated_href_inside_svg_aborts(self):
        # Normalized the way a browser resolves a scheme, so entity obfuscation
        # cannot smuggle one past a raw-substring scan.
        self._assert_aborts('<a xlink:href="jav&#x61;script:alert(1)"><rect/></a>')

    def test_benign_data_image_href_passes(self):
        c4_assemble.verify_embedded_svgs(
            page_with('<image xlink:href="data:image/png;base64,iVBOR"/>'))

    def test_fragment_href_passes(self):
        c4_assemble.verify_embedded_svgs(page_with('<a xlink:href="#anchor"><rect/></a>'))


class EventHandlerAllowlistTest(unittest.TestCase):
    """Only the drill-down handlers this tool injects may survive to the page."""

    def test_wired_drilldown_output_passes(self):
        # The load-bearing case: if the allowlist were wrong, every build with
        # drill-down would abort. Uses the real wire_drilldown output, not a
        # hand-written imitation of it.
        svg = ('<svg xmlns="http://www.w3.org/2000/svg">'
               '<g class="entity" data-qualified-name="Sys.Api"><rect/></g></svg>')
        wired, n = c4_assemble.wire_drilldown(svg, {"Sys.Api": "Component_api"})
        self.assertEqual(n, 1)
        self.assertEqual(c4_assemble.verify_embedded_svgs("<body>%s</body>" % wired), 1)

    def test_wired_then_hoisted_output_passes(self):
        # Full post-verify_clean pipeline order: wire, then hoist, then verify.
        svg = ('<svg xmlns="http://www.w3.org/2000/svg">'
               '<g class="entity" data-qualified-name="Sys.Api">'
               '<text fill="#FFF" font-family="sans-serif" font-size="14">A</text>'
               "</g></svg>")
        wired, _n = c4_assemble.wire_drilldown(svg, {"Sys.Api": "Component_api"})
        hoisted, css = c4_assemble.hoist_text_styles({"a": wired})
        self.assertTrue(css)
        self.assertEqual(c4_assemble.verify_embedded_svgs(hoisted["a"]), 1)

    def test_foreign_onload_aborts(self):
        with self.assertRaises(SystemExit):
            c4_assemble.verify_embedded_svgs(page_with('<rect onload="steal()"/>'))

    def test_onclick_with_foreign_payload_aborts(self):
        # Right handler name, wrong function — the allowlist matches on the value
        # prefix, not merely on the attribute name.
        with self.assertRaises(SystemExit):
            c4_assemble.verify_embedded_svgs(page_with('<rect onclick="steal()"/>'))

    def test_unquoted_handler_aborts(self):
        # An unquoted handler cannot be read by the value parser, so it is a
        # violation in itself rather than something to skip over.
        with self.assertRaises(SystemExit):
            c4_assemble.verify_embedded_svgs(page_with("<rect onclick=steal()/>"))

    def test_slash_separated_handler_aborts(self):
        # HTML accepts `/` as an attribute separator, so <svg/onload=...> runs on
        # parse; a whitespace-only guard would let it through.
        with self.assertRaises(SystemExit):
            c4_assemble.verify_embedded_svgs(page_with('<rect/onload="steal()"/>'))


class EscapedMentionNoLongerMasksViolationTest(unittest.TestCase):
    """Regression pin for the arithmetic this check replaced.

    The old check computed `page.count(raw) - page.count(escaped)`. The two forms
    are disjoint, so each harmless escaped mention in the DSL panel cancelled one
    genuine unescaped violation in an embedded SVG."""

    def test_escaped_dsl_mention_does_not_hide_a_real_title_group(self):
        import html as html_mod
        raw = 'class="title"'
        page = ("<pre><code>%s</code></pre>" % html_mod.escape(raw)) + page_with(
            '<g %s><text>T</text></g>' % raw)
        # Old arithmetic scored this as clean; the sweep must abort.
        self.assertEqual(page.count(raw) - page.count(html_mod.escape(raw)), 0)
        with self.assertRaises(SystemExit):
            c4_assemble.verify_embedded_svgs(page)

    def test_escaped_dsl_mention_alone_still_passes(self):
        import html as html_mod
        page = ("<pre><code>%s</code></pre>" % html_mod.escape('class="title"')
                + page_with("<rect/>"))
        self.assertEqual(c4_assemble.verify_embedded_svgs(page), 1)


if __name__ == "__main__":
    unittest.main()
