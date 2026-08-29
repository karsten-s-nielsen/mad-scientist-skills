# unbiased-review Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a tenth skill, `unbiased-review` (skill + 4 slash-commands), to the `mad-scientist-skills` plugin, generalized off its InterSystems origin, with all repo wiring updated.

**Architecture:** Copy the already-generalized skill from the sibling `sc-ai-marketplace` working copy, strip the three InterSystems-coupled spots, add the first `commands/` and `references/` directories the plugin has carried, and update the seven wiring touchpoints (plugin.json, marketplace.json, README, CHANGELOG, C4 DSL/HTML). The skill ships no runtime Python, so there is no pytest surface; verification is grep-based content checks plus `pre-commit` and the existing (unaffected) `pytest tests -q`.

**Tech Stack:** Markdown skill files; JSON manifests; Structurizr DSL + the `c4` skill for the diagram; `pre-commit` (end-of-file-fixer, trailing-whitespace, check-merge-conflict, check-added-large-files, check-json, detect-secrets); `pytest`.

**Companion design:** `docs/plans/2026-08-28-unbiased-review-skill-design.md` (the *what/why*; this is the *how*).

## Global Constraints

- **Source of truth for the skill files:** `~/Development/agent-skills/sc-ai-marketplace/plugins/supply-chain-review-skills/` (skill + commands, already generalized). Copy from there; do not re-derive.
- **Target repo / branch:** `~/Development/agent-skills/mad-scientist-skills/`, branch `add-unbiased-review-skill` (off `main` `1e1da60`). Already checked out.
- **Version bump:** `1.23.0 → 1.24.0` (minor, additive) everywhere a version appears (`plugin.json`, `marketplace.json`, README badge).
- **Exit-check grep (must return zero hits over the new skill + commands):**
  `grep -riE 'iris|intersystems|objectscript|zpm|%csp|%unittest|%persistent|%status|\$\$\$assert|##class|cube|kpi|sc_data|angular|sc-framework' plugins/mad-scientist-skills/skills/unbiased-review plugins/mad-scientist-skills/commands`
- **No NOTICE.md entry** (content-driven convention; peer gates have none).
- **Commit:** one commit for the whole change, at the very end, authored `Karsten S. Nielsen <knielsen@intersystems.com>`, no trailers. **Claude does not push or open the PR** — the user does.
- **Skill ships no Python** → no new tests, no `conftest.py` change.

---

### Task 1: Copy skill + commands into the plugin, then de-InterSystems the three coupled spots

**Files:**
- Create: `plugins/mad-scientist-skills/skills/unbiased-review/SKILL.md`
- Create: `plugins/mad-scientist-skills/skills/unbiased-review/references/` (9 files)
- Create: `plugins/mad-scientist-skills/commands/{review-spec,review-plan,review-impl,re-review}.md`
- Modify (post-copy): `skills/unbiased-review/SKILL.md`, `skills/unbiased-review/references/stack-notes.md`, `skills/unbiased-review/references/hexagonal-rubric.md`

**Interfaces:**
- Consumes: the generalized files at `sc-ai-marketplace/plugins/supply-chain-review-skills/`.
- Produces: a self-contained skill dir + `commands/` dir referenced by Tasks 2–4.

- [ ] **Step 1: Copy the skill and commands verbatim**

```bash
SRC=~/Development/agent-skills/sc-ai-marketplace/plugins/supply-chain-review-skills
DST=~/Development/agent-skills/mad-scientist-skills/plugins/mad-scientist-skills
mkdir -p "$DST/commands"
cp -R "$SRC/skills/unbiased-review" "$DST/skills/unbiased-review"
cp "$SRC/commands/"{review-spec,review-plan,review-impl,re-review}.md "$DST/commands/"
# drop any stray macOS cruft that would trip check-added-large-files / noise
find "$DST/skills/unbiased-review" "$DST/commands" -name '.DS_Store' -delete
```

- [ ] **Step 2: Confirm the copy landed (10 skill files + 4 commands)**

