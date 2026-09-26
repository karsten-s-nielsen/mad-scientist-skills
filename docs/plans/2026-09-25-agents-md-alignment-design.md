# Design — `AGENTS.md` alignment for `mad-scientist-skills`

**Date:** 2026-09-25
**Author session:** `karstenskyt__mad-scientist-skills` (this session)
**Independent reviewer:** `silly-kicks` part-deux session, at spec / plan / impl
**Repo HEAD measured:** `9a10754` (`main`)

## 1. Problem

The ecosystem moved its project instructions from `CLAUDE.md` to `AGENTS.md`. In a
migrated consumer repo the `CLAUDE.md` is now a one-line `@AGENTS.md` shim, and the
real rules live in `AGENTS.md`. Any audit/review skill in this plugin that *reads* or
*cites* only `CLAUDE.md` therefore misses the rules in a migrated repo.

Not every consumer repo migrates, so a real `CLAUDE.md` may still exist. The correct
treatment is **both files, never a rename** — the exact inverse of the package-repo
`CLAUDE.md → AGENTS.md` sweep.

### 1.1 Measured reality (verified this session, not paraphrased from handoff)

| Fact | Value |
|---|---|
| Top-level / nested `CLAUDE.md` in repo | **NONE** (glob `**/CLAUDE.md` → empty) |
| Repo kind | Claude Code **plugin** (`plugins/mad-scientist-skills/{skills,commands}`); no `pyproject.toml` / `package.json` — not a published package |
| Plan/spec home | `docs/plans/` (tracked project history; `docs/superpowers/` is gitignored scratch) |
| ADR home | `docs/adrs/` (plural) |
| Tests | `tests/skills/c4/*` + `tests/test_version_consistency.py` — **no test asserts any audit skill's read-list**, so Part-A edits break no existing test |
| Commands dir + `unbiased-review` references | **zero** `CLAUDE.md` hits |

## 2. Scope (owner-set 2026-09-25)

| Part | Decision |
|---|---|
| **A** — make audit/review skills `AGENTS.md`-aware | **In scope** (core ecosystem win) |
| **B** — greenfield dev-facing `AGENTS.md` + `CLAUDE.md` shim for this repo | **In scope** (owner: "Include it") |
| Guard test (stdlib) — read-list contract + broad cite anti-rot (allowlist) | **In scope** (owner: "Add the test"; gold-standard two-assertion design per MSS-SPEC-01) |
| ADR recording the convention | **Out of scope** (owner: "No ADR") |
| Plugin version bump + CHANGELOG entry | **Out of scope** (owner: "No bump") — treated as a non-shipping content-alignment edit; `test_version_consistency` stays green because no version string changes |

Nothing here is deferred or dropped except by the owner decisions recorded above.

## 3. Part A — skill edits

### 3.1 Rule (applied per line, verified against the surrounding sentence)

- **Read-list line** (`Read \`CLAUDE.md\`, …`): add `` `AGENTS.md` `` to the list.
- **Cite / file-list line** (instruction file named as a source of rules / ADRs / budgets):
  `` `CLAUDE.md` `` → `` `CLAUDE.md` / `AGENTS.md` ``, or add `` `AGENTS.md` `` to the list.
- **Anti-pattern / finding text** that already names both files: **leave**.
- **Never blanket-replace** `CLAUDE.md` → `AGENTS.md`. It is always *both*.

### 3.2 Read-list edits (2)

| Loc | Before | After |
|---|---|---|
| `cognitive-interface-audit/SKILL.md:184` | Read `CLAUDE.md`, `README.md`, and any design docs or wireframes | Read `CLAUDE.md`, `AGENTS.md`, `README.md`, and any design docs or wireframes |
| `documentation-audit/SKILL.md:154` | Read `CLAUDE.md`, `README.md`, `CONTRIBUTING.md`, and any documentation config … | Read `CLAUDE.md`, `AGENTS.md`, `README.md`, `CONTRIBUTING.md`, and any documentation config … |

### 3.3 Cite / file-list edits (15)

