# research-discipline skill — design spec

**Date:** 2026-10-01
**Author session:** home `mad-scientist-skills` session (model: Claude Opus 4.8)
**Status:** DRAFT rev 3 — all `/review-spec` round-1 findings folded (1 BLOCKING + 6 SHOULD FIX) and all
scope questions ruled by Karsten. Ready for spec re-review (round 1 was REQUEST CHANGES → confirm changes
landed → APPROVE), then the plan stage.
**Source of the content being converted:** `D:\Development\_research-discipline\RESEARCH-DISCIPLINE.md`
(**183 lines** per `wc -l`; Parts A–G + Appendix)
**Handoff:** `D:\Development\_research-discipline\HANDOFF-research-discipline-skill.md`

### Revision log
- **rev 4 (2026-10-01):** cosmetic — source line count stated as "183 lines per `wc -l`" (was "183 content
  lines, 184th blank", a harmless off-by-one both plan reviewers flagged; no semantic change, line-ref map unaffected).
- **rev 3 (2026-10-01):** Karsten's rulings baked in — S3 soften (drop the ≈17% figure, soften the
  smaller-model claim to general guidance); S1 keep football-specific (faithful); S6 add an
  optimization-audit-style content-guard test; S7 write `ADR-005` classifying research-discipline as a 4th
  skill category. Defaults accepted: S2 drop footer; S4 full CI-green set incl NOTICE.md; S5 spec+plan in
  `docs/`; S8 accept a brief two-source window (source retired in the lakehouse follow-up); S9 no command,
  specific triggers. Decisions moved from §8 (open) to §8 (resolved).
- **rev 2 (2026-10-01):** BLOCKING-1 (NOTICE.md); SF-2 architecture.dsl (two *different* edits); SF-3
  faithfulness invariant corrected (183 lines; provenance summarize+full; Part-A preamble mapped); SF-4
  "ships code" corrected + content-guard choice surfaced; SF-5 reference sizing corrected; SF-6 agents-md
  guard covers all 8 files; SF-7 ADR/category surfaced.

---

## 1. Goal

Convert `RESEARCH-DISCIPLINE.md` into a new, auto-discovered skill named **`research-discipline`**
in the `mad-scientist-skills` plugin, mirroring the `unbiased-review` skill's shape (SKILL.md headline
+ `references/*.md` depth). The skill becomes the **canonical** home for the discipline;
`RESEARCH-DISCIPLINE.md` reverts to a draft source (retirement window per §8 S8).

This is a **faithful conversion, not a rewrite**: preserve the substance and the E-numbering; adapt
only the format to the skill shape. The one cut, the one softening, and the two additive files are all
recorded in §8 — nothing silent.

---

## 2. Corrected target and version (deviation from the handoff — ruled by Karsten)

The handoff was written by a session that could only see the **installed marketplace clone** and read
a stale version from it. Two literal handoff instructions were therefore wrong; Karsten has ruled:

