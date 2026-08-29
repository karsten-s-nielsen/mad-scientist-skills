# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.25.0] - 2026-08-29

### Added

- **`unbiased-review`** — Hard rule 8: scope belongs to the human, so an unapproved deferral, TODO, follow-up, or quality reduction is a **finding**, never something the reviewer blesses. Phase 0 now requires establishing the bar from the actual approved spec/plan (including uncommitted/untracked docs in the working tree), not the author's paraphrase; `APPROVE WITH FOLLOW-UPS` can no longer absorb an unapproved deferral; and a "Red flags" section names the rationalizations that precede signing off on an unapproved cut.
- **`unbiased-review`** (`plan-review` / `spec-review`) — a commit-cadence check that **blocks** a plan or spec prescribing micro-commits (per-step / "commit often" / "~N small commits"): each commit must be a fully-tested, coherent rollback target, and a stream of half-tested commits is a `BLOCKING` finding.
- **`unbiased-review`** (`plan-review`) — a branch-strategy check that flags a plan proposing git worktrees (a banned workflow here) or fanning work across multiple branches without a stated reason; a single named feature branch clears silently.
- **`final-review`** — a **Release Hygiene** phase (Phase 3.5): version bump done the repo's own way (single-source first, else the bump script — never hand-editing its files — else every declaring file, always verified) plus TODO/backlog maintenance at release (top summary replaced with no history; completed items removed entirely). Adds a "no unapproved deferrals" rule.
- **Version-consistency test** — `tests/test_version_consistency.py` asserts the version agrees across `plugin.json`, `marketplace.json`, and the README badge (and that the two manifest descriptions stay byte-identical), so a partial version bump fails CI instead of merging silently.

## [1.24.0] - 2026-08-28

### Added

- **`unbiased-review`** — A tenth skill: non-author review of an artifact (spec, plan, or implementation) produced by another session. Verifies the artifact's claims against the actual repo, grades TDD and hexagonal discipline, reproduces empirical claims in an isolated scratch clone, and reports severity-ranked findings with stable IDs — deliberately **without** writing the fix, so the author still defends their own work. Peer to `final-review` (that gates your own work pre-commit; this reviews someone else's), with interoperable severities. Generalized from an InterSystems-specific origin to a Python/JS-centric default. First skill in the plugin to ship `commands/` (four deterministic entry points: `/review-spec`, `/review-plan`, `/review-impl`, `/re-review`) and a `references/` subdirectory.

### Changed

- `CONTRIBUTING.md` documents two new optional skill-layout patterns — a `references/` subdirectory and a plugin-level `commands/` directory — and records `unbiased-review` alongside `final-review` as a review gate.

## [1.23.0] - 2026-08-13

### Added

- **`c4`** — Generated pages are **~35% smaller**, pixel-for-pixel identical. PlantUML positions and justifies every *word* individually, emitting one `<text>` element per word with the full font stack repeated inline; on a real 11-view page that was 5,227 `<text>` elements re-declaring the same 17 attribute combinations, and `<text>` markup ran to ~70% of the file. Two passes remove the repetition. `clean_svg` now drops `lengthAdjust="spacing"` — `spacing` *is* the SVG initial value, so the attribute is pure redundancy on every element (~12% of a page); it is matched on the value, never blanket-stripped, so a genuine `lengthAdjust="spacingAndGlyphs"` survives. `hoist_text_styles` then collects the CSS-inheritable presentation attributes (`fill`, `font-family`, `font-size`, `font-style`, `font-weight`, …) into generated `.c4tN` classes appended to the page's own `<style>` block, leaving the genuinely per-element `x`/`y`/`textLength` inline. Measured on two real projects: 1,027,169 → 640,281 B and 1,156,747 → 736,461 B. Verified by rendering before and after in a headless browser — **zero differing pixels** across 28.8M sampled pixels per page — and by a structural check that every one of 11,105 `<text>` elements resolves to the same computed style, geometry, and text content. The hoist deliberately runs **document-wide rather than inside `clean_svg`**: every SVG is embedded in one HTML document, so `.c4tN` names share a single namespace and per-SVG numbering would make the same class mean different things in different panels. `lengthAdjust` is dropped rather than hoisted because it is not a CSS property in SVG 1.1 and is not inherited from a parent `<g>` either. The saving is in raw bytes — what matters for a file opened from disk; compressed, the same change is worth ~6%, so repo size does not fall proportionally. Because the pass rewrites start tags, it checks its own work: angle-bracket counts must be unchanged per SVG, and a violation **degrades to the un-hoisted SVGs** rather than aborting — a pass whose only purpose is size should cost the size win, never the diagram. That check stands in for re-running `verify_clean` on the final bytes, which is not possible here: `wire_drilldown` has by then injected the `onclick`/`onkeydown` handlers that make boxes clickable, and `verify_clean` rejects `on*=` handlers by design, so re-verifying post-wiring would abort every build that has drill-down.
- **`c4`** — `MAX_BOX_DESCR_CHARS` is acted on too, closing the same gap one level down. The 200-character description cap was documented as an authoring rule that nothing measured, and it had drifted exactly as its sibling did: a scan of **18 real workspaces found 14 descriptions over the cap, the worst at 664 characters** — 3x — including **three in this plugin's own diagram**, now trimmed. `parse_dsl_model` learned to capture the description (the second positional quoted token, stopping there so a technology string is never measured instead), and `find_overlong_descriptions` reports each breach worst-first as a non-fatal `WARN`. `Element` gained a trailing `description` field with a default, so its existing four-positional construction and attribute access are unchanged. An overlong description never broke a render; it inflated one box until the diagram stopped being readable, which is the kind of gradual decay no single change gets blamed for.
- **`c4`** — `MAX_ELEMENTS_PER_VIEW` is finally acted on. The constant has always been annotated "not tool-enforced", and `count_entities` already computed exactly the number needed, so nothing ever surfaced a breach — a view was found that had drifted to **41 element boxes** against a guideline of 15, purely because no output mentioned it. Assembly now prints a non-fatal `WARN` naming the view, its count, and the guideline. Advisory rather than fatal, because a legitimately flat system can exceed 15.

