# Design: `unbiased-review` skill

**Date:** 2026-08-28
**Status:** Approved — implementation plan is the companion `2026-08-28-unbiased-review-skill-plan.md`
**Author:** Karsten S. Nielsen
**Type:** Design/spec. This is the *design* half of the repo's design+plan pair convention
(cf. `*-observability-audit-design.md` / `-plan.md`). It states *what* and *why*; the companion
`-plan.md` states *how* — numbered, verifiable steps with commit boundaries.

## Summary

Add a tenth skill, `unbiased-review`, to the `mad-scientist-skills` plugin. It reviews an artifact
(spec, plan, or implementation) produced by *another* session as a non-author: it verifies the
artifact's claims against the actual repo, grades TDD and hexagonal discipline, and reports
severity-ranked findings **without writing the fix**.

The skill originated as an InterSystems-specific tool and was later generalized. This contribution
back-ports the general form. Its review *discipline* is stack-agnostic; only a thin platform layer
(`references/stack-notes.md`) is opinionated, and that layer is rewritten Python-centric to match what
this plugin actually leans into and tests with.

`unbiased-review` is the non-author peer to the existing `final-review`: `final-review` is a
pre-commit gate you run on **your own** work; `unbiased-review` reviews **someone else's** artifact and
deliberately never produces the patch. Its severities (`BLOCKING` / `SHOULD FIX` / `CONSIDER`) map onto
`final-review`'s Critical+High / Medium / Low so the two reports interoperate.

## Motivation

The plugin has a review *gate* (`final-review`) but no *non-author review* discipline. Reviewing
another session's work is a distinct concern with its own failure modes — trusting session narrative
over artifacts, inventing findings from inferred paths, reporting environment-caused failures as
defects, writing the fix and thereby ceasing to be an impartial reviewer. `unbiased-review` encodes
that discipline as seven hard rules and a six-phase protocol (Phase 0–5).

## Scope of adaptation

The engine ports **verbatim**. Only the platform layer is de-InterSystemsed.

### Ports unchanged (verified zero IRIS content by grep)

- `SKILL.md` — 7 hard rules, 6 phases (Phase 0–5), verdicts, non-goal challenge, self-check (except the two
  routing lines noted below and the Phase-5 teardown label — see the post-review note).
- `references/`: `implementation-review.md`, `plan-review.md`, `spec-review.md`, `re-review.md`,
  `output-contract.md`, `tdd-rubric.md`, `isolation-protocol.md` (the last also took a one-line
  teardown-label fix — see the post-review note).

### Three edits to remove InterSystems specifics

1. **`references/stack-notes.md`** (the only heavily-coupled file) — rewrite **Python-centric
   general**:
   - Keep the universal *counting trap* and *scope-your-measurement* principles, stated generically
     (drop the named SC repos `sc-framework` / `sco-ai-demo-builder` / `audit-skills-poc`).
   - Keep and strengthen the **Python / pytest** section (matches the plugin's own `conftest.py` /
     `pytest.ini` test surface).
   - **Remove** the entire *InterSystems IRIS / ObjectScript* section (`%UnitTest.Manager`,
     `^UnitTestRoot`, `$$$Assert*`, `%Status`, `%Persistent`, ObjectScript hexagonal adaptation).
   - Keep a trimmed, generic **JS/TS/Node** section (no "this org" / "mid-migration" framing).
2. **`SKILL.md` routing lines** (currently ~L43–44) — the sentence stating stack-notes carries
   "IRIS/ObjectScript, Python, and TS/Angular specifics" and "which in this codebase is nearly always"
   → stack-neutral phrasing.
3. **`references/hexagonal-rubric.md`** (L4) — the one ObjectScript `%Persistent` example →
   language-neutral phrasing.

