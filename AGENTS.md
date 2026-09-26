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