Run:
```bash
DST=~/Development/agent-skills/mad-scientist-skills/plugins/mad-scientist-skills
find "$DST/skills/unbiased-review" -type f | sort; echo "---"; ls "$DST/commands"
```
Expected: `SKILL.md` + `references/`{hexagonal-rubric, implementation-review, isolation-protocol, output-contract, plan-review, re-review, spec-review, stack-notes, tdd-rubric}`.md` (9 references), and the 4 command files.

- [ ] **Step 3: Fix SKILL.md routing lines (remove IRIS/Angular naming)**

In `skills/unbiased-review/SKILL.md`, replace the routing sentence:

Old:
```
`references/hexagonal-rubric.md` when the artifact makes claims about tests or architecture — which
in this codebase is nearly always. `references/stack-notes.md` carries IRIS/ObjectScript, Python, and
TS/Angular specifics. `references/isolation-protocol.md` is required before executing anything.
```
New:
```
`references/hexagonal-rubric.md` when the artifact makes claims about tests or architecture — which
is nearly always. `references/stack-notes.md` carries per-stack specifics (Python, JS/TS/Node).
`references/isolation-protocol.md` is required before executing anything.
```

- [ ] **Step 4: Rewrite stack-notes.md Python-centric (remove ObjectScript, de-org the counting trap)**

Replace the entire contents of `skills/unbiased-review/references/stack-notes.md` with:

