# Design: optimization-audit equivalence + discovery improvements

**Date:** 2026-09-29
**Status:** Draft — revised after round-1 independent review (2026-09-29)
**Skills touched:** `optimization-audit`, `measure-before-optimize`, `unbiased-review`, `final-review`
**Source handoff:** `D:\Development\_handoffs\2026-09-29-mad-scientist-skills-optimization-audit-improvements-handoff.md`
**Target release:** 1.27.0 (minor — new capability)

---

## 1. Context and motivation

Optimization work across several silly-kicks cycles surfaced a class of problems the
`optimization-audit` skill cannot currently catch. An independent analysis session
distilled that work into a handoff proposing 24 checks (P1–P24) plus, in a later
revision, a 7-row detection catalog (D1–D7). This design selects and structures a
subset of those proposals into a coherent change set.

Two facts were verified against the current repo before designing:

1. **The gap is real.** Greps across `optimization-audit/SKILL.md`, `measure-before-optimize/SKILL.md`,
   and all eight templates return zero hits for output/numeric equivalence, floating-point
   determinism, bit-identity, fixed-cost-floor, cache immutability, blast-radius, and
   silent-version-degradation. Every "equivalent" / "deterministic" / "oracle" hit in the
   current text is incidental prose (network equivalent, deterministic profiler, Oracle DB
   license). The skill checks whether a change is *faster*; it never checks whether the change
   *still produces the same result*.
2. **`measure-before-optimize` is timing-only.** It captures median/p95 before and after and
   compares against a threshold. It captures no output snapshot, so it cannot detect that an
   optimization moved the numbers.

### The two goals (detection is the priority)

The maintainer's stated priority is **detection**: the optimizations in these cycles took
extended, manual profiling sessions to find, and the audit should have flagged most of them on
a first pass. The design therefore treats the detection catalog as the primary deliverable and
the equivalence machinery as the verification half that lets a detected fix land safely.

- **Detection — surface the opportunity.** Turn each hard-won find into a grep, structural, or
  profiling cue so the tool flags it automatically. Leverage: a check that fires once has paid
  for itself on every future run.
- **Verification — land it safely.** Once found, a numeric optimization is only safe if it is
  proven output-preserving, or its output change is explicitly signed off.

The two chain: a detection check without a matching verification gate tempts an unsafe fix; a
verification gate with no detection check never fires. Every detection row below cross-links to
the verification proposal that lands it.

---

## 2. Scope

### 2.1 In scope

| Group | Items | Summary |
|-------|-------|---------|
| **Detection catalog (priority)** | D1–D6 (D7 already present) | Opportunity cues wired into Phases 0/2/9/12, each cross-linked to its verification gate |
| **Tier 1 — thesis** | P1, P2, P3 | Output-preserving-vs-scope classification; equivalence oracle template + Phase 12 extension; regressions/trade-offs report section |
| **Tier 2 — numeric hazards (conditional)** | P4, P5 | New conditional Phase 11.5 + `numeric-reproducibility.md` template (FP determinism, redefine-the-reference) |
| **Tier 2 — cache/version hazards** | P6, P7, P8 | Cache immutability + identity-keyed-cache; silent-version-degradation grep; blast-radius / consumer enumeration |
| **Tier 3 — measurement rigor** | P9, P10, P11, P12, P13, P15, P17, P18 | Fixed-cost floor, warm-vs-cold, budget granularity, op-count guards, instrumentation no-op, noise floor, shape inventory, profiling posture |
| **Tier 4 — process/gate** | P19, P20, P23, P24 | Correctness-fix gets own cycle; plan-diff; guard + companion share one threshold constant; guard size-ladder |
| **Cross-skill** | Handoff deliverables 6, 7 | `measure-before-optimize` output-snapshot pointer; `unbiased-review` / `final-review` parity-at-production-scale mirror |
| **Governance record** | ADR-004 | The output-preserving principle as repo-wide policy, referenced by all four skills (ADR-003 is reserved for the docs-layout migration, a separate PR landing first) |

### 2.2 Deferred (approved)

These were surfaced and explicitly approved for deferral; they are recorded here so a reviewer
can confirm nothing was silently dropped.

