import os
import sys
import unittest

import c4_assemble

FIXTURES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")


class CountEntitiesTest(unittest.TestCase):
    def test_real_render_has_four_entities(self):
        with open(os.path.join(FIXTURES, "containers.svg"), encoding="utf-8") as fh:
            svg = fh.read()
        self.assertEqual(c4_assemble.count_entities(svg), 4)

    def test_placeholder_has_zero_entities(self):
        # A "Cannot find Graphviz"/"Syntax Error" placeholder carries no entity groups.
        placeholder = '<svg width="413" height="368"><text>Cannot find Graphviz</text></svg>'
        self.assertEqual(c4_assemble.count_entities(placeholder), 0)

    def test_counts_regardless_of_whitespace(self):
        svg = '<g   class="entity" data-qualified-name="x"></g>'
        self.assertEqual(c4_assemble.count_entities(svg), 1)


if __name__ == "__main__":
    unittest.main()
