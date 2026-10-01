# research-discipline Skill Implementation Plan

> **For the implementer:** execute task-by-task in this session; steps use checkbox (`- [ ]`) syntax.
> The one code artifact (the content-guard test) is built test-first (RED → GREEN); the markdown,
> manifest, and C4 wiring are gated by the existing suite (`test_version_consistency`,
> `test_agents_md_awareness`, `test_docs_layout`) plus grep exit-checks. **No commit at any step** —
> the plan ends at a staged diff awaiting Karsten's explicit approval.

**Goal:** Add an eleventh skill, `research-discipline`, to the `mad-scientist-skills` plugin — a faithful
conversion of `D:\Development\_research-discipline\RESEARCH-DISCIPLINE.md` (183 lines, Parts A–G + Appendix)
into `SKILL.md` + 7 `references/*.md`, with all repo wiring, a `NOTICE.md` attribution section, `ADR-005`
(a 4th skill category), and a content-guard test. Version `1.27.0 → 1.28.0`.

**Architecture:** `SKILL.md` carries the headline (intro, Part-A preamble + E1–E7, compact validity ladder,
compact multi-pass protocol, reference pointers); `references/` carries Parts B–G + sources 1:1. The skill
ships no runtime Python, but — per Karsten's S6 ruling — a content-guard test machine-locks the load-bearing
faithfulness + cite-safety invariants. Eleven wiring touchpoints (plugin.json, marketplace.json `plugins[0]`,
README badge+overview-count+table+details, CHANGELOG, NOTICE.md, CONTRIBUTING count-sentence+category-table,
architecture.dsl/.html) plus `ADR-005` complete the one coherent commit.

**Tech Stack:** Markdown skill files; JSON manifests; Python stdlib (pytest-style) for the content guard;
Structurizr DSL + the `c4` skill + pinned Graphviz `dot` for the diagram; `pytest`.

**Companion design:** `docs/specs/2026-10-01-research-discipline-skill-design.md` (the *what/why*; this is
the *how*). All S1–S9 decisions are resolved there (§8) and are not re-opened here.

