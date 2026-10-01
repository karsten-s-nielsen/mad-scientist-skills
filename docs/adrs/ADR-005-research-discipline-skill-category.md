# ADR-005: Add a working / pre-registration discipline category

| Field | Value |
|---|---|
| **Date** | 2026-10-01 |
| **Status** | Accepted |
| **Deciders** | Karsten S. Nielsen |

## Context

Before v1.28.0, mad-scientist-skills contained ten skills. `CONTRIBUTING.md` organises them into two
categories plus a review gate:

- **Retrospective audit** (six skills): `architecture-audit`, `cognitive-interface-audit`,
  `documentation-audit`, `observability-audit`, `optimization-audit`, `security-audit`. Each scans code or
  infrastructure that already exists and produces a prioritised findings report.
- **Pre-change gate** (one skill): `measure-before-optimize`. Fires before a code change, captures a baseline,
  and reports a before/after delta.
- **Review gate** (two skills): `final-review`, `unbiased-review`. Fire after a change, before commit —
  producing a structured checklist or severity-ranked findings on an artifact.

(`c4` is a diagram generator and sits outside this three-row taxonomy.)

The forcing function: a portable "how to research" discipline — the E1–E7 metric-design anti-patterns, the
validity ladder, a data-quality preflight, and a multi-pass review protocol — was being folded into the plugin
as the `research-discipline` skill (converted from an external `RESEARCH-DISCIPLINE.md`). It does not fit any
existing category. It is loaded *while* a session designs, validates, or pre-registers a metric; it produces
no findings report, no before/after delta, and no review verdict. It is a checklist you keep with the work, a
pre-registration gate — a kind the taxonomy does not yet name. CONTRIBUTING lists "introducing a new skill
category" as an ADR trigger, so the classification is recorded here rather than decided silently.

## Decision

Add a fourth category — **working / pre-registration discipline** — with `research-discipline` as its first
member: a skill loaded while doing the work (not after it) that pre-registers the standards a piece of
research must meet, and produces a kept checklist rather than a findings report.

## Alternatives considered

| Option | Pros | Cons | Why rejected |
|---|---|---|---|
| A. Classify it under "Review gate" | No taxonomy change; the skill does carry a review protocol (Part F) | A review gate reviews an *artifact* after a change and emits a verdict; `research-discipline` is loaded *before and during* the work and emits no verdict — the review protocol is one of seven parts, not the skill's purpose | Semantic mismatch: timing (during, not after) and output (kept checklist, not verdict) both differ |
| B. Leave it uncategorised, like `c4` | Zero guideline change | `c4` is a generator, not a discipline that fires on quality prompts; `research-discipline` is squarely a discipline and belongs in the taxonomy. Leaving it out keeps the category guideline silent on a skill it should cover, inviting the next discipline skill to be mis-slotted | Fails to document a decision future contributors will ask about; the taxonomy would understate the plugin |
| C. Add a fourth "working / pre-registration discipline" category (chosen) | Keeps the taxonomy honest and complete; gives future discipline skills a home; makes the pre-registration gate discoverable and correctly distinct from audits and review gates | Contributors must understand a fourth pattern when proposing new skills; CONTRIBUTING and README category surfaces expand | — |

## Consequences

### Positive

- The taxonomy stays honest: a skill that is neither a retrospective audit, a pre-change code gate, nor a
  review gate now has a named home, and its distinct timing (during the work) and output (a kept checklist)
  are documented.
- Future "discipline" skills — pre-registration gates for other research or engineering practices — have a
  category to join and a precedent to follow.
- The pre-registration gate is discoverable via skill selection, with triggers ("design a metric", "validate
  this metric", "pre-register this analysis") distinct from the audit and review skills.

### Negative

- Contributors proposing a new skill now choose among four categories plus the review gate, not three; the
  decision tree is slightly larger.
- A fourth pattern is one more thing a maintainer must hold in mind when judging whether a new skill fits an
  existing category or warrants its own.

### Neutral

- Requires the v1.28.0 version bump and expands the documentation surface (a CONTRIBUTING category row, a
  README skills row + details block, a NOTICE attribution section).

## Project Guideline Amendment

`CONTRIBUTING.md` "Skill Categories" previously opened:

> mad-scientist-skills contains two categories of skills plus a review gate:

This ADR amends it to "three categories of skills plus a review gate" and adds a fourth row to the category
table — **Working / pre-registration discipline** (fires while doing research; member `research-discipline`;
output a pre-registered checklist, no findings report). Future discipline skills declare this category.

## Related

- **Plugin files:** `plugins/mad-scientist-skills/skills/research-discipline/SKILL.md` and its `references/`.
- **Changelog:** `CHANGELOG.md` entry for `[1.28.0] - 2026-10-01`.
- **ADRs:** follows the precedent of `ADR-001` (which added the pre-change-gate category).
- **External references:** Rahimian, P. (2026), *Auditing Construct Validity in Agentic Decision Support with
  Sports Analytics Case Study* (KDD-WS-AgenticEval '26) — the E1–E6 taxonomy; see `NOTICE.md`.

## Notes

E7 (a metric computed on unobserved positions) and the review-reliability guidance are in-house extensions,
not from the Rahimian paper; the skill and `NOTICE.md` attribute them as such. The skill is public-cite-safe:
it names no private data and quotes no restricted numbers.
