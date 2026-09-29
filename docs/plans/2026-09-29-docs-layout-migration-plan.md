# Docs-layout migration (specs / plans / ADRs split) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Split the flat `docs/plans/` (which mixes `-design.md`, `-plan.md`, `-research.md`) into three tracked, semantically-distinct top-level dirs — `docs/specs/` (designs + research), `docs/plans/` (plans), `docs/adrs/` (ADRs, unchanged) — and add a guard test so the bundling cannot recur.

**Architecture:** Mechanical `git mv` (history-preserving) of design/research docs into a new `docs/specs/`, a reference sweep across tests/skills/config, a guard test, and ADR-003 recording the layout policy. `docs/superpowers/` stays deliberately gitignored scratch. ADRs do not move. No shipped-payload change.

**Tech Stack:** Python 3 stdlib (`pathlib`), pytest, git.

**Spec:** This plan is the design of record (the migration was a bounded maintainer decision; directives captured here and in ADR-003). Cross-reference: the optimization-audit feature spec `docs/specs/2026-09-29-optimization-audit-equivalence-discovery-design.md` §11 "Dependency" assumes this migration has landed.

## Global Constraints

- **No version bump.** `docs/` is not in the shipped plugin payload (install cache holds only `.claude-plugin/` + `skills/`, per ADR-002). Zero installer impact.
- **One coherent commit, approval-gated.** Per repo commit discipline: NO per-task commits, NO micro-commits. Tasks 1–5 build the change; Task 6 is a single commit made only after the full suite is green, `/final-review` has run, the diff is shown, and the maintainer gives explicit approval for that specific commit.
- **Preserve history.** Move tracked files with `git mv`, never delete-and-recreate.
- **Tests:** stdlib-only, self-contained, read files with `encoding="utf-8"`, root-level guard under `tests/` (ADR-002).
- **Do not touch** `docs/adrs/` locations or `docs/superpowers/` (stays gitignored). Do not `git add` the untracked feature spec already sitting in `docs/specs/` — it belongs to the separate optimization-audit PR.
- **Branch:** `docs-layout-specs-plans-split` (already created off `main`).

---

### Task 1: Guard test (red first)

**Files:**
- Create: `tests/test_docs_layout.py`

**Interfaces:**
- Consumes: nothing (reads the filesystem).
- Produces: two guard tests other tasks must keep green.

- [ ] **Step 1: Write the failing test**

```python
"""Guard: design/research docs live in docs/specs/, never docs/plans/ (ADR-003).

Before ADR-003 the flat docs/plans/ held both -design.md and -plan.md, which let
a design doc (a spec) sit in a folder named "plans". This guard prevents that
bundling from recurring.
"""
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOCS = REPO_ROOT / "docs"


def test_no_design_or_research_docs_in_plans():
    plans = DOCS / "plans"
    stray = sorted(
        p.name
        for p in plans.glob("*.md")
        if p.stem.endswith("-design") or p.stem.endswith("-research")
    )
    assert stray == [], (
        "design/research docs must live in docs/specs/, "
        f"found in docs/plans/: {stray}"
    )


# The exact set the migration moves. Asserting the specific basenames (not just
# "some *-design.md exists") keeps the test genuinely red before Task 2 — the lone
# untracked feature spec already in docs/specs/ must NOT be enough to pass it.
MIGRATED = {
    "2026-03-08-observability-audit-design.md",
    "2026-03-08-optimization-audit-design.md",
    "2026-03-08-optimization-audit-research.md",
    "2026-03-27-documentation-audit-design.md",
    "2026-08-28-unbiased-review-skill-design.md",
    "2026-09-25-agents-md-alignment-design.md",
}


def test_migrated_designs_live_in_specs():
    specs = DOCS / "specs"
    assert specs.is_dir(), "docs/specs/ must exist (ADR-003)"
    present = {p.name for p in specs.glob("*.md")}
    missing = sorted(MIGRATED - present)
    assert not missing, (
        f"migrated design/research docs missing from docs/specs/: {missing}"
    )
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_docs_layout.py -v`
Expected: BOTH tests FAIL — `test_no_design_or_research_docs_in_plans` (the 6 design/research docs still sit in `docs/plans/`) and `test_migrated_designs_live_in_specs` (the 6 basenames are not yet in `docs/specs/`; the lone untracked feature spec there does not satisfy the set). This is the real red-first — DLM-PLAN-01.

---

### Task 2: Move design + research docs into docs/specs/

