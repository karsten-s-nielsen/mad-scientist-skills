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
