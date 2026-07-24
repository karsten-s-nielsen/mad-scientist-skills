import os
import re
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import c4_assemble  # noqa: E402

FIXTURES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")


def _load(name):
    with open(os.path.join(FIXTURES, name), encoding="utf-8") as fh:
        return fh.read()


class WireDrilldownTest(unittest.TestCase):
    def setUp(self):
        self.svg = _load("containers.svg")
        self.dmap = {"OrderPlatform.APIService": "Component_api"}

    def test_view_key_to_tab_id(self):
        self.assertEqual(c4_assemble.view_key_to_tab_id("Component_api"), "component-api")
        self.assertEqual(c4_assemble.view_key_to_tab_id("SystemContext"), "systemcontext")

    def test_only_container_with_target_is_wired(self):
        out, count = c4_assemble.wire_drilldown(self.svg, self.dmap)
        self.assertEqual(count, 1)

    def test_wired_node_is_apiservice_and_has_onclick(self):
        out, _ = c4_assemble.wire_drilldown(self.svg, self.dmap)
        # Find the entity <g> for APIService and assert it got the handler.
        for m in re.finditer(r'<g [^>]*class="entity"[^>]*data-qualified-name="([^"]*)"[^>]*>', out):
            if m.group(1).endswith("OrderPlatform.APIService"):
                self.assertIn("onclick=\"c4ShowTab('component-api')\"", m.group(0))
                self.assertIn('role="button"', m.group(0))
                self.assertIn('tabindex="0"', m.group(0))
                return
        self.fail("APIService entity group not found in output")

    def test_leaf_nodes_stay_inert(self):
        out, _ = c4_assemble.wire_drilldown(self.svg, self.dmap)
        for m in re.finditer(r'<g [^>]*class="entity"[^>]*data-qualified-name="([^"]*)"[^>]*>', out):
            if m.group(1).endswith(("WebApp", "Database")) or m.group(1) == "EndUser":
                self.assertNotIn("onclick", m.group(0))

    def test_cluster_boundary_never_wired(self):
        out, _ = c4_assemble.wire_drilldown(self.svg, self.dmap)
        # The cluster group carries no onclick.
        seg = out.split('<g class="cluster"', 1)
        self.assertEqual(len(seg), 2)
        self.assertNotIn("onclick", seg[1][:300])

    def test_entity_count_preserved(self):
        out, _ = c4_assemble.wire_drilldown(self.svg, self.dmap)
        self.assertEqual(c4_assemble.count_entities(out), 4)

    def test_empty_map_wires_nothing(self):
        out, count = c4_assemble.wire_drilldown(self.svg, {})
        self.assertEqual(count, 0)
        self.assertNotIn("onclick", out)

    def test_aria_label_uses_display_name_when_provided(self):
        # With a label map, the drill affordance names the container's DSL
        # display name, not the filtered SVG alias (APIService).
        labels = {"Component_api": "API Service"}
        out, _ = c4_assemble.wire_drilldown(self.svg, self.dmap, labels=labels)
        self.assertIn('aria-label="Drill into API Service"', out)
        self.assertNotIn('aria-label="Drill into APIService"', out)

    def test_aria_label_falls_back_to_leaf_without_labels(self):
        out, _ = c4_assemble.wire_drilldown(self.svg, self.dmap)
        self.assertIn('aria-label="Drill into APIService"', out)


import tempfile


class DetectViewsTest(unittest.TestCase):
    def _make_dir(self, filenames):
        d = tempfile.mkdtemp()
        for fn in filenames:
            with open(os.path.join(d, fn), "w", encoding="utf-8") as fh:
                fh.write("<svg></svg>")
        return d

    def test_known_views_yield_four_tuples_with_raw_key(self):
        from pathlib import Path
        d = self._make_dir(["structurizr-SystemContext.svg", "structurizr-Containers.svg"])
        views = c4_assemble.detect_views(Path(d))
        self.assertEqual(views[0], ("structurizr-SystemContext.svg", "systemcontext",
                                    "System Context", "SystemContext"))
        self.assertEqual(views[1], ("structurizr-Containers.svg", "containers",
                                    "Containers", "Containers"))

    def test_split_component_gets_clean_label_not_underscore(self):
        from pathlib import Path
        d = self._make_dir(["structurizr-Component_api.svg"])
        views = c4_assemble.detect_views(Path(d))
        # Old bug produced label "Component_api"; now it's the clean suffix "api".
        self.assertEqual(views[0], ("structurizr-Component_api.svg", "component-api",
                                    "api", "Component_api"))

    def test_parse_view_spec_four_tuple(self):
        fn, tab_id, label, raw = c4_assemble.parse_view_spec(
            "SystemContext:System Context:structurizr-SystemContext.svg")
        self.assertEqual((fn, tab_id, label, raw),
                         ("structurizr-SystemContext.svg", "systemcontext",
                          "System Context", "SystemContext"))


