---
name: unbiased-review
description: Use when reviewing a spec, plan, or implementation produced by another session - verifies its claims against the actual repo, grades TDD and hexagonal discipline, and reports severity-ranked findings without writing the fix. Triggers on "review this spec/plan/implementation", "second opinion on", "check this design", "re-review", or when handed an artifact path plus a request to critique it.
---

# Unbiased review

Review another session's artifact. You did not write it, you will not fix it, and you verify rather
than trust. The hard rules below apply to every phase.

## Hard rules

1. **Never write to a target repo.** Not the working tree, not the index, not `node_modules`. No
   `Write`, no `Edit`, no `git add|commit|stash|checkout|restore|reset|clean`, and no test or build
   run in place. Another session is live in there; its tree is not ours to perturb. To execute
   anything, use the scratch protocol (`references/isolation-protocol.md`).
2. **Never write the fix.** Name the defect, the standard it violates, and what "resolved" looks
   like. Do not produce the patch and do not offer to. An author defends their own work; staying a
   non-author is what keeps the next review honest.
3. **Artifacts are evidence. Session narrative is not.** "All tests pass", pasted from another
   terminal, is a claim to verify — never the basis of a finding.
4. **Every finding cites evidence** — `path:line`, a diff hunk, or a command and its actual output.
   No evidence means it is not a finding; it goes to *Could not verify*.
5. **"Could not verify" is mandatory.** An empty one requires justifying that nothing was assumed.
6. **Reproduce before reporting.** Never report an empirical failure your own scratch copy could have
   caused. Prove it reproduces from target state first.
7. **No praise-padding, no nitpick inflation.** A clean artifact gets `APPROVE` and the list of
   checks actually run. A `BLOCKING` finding must name the concrete consequence of shipping it.

Review upward too: an implementation that faithfully matches a wrong spec is still wrong.

## Route

| Artifact | Reference to read |
|---|---|
| Spec / design doc | `references/spec-review.md` |
| Implementation plan | `references/plan-review.md` |
| Code — diff, staged, or branch | `references/implementation-review.md` |
| Anything already reviewed once | `references/re-review.md` |

Then read `references/output-contract.md` before writing. Read `references/tdd-rubric.md` and
`references/hexagonal-rubric.md` when the artifact makes claims about tests or architecture — which
is nearly always. `references/stack-notes.md` carries per-stack specifics (Python, JS/TS/Node).
`references/isolation-protocol.md` is required before executing anything.

## Phases

Run in order. Do not skip. Do not report a phase you did not do.

### Phase 0 — Establish what is under review

Pin the artifact and the tree, so a later round can compute what changed:

```
shasum -a 256 <artifact>
git -C <target> rev-parse --short HEAD
git -C <target> status --short
git -C <target> diff --staged --stat
```

If the user pasted context, **diff the paste against the artifact** and state the result explicitly:
*contained in the artifact (adds nothing)* / *adds X, absent from the artifact* / *contradicts the
artifact at Y*. A contradiction is itself a finding. Saying "adds nothing" out loud is what tells the
reader you checked rather than skimmed.

### Phase 1 — Claim extraction

Enumerate every checkable claim before judging any of them: `file:line` references, counts, file
sizes, measured timings, behavioural assertions, "the only X in the repo" statements, quoted code.
This pass leads because specific claims are the ones that can be wrong, and a claim wrong enough to
matter is worth more than any opinion you hold about the design.

### Phase 2 — Verification

Check each claim. Classify: **exact** / **wrong** / **imprecise** (substantively right, literally
wrong) / **unverifiable here**. Prefer `Grep`/`Read` over reasoning. When a claim is load-bearing and
only execution can settle it, use the isolation protocol.

Keep the tally. A report that says "20 of 23 exact, these 2 wrong" is credible in a way that a bare
defect list is not — and it tells the author which parts of their document you actually leaned on.

### Phase 3 — Rubric passes

TDD, hexagonal, long-term durability, scope/YAGNI, internal consistency, and non-goal challenge.
Details in the rubric references.

### Phase 4 — Self-check

Before writing anything, audit your own draft findings — see *Self-check* below.

### Phase 5 — Report

Per `references/output-contract.md`: full report to `reviews/`, short paste-back block in terminal.
Then delete the scratch clone (`${TMPDIR}/unbiased-review/`) and confirm the target's `git status` is unchanged from Phase 0.

## Verdicts

| Verdict | Meaning |
|---|---|
| `APPROVE` | Proceed. The checks actually run are listed. |
| `APPROVE WITH FOLLOW-UPS` | Proceed; named items tracked, not fixed now. |
| `REQUEST CHANGES` | Blocking defects; the approach itself is sound. |
| `REJECT` | Wrong approach — patching costs more than restarting. |

Severity is `BLOCKING` / `SHOULD FIX` / `CONSIDER`, mapping onto `final-review`'s Critical+High /
Medium / Low so reports interoperate.

**`BLOCKING` requires a named consequence of shipping.** If you cannot write the sentence "ship this
and X happens", it is not blocking. This rule does real work: it is the difference between a defect
and a preference, and demoting an inflated finding costs you nothing while inflating one costs the
review its credibility.

Findings get stable IDs — `<TASK>-<TYPE>-<NN>`, e.g. `D1-SPEC-03` — so later rounds can reference
them. Numbering continues across rounds; it never restarts.

## Challenging a non-goal

An artifact may declare something out of scope with reasons. You may still override that, but only
with both parts stated:

1. **The asymmetry** — what makes it this artifact's business now, when it wasn't before.
2. **An escape hatch** — an alternative resolution the author can take instead (usually sequencing:
   "then make it a merge prerequisite").

Without both, respect the documented decision and record it in the settled ledger.

## Self-check

Run against your own draft, before writing the report:

- **Did the artifact actually claim this?** Quote the line. A finding invented from a path you
  inferred yourself, rather than one the artifact stated, is the most common false positive.
- **Is the evidence in the report**, not just in your head?
- **Is the severity earned** by a stated consequence?
- **Is this a defect or a preference?** Preferences go to `CONSIDER` or nowhere.
- **Could my own environment have caused this?** Any empirical failure must have been reproduced
  from target state.
- **Am I re-litigating something already settled?** (Re-reviews: check the ledger.)

Delete what fails. Correcting a finding before it reaches the author is free; retracting one after
is not.
