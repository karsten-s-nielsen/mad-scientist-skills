# Spec review

A spec cannot be executed, but its claims about the codebase can be checked — and that is where most
of the value is. A spec's `file:line` references, counts, and measurements are the parts specific
enough to be wrong, and a wrong one propagates into every plan and commit built on it.

## Passes

### Claims about the tree

Verify all of them. `file:line` references, line counts, "the only X in the repo", quoted code,
argument orders, entry counts, script contents. Cheap to check with `Grep`, and the tally is what
makes the report credible.

Distinguish **wrong** from **imprecise**. "`app.routes.ts` is single-route" for a file with three
route entries and one page is imprecise: the substantive point holds. Report it as such and put it in
`CONSIDER`. Treating imprecision as error is how a review loses the author's attention for the two
findings that matter.

Claims about product source or external systems not in the repo go to *Could not verify* — but check
whether the repo-side **consequences** the spec predicts are confirmed. Confirmed consequences are
real indirect support for an unverifiable premise, and worth saying.

### Testability

Every behavioural claim needs a named test — see `tdd-rubric.md`, which is where checks 5 and 6 (does
a pipeline run it; does the named exemplar itself run) usually pay off on a spec.

A spec that lists test files without saying what each asserts has not specified tests; it has
specified filenames. Look for the named boundary case.

### Architecture

Grade per `hexagonal-rubric.md`. Grade each side of the system separately; asymmetry is a real
finding. Check that architectural vocabulary is used accurately — a label applied to a pattern that
does not have the property drains the word for everyone downstream, especially when the spec says
later tasks inherit the pattern.

### Internal consistency

Section counts against their own tables ("four failure modes" over five rows). Numbers that appear
twice. Commit plans against the component list. Non-goals against the design body. These are cheap
findings but they are also signals: an uncounted table row is usually the row added last, and the
last-added row often carries an unreviewed decision.

### Commit cadence

If the spec prescribes a commit plan or a commit workflow, hold it to `plan-review.md`'s *Commit
structure* bar: each commit a fully-tested, coherent rollback target. A spec that bakes in micro-commit
cadence — per-step commits, "commit often", a commit *count* target, or committing before a feature is
complete and its tests are green — is a `BLOCKING` finding, whatever upstream workflow it inherited it
from. A stream of half-tested commits is not a rollback target and not shippable history; the
"granular log" is noise that buries the tested checkpoints. Do not treat it as a matter of taste.

### Scope

YAGNI ruthlessly, in both directions. What is here that no stated requirement needs? What is missing
that the requirements imply? Scope growth the spec **declares** (an extraction that was not in the
original task) is usually fine — the declaration is the discipline. Undeclared growth is the problem.

Check the estimate. A spec that re-prices its own task upward rather than cutting tests to fit is
behaving correctly; say so.

### Non-goals

Read them as decisions, not as walls, and apply the challenge protocol in `SKILL.md`: override only
with the asymmetry and an escape hatch stated. A non-goal that was cheap when written can become
expensive because of what this very artifact adds — that asymmetry is the legitimate grounds for
raising it, and naming it is what separates a challenge from a re-litigation.

## Verdicts for specs

`REJECT` means the approach is wrong — a different design is cheaper than fixing this one. Rare, and
it should name the alternative.

`REQUEST CHANGES` on a strong spec is normal and not an insult. Say plainly which parts must not
change, so the author does not treat blocking findings as an invitation to redesign.