class BuildHtmlTest(unittest.TestCase):
    def _views(self, extra=None):
        v = [
            ("f1.svg", "systemcontext", "System Context", "SystemContext"),
            ("f2.svg", "containers", "Containers", "Containers"),
            ("f3.svg", "component-api", "api", "Component_api"),
        ]
        if extra:
            v.extend(extra)
        return v

    def _svgs(self, views):
        return {tab_id: "<svg>%s</svg>" % tab_id for (_, tab_id, _, _) in views}

    def test_every_showtab_ref_resolves_to_a_panel(self):
        views = self._views()
        html = c4_assemble.build_html(views, self._svgs(views), "dsl", "Sys")
        panels = set(re.findall(r'id="([^"]+)" class="tab-content', html))
        refs = set(re.findall(r"c4ShowTab\('([^']+)'\)", html))
        self.assertTrue(refs, "expected some c4ShowTab refs")
        self.assertTrue(refs <= panels, "dangling tab refs: %s" % (refs - panels))

    def test_system_name_is_escaped(self):
        views = self._views()
        html = c4_assemble.build_html(views, self._svgs(views), "dsl", "Order & <Platform>")
        self.assertIn("Order &amp; &lt;Platform&gt;", html)
        self.assertNotIn("Order & <Platform>", html)

    def test_single_view_groups_emit_no_subtabs(self):
        views = self._views()  # each group has exactly one view
        html = c4_assemble.build_html(views, self._svgs(views), "dsl", "Sys")
        self.assertEqual(len(re.findall(r'class="subtab', html)), 0)

    def test_multi_view_group_emits_subtabs(self):
        views = self._views([("f4.svg", "component-web", "web", "Component_web")])
        html = c4_assemble.build_html(views, self._svgs(views), "dsl", "Sys")
        self.assertEqual(len(re.findall(r'class="subtab', html)), 2)
        sub = html.split('data-subrow="Components"', 1)[1].split("</div>", 1)[0]
        self.assertIn("c4ShowTab('component-api')", sub)
        self.assertIn("c4ShowTab('component-web')", sub)

    def test_component_panel_has_full_breadcrumb(self):
        views = self._views()
        html = c4_assemble.build_html(views, self._svgs(views), "dsl", "Sys")
        panel = html.split('id="component-api"', 1)[1].split("</nav>", 1)[0]
        self.assertIn("c4ShowTab('systemcontext')", panel)
        self.assertIn("c4ShowTab('containers')", panel)

    def test_subtab_and_breadcrumb_use_display_name_label(self):
        # When a label map gives the container's real name, the Components
        # subtab and the breadcrumb current-page should read "API Service",
        # not the view-key suffix "api".
        views = self._views([("f4.svg", "component-web", "web", "Component_web")])
        labels = {"Component_api": "API Service", "Component_web": "Web App"}
        html = c4_assemble.build_html(
            views, self._svgs(views), "dsl", "Sys", view_labels=labels)
        sub = html.split('data-subrow="Components"', 1)[1].split("</div>", 1)[0]
        self.assertIn(">API Service<", sub)
        self.assertIn(">Web App<", sub)
        self.assertNotIn(">api<", sub)
        # breadcrumb current page (aria-current) on the component-api panel
        panel = html.split('id="component-api"', 1)[1].split("</nav>", 1)[0]
        self.assertIn('aria-current="page">API Service<', panel)

    def test_labels_default_to_view_key_suffix_when_absent(self):
        # No label map -> preserve prior behavior (suffix "api").
        views = self._views([("f4.svg", "component-web", "web", "Component_web")])
        html = c4_assemble.build_html(views, self._svgs(views), "dsl", "Sys")
        sub = html.split('data-subrow="Components"', 1)[1].split("</div>", 1)[0]
        self.assertIn(">api<", sub)
        self.assertIn(">web<", sub)

    def test_affordance_style_present_for_clickable_boxes(self):
        # A persistent (non-hover) visual cue must exist for drillable nodes.
        views = self._views()
        html = c4_assemble.build_html(views, self._svgs(views), "dsl", "Sys")
        self.assertIn('.svg-container [role="button"]', html)
        # cue must apply outside :hover / :focus (a bare selector rule exists)
        self.assertRegex(
            html, r'\.svg-container \[role="button"\]\s*\{[^}]*\}')

    def test_breadcrumb_skips_missing_ancestor(self):
        # Component view present but no Containers view.
        views = [
            ("f1.svg", "systemcontext", "System Context", "SystemContext"),
            ("f3.svg", "component-api", "api", "Component_api"),
        ]
        html = c4_assemble.build_html(views, self._svgs(views), "dsl", "Sys")
        panel = html.split('id="component-api"', 1)[1].split("</nav>", 1)[0]
        self.assertIn("c4ShowTab('systemcontext')", panel)
        self.assertNotIn("c4ShowTab('containers')", panel)

    def test_element_name_in_svg_is_not_reinterpreted(self):
        # A name with < & ' " embedded in the SVG must survive; build_html must
        # not double-process it (it embeds svgs verbatim — escaping is on labels).
        views = self._views()
        svgs = self._svgs(views)
        svgs["containers"] = '<svg><text>Tom &amp; Jerry</text></svg>'
        html = c4_assemble.build_html(views, svgs, "dsl", "Sys")
        self.assertIn("<text>Tom &amp; Jerry</text>", html)

    def test_dsl_panel_present(self):
        views = self._views()
        html = c4_assemble.build_html(views, self._svgs(views), "ESCAPED_DSL", "Sys")
        self.assertIn('id="dsl-source"', html)
        self.assertIn("ESCAPED_DSL", html)


