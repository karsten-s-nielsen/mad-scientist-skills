# ADR-004: An optimization must be output-preserving

| Field | Value |
|---|---|
| **Date** | 2026-09-29 |
| **Status** | Accepted |
| **Deciders** | Karsten S. Nielsen |

## Context

The `optimization-audit` skill measured whether a change was **faster**. It never checked whether the
change **still produced the same result**. For a whole class of optimizations — batching,
vectorizing, parallelizing, caching, swapping an algorithm, JIT-compiling a kernel — "faster" is
worthless, or actively harmful, if the output silently changed. Extended optimization cycles surfaced
the same failure repeatedly: a parallel reduce that reordered a floating-point sum, a batched library
call whose routine selection changed the bits, a cache that served a stale value, a dependency
upgrade that flipped an assumption inside a caught-and-ignored exception.

The discipline that made those cycles safe was a single rule applied everywhere: an optimization ships
only behind proof that its output is unchanged, and a change to *what* is computed is a separate,
human-approved decision — never folded into a "performance" commit.

This rule is not one skill's behavior; it is enforced by four skills that must agree on it:
`optimization-audit` (detects and gates), `measure-before-optimize` (captures the pre-change output
snapshot), `unbiased-review` and `final-review` (verify a "byte-identical" claim was actually proven).
That cross-skill scope is what makes it a repo-wide policy rather than a local edit.

## Decision

**An optimization must be output-preserving; changing *what* is computed is a scope decision that
requires explicit human sign-off and must never be laundered as a performance change.**

Every performance finding is classified `optimization` (output-preserving, shipped behind an
equivalence gate) or `scope-decision` (changes the output — needs approval, reported as a decision). A
fidelity reduction with no recorded approval is itself a finding.

## Alternatives considered

| Option | Pros | Cons | Why rejected |
|---|---|---|---|
| A. No ADR — leave it as prose in `optimization-audit` | Less ceremony | The rule spans four skills; without a shared record they drift, and a reviewer has no authority to cite | The policy is cross-cutting; a single skill's prose cannot bind the others |
| B. Accept a looser numeric tolerance when exact reproduction is hard | Simple | Hides a real output change behind a fuzzy bound; a decision *did* change even if a value did not | Rejected in favor of the redefine-the-reference discipline (`numeric-reproducibility.md` P5), which states and tests the bound and gates on no decision flipping |
| C. Output-preserving principle as a repo-wide ADR the four skills cite (chosen) | One authority; every skill references it; a reviewer can cite it; the detection→verification chain is explicit | One more governance document to maintain | — |

## Consequences

### Positive

- A change to *what* is computed can no longer hide in a "performance" commit — it is a named,
  approved scope decision or it is a finding.
- The detection catalog (D1–D6) and the equivalence gate (`equivalence-verification.md`) are two
  halves of one chain: detection says *here is redundant work*, verification says *here is how to
  prove the fix did not move the numbers*.
- Reviewers (`unbiased-review`, `final-review`) have a citable rule for challenging a "byte-identical"
  claim that was only smoke-tested.

### Negative

- Every optimization now carries a proof obligation (an oracle test, a whole-output production-scale
  compare). This is deliberate cost — it is what the rule buys.

### Neutral

- This ADR is **004**, not 003: the docs-layout migration (ADR-003) landed first as its own PR, and
  ADR numbers follow landing order.
- Ships in `1.27.0`, which changes the shipped skill payload (new phase, two templates, new rules).

## Project Guideline Amendment

None. The rule is documented in `optimization-audit/SKILL.md` (Important Rules + Phase 13
classification) and mirrored in the three peer skills; no `CONTRIBUTING.md`/`README.md` governance
rule is amended.

## Related

- **Plugin files:**
  - `plugins/mad-scientist-skills/skills/optimization-audit/SKILL.md` — Important Rules (P1/P19/P20), Phase 12 equivalence posture, Phase 13 classification
  - `plugins/mad-scientist-skills/skills/optimization-audit/templates/equivalence-verification.md` — the oracle gate
  - `plugins/mad-scientist-skills/skills/optimization-audit/templates/numeric-reproducibility.md` — P5 redefine-the-reference
  - `plugins/mad-scientist-skills/skills/measure-before-optimize/SKILL.md` — output-snapshot pointer
  - `plugins/mad-scientist-skills/skills/unbiased-review/SKILL.md`, `.../final-review/SKILL.md` — the review-side mirror
- **Spec / plan:** `docs/specs/2026-09-29-optimization-audit-equivalence-discovery-design.md`, `docs/plans/2026-09-29-optimization-audit-equivalence-discovery-plan.md`
- **ADRs:** ADR-003 (docs-layout migration) landed immediately before this one
- **Changelog:** `CHANGELOG.md` entry for `[1.27.0]`
- **Template:** `docs/adrs/ADR-TEMPLATE.md`
