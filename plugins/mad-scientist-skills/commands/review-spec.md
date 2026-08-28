---
description: Unbiased review of another session's spec or design doc
argument-hint: <absolute path to the spec, or paste the spec text>
---

Review a **spec / design doc** you did not write.

Artifact: $ARGUMENTS

Use the `unbiased-review` skill. Read `references/spec-review.md` and
`references/output-contract.md`; add `references/tdd-rubric.md` and
`references/hexagonal-rubric.md` if the spec makes claims about tests or architecture, and
`references/stack-notes.md` for the platform specifics involved.

Run all six phases in order. Do not skip Phase 1 — enumerate every checkable claim before judging any
of them, because a spec's `file:line` references, counts, and measurements are the parts specific
enough to be wrong, and a wrong one propagates into every plan and commit built on it.

If the argument is a path, the target repo is its enclosing git repo: pin `HEAD`, `git status --short`
and the artifact's `sha256` before reading, so a later round can compute what changed. If the spec was
pasted rather than pointed at, say so in the report — the comparison is text-only and that limits what
Phase 2 can verify.

The skill's **Hard rules** apply. In particular: nothing is written to the target, `BLOCKING`
requires a named consequence of shipping, and *Could not verify* is mandatory.