| Loc | Change |
|---|---|
| `architecture-audit/SKILL.md:122` | "from docs, CLAUDE.md, naming conventions…" → "from docs, CLAUDE.md / AGENTS.md, naming conventions…" |
| `architecture-audit/SKILL.md:459` | "documented in CLAUDE.md, ADRs, or deployment docs" → "documented in CLAUDE.md / AGENTS.md, ADRs, or deployment docs" |
| `architecture-audit/SKILL.md:490` | "ADR sections in README or CLAUDE.md" → "ADR sections in README, CLAUDE.md, or AGENTS.md" |
| `architecture-audit/SKILL.md:491` | "If CLAUDE.md says 'workflows has zero Spark imports' — verify" → "If CLAUDE.md / AGENTS.md says …" |
| `architecture-audit/SKILL.md:495` | Row: label "CLAUDE.md as ADR source" → "CLAUDE.md / AGENTS.md as ADR source"; body "encode … in CLAUDE.md or similar" → "in CLAUDE.md / AGENTS.md or similar"; severity "High (if CLAUDE.md contradicts code)" → "High (if CLAUDE.md / AGENTS.md contradicts code)" |
| `measure-before-optimize/SKILL.md:3` (`description:` frontmatter) | "flagged as a hot path in CLAUDE.md." → "flagged as a hot path in CLAUDE.md / AGENTS.md." |
| `measure-before-optimize/SKILL.md:14` | "hot path in `CLAUDE.md`, `CONTRIBUTING.md`, or …" → "hot path in `CLAUDE.md`, `AGENTS.md`, `CONTRIBUTING.md`, or …" |
| `measure-before-optimize/SKILL.md:54` | "budget from the project's CLAUDE.md or baselines file" → "budget from the project's CLAUDE.md / AGENTS.md or baselines file" |
| `measure-before-optimize/SKILL.md:144` | "(from CLAUDE.md Performance Budgets)" → "(from CLAUDE.md / AGENTS.md Performance Budgets)" |
| `final-review/SKILL.md:82` | "**CLAUDE.md**: Project instructions still valid?…" → "**CLAUDE.md / AGENTS.md**: Project instructions still valid?…" |
| `final-review/SKILL.md:101` | "(its `CLAUDE.md`, a `RELEASING.md`)" → "(its `CLAUDE.md` / `AGENTS.md`, a `RELEASING.md`)" |
| `final-review/SKILL.md:105` | "(in the repo's `CLAUDE.md` or a `RELEASING.md`)" → "(in the repo's `CLAUDE.md` / `AGENTS.md` or a `RELEASING.md`)" |
| `final-review/SKILL.md:162` | "- [x] CLAUDE.md accurate" → "- [x] CLAUDE.md / AGENTS.md accurate" |
| `optimization-audit/SKILL.md:958` | "CLAUDE.md rule: …" → "CLAUDE.md / AGENTS.md rule: …" |
| `optimization-audit/SKILL.md:1100` | "inherited from CLAUDE.md, ADRs, style guides, or comments" → "inherited from CLAUDE.md / AGENTS.md, ADRs, style guides, or comments" |

### 3.4 Explicitly left unchanged

- `documentation-audit/SKILL.md:507` — anti-pattern row ("Monolithic AGENTS.md/CLAUDE.md that merely restates…"), already names both.
- `documentation-audit/templates/repo-architecture.md:60` — same anti-pattern, template copy.
- Already-aware read-lists: `architecture-audit:112`, `final-review:25`, `observability-audit:115`, `optimization-audit:284` & `:344`, `security-audit:122`.

Line numbers are as measured at `9a10754`; the implementation matches on the exact
string, not the line number, since earlier edits shift later lines within a file.

## 4. Part B — greenfield repo dev files

Two new **repo-root** files (dev-facing; **not** part of the shipped plugin payload
under `plugins/`):

- **`AGENTS.md`** — terse dev conventions for working *in this repo*:
  - ADR-001 pre-change discipline; ADR-002 tests live outside skill directories.
  - Test layout: `tests/skills/**`, `conftest.py`, `pytest.ini`; run `pytest` before done.
  - `/final-review` before commit (regenerates `architecture.html` via Graphviz `dot`).
  - Commit discipline: one fully-tested commit per change; `commit → push → PR → merge`
    are separate owner-gated actions; no worktrees, one feature branch off `main`.
  - One line noting audit skills read **both** `CLAUDE.md` and `AGENTS.md`.
- **`CLAUDE.md`** — a single line `@AGENTS.md` (import shim; auto-loads under Claude
  Code, verified at CC 2.1.280) so Claude Code sessions pick up `AGENTS.md`.

Content stays short and non-duplicative of README/CONTRIBUTING/ADRs (which remain the
long-form home). This dogfoods the very `CLAUDE.md`+`AGENTS.md` convention Part A audits for.

## 5. Guard test

`tests/test_agents_md_awareness.py` — stdlib only (`pathlib`, `re`), `encoding="utf-8"`,
byte/line reads only. **Two assertions** (gold-standard anti-rot: precise contract +
broad co-occurrence + documented escape hatch), resolving reviewer finding MSS-SPEC-01
per owner direction ("gold standard, scope not a concern"). This **supersedes** the
narrow read-list-only design the reviewer approved.

### 5.1 `test_read_list_skills_list_agents_md` — precise read-list contract

