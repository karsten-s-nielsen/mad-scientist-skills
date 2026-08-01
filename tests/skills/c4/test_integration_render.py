import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

import c4_assemble

FIXTURES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")
HOME = os.path.expanduser("~")
WAR = os.path.join(HOME, ".claude", "tools", "structurizr.war")
JAR = os.path.join(HOME, ".claude", "tools", "plantuml.jar")


def _toolchain_ready():
    if not (shutil.which("java") and os.path.exists(WAR) and os.path.exists(JAR)):
        return False
    # PlantUML's own Graphviz gate — NOT `dot -V`/`which dot`.
    try:
        r = subprocess.run(["java", "-jar", JAR, "-testdot"],
                           capture_output=True, text=True, timeout=60)
    except Exception:
        return False
    return r.returncode == 0 and "seems OK" in (r.stdout + r.stderr)


def _widest_rect(svg):
    return max((float(w) for w in re.findall(r'<rect[^>]*\bwidth="([0-9.]+)"', svg)),
               default=0.0)


@unittest.skipUnless(_toolchain_ready(),
                     "Java 21 + structurizr.war + plantuml.jar + Graphviz (-testdot) required")
class IntegrationRenderTest(unittest.TestCase):
    def test_wrap_width_narrows_containers_box(self):
        with open(os.path.join(FIXTURES, "sample.dsl"), encoding="utf-8") as fh:
            dsl = fh.read()

        def render(px):
            d = tempfile.mkdtemp()
            dsl_path = os.path.join(d, "architecture.dsl")
            with open(dsl_path, "w", encoding="utf-8") as fh:
                fh.write(dsl)
            subprocess.run(["java", "-jar", WAR, "export", "-workspace", dsl_path,
                            "-format", "plantuml/c4plantuml", "-output", d],
                           check=True, capture_output=True, timeout=180)
            puml = os.path.join(d, "structurizr-Containers.puml")
            with open(puml, encoding="utf-8") as fh:
                text = fh.read()
            with open(puml, "w", encoding="utf-8") as fh:
                fh.write(c4_assemble.inject_wrap_width(text, px))
            subprocess.run(["java", "-jar", JAR, puml, "-tsvg"],
                           check=True, capture_output=True, timeout=180)
            with open(os.path.join(d, "structurizr-Containers.svg"), encoding="utf-8") as fh:
                return fh.read()

        svg200 = render(200)
        svg150 = render(150)
        self.assertGreater(c4_assemble.count_entities(svg150), 0)
        # Rendered-width assertion — source placement alone can't catch clobbering.
        self.assertLess(_widest_rect(svg150), _widest_rect(svg200))

    def test_syntax_error_placeholder_has_zero_entities(self):
        # An all-non-word element name yields an empty alias -> PlantUML "Syntax
        # Error" placeholder (exit 200, no "Cannot find Graphviz" string).
        bad = ('workspace "B" {\n  model {\n    s = softwareSystem "!!!" "d"\n  }\n'
               '  views {\n    systemContext s "SystemContext" {\n      include *\n'
               '      autoLayout\n    }\n  }\n}\n')
        d = tempfile.mkdtemp()
        dsl_path = os.path.join(d, "architecture.dsl")
        with open(dsl_path, "w", encoding="utf-8") as fh:
            fh.write(bad)
        subprocess.run(["java", "-jar", WAR, "export", "-workspace", dsl_path,
                        "-format", "plantuml/c4plantuml", "-output", d],
                       check=True, capture_output=True, timeout=180)
        puml = os.path.join(d, "structurizr-SystemContext.puml")
        subprocess.run(["java", "-jar", JAR, puml, "-tsvg"],
                       capture_output=True, timeout=180)  # may exit non-zero
        svg_path = os.path.join(d, "structurizr-SystemContext.svg")
        if not os.path.exists(svg_path):
            self.skipTest("no SVG emitted for the syntax-error case on this PlantUML build")
        with open(svg_path, encoding="utf-8") as fh:
            svg = fh.read()
        self.assertEqual(c4_assemble.count_entities(svg), 0)


if __name__ == "__main__":
    unittest.main()
