# Equivalence Verification

Reference for the Phase 12 equivalence sub-section. Load this whenever an optimization changes *how*
a result is computed — batch, vectorize, parallelize, cache, memoize, swap algorithm, JIT-compile.

**The rule:** an optimization must be **output-preserving**. Faster is worthless — or actively
harmful — if the output silently changed. Speed is necessary but never sufficient evidence that an
optimization is correct. Prove sameness with an **equivalence oracle**, or the change is not an
optimization but a scope decision (see `SKILL.md` Important Rules P1 and ADR-004).

Detection of *where* to apply this lives in Phase 0 (the "optimization without a parity test"
candidate grep) and the detection catalog; this template is the *gate* that lands the fix safely.

---

## Oracle test exists

When a hot loop / scalar path is vectorized, batched, parallelized, or JIT-compiled, the **original
implementation survives as a test-only reference** (the "legacy-loop oracle"), and the new
implementation is compared against it over a **battery of edge cases**, not just the happy path:

- varying sizes, including **non-power-of-two** and odd/prime lengths;
- validity / **NaN** / empty / partial-overlap inputs;
- single-item vs many-item;
- forced chunk sizes (1, ragged, all-in-one).

## Whole-output, production-scale, final compare

The closing gate is "compare **every** output column, **at production scale**, with the correct
equality" — not only per-unit parity tests. Unit parity is necessary, not sufficient: a batching bug
can be per-unit-correct and still wrong at the seams. Run the final compare on the real corpus, not a
100-row smoke sample (a benchmark green on 100 rows that OOMs or diverges on 3M rows is a false
green).

## Equality matches the contract

- **Bitwise** where the contract is exactness (integer results, byte-identical goldens, decision
  flags).
- A **stated numeric bound with the measured max reported next to it** where exactness is provably
  impossible (see `numeric-reproducibility.md` P5) — never a vague `atol` with no measured value.
- **NaN-aware** comparison where NaN is a valid payload (`equal_nan=True` or an explicit mask), not
  a silent "NaN != NaN" pass.

## Mutation-verify the oracle itself, both directions

Prove each parity/guard test can actually **fail**: apply a single deliberate defect to the
implementation, assert the test goes **RED**, then restore byte-for-byte. A **surviving mutation is a
finding about the test** — typically a one-sided assertion that must become two-sided — to be logged
and fixed, not silently patched. A parity test that cannot fail is decoration.

- *» e.g.* a numerics-parity test had a one-sided tie-break; a mutation survived until the assertion
  was made two-sided.

## Probe-first for platform-dependent identities

If the optimization's *correctness* depends on a numeric identity holding on the target
platform/library, verify it with a disposable ~20-line **probe** script **before** writing the real
implementation and its tests — far cheaper than discovering a parity failure afterward. If the probe
shows the identity is platform-dependent, route to `numeric-reproducibility.md` (scope the claim or
redefine the reference).

---

## Cross-stack illustrations (swappable)

- A rewritten **SQL** query must return the **same rows** (and order, if ordered), not merely run
  faster — diff the result sets at production row counts.
- A concurrent/parallel **reduce** must equal the **sequential** reduce.
- A **quantized/distilled** model must match the reference **within a stated tolerance**, measured.
- A **memoized** function must equal the un-memoized one on **every** key (and be immutable per
  `caching-strategies.md`).
- A **batched** API/DB call must return the same per-item results as the per-item calls it replaces.