| Item | Reason deferred |
|------|-----------------|
| P14 (headline numbers from shipped instrumentation, not a scratch script) | Report hygiene; low first-pass discovery value |
| P16 (estimate expensive-run cost before requesting) | Process nicety; not a code-detectable check |
| P21 (cost-based dispatch between two parity-tested paths) | Niche; applies only when two numerically-different implementations coexist behind a cost heuristic |
| P22 (diagnostic counter correctness test) | Niche; partially covered by P12/P13 once those land |

P23 and P24 return to scope (vs. the earlier "Core + conditional" cut) because D6 —
"a guard that has silently stopped discriminating" — needs a landing gate, and P23/P24 are
general test-guard-quality checks, not numerics-specific.

### 2.3 Non-goals

- No change to the shared findings-table base-column schema (see §5.3). Governance additions
  are new report sections, not new columns.
- No renumbering of existing phases 0–13 (see §4.1). The new numeric phase is 11.5.
- No changes to any other audit skill (security, observability, architecture, cognitive,
  documentation, c4).

---

## 3. Detection catalog (primary deliverable)

Each row is a real find recast as an automatic check, with its verification gate. Wiring is
specified per row. All wording stays stack-agnostic; project examples are marked illustrations.

| # | Waste pattern | Wires into | Lands via |
|---|---------------|------------|-----------|
| **D1** | Expensive invariant *setup* rebuilt every iteration (filter design, query plan, compiled regex, connection, buffer, model load) — often hidden **inside** a library call `f(design, item)`, so it does not read as a naked loop-invariant | Sharpen loop-invariant category (`SKILL.md:231-249`), the "Redundant setup in per-item function calls" row (`SKILL.md:721`), and the four-things per-item check (`SKILL.md:790`): flag a call in a loop where an arg is invariant **and** the call has known-expensive setup (design/compile/connect/allocate/load). Profiling cue in Phase 12: a `tottime` hotspot inside a setup function whose **call count ≫ distinct-input count** | P6 (cache the setup read-only, bounded key) |
| **D2** | Same derived input recomputed per consumer instead of once per group — two+ features/stages derive from the same raw source via the same transform, each independently | New structural check in **Phase 2** (Algorithm), cross-referenced from Phase 9: detect the **same transform on the same source in ≥2 sites**; recommend computing once per larger unit of work and sharing | P2 (equivalence oracle on the shared intermediate) |
| **D3** | Wide structure copied/selected in full, then only a few fields read (`SELECT *`, full-width `.copy()`/`.take()`/`.loc[:]` before using a handful of columns) | **Extend** the existing SELECT * checks (`SKILL.md:167` Phase 0 ORM, `:509`/`:532` Phase 5 DB, `:744` ETL) — do **not** add a duplicate SQL row. D3's new contribution is the dataframe angle (`.copy()`/`.take()`/`.loc[:]`) plus a "narrow read **follows** the wide copy" structural cue. Low/context severity | Trivially output-preserving; still gate with P2 if inside a numeric path |
| **D4** | Thousands of tiny homogeneous calls dominated by per-call overhead — a batched/2-D call or a specialized path avoiding a generic dispatcher would amortize the fixed cost | Extend **Phase 12** profiling posture (P18): if a `tottime` hotspot is a huge call count to one function with high per-call / low per-element cost, look for a batched call shape (2-D instead of looped 1-D) or a specialized path **before** an algorithmic rewrite | P2 + version-fence (P4) |
| **D5** | Per-item budget where the fixed cost already dominates — the `count=0` (no inner work) floor alone exceeds the budget | P9 fixed-cost-floor diagnostic, run **first** on any per-item budget with a variable inner count | P1/P11 (target may be mis-granular; restate or get a scope ruling) |
| **D6** | A guard/registry that has silently stopped discriminating — a scale-guard, liveness gate, or anti-rot check that would no longer catch the regression it exists for | Detection half of P24: **run the known-broken shim** the guard is meant to reject and confirm it still fails; flag if the separation margin has collapsed. **Detection cue in Phase 12 (test-guard posture); P23/P24 authoring guidance in the algorithm-complexity template** | P23/P24 (fix the ladder/threshold pairing) |
| **D7** | Redundant re-ingest / no-op re-work | **Already present** — Ingestion-no-op (`SKILL.md:191-229`) and O(n²)/N+1 categories. Named as the model the new rows extend | — |

**Cross-link enforcement.** The "Lands via" column is not decorative. The catalog table in the
skill keeps it, so a reader who acts on a detection cue is pointed straight at the gate that
proves the fix is safe. This is the concrete mechanism that keeps detection and verification
coupled.