### Fixed

- **`c4`** — An explicit `--views` label is now honoured. `build_html` unpacked the label out of every view tuple and then never used it, resolving sub-tab text through `parse_view_key` instead, so a label passed on the command line was silently discarded for **every** view type — broader than the reported symptom of container-scoped slices rendering as raw CamelCase key suffixes (`GradientSports`, `SkillCornerRestricted`). Labels now resolve explicit `--views` → DSL container display name → key suffix. The precedence matters in that order: auto-detection synthesizes its label *from* the view key, so letting any label win unconditionally would have regressed Component tabs from `Analytics & SAM` back to the bare suffix `analytics` — a regression guarded by test.
- **`c4`** — Tab order follows the DSL instead of the alphabet. `detect_views` matched the five well-known views in a fixed order and then appended everything else **sorted by filename**, so a project with bespoke views got its tab row alphabetised regardless of how the author sequenced the `views` block — a deliberately ordered set of split views read as `Alpha, Mango, Zebra`. Project-specific views are now ordered by where their key appears in the DSL, with filename order as the tiebreaker for keys the DSL does not declare (and for the whole set when the DSL fails to parse), so the result stays deterministic. Note the previous behaviour was *stable*, not random — identical inputs always produced identical output; what it lost was authoring intent. Implementing this moved the `parse_dsl_model` call earlier in `main()` so one parse now feeds view ordering, drill-down, both coverage lints, and labels. The "parsing must never crash assembly" contract is preserved in full, as **two** guards rather than one: the up-front parse degrades to an empty model, and the four consumers that walk that model keep their own guard degrading to no drill-down, no lints, and no DSL-derived labels. Splitting them matters — the original single `try` covered all five calls, and hoisting only the parse out of it would have left a *successful* parse of a well-formed-but-unusual model able to abort the whole assembly through a consumer, where before it produced a working diagram.

- **`c4`** — The final HTML verification actually verifies the bytes that ship. It scanned the assembled page for two patterns (`class="title"`, `<?plantuml`) and, for each, computed `page.count(raw) - page.count(html_escape(raw))` — but the raw and escaped forms are **disjoint strings**, so the raw count never included an escaped occurrence and the subtraction could only ever remove hits that were already excluded. The net effect was a false negative: **each harmless escaped mention in the DSL source panel cancelled one genuine unescaped violation in an embedded SVG**. A workspace whose DSL merely discussed `class="title"` silently disarmed the check. `verify_embedded_svgs` replaces it and closes the wider gap the two-pattern scope left: it re-checks each embedded `<svg>` region **in the form it is embedded** — after drill-down wiring and text-style hoisting, the two stages that run past `verify_clean` — for title elements and groups, processing instructions, `<script>`, `<foreignObject>`, active-scheme hrefs (normalized, so `jav&#x61;script:` cannot slip through), and event handlers. Handlers are matched against an allowlist of exactly what `wire_drilldown` injects (`onclick="c4ShowTab(…"`, `onkeydown="if(event.key===…"`); anything else — including a correctly-named `onclick` carrying a foreign payload, an unquoted handler, or a `/`-separated `<rect/onload=…>` — aborts the build. It is scoped to the SVG regions rather than the whole page because the page's own chrome legitimately contains a head `<title>` and an inline `<script>` runtime, and a permanently-red check teaches the reader to ignore it. Validated against four real committed pages: 36 SVGs and 24 genuinely injected handlers, all accepted.

### Changed

- **`c4`** — SKILL.md's description no longer implies Graphviz must be on `PATH`. It said "Requires Java 21+ and Graphviz (dot)", which reads as a `which dot` check; PlantUML resolves `dot` through its own search paths, so an installed Graphviz that is absent from `PATH` works fine. A reader acting on the old wording called a working toolchain "blocked". The description now points at `plantuml.jar -testdot` as the only valid probe, matching what the body of SKILL.md already said. Graphviz remains a genuine hard requirement — PlantUML does **not** bundle it and does not fall back.
- **`c4`** — SKILL.md documents how to check whether an element actually rendered, after three separate false results cost real time: the DSL panel embeds the whole `.dsl` source so any name greps positive; `wrapWidth` splits a label across one `<text>` per word so `"StatsBomb Orchestrator"` matches nothing on a page that renders it correctly; and collapsed text matches descriptions as well as labels. The per-panel `data-qualified-name` roster is the authoritative list. Also documents that export and render each exceed 30 s on Windows, where a harness that kills a call at that threshold looks exactly like a toolchain failure.

## [1.22.0] - 2026-08-11

### Added

- **`c4`** — Coverage lint extended one level up: `find_orphaned_container_systems` flags any **software system that declares containers but has no `container` view scoped to it**, so an entire subsystem can no longer be modeled and rendered nowhere. The existing lint only ever covered the level below (a container whose *components* never render), and the missing mirror is the more damaging of the two — a missing component view hides one container's internals, a missing container view hides a whole subsystem, and nothing else in the pipeline complains: the DSL is valid, the export succeeds, and the elements still appear in the DSL panel. Found in a real 15-system workspace where two systems held **10 containers between them that rendered in no diagram**, six of them for months. Prints `WARN: software system '<name>' (<id>) has N container(s) but no container <id> "Containers_<id>" view.` and stays non-fatal, matching the Level-3 lint. Coverage is judged **only** on a `container` view scoped to that system: `include <containerId>` inside another system's container view does not count, because a container view may only hold containers of its own scope, so the exporter drops the foreign include and the element still renders nowhere.

