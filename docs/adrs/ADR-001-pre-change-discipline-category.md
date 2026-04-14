# ADR-001: Add pre-change discipline category to the plugin

| Field | Value |
|---|---|
| **Date** | 2026-04-14 |
| **Status** | Accepted |
| **Deciders** | Karsten S. Nielsen |

## Context

Before v1.16.0, mad-scientist-skills contained eight skills organised in three implicit categories:

- **Retrospective audits** (six skills): `architecture-audit`, `cognitive-interface-audit`, `documentation-audit`, `observability-audit`, `optimization-audit`, `security-audit`. Each scans existing code or infrastructure and produces a findings report.
- **Pre-commit review gate** (one skill): `final-review`. Runs after code exists but before commit, reviewing the whole change surface.
- **Diagram generator** (one skill): `c4`. Renders Structurizr DSL to interactive HTML.

The plugin's thematic identity was "disciplined quality checks for code that exists." All six audit skills triggered on "audit this codebase" or equivalent retrospective prompts. `final-review` was the closest to "gate before commit," but it still operated on code that already existed.

A discipline gap became visible during work on perf-sensitive functions in consumer projects (notably luxury-lakehouse): benchmarked code was being modified without first capturing a baseline measurement. Regressions were caught only retrospectively — via `optimization-audit` or post-deployment profiling — when the only remediation was to revert or re-optimise. No skill enforced "capture the baseline BEFORE you change the function." The operator had to remember to do this manually, and the discipline was skipped often enough to matter.

The forcing function: consumer projects have the infrastructure (pytest-benchmark wrappers, baselines files, performance budgets in CLAUDE.md) but no discipline-skill fires to gate changes against those baselines. The infrastructure was in place; the trigger was missing.

## Decision

Extend mad-scientist-skills from "retrospective audits + reviews" to "pre-change gates + retrospective audits + reviews" by adding `measure-before-optimize` as a peer skill to `optimization-audit` — pre-change vs retrospective. The two skills are designed to be invoked independently, with distinct trigger descriptions that prevent skill-selection collision.

## Alternatives considered

| Option | Pros | Cons | Why rejected |
|---|---|---|---|
| A. Mode flag on `optimization-audit` (`--pre-change`) | Zero new skill files; keeps plugin inventory at 8 skills; maintains single-category identity | Mode flags are invisible in skill descriptions; the Skill tool matches on description strings, not flags; an audit skill with a pre-change mode is semantically confusing (the word "audit" implies retrospective scope) | Low discoverability; semantic mismatch between "audit" framing and pre-change timing |
| B. No new skill; document the practice in CONTRIBUTING.md only | Zero code/config changes; plugin identity remains pure audits | Documentation without a skill trigger does not fire; contributors and Claude sessions would continue skipping the discipline; the problem the documentation describes is exactly the problem we already have (an unenforced convention) | Fails to address the discipline gap; documentation alone cannot substitute for a skill-level trigger |
| C. Add `measure-before-optimize` as a standalone peer skill (chosen) | Distinct trigger, distinct scope, distinct output; discoverable via skill selection; establishes a reusable template for future peer-skill pairs; preserves `optimization-audit`'s retrospective scope | Plugin identity now covers two categories (pre-change + retrospective); contributors need to understand both patterns when proposing new skills | — |

## Consequences

### Positive

- The discipline gap is closed: benchmarked functions cannot be modified in a disciplined workflow without first capturing a baseline. The skill's frontmatter description triggers when the user says "optimize X", "speed up Y", or "this function is slow", and when the change target has a `pytest-benchmark` wrapper or appears in a baselines file.
- Establishes a naming template for future peer-skill pairs: `<action>-before-<phase>` paired with `<phase>-audit`. Potential future additions include `scan-before-ship` (pre-deploy security scan paired with `security-audit`) or `review-before-merge` (pre-merge cognitive review paired with `cognitive-interface-audit`).
- The plugin's thematic identity broadens coherently to "disciplined quality checks, pre- and post-change." Both ends of the change lifecycle are now covered by dedicated skills.
- Operators and AI agents can now exercise the full perf lifecycle in a single workflow: `measure-before-optimize` (baseline) → code change → `optimization-audit` (retrospective sweep for any regressions the baseline missed).

### Negative

- The plugin no longer has a single thematic category. Future contributors need to understand both retrospective and pre-change patterns when deciding where a new skill belongs.
- Documentation surface grows on every release: README.md, CHANGELOG.md, architecture.dsl, marketplace.json, and plugin.json all need updates whenever a new skill is added, regardless of category. The category split adds a second dimension contributors must consider when proposing skills.
- The `optimization-audit` skill's identity is mildly diluted: it is now "the retrospective performance audit" rather than "the performance skill." Its description was updated in v1.16.0 to frame it as the retrospective peer of `measure-before-optimize`.

### Neutral

- v1.16.0 minor version bump required per semver (new backward-compatible feature).
- No changes to any existing skill's workflow — the peer relationship is additive.
- The new skill has no academic methodology to cite in NOTICE.md; it is operational tooling built on `pytest-benchmark`.

## Project Guideline Amendment

`CONTRIBUTING.md` is amended to describe the two skill categories (retrospective audits and pre-change gates) and when to pick each. A new "Skill Categories" section lists both categories with examples, and a new "Architectural Decision Records" section documents the ADR process and template location. Contributors proposing new skills are now expected to declare which category the skill belongs to as part of their PR description.

## Related

- **Plugin files:**
  - `plugins/mad-scientist-skills/skills/measure-before-optimize/SKILL.md` — the new skill introduced in v1.16.0
  - `plugins/mad-scientist-skills/skills/optimization-audit/SKILL.md` — the retrospective peer skill
  - `plugins/mad-scientist-skills/skills/final-review/SKILL.md` — Phase 2.5 "Architectural Decision Review" surfaced this decision during the v1.16.0 final review
- **Changelog:** `CHANGELOG.md` entry for `[1.16.0] - 2026-04-14`
- **Template:** `docs/adrs/ADR-TEMPLATE.md`
- **External references:** none — the skill has no academic methodology; it wraps `pytest-benchmark` as operational tooling

## Notes

The decision to document this as ADR-001 was itself surfaced by the new Phase 2.5 "Architectural Decision Review" sub-phase of `final-review`, added in the same release. Phase 2.5's criterion — "Is this documented in an ADR?" — flagged the pre-change category shift during final-review on the v1.16.0 change surface, prompting the drafting of this ADR inline. This is an intentional feedback loop: the plugin's own quality gate catches its own philosophical shifts, and ADR-001 is the first instance of that loop closing.

The lack of a prior `docs/adrs/` directory in this repo meant that establishing the ADR practice was part of this decision. `ADR-TEMPLATE.md` was ported from the luxury-lakehouse project's template (which itself was created in the same workflow cycle), generalised by renaming "CLAUDE.md Amendment" to "Project Guideline Amendment" so the template is reusable across repos that do not have a project-level `CLAUDE.md` file.