class ScriptEmbeddingEscapeTest(unittest.TestCase):
    """FINDING 4: the tab->group / group->tabs JSON maps are embedded inside a
    <script> block; a view key containing </script> must not break the block."""

    def test_json_maps_do_not_break_script_block(self):
        # An unknown view key becomes its own group name (parse_view_key), which
        # is embedded verbatim into the JSON maps inside <script>.
        views = [
            ("f1.svg", "systemcontext", "System Context", "SystemContext"),
            ("f2.svg", "evilgroup", "x", "</script><img src=x onerror=alert(1)>"),
        ]
        svgs = {"systemcontext": "<svg/>", "evilgroup": "<svg/>"}
        html = c4_assemble.build_html(views, svgs, "dsl", "Sys")
        # The raw closing tag must never appear literally (would end the block).
        self.assertNotIn("</script><img", html)
        # It survives hex-escaped inside the JSON instead.
        self.assertIn("\\u003c/script\\u003e", html)


class TabIdInjectionTest(unittest.TestCase):
    """FINDING 5: tab ids are interpolated into id=, data-tab= and onclick=
    contexts unescaped, so view_key_to_tab_id (the single source of truth) must
    slugify away anything that could break out of those contexts."""

    def test_view_key_to_tab_id_keeps_known_keys_stable(self):
        # Regression guard for the existing contract.
        self.assertEqual(c4_assemble.view_key_to_tab_id("Component_api"), "component-api")
        self.assertEqual(c4_assemble.view_key_to_tab_id("SystemContext"), "systemcontext")
        self.assertEqual(
            c4_assemble.view_key_to_tab_id("Deployment_local_dev"), "deployment-local-dev")

    def test_view_key_to_tab_id_slugifies_unsafe_chars(self):
        tid = c4_assemble.view_key_to_tab_id("Component_api');alert(1)//")
        self.assertRegex(tid, r"^[a-z0-9-]*$")
        for bad in ("'", '"', "<", ">", "(", ")", ";", " ", "/"):
            self.assertNotIn(bad, tid)

    def test_dangerous_view_key_cannot_break_out_through_pipeline(self):
        raw = "Component_api\"'/><script>alert(1)</script>"
        tid = c4_assemble.view_key_to_tab_id(raw)
        views = [("f.svg", tid, "api", raw)]
        html = c4_assemble.build_html(views, {tid: "<svg/>"}, "dsl", "Sys")
        # No attribute/JS breakout from the slugified id.
        self.assertNotIn("<script>alert(1)</script>", html)
        self.assertNotIn('onerror', html)
        self.assertRegex(tid, r"^[a-z0-9-]*$")


