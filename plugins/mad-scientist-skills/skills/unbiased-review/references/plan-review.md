# Plan review

A plan is judged on whether someone else could execute it without re-deriving the spec's reasoning,
and on whether each step can be verified when it is done. Vagueness in a plan surfaces as improvisation
in the implementation.

## Passes

### Traceability

Every spec requirement maps to at least one step; every step traces to a requirement. Report both
gaps. Orphan steps are usually scope creep that entered between spec and plan — the place it most
often hides, because the spec was reviewed and the plan feels like mechanics.

If the spec was reviewed and has an open findings report, check the plan against the **findings** too:
a plan that faithfully implements a spec section a prior review flagged as blocking has inherited the
defect. Name the finding ID.

### Step granularity

A step should be completable and verifiable in one sitting, and state what "done" looks like. Steps
that say "implement the service" are not steps. Steps whose verification is "it works" are not
verifiable.

Watch for steps that are secretly several: an innocuous "wire it up" that spans three files and a
config change is where estimates die.

### Test-first ordering

Per `tdd-rubric.md` check 2. In a plan this is concrete: does each step write its failing test before
its implementation, and does the sequence go pure-core-first so mocks are needed only at the edges?

A plan whose first step is the outermost adapter will mock everything below it, and those mocks will
outlive their usefulness.

### Commit structure

Each commit must be a **fully-tested, coherent state** — a rollback target someone would actually
return to. "It compiles" and "its own micro-check passes" are not the bar: a commit that adds a
function "with no error handling yet", or that lands before the feature it belongs to is complete and
its tests are green, is a half-tested increment, not a valid rollback target. Check the claim rather
than accepting it: a commit that deletes a consumer's only data source while its replacement arrives in
the next commit is not independently valid, however it is described.

**Block micro-commit cadence — this is a `BLOCKING` finding, not a style note.** A plan that prescribes
committing per step, "after every change", "as soon as it compiles", a target commit *count* ("~N
small commits"), or otherwise optimises for granular history / easy bisecting rather than for each
commit being a tested, coherent unit — name the specific commits that land half-tested and raise it
`BLOCKING`. The named consequence: a stream of half-tested commits has no value — nobody bisects to or
rolls back to an untested state, so the "granular history" is noise that buries the real tested
checkpoints. That an upstream workflow recommends the cadence (an official skill, a house convention,
"standard incremental commits") is **not** a defence; in this project a commit that is not a
fully-tested, coherent state is not allowed, and a plan cannot inherit its way around that. The
legitimate unit is one commit per coherent, fully-tested change — a feature, a fix, a refactor with its
tests green — however many steps it took to build. Do not soften this to "consider batching"; the plan
must be restructured before it proceeds.

Check ordering dependencies that are real but unstated. If commit 3 needs commit 1's module, say so.

### Branch strategy

The plan should land on a single **feature branch** off the default branch — not a git worktree or other
parallel checkout, and not (without a stated reason) work fanned across several branches in one cycle.
Worktrees are a banned workflow here: flag any plan that proposes one. More than one feature branch per
cycle is the exception, not the default — flag it and ask for the reason. A plan that names its single
feature branch clears this silently.

### Commit authorization

No commit happens without the human's **explicit** approval. A plan step that commits — or otherwise
lands code — on its own authority is a `BLOCKING` finding, however routine the commit looks. "Commit
when green", "commit and open the PR", "commit each step" all fail this: they commit without a gate.
Named consequence: the session commits work the human never signed off on — the exact failure this
rule exists to prevent. The plan must reach "ready to commit", **stop for explicit approval**, and
commit only after it. A plan whose commit is gated on the human's approval clears silently. (Neither
"the tests pass" nor the plan itself listing the step is approval.)

### Verification steps

Does the plan say how to prove each step worked, with a runnable command? Does it name the suite, the
expected count, the host or container? A plan that defers all verification to the end has no feedback
loop, and the first failure will be attributed to the wrong step.

### Sequencing and prerequisites

What must be true before step 1 — a merged CI change, a running instance, a built native module. A
prerequisite discovered mid-implementation stops the work; a prerequisite named in the plan is a
scheduling decision. This is also where a prior review's "make it a merge prerequisite" escape hatch
should appear if the author took it.

### Estimates

Compare against the spec's estimate and against the step list. A plan that inherits an estimate the
spec already revised upward has a stale number.
