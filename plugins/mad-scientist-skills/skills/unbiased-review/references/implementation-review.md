# Implementation review

The only review where execution is available, so use it. Reading a diff tells you what the author
meant; running it tells you what they did.

## Establish the change

```
git -C <target> status --short
git -C <target> diff --staged --stat
git -C <target> diff --stat
git -C <target> ls-files --others --exclude-standard
git -C <target> log --oneline -10
```

Untracked files are part of the change. A review of staged-only content on a tree with untracked new
test files reviews the wrong change — and misses the tests entirely, which inverts every TDD finding.

## Passes

### Does it match the plan and the spec?

Three-way: spec intent, plan steps, actual diff. Report drift in both directions — code with no
corresponding step, and steps with no corresponding code. Where the spec was reviewed, check the
findings report; if a blocking finding was accepted and the code does not reflect it, that is a finding
with a known ID, not a new one.

### Run the tests

Isolated clone per `isolation-protocol.md`. Report the real numbers: files, tests, pass, fail, wall
time. Compare against whatever the author claimed.

If tests fail, establish the cause before reporting it and prove it reproduces from target state.
Pre-existing failures unrelated to the change are context, not findings — but count them, because "35
failures, 4 of them yours" is a materially different report than "35 failures".

### Red-green proof

Per `tdd-rubric.md`. Revert the implementation hunks, keep the new tests, run the suite. This is the
only way to distinguish tests written first from tests written to match. Do it for the change's core
assertions, not for every test.

### Architecture, by import graph

Grade per `hexagonal-rubric.md`, verified mechanically:

```
grep -rn "^import\|require(" <core files>       # what the core pulls in
```

Distinguish `import type` from runtime imports — the difference decides which tests can run without
infrastructure, and it is invisible in a diff review that only reads added lines.

New files are where architecture is set; edits to existing files inherit their surroundings. Judge
them by different standards and say which you applied.

### Code quality

Consistency with the surrounding file's idiom, error handling on every path that can fail, no swallowed
errors, no dead code, type safety (`any`, non-null assertions, unchecked casts), and no secrets. A
deviation from local idiom in a **new** file may be deliberate and correct — check whether the author
declared it, and hold declared deviations to a lower bar than undeclared ones.

### Error paths

Every failure mode in the spec should exist in the code, and every `catch` in the code should map to a
declared failure mode. Silent failures — an empty error handler, an error mapped to `null`, a rejected
promise with no handler — deserve particular attention: they are the defect class that hides other
defects, and they cost nothing to introduce.

### Security

Injection closed by construction rather than escaping, where possible. Client input that reaches a
query, a path, or a shell. Authorization on new routes. Anything logged that should not be.

## Reporting

Separate what the change broke from what was already broken. Give the pre-existing state its own line
so the author can see their own footprint clearly.
