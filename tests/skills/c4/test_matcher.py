import os
import sys
import unittest

import c4_assemble

# Real component-view QN (verified 2026-07-22): the container APIService appears
# as an INTERIOR segment, so a bare-name / endswith match would false-fire.
COMPONENT_QN = ("OrderPlatform_boundary.OrderPlatform.APIService_boundary."
                "OrderPlatform.APIService.AuthMiddleware")
CONTAINER_QN = "OrderPlatform_boundary.OrderPlatform.APIService"


class MatcherTest(unittest.TestCase):
    def test_container_node_matches_own_alias(self):
        self.assertTrue(c4_assemble.alias_matches_qn(CONTAINER_QN, "OrderPlatform.APIService"))

    def test_container_alias_does_not_match_interior_of_component_qn(self):
        # This is the false positive the review caught: 3 spurious matches.
        self.assertFalse(c4_assemble.alias_matches_qn(COMPONENT_QN, "OrderPlatform.APIService"))

    def test_component_alias_matches_component_qn(self):
        self.assertTrue(c4_assemble.alias_matches_qn(
            COMPONENT_QN, "OrderPlatform.APIService.AuthMiddleware"))

    def test_not_endswith_on_non_segment_boundary(self):
        # 'MegaPlatform.Service'.endswith('Platform.Service') is True — must NOT match.
        self.assertFalse(c4_assemble.alias_matches_qn("A.MegaPlatform.Service", "Platform.Service"))

    def test_not_bare_suffix(self):
        # 'X.OrderService'.endswith('Service') is True — must NOT match.
        self.assertFalse(c4_assemble.alias_matches_qn("X.OrderService", "Service"))

    def test_sibling_systems_wire_distinctly(self):
        self.assertTrue(c4_assemble.alias_matches_qn("Sys.Alpha.Service", "Alpha.Service"))
        self.assertFalse(c4_assemble.alias_matches_qn("Sys.Alpha.Service", "Beta.Service"))

    def test_empty_alias_never_matches(self):
        self.assertFalse(c4_assemble.alias_matches_qn(CONTAINER_QN, ""))


if __name__ == "__main__":
    unittest.main()
