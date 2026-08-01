# ADR-002: Tests live outside skill directories

| Field | Value |
|---|---|
| **Date** | 2026-07-30 |
| **Status** | Accepted |
| **Deciders** | Karsten S. Nielsen |

## Context

A skill directory is not a source tree — it is a shipping container. When a user installs this plugin, Claude Code downloads `plugins/mad-scientist-skills/` and nothing else: the install cache for 1.21.1 holds exactly `.claude-plugin/` and `skills/`. Repo-root files (`CONTRIBUTING.md`, `docs/`, `.github/`, `CHANGELOG.md`) are never fetched. Whatever sits inside a skill directory ships **verbatim** to every installer, forever.

The `c4` skill has the plugin's only runtime Python module, `c4_assemble.py`, and it grew a real test suite — 15 files, 161 tests, 105K — parked at `skills/c4/tests/`. That suite is developer infrastructure, but because of where it lived it was installed on every machine that ever installed the plugin. Two thirds of the `c4` skill's files and 44% of its bytes (15 of 22 files, 105K of 239K) was test code that no user or Claude session will ever execute. Nothing else in the plugin has this problem, because nothing else ships code.

Two further forcing functions surfaced while examining this:

1. **The suite was ungated.** CI ran only `pre-commit` (file hygiene and secret scanning). No job ran `pytest`, so the 161 tests passed or failed purely at the contributor's discretion. The v1.21.1 fixes were behaviour changes to a module whose tests nothing verified in CI.
2. **`SKILL.md` is a prompt, and a skill directory is its context surface.** Files beside `SKILL.md` are candidates for a model to read while executing the skill. A `tests/` directory of twelve test modules and a 33K SVG fixture is noise on that surface, competing with the runtime files that matter.

Moving the tests out is free for the developer and non-negotiable for the installer: the top-level `tests/` tree costs installers exactly zero bytes because repo-root paths are not part of the download.

## Decision

Tests live in a top-level `tests/` tree that mirrors the skill path (`tests/skills/<skill-name>/`), never inside a skill directory. A skill directory holds only what the skill needs at runtime. A root `conftest.py` puts each skill directory that ships an importable module on `sys.path`, and a `pytest` CI job gates the suite on every PR.

## Alternatives considered

| Option | Pros | Cons | Why rejected |
|---|---|---|---|
| A. Keep `skills/c4/tests/`, exclude it at package time | Zero file moves; tests stay adjacent to the module they exercise, which is the Python default | There is no package step to hook — Claude Code copies the skill directory as-is, so there is nowhere to apply an exclusion; would require the marketplace spec to grow an ignore mechanism that does not exist | No mechanism exists; the fix would have to land upstream in Claude Code, not here |
| B. Keep tests in place and accept the payload | No change at all; preserves sibling imports | Every installer downloads 105K/15 files of dead weight in perpetuity, and the cost grows with every skill that gains a runtime module; leaves fixture noise on the skill's context surface | Cost is permanent, borne by users, and compounds per skill |
| C. `tests/c4/` — flat, not mirroring the plugin path | Shorter paths | Loses the correspondence to `plugins/<plugin>/skills/<skill>/`; ambiguous if the repo ever hosts a second plugin | Path should mirror the thing it tests so the mapping needs no explanation |
| D. `tests/skills/<skill-name>/` with a root `conftest.py` (chosen) | Skill payload holds runtime files only; mirrors the plugin path exactly; one `sys.path` setup instead of one per module; the tree is a natural home for future skills' tests | Tests no longer import the module under test as a sibling, so a `conftest.py` is now load-bearing; a contributor adding a runtime module to a new skill must add it to the conftest tuple | — |

## Consequences

### Positive

- The `c4` skill's installed payload drops from **239K / 22 files to 134K / 7 files**; the whole plugin from **1236K / 63 files to 1131K / 48 files**. The tests are still in the repo and still run — they just stop shipping.
- The suite is now gated: 159 of the 161 tests run in CI, the other two being the real-render integration tests, which skip on a runner without the Structurizr/PlantUML toolchain. A new `pytest` CI job runs `python -m pytest tests -q` on every PR and push to `main`. Verified to actually fail, not merely pass: reverting the `TAIL_GROUPS` fix from v1.21.1 turns the job red — `1 failed, 158 passed, 2 skipped` with the toolchain absent as in CI, `1 failed, 160 passed` locally with it present — so the gate has teeth.
- `sys.path` manipulation moves from 12 duplicated per-file inserts to one documented place.
- A skill directory now means one thing — runtime payload — which is a rule a contributor can apply to a new skill without being told.
- The `tests/` tree gives future skills with runtime modules an obvious home, so this decision does not need re-litigating per skill.

