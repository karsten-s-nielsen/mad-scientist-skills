# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

[Unreleased]: https://github.com/karsten-s-nielsen/mad-scientist-skills/compare/v1.12.0...HEAD
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
