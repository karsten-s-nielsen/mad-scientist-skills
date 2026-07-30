import os
import sys
import unittest

import c4_assemble  # noqa: E402

FIXTURES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")


def _load(name):
    with open(os.path.join(FIXTURES, name), encoding="utf-8") as fh:
        return fh.read()


COLLISION_DSL = '''workspace "C" {
    model {
        sys = softwareSystem "Sys" {
            a = container "Web App" "d" "t"
            b = container "WebApp" "d" "t"
        }
    }
    views {
        component a "Component_a" { include * }
        component b "Component_b" { include * }
    }
}'''

CJK_DSL = '''workspace "U" {
    model {
        sys = softwareSystem "Sys" {
            n1 = container "北京 Node" "d" "t"
        }
    }
    views {
        component n1 "Component_n1" { include * }
    }
}'''


class BuildDrilldownMapTest(unittest.TestCase):
    def test_container_with_component_view_is_wired(self):
        elements, views = c4_assemble.parse_dsl_model(_load("sample.dsl"))
        dmap = c4_assemble.build_drilldown_map(elements, views)
        self.assertEqual(dmap.get("OrderPlatform.APIService"), "Component_api")

    def test_leaf_container_without_component_view_not_wired(self):
        elements, views = c4_assemble.parse_dsl_model(_load("sample.dsl"))
        dmap = c4_assemble.build_drilldown_map(elements, views)
        self.assertNotIn("OrderPlatform.WebApp", dmap)  # no Component view for web

    def test_alias_collision_neither_wired(self):
        elements, views = c4_assemble.parse_dsl_model(COLLISION_DSL)
        dmap = c4_assemble.build_drilldown_map(elements, views)
        # "Web App" and "WebApp" both filter to Sys.WebApp -> neither wired.
        self.assertEqual(dmap, {})

    def test_non_ascii_scope_left_inert(self):
        elements, views = c4_assemble.parse_dsl_model(CJK_DSL)
        dmap = c4_assemble.build_drilldown_map(elements, views)
        self.assertEqual(dmap, {})

    def test_breadcrumbs_component_full_chain(self):
        keys = ["SystemContext", "Containers", "Component_api"]
        self.assertEqual(
            c4_assemble.build_breadcrumbs("Component_api", keys),
            [("SystemContext", "Context"), ("Containers", "Containers")],
        )

    def test_breadcrumbs_containers(self):
        keys = ["SystemContext", "Containers", "Component_api"]
        self.assertEqual(
            c4_assemble.build_breadcrumbs("Containers", keys),
            [("SystemContext", "Context")],
        )

    def test_breadcrumbs_skip_missing_ancestor(self):
        # A component view but no Containers view -> Containers crumb is skipped.
        keys = ["SystemContext", "Component_api"]
        self.assertEqual(
            c4_assemble.build_breadcrumbs("Component_api", keys),
            [("SystemContext", "Context")],
        )

    def test_breadcrumbs_context_is_empty(self):
        keys = ["SystemContext", "Containers", "Component_api"]
        self.assertEqual(c4_assemble.build_breadcrumbs("SystemContext", keys), [])

    def test_rendered_keys_none_keeps_all(self):
        # Default (no filter) preserves prior behavior: Component_api wired.
        elements, views = c4_assemble.parse_dsl_model(_load("sample.dsl"))
        dmap = c4_assemble.build_drilldown_map(elements, views)
        self.assertEqual(dmap.get("OrderPlatform.APIService"), "Component_api")

    def test_unrendered_component_view_is_not_wired(self):
        # FINDING 1: the DSL declares Component_api, but only SystemContext +
        # Containers actually rendered. The container must NOT be wired to a
        # panel that build_html will never create (no dangling c4ShowTab target).
        elements, views = c4_assemble.parse_dsl_model(_load("sample.dsl"))
        dmap = c4_assemble.build_drilldown_map(
            elements, views, rendered_keys={"SystemContext", "Containers"})
        self.assertEqual(dmap, {})

    def test_rendered_component_view_is_still_wired(self):
        elements, views = c4_assemble.parse_dsl_model(_load("sample.dsl"))
        dmap = c4_assemble.build_drilldown_map(
            elements, views,
            rendered_keys={"SystemContext", "Containers", "Component_api"})
        self.assertEqual(dmap.get("OrderPlatform.APIService"), "Component_api")

    def test_build_view_labels_maps_component_view_to_container_name(self):
        # The drill target / subtab / breadcrumb should read the container's DSL
        # display name ("API Service"), not the view-key suffix ("api").
        elements, views = c4_assemble.parse_dsl_model(_load("sample.dsl"))
        labels = c4_assemble.build_view_labels(elements, views)
        self.assertEqual(labels.get("Component_api"), "API Service")

    def test_build_view_labels_ignores_non_component_views(self):
        elements, views = c4_assemble.parse_dsl_model(_load("sample.dsl"))
        labels = c4_assemble.build_view_labels(elements, views)
        self.assertNotIn("SystemContext", labels)
        self.assertNotIn("Containers", labels)


if __name__ == "__main__":
    unittest.main()