### Revision log
- **rev 3 (2026-10-01, as-built):** two faithful-execution corrections of plan imprecisions (no scope change).
  (1) `tests/skills/research-discipline/` ships **no `__init__.py`** (and no `conftest.py`): the dir name is
  hyphenated — not a valid Python package — so it follows the `optimization-audit` convention (pytest path
  load), not `c4` (whose `__init__.py` works only because "c4" is a valid identifier). (2) The faithful E1–E7
  lines are bulleted (`- **E1 — …`, as in the source), so the content guard and the exit-check greps anchor on
  `^- \*\*E[1-7] `, not the plan's `^\*\*E[1-7] ` (which matches nothing — the source's E-lines and its
  `- **Efficacy` line are all `- **`-bulleted; the `[1-7]` digit class still excludes `- **Efficacy`). Also:
  `architecture.dsl` line 6 was trimmed to 189 chars to clear the 200-char authoring-lint cap my enum addition
  had pushed to 222 (the pre-existing 259-char `optimization-audit` description WARN is left untouched — not
  this change's scope).
- **rev 2 (2026-10-01):** folds `/review-plan` round 1. BLOCKING D1-PLAN-01 (README:9 "10 skills" overview
  count + enum — Task 7 step + Task 9 grep); SHOULD D1-PLAN-02 (CONTRIBUTING :83 count sentence "two →
  three categories" + correct table line-refs :85–89); SHOULD D1-PLAN-03 (NOTICE ordering — Task 2 checkpoint
  is green-except-NOTICE, fully green at Task 3); SHOULD D1-PLAN-04 (CHANGELOG `[Unreleased]` is empty —
  author fresh, do not "cut"); CONSIDERs: Task 0 creates the branch; guard also asserts the Part-A preamble;
  Task-2 grep tightened to `\*\*E[1-7] `; ADR-005 follows the full template incl. *Alternatives considered* +
  *Project Guideline Amendment*; C4 verification strengthened to an 11-entity render-proof. Flag (not fixed):
  marketplace top-level `description` (:3) is pre-existing-stale — see Global Constraints.

---

## Global Constraints

- **Branch:** one feature branch off `main` — `feat/research-discipline-skill` (created in Task 0). No
  worktree, no second branch.
- **One coherent commit:** every file below lands together, fully tested. No micro-commits, no "commit when green".
- **Commit gate:** the plan stops at a staged diff. `commit`, `push`, PR, merge each wait for Karsten's
  explicit per-commit approval.
- **Faithful conversion:** preserve substance + E-numbering; the only cut is the source footer (S2); the only
  softening is the S3 figures. Nothing else added, dropped, or re-scoped.
- **Public-cite-safe:** no restricted-tier numbers, no club/keeper names. Post-softening the shipped skill has
  **zero `\d+%` tokens** — verified: the source's only two `%` are `:124` (`≈17%`, dropped by S3) and `:174`
  (`"% of studies…"`, prose in the Appendix ⚠, not `\d+%`, kept as the do-not-cite warning).
- **Tests:** stdlib-only, `encoding="utf-8"`, live under `tests/` (ADR-002), never inside the skill dir.
- **Edits byte-safe:** manifest/markdown edits via the `Edit` tool (no `Set-Content` BOM/line-ending damage);
  confirm with `git diff --stat`.
- **Flag, do not fix:** the top-level `marketplace.json` `description` (:3) is **already stale** (it omits
  `measure-before-optimize` and `unbiased-review`). It is **test-safe** (`test_version_consistency` compares
  only `plugins[0].description`) and its staleness predates this change, so this commit leaves it untouched
  and surfaces it to Karsten as a separate follow-up rather than silently re-scoping it.

---

### Task 0: Create the feature branch

**Files:** none (git state).

- [ ] **Step 1:** From `main` (clean tree, confirmed at `7b74d3a`): `git checkout -b feat/research-discipline-skill`.
- [ ] **Step 2:** Confirm the branch and that no tracked file is dirty (`git status`).

---

### Task 1: Content-guard test — TDD RED

**Files:** `tests/skills/research-discipline/test_content_guard.py` (new);
`tests/skills/research-discipline/__init__.py` (new — `tests/skills/c4/__init__.py` exists; match the convention).

- [ ] **Step 1: Write the guard** asserting, against the not-yet-written skill:
  - `SKILL.md` frontmatter parses; `name == "research-discipline"`; `description` non-empty and contains at
    least one specific trigger ("design a metric" / "validate").
  - **E1–E7 all present**, each as a single bulleted `- **E<n> —` line (seven matches via `^- \*\*E[1-7] `, one line each).
  - **The Part-A preamble** is present (a stable substring of source :21, e.g. "clear all seven").
  - SKILL.md contains the validity-ladder section and the multi-pass protocol section.
  - All 7 `references/*.md` exist (validity-ladder, attribution, data-preflight, reproducibility, reviewing,
    defect-smell-test, sources).
  - `references/sources.md` cites "Rahimian", "Landis", and "Koch".
  - `NOTICE.md` contains a `## research-discipline` section.
  - **No bare `\d+%` token** in any shipped skill file (SKILL.md + all references) — locks the S3 softening.
  - No shipped skill file names `CLAUDE.md` without also naming `AGENTS.md`.
  - *(Not machine-checked: per-Part 1:1 faithfulness — that is the manual source-diff in spec §6 / Task 9.2.)*
- [ ] **Step 2: Run it → expect RED** (`python -m pytest tests/skills/research-discipline -q`): fails because
  the skill files do not exist yet. Record the failure as the TDD baseline.

---

### Task 2: Author the skill content — TDD toward GREEN (NOTICE assertion stays RED until Task 3)

**Files (new):** `plugins/mad-scientist-skills/skills/research-discipline/SKILL.md` and
`…/references/{validity-ladder,attribution,data-preflight,reproducibility,reviewing,defect-smell-test,sources}.md`.

- [ ] **Step 1: `SKILL.md`** — frontmatter per spec §3.1 (specific triggers, no bare "review"). Body:
  1. Intro (source 1–7, 14–15) + one-line provenance pointer to `references/sources.md`; football-specific (S1).
  2. **Part-A preamble (source :21)**, then **E1–E7 one line each** (source 23–41) verbatim-faithful, then the
     **E2/E6 note** (source 43–44).
  3. Compact validity ladder (source 50–51, 63–64) → pointer to `validity-ladder.md`.
  4. Compact multi-pass protocol (source 123–128, 141–144) **with S3 softening**: "replicated audits agree
     only a fraction of the time" (no `≈17%`); "pick the reviewer by measured precision, not tier" (drop the
     smaller-model-FPR specific). Pointer to `reviewing.md`.
  5. "Deeper references" — one line per reference file.
  6. Template-deviation note (no modes/coverage — a working discipline, not an audit).