---

## 4. optimization-audit/SKILL.md changes

> Line anchors below are as-of `a9ce136` (post docs-layout migration, which shifted every anchor
> below `SKILL.md:283` by +1). They are indicative — the implementation plan re-pins exact bytes by
> the named content (row/section titles), which is drift-proof, since this feature's own edits shift
> them further.

### 4.1 Phase structure

- **New conditional Phase 11.5 — Numeric Reproducibility & Determinism.** Fires only when the
  codebase performs floating-point reductions, uses BLAS/LAPACK/FFT or compiled numeric kernels,
  or ships numeric goldens (mirrors the Phase 8/9/10/11 conditional pattern). Loads
  `templates/numeric-reproducibility.md`. Sits between Phase 11 (Cloud Cost, conditional) and
  Phase 12.
- **Phase 12 renamed** "Profiling & Benchmarking Posture" → "Profiling, Benchmarking &
  Equivalence Posture." Gains an equivalence sub-section that loads
  `templates/equivalence-verification.md`, plus the measurement-rigor bullets (P9–P18, see §4.4).
- **Consistency edits (Hyrum's-Law-sensitive — all FIVE must move together; fixes OAED-SPEC-01):**
  1. Phase-order line (`SKILL.md:56`): insert `11.5` before `12`.
  2. Phase-**count** prose (`SKILL.md:39`, "run all 14 phases"): reword to "all phases 0–13, plus
     conditional 0.5 and 11.5" rather than a bare count. This is the **only** count location.
  3. Conditional-**skip** list (`SKILL.md:54`, "Skip conditional phases (8, 9, 10, 11)"): change to
     "(8, 9, 10, 11, 11.5)". **Distinct from :39** — :54 is not a count. Without this edit Phase
     11.5 is never added to the skip set and therefore runs on non-numeric repos. The first draft
     mislabeled :54 as a count location and omitted it from the guard; that was the review finding.
  4. Important-Rules conditional-phases rule (`SKILL.md:1102`): add "Phase 11.5 (Numeric
     Reproducibility) only if the codebase performs floating-point reductions, uses BLAS/LAPACK/FFT
     or compiled numeric kernels, or ships numeric goldens."
  5. Phase Coverage Matrix (`SKILL.md:1051-1067`): add an "11.5: Numeric Reproducibility (if
     applicable)" row.
  - `test_phase_numbering_consistency` asserts all FIVE locations reference 11.5 — **explicitly
    including :54** and :1102 (the two conditional lists), the phase-order line, the coverage
    matrix, and the reworded count prose.

### 4.2 Phase 0 (anti-pattern scan) — new grep categories

- **D3 wide-select/copy-then-narrow-read** (discovery; fixes OAED-SPEC-04). **Extend** the existing
  SELECT * checks (`:167`, `:509`, `:532`, `:744`) rather than adding a duplicate SQL row. The new
  contribution is the dataframe angle — full-width `.copy()`/`.take()`/`.loc[:]` **followed by** a
  narrow column read — plus the "narrow read follows" structural cue that separates waste from a
  legitimate wide copy. Low/context severity.
- **P2 optimization-without-parity-test** (hazard; **grep-surfaces-candidate + structural-confirm**,
  fixes OAED-SPEC-03). Absence of a parity test is not a local regex match, so this follows the
  Ingestion-no-op precedent (`SKILL.md:195`, "Structural analysis — not just grep"): the grep
  surfaces a recompute-shape candidate (vectorize/batch/parallelize/JIT markers); a structural step
  then confirms whether a corresponding oracle/parity test exists before flagging.
- **P7 silent-degradation-on-version-change** (hazard). Grep for a catch-and-continue around a
  mutation or an assumption a dependency/runtime upgrade can flip — for example a caught error
  on an in-place write followed by warn/log/continue. Treat a warning-based fallback on a
  correctness-relevant path as a bug, not a feature. Ships with positive **and negative** fixtures
  (§8) because the raw catch/continue shape is common in legitimate code.
- **D1 sharpening** lives in the existing loop-invariant grep rows (`:242`, `:756-757`) plus the
  structural rows at `:720-721` and `:790`, extended to name expensive-setup verbs
  (design/compile/connect/allocate/load).

### 4.3 Phase 1 (discovery) and Phase 2 (algorithm)

