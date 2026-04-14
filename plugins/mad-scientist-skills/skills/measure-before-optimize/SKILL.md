---
name: measure-before-optimize
description: Pre-change measurement gate for perf-sensitive functions. Use BEFORE modifying any function that has a pytest-benchmark test, appears in a performance baselines file, or is flagged as a hot path in CLAUDE.md. Captures baseline median and p95, verifies the change does not regress beyond a configurable threshold, reports the delta. Peer skill to optimization-audit — this one is pre-change; that one is retrospective.
---

# Measure Before Optimize

A pre-change measurement discipline that captures a performance baseline, gates the change on a regression threshold, and reports the delta. Designed as a peer to `optimization-audit`: this skill is pre-change, that one is retrospective.

## When to use this skill

- Before modifying a function that has a `pytest-benchmark` test.
- Before modifying a function listed in the project's performance baselines file (commonly `docs/performance-baselines.md` or `docs/benchmarks.md`).
- Before modifying a function flagged as a hot path in `CLAUDE.md`, `CONTRIBUTING.md`, or a performance-related document.
- When the user says "optimize X", "speed up Y", "this function is slow", or similar performance-intent phrases.
- When a task touches tracking-scale data, Spark UDFs with strict memory budgets, or any code in a documented hot loop.

## What this skill is NOT for

- Retrospective performance audits — use `optimization-audit` instead.
- First-time benchmark creation — if no benchmark exists for the function being modified, warn the user and offer to add one, but do not block. This skill gates CHANGES to measured functions, not the creation of new ones.
- Micro-benchmarks of framework internals that you do not own.
- Production profiling — this skill runs local micro-benchmarks only, not production traces.

## Workflow

### Phase 1: Identify the measurement surface

Read the project's baselines file (default: `docs/performance-baselines.md`). Extract the table of benchmarked functions. If the file is a JSON baselines file, parse it directly. If neither exists, `grep` for `@pytest.mark.benchmark` or `benchmark(` invocations in `tests/` and `src/tests/`.

Build a set of "measured functions" — functions with known benchmarks. Cross-reference with the function being modified.

- **If the function is in the measurement surface**: proceed to Phase 2.
- **If the function is NOT in the measurement surface**: warn the user:
  > "The function `<name>` is not currently benchmarked. I can add a `pytest-benchmark` test before modifying it, or you can proceed without a baseline. Which?"
- **Do not block** — the user may have a good reason to proceed without a baseline.

### Phase 2: Capture baseline

Run the matching `pytest-benchmark` test before any code change:

```bash
uv run pytest <test_path>::<test_name> --benchmark-only --benchmark-min-rounds=3 --benchmark-json=<scratch_file_pre>
```

Write the scratch file to `tempfile.gettempdir()` (typically `%TEMP%` on Windows, `/tmp/` on Linux). **NEVER write to the project root** — the scratch file must not be accidentally committable.

Parse the JSON output. For each benchmark in `benchmarks[]`:
- `stats.mean` or `stats.median` (median is preferred — more robust to outliers)
- `stats.hd15iqr` or `stats.iqr_outliers` (p95 equivalent)
- `stats.rounds`
- `stats.ops`

Look up the function's budget from the project's CLAUDE.md or baselines file if available.

Report to the user:

```
Baseline captured — <function_name>
  median:   <value> µs
  p95:      <value> µs
  rounds:   <count>
  budget:   <budget> (from <source>)
  headroom: <pct>% of budget
```

### Phase 3: Yield to the main agent

Exit the skill at this point. The main agent makes the planned code change. The skill reactivates when the user (or main agent) indicates the change is complete and it is time to re-measure. The skill does NOT attempt to wrap or supervise the code change itself.

### Phase 4: Re-run the benchmark

Run the same benchmark command with a different scratch file suffix (e.g., `.post.json` instead of `.pre.json`):

```bash
uv run pytest <test_path>::<test_name> --benchmark-only --benchmark-min-rounds=3 --benchmark-json=<scratch_file_post>
```

### Phase 5: Compare and report

Calculate:
- `delta_median_pct = (new_median - baseline_median) / baseline_median * 100`
- `delta_p95_pct = (new_p95 - baseline_p95) / baseline_p95 * 100`

