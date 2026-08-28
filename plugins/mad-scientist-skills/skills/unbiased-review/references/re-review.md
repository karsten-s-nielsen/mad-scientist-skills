# Re-review

Round 2+. Two jobs: confirm the revisions were actually made, and catch anything the revisions broke.
One prohibition: do not re-litigate what round 1 settled.

Re-litigation is the failure mode that makes second reviews worthless. It reads as thoroughness and
costs the author a second argument about a decision they already made — so the constraint below is a
rule, not a preference.

## Setup

Read the prior report in full first. Extract:

- Every finding ID, its severity, and its **Resolved when** condition.
- The recorded `HEAD` and artifact `sha256`.
- Anything round 1 explicitly accepted or declined.

Then compute what changed:

```bash
shasum -a 256 <artifact>                      # vs recorded hash
git -C <target> diff <recorded-sha>..HEAD --stat
git -C <target> diff --staged --stat
```

For an unversioned artifact (a staged or working-tree doc), diff the text directly against the version
round 1 reviewed if it is still recoverable; otherwise say the comparison is by section, not by line,
and treat that as a limitation of the round.

## Job 1 — Verify each prior finding

One line per ID, with fresh evidence from the tree. **Never** accept the author's claim that they fixed
it; the whole point of the round is independent confirmation.

| Outcome | Meaning |
|---|---|
| `RESOLVED` | The **Resolved when** condition is met — verified, with evidence |
| `PARTIAL` | Addressed in part; state precisely what remains |
| `NOT ADDRESSED` | No change, or a change that does not meet the condition |
| `DECLINED` | Author explicitly rejected it, with reasons. A durable outcome — see below |
| `SUPERSEDED` | The change made it moot; explain why |

A fix that satisfies the letter of *Resolved when* but not the defect is `PARTIAL`, and say which. This
is where your round-1 wording gets audited: a condition that could be met without fixing the problem
was a badly written condition, and it is worth noting that too.

## Job 2 — New issues, scoped

**A new finding is admissible only if it is:**

1. in **changed content**, or
2. a prior judgement whose **basis the change invalidated** — and then it must name which judgement
   and what invalidated it.

Anything else is out of scope for this round, no matter how much you would like to raise it. If you
find something genuinely serious outside both categories, do not smuggle it in as a finding: put it in
a clearly labelled *Outside this round* note with one sentence, and let the author decide whether to
open it.

## The settled ledger

Carry forward, in the report, a short list of what is closed:

- Design decisions round 1 accepted or explicitly declined to challenge.
- `CONSIDER` items the author declined.
- Findings marked `RESOLVED` in an earlier round.

These may not be reopened unless rule 2 above applies. `DECLINED` is a durable outcome: an author who
declines a `CONSIDER` with reasons has decided, and re-raising it next round is a form of not
listening.

The ledger is cumulative — round 3 inherits round 2's.

## Verdict

Same vocabulary. Add one explicit regression line:

> Regression check: <what was re-run>, <result>. No previously-passing test now fails. / N now fail.

If nothing new was found and all blocking findings are resolved, say `APPROVE` plainly. A round 2 that
manufactures a finding to justify itself is worse than a round 2 that says "resolved, ship it" —
credibility is the only thing an unbiased reviewer has, and a clean bill of health is a real result.
