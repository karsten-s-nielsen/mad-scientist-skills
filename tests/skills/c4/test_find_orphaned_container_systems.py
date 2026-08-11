import os
import sys
import unittest

import c4_assemble

FIXTURES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")


def _load(name):
    with open(os.path.join(FIXTURES, name), encoding="utf-8") as fh:
        return fh.read()


# billing has 2 containers AND a `container billing "Containers_billing"` view -> covered.
# deploy has 3 containers and NO container view -> orphaned.
# email declares no containers -> never an orphan.
ORPHAN_DSL = '''workspace "C" {
    model {
        billing = softwareSystem "Billing" {
            api = container "API" "d" "t"
            db = container "Ledger" "d" "PostgreSQL" "Database"
        }
        deploy = softwareSystem "Deploy Pipeline" {
            t1 = container "manage_space" "d" "Python"
            t2 = container "deploy_wheel" "d" "Python"
            t3 = container "bump_wheel" "d" "Python"
        }
        email = softwareSystem "Email Service" "Sends mail" "External"
    }
    views {
        systemContext billing "SystemContext" { include * }
        container billing "Containers_billing" { include * }
    }
}'''


class FindOrphanedContainerSystemsTest(unittest.TestCase):
    def test_sample_fixture_has_no_orphans(self):
        # sample.dsl: `system` is the only decomposed system and it HAS Containers.
        elements, views = c4_assemble.parse_dsl_model(_load("sample.dsl"))
        self.assertEqual(
            c4_assemble.find_orphaned_container_systems(elements, views), [])

    def test_decomposed_system_without_view_is_flagged(self):
        elements, views = c4_assemble.parse_dsl_model(ORPHAN_DSL)
        self.assertEqual(
            c4_assemble.find_orphaned_container_systems(elements, views),
            [("deploy", "Deploy Pipeline", 3)])

    def test_covered_system_not_flagged(self):
        elements, views = c4_assemble.parse_dsl_model(ORPHAN_DSL)
        orphans = c4_assemble.find_orphaned_container_systems(elements, views)
        self.assertNotIn("billing", [sid for sid, _, _ in orphans])

    def test_system_without_containers_not_flagged(self):
        # email has zero containers -> nothing to surface, so never an orphan.
        elements, views = c4_assemble.parse_dsl_model(ORPHAN_DSL)
        orphans = c4_assemble.find_orphaned_container_systems(elements, views)
        self.assertNotIn("email", [sid for sid, _, _ in orphans])

    def test_multiple_orphans_sorted_by_identifier(self):
        dsl = '''workspace "C" {
    model {
        zeta = softwareSystem "Zeta" { z1 = container "Z" "d" "t" }
        alpha = softwareSystem "Alpha" { a1 = container "A" "d" "t" }
    }
    views {
        systemContext zeta "SystemContext" { include * }
    }
}'''
        elements, views = c4_assemble.parse_dsl_model(dsl)
        orphans = c4_assemble.find_orphaned_container_systems(elements, views)
        self.assertEqual([sid for sid, _, _ in orphans], ["alpha", "zeta"])

    def test_include_from_another_systems_view_is_not_coverage(self):
        # THE case that made the real defect survive review. `include <containerId>`
        # inside ANOTHER system's container view looks like coverage but is not: a
        # container view may only hold containers of its own scope, so the exporter
        # drops the foreign include and the element renders in no diagram. Only a
        # `container <thisSystem> ...` view counts.
        dsl = '''workspace "C" {
    model {
        store = softwareSystem "Store" { s1 = container "Catalog" "d" "t" }
        dbt = softwareSystem "dbt Project" {
            costs = container "fct_workflow_costs" "d" "SQL, dbt" "Database"
        }
    }
    views {
        container store "Containers_store" {
            include *
            include costs
            autoLayout
        }
    }
}'''
        elements, views = c4_assemble.parse_dsl_model(dsl)
        self.assertEqual(
            c4_assemble.find_orphaned_container_systems(elements, views),
            [("dbt", "dbt Project", 1)],
            "an include in a foreign system's view must not suppress the warning")

    def test_keyless_container_view_still_covers_its_scope(self):
        # The view key is OPTIONAL in Structurizr DSL (the exporter generates one).
        # scope_identifier is the anchor, not the absent key — mirrors the component
        # lint's keyless case.
        dsl = '''workspace "C" {
    model {
        sys = softwareSystem "Sys" { api = container "API" "d" "t" }
    }
    views {
        container sys {
            include *
        }
    }
}'''
        elements, views = c4_assemble.parse_dsl_model(dsl)
        self.assertEqual(
            c4_assemble.find_orphaned_container_systems(elements, views), [],
            "keyless container view scoped to 'sys' should cover it")

    def test_component_view_is_not_container_coverage(self):
        # A deeper view does not stand in for the level above it: the components
        # render, the containers themselves still appear in no Level-2 diagram.
        dsl = '''workspace "C" {
    model {
        sys = softwareSystem "Sys" {
            api = container "API" "d" "t" { c1 = component "Ctrl" "d" "t" }
        }
    }
    views {
        component api "Component_api" { include * }
    }
}'''
        elements, views = c4_assemble.parse_dsl_model(dsl)
        self.assertEqual(
            c4_assemble.find_orphaned_container_systems(elements, views),
            [("sys", "Sys", 1)])

    def test_commented_out_container_view_is_not_coverage(self):
        # Commenting a view out is how someone disables it; if the tokenizer still
        # reads it as a view declaration, the lint that should now fire goes quiet.
        dsl = '''workspace "C" {
    model {
        sys = softwareSystem "Sys" { api = container "API" "d" "t" }
    }
    views {
        systemContext sys "SystemContext" { include * }
        # container sys "Containers_sys" {
        #     include *
        # }
    }
}'''
        elements, views = c4_assemble.parse_dsl_model(dsl)
        self.assertEqual(
            c4_assemble.find_orphaned_container_systems(elements, views),
            [("sys", "Sys", 1)],
            "a commented-out container view must not count as coverage")

    def test_grouped_containers_still_attach_to_their_system(self):
        # `group` is a transparent scope: containers inside one still belong to the
        # software system, so a grouped-but-unrendered system is still flagged.
        dsl = '''workspace "C" {
    model {
        sys = softwareSystem "Sys" {
            group "Backend" {
                api = container "API" "d" "t"
            }
        }
    }
    views {
        systemContext sys "SystemContext" { include * }
    }
}'''
        elements, views = c4_assemble.parse_dsl_model(dsl)
        self.assertEqual(
            c4_assemble.find_orphaned_container_systems(elements, views),
            [("sys", "Sys", 1)])


if __name__ == "__main__":
    unittest.main()