```markdown
# Stack notes

Platform specifics that recur across reviews regardless of topic. Not a tutorial — these are the
places where a claim is likely to be wrong, and the command that settles it.

## The counting trap, all stacks

**The same logical repo often exists at several filesystem paths** — vendored copies, git worktrees
(commonly prefixed `wt-`), submodules, a `node_modules` mirror of a workspace package. Any repo-wide
`grep -c` is then inflated by an unknown multiple: one test file with 1,800 assertions, duplicated
five times, reads as 9,000 and makes a niche pattern look dominant.

Scope every count to one checkout, and say which:

```bash
grep -rc "<pattern>" --include="*.py" <one-repo-root>/src
```

When an artifact claims "N occurrences in the codebase", ask which tree it counted before treating the
number as right *or* wrong.

## Python

pytest, configured by `pytest.ini` or `pyproject.toml`, with `conftest.py` for fixtures.
**`test_*.py` is the dominant convention**; `*_test.py` also collects but is worth flagging as
inconsistent when both appear in one tree.

**Scope decides the count.** `pytest tests` collects a different set than `pytest tests/unit`, and
slow browser/integration suites (Selenium, `tests/integration/`) frequently live in their own trees
with their own `pytest.ini`. A unit-test figure that silently includes them is the most common way a
Python test count becomes unreproducible — check what the invoked path actually collects, and record
the exact command beside any number.

**A test that imports the module under test but asserts nothing about its return value is a silent
pass** — the call ran, nothing was checked. This is the Python analogue of ignoring a status return:
grep the test body for an `assert` that actually references the call's result.

**Markers gate collection.** `@pytest.mark.skip` / `skipif` / `xfail` change what runs; a green
summary with a high skip count is not the same claim as "all tests pass". Read the summary line, not
just the exit code.

## JavaScript / TypeScript / Node

**Test runner is decided per project**, not by the language — Jest, vitest, node:test, Karma. Read
the `test` script in `package.json` (and, for a monorepo, the per-workspace one) before accepting any
"the suite runs in Xs headless" claim; a browser runner needs a browser binary in the image and a
headless one does not.

`vitest run` collects everything, including `test/integration/*` files that may be skipped at
runtime; `vitest run test/unit` collects less. **Two honest measurements of the same tree differ by
scope** — record the exact command beside any count; reconciling a discrepancy as a scope difference
is usually right and worth stating rather than reporting as a regression.

Native modules (e.g. `better-sqlite3`) fail at *module load*, taking down every test file whose import
graph reaches them — including files that never touch the database. `import type` does not trigger it;
a runtime import does. That distinction decides the blast radius and is invisible in a diff review:

```bash
grep -rn "better-sqlite3" <repo>/src   # separate the type-only imports from runtime ones
```

Per `isolation-protocol.md`, confirm the binding is absent in the **target** before attributing such a
failure to anything but the environment.

**npm workspaces.** `npm run test --workspace <name>` runs that workspace's own `test` script; flags
after `--` pass through. Root scripts and CI jobs frequently disagree about which is the real entry
point — verify which one a pipeline actually invokes rather than assuming the root script is it.
```

- [ ] **Step 5: De-ObjectScript the hexagonal-rubric.md opener**

In `skills/unbiased-review/references/hexagonal-rubric.md`, replace lines 3–6:

Old:
```
Graded, not pass/fail. No repo in this ecosystem has a `domain/ports/adapters`
layout, and ObjectScript's `%Persistent` inheritance makes a genuinely pure core hard. A rubric that
demands the textbook shape emits noise on every review and gets ignored. Grade the direction of
travel and name the cheapest move up one rung.
```
New:
```
Graded, not pass/fail. Most real repos have no textbook `domain/ports/adapters`
layout, and some languages (persistence frameworks with base-class inheritance, ORMs active-record
style) make a genuinely pure core hard. A rubric that demands the textbook shape emits noise on every
review and gets ignored. Grade the direction of travel and name the cheapest move up one rung.
```

- [ ] **Step 6: Run the exit-check grep — expect zero hits**

Run (from repo root):
```bash
grep -riE 'iris|intersystems|objectscript|zpm|%csp|%unittest|%persistent|%status|\$\$\$assert|##class|cube|kpi|sc_data|angular|sc-framework' \
  plugins/mad-scientist-skills/skills/unbiased-review plugins/mad-scientist-skills/commands
```
Expected: **no output** (exit 1). Any hit is a residual to remove before proceeding.

- [ ] **Step 7: Confirm commands are self-contained (no CLAUDE.md / target-repo path leakage)**

Run:
```bash
grep -rniE "CLAUDE\.md|\.scratch|/Users/" plugins/mad-scientist-skills/commands
```
Expected: no hits. (The commands were already fixed to reference "the skill's Hard rules" and a `${TMPDIR}` scratch anchor during the earlier port; this confirms it.)

---

### Task 2: Manifests — plugin.json + marketplace.json

**Files:**
- Modify: `plugins/mad-scientist-skills/.claude-plugin/plugin.json`
- Modify: `.claude-plugin/marketplace.json`

**Interfaces:**
- Consumes: nothing from prior tasks (independent metadata).
- Produces: version `1.24.0` and an `unbiased-review` description clause, relied on by the README/CHANGELOG for consistency.

- [ ] **Step 1: Bump `plugin.json` version and extend description**

In `plugins/mad-scientist-skills/.claude-plugin/plugin.json`: set `"version": "1.24.0"`, and append to the end of the long `description` string (before the closing quote), after "…and pre-commit quality gate with architecture diagram generation":
```
, and non-author artifact review (unbiased-review: verifies a spec, plan, or implementation produced by another session against the actual repo, grades TDD and hexagonal discipline, reproduces empirical claims in isolation, and reports severity-ranked findings with stable IDs without writing the fix)
```

- [ ] **Step 2: Mirror the same two edits into `marketplace.json`**

In `.claude-plugin/marketplace.json`, the single `plugins[0]` entry: set `"version": "1.24.0"` and append the identical clause to its `description`. (The two descriptions are kept byte-identical; copy the exact string from Step 1.)

- [ ] **Step 3: Verify both are valid JSON and versions match**

Run:
```bash
python3 -c "import json;a=json.load(open('plugins/mad-scientist-skills/.claude-plugin/plugin.json'));b=json.load(open('.claude-plugin/marketplace.json'));print(a['version'], b['plugins'][0]['version']); assert a['version']=='1.24.0'==b['plugins'][0]['version']; assert a['description']==b['plugins'][0]['description']"
```
Expected: `1.24.0 1.24.0` and no AssertionError.

---

### Task 3: README — count, badge, table row, details block, safety note

**Files:**
- Modify: `README.md` (lines 6, 9, the `## Skills` table ~L19, the `## Skill Details` `<details>` blocks, and the Safety note L33)

**Interfaces:**
- Consumes: version `1.24.0` (Task 2).
- Produces: user-facing docs; no downstream consumer.

- [ ] **Step 1: Version badge (L6)**

Replace `version-1.23.0-blue` → `version-1.24.0-blue`.

- [ ] **Step 2: Prose skill count (L9)**

In the sentence "Install this plugin to get **9** skills for architecture auditing, …, and pre-commit quality checks." — change `9` → `10` and append `, and non-author artifact review` before the closing period.

- [ ] **Step 3: Add a `## Skills` table row**

Insert immediately after the `security-audit` row (currently the last row in the `## Skills` table), so `unbiased-review` lands at the end:
```
| **unbiased-review** | Review a spec, plan, or implementation written by another session — verify its claims against the repo, grade TDD/hexagonal discipline, report severity-ranked findings without writing the fix | `/mad-scientist-skills:unbiased-review` |
```

- [ ] **Step 4: Add a `## Skill Details` `<details>` block**

After the `measure-before-optimize` `</details>` block, insert:
```markdown
<details>
<summary><strong>unbiased-review</strong> — Non-Author Review Gate (spec / plan / implementation)</summary>

Reviews an artifact produced by another session. You did not write it, you will not fix it, and you verify rather than trust. Peer to `final-review`: that one gates your own work pre-commit; this one reviews someone else's artifact and never produces the patch. Its severities (`BLOCKING` / `SHOULD FIX` / `CONSIDER`) map onto `final-review`'s Critical+High / Medium / Low so reports interoperate.

### What it does

1. **Establish scope** — pins the artifact (sha) and the target tree (HEAD, status, staged diff)
2. **Claim extraction** — enumerates every checkable claim before judging any
3. **Verification** — classifies each claim exact / wrong / imprecise / unverifiable; prefers Grep/Read, uses an isolated scratch clone when only execution settles it
4. **Rubric passes** — TDD, hexagonal, durability, scope/YAGNI, internal consistency, non-goal challenge
5. **Self-check then report** — a full report to `reviews/` plus a short paste-back block; leaves the target's `git status` unchanged

### Ships slash-commands

Unlike the audit skills, this one ships four commands as deterministic entry points, because "review this" otherwise collides with generic review matching:

```
/review-spec <path>     /review-plan <path>     /review-impl <path>     /re-review <path>
```

Or invoke the skill directly:

```
/mad-scientist-skills:unbiased-review
```

</details>
```

- [ ] **Step 5: Amend the Safety note (L33)**

Replace:
```
> **Safety note:** All audit skills perform read-only analysis — they scan your code and produce a findings report but do not modify files. Only `final-review` and `c4` produce output files (`architecture.html`, `architecture.dsl`).
```
with:
```
> **Safety note:** The audit skills perform read-only analysis — they scan your code and produce a findings report but do not modify files. `final-review` and `c4` produce output files (`architecture.html`, `architecture.dsl`). `unbiased-review` never writes to the repo under review, but does write its own report to `reviews/` and uses a scratch directory outside the target tree.
```

- [ ] **Step 6: Verify the count and row are consistent**

Run:
```bash
grep -nE "get 10 skills|version-1.24.0|unbiased-review" README.md | head
```
Expected: the badge line, the "10 skills" prose, the table row, and the details summary all present.

---

### Task 4: C4 diagram — DSL edit + regenerate HTML (with fallback)

**Files:**
- Modify: `architecture.dsl`
- Regenerate: `architecture.html` (via the `c4` skill)

**Interfaces:**
- Consumes: nothing from prior tasks (the DSL models skills, not files).
- Produces: the updated diagram; terminal deliverable.

- [ ] **Step 1: Add the container (after the `securityAuditSkill` line, L15)**

Insert inside the `plugin` softwareSystem block:
```
            unbiasedReviewSkill = container "unbiased-review Skill" "Non-author review of a spec, plan, or implementation from another session: verifies claims against the repo, grades TDD and hexagonal discipline, reports severity-ranked findings without writing the fix" "SKILL.md, references/, 4 commands"
```

- [ ] **Step 2: Add the invoke + interop relationships (after L32 / near L33)**

Add an invoke edge alongside the other `claudeCode -> …Skill "Invokes"` lines:
```
        claudeCode -> unbiasedReviewSkill "Invokes" "/mad-scientist-skills:unbiased-review"
```
And an interop edge modeling the severity mapping (mirrors the existing `finalReviewSkill -> c4Skill`):
```
        unbiasedReviewSkill -> finalReviewSkill "Severity maps onto" "Interoperable reports"
```

- [ ] **Step 3: Fix the plugin-description count (L6)**

In `plugin = softwareSystem …`: change `Claude Code plugin of nine skills:` → `Claude Code plugin of ten skills:`, and add `, and non-author review` to that sentence's capability list before the closing quote.

- [ ] **Step 4: Add a capability clause to the workspace description (L1)**

The workspace line has no count; append `, and non-author artifact review` to its capability list before the closing quote (parity, not a count fix).

- [ ] **Step 5: Regenerate architecture.html via the c4 skill**

Invoke the `c4` skill against `architecture.dsl` (it locates/fetches `structurizr.war` + `plantuml.jar`; Java 21 + Graphviz `dot` are present). Produce a refreshed `architecture.html` containing the `unbiased-review Skill` container in the Containers view.

**Fallback:** if the render toolchain cannot assemble (jars unfetchable / offline), do **not** hand-edit the HTML. Leave `architecture.html` unchanged, keep the DSL edit, and record in the PR body that `architecture.html` regeneration is a follow-up. This is acceptable per the design.

- [ ] **Step 6: Verify the DSL parses / contains the new elements**

Run:
```bash
grep -nE "unbiasedReviewSkill|ten skills" architecture.dsl
```
Expected: the container definition, both relationship lines, and the "ten skills" description all present. If HTML was regenerated, also: `grep -c "unbiased-review Skill" architecture.html` ≥ 1.

---

### Task 5: CONTRIBUTING.md — bless the two new layout patterns

**Files:**
- Modify: `CONTRIBUTING.md` (the `## Repository Structure` fenced skill-layout block ~L14–21, and the `## Skill Categories` table ~L73–81)

**Interfaces:**
- Consumes: nothing from prior tasks (documents patterns the copy in Task 1 introduces).
- Produces: convention doc in sync with what this PR ships; no downstream consumer.

**Rationale:** This PR is the first to add a `references/` subdir *and* a plugin-level `commands/` dir. The maintainer (Karsten) has decided to bless both patterns in the same PR rather than leave them undocumented, so the structure doc matches the shipped tree.

- [ ] **Step 1: Extend the Repository Structure skill-layout block**

In the fenced block at `## Repository Structure`, replace:
```
plugins/mad-scientist-skills/
└── skills/
    └── <skill-name>/
        ├── SKILL.md        # Skill definition (YAML frontmatter + body)
        ├── templates/      # Optional output templates
        └── *.py            # Optional runtime scripts the skill invokes
```
with:
```
plugins/mad-scientist-skills/
├── skills/
│   └── <skill-name>/
│       ├── SKILL.md        # Skill definition (YAML frontmatter + body)
│       ├── templates/      # Optional output templates
│       ├── references/     # Optional supporting docs a long SKILL.md routes into
│       └── *.py            # Optional runtime scripts the skill invokes
└── commands/               # Optional slash-commands that provide deterministic
    └── <command>.md        #   entry points to a skill (see Skill Categories)
```

- [ ] **Step 2: Add a sentence explaining when each optional dir applies**

Immediately after the fenced block above (before the "Each skill is self-contained…" sentence), insert this paragraph:
```
`templates/`, `references/`, and a plugin-level `commands/` directory are all optional.
Use `references/` when a skill's `SKILL.md` grows long enough that splitting its supporting
material into routed documents keeps the entry file scannable. Add a `commands/` file when a
skill needs a *deterministic* invocation trigger: a skill is normally selected by description
match, but a skill whose purpose collides with a common word (e.g. "review") can lose that match
to a generic or built-in skill, and a slash-command guarantees the intended entry point.
```

- [ ] **Step 3: Note the review-gate pairing in Skill Categories (optional prose, no table change)**

The `## Skill Categories` **Review gate** row currently lists only `final-review`. Append `unbiased-review` to that row's Examples cell so the category table reflects both gates:
```
| **Review gate** | After a change, before commit — "final review before shipping"; or reviewing an artifact authored by another session | `final-review`, `unbiased-review` | Structured checklist / severity-ranked findings |
```

- [ ] **Step 4: Verify the edits landed and nothing else shifted**

Run:
```bash
grep -nE "references/|commands/|unbiased-review" CONTRIBUTING.md
```
Expected: the two new fenced-block lines, the `commands/` explanation paragraph, and the `unbiased-review` entry in the Review-gate row.

---

### Task 6: CHANGELOG + full-change verification + single commit

**Files:**
- Modify: `CHANGELOG.md`
- (Verification spans the whole change)

**Interfaces:**
- Consumes: all prior tasks.
- Produces: the commit.

- [ ] **Step 1: Add a CHANGELOG `### Added` entry under `## [Unreleased]`**

Under `## [Unreleased]`, add (create the `### Added` subheading if absent):
```markdown
### Added

- **`unbiased-review`** — A tenth skill: non-author review of an artifact (spec, plan, or implementation) produced by another session. Verifies the artifact's claims against the actual repo, grades TDD and hexagonal discipline, reproduces empirical claims in an isolated scratch clone, and reports severity-ranked findings with stable IDs — deliberately **without** writing the fix, so the author still defends their own work. Peer to `final-review` (that gates your own work pre-commit; this reviews someone else's), with interoperable severities. Generalized from an InterSystems-specific origin to a Python/JS-centric default. First skill in the plugin to ship `commands/` (four deterministic entry points: `/review-spec`, `/review-plan`, `/review-impl`, `/re-review`) and a `references/` subdirectory.
```

Also add a `### Changed` entry (create the subheading if absent):
```markdown
### Changed

- `CONTRIBUTING.md` documents two new optional skill-layout patterns — a `references/` subdirectory and a plugin-level `commands/` directory — and records `unbiased-review` alongside `final-review` as a review gate.
```

- [ ] **Step 2: Run pre-commit on all files**

Run:
```bash
cd ~/Development/agent-skills/mad-scientist-skills && pre-commit run --all-files
```
Expected: all hooks pass (end-of-file-fixer, trailing-whitespace, check-merge-conflict, check-added-large-files, check-json, detect-secrets). If a hook auto-fixes whitespace/EOF, re-run until clean and re-stage.

- [ ] **Step 3: Run the existing test suite (must be unaffected)**

Run:
```bash
python -m pytest tests -q
```
Expected: same pass/skip result as on `main` (the change ships no Python; nothing new collected).

- [ ] **Step 4: Final content sweep**

Run:
```bash
# exit-check grep (zero hits)
grep -riE 'iris|intersystems|objectscript|zpm|%csp|%unittest|%persistent|%status|\$\$\$assert|##class|cube|kpi|sc_data|angular|sc-framework' plugins/mad-scientist-skills/skills/unbiased-review plugins/mad-scientist-skills/commands
# version consistency
grep -RnE "1\.24\.0" plugins/mad-scientist-skills/.claude-plugin/plugin.json .claude-plugin/marketplace.json README.md
```
Expected: first grep empty; second shows `1.24.0` in all three.

- [ ] **Step 5: Stage and make the single commit**

Run:
```bash
cd ~/Development/agent-skills/mad-scientist-skills
git add -A
git status   # review: skill + references + 4 commands + plugin.json + marketplace.json + README + CONTRIBUTING.md + CHANGELOG + architecture.dsl (+ architecture.html if regenerated) + both design/plan docs
```
Then commit as a single change (author per Global Constraints, no trailers):
```bash
git commit --author="Karsten S. Nielsen <knielsen@intersystems.com>" -m "feat(unbiased-review): add non-author review skill (v1.24.0)"
```

**Note:** Per the working conventions, Claude authors and stages but the user runs the actual `git commit`/push and opens the PR. If executing inline, stop after `git status` and hand off unless the user has explicitly authorized the commit.

- [ ] **Step 6: PR body (hand to user)**

Draft a PR description covering: the new skill + its non-author-review purpose; the two structural firsts (`references/` subdir, `commands/` dir) **with the deterministic-trigger rationale** (a skill named around the generic word "review" loses the trigger to generic matching without a command — observed in practice) — and note that this PR also documents both patterns in `CONTRIBUTING.md` so the convention doc stays in sync; the generalization from InterSystems origin; version bump to 1.24.0; and whether `architecture.html` was regenerated or deferred.

---

## Self-Review

**Spec coverage** (design → task):
- Adaptation scope (3 edits) → Task 1 Steps 3–5. ✅
- Structure (references/ kept, commands/ added) → Task 1 Steps 1–2. ✅
- Wiring 1–2 (plugin.json/marketplace.json) → Task 2. ✅
- Wiring 3 (README count/badge/row/details/safety) → Task 3. ✅
- Wiring 4 (CHANGELOG) → Task 6 Step 1. ✅
- Wiring 5 (NO NOTICE) → Global Constraints (explicitly no task). ✅
- Wiring 6 (CI/pre-commit/pytest) → Task 6 Steps 2–3. ✅
- Wiring 7 (C4 DSL + HTML + fallback) → Task 4. ✅
- CONTRIBUTING.md blesses `references/` + `commands/` (maintainer decision, 2026-08-28) → Task 5. ✅
- Exit-check grep incl. ObjectScript tokens → Global Constraints + Task 1 Step 6 + Task 6 Step 4. ✅
- Delivery (branch, single commit, user pushes) → Global Constraints + Task 6 Steps 5–6. ✅
- Acceptance criteria → distributed across Task verifications. ✅

**Placeholder scan:** No TBD/TODO; every edit shows exact old/new text; grep commands are literal. ✅

**Type/name consistency:** DSL identifier `unbiasedReviewSkill` used consistently (Task 4 Steps 1–2, 6). Command names `/review-spec|review-plan|review-impl|re-review` consistent across Task 1, README (Task 3 Step 4), CONTRIBUTING (Task 5 Step 2), CHANGELOG (Task 6). Version `1.24.0` consistent (Tasks 2, 3, 6). ✅

---

## Post-review addendum (2026-08-28)

After Task 6, a final whole-branch review (APPROVE, 0 blocking) produced one fix round applied before
staging:

- **DSL description caps.** Both edited `architecture.dsl` descriptions exceeded the c4 assembler's
  200-char soft cap — the `unbiasedReviewSkill` container (202) and, as a regression introduced by the
  Task 4 "nine → ten skills" edit, the `plugin` software-system description (195 → 213). Both trimmed
  under 200 (197 and 198) and `architecture.html` re-rendered; the assembler now warns on neither.
- **Scratch-path label.** Two prose lines still named a `.scratch/` directory the skill never creates;
  reconciled to the real `${TMPDIR}/unbiased-review/` anchor in `SKILL.md` (Phase 5) and
  `references/isolation-protocol.md` (Teardown). See the design doc's post-review note.
- **README detail order.** The `unbiased-review` `## Skill Details` block was moved to last so the
  section is alphabetical and matches the `## Skills` table.

Re-review confirmed all fixes; pytest (239 passed) and `pre-commit` remained green.