- [ ] **Step 2–8: the seven reference files**, each 1:1 with its source Part:
  - `validity-ladder.md` ← Part B (48–64); `attribution.md` ← Part C (68–80); `data-preflight.md` ← Part D
    (84–99); `reproducibility.md` ← Part E (103–117) — carries the "one source of truth / do not fork"
    principle that absorbs the dropped footer (S2); `reviewing.md` ← Part F (121–144) **with the same S3
    softening**; `defect-smell-test.md` ← Part G (148–164); `sources.md` ← Appendix (168–179) + provenance
    (8–12): Rahimian 2026 (⚠ taxonomy only — do not cite the "% of studies" figures), Landis & Koch 1977 (κ
    bands), in-house note. **Drop the file-placement footer (source 181–183, S2).**
- [ ] **Step 9: Run the content guard** (`python -m pytest tests/skills/research-discipline -q`): **expect
  green on every assertion EXCEPT the NOTICE `## research-discipline` section, which is RED until Task 3.**
  (Mirrors the CHANGELOG assertion in Task 5, RED until Task 6.) Confirm the failure is *only* the NOTICE one.
- [ ] **Step 10: Faithfulness + cite-safety greps:**
  - `grep -rnoE "[0-9]+%"` the skill dir → **zero hits**.
  - `grep -cE "^- \*\*E[1-7] " SKILL.md` → **7** (E1–E7; the bulleted anchor still avoids miscounting a `- **Efficacy`
    bold such as source :53).
  - `grep -rn "CLAUDE.md" skills/research-discipline` → any hit also names `AGENTS.md` (expected: none).

---

### Task 3: NOTICE.md attribution section (completes the content guard)

**Files:** `NOTICE.md`.

