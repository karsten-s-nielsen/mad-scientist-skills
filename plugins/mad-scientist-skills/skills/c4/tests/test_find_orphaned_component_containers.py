import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import c4_assemble  # noqa: E402

FIXTURES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")


def _load(name):
    with open(os.path.join(FIXTURES, name), encoding="utf-8") as fh:
        return fh.read()


# api has 3 components AND a `component api "Component_api"` view -> covered.
# svc has 2 components and NO component view -> orphaned.
ORPHAN_DSL = '''workspace "C" {
    model {
        sys = softwareSystem "Sys" {
            api = container "API Service" "d" "t" {
                c1 = component "Ctrl" "d" "t"
                c2 = component "Svc" "d" "t"
            }
            svc = container "Scheduled Tasks" "d" "t" {
                t1 = component "PurgeTask" "d" "t"
                t2 = component "IndexTask" "d" "t"
            }
            db = container "Database" "d" "PostgreSQL" "Database"
        }
    }
    views {
        systemContext sys "SystemContext" { include * }
        container sys "Containers" { include * }
        component api "Component_api" { include * }
    }
}'''


class FindOrphanedComponentContainersTest(unittest.TestCase):
    def test_sample_fixture_has_no_orphans(self):
        # sample.dsl: api is the only decomposed container and it HAS Component_api.
        elements, views = c4_assemble.parse_dsl_model(_load("sample.dsl"))
        self.assertEqual(
            c4_assemble.find_orphaned_component_containers(elements, views), [])

    def test_decomposed_container_without_view_is_flagged(self):
        elements, views = c4_assemble.parse_dsl_model(ORPHAN_DSL)
        orphans = c4_assemble.find_orphaned_component_containers(elements, views)
        self.assertEqual(orphans, [("svc", "Scheduled Tasks", 2)])

    def test_covered_container_not_flagged(self):
        elements, views = c4_assemble.parse_dsl_model(ORPHAN_DSL)
        orphans = c4_assemble.find_orphaned_component_containers(elements, views)
        self.assertNotIn("api", [cid for cid, _, _ in orphans])

    def test_container_without_components_not_flagged(self):
        # db has zero components -> never an orphan (nothing to surface).
        elements, views = c4_assemble.parse_dsl_model(ORPHAN_DSL)
        orphans = c4_assemble.find_orphaned_component_containers(elements, views)
        self.assertNotIn("db", [cid for cid, _, _ in orphans])

    def test_multiple_orphans_sorted_by_identifier(self):
        dsl = '''workspace "C" {
    model {
        sys = softwareSystem "Sys" {
            zeta = container "Zeta" "d" "t" { z1 = component "Z" "d" "t" }
            alpha = container "Alpha" "d" "t" { a1 = component "A" "d" "t" }
        }
    }
    views {
        container sys "Containers" { include * }
    }
}'''
        elements, views = c4_assemble.parse_dsl_model(dsl)
        orphans = c4_assemble.find_orphaned_component_containers(elements, views)
        self.assertEqual([cid for cid, _, _ in orphans], ["alpha", "zeta"])

    def test_combined_components_view_covers_its_scope(self):
        # A single combined `component <c> "Components"` view still counts as coverage.
        dsl = '''workspace "C" {
    model {
        sys = softwareSystem "Sys" {
            iris = container "IRIS" "d" "t" { p1 = component "P" "d" "t" }
        }
    }
    views {
        component iris "Components" { include * }
    }
}'''
        elements, views = c4_assemble.parse_dsl_model(dsl)
        self.assertEqual(
            c4_assemble.find_orphaned_component_containers(elements, views), [])

    def test_keyless_component_view_still_covers_its_scope(self):
        # Structurizr treats the view key as OPTIONAL. A keyless component view
        # (the exporter auto-generates the key) must still count as coverage, or
        # the container is falsely flagged as orphaned. scope_identifier is the
        # anchor here, not the (absent) key.
        dsl = '''workspace "C" {
    model {
        sys = softwareSystem "Sys" {
            api = container "API Service" "d" "t" {
                c1 = component "Ctrl" "d" "t"
            }
        }
    }
    views {
        component api {
            include *
        }
    }
}'''
        elements, views = c4_assemble.parse_dsl_model(dsl)
        self.assertEqual(
            c4_assemble.find_orphaned_component_containers(elements, views), [],
            "keyless component view scoped to 'api' should cover it")


if __name__ == "__main__":
    unittest.main()