### Fixed

- **`c4`** — `parse_dsl_model` no longer reads comments as source. `_tokenize_dsl` had no comment handling at all, which let a comment do two things it should not: a **commented-out view still counted as coverage** in both lints — the exact bypass someone reaches for when temporarily disabling a view — and an **unbalanced `{` inside a comment shifted brace depth**, re-parenting every element after it. Both were observed against a real workspace, where prose in a `#` comment (`"...had no container view, so..."`) also minted a phantom view declaration scoped to the identifier `view,`. `/* ... */` is now dropped anywhere outside a quoted string; `#` and `//` are dropped when they are the first non-whitespace on a line — line-start only, because mid-line `#` is a colour literal in Structurizr DSL (`background #08427B`) and stripping to end-of-line would eat it along with the styles block's braces.

### Changed

- **repo** — `.gitignore` now excludes `docs/superpowers/`, where the superpowers plugin writes its brainstorming plans and specs. That is session scratch rather than project documentation, and nothing under the path has ever been committed, so it only ever showed up as untracked noise in `git status`. Scoped to that one directory on purpose — `docs/plans/` and `docs/adrs/` are tracked project history.
- **`c4`** — SKILL.md documents the coverage lint as a two-level table (Level 2 and Level 3) with the resolution for each, notes that Level 2 is the damaging case, and adds **"do not verify coverage by grepping the output"**: PlantUML splits label text across `<text>` nodes (`CVE Review` → `>CVE<` + `>Review<`), the assembled HTML embeds the DSL source panel so a name "found" in the page may be model text rather than a rendered element, and `.puml` files carry generated aliases rather than DSL identifiers — so an identifier grep returns nothing even for elements that did render. The element name in the `.puml` is the only reliable key; the structural lint is better still.

## [1.21.2] - 2026-08-01

### Changed

- **repo** — Skill tests moved out of the shipped payload. A skill directory is copied **verbatim** on install — the install cache holds only `.claude-plugin/` and `skills/`, never repo-root files — so `c4`'s 15-file test suite at `skills/c4/tests/` was downloaded by every installer despite being developer infrastructure. Tests now live in a top-level `tests/` tree mirroring the skill path (`tests/skills/c4/`), which costs installers nothing. The `c4` skill's payload drops **239K / 22 files → 134K / 7 files** (44% of its bytes, two thirds of its files); the whole plugin **1236K / 63 files → 1131K / 48 files**. A root `conftest.py` puts each skill directory that ships an importable module on `sys.path`, replacing 12 duplicated per-file inserts. No runtime file changed — `c4_assemble.py` is untouched and plugin behaviour is byte-for-byte identical. Released as a patch even so, because the version is the install cache key (`~/.claude/plugins/cache/.../<version>/`): without a bump, an existing install keeps its copy of the tests and the payload reduction reaches nobody. See `ADR-002`.

### Added

- **ci** — New `pytest` job runs `python -m pytest tests -q` on every PR and push to `main`. CI previously ran only `pre-commit` (file hygiene, secret scanning), so the 161 `c4` tests were ungated — including the v1.21.1 behaviour fixes to `c4_assemble.py`. Verified the gate can fail, not just pass: reverting the v1.21.1 `TAIL_GROUPS` fix turns the job red. The suites import only the stdlib, so the job installs `pytest` and needs no PlantUML, Graphviz, or JRE — it gates 159 of the 161 tests, the two real-render integration tests being `skipUnless`-gated on a toolchain the runner does not have.
- **repo** — New root `pytest.ini` pins pytest's `rootdir` at the repo root. The root `conftest.py` is only loaded from `rootdir` down, and with no config file present `rootdir` is inferred from the invocation — so pinning it makes conftest discovery independent of how the suite is called rather than a property of the arguments it was given.

## [1.21.1] - 2026-07-27

### Fixed

- **`c4`** — Multi-system workspaces can now group their Level-2 diagrams. `parse_view_key`'s prefix table recognised `Component_<id>`, `Dynamic_<id>` and `Deployment_<id>` but had no entry for container views, so the only container key it understood was the bare singular `Containers`. Because Structurizr view keys must be unique across a workspace, a model with N software systems needs N distinct container-view keys — and every one of them fell through to "unknown key becomes its own group". A 15-system workspace rendered **12 top-level tabs, 8 of them container views**, each advertising an architectural level that does not exist. Added `Containers_<systemId>` and the singular `Container_<systemId>` to the prefix table (both `_` and `-` separators); the same workspace now renders **5 canonical tabs** — Context, Containers (8 sub-tabs), Dynamic, Deployment, DSL. `Container_` and `Containers_` are disjoint prefixes, so no ordering logic is needed. A side effect of correct grouping: split container panels now also receive their `Context ›` breadcrumb, which an unrecognised key never got.
- **`c4`** — The synthetic **DSL** source panel now sorts last unconditionally. Group ordering placed every `GROUP_ORDER` member ahead of every unrecognised group, and `DSL` is a `GROUP_ORDER` member — so a single bespoke view key was enough to push the DSL panel into the middle of the tab row (it rendered 4th of 12 in the workspace above). Introduced `TAIL_GROUPS` for synthetic, non-diagram panels, which sort after the unknown groups. Note that the first fix masks this one for well-formed workspaces; it is fixed on its own merits so the "synthetic panel is always last" invariant holds by construction rather than by accident of what else is in the model.

### Changed