Report to the user:

```
## Measure-before-optimize report

Function: <function_name>
Budget:   <budget>

             baseline       new            delta
median       <v> µs         <v> µs         <±%>
p95          <v> µs         <v> µs         <±%>

Budget status:        <within / over> budget (<pct>% of budget)
Regression threshold: <threshold>% (default 10%)
Result:               <within threshold / EXCEEDS THRESHOLD / IMPROVEMENT>
```

**If delta exceeds the regression threshold (default 10%)**: escalate to the user with the full delta and ask whether to proceed, revert, or investigate. Do not silently accept a regression.

**If delta is negative (improvement)**: report the improvement explicitly and suggest updating the baselines file to reflect the new floor. Do not update the file automatically.

## Parameters

Resolved from natural language or default. The skill never asks for these — it uses defaults unless the user names a parameter explicitly.

| Parameter | Default | Description |
|---|---|---|
| `baselines_file` | `docs/performance-baselines.md` | Path to the project's baselines markdown or JSON |
| `regression_threshold` | `10%` | Percent regression that escalates to user prompt |
| `budget_enforcement` | `warn` | `warn` (report and ask) or `block` (halt execution) |
| `benchmark_rounds` | `3` | `pytest-benchmark --benchmark-min-rounds` — raise for more stable measurements |

## Comparison to optimization-audit

| Attribute | optimization-audit | measure-before-optimize |
|---|---|---|
| **Timing** | Retrospective (after code exists) | Pre-change gate |
| **Trigger** | "Audit this codebase for perf issues" | "About to touch a measured function" |
| **Output** | Audit report with prioritised issues | Before/after delta, regression flag |
| **Scope** | Whole codebase | Single function / small change |
| **Action** | Recommends fixes | Gates the change |

Both skills share the theme of "don't change perf-sensitive code on vibes." They are designed to be invoked independently and do not overlap.

## Example invocation

**User:** "I'm going to rewrite `compute_pitch_control_at_points` to use a batched NumPy approach instead of the per-player loop."

**Claude:** Invokes `measure-before-optimize`.

**Skill Phase 1:** Reads `docs/performance-baselines.md`. Finds `compute_pitch_control_at_points` with median 347 µs, p95 512 µs, budget ≤5 ms.

**Skill Phase 2:** Runs `uv run pytest src/tests/test_pitch_control_benchmark.py::test_pitch_control_batched --benchmark-only --benchmark-min-rounds=3 --benchmark-json=%TEMP%/pitch_control_pre.json`. Reports baseline:

```
Baseline captured — compute_pitch_control_at_points
  median:   347 µs
  p95:      512 µs
  rounds:   3
  budget:   ≤5 ms (from CLAUDE.md Performance Budgets)
  headroom: 93.1% of budget
```

**Skill Phase 3:** Exits. Main agent makes the change.

**Skill Phase 4 (after change):** Same command with `%TEMP%/pitch_control_post.json`.

**Skill Phase 5:** Reports:

```
## Measure-before-optimize report

Function: compute_pitch_control_at_points
Budget:   ≤5 ms

             baseline       new            delta
median       347 µs         362 µs         +4.3%
p95          512 µs         534 µs         +4.3%

Budget status:        within budget (7.2% of 5 ms)
Regression threshold: 10% (default)
Result:               within threshold
```

If the new median had been 402 µs (+15.8%), the skill would have escalated.

## Important rules

- **Never write scratch baseline files to the project root.** Always use `tempfile.gettempdir()`. Scratch files that end up committed are a workflow smell.
- **Report BOTH delta-vs-baseline AND position-vs-budget.** A function at 70% of budget can absorb a 20% regression without blowing budget; a function at 95% cannot. Both numbers are load-bearing for the operator's decision.
- **The threshold is a prompt, not a block.** Operator judgment decides whether a regression is acceptable. This skill surfaces the delta; the operator decides.
- **Do not attempt this skill if no benchmark exists.** Warn and exit — creating benchmarks is a separate workflow that deserves its own TDD pass.
- **Use `--benchmark-min-rounds=3` for fast checks, `--benchmark-min-rounds=10` for stable measurements.** The default is set for fast feedback; raise it when the delta is borderline and you need more confidence.