**Files:**
- Move (`git mv`) from `docs/plans/` → `docs/specs/`:
  - `2026-03-08-observability-audit-design.md`
  - `2026-03-08-optimization-audit-design.md`
  - `2026-03-08-optimization-audit-research.md`
  - `2026-03-27-documentation-audit-design.md`
  - `2026-08-28-unbiased-review-skill-design.md`
  - `2026-09-25-agents-md-alignment-design.md`
- Leave in `docs/plans/`: all `*-plan.md` (`observability-audit`, `optimization-audit`, `documentation-audit`, `unbiased-review-skill`, `agents-md-alignment`).

- [ ] **Step 1: Move the files**

```bash
cd /d/Development/karstenskyt__mad-scientist-skills
for f in 2026-03-08-observability-audit-design.md \
         2026-03-08-optimization-audit-design.md \
         2026-03-08-optimization-audit-research.md \
         2026-03-27-documentation-audit-design.md \
         2026-08-28-unbiased-review-skill-design.md \
         2026-09-25-agents-md-alignment-design.md; do
  git mv "docs/plans/$f" "docs/specs/$f"
done
```

- [ ] **Step 2: Verify the guard test now passes**

Run: `python -m pytest tests/test_docs_layout.py -v`
Expected: both tests PASS.

- [ ] **Step 3: Confirm git recorded renames, not delete+add**

Run: `git status --short docs/`
Expected: `R` (rename) entries for all six files; no `D`/`A` pairs.

---

### Task 3: Reference sweep

**Files:**
- Modify: `tests/test_agents_md_awareness.py` (module docstring, line ~3)
- Modify: `plugins/mad-scientist-skills/skills/optimization-audit/SKILL.md` (Phase 0.5 doc-scan table, ~line 283)
- Modify: `.gitignore` (the tracked-history comment, ~lines 26–27)

- [ ] **Step 1: Update the test docstring**

In `tests/test_agents_md_awareness.py`, change the path in the module docstring:
`docs/plans/2026-09-25-agents-md-alignment-design.md` → `docs/specs/2026-09-25-agents-md-alignment-design.md`.
(Verify first that this is a docstring comment, not a runtime file open — it is a reference in prose, so only the string changes.)

- [ ] **Step 2: Update the optimization-audit doc-scan table**

In `optimization-audit/SKILL.md`, the Phase 0.5 table row `| \`docs/plans/*.md\` | Phase-specific implementation plans |` gains a sibling row above it so both artifact locations are scanned:

```markdown
| `docs/specs/*.md` | Design/spec docs and research notes |
| `docs/plans/*.md` | Phase-specific implementation plans |
```

Read the surrounding table (offset ~278–288) first to match column count and formatting exactly.

- [ ] **Step 3: Update the .gitignore comment**

The comment currently reads (lines ~26–27):
`# committed. Deliberately narrower than \`docs/\`: \`docs/plans/\` and \`docs/adrs/\`` / `# are tracked project history and must stay that way.`
Change the enumeration to include specs: `\`docs/specs/\`, \`docs/plans/\` and \`docs/adrs/\``. The ignore line itself (`docs/superpowers/`) is unchanged.

- [ ] **Step 4: Sweep for any remaining stale references**

Run:
```bash
grep -rnE "docs/plans/[0-9]{4}-.*-(design|research)" --include="*.md" --include="*.py" \
  . 2>/dev/null | grep -v "^\./docs/"
```
Expected: no hits (every design/research reference now points at `docs/specs/`). Also grep the moved design docs and the staying `-plan.md` files for cross-references to a moved design's old `docs/plans/…-design.md` path and repoint any to `docs/specs/`.

- [ ] **Step 5: Confirm CONTRIBUTING/README/AGENTS need no change**

Run:
```bash
grep -rnE "docs/plans" CONTRIBUTING.md README.md AGENTS.md 2>/dev/null
```
Expected: no hits (these reference only `docs/adrs/`, which is unchanged). If a `docs/plans` mention surfaces, add a `docs/specs/` sibling and note it in the ADR's Project Guideline Amendment.

- [ ] **Step 6: Run the full suite**

Run: `python -m pytest -q`
Expected: all green, including `test_docs_layout.py` and `test_agents_md_awareness.py`.

---

### Task 4: ADR-003 (docs-layout policy)

**Files:**
- Create: `docs/adrs/ADR-003-docs-layout-specs-plans-split.md`

- [ ] **Step 1: Write the ADR (Nygard format, per `docs/adrs/ADR-TEMPLATE.md`)**

```markdown
# ADR-003: Documentation layout — split specs, plans, and ADRs

| Field | Value |
|---|---|
| **Date** | 2026-09-29 |
| **Status** | Accepted |
| **Deciders** | Karsten S. Nielsen |

## Context

`docs/plans/` historically held both `-design.md` (specs) and `-plan.md`, a flat
folder mixing two artifact types. A design doc therefore sat in a folder named
"plans" — the bundling that surfaced when a new optimization-audit design was
written to `docs/plans/`. Peer repos (silly-kicks) keep specs, plans, and ADRs as
three semantically-distinct directories.

This repo already half-anticipated the split: `documentation-audit/SKILL.md`
exempts `docs/specs/` as an internal-docs path, but no `docs/specs/` directory
existed — the reference was dangling.

`docs/superpowers/` is deliberately gitignored scratch (the `brainstorming` /
`writing-plans` skills default there; nothing under the path has ever been
committed). Any layout that tracks specs must not repurpose that scratch area.

## Decision

Tracked planning docs use three top-level, semantically-split directories:
`docs/specs/` (design docs and `-research.md`), `docs/plans/` (`-plan.md`),
`docs/adrs/` (ADRs). All are under `docs/` and committed. `docs/superpowers/`
remains gitignored scratch. Design and research docs never live in `docs/plans/`.

## Alternatives considered

| Option | Pros | Cons | Why rejected |
|---|---|---|---|
| A. Keep flat `docs/plans/` (both types) | Zero moves | Mixes artifact types; a design in a "plans" folder is exactly the bundling this fixes | Does not solve the problem |
| B. `docs/superpowers/{specs,plans,adrs}` (exact silly-kicks match) | Cross-repo path identity | Requires un-ignoring the deliberately-scratch `docs/superpowers/`, exposes never-committed scratch files, forces moving ADRs and rewriting every `docs/adrs/` cross-reference | Large blast radius; contradicts the scratch policy (Chesterton's Fence) |
| C. `docs/specs/` + `docs/plans/` + `docs/adrs/` top-level (chosen) | Makes reality match the repo's own `documentation-audit` reference to `docs/specs/`; no `.gitignore` change; ADRs unmoved; minimal and reversible | Contributors must learn the split; a docstring, a SKILL.md table, and the `.gitignore` comment need updating | — |

## Consequences

### Positive

- Three artifact types (spec / plan / decision) are structurally distinct and self-evident from the path.
- The repo's own `documentation-audit` reference to `docs/specs/` is no longer dangling.
- A guard test (`tests/test_docs_layout.py`) makes the bundling structurally impossible to reintroduce.

### Negative

- Tooling or muscle-memory that assumed "all planning docs in `docs/plans/`" must learn the split. Three call sites updated (test docstring, SKILL.md doc-scan table, `.gitignore` comment).

### Neutral

- **No version bump.** `docs/` is not in the shipped plugin payload (the install cache holds only `.claude-plugin/` + `skills/`, per ADR-002), so the reorg reaches no installer and needs no release. A repo-scoped `CHANGELOG.md` entry records it.
- Git records the six moves as renames, so history is content-preserving.
- The concurrent optimization-audit feature carries its own ADR-004 (output-preserving optimization); this ADR takes 003 because the migration lands first.

## Project Guideline Amendment

None required beyond the `.gitignore` comment, which is amended to list `docs/specs/` alongside `docs/plans/` and `docs/adrs/` as tracked project history. `CONTRIBUTING.md` references only `docs/adrs/` and is unchanged.

## Related

- **Repo files:** `tests/test_docs_layout.py` (new guard), `.gitignore` (comment), `tests/test_agents_md_awareness.py` (docstring), `plugins/mad-scientist-skills/skills/optimization-audit/SKILL.md` (doc-scan table)
- **Moved files:** six `-design.md`/`-research.md` docs, `docs/plans/` → `docs/specs/`
- **ADRs:** ADR-004 (output-preserving optimization) lands in the concurrent optimization-audit PR
- **Changelog:** `CHANGELOG.md` repo-scoped entry (no version)
- **Template:** `docs/adrs/ADR-TEMPLATE.md`
```

- [ ] **Step 2: No test for the ADR** — prose artifact. Confirm the file renders and links resolve by eye.

---

### Task 5: CHANGELOG entry (repo-scoped, no version)

**Files:**
- Modify: `CHANGELOG.md`

- [ ] **Step 1: Read the CHANGELOG head to match style**

Run: `python -m pytest -q` is not needed here; open the top of `CHANGELOG.md` (first ~40 lines) and find where repo-scoped, non-release entries live (the existing `.gitignore`/`docs/superpowers/` note at line ~68 is the style precedent — a `**repo**`-prefixed bullet).

- [ ] **Step 2: Add the entry**

Add, in the same style and section as the existing `**repo**` entry:

```markdown
- **repo** — split `docs/plans/` into `docs/specs/` (design + research docs) and `docs/plans/` (implementation plans), with `docs/adrs/` unchanged, so the three planning-doc types are structurally distinct. Design/research docs no longer sit in a folder named "plans". A guard test (`tests/test_docs_layout.py`) prevents regression. Docs are not in the shipped payload, so this carries no version bump. See ADR-003.
```

Place it under the current unreleased/most-recent-appropriate heading, matching how the line-68 entry is filed. Do not invent a new version heading.

---

### Task 6: Pre-commit gate + single commit (approval-gated)

- [ ] **Step 1: Full suite green**

Run: `python -m pytest -q`
Expected: all pass.

- [ ] **Step 2: Run `/final-review`**

Run the `final-review` skill. It regenerates `architecture.html` via Graphviz `dot`. No code changed, so the C4 output is expected to be byte-identical; if it produces a diff, stop and investigate before committing.

- [ ] **Step 3: Show the diff and the file list**

Run: `git status --short && git diff --stat HEAD`
Present the full staged picture to the maintainer. Confirm the untracked feature spec (`docs/specs/2026-09-29-optimization-audit-equivalence-discovery-design.md`) and `.serena/` are NOT staged.

- [ ] **Step 4: Commit only on explicit approval**

Do not run this until the maintainer says yes to this specific commit.

The six file moves are already staged by `git mv` (Task 2). Stage the rest with
**explicit paths only** — never `git add docs/specs/`, which would sweep in the
untracked feature spec that belongs to the separate optimization-audit PR:

```bash
git add tests/test_docs_layout.py \
        docs/adrs/ADR-003-docs-layout-specs-plans-split.md \
        docs/plans/2026-09-29-docs-layout-migration-plan.md \
        tests/test_agents_md_awareness.py \
        plugins/mad-scientist-skills/skills/optimization-audit/SKILL.md \
        .gitignore CHANGELOG.md
# Verify the feature spec is NOT staged:
git status --short | grep -q "^A.*optimization-audit-equivalence-discovery-design" \
  && { echo "ABORT: feature spec staged"; exit 1; } || true
git commit -m "$(cat <<'EOF'
docs: split docs/plans into docs/specs + docs/plans (ADR-003)

Design and research docs move to a new tracked docs/specs/; implementation
plans stay in docs/plans/; ADRs are unchanged in docs/adrs/. docs/superpowers/
stays gitignored scratch. A guard test prevents design docs from landing in
docs/plans/ again. No shipped-payload change, so no version bump.

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>
EOF
)"
```

- [ ] **Step 5: Push + PR only on explicit approval** (each a separate gate).

---

## Self-Review

**Spec coverage** (against the maintainer's directives):
- git mv preserve history → Task 2. ✓
- sweep every reference → Task 3 (docstring, SKILL.md, .gitignore, grep verification). ✓
- leave -plan.md in docs/plans/ → Task 2. ✓
- reconcile in-flight spec → already moved to docs/specs/ (untracked), kept out of this commit (Global Constraints, Task 6 Step 3). ✓
- migration as its own PR, lands first → whole plan; ADR-003 vs ADR-004 numbering (Task 4). ✓
- its own ADR → Task 4. ✓
- research folds into docs/specs/ → Task 2 (moves the -research.md). ✓
- guard test → Task 1. ✓
- no version bump → Global Constraints, Task 5, ADR Neutral. ✓

**Placeholder scan:** none — test code, ADR body, CHANGELOG entry, and commit message are all concrete. The two "read the surrounding file first" steps (SKILL.md table, CHANGELOG head) are format-matching confirmations, not deferred content.

**Type/name consistency:** guard test names (`test_no_design_or_research_docs_in_plans`, `test_migrated_designs_live_in_specs`) referenced consistently; `docs/specs/` path used identically throughout; the `MIGRATED` basename set matches Task 2's `git mv` list exactly (6 files).