- **`c4`** — Documented the `Containers_<systemId>` view-key convention as **required** for multi-system workspaces in the SKILL.md naming-convention block, and narrowed the former "multi-system workspaces are out of scope" note: grouping and breadcrumbs now work for them, while click-through drill-down remains single-system (a Component panel's `Containers` crumb resolves against the bare key, so it is omitted rather than dangled).

## [1.21.0] - 2026-07-23

### Added

- **`security-audit`** — New **Phase 4c: Unsafe HTML/SVG Sanitization — Regex Sanitizer Bypasses** (OWASP A03; CWE-79 / CWE-83 / CWE-116 / CWE-184). Audits hand-rolled regex "cleaners" that strip active content from HTML/SVG before embedding it (`innerHTML`, `dangerouslySetInnerHTML`, inline SVG, a generated `.html` artifact). Ships grep patterns to locate such sanitizers plus a seven-row payload matrix to test each one against: slash-separated handlers (`<svg/onload=…>`, which fires on parse with no interaction), unquoted/mixed-quote handlers, entity/control-char-obfuscated schemes (`jav&#x61;script:`, `java\tscript:`), non-`javascript:` schemes (`data:text/html`, `vbscript:`, scriptable `data:image/svg+xml`), non-recursive re-forming (`<scr<script>ipt>`), case/namespace variants, and mutation XSS. Remediation prioritizes parser-based allowlist sanitizers (DOMPurify, `nh3`, `ammonia`, `bluemonday`) over regex, with a fail-closed + browser-normalized gate as the stdlib-only fallback, honest "hardening vs sanitizing" scoping, and a CSP defense-in-depth note. Grounded in the v1.20.0 `c4` SVG-cleaner hardening (Finding 1).
- **`security-audit`** — New **Important rule** — *"Regex is not a sanitizer"*: any hand-rolled regex that cleans/strips/scrubs HTML or SVG is a denylist and will leak; prefer a parser-based allowlist sanitizer, and if a stdlib-only cleaner is unavoidable, make it fail-closed and normalize input (decode entities, strip control chars, treat `/` as an attribute separator) before matching.

### Changed

- **`c4`** — `BOX_WRAP_WIDTH_PX` default raised **150 → 200** px (C4-PlantUML's stock wrap). Rendered container/component boxes are now more square — wider, with less vertical stacking — instead of narrow and tall. Override per render with `--wrap-width N`; lower it for narrower boxes. Regenerated the repo's `architecture.html` at the new width.

## [1.20.0] - 2026-07-23

### Added

- **`c4`** — Interactive click-through drill-down between diagram levels, a breadcrumb trail, and two-level grouped tabs (with sub-tabs) in the assembled `architecture.html`, replacing the flat single-row tab bar. Container boxes whose components are decomposed carry a persistent affordance and link to their Component view.
- **`c4`** — `--inject-wrap-width` / `--wrap-width` CLI flags to control PlantUML label wrap width in the rendered diagrams.

### Fixed

- **`c4`** — Hardened SVG cleaning to strip active content (`<script>`, `<foreignObject>`, `on*=` event handlers, and `javascript:`/`vbscript:` hrefs) with a fail-closed `verify_clean` gate. The handler match is tag-anchored so benign label text (e.g. `online=true`) is never mangled or falsely aborted, while `data:image/…` icons and `#fragment` links are preserved. The gate is anchored on `[\s/]` so a slash-separated handler (`<svg/onload=…>`, which browsers execute on parse) fails closed, and dangerous-scheme hrefs are matched against a browser-normalized value (HTML entities decoded, tab/newline stripped) so `jav&#x61;script:` / `java⇥script:` obfuscation and `data:text/html` cannot slip past — with the scope documented in `clean_svg`: best-effort hardening of inert PlantUML output, not a general-purpose untrusted-SVG sanitizer.
- **`c4`** — Correctness guards in the HTML assembler: a stable fallback tab id for degenerate/empty view-key slugs, reserved-`dsl`-tab-id shadow detection (`find_reserved_id_shadow`), keyless component-view handling, orphaned-component-container lint, and tab-id collision warnings.
- **`c4`** — Escaping fixes for view keys and group names flowing into `id=`/`data-tab=`/`onclick=` and embedded JSON so a hostile view key cannot break out of an attribute, JS-string, or `<script>` context.
- **docs** — Corrected the repository slug (`karstenskyt` → `karsten-s-nielsen`) in the README CI badge and the `SECURITY.md` security-advisory link, which pointed at a non-existent repository.

## [1.19.0] - 2026-04-21

### Added

- **`optimization-audit`** — Phase 0.5 gains a **Baseline currency check** sub-phase. Documentation decays: row counts (`"~2M rows"`), timing baselines (`"~2s for 232K rows"`), memory budgets, cache hit-rate targets, and throughput figures cited in comments and ADRs silently age as the system grows. The new sub-phase enumerates every numeric figure found in Phase 0.5 into a **Baseline Currency Table** (`documented value | source | date | measured value | drift factor | staleness?`), measures each against the live value (`SELECT COUNT(*)`, recent benchmark artifact, `DESCRIBE DETAIL`, or explicit "unmeasurable" flag), and flags >2× drift as a finding. Severity is keyed to how the code depends on the number: **High** if a buffer size / `LIMIT` / batch size / algorithm choice uses it, **High–Critical** if a cache-sizing, timeout, or pool constant uses it, **Low** if only a comment or docstring references it.
- **`optimization-audit`** — Phase 12 gains a **Benchmark coverage-breadth audit** sub-phase. Existence is not coverage: a codebase can have many benchmarks and still be blind to the layer that regresses in production. The new sub-phase classifies every benchmark into one of five stack layers (**L1** pure-compute hot paths / **L2** data-layer and query / **L3** service and API / **L4** UI and end-user / **L5** pipeline and batch), produces a coverage table gated on CI integration and production-scale fixtures, and flags any layer with zero benchmarks on a user-facing path. Scoring: zero-coverage layer = Medium by default, High if SLO or incident history; benchmarks without CI gate = Medium; benchmarks on toy data = High ("100 rows passing when production is 10M is a false green"); over-represented layer while the regressing layer has zero coverage = explicit blind-spot call-out in the Phase 13 report.
- **`optimization-audit`** — two new **Important rules** at the bottom of the skill:
  - **Check that workarounds still win.** For every project-level "never do X" rule the codebase inherits (`SELECT DISTINCT`, `.toPandas()`, `iterrows()`, `df.cache()`, etc.), identify the chosen workaround (recursive CTE, `.limit().toPandas()`, `itertuples()`, Delta temp tables) and verify it is still faster than the forbidden pattern **at the current data scale**. Rules written at 100K rows can invert at 10M rows — a recursive CTE doing N inner `SELECT MIN` subqueries loses to `SELECT DISTINCT col` with a covering index once N grows large enough. When the workaround has become its own anti-pattern, flag it and recommend reverting to the previously-forbidden pattern with the missing enabling change.
  - **Parallelize for large codebases.** On repos with ≥5K source files or ≥50 modules, dispatch independent phases to parallel explorer sub-agents with explicit, non-overlapping file-set scopes. Suggested split: (a) Phase 0.5 docs + tech debt, (b) Phase 5 database/query, (c) Phases 6 + 8 cache + frontend, (d) Phase 9 pipeline + dbt, (e) Phases 0 + 2 + 3 + 4 + 7 grep-wide anti-patterns; Phases 10–12 stay in the main thread. Each agent produces a severity-tagged findings table so the main thread can merge mechanically. Single-shot `Read`+`Grep` in the main thread remains correct for small codebases (<1K files).
- **`optimization-audit`** — intro navigation block added above Phase 0 pointing operators to the two new Important Rules and the new Phase 0.5 sub-check so they are seen before the audit starts, rather than only at the bottom of a 1K-line document.

### Worked example

The three additions were all derived from the 2026-04 `luxury-lakehouse` warm-tier audit:

1. A `"~2M rows (Pitch Control)"` code comment had drifted 4–5× without the surrounding buffer-sized code being updated — the kind of "positive problem" (more data flowing correctly) that tips queries, caches, and pipelines over a latent scale cliff. The **Baseline Currency Table** would have surfaced the gap before Phase 5 started querying indexes sized for the old value.
2. A heavy `pytest-benchmark` suite concentrated at L1 pure-compute level masked an essentially zero-coverage L2 query layer that was the actual regressing surface in production. The **stack-layer coverage table** forces this blind spot to be named in Phase 13.
3. A project-level "never `SELECT DISTINCT`" rule had pushed the codebase onto a recursive-CTE workaround that inverted in performance characteristics once the underlying table grew — the forbidden pattern paired with a covering index would have been faster than the rule-compliant workaround. The **Check that workarounds still win** rule encodes this as a first-class audit obligation.

## [1.18.0] - 2026-04-16

### Added

- **`cognitive-interface-audit`** — ColorBrewer palette enforcement (two-tier, Option C):
  - **Phase 0 Anti-Pattern Scan** — new grep row for perceptually non-uniform colormaps (`jet`, `hot`, `rainbow`, `hsv`, custom `LinearSegmentedColormap` without perceptual validation). Flagged as High because non-validated colormaps create false magnitude boundaries at hue transitions that do not exist in the data.
  - **Phase 6 Data Visualization Integrity** — two new rows:
    - **Colormap provenance** — continuous, sequential, and diverging colormaps must use a scientifically validated palette: ColorBrewer (Harrower & Brewer 2003), viridis/magma/plasma/inferno (matplotlib perceptually uniform), or cividis (colorblind-optimised). Non-validated colormaps fail under colour-vision deficiency. Grep for `cmap=`/`colorscale=`/`color_continuous_scale=` against validated allowlist. High severity.
    - **Diverging colormap CVD safety** — three ColorBrewer diverging palettes (`RdYlGn`, `RdGy`, `Spectral`) fail under deuteranopia/protanopia. Safe alternatives listed. Medium severity.
  - **Phase 6 Practitioner note** — explains the two-tier colour enforcement rationale: colormaps must be from a validated palette (perceptual uniformity is non-negotiable at 256 interpolated steps); semantic constants can be custom-chosen for domain meaning but must pass programmatic CVD distinguishability check (Phase 7).
  - **Phase 7 Accessibility** — new row for semantic colour set CVD distinguishability: categorical semantic colours not drawn from a named colorblind-safe palette must pass pairwise CIEDE2000 ΔE > 20 under deuteranopia and protanopia simulation. Validates the actual perceptual property (distinguishability) rather than palette membership, allowing domain-meaningful custom colours while guaranteeing accessibility. New automated grep pattern for non-validated colormaps.
  - **Academic foundations** — added Harrower & Brewer 2003 (ColorBrewer palette design in Munsell perceptual colour space) and Olson & Brewer 1997 (empirical colorblind safety evaluation of cartographic palettes).

### Design rationale

Two-tier enforcement (Option C) was chosen over blanket ColorBrewer mandate (Option B) because:

1. ColorBrewer's science is strongest for continuous/ordered scales (27 of 35 palettes are sequential/diverging); its qualitative offering is thin (only 3 of 8 pass colorblind filter at 3+ classes, only Paired survives at 4+).
2. Semantic constants (team colours, credit categories) serve domain meaning and dark-theme contrast — forcing them into Paired/Dark2/Set2 would degrade visual design for no perceptual gain.
3. Option B degrades into exception lists ("DEFCON exempt, home/away exempt..."); Option C validates the actual property (ΔE distinguishability) programmatically, preventing decay without requiring palette membership.

## [1.17.0] - 2026-04-15

### Added

- **`architecture-audit`** — Phase 0 Anti-Pattern Scan gains three new rows for silent-exception-swallow patterns and schema drift:
  - **Silent telemetry swallow** — `except Exception: logger.warning(...)` or `except Exception: pass` in hook/callback/observer/fire-and-forget code paths. Flagged as critical data-integrity risk because warning-level logs are filtered out of standard error-log queries. Default telemetry exception handling must be raise, typed error return, or log-at-ERROR — never `logger.warning` in a fire-and-forget path.
  - **UDF empty-return on exception** — `except Exception: return pd.DataFrame(columns=...)` or `return []` inside `applyInPandas`/`mapInPandas`/`map_partitions`/Ray actors. Flagged as critical per-group data loss because distributed frameworks concatenate UDF outputs without tracking empty returns. Must propagate with group-key context (`raise RuntimeError(f"... failed for <key>={value}")`).
  - **Writer-to-target schema drift** — hardcoded `StructType`/`pydantic.BaseModel` in one file paired with `CREATE TABLE` DDL in another file without a programmatic reconciliation test. Flagged as critical because Delta `whenMatchedUpdateAll()` validates target columns at parse time and raises `DELTA_MERGE_UNRESOLVED_EXPRESSION` when the source schema is missing a target column.
- **`architecture-audit`** — Phase 4 Cross-deployment contract validation gains a new "Writer/target schema reconciliation" check requiring a test that parses target DDL and asserts equality with the in-code writer schema.
- **`architecture-audit`** — Phase 5 Data Platforms "Schema as implicit contract" row extended to explicitly cover hardcoded StructType literals paired with CREATE TABLE DDL files without reconciliation.
- **`observability-audit`** — Phase 0 Anti-Pattern Scan gains four new rows:
  - **Silent telemetry swallow** — same pattern as architecture-audit, scoped to observability concerns.
  - **UDF empty-return on exception** — same pattern as architecture-audit.
  - **Silent fallback to default value without observable signal** — `except Exception: var = default_value` patterns (hardcoded 0.5, None, False, {}) without metric/log/flag making the fallback visible.
  - **Hook/callback registration without completion assertion test** — telemetry assumed to work based on registration, not on observed output. Requires a test that exercises the hook and asserts the output lands in the target sink.
- **`observability-audit`** — practitioner note clarifying that a catch logging at WARNING level inside a fire-and-forget path is structurally equivalent to no logging at all. Audit must check not just *whether* the catch logs, but *at what level* and *through which observability channel*.

### Worked example

The three silent-swallow anti-patterns added in this release were all derived from the 2026-04-12 `luxury-lakehouse` warm-tier blocker, where:

1. A schema migration left an orphaned `task_key` column in a production Delta table.
2. The `CostEstimateHook` MERGE failed every call with `DELTA_MERGE_UNRESOLVED_EXPRESSION` at parse time.
3. Four `except Exception: logger.warning(...)` catches in the hook and its dispatcher hid the failure for 62+ hours.
4. The root cause only surfaced when a downstream dbt test was wired into the daily job and started firing.

The new anti-patterns provide grep-based early detection of this class of bug. Field-tested against a production repo during remediation; caught 55+ instances in `src/` alone.

## [1.16.0] - 2026-04-14

### Added

- **New skill: `measure-before-optimize`** — pre-change measurement gate for perf-sensitive functions. Captures a `pytest-benchmark` baseline, waits for the change, re-measures, reports delta against budget and a configurable regression threshold. Peer to `optimization-audit` — this skill is pre-change, the other is retrospective. See `plugins/mad-scientist-skills/skills/measure-before-optimize/SKILL.md`.

### Changed

- **`final-review` skill** — added Phase 2.5 "Architectural Decision Review" between Phase 2 (Code Quality Review) and Phase 3 (Documentation Review). Scans the change for decisions matching six patterns (cross-cutting dependency changes, schema ownership, platform workarounds, naming conventions, algorithm reimplementations, defense-in-depth controls) and prompts for an ADR when one is missing or stale. Updated Phase 5 verification summary checklist with an "Architectural Decisions" row.

## [1.15.0] - 2026-04-07

### Added
- **cognitive-interface-audit**: Data visualization integrity checks in Phase 6 (Visual Grounding) — bar/area chart zero-baseline enforcement, shape sizing method (area vs diameter), chart-question alignment, data colour consistency, categorical palette limits, quantitative encoding method, label overload detection, annotation sufficiency, pie chart integrity, diverging scale symmetry, editorial focus hierarchy. Grounded in Kirk's *Data Visualisation* (3rd ed., 2025), Cleveland & McGill (1984), and Mackinlay (1986)
- **cognitive-interface-audit**: Red-green data opposition and redundant data encoding checks in Phase 7 (Accessibility) for colour-deficient viewers (~5% of population). Grounded in Kirk Ch9, WCAG 1.4.1
- **cognitive-interface-audit**: Data colour association consistency check in Phase 3 (Consistency) — same colour must represent same data category across all pages
- **documentation-audit**: Limitation front-loading and error message empathy checks in Phase 3 (Linguistic Precision). Grounded in Voss's *Never Split the Difference* (Accusation Audit, Labeling, Tactical Empathy)
- **documentation-audit**: Simplify-vs-clarify decision rule in Phase 4 (Pedagogical Scaffolding) — Kirk's complicated/complex/simple taxonomy for calibrating documentation depth to audience capacity
- **documentation-audit**: Reader ownership check in Phase 4 — Voss's "That's Right" vs "You're Right" principle applied to tutorial scaffolding weight
- **documentation-audit**: Voice/tone guidance in Phase 5 (Structural Consistency) — Voss's three voice tones (positive/playful default, authoritative for warnings, assertive almost never) as tone consistency framework

## [1.14.0] - 2026-04-04

### Added
- **optimization-audit**: PyTorch / ML training anti-patterns in Phase 0 — DataLoader configuration (`num_workers=0`, `pin_memory` without workers, missing `persistent_workers`), Dataset `__getitem__` hot path (per-sample tensor allocation, `torch.tensor()` from Python lists, `.item()` in loops, Python for-loops over sequence positions), model forward pass (`register_buffer` candidates for config-dependent tensors, redundant `.to(device)` calls, per-iteration GPU transfer in eval loops). Includes audit instruction prioritizing data loading path over model optimization.

## [1.13.0] - 2026-03-31

### Added
- **architecture-audit**: New audit skill (beta) with 10-phase methodology covering architectural pattern detection (incl. framework coupling depth), dependency direction analysis, bounded context assessment (incl. cross-deployment contract validation), domain model quality (incl. data access centralization, presentation framework coupling), SOLID compliance, coupling/cohesion analysis (incl. cross-deployment duplication detection), CQRS/Event Sourcing correctness, Twelve-Factor App compliance (incl. deployment constraint inventory), API-First assessment, and architectural decision records
- **security-audit**: Secrets strategy assessment in Phase 9 — vault appropriateness heuristic, platform-native store utilization, long-lived credential inventory, rotation capability, environment separation, fallback credential hygiene
- **optimization-audit**: Anti-corruption layer and cross-context data coupling checks in Phase 9 (Data Pipeline Efficiency) with matching grep patterns
- **cognitive-interface-audit**: Ubiquitous language consistency checks in Phase 3 (Consistency & Convention) — cross-surface synonym detection, metric label-to-column alignment, glossary completeness, abbreviation consistency, term concordance table

## [1.12.1] - 2026-03-29

### Added
- README: defined "Claude Code skill" concept, badges, benefit-first skill descriptions, prerequisites (incl. Claude Code), installation verification and troubleshooting, Quick Start with sample output, glossary (12 terms), contributing section
- CHANGELOG.md (retroactive from v1.0.0 through v1.12.0)
- CONTRIBUTING.md with skill file format, commit conventions, and PR process
- SECURITY.md with vulnerability disclosure policy
- CODE_OF_CONDUCT.md (Contributor Covenant v2.1)
- Pre-audit checklists added to all cognitive-interface-audit and documentation-audit templates

### Changed
- Standardized Phase 0 naming ("Anti-Pattern Scan") across all audit skills
- Standardized Critical severity action text ("Fix immediately") across all audit skills
- Standardized "Fix as you go" boilerplate across all audit skills
- Added core questions to security-audit and observability-audit
- Added report schema convention notes to all audit SKILL.md files
- Replaced HTML arrow entities with Unicode arrows in documentation-audit and cognitive-interface-audit
- Removed "(beta)" from observability-audit H1 (retained in frontmatter metadata)
- Updated final-review severity scale to Critical/High/Medium/Low and cross-referenced all audit skills
- Renamed "Giving Back" to "Support" in README

### Fixed
- Replaced 4 "whitelist" instances with "allowlist" in security-audit (inclusive language)
- Removed 2 dead references to nonexistent `c4-plantuml` skill in c4/SKILL.md
- Replaced hardcoded structurizr.war version URL with reference to binaries page
- Fixed cognitive-interface-audit "seven threads" grouping in README (was listing 10 flat items)
- Fixed README coverage tables to match SKILL.md phase names
- Removed temporal "currently" from optimization-audit and pipeline-observability
- Added NOTICE.md back-reference to README

## [1.12.0] - 2026-03-29

### Added
- **security-audit**: ML/AI model security checks
- **security-audit**: AI regulatory compliance analysis
- **security-audit**: Cross-organisation trust boundary detection
- **security-audit**: Confidential computing patterns

## [1.11.0] - 2026-03-27

### Added
- **documentation-audit**: New audit skill with a 10-phase methodology covering structure, clarity, completeness, and maintainability

## [1.10.0] - 2026-03-27

### Added
- **optimization-audit**: Loop-invariant computation detection pattern
- **optimization-audit**: Remote container memory budget pattern

## [1.9.1] - 2026-03-27

### Fixed
- **optimization-audit**: Added DataFrame-filter-inside-loop O(n²) anti-pattern detection

## [1.9.0] - 2026-03-27

### Added
- **cognitive-interface-audit**: Inline academic citations throughout the skill
- **cognitive-interface-audit**: Extended references section

## [1.8.1] - 2026-03-27

### Fixed
- **cognitive-interface-audit**: Added report self-consistency rule to prevent contradictory findings

## [1.8.0] - 2026-03-27

### Added
- **cognitive-interface-audit**: Extraneous Information Detection (EID) checks
- **cognitive-interface-audit**: Visual encoding analysis
- **cognitive-interface-audit**: Expert blind spot detection
- **cognitive-interface-audit**: Academic attribution for cognitive principles

## [1.7.0] - 2026-03-27

### Added
- **cognitive-interface-audit**: New audit skill for evaluating user-facing interfaces against cognitive load and UX principles

## [1.6.0] - 2026-03-27

### Added
- **optimization-audit**: Ingestion no-op waste detection (identifies pipeline stages that consume resources without producing output)

## [1.5.0] - 2026-03-27

### Added
- **optimization-audit**: Expanded distributed execution patterns
- **optimization-audit**: Cloud cost analysis for distributed workloads

## [1.4.0] - 2026-03-27

### Added
- **optimization-audit**: Distributed execution detection (identifies code inadvertently running in driver/controller processes instead of workers)

> **Note on tag placement:** The v1.4.0 tag was applied to commit `9cc755c` ("fix: remove trailing blank line in algorithm-complexity.md") rather than to the feature commit `7f7f0f1` that introduced the distributed execution detection. The feature content is correct; only the tagged commit is cosmetically off.

## [1.3.1] - 2026-03-27

### Fixed
- **optimization-audit**: Enhanced anti-patterns with additional detection rules and code clean-up

## [1.3.0] - 2026-03-27

### Changed
- **optimization-audit**: Promoted from beta to GA with improved pattern coverage and reliability

## [1.2.0] - 2026-03-27

### Added
- **optimization-audit**: New audit skill (beta) for detecting performance anti-patterns, algorithmic complexity issues, and resource inefficiencies

## [1.1.0] - 2026-03-27

### Added
- **observability-audit**: New audit skill (beta) for telemetry strategy, instrumentation gaps, and observability maturity

## [1.0.0] - 2026-03-27

### Added
- **security-audit**: Initial skill for architecture-level security review
- **c4**: Skill for generating interactive C4 architecture diagrams via Structurizr DSL
- Pre-commit quality gate (`final-review` skill)
- GitHub Actions CI with `actions/checkout` and `actions/setup-python`
- `CODEOWNERS` file
- Marketplace install path for the `karsten-s-nielsen` organisation

### Fixed
- Trailing newline in `architecture.html`

[Unreleased]: https://github.com/karsten-s-nielsen/mad-scientist-skills/compare/v1.25.0...HEAD
[1.25.0]: https://github.com/karsten-s-nielsen/mad-scientist-skills/compare/v1.24.0...v1.25.0
[1.24.0]: https://github.com/karsten-s-nielsen/mad-scientist-skills/compare/v1.23.0...v1.24.0
[1.23.0]: https://github.com/karsten-s-nielsen/mad-scientist-skills/compare/v1.22.0...v1.23.0
[1.22.0]: https://github.com/karsten-s-nielsen/mad-scientist-skills/compare/v1.21.2...v1.22.0
[1.21.2]: https://github.com/karsten-s-nielsen/mad-scientist-skills/compare/v1.21.1...v1.21.2
[1.21.1]: https://github.com/karsten-s-nielsen/mad-scientist-skills/compare/v1.21.0...v1.21.1
[1.21.0]: https://github.com/karsten-s-nielsen/mad-scientist-skills/compare/v1.20.0...v1.21.0
[1.20.0]: https://github.com/karsten-s-nielsen/mad-scientist-skills/compare/v1.19.0...v1.20.0
[1.19.0]: https://github.com/karsten-s-nielsen/mad-scientist-skills/compare/v1.18.0...v1.19.0
[1.18.0]: https://github.com/karsten-s-nielsen/mad-scientist-skills/compare/v1.17.0...v1.18.0
[1.17.0]: https://github.com/karsten-s-nielsen/mad-scientist-skills/compare/v1.16.0...v1.17.0
[1.16.0]: https://github.com/karsten-s-nielsen/mad-scientist-skills/compare/v1.15.0...v1.16.0
[1.15.0]: https://github.com/karsten-s-nielsen/mad-scientist-skills/compare/v1.14.0...v1.15.0
[1.14.0]: https://github.com/karsten-s-nielsen/mad-scientist-skills/compare/v1.13.0...v1.14.0
[1.13.0]: https://github.com/karsten-s-nielsen/mad-scientist-skills/compare/v1.12.0...v1.13.0
[1.12.0]: https://github.com/karsten-s-nielsen/mad-scientist-skills/compare/v1.11.0...v1.12.0
[1.11.0]: https://github.com/karsten-s-nielsen/mad-scientist-skills/compare/v1.10.0...v1.11.0
[1.10.0]: https://github.com/karsten-s-nielsen/mad-scientist-skills/compare/v1.9.1...v1.10.0
[1.9.1]: https://github.com/karsten-s-nielsen/mad-scientist-skills/compare/v1.9.0...v1.9.1
[1.9.0]: https://github.com/karsten-s-nielsen/mad-scientist-skills/compare/v1.8.1...v1.9.0
[1.8.1]: https://github.com/karsten-s-nielsen/mad-scientist-skills/compare/v1.8.0...v1.8.1
[1.8.0]: https://github.com/karsten-s-nielsen/mad-scientist-skills/compare/v1.7.0...v1.8.0
[1.7.0]: https://github.com/karsten-s-nielsen/mad-scientist-skills/compare/v1.6.0...v1.7.0
[1.6.0]: https://github.com/karsten-s-nielsen/mad-scientist-skills/compare/v1.5.0...v1.6.0
[1.5.0]: https://github.com/karsten-s-nielsen/mad-scientist-skills/compare/v1.4.0...v1.5.0
[1.4.0]: https://github.com/karsten-s-nielsen/mad-scientist-skills/compare/v1.3.1...v1.4.0
[1.3.1]: https://github.com/karsten-s-nielsen/mad-scientist-skills/compare/v1.3.0...v1.3.1
[1.3.0]: https://github.com/karsten-s-nielsen/mad-scientist-skills/compare/v1.2.0...v1.3.0
[1.2.0]: https://github.com/karsten-s-nielsen/mad-scientist-skills/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/karsten-s-nielsen/mad-scientist-skills/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/karsten-s-nielsen/mad-scientist-skills/releases/tag/v1.0.0
