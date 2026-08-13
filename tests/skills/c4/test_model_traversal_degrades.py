"""Assembly must survive a model that parses but then breaks a consumer.

`parse_dsl_model` and its four consumers (`build_drilldown_map`, both coverage
lints, `build_view_labels`) were originally wrapped in ONE try/except under the
contract "parsing must never crash assembly". Hoisting the parse earlier so tab
order can follow the DSL must not shrink that contract to the parse call alone:
a successful parse yielding a well-formed-but-unusual model that trips a consumer
should still produce a diagram, with drill-down disabled.
"""

import os
import subprocess
import sys
import tempfile
import textwrap
import unittest

_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))
SCRIPT = os.path.join(_REPO_ROOT, "plugins", "mad-scientist-skills",
                      "skills", "c4", "c4_assemble.py")

SVG = ('<svg xmlns="http://www.w3.org/2000/svg">'
       '<g class="entity" data-qualified-name="Sys"><rect width="10" height="10"/>'
       "</g></svg>")

DSL = ('workspace "Sys" {\n  model {\n    s = softwareSystem "Sys" "d"\n  }\n'
       '  views {\n    systemContext s "SystemContext" { include * }\n  }\n}\n')

# Sitecustomize-style shim: make one consumer raise on a model that parsed fine.
SHIM = textwrap.dedent("""
    import runpy, sys
    import c4_assemble

    def boom(*a, **k):
        raise RuntimeError("synthetic consumer failure")

    c4_assemble.build_drilldown_map = boom
    sys.argv = ARGV
    c4_assemble.main()
""")


class ModelTraversalDegradesTest(unittest.TestCase):
    def _run_with_broken_consumer(self, d):
        dsl_path = os.path.join(d, "architecture.dsl")
        with open(dsl_path, "w", encoding="utf-8") as fh:
            fh.write(DSL)
        svg_dir = os.path.join(d, "svgs")
        os.makedirs(svg_dir, exist_ok=True)
        with open(os.path.join(svg_dir, "structurizr-SystemContext.svg"),
                  "w", encoding="utf-8") as fh:
            fh.write(SVG)
        out = os.path.join(d, "architecture.html")
        argv = [SCRIPT, d, "--dsl-path", dsl_path, "--svg-dir", svg_dir,
                "--system-name", "Sys", "--output", out]
        driver = os.path.join(d, "driver.py")
        with open(driver, "w", encoding="utf-8") as fh:
            fh.write("ARGV = %r\n" % argv + SHIM)
        env = dict(os.environ)
        env["PYTHONPATH"] = os.path.dirname(SCRIPT)
        r = subprocess.run([sys.executable, driver], capture_output=True,
                           text=True, timeout=60, env=env)
        return r, out

    def test_consumer_failure_still_writes_a_diagram(self):
        with tempfile.TemporaryDirectory() as d:
            r, out = self._run_with_broken_consumer(d)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            self.assertTrue(os.path.exists(out),
                            "a consumer failure must not cost the whole diagram")
            self.assertIn("synthetic consumer failure", r.stderr)
            with open(out, encoding="utf-8") as fh:
                self.assertIn("<svg", fh.read())

    def test_failure_is_reported_not_swallowed(self):
        with tempfile.TemporaryDirectory() as d:
            r, _out = self._run_with_broken_consumer(d)
            self.assertIn("WARN", r.stderr)


if __name__ == "__main__":
    unittest.main()
