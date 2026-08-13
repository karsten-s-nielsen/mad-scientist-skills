"""The box-description authoring cap.

`MAX_BOX_DESCR_CHARS` was a documented rule that nothing measured — the same shape
of gap as `MAX_ELEMENTS_PER_VIEW`. A scan of 18 real workspaces found 14 elements
over the cap, the worst at 664 characters, including three in this repo's own
diagram. Advisory, like its peer: an overlong description is a readability cost,
not a broken render.
"""

import unittest

import c4_assemble


def dsl_with(description, kind="container"):
    return ('workspace "W" {\n  model {\n'
            '    s = softwareSystem "Sys" "d" {\n'
            '      c = %s "Box" "%s" "Tech"\n'
            "    }\n  }\n"
            '  views {\n    systemContext s "SystemContext" { include * }\n  }\n}\n'
            % (kind, description))


class DescriptionParsingTest(unittest.TestCase):
    def test_second_quoted_token_is_the_description(self):
        elements, _v = c4_assemble.parse_dsl_model(dsl_with("A description"))
        box = next(e for e in elements if e.identifier == "c")
        self.assertEqual(box.name, "Box")
        self.assertEqual(box.description, "A description")

    def test_technology_is_not_mistaken_for_description(self):
        # `container "Name" "Description" "Technology"` — parsing must stop at the
        # second quoted token or a short description followed by a long technology
        # string would be measured instead.
        elements, _v = c4_assemble.parse_dsl_model(dsl_with("short"))
        box = next(e for e in elements if e.identifier == "c")
        self.assertEqual(box.description, "short")

    def test_missing_description_is_none(self):
        dsl = ('workspace "W" {\n  model {\n    s = softwareSystem "Sys"\n  }\n'
               '  views {\n    systemContext s "SystemContext" { include * }\n  }\n}\n')
        elements, _v = c4_assemble.parse_dsl_model(dsl)
        self.assertIsNone(elements[0].description)

    def test_element_still_constructs_from_four_positionals(self):
        # The field was appended with a default precisely so existing construction
        # and attribute access keep working.
        e = c4_assemble.Element("id", "Name", "container", None)
        self.assertIsNone(e.description)
        self.assertEqual((e.identifier, e.name, e.kind, e.parent),
                         ("id", "Name", "container", None))


class FindOverlongDescriptionsTest(unittest.TestCase):
    def _elements(self, *lengths):
        return [c4_assemble.Element("id%d" % i, "N%d" % i, "container", None, "x" * n)
                for i, n in enumerate(lengths)]

    def test_flags_only_above_the_cap(self):
        cap = c4_assemble.MAX_BOX_DESCR_CHARS
        over = c4_assemble.find_overlong_descriptions(
            self._elements(cap - 1, cap, cap + 1))
        self.assertEqual([o[0] for o in over], ["id2"])

    def test_reports_the_measured_length(self):
        cap = c4_assemble.MAX_BOX_DESCR_CHARS
        over = c4_assemble.find_overlong_descriptions(self._elements(cap + 42))
        self.assertEqual(over[0][2], cap + 42)

    def test_sorted_worst_first(self):
        cap = c4_assemble.MAX_BOX_DESCR_CHARS
        over = c4_assemble.find_overlong_descriptions(
            self._elements(cap + 5, cap + 500, cap + 50))
        self.assertEqual([o[2] for o in over], [cap + 500, cap + 50, cap + 5])

    def test_empty_when_all_within_cap(self):
        self.assertEqual(c4_assemble.find_overlong_descriptions(self._elements(10)), [])

    def test_none_description_is_not_flagged(self):
        e = [c4_assemble.Element("id", "N", "container", None, None)]
        self.assertEqual(c4_assemble.find_overlong_descriptions(e), [])

    def test_cap_is_injectable_for_callers(self):
        over = c4_assemble.find_overlong_descriptions(self._elements(50), cap=10)
        self.assertEqual(len(over), 1)

    def test_end_to_end_from_dsl(self):
        cap = c4_assemble.MAX_BOX_DESCR_CHARS
        elements, _v = c4_assemble.parse_dsl_model(dsl_with("y" * (cap + 1)))
        over = c4_assemble.find_overlong_descriptions(elements)
        self.assertEqual([o[1] for o in over], ["Box"])


if __name__ == "__main__":
    unittest.main()
