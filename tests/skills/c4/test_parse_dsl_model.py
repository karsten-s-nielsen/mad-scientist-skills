import os
import sys
import unittest

import c4_assemble  # noqa: E402

FIXTURES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")


def _load(name):
    with open(os.path.join(FIXTURES, name), encoding="utf-8") as fh:
        return fh.read()


# Inline fixtures for edge cases (kept in-test so they're readable next to the assertion).
GROUP_DSL = '''workspace "G" {
    model {
        sys = softwareSystem "Sys" {
            group "Backend" {
                api = container "API Service" "desc" "tech"
            }
        }
    }
    views {
        container sys "Containers" { include * }
    }
}'''

BRACE_IN_STRING_DSL = '''workspace "B" {
    model {
        sys = softwareSystem "Sys" "A description with a { brace } inside" {
            api = container "API" "another { brace }" "tech"
        }
    }
    views {
        container sys "Containers" { include * }
    }
}'''


class ParseDslModelTest(unittest.TestCase):
    def setUp(self):
        self.elements, self.views = c4_assemble.parse_dsl_model(_load("sample.dsl"))
        self.by_id = {e.identifier: e for e in self.elements}

    def test_finds_all_named_elements(self):
        self.assertIn("web", self.by_id)
        self.assertIn("api", self.by_id)
        self.assertIn("authMw", self.by_id)
        self.assertEqual(self.by_id["api"].name, "API Service")

    def test_parent_chain(self):
        self.assertEqual(self.by_id["api"].parent, "system")
        self.assertEqual(self.by_id["authMw"].parent, "api")
        self.assertIsNone(self.by_id["user"].parent)

    def test_kinds(self):
        self.assertEqual(self.by_id["user"].kind, "person")
        self.assertEqual(self.by_id["system"].kind, "softwareSystem")
        self.assertEqual(self.by_id["web"].kind, "container")
        self.assertEqual(self.by_id["authMw"].kind, "component")

    def test_views(self):
        keys = {v.key for v in self.views}
        self.assertEqual(keys, {"SystemContext", "Containers", "Component_api"})
        comp = next(v for v in self.views if v.key == "Component_api")
        self.assertEqual(comp.view_type, "component")
        self.assertEqual(comp.scope_identifier, "api")

    def test_dsl_alias_for_walks_parents(self):
        self.assertEqual(
            c4_assemble.dsl_alias_for("authMw", self.elements),
            "OrderPlatform.APIService.AuthMiddleware",
        )
        self.assertEqual(
            c4_assemble.dsl_alias_for("api", self.elements),
            "OrderPlatform.APIService",
        )

    def test_group_is_transparent_scope(self):
        elements, _ = c4_assemble.parse_dsl_model(GROUP_DSL)
        by_id = {e.identifier: e for e in elements}
        # The group does not become the parent; the softwareSystem does.
        self.assertEqual(by_id["api"].parent, "sys")
        self.assertEqual(
            c4_assemble.dsl_alias_for("api", elements), "Sys.APIService")

    def test_brace_inside_quoted_string_does_not_break_nesting(self):
        elements, _ = c4_assemble.parse_dsl_model(BRACE_IN_STRING_DSL)
        by_id = {e.identifier: e for e in elements}
        self.assertEqual(by_id["api"].parent, "sys")

    def test_keyless_component_view_is_recorded_with_scope(self):
        # A component view key is OPTIONAL in Structurizr DSL. The old parser
        # dropped keyless views entirely (`if key is not None`), so scope-based
        # consumers (orphan lint, drill-down) never saw them. A keyless component
        # view must still be recorded, anchored by its scope_identifier.
        dsl = '''workspace "K" {
    model {
        sys = softwareSystem "Sys" {
            api = container "API" "d" "t" { c = component "C" "d" "t" }
        }
    }
    views {
        component api {
            include *
        }
    }
}'''
        _elements, views = c4_assemble.parse_dsl_model(dsl)
        comp = [v for v in views if v.view_type == "component"]
        self.assertEqual(len(comp), 1, "keyless component view must be recorded")
        self.assertEqual(comp[0].scope_identifier, "api")

    def test_keyed_component_view_still_records_its_key(self):
        # Regression: an explicit key must survive unchanged.
        comp = next(v for v in self.views if v.view_type == "component")
        self.assertEqual(comp.key, "Component_api")


if __name__ == "__main__":
    unittest.main()