### Negative

- `conftest.py` is load-bearing, and what it costs is narrower than it first appears. Any `python -m pytest` invocation still works from any working directory — pytest walks up to `rootdir` and loads the root `conftest.py`, so both `python -m pytest tests` and a single module by absolute path resolve the import from an unrelated cwd. What no longer works is running a test file as a bare script (`python tests/skills/c4/test_matcher.py`), which is exactly what the twelve deleted per-file `sys.path` inserts used to buy; that now raises `ModuleNotFoundError`. Since `rootdir` inference is what makes the conftest discoverable, a root `pytest.ini` pins it explicitly rather than leaving it dependent on how the suite is invoked.
- Adding a skill with an importable Python module requires editing the `conftest.py` tuple. This is documented in `CONTRIBUTING.md`, but it is a step that did not exist before and will be forgotten at least once.
- `test_cli_main.py` shells out to the assembler rather than only importing it, so it needs the shipped path and `conftest.py` cannot help. It resolves the repo root by walking up from `__file__`, which couples one test module to its own depth in the tree. Commented in place.
- Tests are no longer adjacent to the code they exercise, which is the Python convention this repo previously followed. The reviewer's habit of "open the skill, see its tests" is broken; the mirrored path is the compensation.

### Neutral

- `.gitignore`'s `__pycache__/` rule already covers the new location; no ignore changes were needed.
- The `.secrets.baseline` needed no update — detect-secrets keys its baseline entries by path, and its one entry is an unrelated template that this commit does not move.
- No runtime file changed. `c4_assemble.py` is untouched, so plugin behaviour is byte-for-byte identical. This still ships as **v1.21.2** — a patch, since nothing was added to the shipped surface and it only got smaller — because the version is the install cache key: the cache lives at `~/.claude/plugins/cache/.../<version>/`, so an existing install keeps its copy of the tests until the version changes. Without a bump the payload reduction reaches nobody who already installed.
- Git recorded all 15 files as renames, so the move reads as content-preserving in history rather than as a delete-and-re-add.

## Project Guideline Amendment

`CONTRIBUTING.md` "Repository Structure" previously described only the in-plugin skill tree and stated that "each skill is self-contained in its own directory," with no guidance on where tests belong. This ADR amends it to state that a skill directory ships verbatim and therefore holds only runtime files, and to document the `tests/skills/<skill-name>/` mirror, the root `conftest.py` and its per-skill tuple, the `python -m pytest tests -q` invocation, and the `pytest` CI job that gates it.

## Related

- **Plugin files:**
  - `plugins/mad-scientist-skills/skills/c4/c4_assemble.py` — the plugin's only runtime Python module, and so the only skill this affects today
- **Repo files:**
  - `conftest.py` — new; makes each skill directory importable for its tests
  - `pytest.ini` — new; pins `rootdir` at the repo root so the conftest is found regardless of invocation
  - `tests/skills/c4/` — the relocated suite, 15 files
  - `.github/workflows/ci.yml` — new `pytest` job
  - `CONTRIBUTING.md` — "Repository Structure" amended per the section above
- **ADRs:** none superseded
- **Template:** `docs/adrs/ADR-TEMPLATE.md`

## Notes

The decision was forced by measuring the install rather than reading the spec. The install cache at `~/.claude/plugins/cache/mad-scientist-skills/mad-scientist-skills/1.21.1/` contains `.claude-plugin/`, `.in_use`, and `skills/` — and `skills/c4/tests/`, all 15 files of it. That the repo-root files are absent from the same cache is what makes the top-level `tests/` tree free: the asymmetry between "inside a skill directory" and "anywhere else in the repo" is total, and it is the entire basis for this decision.

The `pytest` job was checked in both directions. Passing on green proves little, so the `TAIL_GROUPS = {"DSL"}` fix from v1.21.1 was reverted to `set()` and the suite re-run: `test_dsl_group_sorts_last_despite_unknown_group` failed and the run exited non-zero, both with the render toolchain present (`1 failed, 160 passed`) and with it hidden to mimic the runner (`1 failed, 158 passed, 2 skipped`). A CI job that cannot fail is decoration, and this one is not.

The suites import only the stdlib, so the CI job installs nothing but `pytest`. Most of them read a pre-rendered SVG fixture rather than invoking a renderer; the one module that does render for real, `test_integration_render.py`, shells out to Structurizr and PlantUML behind a `skipUnless` gate on Java, the two jars, and a passing `-testdot` Graphviz check. So CI needs no PlantUML, Graphviz, or JRE — but note that those two tests skip there rather than run, and CI's green covers 159 tests, not all 161.
