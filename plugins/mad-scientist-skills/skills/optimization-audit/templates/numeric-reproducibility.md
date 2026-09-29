# Numeric Reproducibility & Determinism

Reference for Phase 11.5. Load this only when the codebase performs floating-point reductions, uses
BLAS/LAPACK/FFT or compiled numeric kernels (numba, Cython, C extensions, GPU), or ships numeric
goldens. Nothing here applies to a web backend, a SQL rewrite, or string processing.

The governing fact: **a floating-point result is not a value, it is a value plus a computation
order.** Reordering a reduction, or letting hardware/library dispatch pick a fused or vectorized
code path, changes the result bits. So "the same source" can produce different numbers across CPUs,
across SIMD/GPU code paths, and across library versions. Any bit-identity claim must either be scoped
to the environment where it was verified, or the reference redefined so no dispatcher can vary it.

Every check pairs with the equivalence discipline in `equivalence-verification.md`: detection here,
the oracle/mutation/whole-output gate there.

---

## Reduction-order sensitivity

Flag any *vectorize* / *batch* / "add a batch axis" refactor that reduces (sum / mean / dot /
`cumsum`) along an axis whose inputs may be **non-contiguous or reordered**. Summation is not
associative in floating point, so a pairwise/tree reduction and a sequential reduction differ by
1–2 ulp, silently.

**Check:** require an explicit contiguity/order re-assertion before the reduction (e.g.
`np.ascontiguousarray`, an asserted stride, an explicit sort), and a **bitwise oracle test at
multiple shapes** (including non-power-of-two and prime lengths).

- *» e.g.* fancy-indexing a middle axis returned a non-contiguous view; the reduction that followed
  became a sequential sum instead of a pairwise one — a 1–2 ulp drift, no exception, no warning.

| Language | Grep cue | Issue |
|----------|----------|-------|
| Python | `\.sum\(\|\.mean\(\|np\.dot\|@` immediately after fancy-indexing or `transpose`/`moveaxis` | Reduction over a possibly-non-contiguous axis |
| Any | a scalar accumulation loop replaced by a batched/tree reduction | Reduction-order change; needs a bitwise oracle |

## Dispatched fused ops break "compiled == reference bit-for-bit" as a portable claim

Before asserting a compiled/JIT kernel matches a reference **everywhere**, check whether the
reference itself routes through a CPU-dispatched **fused** path: **FMA** (fused multiply-add),
AVX-512-vs-AVX2 code selection, GPU atomics. A fused `a*b+c` keeps more intermediate precision than
the unfused form, so no single unfused compiled formulation can match the as-built reference on every
CPU.

**Check:** either scope the claim to "same machine / same ISA only", or **redefine the reference**
(see below) so it names one explicit, unfused formulation.

- *» e.g.* a complex multiply used **FMA** on the test CPU — 100% match to the FMA formula, 56% to
  the plain formula. No single compiled formulation matched the as-built reference on every CPU.

## BLAS/LAPACK calls are shape-dependent — do not batch them blind

A call that delegates to **BLAS/LAPACK** (`corrcoef`, matrix products, `solve`, `lstsq`, `svd`)
selects its routine and blocking by operand **shape**. Batching many small calls into one large call
commonly changes routine selection and therefore the result bits.

**Check:** probe for bit-identity *before* batching a BLAS/LAPACK call; sometimes the correct answer
is **not to batch** — keep the per-item call and document why.

## Library-version numeric drift — the version-fence test

Any bit-identity claim about a batched-vs-per-item, hand-replicated-vs-library, or
compiled-vs-library call must be re-verified on **every pinned CI version** (major *and* minor). A
**version-fence test** runs the real library call and compares, so a future dependency bump **fails
loudly** instead of drifting silently.

- *» e.g.* a batched FFT was per-row-identical on one scipy minor version but not the next; the fix
  was to keep per-item library calls plus a version-fence test. Separately, a Hilbert transform
  changed the **sign of exact zeros** between minor versions, forcing a version-aware fence.

## Substitution edge cases

A cheap-form substitution of a numeric identity must special-case its **singularities**, with a
dedicated test.

- *» e.g.* replacing `exp(i·angle(x))` with `conj(x)/|x|` diverges at `x = 0` (`1+0j` vs `NaN`);
  the fix is `where(|x| > 0, conj(x)/|x|, 1)` plus a zero-magnitude test.

## Conditioning, not precision

When a parity gate reports a surprisingly large delta on a **derived** column, check the transform's
**conditioning** — does its derivative blow up near the observed value? — before calling it a bug.
Trace the delta to its upstream primitive and check *that* bound.

- *» e.g.* an ulp-level change in a correlation surfaced as a ~1e-9° change in a downstream
  angle-spread whose derivative diverges as the correlation → 1. The primitive was fine; the
  transform amplified it.

---

## P5 — redefine-the-reference-once (the sanctioned exit)

When as-built numerics cannot be reproduced bit-exactly across platforms/backends/versions, the
correct move is **not** "accept a looser tolerance." It is:

1. Author **one** new reference formulation — explicit operations, a fixed and documented reduction
   order, no dispatched fused ops or transcendentals in the hot path.
2. Bound the new implementation against the old reference with a **stated, tested tolerance**, and
   report the **measured max next to the bound** (e.g. bound `1e-12`, measured `7.8e-16`).
3. Add a **decision-level no-flip gate** — prove no *decision* changed (not merely no value), run on
   the **full corpus**, not a sample.
4. When replacing an external dependency, enumerate its known defects as **documented divergences**
   with named regression tests, and freeze a **dev-only golden** against the old dependency before
   dropping it.

- *» e.g.* a native kernel reimplementation replaced a library dependency, fixed the library's bugs
  as ~11 named "documented divergences" each with a regression test, kept the old library as a
  pinned dev-only parity oracle, and gated on a full-corpus no-flip. Parity bounds were stated with
  the measured max beside them.

A redefinition is a **durable, recorded change** (ADR + changelog), distinct from any perf commit —
it changes *what* the reference is, even though it is chosen to preserve every decision.
