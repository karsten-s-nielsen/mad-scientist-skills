---
description: Round 2+ review — confirm revisions landed, catch regressions, do not re-litigate
argument-hint: <path to the revised artifact, or the prior report in reviews/>
---

Re-review a revised artifact.

Artifact: $ARGUMENTS

Use the `unbiased-review` skill. Read `references/re-review.md` first, then the reference for the
artifact's type and `references/output-contract.md`.

Two jobs, one prohibition. Confirm the revisions were actually made; catch anything the revisions
broke; **do not re-litigate what the last round settled.**

Start by reading the prior report in `reviews/` in full — every finding ID, its severity, its
*Resolved when* condition, the recorded `HEAD` and artifact `sha256`, and anything explicitly accepted
or declined. Then compute what changed before judging anything. If the artifact is unversioned, try to
recover the reviewed revision from loose git objects so the comparison is a real line-level diff rather
than a section-level guess; if it cannot be recovered, say so and treat it as a limitation of the round.

**Verify each prior finding from the tree with fresh evidence.** Never accept the author's claim that
they fixed it — independent confirmation is the entire point of the round. A fix that satisfies the
letter of *Resolved when* but not the defect is `PARTIAL`; say which. If the condition could be met
without fixing the problem, the condition was badly written, and **that is worth reporting too, plainly
and as your own error**.

New findings are admissible only if they are in changed content, or a prior judgement whose basis the
change invalidated. Anything else goes in a one-line *Outside this round* note.

Carry the settled ledger forward — resolved findings, accepted decisions, and declined `CONSIDER`s are
closed. `DECLINED` is durable; re-raising it is a form of not listening.

End with the explicit regression line. If everything blocking is resolved and nothing new turned up,
say `APPROVE` plainly — a round that manufactures a finding to justify itself is worse than one that
says "ship it".
