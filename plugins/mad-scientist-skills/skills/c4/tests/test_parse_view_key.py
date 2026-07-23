import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import c4_assemble  # noqa: E402


class ParseViewKeyTest(unittest.TestCase):
    def test_system_context(self):
        self.assertEqual(c4_assemble.parse_view_key("SystemContext"), ("Context", "System Context"))

    def test_containers(self):
        self.assertEqual(c4_assemble.parse_view_key("Containers"), ("Containers", "Containers"))

    def test_combined_components(self):
        self.assertEqual(c4_assemble.parse_view_key("Components"), ("Components", "Components"))

    def test_split_component_underscore(self):
        self.assertEqual(c4_assemble.parse_view_key("Component_api"), ("Components", "api"))

    def test_split_component_hyphen(self):
        # Pre-existing workspaces may use a hyphen — must still group.
        self.assertEqual(c4_assemble.parse_view_key("Component-api"), ("Components", "api"))

    def test_dynamic(self):
        self.assertEqual(c4_assemble.parse_view_key("Dynamic_PlaceOrder"), ("Dynamic", "PlaceOrder"))

    def test_deployment(self):
        self.assertEqual(c4_assemble.parse_view_key("Deployment_Production"), ("Deployment", "Production"))

    def test_dsl(self):
        self.assertEqual(c4_assemble.parse_view_key("DSL"), ("DSL", "Structurizr DSL"))

    def test_unknown_is_own_group(self):
        self.assertEqual(c4_assemble.parse_view_key("Weird"), ("Weird", "Weird"))


if __name__ == "__main__":
    unittest.main()
