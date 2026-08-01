import os
import sys
import unittest

import c4_assemble


class ParseViewKeyTest(unittest.TestCase):
    def test_system_context(self):
        self.assertEqual(c4_assemble.parse_view_key("SystemContext"), ("Context", "System Context"))

    def test_containers(self):
        self.assertEqual(c4_assemble.parse_view_key("Containers"), ("Containers", "Containers"))

    def test_split_containers_underscore(self):
        # Structurizr view keys are unique, so a workspace with >1 software system
        # must give each container view a distinct key. They are all C4 Level 2 and
        # must land in the one Containers group, not become 8 top-level groups.
        self.assertEqual(c4_assemble.parse_view_key("Containers_api"), ("Containers", "api"))

    def test_split_containers_hyphen(self):
        self.assertEqual(c4_assemble.parse_view_key("Containers-api"), ("Containers", "api"))

    def test_split_container_singular_underscore(self):
        # The DSL keyword is `container` (singular), so authors reach for it too.
        self.assertEqual(c4_assemble.parse_view_key("Container_api"), ("Containers", "api"))

    def test_split_container_singular_hyphen(self):
        self.assertEqual(c4_assemble.parse_view_key("Container-api"), ("Containers", "api"))

    def test_container_and_containers_prefixes_are_disjoint(self):
        # 'Containers_x' must not be parsed by the 'Container' entry (which would
        # yield the sub-label 's_x'). Position 9 is '_' vs 's', so the prefixes
        # never overlap and the tuple order is free — this pins that.
        self.assertEqual(c4_assemble.parse_view_key("Containers_Taipy"), ("Containers", "Taipy"))
        self.assertEqual(c4_assemble.parse_view_key("Container_Taipy"), ("Containers", "Taipy"))

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