| Handoff said | Reality | Ruling |
|---|---|---|
| Edit `C:\…\plugins\marketplaces\mad-scientist-skills\…` | That clone is the installed copy, 3 releases behind (v1.26.0), remote `karstenskyt/…` (redirects to `karsten-s-nielsen/…` — same repo) | **Edit the canonical dev repo** `D:\Development\karstenskyt__mad-scientist-skills` (remote `karsten-s-nielsen`, where PRs #18–#20 landed) |
| Bump `1.26.0 → 1.27.0` | `1.27.0` already shipped in the dev repo (optimization-audit equivalence, #20, tag pushed) | **Bump `1.27.0 → 1.28.0`** (minor; new additive skill) |

Diagnostic (answering Karsten's question): v1.27.0 was published correctly — commit `7b74d3a` on main,
annotated tag `v1.27.0` pushed, both manifests at 1.27.0. The confusion was purely the installed plugin
clone lagging the source; both this session's and the reviewing session's plugins have since been reloaded.

Everything else in the handoff (shape, E1–E7 placement, references split, no command, public-cite-safe,
faithful conversion, one feature branch, one coherent commit, no commit without explicit approval) stands.

---

## 3. Skill shape

### 3.1 `SKILL.md` — the headline (loaded every time the skill fires)

Frontmatter (the "review" triggers are kept **specific** — bare "review" collides with the review-*/
built-in review skills per CONTRIBUTING:28–31; S9):

```yaml
---
name: research-discipline
description: Use when designing or validating a quantitative metric, model, or ranking, when pre-registering an analysis, or before shipping a research claim or write-up to a paper, deck, post, or proposal — pre-registers the E1–E7 metric-design anti-patterns, the validity ladder (construct → face → predictive → robustness), and the multi-pass review protocol. Also use when scrutinising a research metric or empirical claim for soundness. Triggers on "design a metric", "validate this metric/model/ranking", "is this metric sound", "pre-register this analysis", "research claim", "efficacy without an outcome label", or an analytics write-up headed for external publication.
---
```

Body (sections, in order):

1. **Intro** — what this is / when it fires / how to use it (a checklist and pre-registration gate, not a
   rulebook; every threshold is a documented, defensible choice). Adapted from source lines 1–7 and 14–15,
   with a **one-line provenance note** pointing at `references/sources.md` (the full "Where it comes from"
   provenance, source lines 8–12, lives in `sources.md`). **Kept football-analytics-specific (S1).**
2. **Metric-design anti-patterns (E1–E7)** — the Part-A preamble (source :21), then E1–E7 one line each,
   verbatim-faithful to source lines 23–41, plus the E2/E6 note (source lines 43–44). **Part A stays in
   SKILL.md because it is the headline.**
3. **The validity ladder (compact)** — construct → face → predictive → robustness; report all four, don't
   skip to a single outcome-AUC; pre-register direction + decision rule before seeing numbers. Distilled
   from source lines 50–51, 63–64. Full ladder in `references/validity-ladder.md`.
4. **Reviewing: the multi-pass protocol (compact)** — ≥3 independent passes with reported agreement; pin
   reviewer model id + prompt/skill version and re-check after a model upgrade; verify, don't OR-union;
   probe omissions. Distilled from source lines 123–128, 141–144. **Per S3: the ≈17% figure (source :124)
   is dropped — rendered as "replicated audits of the same claim agree only a fraction of the time"; the
   "smaller model had the lower false-positive rate" specific (source :126–127) is softened to general
   guidance ("pick the reviewer by measured precision, not tier").** Full protocol in `references/reviewing.md`.
5. **Deeper references** — a one-line pointer per `references/*.md` file (Parts B–G + sources), mirroring
   `unbiased-review/SKILL.md`.

**Template note:** CONTRIBUTING's SKILL.md convention targets the audit skills (Planning/Audit modes,
Coverage, Templates). research-discipline is a *discipline loaded while working*, not an audit, so it
intentionally deviates — no modes, no coverage matrix. Noted so review does not read it as an omission;
it motivates the new category (S7 / ADR-005).

**agents-md guard:** `tests/test_agents_md_awareness.py` has **two** assertions — one over `rglob("SKILL.md")`
(read-list pairing, rule 5.1) and `test_no_claude_md_without_agents_md` over **every** `plugins/**/*.md` line
(rule 5.2 — all **8** shipped files: SKILL.md + the 7 references/, prose included). This skill reads no
consumer-repo instruction files, so **no shipped file may name `CLAUDE.md` without also naming `AGENTS.md`**.
Verified across all 8 files, the suite stays green.

### 3.2 `references/` — the depth (Parts B–G, faithful, + sources)

One file per source Part, mirroring `unbiased-review/references/` granularity. **Size:** source Parts are
11–24 content lines each; a faithful reformat is ~15–35 lines. **No content is added** — any addition would
be a §8 scope change, not a silent expansion.

| File | Source | Content |
|---|---|---|
| `references/validity-ladder.md` | Part B (lines 48–64) | ladder, efficacy-without-outcome, grain cross-check, ICC controls (plant/scramble/ceiling), bootstrap the unit, pre-registration |
| `references/attribution.md` | Part C (68–80) | player ≠ team, crossed random effects, identifiability, transfer/mover test, description vs benchmark |
| `references/data-preflight.md` | Part D (84–99) | observability/censoring, coordinate-frame agreement, schema landmines, fail-closed defaults |
| `references/reproducibility.md` | Part E (103–117) | one source of truth, quote the run, public-tier recompute, audit pointers, verify the artifact, diagnostics-must-not-mutate |
| `references/reviewing.md` | Part F (121–144) | multi-pass ≥3 + agreement, model choice by precision + pin id/version, no OR-union, grade by exactness, probe omissions, ReviewBench, human category-not-severity, reviewing another session's spec/plan/impl. **≈17% dropped + smaller-model softened (S3).** |
| `references/defect-smell-test.md` | Part G (148–164) | vacuous fixtures, wrong-layer guards, silent-zeros/honest-NaN, derived-exports-hide-omissions, prose-halo, one-way scope ratchet, exhaustiveness-needs-a-gate |
| `references/sources.md` | Appendix (168–179) + provenance (8–12) | Rahimian 2026 (taxonomy only ⚠), Landis & Koch 1977, in-house-lessons note |

**Faithfulness map:**
- The seven reference-file rows carry source Parts B–G + Appendix **1:1 in content** (only Part F's two
  empirical specifics are softened per the S3 ruling — recorded, not silent).
- **Provenance (source 8–12)** maps to two places by design: a one-line note in the SKILL.md intro and the
  full text in `sources.md` (summarize-plus-full, not a silent double-map).
- **Part-A preamble (source :21)** maps to the SKILL.md Part-A intro (§3.1 item 2).
- **E-numbering (E1–E7) preserved exactly.**
- The **only** omission is the trailing file-placement footer (source 181–183) — S2.

### 3.3 No command file

A discipline loaded while working, not a slash workflow — no `commands/*.md`. The "review" common-word
collision is handled by specific trigger phrasing (§3.1, S9). Not adding one unless Karsten asks.

---

## 4. Full change set (the one coherent commit)

The handoff named only "bump plugin.json + append a description clause." The repo's gates
(`test_version_consistency`, `test_agents_md_awareness`, `final-review` incl. Phase 2.5) make the following
**mandatory for a green CI and a clean final-review** (S4):

**New skill files (8):**
- `plugins/mad-scientist-skills/skills/research-discipline/SKILL.md`
- `…/research-discipline/references/{validity-ladder,attribution,data-preflight,reproducibility,reviewing,defect-smell-test,sources}.md`

**Canonical attribution (BLOCKING round 1):**
- `NOTICE.md` (repo root) — add a `## research-discipline` section citing **Rahimian, P. (2026)** (E1–E6
  taxonomy only ⚠) and **Landis, J. R., & Koch, G. G. (1977)** (κ bands). NOTICE is the single citation home
  (README "## Academic Attribution"); `final-review` Phase 2.5 scans for the gap.

**ADR (S7 ruling):**
- `docs/adrs/ADR-005-research-discipline-skill-category.md` — Nygard format (per `ADR-TEMPLATE.md`).
  Decision: research-discipline is a **4th skill category — a working / pre-registration discipline** (no
  findings report, no before/after delta, no review verdict), distinct from Retrospective audit / Pre-change
  gate / Review gate. Context: the 3 documented categories do not fit a discipline loaded *while* doing
  research. Consequences: future "discipline" skills join this category; CONTRIBUTING's category table gains
  a 4th row (CONTRIBUTING edit included below).

**Content-guard test (S6 ruling) — lives outside the skill dir per ADR-002, stdlib-only per AGENTS.md:**
- `tests/skills/research-discipline/test_content_guard.py` (+ `__init__.py` only if the sibling test dirs
  carry one — `tests/skills/c4/` does, `tests/skills/optimization-audit/` has `conftest.py`; match the
  convention at plan stage). Asserts: frontmatter valid (`name: research-discipline`, non-empty description);
  **E1–E7 all present, each on a single line**; the validity-ladder and multi-pass sections present; all 7
  reference files exist; `sources.md` cites Rahimian + Landis & Koch; `NOTICE.md` has the `## research-discipline`
  section; **no bare `\d+%` token in any shipped skill file** (machine-locks the S3 softening). These are the
  load-bearing invariants (faithfulness + cite-safety); the guard shifts them left from a one-time grep to CI.

**Version sites — all three agree at `1.28.0` (`test_version_consistency`):**
- `plugins/mad-scientist-skills/.claude-plugin/plugin.json` — `version` → `1.28.0`; append one
  `research-discipline` clause to the long `description` catalog.
- `.claude-plugin/marketplace.json` — `plugins[0].version` → `1.28.0`; append the **same** clause to
  **`plugins[0].description`**, byte-identical to plugin.json (the test compares `plugins[0]`). Leave the
  top-level marketplace `description` untouched.
- `README.md` — `version-1.27.0-` badge → `version-1.28.0-`.

**CHANGELOG (`test_version_consistency`):**
- `CHANGELOG.md` — new `## [1.28.0] - 2026-10-01` section with an `### Added` entry; add `[1.28.0]:`
  compare-link in the footer and repoint `[Unreleased]` to `compare/v1.28.0...HEAD`.

**README skill listing + category table (convention + ADR-005):**
- `README.md` — a new row in the `## Skills` table and a `## Skill Details` entry.
- `CONTRIBUTING.md` — add the 4th category row (working/pre-registration discipline) to the category table
  (:83) so the taxonomy ADR-005 documents is reflected where contributors read it.

**C4 architecture (real drift — `final-review` regenerates via pinned Graphviz `dot`, never Smetana):**
- `architecture.dsl` — **two different edits**:
  - **line 6** (`"…plugin of ten skills: …"`): `ten` → `eleven` **and** add `research-discipline` to its enumeration.
  - **line 1** (workspace description, count-free 10-item prose enum): **add `research-discipline` to the
    enumeration** (no count word). No C4 gate catches a stale prose-enum → hand-verified.
  - add the 11th `container` (`researchDisciplineSkill` + description) and a
    `claudeCode -> researchDisciplineSkill "Invokes" "/mad-scientist-skills:research-discipline"` relationship.
- `architecture.html` — regenerated via the pinned `dot` pipeline, run by `final-review`.

**Planning docs (tracked per the ADR-003 convention; `test_docs_layout` guards the *layout*):**
- `docs/specs/2026-10-01-research-discipline-skill-design.md` (this file)
- `docs/plans/2026-10-01-research-discipline-skill-plan.md` (next stage)

---

## 5. Acceptance criteria (done = all true)

1. `skills/research-discipline/SKILL.md` exists with valid frontmatter and auto-discovers (loads via Skill tool).
2. SKILL.md carries the Part-A preamble + E1–E7 (one line each) + the compact validity ladder + the compact
   multi-pass protocol; `references/` carries Parts B–G faithfully; sources preserved.
3. **Public-cite-safe:** no restricted-tier numbers, no club/keeper names, no private data; the ≈17% figure
   is softened out and the smaller-model claim generalized (S3); the content guard's no-`\d+%` assertion holds.
4. **Faithful:** substance and E-numbering preserved; provenance summarized in intro + full in `sources.md`;
   Part-A preamble carried; footer (181–183) is the only omission; the only softening is S3 (recorded).
5. `NOTICE.md` has a `## research-discipline` section (Rahimian 2026 taxonomy + Landis & Koch 1977).
6. `ADR-005` exists (Nygard format) classifying the skill as a 4th category; `CONTRIBUTING.md` category table
   gains the matching row; `final-review` Phase 2.5 satisfied.
7. `tests/skills/research-discipline/test_content_guard.py` passes and asserts the §4 invariants (incl. no `\d+%`).
8. `plugin.json` version, `marketplace.json` `plugins[0].version`, README badge all `1.28.0`;
   `plugin.json.description` and `marketplace.json plugins[0].description` byte-identical; CHANGELOG has a dated
   `## [1.28.0]` section + `[1.28.0]:` compare-link.
9. README Skills table + Skill Details list `research-discipline`; `architecture.dsl` has the 11th container +
   relationship, line 6 says "eleven skills", **and line 1's prose enum includes research-discipline**;
   `architecture.html` regenerated via Graphviz `dot`.
10. `python -m pytest` green (version consistency, agents-md across all 8 files, docs layout, c4,
    optimization-audit, and the new content guard).
11. One feature branch off `main`; one coherent, fully-tested commit staged; **diff shown and NOT committed**
    until Karsten's explicit per-commit approval. No micro-commits, no worktree.

---

## 6. Verification plan (shift-left, before declaring done)

- `python -m pytest` (full suite) — green, including the new content guard.
- Grep the shipped skill + NOTICE section for restricted-tier leak patterns and any bare `\d+%` — clean.
- Confirm the faithfulness map by diffing source Parts against target files (reviewer-checkable).
- Confirm `NOTICE.md` section + both citations; confirm `ADR-005` + CONTRIBUTING category row.
- `final-review` regenerates `architecture.html`; the assembler aborts on a 0-entity placeholder, so a clean
  assemble proves `dot` ran (not Smetana). Phase 2.5 ADR prompt satisfied by ADR-005.
- Confirm the `Skill` tool loads `research-discipline` after plugin reload.

---

## 7. Workflow + commit discipline

- One feature branch off `main` (proposed: `feat/research-discipline-skill`). No worktree. One coherent,
  fully-tested commit (all §4 files together). No micro-commits.
- Stages: **spec → `/review-spec` (×2) → plan → `/review-plan` (×2) → implement → `/review-impl` (×2) →
  commit on Karsten's explicit go.** Reviews land in `D:\Development\_reviews\`
  (`YYYY-MM-DD-research-discipline-skill-<type>.md`), recording reviewer model id + skill version per pass.
- **Commit gate:** `commit`, `push`, PR, and merge are separate actions; each waits for Karsten's explicit
  approval. Nothing commits on "tests green" or on this spec's approval.

---

## 8. Decisions (resolved by Karsten — recorded, not re-opened)

- **S1 — Domain framing: KEEP football-analytics-specific.** Faithful conversion; concrete anchors preserved
  verbatim. Generalization, if ever wanted, is a separate follow-up cycle.
- **S2 — Drop the file-placement footer (source 181–183).** Obsolete once the skill is canonical; its
  "one source of truth / do not fork" principle survives in Part E → `reproducibility.md`. The only cut.
- **S3 — ≈17% is a repo-note: SOFTEN.** Drop the bare number ("agree only a fraction of the time"); soften the
  smaller-model-FPR specific (:126–127) to general guidance. Keep all method prescriptions (≥3 passes, pin
  model id/version). The content guard's no-`\d+%` assertion locks this.
- **S4 — Full CI-green change set.** NOTICE.md, marketplace.json per-plugin description, README badge +
  listing, CHANGELOG, architecture.dsl/.html, ADR-005, content guard — all in the one commit.
- **S5 — Spec + plan tracked in `docs/specs/` and `docs/plans/`, in the feature commit.**
- **S6 — Add a content-guard test** (`tests/skills/research-discipline/test_content_guard.py`), scope as §4.
- **S7 — Write `ADR-005`** classifying research-discipline as a 4th skill category; reflect it in the
  CONTRIBUTING category table.
- **S8 — Accept a brief two-source window.** `RESEARCH-DISCIPLINE.md` stays a draft source; its full
  retirement/re-point is the lakehouse follow-up (§9). (If you later prefer, a one-line canonical-pointer
  header on the source file can be added — say the word.)
- **S9 — No command.** Trigger phrasing kept specific so "review" does not collide; revisit only if the Skill
  tool mis-selects in practice.

---

## 9. Out of scope (flag, do not do — per the handoff)

- **Editing other skills' cross-references.** `unbiased-review` / `review-spec` lean on "Part F" and could
  cross-link `research-discipline`, but that edits existing skills. A **recommendation** for Karsten, not this change.
- **The per-repo `docs/research/README.md` stub.** Each consuming repo (silly-kicks, lakehouse) owns its own
  path-free E1–E7 stub.
- **The lakehouse re-source.** Retiring/re-pointing the lakehouse's consumption of `RESEARCH-DISCIPLINE.md`
  is a separate lakehouse follow-up.
- **Full removal of `RESEARCH-DISCIPLINE.md`.** Beyond the S8 window, its demotion/removal is handled outside
  this change.

---

## 10. Non-goals of this spec

This spec writes no skill content, touches no code, and authorizes no commit. It defines *what* the skill
will contain and *which* files the single commit touches, for review before the plan stage.
