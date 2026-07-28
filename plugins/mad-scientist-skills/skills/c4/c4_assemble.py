#!/usr/bin/env python3
"""C4 Architecture HTML Assembler.

Cleans rendered SVGs and assembles them into a self-contained architecture.html
with tabbed navigation, embedded SVGs, and a Structurizr DSL source panel.

Usage:
    python c4_assemble.py <project-dir> [--svg-dir <dir>] [--views <view-spec>...]

Arguments:
    project-dir         Path to the project root
    --dsl-path          Path to architecture.dsl (default: <project-dir>/architecture.dsl,
                        falls back to <project-dir>/docs/c4/architecture.dsl)
    --output            Path to write architecture.html (default: same dir as DSL file)
    --svg-dir           Directory containing rendered SVGs (default: system temp dir)
    --views             View specifications as key:label:filename triples (default: auto-detect).
                        The key is the Structurizr view key and controls tab grouping via
                        parse_view_key, so it must match the exported key (e.g. SystemContext,
                        Containers, Containers_<systemId>, Component_<containerId>) — not a
                        lowercase-hyphen slug.
    --system-name       System name for the HTML title (default: extracted from DSL)
    --inject-wrap-width PUML_DIR
                        Pre-render mode: inject `skinparam wrapWidth` into every *.puml in
                        PUML_DIR (after the last C4 include) and exit. Run between the
                        structurizr export and the plantuml render; does not assemble HTML.
    --wrap-width        Pixel wrap width injected by --inject-wrap-width (default: BOX_WRAP_WIDTH_PX).

Examples:
    # Auto-detect DSL location and views from SVG filenames in temp dir
    python c4_assemble.py /path/to/project

    # Specify SVG directory explicitly
    python c4_assemble.py /path/to/project --svg-dir /tmp/c4-render

    # Specify DSL path for projects with non-standard layout
    python c4_assemble.py /path/to/project --dsl-path /path/to/project/docs/c4/architecture.dsl

    # Pre-render: inject wrapWidth into exported *.puml, then exit (run before plantuml)
    python c4_assemble.py /path/to/project --inject-wrap-width /tmp/c4-render

    # Specify views explicitly (one --views flag, space-separated specs; the key must be
    # the Structurizr view key so tabs group correctly)
    python c4_assemble.py /path/to/project --views \
        "SystemContext:System Context:structurizr-SystemContext.svg" \
        "Containers:Containers:structurizr-Containers.svg"

SVG Cleaning (per C4 skill spec):
    1. Strips <?plantuml ...?> processing instructions
    2. Strips <?plantuml-src ...?> processing instructions
    3. Strips <title>...</title> elements
    4. Strips <g class="title"[^>]*>...</g> groups (handles extra attributes)
    5. Strips active content — <script>/<foreignObject> blocks, on*= handlers,
       and javascript:/vbscript: hrefs — while preserving data:image/# links.
       Scoped to inert PlantUML output; hostile shapes it cannot safely rewrite
       (slash-separated handlers, obfuscated schemes) fail-closed at step 6
       rather than being neutralized in place — see clean_svg's docstring.
    6. Verifies each SVG is clean before embedding (mandatory check; aborts on leak)

Output:
    Writes architecture.html in the same directory as the DSL file.
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import html as html_mod
import json
import re
import sys
import tempfile
from pathlib import Path

# --- Readability & navigation constants (see SKILL.md "Readability & Navigation") ---
MAX_BOX_DESCR_CHARS = 200   # authoring cap (chars) — enforced by SKILL.md rule, not code
BOX_WRAP_WIDTH_PX = 200     # render wrap (px) — injected into intermediate .puml (C4 stock width)
MAX_ELEMENTS_PER_VIEW = 15  # subdivision guideline (SKILL.md) — not tool-enforced

# (filename, raw Structurizr view key, tab label). tab_id is derived via
# view_key_to_tab_id(raw_key); grouping/breadcrumbs key on raw_key.
# The fallback detection (below) handles any structurizr-*.svg file not listed here.
KNOWN_VIEWS = [
    ("structurizr-SystemContext.svg", "SystemContext", "System Context"),
    ("structurizr-Containers.svg", "Containers", "Containers"),
    ("structurizr-Components.svg", "Components", "Components"),
    ("structurizr-Dynamic.svg", "Dynamic", "Dynamic"),
    ("structurizr-Deployment.svg", "Deployment", "Deployment"),
]


# Active-content patterns stripped from third-party SVG before it is embedded
# verbatim into architecture.html, plus the matching verify_clean guards. The
# cleaned SVG lands inline in the page, so anything the browser would execute
# has to go. PlantUML's own output is inert, but the module bills itself as
# "cleaning" the SVG — so it must actually neutralize active content rather than
# create false assurance. Dangerous-scheme hrefs are matched narrowly:
# javascript:/vbscript: only, so legitimate `data:image/...` icons and
# `#fragment` refs that PlantUML emits are left untouched. The value class
# [^"']* stops at the first quote of EITHER kind, so a scheme href whose value
# embeds the opposite quote (href="javascript:x('y')") is NOT rewritten here —
# by design: verify_clean's quote-agnostic guard then aborts the build
# fail-closed rather than shipping it. (PlantUML never emits such hrefs.)
_ACTIVE_SCHEME_RE = re.compile(
    r"""((?:xlink:)?href\s*=\s*)(["'])\s*(?:javascript|vbscript):[^"']*(\2)""",
    re.IGNORECASE,
)

# on*= handler with a QUOTED value, matched only within a single start-tag span
# (the enclosing `<[^>]+>` guarantees no `>` intervenes, so the lazy value stays
# inside the tag and cannot run into following markup).
_HANDLER_IN_TAG_RE = re.compile(r"""\s+on[a-zA-Z]+\s*=\s*(["'])[\s\S]*?\1""")


def _strip_handlers_in_tag(m) -> str:
    """Drop quoted on*= handlers from a single matched start-tag span."""
    return _HANDLER_IN_TAG_RE.sub("", m.group(0))


def clean_svg(content: str) -> str:
    """Strip processing instructions, title elements/groups, AND active content.

    This is the critical cleaning step. PlantUML generates SVGs with:
    - <?plantuml ...?> processing instructions at the top
    - <title>...</title> elements inside the SVG
    - <g class="title" data-source-line="1">...</g> groups with rendered title text

    The <g> tag has EXTRA ATTRIBUTES beyond just class="title", so the regex
    must use [^>]* to match them. A regex like <g class="title">...</g>
    without the attribute wildcard will SILENTLY FAIL to match.

    Active-content hardening (defense-in-depth, stdlib only): remove <script> and
    <foreignObject> blocks, drop on*= event-handler attributes, and neutralize
    javascript:/vbscript: href schemes. Benign PlantUML output — embedded
    `data:image/...` icons and `#fragment` links — is deliberately preserved.

    Scope (read before trusting this as a boundary): this is best-effort
    hardening of PlantUML's own (inert) output plus a fail-closed `verify_clean`
    gate — NOT a general-purpose sanitizer for arbitrary untrusted SVG (regex is
    the wrong tool for that). clean_svg only rewrites shapes it can neutralize
    WITHOUT risking corruption of benign markup (quoted, whitespace-separated
    handlers; literal javascript:/vbscript:). Anything it cannot safely rewrite —
    slash-separated handlers (`<svg/onload=...>`), or entity/control-char
    obfuscated schemes (`jav&#x61;script:`) — is left for verify_clean to REJECT,
    aborting the build rather than shipping active content.
    """
    # 1. Remove <?plantuml ...?> processing instructions
    content = re.sub(r"<\?plantuml[\s\S]*?\?>", "", content)
    # 2. Remove <?plantuml-src ...?> processing instructions (can be multiline)
    content = re.sub(r"<\?plantuml-src[\s\S]*?\?>", "", content)
    # 3. Remove <title>...</title> element
    content = re.sub(r"<title>.*?</title>", "", content, flags=re.DOTALL)
    # 4. Remove <g class="title" ...>...</g> group — [^>]* matches extra attributes
    content = re.sub(r'<g class="title"[^>]*>.*?</g>', "", content, flags=re.DOTALL)
    # 5. Remove <script>...</script> blocks (with or without attributes; also a
    #    self-closing/empty variant).
    content = re.sub(r"<script\b[^>]*>[\s\S]*?</script\s*>", "", content, flags=re.IGNORECASE)
    content = re.sub(r"<script\b[^>]*/>", "", content, flags=re.IGNORECASE)
    # 6. Remove <foreignObject>...</foreignObject> (can smuggle HTML/iframes).
    content = re.sub(r"<foreignObject\b[^>]*>[\s\S]*?</foreignObject\s*>", "",
                     content, flags=re.IGNORECASE)
    content = re.sub(r"<foreignObject\b[^>]*/>", "", content, flags=re.IGNORECASE)
    # 7. Drop on*= event-handler attributes (onload, onclick, ...), but ONLY
    #    inside an element start tag — a handler executes only as an attribute,
    #    never as text. Anchoring to a single `<...>` span (which cannot contain
    #    a `>`) keeps the strip from (a) mangling <text> prose that merely reads
    #    "online=..." / 'only="30"' and (b) letting the lazy value match run
    #    across a tag boundary and delete real markup. Quoted values only — an
    #    UNquoted handler can't be delimited safely by regex, so we deliberately
    #    do NOT strip it here; verify_clean's unquoted-tolerant, tag-anchored
    #    check then ABORTS the build rather than shipping it (fail-closed).
    content = re.sub(r"<[^>]+>", _strip_handlers_in_tag, content)
    # 8. Neutralize javascript:/vbscript: in (xlink:)href — leave data:image/# intact.
    content = _ACTIVE_SCHEME_RE.sub(r'\1\2#\3', content)
    return content.strip()


# (xlink:)href value extractor + dangerous-scheme matcher for verify_clean. The
# scheme is tested against a NORMALIZED value (HTML entities decoded, tab/newline
# stripped, leading control/space removed) — the same normalization a browser
# applies before resolving a URL — so `jav&#x61;script:` and `java\tscript:`
# cannot smuggle a live scheme past a raw-substring scan. Matched anchored at the
# value start, so a benign `?next=javascript` query value never trips it.
# data:text/html is rejected (renders attacker HTML); data:image/... stays allowed.
_HREF_VALUE_RE = re.compile(r'(?:xlink:)?href\s*=\s*(["\'])(.*?)\1',
                            re.IGNORECASE | re.DOTALL)
_DANGEROUS_HREF_RE = re.compile(r"(?:javascript|vbscript):|data:text/html", re.IGNORECASE)


def _normalized_href_values(content: str):
    """Yield each (xlink:)href value the way a browser normalizes a URL scheme:
    HTML entities decoded, ASCII tab/newline removed, leading control/space stripped."""
    for m in _HREF_VALUE_RE.finditer(content):
        val = html_mod.unescape(m.group(2))
        val = re.sub(r"[\t\n\r]", "", val)       # URL parser drops these anywhere
        val = re.sub(r"^[\x00-\x20]+", "", val)  # leading C0-control/space stripped
        yield val


def verify_clean(name: str, content: str) -> None:
    """Verify title-related AND active content has been removed. Abort if not."""
    checks = [
        (r"<\?plantuml", "processing instruction (<?plantuml)"),
        (r"<title>", "title element (<title>)"),
        (r'class="title"', 'title group (class="title")'),
        (r"<script\b", "script element (<script>)"),
        (r"<foreignObject\b", "foreignObject element"),
        # Anchor to a start tag (`<` then no intervening `>`), mirroring where a
        # handler can execute. `[\s/]` — not just `\s` — because HTML also accepts
        # `/` as an attribute separator, so `<svg/onload=...>` runs on parse and a
        # whitespace-only guard let it through. Anchoring still ignores benign
        # <text> prose like "online=true"; still catches quoted AND unquoted.
        (r"<[^>]*[\s/]on[a-zA-Z]+\s*=", "inline event handler (on*=)"),
    ]
    for pattern, desc in checks:
        if re.search(pattern, content, re.IGNORECASE):
            print(f"  FAIL: {name} still contains {desc} after cleaning!", file=sys.stderr)
            sys.exit(1)
    # Dangerous-scheme href check on the NORMALIZED value, so entity/whitespace
    # obfuscation cannot slip a live javascript:/vbscript:/data:text/html past.
    for val in _normalized_href_values(content):
        if _DANGEROUS_HREF_RE.match(val):
            print(f"  FAIL: {name} still contains active-scheme href "
                  f"({val[:40]!r}) after cleaning!", file=sys.stderr)
            sys.exit(1)
    print(f"  VERIFIED: {name}")


def inject_wrap_width(puml: str, px: int) -> str:
    """Insert `skinparam wrapWidth <px>` after the LAST `!include <C4/...>` line.

    Every C4 sub-include (C4, C4_Context, C4_Container, C4_Component) re-emits
    `skinparam wrapWidth $DEFAULT_WRAP_WIDTH` (200), so an injection before the
    last include is silently clobbered and does NOT narrow the box. Fallback:
    before the last @enduml. If neither anchor exists, return unchanged + warn.
    Idempotent for the same px.
    """
    directive = "skinparam wrapWidth %d" % px
    if directive in puml:
        return puml

    lines = puml.splitlines(keepends=True)
    last_include = -1
    last_enduml = -1
    for i, line in enumerate(lines):
        if line.startswith("!include <C4/"):
            last_include = i
        if line.strip() == "@enduml":
            last_enduml = i

    if last_include >= 0:
        insert_at = last_include + 1
    elif last_enduml >= 0:
        insert_at = last_enduml
    else:
        print("  WARN: no !include <C4/...> or @enduml anchor; wrapWidth not injected",
              file=sys.stderr)
        return puml

    # Match the surrounding newline style: reuse the anchor line's trailing newline.
    ref = lines[last_include] if last_include >= 0 else lines[last_enduml]
    nl = "\r\n" if ref.endswith("\r\n") else "\n"
    lines.insert(insert_at, directive + nl)
    return "".join(lines)


def _filter_ident(s: str) -> str:
    """Exporter's filter(name): strip all non-word chars. Unicode-aware \\W;
    do NOT add re.ASCII (would corrupt Unicode names)."""
    return re.sub(r"\W", "", s)


def dsl_alias(name: str, parents: list[str]) -> str:
    """Full dotted alias = filter(each parent name) + filter(name), joined by '.'.

    Mirrors the Structurizr exporter's identifier construction. Returns "" when
    the element's own filtered segment is empty (all-non-word name) — callers
    treat "" as "do not wire".
    """
    own = _filter_ident(name)
    if not own:
        return ""
    segs = [_filter_ident(p) for p in parents] + [own]
    return ".".join(segs)


def alias_matches_qn(qn: str, alias: str) -> bool:
    """True iff the trailing '.'-segments of the SVG qualified-name equal the
    element's dotted alias. Segment-equality ONLY — never bare-name containment
    (interior segments false-fire) and never str.endswith (non-segment
    boundaries false-fire). See spec Verification Basis."""
    if not alias:
        return False
    a = alias.split(".")
    return qn.split(".")[-len(a):] == a


Element = collections.namedtuple("Element", ["identifier", "name", "kind", "parent"])
ViewDecl = collections.namedtuple("ViewDecl", ["view_type", "scope_identifier", "key"])

_ELEMENT_KINDS = ("softwareSystem", "container", "component", "person")
_VIEW_TYPES = ("systemContext", "container", "component", "dynamic", "deployment")
# Keywords that open a brace scope but are NOT element parents (transparent).
_TRANSPARENT_SCOPES = ("group", "deploymentEnvironment", "deploymentNode")


def _tokenize_dsl(dsl: str) -> list:
    """Tokens: quoted strings (one token, quotes kept), braces, and bare words.
    String-skipping so braces inside quoted descriptions do not count as scope."""
    tokens = []
    i, n = 0, len(dsl)
    while i < n:
        c = dsl[i]
        if c in " \t\r\n":
            i += 1
        elif c == '"':
            j = i + 1
            while j < n and dsl[j] != '"':
                if dsl[j] == "\\":
                    j += 1
                j += 1
            tokens.append(dsl[i:j + 1])  # include closing quote
            i = j + 1
        elif c in "{}":
            tokens.append(c)
            i += 1
        else:
            j = i
            while j < n and dsl[j] not in ' \t\r\n{}"':
                j += 1
            tokens.append(dsl[i:j])
            i = j
    return tokens


def _unquote(tok: str) -> str:
    if len(tok) >= 2 and tok[0] == '"' and tok[-1] == '"':
        return tok[1:-1]
    return tok


def parse_dsl_model(dsl: str):
    """Parse elements (identifier, name, kind, parent) and view declarations.

    Handles: braces inside quoted strings (string-skipping tokenizer),
    `group`/deployment scopes as transparent (brace-balanced but not element
    parents), anonymous elements (no `=` -> skipped), and multi-token
    positional args (name is the first quoted token after the kind keyword).
    Returns (list[Element], list[ViewDecl]).
    """
    tokens = _tokenize_dsl(dsl)
    elements = []
    views = []

    # frame_scope[d] = element identifier that owns brace level d, or None
    # (transparent / non-element block). Index 0 is outside the workspace.
    frame_scope = [None]
    depth = 0
    in_views_depth = None      # brace depth of the `views { }` block, or None
    pending_scope = None       # scope to assign to the NEXT `{` we open

    i = 0
    while i < len(tokens):
        tok = tokens[i]

        if tok == "{":
            depth += 1
            if len(frame_scope) <= depth:
                frame_scope.append(pending_scope)
            else:
                frame_scope[depth] = pending_scope
            pending_scope = None
            i += 1
            continue

        if tok == "}":
            if in_views_depth is not None and depth == in_views_depth:
                in_views_depth = None
            depth -= 1
            i += 1
            continue

        if tok == "views":
            in_views_depth = depth + 1  # the `{` that follows opens the views block
            pending_scope = None
            i += 1
            continue

        # View declarations: `<view_type> <scopeIdent> "Key" ... {`
        if in_views_depth is not None and depth >= in_views_depth and tok in _VIEW_TYPES:
            scope_ident = None
            key = None
            j = i + 1
            if j < len(tokens) and not tokens[j].startswith('"') and tokens[j] not in "{}":
                scope_ident = tokens[j]
                j += 1
            while j < len(tokens) and tokens[j] not in "{}":
                if tokens[j].startswith('"'):
                    key = _unquote(tokens[j])
                    break
                j += 1
            # Record even keyless views: the key is OPTIONAL in Structurizr DSL
            # (the exporter auto-generates one). scope_identifier still anchors
            # the view to its container, so the orphan lint counts it as coverage
            # and no false "declares components but has no view" WARN is emitted.
            # Drill-down wiring skips keyless views (their rendered key is
            # unpredictable — see build_drilldown_map's `not v.key` guard).
            views.append(ViewDecl(tok, scope_ident, key))
            i += 1
            continue

        # Transparent scope opener: its block must push None, not an element id.
        if tok in _TRANSPARENT_SCOPES:
            pending_scope = None
            i += 1
            continue

        # Element declarations: `ident = kind "Name" ...` (anonymous -> skipped).
        if tok in _ELEMENT_KINDS and in_views_depth is None:
            identifier = tokens[i - 2] if (i >= 2 and tokens[i - 1] == "=") else None
            name = None
            j = i + 1
            while j < len(tokens) and tokens[j] not in "{}":
                if tokens[j].startswith('"'):
                    name = _unquote(tokens[j])
                    break
                j += 1
            parent = next((frame_scope[d] for d in range(depth, -1, -1)
                           if frame_scope[d] is not None), None)
            if identifier is not None and name is not None:
                elements.append(Element(identifier, name, tok, parent))
                # If a `{` opens before the next `}`/sibling kind, it's this
                # element's block -> nested elements see it as parent.
                k = i + 1
                opens = False
                while k < len(tokens):
                    if tokens[k] == "{":
                        opens = True
                        break
                    if tokens[k] == "}" or tokens[k] in _ELEMENT_KINDS:
                        break
                    k += 1
                if opens:
                    pending_scope = identifier
            i += 1
            continue

        i += 1

    return elements, views


def dsl_alias_for(identifier: str, elements) -> str:
    """Resolve identifier -> element name + parent-name chain -> dsl_alias."""
    by_id = {e.identifier: e for e in elements}
    if identifier not in by_id:
        return ""
    parents = []
    p = by_id[identifier].parent
    guard = 0
    while p is not None and p in by_id and guard < 100:
        parents.append(by_id[p].name)
        p = by_id[p].parent
        guard += 1
    parents.reverse()
    return dsl_alias(by_id[identifier].name, parents)


GROUP_ORDER = ["Context", "Containers", "Components", "Dynamic", "Deployment", "DSL"]

# Synthetic (non-diagram) groups that always sort last, after any unknown group.
# Without this they sort by GROUP_ORDER position, which puts them AHEAD of the
# unknown groups appended afterwards — so a single bespoke view key pushed the
# DSL source panel into the middle of the tab row.
TAIL_GROUPS = {"DSL"}

# Synthetic panel holding the copyable Structurizr DSL source. Appended to the
# view set inside build_html; its tab id 'dsl' is RESERVED, so the collision
# check (run in main() over the rendered views) must include this entry or a
# user view whose key slugifies to 'dsl' would silently shadow it.
# (filename, tab_id, label, raw_key)
_DSL_VIEW = ("", "dsl", "Structurizr DSL", "DSL")


def parse_view_key(key: str) -> tuple:
    """Map a Structurizr view key to (group, sub_label) via a prefix table.

    NOT a naive split('_') — SystemContext/Containers carry no separator.
    Tolerant of both '_' and '-' as the level/scope separator so pre-existing
    user workspaces still group correctly. Unknown keys become their own group.

    The bare `Containers`/`Components` keys only cover a SINGLE-software-system
    workspace. Structurizr view keys must be unique, so a workspace with N systems
    needs N distinct container-view keys; without the `Containers`/`Container`
    prefixes below they each fell through to their own top-level group, and the
    tab row advertised architectural levels that do not exist.
    """
    if key == "SystemContext":
        return ("Context", "System Context")
    if key == "Containers":
        return ("Containers", "Containers")
    if key == "Components":
        return ("Components", "Components")
    if key == "DSL":
        return ("DSL", "Structurizr DSL")
    # Order is free: 'Container_' and 'Containers_' are disjoint prefixes
    # (position 9 is '_' vs 's'), so neither can shadow the other.
    for prefix, group in (("Component", "Components"),
                          ("Containers", "Containers"),  # multi-system Level 2
                          ("Container", "Containers"),   # singular, as in the DSL
                          ("Dynamic", "Dynamic"),
                          ("Deployment", "Deployment")):
        if key.startswith(prefix + "_") or key.startswith(prefix + "-"):
            return (group, key[len(prefix) + 1:])
        if key == prefix:
            return (group, prefix)
    return (key, key)


def _has_non_ascii(s: str) -> bool:
    return any(ord(ch) > 127 for ch in s)


def build_drilldown_map(elements, views, rendered_keys=None) -> dict:
    """Map each container's dotted alias -> the Component view keyed to it.

    Wired only where a `component` view is scoped to the container (combined
    `Components` or split `Component_<id>`). Skips non-ASCII names, empty
    aliases, and whole-model alias collisions (both sides dropped).

    `rendered_keys`, when given, is the set of raw view keys that actually
    produced an embedded panel. A view declared in the DSL but skipped at render
    (0-entity placeholder, missing SVG) is NOT wired — otherwise the injected
    `c4ShowTab('component-<id>')` would target a panel build_html never creates
    (a dangling ref). None means "no filter" (every declared component view is
    eligible), preserving the pre-render/standalone contract. Mirrors
    build_breadcrumbs' `existing_keys` gate."""
    by_id = {e.identifier: e for e in elements}

    # Whole-model alias -> [identifiers]; a collision drops every side.
    alias_owners = {}
    for e in elements:
        if _has_non_ascii(e.name):
            continue
        a = dsl_alias_for(e.identifier, elements)
        if not a:
            continue
        alias_owners.setdefault(a, []).append(e.identifier)
    collisions = {a for a, ids in alias_owners.items() if len(ids) > 1}

    dmap = {}
    for v in views:
        if v.view_type != "component" or not v.scope_identifier:
            continue
        if not v.key:
            # Keyless component view: recorded for the orphan lint, but its
            # exporter-auto-generated key is unpredictable, so we can't map a
            # drill target to it without risking a dangling c4ShowTab reference.
            continue
        if rendered_keys is not None and v.key not in rendered_keys:
            # Declared but not rendered -> wiring it would dangle. Silent:
            # find_orphaned_component_containers already reports missing views;
            # a render-skipped view is a render concern, not an authoring gap.
            continue
        el = by_id.get(v.scope_identifier)
        if el is None:
            print("  WARN: view %r scope %r not in model; drill-down skipped"
                  % (v.key, v.scope_identifier), file=sys.stderr)
            continue
        if _has_non_ascii(el.name):
            print("  WARN: non-ASCII scope %r; drill-down left inert" % el.name,
                  file=sys.stderr)
            continue
        alias = dsl_alias_for(v.scope_identifier, elements)
        if not alias:
            print("  WARN: empty alias for %r; drill-down skipped" % el.name,
                  file=sys.stderr)
            continue
        if alias in collisions:
            print("  WARN: alias collision on %r; drill-down left inert" % alias,
                  file=sys.stderr)
            continue
        dmap[alias] = v.key
    return dmap


def build_view_labels(elements, views) -> dict:
    """Map each `component` view key -> the DISPLAY NAME of the container it is
    scoped to (e.g. "Component_analytics" -> "Analytics & SAM").

    Subtabs, breadcrumbs and the drill-down aria-label otherwise fall back to the
    view-key suffix ("analytics") or the filtered SVG alias ("RESTAPILayer"),
    neither of which is the human name the author wrote in the DSL. Only
    `component` views map (that is where the suffix/name divergence bites); other
    view types keep their existing labels. Keyed by raw view key so callers can
    look up by the key they already hold."""
    by_id = {e.identifier: e for e in elements}
    labels = {}
    for v in views:
        if v.view_type != "component" or not v.scope_identifier or not v.key:
            continue  # keyless views carry no key to label (see parse_dsl_model)
        el = by_id.get(v.scope_identifier)
        if el is not None:
            labels[v.key] = el.name
    return labels


def find_orphaned_component_containers(elements, views) -> list:
    """Containers that declare `component` children but have NO `component` view
    scoped to them — so their Level-3 decomposition never renders anywhere.

    A pure completeness lint: the model stays internally consistent (the
    container is correctly left inert for drill-down); this only flags authoring
    effort that is invisible in the output. Returns
    [(container_identifier, container_name, component_count), ...] sorted by
    identifier (deterministic). Empty when every decomposed container is covered.
    """
    by_id = {e.identifier: e for e in elements}
    # container identifier -> number of direct component children
    comp_children = collections.Counter()
    for e in elements:
        if e.kind != "component" or e.parent is None:
            continue
        parent = by_id.get(e.parent)
        if parent is None or parent.kind != "container":
            continue  # defensive: only attribute components to real containers
        comp_children[e.parent] += 1

    # containers that ARE the scope of some `component` view (combined or split)
    covered = {v.scope_identifier for v in views
               if v.view_type == "component" and v.scope_identifier}

    orphans = []
    for cid, count in comp_children.items():
        if cid in covered:
            continue
        el = by_id.get(cid)
        orphans.append((cid, el.name if el is not None else cid, count))
    orphans.sort(key=lambda t: t[0])
    return orphans


def build_breadcrumbs(view_key: str, existing_keys) -> list:
    """Ordered ancestor crumbs [(ancestor_raw_key, label), ...], existing keys only.

    `existing_keys` is an iterable of raw Structurizr view-key strings that
    actually rendered (so a crumb never points to a missing panel). The caller
    maps each ancestor raw-key to its real tab-id — this never re-derives ids."""
    existing = set(existing_keys)
    group, _ = parse_view_key(view_key)
    chain = []
    if group in ("Containers", "Components"):
        chain.append(("SystemContext", "Context"))
    if group == "Components":
        chain.append(("Containers", "Containers"))
    return [(k, label) for (k, label) in chain if k in existing]


_ENTITY_OPEN_RE = re.compile(r'<g\s+class="entity"\s+data-qualified-name="([^"]*)"[^>]*>')


def view_key_to_tab_id(raw_key: str) -> str:
    """Single source of truth: Structurizr view key -> HTML tab id / data-tab.

    The result is emitted UNESCAPED into `id="..."`, `data-tab="..."`,
    `onclick="c4ShowTab('...')"` and as a JS map key, so it must be a safe
    slug. Lowercase, map '_' -> '-', then strip everything outside [a-z0-9-]
    — a hostile view key ("Component_api');alert(1)//") cannot break out of an
    attribute or the JS string. Well-formed keys (SystemContext, Component_api,
    Deployment_local_dev) are unaffected. Two distinct keys can slugify to the
    same id (non-injective); find_tab_id_collisions surfaces that.

    Degenerate keys (all non-ASCII or punctuation-only, e.g. a CJK view name)
    would otherwise slug to "" or an all-hyphen string, emitting id="" —
    getElementById("") is null, so the panel and its tab button are dead, and a
    LONE empty slug slips past find_tab_id_collisions (it only fires at 2+ keys
    per id). Fall back to a stable, distinct, alnum-anchored id derived from a
    hash of the raw key so the panel stays reachable and two different degenerate
    keys never collapse to the same dead id."""
    slug = re.sub(r"[^a-z0-9-]", "", raw_key.lower().replace("_", "-"))
    if not re.search(r"[a-z0-9]", slug):   # no alphanumeric anchor -> degenerate
        return "view-" + hashlib.sha1(raw_key.encode("utf-8")).hexdigest()[:8]
    return slug


def find_tab_id_collisions(views) -> dict:
    """Distinct view keys whose derived tab-id collides (view_key_to_tab_id is
    non-injective: 'Foo_bar' and 'Foo-bar' both -> 'foo-bar', and slugifying can
    merge more). views: (filename, tab_id, label, raw_key) 4-tuples. Returns
    {tab_id: sorted[raw_key, ...]} for every id claimed by 2+ distinct keys, so
    the caller can warn instead of silently emitting a duplicate DOM id (which
    hides the second panel). Empty when all ids are unique."""
    by_tab = {}
    for (_f, tab_id, _lbl, raw_key) in views:
        by_tab.setdefault(tab_id, set()).add(raw_key)
    return {t: sorted(keys) for t, keys in by_tab.items() if len(keys) > 1}


# Tab ids reserved for synthetic panels build_html appends after main()'s
# collision check. A user view claiming one shadows the synthetic panel.
_RESERVED_TAB_IDS = {_DSL_VIEW[1]: _DSL_VIEW[3]}  # {'dsl': 'DSL'}


def find_reserved_id_shadow(views) -> dict:
    """User views whose tab id collides with a RESERVED synthetic-panel id.

    find_tab_id_collisions set-dedups on raw_key, so it misses the case where a
    user view's raw_key is EXACTLY the reserved key (e.g. 'DSL'): the duplicate
    collapses and no collision is reported, yet build_html emits two panels with
    the same DOM id (and routes the user 'DSL' view into the source panel). This
    check is raw_key-agnostic — it flags any user tab id equal to a reserved id,
    whether reached by an identical key or by slugification ('Dsl' -> 'dsl').
    Returns {reserved_tab_id: sorted[user raw_key, ...]}; empty when none clash.
    """
    hits = {}
    for (_f, tab_id, _lbl, raw_key) in views:
        if tab_id in _RESERVED_TAB_IDS:
            hits.setdefault(tab_id, set()).add(raw_key)
    return {t: sorted(keys) for t, keys in hits.items()}


def count_entities(svg: str) -> int:
    """Count `<g class="entity">` element groups. Zero => placeholder SVG
    (Graphviz-missing, syntax-error, or empty-alias) — never trust dimensions."""
    return len(re.findall(r'<g\s+class="entity"', svg))


def wire_drilldown(svg: str, dmap: dict, labels=None):
    """Attach drill affordance to entity <g> nodes whose QN matches a mapped alias.

    Returns (wired_svg, wired_count). Boundary `class="cluster"` nodes are never
    candidates (regex keys on class="entity"). aria-label is html-escaped.
    `labels` (view_key -> display name, from build_view_labels) names the drill
    target by its DSL display name ("Analytics & SAM"); without it the aria-label
    falls back to the filtered SVG leaf alias ("Analytics" / "RESTAPILayer")."""
    labels = labels or {}
    wired = [0]

    def repl(m):
        qn = m.group(1)
        target = None
        for alias, view_key in dmap.items():
            if alias_matches_qn(qn, alias):
                target = view_key
                break
        if target is None:
            return m.group(0)
        wired[0] += 1
        tab_id = view_key_to_tab_id(target)
        leaf = labels.get(target) or qn.split(".")[-1]
        label = html_mod.escape("Drill into %s" % leaf, quote=True)
        # Splice the drill attributes BEFORE the opening tag's closing `>` so the
        # `<g class="entity"` prefix is preserved (count_entities keys on it).
        inject = (
            'role="button" tabindex="0" style="cursor:pointer" '
            "onclick=\"c4ShowTab('%s')\" "
            "onkeydown=\"if(event.key==='Enter'||event.key===' '){event.preventDefault();c4ShowTab('%s');}\" "
            'aria-label="%s"' % (tab_id, tab_id, label)
        )
        open_tag = m.group(0)
        return open_tag[:-1].rstrip() + " " + inject + ">"

    out = _ENTITY_OPEN_RE.sub(repl, svg)
    return out, wired[0]


def detect_views(svg_dir: Path) -> list:
    """Auto-detect views from SVG files present in the directory.

    First matches well-known Structurizr view names (SystemContext, Containers, etc.)
    in a stable order, then appends any remaining structurizr-*.svg files found in
    the directory (sorted alphabetically). This handles both standard and
    project-specific view names without hardcoding.

    Returns list of (filename, tab_id, label, raw_key) tuples. tab_id is a pure
    function of raw_key via view_key_to_tab_id; label comes from parse_view_key
    for unknown views (fixing the old camelCase-only label bug).
    """
    found = []
    seen_filenames: set[str] = set()

    # 1. Match well-known views in stable order
    for filename, raw_key, label in KNOWN_VIEWS:
        if (svg_dir / filename).exists():
            found.append((filename, view_key_to_tab_id(raw_key), label, raw_key))
            seen_filenames.add(filename)

    # 2. Append any remaining structurizr-*.svg files not already matched
    for svg_file in sorted(svg_dir.glob("structurizr-*.svg")):
        if svg_file.name in seen_filenames:
            continue
        raw_key = svg_file.stem.replace("structurizr-", "")
        _group, label = parse_view_key(raw_key)
        found.append((svg_file.name, view_key_to_tab_id(raw_key), label, raw_key))

    return found


def parse_view_spec(spec: str) -> tuple:
    """Parse 'key:label:filename' -> (filename, tab_id, label, raw_key).

    The `key` field is treated as the raw Structurizr view key; the tab id is
    derived from it so it stays consistent with detect_views."""
    parts = spec.split(":")
    if len(parts) != 3:
        print(f"Invalid view spec '{spec}'. Expected key:label:filename", file=sys.stderr)
        sys.exit(1)
    raw_key, label, filename = parts[0], parts[1], parts[2]
    return filename, view_key_to_tab_id(raw_key), label, raw_key


def _json_for_script(obj) -> str:
    """json.dumps hardened for embedding inside an inline <script> block.

    A view key containing "</script>" would otherwise close the block early and
    let the trailing markup execute. Escaping '<' '>' '&' as \\uXXXX keeps the
    JSON semantically identical (the browser's JSON parser un-escapes them) while
    making it impossible to terminate the script element or start a comment."""
    return (json.dumps(obj)
            .replace("<", "\\u003c")
            .replace(">", "\\u003e")
            .replace("&", "\\u0026"))


def _js_str_in_attr(s: str) -> str:
    """Escape s for a single-quoted JS string that lives inside a double-quoted
    HTML attribute: onclick="c4ShowGroup('<here>')".

    html-escaping is WRONG for this nested context — the browser HTML-decodes the
    attribute BEFORE the JS parser runs, so `&#x27;` becomes `'` and closes the
    string (XSS). Emit `\\uXXXX` for every char outside a conservative safe set;
    those survive HTML decoding unchanged and the JS engine maps them back, so the
    runtime value equals the original string (kept consistent with the
    `data-group=` attribute and the JS group maps, which the click handler
    compares against). Astral chars degrade to an inert wrong string, never a
    breakout. Known group names (Context, Components, …) are all-safe -> verbatim."""
    out = []
    for ch in s:
        if (ch.isalnum() and ord(ch) < 128) or ch in " _.-":
            out.append(ch)
        else:
            out.append("\\u%04x" % ord(ch))
    return "".join(out)


def build_html(views, svgs, dsl_escaped, system_name, dmap=None, view_labels=None):
    """Two-level grouped tabs + breadcrumbs + drill-down JS. Names html-escaped.

    views: (filename, tab_id, label, raw_key) 4-tuples. svgs: {tab_id: cleaned_svg}.
    dmap is accepted for signature stability but unused here (drill-wiring is done
    in main() before embedding). A synthetic DSL view is appended internally.
    Every c4ShowTab('<id>') argument is a real panel id — breadcrumb ancestors are
    mapped raw_key -> tab_id via `raw_to_tabid`, never re-derived.
    `view_labels` (raw view key -> display name, from build_view_labels) overrides
    the subtab and breadcrumb-current-page text so a Component view reads its
    container's DSL name ("Analytics & SAM") instead of the key suffix
    ("analytics"); absent keys keep the parse_view_key suffix."""
    view_labels = view_labels or {}
    all_views = list(views) + [_DSL_VIEW]
    raw_to_tabid = {}
    for (_, tab_id, _, raw_key) in all_views:
        raw_to_tabid[raw_key] = tab_id
    existing_raw = list(raw_to_tabid.keys())
    sysname = html_mod.escape(system_name)

    groups = {}
    for (_, tab_id, _label, raw_key) in all_views:
        group, sub = parse_view_key(raw_key)
        groups.setdefault(group, []).append((tab_id, sub, raw_key))
    ordered_groups = [g for g in GROUP_ORDER if g in groups and g not in TAIL_GROUPS] + \
                     [g for g in groups if g not in GROUP_ORDER] + \
                     [g for g in GROUP_ORDER if g in groups and g in TAIL_GROUPS]

    first_group = ordered_groups[0]
    first_tab = groups[first_group][0][0]

    tab_to_group = {}
    group_tabs = {}
    for g in ordered_groups:
        group_tabs[g] = [t for (t, _, _) in groups[g]]
        for (t, _, _) in groups[g]:
            tab_to_group[t] = g

    grp_html = ""
    for g in ordered_groups:
        active = " active" if g == first_group else ""
        ge = html_mod.escape(g, quote=True)       # HTML context: data-group=, text
        gj = _js_str_in_attr(g)                   # nested JS-string-in-attr: onclick arg
        grp_html += ('    <button class="grp%s" role="tab" aria-selected="%s" '
                     'data-group="%s" onclick="c4ShowGroup(\'%s\')">%s</button>\n'
                     % (active, "true" if g == first_group else "false",
                        ge, gj, html_mod.escape(g)))

    subrows_html = ""
    for g in ordered_groups:
        members = groups[g]
        show = " active" if g == first_group else ""
        ge = html_mod.escape(g, quote=True)
        if len(members) <= 1:
            subrows_html += '  <div class="subrow%s" data-subrow="%s"></div>\n' % (show, ge)
            continue
        subrows_html += '  <div class="subrow%s" data-subrow="%s" role="tablist">\n' % (show, ge)
        for i, (tab_id, sub, _rk) in enumerate(members):
            sa = " active" if i == 0 else ""
            sub_label = view_labels.get(_rk, sub)  # prefer container display name
            subrows_html += ('    <button class="subtab%s" role="tab" data-tab="%s" '
                             'onclick="c4ShowTab(\'%s\')">%s</button>\n'
                             % (sa, tab_id, tab_id, html_mod.escape(sub_label)))
        subrows_html += "  </div>\n"

    panels_html = ""
    for (_, tab_id, _label, raw_key) in all_views:
        active = " active" if tab_id == first_tab else ""
        crumbs = build_breadcrumbs(raw_key, existing_raw)
        bc = ""
        if crumbs:
            parts = []
            for (ck, cl) in crumbs:
                ctab = raw_to_tabid[ck]  # real panel id — never re-derived
                parts.append('<a href="#" onclick="c4ShowTab(\'%s\');return false;">%s</a>'
                             % (ctab, html_mod.escape(cl)))
            _g, sub = parse_view_key(raw_key)
            cur_label = view_labels.get(raw_key, sub)  # prefer container display name
            parts.append('<span aria-current="page">%s</span>' % html_mod.escape(cur_label))
            bc = ('    <nav class="breadcrumb" aria-label="Breadcrumb">%s</nav>\n'
                  % ' <span class="crumb-sep">&rsaquo;</span> '.join(parts))
        if raw_key == "DSL":
            body = ('    <div class="dsl-panel">\n'
                    '      <button class="copy-btn" id="copyBtn" onclick="copyDSL()">Copy</button>\n'
                    '      <pre><code id="dsl-source">%s</code></pre>\n'
                    '    </div>\n' % dsl_escaped)
        else:
            body = ('    <div class="svg-container">\n      %s\n    </div>\n' % svgs[tab_id])
        panels_html += ('  <div id="%s" class="tab-content%s" role="tabpanel" tabindex="-1">\n'
                        '%s%s  </div>\n\n' % (tab_id, active, bc, body))

    return TEMPLATE % dict(
        sysname=sysname, grp_html=grp_html, subrows_html=subrows_html,
        panels_html=panels_html,
        tab_to_group_js=_json_for_script(tab_to_group),
        group_tabs_js=_json_for_script(group_tabs),
    )


TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>%(sysname)s &mdash; C4 Architecture</title>
  <style>
    *, *::before, *::after { box-sizing: border-box; }
    body { background:#1a1a2e; color:#e0e0e0; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif; margin:0; padding:24px 32px; line-height:1.6; }
    h1 { font-size:1.8rem; font-weight:700; margin:0 0 16px 0; color:#fff; }
    code { background:#16213e; padding:2px 6px; border-radius:4px; font-family:'Cascadia Code','Fira Code','Consolas',monospace; font-size:0.9em; color:#7ec8e3; }
    .tabs { display:flex; gap:8px; margin-bottom:8px; flex-wrap:wrap; }
    .grp { background:#16213e; color:#a0a0b8; border:1px solid #2a2a4a; border-radius:24px; padding:8px 20px; font-size:0.9rem; font-family:inherit; cursor:pointer; transition:all .2s ease; }
    .grp:hover { background:#1f2b4d; color:#e0e0e0; }
    .grp.active { background:#438DD5; color:#fff; border-color:#438DD5; }
    .subrow { display:none; gap:6px; margin:0 0 16px 8px; flex-wrap:wrap; }
    .subrow.active { display:flex; }
    .subtab { background:#12182e; color:#8a8aa0; border:1px solid #24243e; border-radius:16px; padding:5px 14px; font-size:0.82rem; font-family:inherit; cursor:pointer; }
    .subtab:hover { color:#e0e0e0; }
    .subtab.active { background:#2a5a8a; color:#fff; border-color:#2a5a8a; }
    .breadcrumb { margin:0 0 12px 0; font-size:0.85rem; color:#8a8aa0; }
    .breadcrumb a { color:#7ec8e3; text-decoration:none; }
    .breadcrumb a:hover { text-decoration:underline; }
    .crumb-sep { color:#55556a; }
    .tab-content { display:none; }
    .tab-content.active { display:block; }
    .tab-content:focus { outline:2px solid #438DD5; outline-offset:4px; }
    .svg-container { background:#fff; border-radius:8px; padding:16px; overflow-x:auto; box-shadow:0 4px 16px rgba(0,0,0,.3); border:1px solid #2a2a4a; }
    .svg-container svg { display:block; margin:0 auto; height:auto; }
    /* Persistent drill-down affordance: clickable boxes carry a dashed outline +
       dashed inner border so they read as clickable WITHOUT hovering; the cue
       solidifies and brightens on hover/focus. */
    .svg-container [role="button"] { outline:2px dashed #2a5a8a; outline-offset:2px; cursor:pointer; }
    .svg-container [role="button"] rect { stroke:#08427B; stroke-width:2; stroke-dasharray:4 3; }
    .svg-container [role="button"]:hover { outline:2px solid #438DD5; }
    .svg-container [role="button"]:hover rect { stroke:#438DD5; stroke-dasharray:none; }
    .svg-container [role="button"]:focus { outline:2px solid #438DD5; }
    .dsl-panel { position:relative; background:#16213e; border-radius:8px; border:1px solid #2a2a4a; box-shadow:0 4px 16px rgba(0,0,0,.3); overflow:hidden; }
    .dsl-panel pre { margin:0; padding:20px; overflow-x:auto; font-family:'Cascadia Code','Fira Code','Consolas',monospace; font-size:0.85rem; line-height:1.6; color:#c8d0e0; tab-size:4; }
    .dsl-panel code { background:none; padding:0; border-radius:0; color:inherit; font-size:inherit; }
    .copy-btn { position:absolute; top:12px; right:12px; background:#2a2a4a; color:#a0a0b8; border:1px solid #3a3a5a; border-radius:6px; padding:6px 14px; font-size:0.8rem; font-family:inherit; cursor:pointer; z-index:10; }
    .copy-btn:hover { background:#3a3a5a; color:#e0e0e0; }
    .copy-btn.copied { background:#2e7d32; color:#fff; border-color:#2e7d32; }
    @media (max-width:600px){ body{padding:16px;} h1{font-size:1.4rem;} .grp{padding:6px 14px; font-size:0.8rem;} }
  </style>
</head>
<body>
  <h1>%(sysname)s &mdash; C4 Architecture</h1>
  <div class="tabs" role="tablist">
%(grp_html)s  </div>
%(subrows_html)s
%(panels_html)s
  <script>
    var C4_TAB_GROUP = %(tab_to_group_js)s;
    var C4_GROUP_TABS = %(group_tabs_js)s;
    function c4ShowGroup(g) {
      var tabs = C4_GROUP_TABS[g];
      if (tabs && tabs.length) { c4ShowTab(tabs[0]); }
    }
    function c4ShowTab(tabId) {
      var g = C4_TAB_GROUP[tabId];
      document.querySelectorAll('.tab-content').forEach(function(c){ c.classList.remove('active'); });
      document.querySelectorAll('.grp').forEach(function(b){ b.classList.remove('active'); b.setAttribute('aria-selected','false'); });
      document.querySelectorAll('.subrow').forEach(function(s){ s.classList.remove('active'); });
      document.querySelectorAll('.subtab').forEach(function(b){ b.classList.remove('active'); });
      var panel = document.getElementById(tabId);
      if (panel) { panel.classList.add('active'); }
      var grpBtn = document.querySelector('.grp[data-group="' + g + '"]');
      if (grpBtn) { grpBtn.classList.add('active'); grpBtn.setAttribute('aria-selected','true'); }
      var sub = document.querySelector('.subrow[data-subrow="' + g + '"]');
      if (sub) { sub.classList.add('active'); }
      var subBtn = document.querySelector('.subtab[data-tab="' + tabId + '"]');
      if (subBtn) { subBtn.classList.add('active'); }
      if (panel) { panel.focus(); }
    }
    function copyDSL() {
      var dslText = document.getElementById('dsl-source').textContent;
      var btn = document.getElementById('copyBtn');
      function done(){ btn.textContent='Copied!'; btn.classList.add('copied'); setTimeout(function(){ btn.textContent='Copy'; btn.classList.remove('copied'); },2000); }
      if (navigator.clipboard && navigator.clipboard.writeText) { navigator.clipboard.writeText(dslText).then(done); }
      else { var ta=document.createElement('textarea'); ta.value=dslText; ta.style.position='fixed'; ta.style.opacity='0'; document.body.appendChild(ta); ta.select(); document.execCommand('copy'); document.body.removeChild(ta); done(); }
    }
  </script>
</body>
</html>
"""


def main() -> None:
    parser = argparse.ArgumentParser(description="Assemble C4 architecture.html from rendered SVGs")
    parser.add_argument("project_dir", help="Project root directory")
    parser.add_argument("--dsl-path", help="Path to architecture.dsl (default: auto-detect)")
    parser.add_argument("--output", help="Path to write architecture.html (default: same dir as DSL)")
    parser.add_argument("--svg-dir", help="Directory containing rendered SVGs (default: auto-detect temp dir)")
    parser.add_argument("--views", nargs="*", help="View specs as key:label:filename (default: auto-detect)")
    parser.add_argument("--system-name", help="System name for HTML title (default: extracted from DSL)")
    parser.add_argument("--inject-wrap-width", metavar="PUML_DIR",
                        help="Pre-render mode: inject `skinparam wrapWidth` into every "
                             "*.puml in PUML_DIR (after the last C4 include) and exit. "
                             "Run between structurizr export and plantuml render.")
    parser.add_argument("--wrap-width", type=int, default=BOX_WRAP_WIDTH_PX,
                        help="Pixel wrap width to inject (default: %d)" % BOX_WRAP_WIDTH_PX)
    args = parser.parse_args()

    if args.inject_wrap_width:
        puml_dir = Path(args.inject_wrap_width)
        if not puml_dir.exists():
            print("PUML dir not found: %s" % puml_dir, file=sys.stderr)
            sys.exit(1)
        pumls = sorted(puml_dir.glob("*.puml"))
        if not pumls:
            print("No .puml files in %s" % puml_dir, file=sys.stderr)
            sys.exit(1)
        for p in pumls:
            text = p.read_text(encoding="utf-8")
            p.write_text(inject_wrap_width(text, args.wrap_width), encoding="utf-8")
            print("  wrapWidth %d injected: %s" % (args.wrap_width, p.name))
        print("Injected wrapWidth into %d .puml file(s)." % len(pumls))
        return

    project_dir = Path(args.project_dir)

    # Auto-detect DSL path: try root first, then docs/c4/
    if args.dsl_path:
        dsl_path = Path(args.dsl_path)
    elif (project_dir / "architecture.dsl").exists():
        dsl_path = project_dir / "architecture.dsl"
    elif (project_dir / "docs" / "c4" / "architecture.dsl").exists():
        dsl_path = project_dir / "docs" / "c4" / "architecture.dsl"
    else:
        print("DSL file not found. Searched:", file=sys.stderr)
        print(f"  {project_dir / 'architecture.dsl'}", file=sys.stderr)
        print(f"  {project_dir / 'docs' / 'c4' / 'architecture.dsl'}", file=sys.stderr)
        print("Use --dsl-path to specify the location.", file=sys.stderr)
        sys.exit(1)

    # Determine SVG directory
    if args.svg_dir:
        svg_dir = Path(args.svg_dir)
    else:
        svg_dir = Path(tempfile.gettempdir()) / "c4-render"

    if not svg_dir.exists():
        print(f"SVG directory not found: {svg_dir}", file=sys.stderr)
        sys.exit(1)

    # Read DSL and extract system name
    dsl_source = dsl_path.read_text(encoding="utf-8")
    if args.system_name:
        system_name = args.system_name
    else:
        match = re.search(r'workspace\s+"([^"]+)"', dsl_source)
        system_name = match.group(1) if match else "System"

    # Determine views
    if args.views:
        views = [parse_view_spec(v) for v in args.views]
    else:
        views = detect_views(svg_dir)

    if not views:
        print(f"No SVG files found in {svg_dir}", file=sys.stderr)
        sys.exit(1)

    print(f"System: {system_name}")
    print(f"SVG dir: {svg_dir}")
    print(f"Views: {len(views)}")
    print()

    # Read, clean, and verify SVGs
    print("Cleaning SVGs:")
    svgs: dict[str, str] = {}
    for filename, key, label, raw_key in views:
        svg_path = svg_dir / filename
        if not svg_path.exists():
            print(f"  SKIP: {filename} (not found)", file=sys.stderr)
            continue
        raw = svg_path.read_text(encoding="utf-8")
        cleaned = clean_svg(raw)
        verify_clean("%s (%s)" % (key, filename), cleaned)
        n_entities = count_entities(cleaned)
        if n_entities == 0:
            print("  FAIL: %s has 0 <g class=\"entity\"> nodes — this is a placeholder "
                  "SVG (Graphviz missing, syntax error, or empty alias), not a diagram. "
                  "Check the render step (see SKILL.md: Graphviz Not Found)." % filename,
                  file=sys.stderr)
            sys.exit(1)
        print("  OK: %s has %d element node(s)" % (filename, n_entities))
        svgs[key] = cleaned

    # Filter views to only those with successfully-embedded SVGs (4-tuples now).
    views = [(f, k, lbl, rk) for (f, k, lbl, rk) in views if k in svgs]
    if not views:
        print("No valid SVGs to embed!", file=sys.stderr)
        sys.exit(1)

    # Detect tab-id collisions among rendered views (non-fatal): two distinct
    # view keys collapsing to one DOM id would hide the second panel. Include the
    # synthetic DSL panel (build_html appends it) so a user key slugifying to the
    # reserved 'dsl' id is caught too — otherwise the copyable DSL source panel is
    # silently shadowed.
    collisions = find_tab_id_collisions(views + [_DSL_VIEW])
    for tab_id, raw_keys in sorted(collisions.items()):
        print("  WARN: view keys %s all map to tab id %r — only the last panel "
              "is reachable; rename so keys differ after lowercasing/slugifying."
              % (", ".join(repr(k) for k in raw_keys), tab_id), file=sys.stderr)

    # Separately flag a user view that claims a RESERVED synthetic-panel id (the
    # DSL source panel's 'dsl'). find_tab_id_collisions set-dedups on raw_key, so
    # an EXACT 'DSL' key would collapse and slip past the check above while still
    # shadowing the synthetic panel — this check is raw_key-agnostic.
    for tab_id, raw_keys in sorted(find_reserved_id_shadow(views).items()):
        print("  WARN: view key(s) %s use the reserved tab id %r (the synthetic "
              "%s panel) — the built-in panel is shadowed; rename the view."
              % (", ".join(repr(k) for k in raw_keys), tab_id,
                 _RESERVED_TAB_IDS[tab_id]), file=sys.stderr)

    # Build the drill-down map from the DSL model and wire matching SVG nodes.
    # Only views that actually rendered a panel are eligible for wiring, so an
    # injected c4ShowTab target can never dangle (Finding: dangling drill ref).
    rendered_keys = {rk for (_f, _k, _lbl, rk) in views}
    try:
        elements, view_decls = parse_dsl_model(dsl_source)
        dmap = build_drilldown_map(elements, view_decls, rendered_keys=rendered_keys)
        orphans = find_orphaned_component_containers(elements, view_decls)
        view_labels = build_view_labels(elements, view_decls)
    except Exception as exc:  # parsing must never crash assembly — degrade to no drill-down
        print("  WARN: DSL model parse failed (%s); drill-down disabled" % exc, file=sys.stderr)
        dmap = {}
        orphans = []
        view_labels = {}

    # Completeness lint (non-fatal): container decomposed but never surfaced.
    if orphans:
        print("Coverage lint: %d container(s) declare components but have no "
              "component view — their Level-3 decomposition never renders:"
              % len(orphans), file=sys.stderr)
        for cid, name, count in orphans:
            print("  WARN: container %r (%s) has %d component(s) but no "
                  "`component %s \"Component_%s\"` view."
                  % (name, cid, count, cid, cid), file=sys.stderr)
    if dmap:
        total_wired = 0
        for _f, key, _lbl, _rk in views:
            svgs[key], n = wire_drilldown(svgs[key], dmap, labels=view_labels)
            total_wired += n
        print("Drill-down: wired %d node(s) across %d view(s)." % (total_wired, len(views)))
    else:
        print("Drill-down: no container has a deeper Component view; none wired.")

    # Build and write HTML
    dsl_escaped = html_mod.escape(dsl_source)
    page = build_html(views, svgs, dsl_escaped, system_name, view_labels=view_labels)

    if args.output:
        out_path = Path(args.output)
    else:
        out_path = dsl_path.parent / "architecture.html"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(page, encoding="utf-8")

    print(f"\nWritten {len(page):,} chars to {out_path}")

    # Final verification on the output
    print("\nFinal HTML verification:")
    for pattern, desc in [('class="title"', "title group"), ("<?plantuml", "processing instruction")]:
        if pattern in page:
            # Check if it's only in the DSL panel (escaped)
            escaped = html_mod.escape(pattern)
            outside_dsl = page.count(pattern) - page.count(escaped)
            if outside_dsl > 0:
                print(f"  FAIL: {outside_dsl} unescaped {desc} found in output!", file=sys.stderr)
                sys.exit(1)
        print(f"  OK: {desc}")

    print("\nDone.")


if __name__ == "__main__":
    main()