- **Phase 1 (`SKILL.md:341`)** gains a consumer-enumeration step (P8): an optimization to shared
  or hot-path code must enumerate every consumer and validate across all of them before landing;
  the blast radius is the consumer set, not the edited function. A value-changing finding gets
  its own durable record.
- **Phase 2 (`SKILL.md:366`)** gains the D2 structural check (same transform, same source, ≥2
  sites). The D6 eroded-guard **detection** cue moves to Phase 12 posture (§4.4, fixes
  OAED-SPEC-07); the P23/P24 **authoring** guidance (guard and its check share one named threshold
  constant; size-ladder wide enough for the growth term to dominate) lives in the
  algorithm-complexity template.

### 4.4 Phase 12 (extended) — equivalence posture + measurement rigor

Equivalence posture (loads `equivalence-verification.md`). Measurement-rigor additions, each a
concise bullet or short sub-section:

- **P9** fixed-cost-floor diagnostic (measure the `count=0` floor first). *(D5's gate.)*
- **P10** warm-vs-cold for any JIT/compiled/warm-cache path (force warm-up or report both).
- **P11** budget-granularity check before declaring a miss (look for an already-approved coarser
  bound — corpus-level, throughput, SLA — before proposing a scope cut).
- **P12** structural op-count guards (counter/spy) pin algorithmic wins, not wall-clock alone.
- **P13** instrumentation must be a no-op on the result (test result identical with instrumentation
  on vs off). Coupled to P12 (op-count guards use counters/spies). **Confirmed in scope** (maintainer, round 2).
- **P15** state the noise floor (run-to-run spread; an improvement smaller than the spread is not
  a win without repeated-run evidence).
- **P17** structural shape inventory (counts/sizes/eligibility of the actual corpus) before
  optimizing.
- **P18** profiling posture (require both `tottime` and cumulative; a `tottime` hotspot inside a
  library function is a signal to find a cacheable/reusable design input, not to rewrite the
  caller). *(D1's and D4's profiling cue.)*
- **D6 / P23 / P24** eroded-guard detection (moved here per OAED-SPEC-07): run the known-broken shim
  a scale/complexity guard is meant to reject and confirm it still fails; flag a collapsed
  separation margin. The authoring guidance (shared threshold constant; wide-enough size-ladder)
  lives in the algorithm-complexity template, cross-referenced from here.

### 4.5 Phase 13 (findings report) — new sections

- **Optimization vs Scope-Decision Classification** (P1). Each finding is classified
  `optimization` (output-preserving, gated by an equivalence check) or `scope-decision` (changes
  *what* is computed — needs explicit human sign-off). A performance change that reduces output
  fidelity with no recorded approval is itself a finding.
- **Regressions / trade-offs accepted** (P3). Any fidelity reduction or regression introduced as a
  side effect must be called out with the reason it is acceptable. The Executive Summary must not
  net a fidelity loss into a speed gain.
- **Durable-record note** (P8/P19): a behavior-changing finding — even a provably-correct fix —
  needs its own record (ADR/changelog) distinct from the perf commit.
- **Plan-diff finding** (P20): compare the as-built code to its approved plan/spec; an unrecorded
  deviation is a finding requiring a ruling, whether or not it happens to be behavior-preserving.

The shared findings-table columns are unchanged; classification lives in the new sections and
inline in the Description.

### 4.6 Important Rules

Add three rules to the Important Rules block (`SKILL.md:1091-1105`):

- **P1** — an optimization must be output-preserving; changing *what* is computed is a scope
  decision requiring sign-off. References ADR-004.
- **P19** — a correctness fix found during perf work gets its own test-first cycle, its own
  before/after impact quantification, and its own sign-off. It cannot be "byte-identical" if it
  fixes a bug.
- **P20** — diff as-built against the approved plan/spec for behavior deviations.

### 4.7 CACHE template + Phase 6 (P6)

`templates/caching-strategies.md`, after the bounded-key section (`:515-524`), and Phase 6
(`SKILL.md:551`) gain:

- A shared cached object handed back to callers must be immutable or defensively copied; copy only
  at the point an external API demands mutability (a preemptive copy defeats the cache).
- A cache keyed on an identity can serve a stale/wrong value when a caller passes modified content
  under that same identity. A what-if/counterfactual path must be scored on its own content, never
  re-fetched by the original key. Prefer a structural guarantee (assert the modification is real)
  over a comment.
- A Phase 0 grep for "cached array/collection returned then mutated downstream."

---

## 5. New templates

### 5.1 templates/equivalence-verification.md (P2, P3)

The oracle discipline, loaded by the Phase 12 equivalence sub-section:

- **Oracle test exists.** When a hot loop / scalar path is vectorized, batched, parallelized, or
  JIT-compiled, the original implementation survives as a test-only reference, compared over a
  battery (varying sizes incl. non-power-of-two and odd/prime; validity/NaN/empty/partial-overlap;
  single vs many). Not just the happy path.
- **Whole-output, production-scale, final compare.** Compare every output column, at production
  scale, with the correct equality — not only per-unit parity tests.
- **Equality matches the contract.** Bitwise for an exactness contract; a stated numeric bound with
  the measured max reported next to it otherwise; NaN-aware where NaN is a valid payload.
- **Mutation-verify the oracle both directions.** Apply a single deliberate defect, assert the test
  goes RED, restore. A surviving mutation is a finding about the test (typically a one-sided
  assertion that must become two-sided).
- **Probe-first for platform-dependent identities.** Verify a numeric identity on the target
  platform with a disposable ~20-line probe before writing the real implementation and tests.
- Cross-stack illustrations: a rewritten SQL query must return the same rows; a parallel reduce
  must equal the sequential result; a quantized model must match the reference within a stated
  tolerance; a memoized function must equal the un-memoized one on every key.

### 5.2 templates/numeric-reproducibility.md (P4, P5) — conditional, loaded by Phase 11.5

- **Reduction-order sensitivity.** Flag any vectorize/add-a-batch-axis refactor that reduces
  (sum/mean/dot) along an axis whose inputs may be non-contiguous or reordered; require an explicit
  contiguity/order re-assertion and a bitwise oracle test at multiple shapes.
- **Dispatched fused ops break portable bit-identity.** Before asserting a compiled/JIT kernel
  matches a reference everywhere, check whether the reference routes through a CPU-dispatched fused
  path (FMA, AVX-512-vs-AVX2, GPU atomics). Scope the claim to the machine, or redefine the
  reference.
- **BLAS/LAPACK calls are shape-dependent — do not batch them blind.** Probe for bit-identity
  before batching; sometimes the right answer is not to batch, documented.
- **Library-version numeric drift.** A bit-identity claim about a batched-vs-per-item or
  hand-replicated-vs-library call must be re-verified on every pinned CI version via a version-fence
  test, so a future bump fails loudly.
- **Substitution edge cases.** Cheap-form substitutions of a numeric identity must special-case
  their singularities with a dedicated test.
- **Conditioning, not precision.** A surprisingly large delta on a derived column may be the
  transform's conditioning, not a bug — trace the delta to its upstream primitive and check that
  bound.
- **P5 redefine-the-reference-once.** When as-built numerics cannot be reproduced bit-exactly
  across platforms, author one new reference formulation (explicit ops, fixed and documented
  reduction order, no dispatched fused ops in the hot path), bound the new implementation against
  the old with a stated, tested tolerance, and add a decision-level no-flip gate on the full corpus.
  When replacing an external dependency, enumerate its known defects as documented divergences with
  named tests and freeze a dev-only golden against the old dependency before dropping it.

### 5.3 Note on shared schema

The findings-table base columns (#, Severity, Phase, File:Line, Description, Status) are shared
across all audit skills, with an explicit schema note in the report template. This design does not
touch them (decision recorded in §2.3). The optimization-vs-scope classification is a new report
section, so no cross-skill schema break.

---

## 6. Cross-skill changes

### 6.1 measure-before-optimize/SKILL.md (handoff deliverable 6)

Add a pointer that a pre-change gate on a numeric function should also capture an **output
snapshot** for a post-change equivalence check, deferring to `equivalence-verification.md`. Today
MBO is purely "did it get slower"; this makes it also "did the numbers move." One short addition to
the workflow and the "What this skill is NOT for" framing; MBO stays timing-first, with the
equivalence check delegated, not duplicated.

### 6.2 unbiased-review + final-review (handoff deliverable 7)

The review-side mirror of P2/P19. A reviewer verifying a "byte-identical" / "no-flip" optimization
claim should confirm (a) the parity gate ran at production scale, not a smoke sample, and (b) any
behavior-changing part was separated out with its own record. Small additions to each skill's
checklist. These edits must preserve the CLAUDE.md-and-AGENTS.md pairing that
`tests/test_agents_md_awareness.py` enforces.

---

## 7. ADR-004

New `docs/adrs/ADR-004-output-preserving-optimization.md` (ADR-003 is reserved for the docs-layout
migration, which lands first as its own PR; numbering follows landing order per the maintainer),
following `ADR-TEMPLATE.md`. Records the repo-wide policy:

> An optimization must be output-preserving; changing *what* is computed is a scope decision that
> requires explicit human sign-off and must never be laundered as a performance change.

Justified as an ADR (not a single-skill behavior change) because the principle is enforced by four
skills — optimization-audit, measure-before-optimize, unbiased-review, final-review — which each
reference it. This is the cross-cutting, repo-wide-policy bar for an ADR.

---

## 8. Testing strategy

New tests under `tests/skills/optimization-audit/` (directory does not exist yet). All stdlib-only,
self-contained, reading files with `encoding="utf-8"`, per ADR-002 and repo convention.

- **test_detection_catalog.py** — assert each of D1–D6's cue text/grep row is present in
  `SKILL.md`; for the grep-able rows (D1 sharpening, D3), positive and negative fixtures confirm the
  pattern matches the waste and does **not** match legitimate code (false-positive guard,
  particularly for D3's dataframe copy-then-narrow angle).
- **test_phase0_hazard_greps.py** — positive **and negative** fixtures for the P7 catch-and-continue
  grep and the P2 recompute-shape-candidate grep (fixes OAED-SPEC-02 — §10 names both
  false-positive-prone, so both need a negative fixture, not only D1/D3). The negative fixtures are
  legitimate catch/continue and legitimate vectorize/batch code that the greps must **not** flag.
- **test_equivalence_discipline.py** — assert `equivalence-verification.md` exists; Phase 12 renamed;
  oracle / whole-output-production-scale / mutation-both-directions / probe-first checks present.
- **test_numeric_reproducibility.py** — assert `numeric-reproducibility.md` exists; Phase 11.5
  present and marked conditional; reduction-order / FMA-dispatch / BLAS-shape / version-fence /
  redefine-the-reference present.
- **test_report_governance.py** — assert the report template has the optimization-vs-scope and
  regressions/trade-offs sections; Important Rules contain P1/P19/P20.
- **test_phase_numbering_consistency.py** — assert Phase 11.5 appears in all FIVE consistency
  locations, **located by section content/heading, not hardcoded line numbers** (so the guard
  survives line drift such as the docs-layout migration's +1 shift): the phase-order line, the
  reworded count prose, the conditional-skip list (`Skip conditional phases (…)`), the
  Important-Rules conditional-phases rule, and the coverage matrix. The conditional-skip list is
  the location the first draft omitted (OAED-SPEC-01).
- **Existing suites stay green:** `tests/test_agents_md_awareness.py` (review-skill edits preserve
  the CLAUDE.md+AGENTS.md pairing) and the version-consistency test (§9).
- **Dogfood (test-before-ship, not committed):** run the new Phase 0 greps against the silly-kicks
  working tree locally to confirm they fire on the real finds. **Also dogfood P7 and D3 against a
  non-numeric repo** (fixes OAED-SPEC-05) — those two misfire on general codebases, where their
  false-positive rate actually shows; silly-kicks alone would not surface it. Per the standing rule,
  new audit checks are validated against a real repo before shipping.
- Full `python -m pytest` green before the work is declared done.

---

## 9. Release

Minor bump to **1.27.0** across all locations (no release automation exists — each is manual):

1. `plugins/mad-scientist-skills/.claude-plugin/plugin.json` — `version`
2. `.claude-plugin/marketplace.json` — version
3. `README.md` — version badge
4. `CHANGELOG.md` — new 1.27.0 section + footer compare-link
5. Manual `git tag v1.27.0` + push (separate, after merge, on explicit approval)

A version-consistency test already enforces that these agree and that a matching CHANGELOG section
exists.

`/final-review` runs before committing — it regenerates `architecture.html` via Graphviz `dot`
(never PlantUML Smetana), on the home machine to avoid the known work-fork render divergence.

`commit`, `push`, opening the `PR`, and `merge` are separate actions, each gated on explicit
maintainer approval.

---

## 10. Risks and mitigations

- **Phase-numbering drift (Hyrum's Law).** Inserting 11.5 rather than renumbering keeps the blast
  radius small, but the four consistency locations (§4.1) must move together;
  `test_phase_numbering_consistency.py` enforces this.
- **Grep false positives.** D3 (`SELECT *`) and the P7 catch-and-continue pattern are common in
  legitimate code. Both are scoped narrowly (D3: wide copy *followed by* narrow read; P7: catch
  around a mutation/assumption on a correctness path) and carry Low/context severity where
  appropriate. Negative fixtures guard against noise.
- **Skill-size growth.** `SKILL.md` is already ~1105 lines and the templates total ~8000+. Deep
  numerics content lives in the conditional `numeric-reproducibility.md` template, which only loads
  when Phase 11.5 fires, so a web-backend or SQL audit is not burdened with FMA/BLAS prose.
  Detection rows are terse and reuse existing tables.
- **Detection without verification.** Mitigated structurally: the catalog keeps the "Lands via"
  column, pointing every opportunity cue at its equivalence gate.
- **Scope creep.** Deferred items (§2.3) are recorded, not silently dropped. P13 is flagged inline
  as coupled-to-P12 for the reviewer to confirm or cut.

---

## 11. Notes for the reviewer

- **Decisions already made** (maintainer-approved): Phase 11.5 + extended Phase 12 (not a
  renumber); classification in new report sections (not a new findings-table column); one ADR for
  the output-preserving principle; P23/P24 back in via D6; P21/P22/P14/P16 deferred.
- **Round-1 review resolutions** (report `D:\Development\_reviews\2026-09-29-optimization-audit-equivalence-discovery-spec.md`):
  - **OAED-SPEC-01 (fixed)** — §4.1 now lists FIVE consistency locations; :54 corrected from a
    mislabeled "count" to the conditional-skip list and added to the guard.
  - **OAED-SPEC-02 (fixed)** — §8 adds `test_phase0_hazard_greps.py` with positive+negative fixtures
    for the P7 and P2 greps.
  - **OAED-SPEC-03 (fixed)** — §4.2 reclassifies P2 as grep-surfaces-candidate + structural-confirm,
    per the `:195` precedent.
  - **OAED-SPEC-04 (fixed)** — §3/§4.2 extend the existing SELECT * checks (`:167`/`:509`/`:532`/`:744`)
    instead of duplicating; D3's new angle is the dataframe copy-then-narrow.
  - **OAED-SPEC-05 (adopted)** — §8 dogfoods P7/D3 against a non-numeric repo as well.
  - **OAED-SPEC-07 (adopted)** — D6 detection moves to Phase 12 posture; P23/P24 authoring guidance
    stays in the algorithm-complexity template.
  - **OAED-SPEC-06 (verified)** — anchors confirmed present; re-pinned to `SKILL.md @ a9ce136`
    (post-migration). `:1102` is the Important-Rules "Conditional phases" rule.
  - **OAED-SPEC-08 (fixed, round 2)** — the docs-layout migration (`a9ce136`) inserted a row at
    `SKILL.md:283`, shifting every anchor below it by +1. All such anchors in this spec were
    incremented and the verification SHA updated `35dafdd` → `a9ce136`. Line anchors are indicative
    as-of `a9ce136`; the implementation plan re-pins exact bytes by named content, since this
    feature's own SKILL.md edits shift them again.
- **Resolved (maintainer, round 2):**
  1. P13 (instrumentation no-op test) — **included**, coupled to P12.
  2. ADR-004 policy sentence — **approved as-is**, to be used verbatim in the ADR.

- **Dependency:** this feature assumes the docs-layout migration (a separate, prerequisite PR:
  flat `docs/plans/` split into `docs/specs/` + `docs/plans/`, its own ADR-003, guard test) has
  landed. This spec already lives at `docs/specs/…-design.md`, and the accompanying `-plan.md`
  will land in `docs/plans/`.
- **Rebase note (DLM-PLAN-03) — satisfied:** the docs-layout migration (PR #19, `a9ce136`) has
  merged, and this feature branch is cut from post-migration `main`. The `docs/specs/*.md` doc-scan
  row it added to `optimization-audit/SKILL.md:283` is already present, so this feature's SKILL.md
  edits build on top of it — no rebase or clobber risk remains.
- **Completeness check against the handoff:** in scope = D1–D7, P1–P13, P15, P17–P20, P23, P24,
  deliverables 6–7, ADR. Deferred = P14, P16, P21, P22.