1. Glob `plugins/**/skills/**/SKILL.md`.
2. For each line matching the read-list anchor `^\s*-?\s*Read\b` **and** containing
   `CLAUDE.md`, assert the same line also contains `AGENTS.md`.
3. The `Read` anchor targets exactly the read-list contract; failure names the offending
   skill + line so the diagnostic is specific ("cognitive-interface-audit read-list
   missing AGENTS.md"), not a generic line hit.

Failing-first: fails against the pre-edit `cognitive-interface-audit:184` and
`documentation-audit:154` read-lists; the §3.2 edits turn it green (TDD).

### 5.2 `test_no_claude_md_without_agents_md` — broad cite anti-rot

1. Glob `plugins/**/*.md` (skills, commands, templates, references — the shipped payload).
2. For every line containing `CLAUDE.md`, assert it also contains `AGENTS.md`, **unless**
   the `(relative_path, line_text_substring)` is in an explicit module-level `ALLOWLIST`.
3. `ALLOWLIST` is **empty today** — verified: all 25 `CLAUDE.md` lines under `plugins/**`
   pair with `AGENTS.md` on the same line post-edit (17 edited + 6 already-aware +
   `documentation-audit:507` + `templates/repo-architecture.md:60`). Each future entry
   must carry a one-line comment stating why that line legitimately names only `CLAUDE.md`.
4. Failure output prints `file:line`, the offending text, and the fix instruction (pair
   it with `AGENTS.md`, or add to `ALLOWLIST` with a reason).

Rationale (MSS-SPEC-01): the narrow guard alone left the 15 cite edits (§3.3) unprotected
against a silent revert to `CLAUDE.md`-only. Same-line co-occurrence is a deterministic
proxy (no fuzzy paragraph logic — YAGNI); the `ALLOWLIST` is the Chesterton's-fence escape
hatch so a genuinely `CLAUDE.md`-only line forces a conscious, commented exception rather
than a silent gap. Enforce broadly, document exceptions explicitly.

Failing-first: with an empty `ALLOWLIST`, fails against the pre-edit cite lines that name
only `CLAUDE.md` (e.g. `architecture-audit:122`, `optimization-audit:958`); the §3.3 edits
turn it green.

## 6. Non-goals / out of scope

- No blanket `CLAUDE.md → AGENTS.md` rename anywhere.
- No edits to already-aware read-lists or to anti-pattern finding text (§3.4).
- No ADR (owner decision).
- No version bump, no CHANGELOG entry (owner decision).
- No changes to `c4` code or its tests; no architecture change.
- `~/.claude/CLAUDE.md` (global) is never touched.
- Historical / consumer-facing `CLAUDE.md` mentions in `docs/**` and `README.md` are
  left (they describe past cycles or a consumer's file), re-confirmed: none is a live
  rule-text pointer for *this* repo.

## 7. Gates & workflow

- **Branch:** one feature branch off `main` (no worktree).
- **TDD:** guard test failing-first → Part-A edits green → full `pytest` suite green
  (`tests/skills/c4/*` untouched, must stay green).
- **`/final-review`** before the commit; re-renders `architecture.html` with Graphviz
  `dot` (not Smetana). This change alters no architecture, so a diff-free/legitimate
  re-render is expected; a non-trivial diff would be a signal to investigate.
- **Commit:** a single, fully-tested commit containing spec + plan + skill edits +
  Part-B files + guard test. No micro-commits.
- **Owner gates:** `commit`, `push`, `PR`, `merge` are four separate actions, each
  requiring explicit owner approval; this session commits nothing without it.
- **Review:** the part-deux session reviews spec / plan / impl independently; this
  author session runs **no** `/review-*` on its own work. Reports land in
  `D:\Development\_reviews\` as `2026-09-2X-mad-scientist-skills-agents-md-*.md`.

## 8. Risk / edge cases

- **Line drift:** editing earlier lines shifts later line numbers; implementation keys
  on exact strings, so drift is harmless.
- **Guard over-match (§5.1):** an already-aware read-list already contains `AGENTS.md`, so
  it passes; no false failure today.
- **Broad guard false-positive (§5.2):** a future line legitimately naming only `CLAUDE.md`
  trips `test_no_claude_md_without_agents_md`. This is intended — the fix is to pair it with
  `AGENTS.md` (usually correct) or add a commented `ALLOWLIST` entry. `ALLOWLIST` is empty
  today (all 25 lines pair post-edit, verified).
- **`description:` edit:** widening `measure-before-optimize`'s description to name
  `AGENTS.md` only broadens its trigger surface; no test snapshots the description.
- **Shim precedence:** adding a root `CLAUDE.md`=`@AGENTS.md` does not re-introduce a
  "monolithic CLAUDE.md" — it is one import line, and the audit skills treat both files.
