# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

[Unreleased]: https://github.com/karsten-s-nielsen/mad-scientist-skills/compare/v1.16.0...HEAD
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
