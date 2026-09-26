# AGENTS.md Alignment Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan **inline in one session** on a single feature branch. No subagent fan-out, no worktrees, one final commit (per this repo's standing directive). Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the audit/review skills treat a consumer repo's `CLAUDE.md` and `AGENTS.md` as a pair, add a stdlib guard test that locks that in, and give this repo its own greenfield `AGENTS.md` (+ `CLAUDE.md` shim).

**Architecture:** Two-part content change plus a guard. Part A edits 6 SKILL.md files (2 read-list lines get `AGENTS.md` added; 15 cite lines change `CLAUDE.md` → `CLAUDE.md` / `AGENTS.md`). Part B adds repo-root `AGENTS.md` + a one-line `CLAUDE.md` = `@AGENTS.md` shim. A stdlib test (`tests/test_agents_md_awareness.py`) asserts both the read-list contract and broad cite anti-rot (with an explicit, empty allowlist).

**Tech Stack:** Markdown (skill content), Python stdlib (`pathlib`, `re`) + pytest for the guard. No new dependencies.

**Spec:** `docs/plans/2026-09-25-agents-md-alignment-design.md`

## Global Constraints

- **Never blanket-replace `CLAUDE.md` → `AGENTS.md`.** It is always *both* — a consumer repo may still keep a real `CLAUDE.md`. (Spec §3.1)
- **Match on exact strings, not line numbers.** Line numbers below are as measured at `9a10754`; earlier edits shift later lines within a file. (Spec §3.4)
- **Commit discipline (overrides the skill's per-task commit steps):** NO per-task commits, NO micro-commits. One fully-tested, coherent commit at the very end containing spec + plan + all code, and only after explicit maintainer approval. `commit → push → PR → merge` are four separate maintainer-gated actions.
- **Branch:** one feature branch off `main`; no worktree, no parallel checkout.
- **No version bump, no CHANGELOG entry** (owner decision, spec §2). Do not touch `plugin.json` / `marketplace.json` / README badge / CHANGELOG. `tests/test_version_consistency.py` must stay green (it will, unchanged).
- **No ADR** (owner decision, spec §2).
- **Never touch `~/.claude/CLAUDE.md`** (global instruction file).
- **New test:** stdlib only, `encoding="utf-8"`, deterministic; lives under `tests/` (ADR-002 — outside skill dirs).
- **Full `pytest` suite green** before done (`tests/skills/c4/*` untouched).

---

## File Structure

| File | Responsibility | Action |
|---|---|---|
| `tests/test_agents_md_awareness.py` | Guard: read-list contract + broad cite anti-rot | Create |
| `AGENTS.md` (repo root) | Greenfield contributor brief (dev conventions) | Create |
| `CLAUDE.md` (repo root) | One-line `@AGENTS.md` import shim (auto-load under Claude Code) | Create |
| `plugins/mad-scientist-skills/skills/cognitive-interface-audit/SKILL.md` | 1 read-list edit | Modify |
| `plugins/mad-scientist-skills/skills/documentation-audit/SKILL.md` | 1 read-list edit | Modify |
| `plugins/mad-scientist-skills/skills/architecture-audit/SKILL.md` | 5 cite edits | Modify |
| `plugins/mad-scientist-skills/skills/measure-before-optimize/SKILL.md` | 4 cite edits | Modify |
| `plugins/mad-scientist-skills/skills/final-review/SKILL.md` | 4 cite edits | Modify |
| `plugins/mad-scientist-skills/skills/optimization-audit/SKILL.md` | 2 cite edits | Modify |

TDD order: Task 1 writes the guard (both tests fail). Task 2 (read-list edits) makes `test_read_list_skills_list_agents_md` pass. Task 3 (cite edits) makes `test_no_claude_md_without_agents_md` pass. Task 4 adds Part-B files. Task 5 verifies + single gated commit.

---

## Task 0: Feature branch

- [ ] **Step 1: Create and switch to the feature branch off `main`**

Run:
```bash
git switch -c feat/agents-md-alignment
```
Expected: on a clean `feat/agents-md-alignment` off `9a10754`. No worktree.

---

## Task 1: Guard test (failing-first)

**Files:**
- Create: `tests/test_agents_md_awareness.py`

**Interfaces:**
- Consumes: repo layout only (`plugins/**/*.md`).
- Produces: two test functions `test_read_list_skills_list_agents_md`, `test_no_claude_md_without_agents_md`; a module-level `ALLOWLIST: set[tuple[str, str]]` (empty).

- [ ] **Step 1: Write the guard test**

```python
"""Guard: audit/review skills treat CLAUDE.md and AGENTS.md as a pair.

Two contracts (spec docs/plans/2026-09-25-agents-md-alignment-design.md §5):
  5.1  Every SKILL.md read-list line naming CLAUDE.md must also name AGENTS.md.
  5.2  Every line under plugins/**/*.md naming CLAUDE.md must also name AGENTS.md,
       except explicitly allow-listed lines.
"""
from __future__ import annotations

import re
from pathlib import Path

PLUGINS = Path(__file__).resolve().parent.parent / "plugins"
REPO_ROOT = PLUGINS.parent

# Read-list lines look like:  "- Read `CLAUDE.md`, `AGENTS.md`, `README.md`, ..."
READ_LIST_RE = re.compile(r"^\s*[-*]?\s*Read\b")

# (relative posix path, substring of the offending line) pairs that legitimately
# name only CLAUDE.md. EMPTY today — every CLAUDE.md line under plugins/ pairs with
# AGENTS.md. Each future entry MUST carry a comment explaining why the pairing does
# not apply to that line.
ALLOWLIST: set[tuple[str, str]] = set()


def _iter_lines(paths):
    for path in paths:
        rel = path.relative_to(REPO_ROOT).as_posix()
        for lineno, line in enumerate(
            path.read_text(encoding="utf-8").splitlines(), start=1
        ):
            yield rel, lineno, line


def test_read_list_skills_list_agents_md():
    offenders = [
        f"{rel}:{lineno}: {line.strip()}"
        for rel, lineno, line in _iter_lines(sorted(PLUGINS.rglob("SKILL.md")))
        if READ_LIST_RE.match(line) and "CLAUDE.md" in line and "AGENTS.md" not in line
    ]
    assert not offenders, (
        "Read-list lines naming CLAUDE.md must also name AGENTS.md "
        "(add `AGENTS.md` to the read list):\n" + "\n".join(offenders)
    )


def test_no_claude_md_without_agents_md():
    offenders = []
    for rel, lineno, line in _iter_lines(sorted(PLUGINS.rglob("*.md"))):
        if "CLAUDE.md" not in line or "AGENTS.md" in line:
            continue
        if any(a_rel == rel and sub in line for a_rel, sub in ALLOWLIST):
            continue
        offenders.append(f"{rel}:{lineno}: {line.strip()}")
    assert not offenders, (
        "Lines naming CLAUDE.md must also name AGENTS.md. Fix each by pairing it with "
        "AGENTS.md, or add (path, substring) to ALLOWLIST with a reason:\n"
        + "\n".join(offenders)
    )
```

- [ ] **Step 2: Run the guard, verify BOTH tests fail**

Run:
```bash
python -m pytest tests/test_agents_md_awareness.py -v
```
Expected: FAIL — `test_read_list_skills_list_agents_md` reports `cognitive-interface-audit/SKILL.md` and `documentation-audit/SKILL.md` read-list lines; `test_no_claude_md_without_agents_md` reports the 15 cite lines (e.g. `architecture-audit/SKILL.md:122`, `optimization-audit/SKILL.md:958`). If either passes now, STOP — the anchor/glob is wrong.

---

## Task 2: Part-A read-list edits (2)

**Files:**
- Modify: `plugins/mad-scientist-skills/skills/cognitive-interface-audit/SKILL.md`
- Modify: `plugins/mad-scientist-skills/skills/documentation-audit/SKILL.md`

- [ ] **Step 1: Edit `cognitive-interface-audit/SKILL.md` (~line 184)**

Old:
```
- Read `CLAUDE.md`, `README.md`, and any design docs or wireframes
```
New:
```
- Read `CLAUDE.md`, `AGENTS.md`, `README.md`, and any design docs or wireframes
```

- [ ] **Step 2: Edit `documentation-audit/SKILL.md` (~line 154)**

Old:
```
- Read `CLAUDE.md`, `README.md`, `CONTRIBUTING.md`, and any documentation config (mkdocs.yml, docusaurus.config.js, conf.py, etc.)
```
New:
```
- Read `CLAUDE.md`, `AGENTS.md`, `README.md`, `CONTRIBUTING.md`, and any documentation config (mkdocs.yml, docusaurus.config.js, conf.py, etc.)
```

- [ ] **Step 3: Run the read-list guard, verify it PASSES**

Run:
```bash
python -m pytest tests/test_agents_md_awareness.py::test_read_list_skills_list_agents_md -v
```
Expected: PASS. (`test_no_claude_md_without_agents_md` still FAILS — cite lines remain; that is expected until Task 3.)

---

## Task 3: Part-A cite edits (15)

**Files:**
- Modify: `plugins/mad-scientist-skills/skills/architecture-audit/SKILL.md` (5)
- Modify: `plugins/mad-scientist-skills/skills/measure-before-optimize/SKILL.md` (4)
- Modify: `plugins/mad-scientist-skills/skills/final-review/SKILL.md` (4)
- Modify: `plugins/mad-scientist-skills/skills/optimization-audit/SKILL.md` (2)

Each edit matches on enough of the line to be unique within its file. Rule: `CLAUDE.md` → `CLAUDE.md` / `AGENTS.md`, or add `` `AGENTS.md` `` to a filename list.

- [ ] **Step 1: `architecture-audit/SKILL.md` — 5 edits**

1. Old: `- Identify the **intended architecture** (from docs, CLAUDE.md, naming conventions, or team conventions):`
   New: `- Identify the **intended architecture** (from docs, CLAUDE.md / AGENTS.md, naming conventions, or team conventions):`
2. Old fragment: `documented in CLAUDE.md, ADRs, or deployment docs?`
   New fragment: `documented in CLAUDE.md / AGENTS.md, ADRs, or deployment docs?`
3. Old fragment: `ADR sections in README or CLAUDE.md)`
   New fragment: `ADR sections in README, CLAUDE.md, or AGENTS.md)`
4. Old fragment: `If CLAUDE.md says "workflows has zero Spark imports" — verify this is true`
   New fragment: `If CLAUDE.md / AGENTS.md says "workflows has zero Spark imports" — verify this is true`
5. Row (line ~495) — three substitutions in the one row:
   - `| CLAUDE.md as ADR source |` → `| CLAUDE.md / AGENTS.md as ADR source |`
   - `encode architectural decisions in CLAUDE.md or similar AI-assistant context files` → `encode architectural decisions in CLAUDE.md / AGENTS.md or similar AI-assistant context files`
   - `High (if CLAUDE.md contradicts code)` → `High (if CLAUDE.md / AGENTS.md contradicts code)`

- [ ] **Step 2: `measure-before-optimize/SKILL.md` — 4 edits**

1. Frontmatter `description:` (line ~3): Old fragment `flagged as a hot path in CLAUDE.md.` → New `flagged as a hot path in CLAUDE.md / AGENTS.md.`
2. Old: `- Before modifying a function flagged as a hot path in \`CLAUDE.md\`, \`CONTRIBUTING.md\`, or a performance-related document.`
   New: `- Before modifying a function flagged as a hot path in \`CLAUDE.md\`, \`AGENTS.md\`, \`CONTRIBUTING.md\`, or a performance-related document.`
3. Old: `Look up the function's budget from the project's CLAUDE.md or baselines file if available.`
   New: `Look up the function's budget from the project's CLAUDE.md / AGENTS.md or baselines file if available.`
4. Old fragment: `(from CLAUDE.md Performance Budgets)` → New `(from CLAUDE.md / AGENTS.md Performance Budgets)`

- [ ] **Step 3: `final-review/SKILL.md` — 4 edits**

1. Old: `- **CLAUDE.md**: Project instructions still valid? Architecture section matches reality? Test commands work?`
   New: `- **CLAUDE.md / AGENTS.md**: Project instructions still valid? Architecture section matches reality? Test commands work?`
2. Old fragment: `Prefer a procedure the repo documents (its \`CLAUDE.md\`, a \`RELEASING.md\`).`
   New fragment: `Prefer a procedure the repo documents (its \`CLAUDE.md\` / \`AGENTS.md\`, a \`RELEASING.md\`).`
3. Old fragment: `offer to record it (in the repo's \`CLAUDE.md\` or a \`RELEASING.md\`)`
   New fragment: `offer to record it (in the repo's \`CLAUDE.md\` / \`AGENTS.md\` or a \`RELEASING.md\`)`
4. Old: `- [x] CLAUDE.md accurate` → New: `- [x] CLAUDE.md / AGENTS.md accurate`

- [ ] **Step 4: `optimization-audit/SKILL.md` — 2 edits**

1. Old fragment: `= High. CLAUDE.md rule: "a benchmark that passes on 100 rows` → New: `= High. CLAUDE.md / AGENTS.md rule: "a benchmark that passes on 100 rows`
2. Old fragment: `any rule inherited from CLAUDE.md, ADRs, style guides, or comments` → New: `any rule inherited from CLAUDE.md / AGENTS.md, ADRs, style guides, or comments`

- [ ] **Step 5: Run the full guard, verify BOTH tests PASS**

Run:
```bash
python -m pytest tests/test_agents_md_awareness.py -v
```
Expected: PASS (both). If `test_no_claude_md_without_agents_md` still reports a line, an edit was missed — fix the exact line it names (do not add to `ALLOWLIST`; every line should pair today).

---

## Task 4: Part-B greenfield repo files

**Files:**
- Create: `AGENTS.md` (repo root)
- Create: `CLAUDE.md` (repo root)

- [ ] **Step 1: Create `AGENTS.md`**

```markdown
# AGENTS.md — Contributor guide for mad-scientist-skills

This is a Claude Code **plugin** repo: skills and slash commands under
`plugins/mad-scientist-skills/`. It ships no package — there is no
`pyproject.toml` or `package.json`. This file is the always-loaded contributor
brief; long-form docs live in `README.md`, `CONTRIBUTING.md`, and `docs/`.

## Before you change anything

- **Pre-change discipline (ADR-001):** run the relevant pre-change gate before
  editing perf- or contract-sensitive code (for example the
  `measure-before-optimize` skill before touching a benchmarked function).
- **Chesterton's Fence:** understand why a guard, rule, or convention exists
  before you remove it.

## Tests

- Tests live **outside** the skill directories (ADR-002), under `tests/`:
  `tests/skills/**` plus root-level guards, with `conftest.py` and `pytest.ini`.
- Run the full suite before declaring work done: `python -m pytest`.
- New tests are stdlib-only where practical and read files with
  `encoding="utf-8"`.

## Audit skills read both instruction files

Skills that read a consumer repo's project instructions must read **both**
`CLAUDE.md` and `AGENTS.md`, never one alone. A migrated repo's `CLAUDE.md` is a
one-line `@AGENTS.md` shim, so the real rules live in `AGENTS.md`; an unmigrated
repo may still keep a real `CLAUDE.md`. `tests/test_agents_md_awareness.py`
enforces this pairing across the shipped skills.

## Committing

- Do the work on **one feature branch** off `main` — never a worktree.
- One fully-tested, coherent commit per change; no micro-commits.
- Run `/final-review` before committing — it regenerates `architecture.html` via
  Graphviz `dot` (never PlantUML Smetana).
- `commit`, `push`, opening the `PR`, and `merge` are separate actions; each
  waits for explicit maintainer approval.
```

- [ ] **Step 2: Create `CLAUDE.md` (one-line import shim)**

```markdown
@AGENTS.md
```

- [ ] **Step 3: Verify the guard is unaffected**

Run:
```bash
python -m pytest tests/test_agents_md_awareness.py -v
```
Expected: PASS. (Root `AGENTS.md`/`CLAUDE.md` are outside `plugins/`, so the broad glob does not scan them; this step just confirms no regression.)

---

## Task 5: Full verification + single maintainer-gated commit

**Files:** none created; verification + commit only.

- [ ] **Step 1: Run the full test suite**

Run:
```bash
python -m pytest -q
```
Expected: all pass — the new guard, `tests/skills/c4/*`, and `tests/test_version_consistency.py` (version untouched).

- [ ] **Step 2: Run `/final-review`**

Invoke the `final-review` skill. It regenerates `architecture.html` via Graphviz `dot`.
Expected: a diff-free or legitimate re-render — this change alters no architecture. A non-trivial architecture diff is a signal to STOP and investigate (e.g. Smetana fallback), not to commit.

- [ ] **Step 3: Show the maintainer exactly what would be committed**

Run:
```bash
git status
git --no-pager diff --stat
```
Present the file list + stat. Confirm it contains only: the spec, this plan, the 6 SKILL.md edits, `tests/test_agents_md_awareness.py`, `AGENTS.md`, `CLAUDE.md`, and any legitimate `architecture.html` re-render — nothing else (no version files).

- [ ] **Step 4: STOP — wait for explicit maintainer approval to commit**

Do NOT run `git commit` until the maintainer says yes to this specific commit. "Tests green" is not approval.

- [ ] **Step 5: Single commit (only after approval)**

```bash
git add docs/plans/2026-09-25-agents-md-alignment-design.md \
        docs/plans/2026-09-25-agents-md-alignment-plan.md \
        tests/test_agents_md_awareness.py \
        AGENTS.md CLAUDE.md \
        plugins/mad-scientist-skills/skills/cognitive-interface-audit/SKILL.md \
        plugins/mad-scientist-skills/skills/documentation-audit/SKILL.md \
        plugins/mad-scientist-skills/skills/architecture-audit/SKILL.md \
        plugins/mad-scientist-skills/skills/measure-before-optimize/SKILL.md \
        plugins/mad-scientist-skills/skills/final-review/SKILL.md \
        plugins/mad-scientist-skills/skills/optimization-audit/SKILL.md
# add architecture.html only if it legitimately re-rendered
git commit -m "$(cat <<'EOF'
feat(skills): make audit/review skills read both CLAUDE.md and AGENTS.md

Audit and review skills that read a consumer repo's project instructions now
treat CLAUDE.md and AGENTS.md as a pair (a migrated repo's CLAUDE.md is an
@AGENTS.md shim). Adds a stdlib guard (read-list contract + broad cite anti-rot
with an explicit allowlist) and a greenfield repo-root AGENTS.md + CLAUDE.md
shim. No version bump (content alignment).

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>
EOF
)"
```

- [ ] **Step 6: STOP — push / PR / merge are separate maintainer-gated actions**

Do not push or open a PR without separate explicit approval.

---

## Self-Review (completed by plan author)

- **Spec coverage:** §3.2 → Task 2; §3.3 (all 15) → Task 3; §4 → Task 4; §5.1 + §5.2 → Task 1; §7 gates → Tasks 0 & 5; §2 no-bump/no-ADR → Global Constraints. No gap.
- **Placeholder scan:** no TBD/TODO; every edit gives exact old→new; test code is complete.
- **Type consistency:** test names, `ALLOWLIST` type, and `_iter_lines` signature are consistent across Task 1 and the run steps; guard function names match between Task 1 and Tasks 2/3 run commands.
