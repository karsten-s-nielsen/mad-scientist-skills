import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import c4_assemble  # noqa: E402

# Minimal shapes mirroring the real exporter output (verified 2026-07-22):
# the LAST C4 include differs per view type.
CONTAINERS = "@startuml\n!include <C4/C4>\n!include <C4/C4_Context>\n!include <C4/C4_Container>\n\nPerson(EndUser, \"End User\")\n@enduml\n"
CONTEXT = "@startuml\n!include <C4/C4>\n!include <C4/C4_Context>\n\nPerson(EndUser, \"End User\")\n@enduml\n"
COMPONENT = "@startuml\n!include <C4/C4>\n!include <C4/C4_Context>\n!include <C4/C4_Component>\n\nComponent(x, \"X\")\n@enduml\n"
NO_INCLUDE = "@startuml\nPerson(EndUser, \"End User\")\n@enduml\n"


def _lines(s):
    return s.splitlines()


class InjectWrapWidthTest(unittest.TestCase):
    def _assert_after_last_include(self, puml, px=150):
        out = c4_assemble.inject_wrap_width(puml, px)
        lines = _lines(out)
        inject_idx = next(i for i, ln in enumerate(lines)
                          if ln.strip() == "skinparam wrapWidth %d" % px)
        include_idxs = [i for i, ln in enumerate(lines) if ln.startswith("!include <C4/")]
        self.assertTrue(include_idxs, "fixture must have C4 includes")
        # skinparam lands immediately after the LAST include.
        self.assertEqual(inject_idx, max(include_idxs) + 1)

    def test_after_last_include_container(self):
        self._assert_after_last_include(CONTAINERS)

    def test_after_last_include_context(self):
        self._assert_after_last_include(CONTEXT)

    def test_after_last_include_component(self):
        self._assert_after_last_include(COMPONENT)

    def test_exactly_one_skinparam_line(self):
        out = c4_assemble.inject_wrap_width(CONTAINERS, 150)
        self.assertEqual(out.count("skinparam wrapWidth 150"), 1)

    def test_no_include_falls_back_before_enduml(self):
        out = c4_assemble.inject_wrap_width(NO_INCLUDE, 150)
        lines = _lines(out)
        inject_idx = next(i for i, ln in enumerate(lines)
                          if ln.strip() == "skinparam wrapWidth 150")
        enduml_idx = next(i for i, ln in enumerate(lines) if ln.strip() == "@enduml")
        self.assertLess(inject_idx, enduml_idx)

    def test_no_anchor_returns_unchanged(self):
        src = "just some text\nno markers here\n"
        out = c4_assemble.inject_wrap_width(src, 150)
        self.assertEqual(out, src)

    def test_idempotent(self):
        once = c4_assemble.inject_wrap_width(CONTAINERS, 150)
        twice = c4_assemble.inject_wrap_width(once, 150)
        self.assertEqual(once, twice)


if __name__ == "__main__":
    unittest.main()
