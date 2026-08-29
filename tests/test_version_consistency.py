"""Guard against version drift across the plugin's declaration sites.

The version is declared in three hand-maintained places — the plugin manifest,
the marketplace manifest, and the README badge — with nothing else enforcing
that they agree. Unlike a Python package, a Claude Code plugin cannot collapse
these to a single source: the plugin and marketplace manifests each require the
version inline. So the guard is a CI check, not single-sourcing: this suite
fails when any site drifts, which turns a partial bump (some files moved, one
left behind) from a silent merge into a red build.

The two manifests also keep the plugin ``description`` byte-identical; that is
guarded here too, since a description edit to one manifest is just as easy to
forget in the other.
"""
import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PLUGIN_JSON = REPO_ROOT / "plugins" / "mad-scientist-skills" / ".claude-plugin" / "plugin.json"
MARKETPLACE_JSON = REPO_ROOT / ".claude-plugin" / "marketplace.json"
README = REPO_ROOT / "README.md"

_SEMVER = r"[0-9]+\.[0-9]+\.[0-9]+"
_BADGE_RE = re.compile(rf"version-({_SEMVER})-")


def _plugin_manifest():
    return json.loads(PLUGIN_JSON.read_text(encoding="utf-8"))


def _marketplace_entry():
    data = json.loads(MARKETPLACE_JSON.read_text(encoding="utf-8"))
    plugins = data["plugins"]
    assert len(plugins) == 1, f"expected exactly one plugin entry, got {len(plugins)}"
    return plugins[0]


def _readme_badge_version():
    match = _BADGE_RE.search(README.read_text(encoding="utf-8"))
    assert match is not None, "no `version-X.Y.Z-` badge found in README.md"
    return match.group(1)


def test_version_agrees_across_all_declaration_sites():
    plugin_version = _plugin_manifest()["version"]
    marketplace_version = _marketplace_entry()["version"]
    badge_version = _readme_badge_version()
    assert plugin_version == marketplace_version == badge_version, (
        "version drift: "
        f"plugin.json={plugin_version!r}, "
        f"marketplace.json={marketplace_version!r}, "
        f"README badge={badge_version!r} — bump all three together."
    )


def test_plugin_description_is_byte_identical_across_manifests():
    plugin_description = _plugin_manifest()["description"]
    marketplace_description = _marketplace_entry()["description"]
    assert plugin_description == marketplace_description, (
        "plugin.json and marketplace.json plugin descriptions have diverged — "
        "keep them byte-identical (edit both, or copy one into the other)."
    )
