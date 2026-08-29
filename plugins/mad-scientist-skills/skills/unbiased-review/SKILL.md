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
   terminal, is a claim to verify — never the basis of a finding. This also covers the author's account
   of what the spec or plan required: read the approved document yourself. A paraphrase of the bar is
   narrative like any other, and reviewing against it lets the author quietly set their own scope.
4. **Every finding cites evidence** — `path:line`, a diff hunk, or a command and its actual output.
   No evidence means it is not a finding; it goes to *Could not verify*.
5. **"Could not verify" is mandatory.** An empty one requires justifying that nothing was assumed.
6. **Reproduce before reporting.** Never report an empirical failure your own scratch copy could have
   caused. Prove it reproduces from target state first.
7. **No praise-padding, no nitpick inflation.** A clean artifact gets `APPROVE` and the list of
   checks actually run. A `BLOCKING` finding must name the concrete consequence of shipping it.
8. **Scope is the human's to set — no session's.** No session, author or reviewer, may decide scope,
   defer work, drop or soften a requirement, lower the agreed quality bar, add a TODO, or record a
   follow-up without the human's explicit, recorded approval. So any deferral, "later", "out of scope",
   "good enough for now", or quality below the bar is a **finding** unless the record shows the human
   approved that exact reduction. You never grant the approval yourself, and you never park an
   unapproved reduction on a verdict or a follow-up line — an unsanctioned follow-up is the defect, not
   a way to dispose of one.

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

**Establish the bar.** Expectations are set by the approved spec and plan, not by the author's summary
of them. Locate them before judging any scope question: the spec/plan documents in the target —
**including uncommitted or untracked files sitting in the working tree**, which is where a spec/plan
written in the same session usually lives — plus any saved spec/plan review reports in the reviews
location (an approved review is the strongest source). Read the actual documents. If the author says
"the plan scoped this to X", open the plan and confirm; do not take the paraphrase. If no approved bar
exists anywhere, that absence is itself a finding and blocks `APPROVE` — you do not fall back to the
scope the author asserts.

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

**`APPROVE WITH FOLLOW-UPS` is not a place to park unapproved deferrals.** The follow-ups it carries
are items the *human* already approved deferring. An author-initiated deferral, TODO, or scope cut the
human never sanctioned does not become acceptable by being written on a follow-up line — it is the
defect itself (Hard rule 8), so it drives `REQUEST CHANGES`. And never `APPROVE` (with or without
follow-ups) an implementation whose scope you could confirm only from the author's account: an
unverified bar blocks approval on its own.

Findings get stable IDs — `<TASK>-<TYPE>-<NN>`, e.g. `D1-SPEC-03` — so later rounds can reference
them. Numbering continues across rounds; it never restarts.

## Challenging a non-goal

First, a non-goal only counts as documented if the **human** approved it. An author's own "out of
scope" / "deferred to a follow-up", declared in a handoff note, a commit message, or a `TODO`, is not
an approved non-goal — it is an unapproved scope decision (Hard rule 8), so it is a finding, not a
settled-ledger entry. The rest of this section applies only to non-goals the human approved.

An approved non-goal may be declared out of scope with reasons. You may still override that, but only
with both parts stated:

1. **The asymmetry** — what makes it this artifact's business now, when it wasn't before.
2. **An escape hatch** — an alternative resolution the author can take instead (usually sequencing:
   "then make it a merge prerequisite").

Without both, respect the documented decision and record it in the settled ledger.

## Red flags — you are rationalizing an unapproved cut

Any of these thoughts means STOP: the reduction is a finding, and you do not sign off until the human's
approval for it is in the record.

- "The author documented it as out of scope, so I'll respect it." — Only the *human's* documented
  non-goal gets respected. An author's is a finding.
- "It's reasonable engineering judgment / a pragmatic cut / the senior author decided." — Scope is not
  the author's call and not yours. Reasonableness never substitutes for the human's approval.
- "I'll `APPROVE WITH FOLLOW-UPS` and let them track it." — A follow-up the human did not sanction is
  the defect, not the disposition for one.
- "Per the author, the plan scoped it this way." / "The plan probably says read-path only." — Read the
  actual plan. A paraphrase of the bar is narrative (Hard rule 3).
- "The tests are green and the code is clean, so there's nothing to block on." — Green proves the
  delivered subset works, not that the subset was the authorized scope.

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
