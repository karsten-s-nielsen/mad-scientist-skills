import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import c4_assemble  # noqa: E402


class DslAliasTest(unittest.TestCase):
    def test_single_word_stripped(self):
        self.assertEqual(c4_assemble.dsl_alias("Web App", []), "WebApp")

    def test_api_service(self):
        self.assertEqual(c4_assemble.dsl_alias("API Service", []), "APIService")

    def test_multi_parent_chain(self):
        self.assertEqual(
            c4_assemble.dsl_alias("Auth Middleware", ["Order Platform", "API Service"]),
            "OrderPlatform.APIService.AuthMiddleware",
        )

    def test_unicode_preserved_no_re_ascii(self):
        # Python's default \W is Unicode-aware; re.ASCII would give "Cafber".
        self.assertEqual(c4_assemble.dsl_alias("Café Über", []), "CaféÜber")

    def test_all_non_word_name_is_empty(self):
        self.assertEqual(c4_assemble.dsl_alias("!!!", []), "")

    def test_punctuation_stripped_but_alnum_kept(self):
        self.assertEqual(c4_assemble.dsl_alias("Tom & Jerry's App", []), "TomJerrysApp")


if __name__ == "__main__":
    unittest.main()
