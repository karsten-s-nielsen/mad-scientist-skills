# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

[Unreleased]: https://github.com/karsten-s-nielsen/mad-scientist-skills/compare/v1.20.0...HEAD
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
