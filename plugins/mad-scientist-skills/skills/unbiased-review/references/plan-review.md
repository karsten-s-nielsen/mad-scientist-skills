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

Each commit independently valid — no step leaves the tree broken, and each can be dropped or reordered
if someone else lands a change first. Check the claim rather than accepting it: a commit that deletes a
consumer's only data source while its replacement arrives in the next commit is not independently
valid, however it is described.

Check ordering dependencies that are real but unstated. If commit 3 needs commit 1's module, say so.

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
