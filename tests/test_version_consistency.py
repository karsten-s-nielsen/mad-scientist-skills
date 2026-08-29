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

A companion check guards the release step most often forgotten (missed three
times across past releases): that the current version has a dated ``## [X.Y.Z]``
section *and* a ``[X.Y.Z]:`` compare-link in the CHANGELOG — not just changes
accumulated under ``[Unreleased]``.
"""
import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PLUGIN_JSON = REPO_ROOT / "plugins" / "mad-scientist-skills" / ".claude-plugin" / "plugin.json"
MARKETPLACE_JSON = REPO_ROOT / ".claude-plugin" / "marketplace.json"
README = REPO_ROOT / "README.md"
CHANGELOG = REPO_ROOT / "CHANGELOG.md"

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


def test_changelog_has_a_dated_section_and_compare_link_for_the_current_version():
    version = _plugin_manifest()["version"]
    changelog = CHANGELOG.read_text(encoding="utf-8")
    escaped = re.escape(version)
    has_section = re.search(rf"^## \[{escaped}\] - \d{{4}}-\d{{2}}-\d{{2}}", changelog, re.MULTILINE)
    has_link = re.search(rf"^\[{escaped}\]: \S+", changelog, re.MULTILINE)
    assert has_section, (
        f"CHANGELOG.md has no dated '## [{version}] - YYYY-MM-DD' section — "
        "cut the release section; do not leave the changes under [Unreleased]."
    )
    assert has_link, (
        f"CHANGELOG.md footer has no '[{version}]:' compare-link — "
        "add it (and repoint [Unreleased]) when cutting the release."
    )