- [ ] **Step 1:** Add a `## research-discipline` section (matching the 7 existing sections' format) citing
  **Rahimian, P. (2026)** — *Auditing Construct Validity in Agentic Decision Support with Sports Analytics
  Case Study* (KDD-WS-AgenticEval '26), used for the **E1–E6 taxonomy only** — and **Landis, J. R., & Koch,
  G. G. (1977)** — *The measurement of observer agreement for categorical data*, Biometrics 33(1) (κ bands).
- [ ] **Step 2:** Re-run `python -m pytest tests/skills/research-discipline -q` → **now fully GREEN** (TDD
  GREEN reached: Task 1 RED → Task 2 all-but-NOTICE → Task 3 full green).

---

### Task 4: ADR-005 + CONTRIBUTING (count sentence + category table)

**Files:** `docs/adrs/ADR-005-research-discipline-skill-category.md` (new); `CONTRIBUTING.md`.

- [ ] **Step 1:** Write `ADR-005` using the **full** `docs/adrs/ADR-TEMPLATE.md` section set — `Context`,
  `Decision`, **`Alternatives considered`**, `Consequences` (Positive/Negative/Neutral), **`Project Guideline
  Amendment`** (records that this ADR amends CONTRIBUTING's category guideline), `Related`, `Notes`. **Status**
  Accepted. **Decision:** introduce a 4th category — **working / pre-registration discipline** — with
  `research-discipline` as its first member, distinct from Retrospective audit / Pre-change gate / Review gate
  (no findings report, no delta, no verdict). **Alternatives considered:** shoehorn into "Review gate" (rejected
  — it is not a review-of-an-artifact), or no category (rejected — leaves the taxonomy silent). Precedent:
  `ADR-001` added the pre-change-gate category.
- [ ] **Step 2: `CONTRIBUTING.md` :83 count sentence** — "contains **two** categories of skills plus a review
  gate" → "contains **three** categories of skills plus a review gate".
- [ ] **Step 3: `CONTRIBUTING.md` category table (:85–89)** — add a 4th data row: **Working / pre-registration
  discipline** | "while doing research — 'design/validate a metric', 'pre-register an analysis'" |
  `research-discipline` | "pre-registered checklist; no findings report".

---

### Task 5: Version wiring — plugin.json + marketplace.json

**Files:** `plugins/mad-scientist-skills/.claude-plugin/plugin.json`; `.claude-plugin/marketplace.json`.

- [ ] **Step 1:** `plugin.json` — `version` → `1.28.0`; append one `research-discipline` clause to the long
  `description` catalog ("…, and research-discipline (a pre-registration discipline: the E1–E7 metric-design
  anti-patterns, the construct→face→predictive→robustness validity ladder, and a multi-pass review protocol)").
- [ ] **Step 2:** `marketplace.json` — `plugins[0].version` → `1.28.0`; append the **byte-identical** clause to
  **`plugins[0].description`**. **Leave the top-level `description` (:3) untouched** (Global Constraints flag).
- [ ] **Step 3:** Both valid JSON; `plugins[0].description == plugin.json.description`;
  `python -m pytest tests/test_version_consistency.py -q` — version + description assertions green (the CHANGELOG
  assertion is RED until Task 6).

---

### Task 6: CHANGELOG

**Files:** `CHANGELOG.md`.

- [ ] **Step 1:** `[Unreleased]` is **empty** at `7b74d3a` — **add a new `## [1.28.0] - 2026-10-01` section**
  with an `### Added` entry for `research-discipline` (skill + NOTICE + ADR-005 + content guard). Do not "cut
  from Unreleased" (there is nothing there).
- [ ] **Step 2:** Footer — add `[1.28.0]: https://github.com/karsten-s-nielsen/mad-scientist-skills/compare/v1.27.0...v1.28.0`
  and repoint `[Unreleased]: …/compare/v1.28.0...HEAD`.
- [ ] **Step 3:** `python -m pytest tests/test_version_consistency.py -q` → fully green.

---

### Task 7: README — badge, overview count, table row, details block

**Files:** `README.md`.

- [ ] **Step 1:** Version badge (L6) `version-1.27.0-` → `version-1.28.0-`.
- [ ] **Step 2 (BLOCKING fix):** Overview sentence (**L9**) — "get **10 skills** for … and non-author artifact
  review." → "get **11 skills** for …, non-author artifact review**, and research-discipline (pre-registration
  metric discipline)**." Hand-verified (prose, no gate — like the DSL line-1 enum).
- [ ] **Step 3:** Add a `## Skills` table row for `research-discipline`.
- [ ] **Step 4:** Add a `## Skill Details` entry (format matching siblings): pre-registration discipline, E1–E7
  headline, the validity ladder, the multi-pass protocol, "no command — loaded while working".
- [ ] **Step 5:** Re-run `test_version_consistency` (badge) and eyeball the overview count.

---

### Task 8: C4 — architecture.dsl (two edits) + regenerate architecture.html

**Files:** `architecture.dsl`; `architecture.html` (regenerated).

- [ ] **Step 1: `architecture.dsl` line 6** (`"…plugin of ten skills: …"`): `ten` → `eleven` **and** add
  `research-discipline` to its enumeration.
- [ ] **Step 2: `architecture.dsl` line 1** (workspace desc, count-free 10-item prose enum): **add
  `research-discipline`** to the enumeration (no count word; hand-verify — no gate catches a stale prose-enum).
- [ ] **Step 3:** Add the 11th `container` `researchDisciplineSkill = container "research-discipline Skill"
  "Pre-registration discipline: E1–E7 metric-design anti-patterns, the construct→face→predictive→robustness
  validity ladder, and a multi-pass review protocol" "SKILL.md, references/"` and the relationship
  `claudeCode -> researchDisciplineSkill "Invokes" "/mad-scientist-skills:research-discipline"`.
- [ ] **Step 4: Regenerate `architecture.html`** via the `final-review` / `c4` pipeline with pinned Graphviz
  `dot` (`-graphvizdot "C:/Users/Karsten/.claude/tools/graphviz/dot.exe"`), **never Smetana**. A clean assemble
  (no 0-entity placeholder abort) proves `dot` ran. Rendered on this **home** machine.
- [ ] **Step 5 (render-proof, not eyeball):** grep the regenerated `architecture.html` for the string
  `research-discipline Skill` (present) **and** count the embedded `… Skill` container labels in the Container
  view → **11**. A bare viewBox glance is not sufficient proof.

---

### Task 9: Full verification (shift-left)

- [ ] **Step 1:** `python -m pytest` (whole suite) → green: version consistency, agents-md awareness (all 8
  shipped files), docs layout, c4, optimization-audit, **and** the new `research-discipline` content guard.
- [ ] **Step 2:** Manual faithfulness source-diff — each source Part vs its target file, 1:1 (the guard does not
  machine-check this); plus the cite-safety/count greps (zero `\d+%`; `^- \*\*E[1-7] ` = 7; no lone CLAUDE.md).
- [ ] **Step 3: Prose-count greps** (the class of defect the C4 line-1 / README:9 / CONTRIBUTING:83 edits
  address) — `grep -rniE "ten skills|10 skills|two categories" README.md CONTRIBUTING.md architecture.dsl` →
  **zero stale hits**; confirm "eleven"/"11"/"three categories" where expected.
- [ ] **Step 4:** Confirm the `Skill` tool loads `research-discipline` after a plugin reload (frontmatter valid,
  auto-discovered).
- [ ] **Step 5:** `pre-commit` hygiene by hand if available locally (end-of-file, trailing-whitespace, check-json,
  detect-secrets); CI runs it regardless. `final-review` Phase 2.5 satisfied by `ADR-005`.

---

### Task 10: Stage + stop at the commit boundary

- [ ] **Step 1:** `git add` the full change set (Tasks 1–8 + this plan + the spec + ADR-005). Show `git status`
  + `git diff --stat` + the full diff.
- [ ] **Step 2:** **STOP.** Present the staged diff and the proposed commit message. Do **not** commit, push,
  open a PR, or merge. Wait for Karsten's explicit per-commit approval.

**Proposed commit message (for approval, not yet applied):**
```
feat(research-discipline): add pre-registration discipline skill (v1.28.0)

Convert RESEARCH-DISCIPLINE.md into an auto-discovered skill: SKILL.md
(E1–E7 anti-patterns, validity ladder, multi-pass protocol) + references/
(Parts B–G + sources). New 4th skill category (ADR-005). NOTICE attribution,
content-guard test, and full release wiring (manifests, README, CHANGELOG, C4).

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>
```

---

## Task dependency / ordering

0 (branch) → 1 (RED) → 2 (green-except-NOTICE) → 3 (NOTICE → full GREEN) → 4 → 5 → 6 → 7 → 8 → 9 (whole-suite
green + prose-count greps) → 10 (stage, stop). Tasks 4–8 are independent of each other but all precede Task 9's
whole-suite gate. The commit is one unit.