class GroupNameInjectionTest(unittest.TestCase):
    """An unknown view key becomes its own GROUP name (parse_view_key fallback),
    which flows into onclick="c4ShowGroup('<g>')". html-escaping does NOT protect
    a JS-string-in-attribute context (the browser HTML-decodes &#x27; -> ' before
    the JS parser runs), so the group onclick arg must be JS-\\uXXXX-escaped."""

    def test_group_onclick_survives_html_decode(self):
        import html as H
        evil = "x');alert(1)//"
        views = [
            ("f1.svg", "systemcontext", "System Context", "SystemContext"),
            ("f2.svg", c4_assemble.view_key_to_tab_id(evil), "x", evil),
        ]
        svgs = {tab_id: "<svg/>" for (_, tab_id, _, _) in views}
        html = c4_assemble.build_html(views, svgs, "dsl", "Sys")
        # Grab the evil group button's onclick attribute value.
        attrs = [a for a in re.findall(r'onclick="(c4ShowGroup\([^"]*\))"', html)
                 if "alert" in a]
        self.assertTrue(attrs, "evil group button not found")
        # What the JS engine actually parses is the HTML-DECODED attribute.
        js_sees = H.unescape(attrs[0])
        # A raw single-quote that closes the string literal is the breakout.
        self.assertNotIn("');alert", js_sees)

    def test_known_group_onclick_unchanged(self):
        # Safe group names must render verbatim (no churn to real diagrams).
        views = [
            ("f1.svg", "systemcontext", "System Context", "SystemContext"),
            ("f2.svg", "containers", "Containers", "Containers"),
            ("f3.svg", "component-api", "api", "Component_api"),
        ]
        svgs = {tab_id: "<svg/>" for (_, tab_id, _, _) in views}
        html = c4_assemble.build_html(views, svgs, "dsl", "Sys")
        self.assertIn("c4ShowGroup('Context')", html)
        self.assertIn("c4ShowGroup('Components')", html)
        self.assertIn('data-group="Components"', html)  # attr unchanged


class TabIdCollisionTest(unittest.TestCase):
    """FINDING 6: view_key_to_tab_id is non-injective; two distinct view keys
    that collapse to one id would emit duplicate DOM ids (a hidden panel)."""

    def test_collision_detected(self):
        views = [
            ("a.svg", "component-api", "api", "Component_api"),
            ("b.svg", "component-api", "api2", "Component-api"),  # collides
            ("c.svg", "containers", "Containers", "Containers"),
        ]
        dupes = c4_assemble.find_tab_id_collisions(views)
        self.assertIn("component-api", dupes)
        self.assertEqual(sorted(dupes["component-api"]), ["Component-api", "Component_api"])
        self.assertNotIn("containers", dupes)

    def test_no_collision_returns_empty(self):
        views = [
            ("a.svg", "systemcontext", "x", "SystemContext"),
            ("b.svg", "containers", "y", "Containers"),
        ]
        self.assertEqual(c4_assemble.find_tab_id_collisions(views), {})


class EmptySlugTabIdTest(unittest.TestCase):
    """A view key with no ASCII alphanumerics slugifies to '' (or an all-hyphen
    string): build_html then emits id="" / id="---", getElementById returns null,
    and the panel + group button are dead. find_tab_id_collisions only fires at
    2+ keys per id, so a lone degenerate slug is NOT surfaced. view_key_to_tab_id
    must fall back to a stable, non-empty, collision-free id."""

    def test_non_ascii_key_gets_nonempty_id(self):
        tid = c4_assemble.view_key_to_tab_id("日本語")  # Japanese
        self.assertTrue(tid, "id must not be empty")
        self.assertRegex(tid, r"[a-z0-9]")        # has a real alphanumeric
        self.assertRegex(tid, r"^[a-z0-9-]+$")    # still a safe slug

    def test_punctuation_only_key_gets_nonempty_id(self):
        self.assertRegex(c4_assemble.view_key_to_tab_id("!!!"), r"[a-z0-9]")

    def test_all_underscore_key_not_degenerate(self):
        # '___' -> '---' pre-fix: a slug with no alphanumerics is degenerate too.
        self.assertRegex(c4_assemble.view_key_to_tab_id("___"), r"[a-z0-9]")

    def test_fallback_is_deterministic(self):
        self.assertEqual(
            c4_assemble.view_key_to_tab_id("日本語"),
            c4_assemble.view_key_to_tab_id("日本語"))

    def test_distinct_degenerate_keys_stay_distinct(self):
        # Two different all-non-ASCII keys must not collapse to one dead id.
        self.assertNotEqual(
            c4_assemble.view_key_to_tab_id("日本語"),
            c4_assemble.view_key_to_tab_id("中文"))

    def test_known_keys_unaffected(self):
        # Regression guard: real keys must not churn.
        self.assertEqual(c4_assemble.view_key_to_tab_id("Component_api"), "component-api")
        self.assertEqual(c4_assemble.view_key_to_tab_id("SystemContext"), "systemcontext")
        self.assertEqual(
            c4_assemble.view_key_to_tab_id("Deployment_local_dev"), "deployment-local-dev")

    def test_degenerate_key_panel_is_reachable_in_html(self):
        # End-to-end: the emitted panel id must be a non-empty selector.
        raw = "日本語"
        tid = c4_assemble.view_key_to_tab_id(raw)
        views = [("f.svg", tid, "x", raw)]
        html = c4_assemble.build_html(views, {tid: "<svg/>"}, "dsl", "Sys")
        self.assertNotIn('id=""', html)
        self.assertIn('id="%s"' % tid, html)