**Post-review note (2026-08-28) — a fourth, non-IRIS edit.** The final whole-branch review found that
two prose lines still named a `.scratch/` scratch directory the skill never creates: the actual scratch
path (defined in `isolation-protocol.md` and used by its own teardown `rm -rf`) is
`${TMPDIR:-/tmp}/unbiased-review/`. The stale `.scratch/` label was a pre-generalization residue that
contradicted the file's own code block. Both mentions — `SKILL.md` Phase 5 and `isolation-protocol.md`
Teardown — were reconciled to `${TMPDIR}/unbiased-review/`. This is a coherence fix, not an IRIS scrub,
so it sits outside the three edits above; the "Ports unchanged" bullets are footnoted accordingly.

**Exit check:** the following grep over the new skill and its commands returns zero hits —
```
grep -riE 'iris|intersystems|objectscript|zpm|%csp|%unittest|%persistent|%status|\$\$\$assert|##class|cube|kpi|sc_data|angular|sc-framework'
```
The `%persistent` / `%status` / `$$$assert` / `##class` tokens are included explicitly because they
are exactly the ObjectScript constructs the adaptation removes (currently present in `stack-notes.md`
and `hexagonal-rubric.md`); relying on the broader terms to catch them by co-occurrence is not enough.

## Structure & placement

Following `CONTRIBUTING.md` (skills live under `plugins/mad-scientist-skills/skills/<name>/`):

```
plugins/mad-scientist-skills/
├── skills/unbiased-review/
│   ├── SKILL.md
│   └── references/                    # KEPT — 9 docs (3 adapted per above)
└── commands/                          # NEW dir — first in the plugin
    ├── review-spec.md
    ├── review-plan.md
    ├── review-impl.md
    └── re-review.md
```

Two structural firsts for this repo, both intentional and both explained in the PR body:

- **`references/` subdir.** Every existing skill is flat `SKILL.md` + optional `templates/`. This skill
  routes into 9 supporting docs; keeping them split is what holds `SKILL.md` scannable at ~141 lines.
  Flagged for the maintainer as a candidate new pattern (`CONTRIBUTING.md` mentions only `templates/`).
- **`commands/` dir.** The plugin is currently skills-only. The 4 slash-commands are included because
  a skill is invoked by Claude's *judgment* (description match), whereas a slash-command is a
  *deterministic* user-typed trigger. For a skill named around the generic word "review", the command
  is what stops a generic/built-in reviewer from winning the trigger — this is not hypothetical: the
  skill-only version was hijacked by a generic reviewer in practice until the commands were added. The
  same collision risk exists here against `final-review`'s "final review" / "pre-commit check" matching.

