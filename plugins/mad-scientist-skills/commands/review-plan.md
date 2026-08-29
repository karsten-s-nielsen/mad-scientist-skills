---
description: Unbiased review of another session's implementation plan
argument-hint: <absolute path to the plan, or paste the plan text>
---

Review an **implementation plan** you did not write.

Artifact: $ARGUMENTS

Use the `unbiased-review` skill. Read `references/plan-review.md` and
`references/output-contract.md`, plus `references/tdd-rubric.md` (check 2, test-first ordering, is
concrete in a plan) and `references/stack-notes.md`.

A plan is judged on whether someone else could execute it without re-deriving the spec's reasoning,
and on whether each step can be verified when it is done.

Two things to establish before the rubric passes:

- **Find the spec this plan implements**, and check the plan against it in both directions — steps with
  no requirement, requirements with no step.
- **Check `reviews/` for a prior report on that spec.** If a blocking finding was accepted and the plan
  faithfully implements the defective section anyway, that is a finding with a **known ID**, not a new
  one. Cite the ID.

Verify commit-structure claims rather than accepting them: a commit that deletes a consumer's only data
source while its replacement arrives in the next commit is not independently valid, however it is
described.

The skill's **Hard rules** apply — including rule 2: name the defect and what "resolved" looks like,
never the patch.