class DslReservedTabIdTest(unittest.TestCase):
    """The synthetic Structurizr-DSL panel always claims tab id 'dsl'. A user
    view whose key slugifies to 'dsl' collides with it, hiding the DSL source
    panel. Because build_html appends the synthetic entry AFTER main() runs
    find_tab_id_collisions, the clash is invisible unless the collision check is
    run over the full set including the reserved DSL view."""

    def test_dsl_view_constant_exists_with_reserved_id(self):
        # Single source of truth for the synthetic panel (filename, id, label, key).
        self.assertEqual(c4_assemble._DSL_VIEW[1], "dsl")
        self.assertEqual(c4_assemble._DSL_VIEW[3], "DSL")

    def test_user_view_colliding_with_dsl_is_detected(self):
        # "Dsl" slugifies to 'dsl' -> collides with the reserved synthetic panel.
        colliding_id = c4_assemble.view_key_to_tab_id("Dsl")
        self.assertEqual(colliding_id, "dsl")
        views = [
            ("a.svg", "systemcontext", "x", "SystemContext"),
            ("b.svg", colliding_id, "d", "Dsl"),
        ]
        dupes = c4_assemble.find_tab_id_collisions(views + [c4_assemble._DSL_VIEW])
        self.assertIn("dsl", dupes)
        self.assertEqual(sorted(dupes["dsl"]), ["DSL", "Dsl"])

    def test_no_false_collision_without_a_dsl_clash(self):
        views = [
            ("a.svg", "systemcontext", "x", "SystemContext"),
            ("b.svg", "containers", "y", "Containers"),
        ]
        self.assertEqual(
            c4_assemble.find_tab_id_collisions(views + [c4_assemble._DSL_VIEW]), {})

    def test_exact_dsl_raw_key_collision_is_detected(self):
        # A user view keyed EXACTLY 'DSL' shares both tab id 'dsl' AND raw_key
        # 'DSL' with _DSL_VIEW. find_tab_id_collisions set-dedups on raw_key, so
        # the identical-key clash collapses to len==1 and is missed — yet
        # build_html emits two id="dsl" panels (and treats the user view as the
        # DSL source panel, dropping its SVG). The reserved-id shadow must be
        # surfaced regardless of raw_key equality.
        views = [
            ("a.svg", "systemcontext", "x", "SystemContext"),
            ("b.svg", "dsl", "d", "DSL"),  # exact reserved-key clash
        ]
        shadow = c4_assemble.find_reserved_id_shadow(views)
        self.assertIn("dsl", shadow)

    def test_no_reserved_shadow_for_ordinary_views(self):
        views = [
            ("a.svg", "systemcontext", "x", "SystemContext"),
            ("b.svg", "containers", "y", "Containers"),
        ]
        self.assertEqual(c4_assemble.find_reserved_id_shadow(views), {})

    def test_reserved_shadow_catches_slugified_dsl_clash(self):
        # A key that slugifies to 'dsl' but ISN'T raw 'DSL' (e.g. 'Dsl') must
        # also be flagged as shadowing the reserved panel.
        views = [("b.svg", c4_assemble.view_key_to_tab_id("Dsl"), "d", "Dsl")]
        self.assertIn("dsl", c4_assemble.find_reserved_id_shadow(views))


class TabIdCollisionConsequenceTest(unittest.TestCase):
    """Documents the consequence find_tab_id_collisions warns about: two views
    sharing a tab id emit a duplicate DOM id, so the second panel is unreachable
    via getElementById (which returns the first match)."""

    def test_colliding_views_emit_duplicate_dom_id(self):
        views = [
            ("a.svg", "component-api", "api", "Component_api"),
            ("b.svg", "component-api", "api2", "Component-api"),  # same slug
        ]
        svgs = {"component-api": "<svg><rect/></svg>"}
        html = c4_assemble.build_html(views, svgs, "dsl", "Sys")
        # Both panels carry id="component-api" -> the second is shadowed.
        self.assertEqual(html.count('id="component-api"'), 2)


if __name__ == "__main__":
    unittest.main()