Because these are the first uses of both patterns, this PR also documents them in `CONTRIBUTING.md`
(wiring #8) so the convention doc matches the shipped tree — a maintainer decision (2026-08-28), not a
punt to a later reviewer.

The 4 command files are already self-contained (they reference "the skill's **Hard rules**" and a
`${TMPDIR}`-anchored scratch dir, not a sibling `CLAUDE.md`). Implementation verifies no residual
`CLAUDE.md` / IRIS references survive.

## Repo wiring (touchpoints)

1. **`plugins/mad-scientist-skills/.claude-plugin/plugin.json`** — bump `version` `1.23.0 → 1.24.0`
   (minor: additive skill); append an `unbiased-review (…)` clause to the long `description`.
2. **`.claude-plugin/marketplace.json`** — mirror the version bump + description clause (kept in sync).
3. **`README.md`** — four edits:
   - the **prose skill count** at line 9 ("Install this plugin to get **9** skills for…") → **10**,
     and extend that sentence's list of capability phrases with unbiased review of others' work;
   - the **version badge** at line 6 (`version-1.23.0`) → `1.24.0`;
   - a **row** in the `## Skills` table and a **`<details>` block** under `## Skill Details` matching
     the `final-review` / `measure-before-optimize` pattern;
   - **amend the Safety note** — `unbiased-review` writes to `reviews/` and a scratch dir, so the
     current "only final-review and c4 produce output files" is no longer accurate.
4. **`CHANGELOG.md`** — new `### Added` entry under `## [Unreleased]`.
5. **`NOTICE.md`** — **no entry.** NOTICE sections are content-driven — they attribute external
   academic sources a skill's methodology references. The two peer review-gates `final-review` and
   `measure-before-optimize` have no NOTICE section for the same reason, and `unbiased-review` cites no
   external methodology of its own. Adding one would break the convention, not follow it.
6. **CI** — no change. No Python ships, so the `pytest` job is untouched; only **pre-commit**
   (end-of-file-fixer, trailing-whitespace, check-merge-conflict, check-added-large-files, check-json,
   detect-secrets) must pass. Run `pre-commit run --all-files` locally.
7. **C4 diagram** (`architecture.dsl` / `architecture.html`):
   - Add `unbiasedReviewSkill = container "unbiased-review Skill" "…" "SKILL.md, references/, 4 commands"`
     inside the `plugin` software system.
   - Add `claudeCode -> unbiasedReviewSkill "Invokes" "/mad-scientist-skills:unbiased-review"`.
   - Add an interop edge `unbiasedReviewSkill -> finalReviewSkill "Severity maps onto"` (mirrors the
     existing `finalReviewSkill -> c4Skill` modeling of skill relationships).
   - Fix the hardcoded count in the **plugin** software-system description (`architecture.dsl:6`,
     "plugin of **nine** skills" → "**ten** skills"). The workspace description (`architecture.dsl:1`)
     lists capabilities without a number, so it needs no count edit — only an added "non-author review"
     clause for parity.
   - Regenerate `architecture.html` via the `c4` skill during implementation. Render needs Java 21 +
     Graphviz `dot` (both present) plus `structurizr.war` + `plantuml.jar` (not in-repo; the c4 skill
     locates/fetches them). **Fallback:** if the toolchain cannot assemble, commit the DSL edit and
     flag HTML regeneration as a follow-up rather than block the PR.
8. **`CONTRIBUTING.md`** — document the two new optional layout patterns (a `references/` subdir and a
   plugin-level `commands/` dir) in the *Repository Structure* block, with a sentence on when each
   applies, and add `unbiased-review` to the *Skill Categories* review-gate row. Folded in per the
   maintainer's 2026-08-28 decision (below), since this PR is the first to introduce both patterns.

## Delivery & process

- **Full cycle:** this design → companion `-plan.md` (numbered steps + commit structure) → adapt →
  self-review → user review.
- **Branch in the local clone** `~/Development/agent-skills/mad-scientist-skills/`
  (branch `add-unbiased-review-skill`, off `main` `1e1da60`).
- Claude authors files and runs pre-commit locally; **the user commits, pushes, and opens the PR**
  (no-push convention). Author line `Karsten S. Nielsen <knielsen@intersystems.com>`, no trailers.

## Acceptance criteria

- Skill + 4 commands under the correct paths; the exit-check grep (the pattern under *Scope of
  adaptation*) returns zero hits over the new skill and its commands.
- `plugin.json` + `marketplace.json` at `1.24.0`, descriptions synced.
- README: prose count `9 → 10` (L9) + version badge `1.23.0 → 1.24.0` (L6) + `## Skills` table row +
  `## Skill Details` block + amended Safety note. CHANGELOG `### Added` + `### Changed`. **No** NOTICE
  entry (see #5).
- `CONTRIBUTING.md` documents `references/` + `commands/` in *Repository Structure* and lists
  `unbiased-review` in the *Skill Categories* review-gate row (see #8).
- `architecture.dsl` updated (new container + invoke edge + interop edge + plugin-desc "nine"→"ten" +
  workspace-desc capability clause); `architecture.html` regenerated, or DSL-only with HTML regen flagged.
- `python -m pytest tests -q` green (unaffected); `pre-commit run --all-files` clean.
- PR body explains the two structural firsts with the deterministic-trigger rationale.

## Non-goals

- Not porting `final-review` or `measure-before-optimize` in the other direction (separate threads).
- Not restructuring existing skills to adopt `references/` — the pattern is documented (wiring #8) and
  available, but no existing skill is migrated.
- Not adding Python runtime code or tests (the skill ships none).
