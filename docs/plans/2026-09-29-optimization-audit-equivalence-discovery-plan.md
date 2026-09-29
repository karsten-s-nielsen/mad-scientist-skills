# optimization-audit equivalence + discovery Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Give `optimization-audit` a detection catalog (D1–D6) that flags optimization opportunities on a first pass, plus an equivalence/governance discipline (P1–P24 subset) that proves an optimization is output-preserving before it lands, with a conditional numeric-reproducibility phase for float-heavy code.

**Architecture:** Prompt-and-template edits to `optimization-audit/SKILL.md` and two new templates, cross-skill pointers in `measure-before-optimize`/`unbiased-review`/`final-review`, one ADR, and a self-contained stdlib test suite that guards the new content (grep fixtures + structural/consistency assertions). No runtime Python module changes.

**Tech Stack:** Markdown skill prompts + templates; Python 3 stdlib + pytest for guards; git.

**Spec:** `docs/specs/2026-09-29-optimization-audit-equivalence-discovery-design.md` — read it alongside this plan. The spec argues *why* and is the authority for scope; this plan is *how*. Section refs below (e.g. §4.4) point into it.

## Global Constraints

- **One coherent, approval-gated commit.** No per-task commits, no micro-commits. Tasks 1–11 build and test; the final task commits once, after the full suite is green, `/final-review` has run, the diff is shown, and the maintainer gives explicit approval. `commit`/`push`/`PR`/`merge` are separate gates.
- **Version bump to 1.27.0** — this feature changes the shipped skill payload, so bump every declaring file (no bump script exists): `plugins/mad-scientist-skills/.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` (version + keep the two descriptions byte-identical), `README.md` badge, `CHANGELOG.md` (new `## [1.27.0]` dated section + footer compare-link). Verify with `git grep -nF "1.26.0"` returning nothing outside history. Manual `git tag v1.27.0` is a separate post-merge gate.
- **Anchors drift.** SKILL.md line numbers in the spec are as-of `a9ce136`; every edit here shifts subsequent lines, so **locate each edit by the named content (row/section title), not by line number.** Re-grep before each edit.
- **Tests:** live under `tests/skills/optimization-audit/` (ADR-002), stdlib-only, self-contained, `encoding="utf-8"`. TDD: write the guard/fixture test first, watch it fail, add the content, watch it pass.
- **Keep green:** `tests/test_agents_md_awareness.py` (the cross-skill edits must preserve every `CLAUDE.md`+`AGENTS.md` pairing) and `tests/test_version_consistency.py`.
- **Multi-stack wording.** Every new grep row and rule reads for Python/Go/Java/SQL/Any, matching the existing Phase 0 tables. Project specifics are marked `» e.g.` illustrations only.
- **Branch:** `optimization-audit-equivalence-discovery` (already cut from post-migration `main` `a9ce136`).
- **ADR-004 policy sentence (approved verbatim):** "An optimization must be output-preserving; changing *what* is computed is a scope decision that requires explicit human sign-off and must never be laundered as a performance change."

---

### Task 1: Phase 11.5 (Numeric Reproducibility) + numeric-reproducibility.md + phase-numbering consistency

Implements spec §4.1, §5.2 (P4/P5), and the 5-location consistency guard.

**Files:**
- Create: `plugins/mad-scientist-skills/skills/optimization-audit/templates/numeric-reproducibility.md`
- Modify: `plugins/mad-scientist-skills/skills/optimization-audit/SKILL.md` (new Phase 11.5; 5 consistency locations)
- Create: `tests/skills/optimization-audit/test_phase_numbering_consistency.py`
- Create: `tests/skills/optimization-audit/test_numeric_reproducibility.py`

**Interfaces:**
- Produces: the phrase `Phase 11.5` present in five locations; the file `templates/numeric-reproducibility.md`; a rename "Profiling, Benchmarking & Equivalence Posture" (completed in Task 2, so Task 1's consistency test does not assert it).

- [ ] **Step 1: Write the failing consistency test (content-based, not line-based)**

```python
"""Guard: Phase 11.5 (conditional numeric phase) is declared consistently.

Locates each section by content/heading, never by line number, so it survives
line drift (ADR-003 migration shifted anchors, and this feature shifts them more).
"""
from pathlib import Path

SKILL = (
    Path(__file__).resolve().parents[3]
    / "plugins/mad-scientist-skills/skills/optimization-audit/SKILL.md"
)


def _text():
    return SKILL.read_text(encoding="utf-8")


def test_phase_11_5_in_phase_order_line():
    t = _text()
    line = next(l for l in t.splitlines() if l.startswith("**Phase order:**"))
    assert "11.5" in line, "phase-order line must include 11.5"


def test_phase_11_5_in_conditional_skip_list():
    t = _text()
    # the audit-process "Skip conditional phases (…)" instruction
    line = next(l for l in t.splitlines() if "Skip conditional phases" in l)
    assert "11.5" in line, "conditional-skip list must include 11.5"


def test_phase_11_5_in_important_rules_conditional_rule():
    t = _text()
    line = next(l for l in t.splitlines() if l.strip().startswith("- **Conditional phases.**"))
    assert "11.5" in line, "Important-Rules conditional-phases rule must name 11.5"


def test_phase_11_5_in_coverage_matrix():
    t = _text()
    matrix = t.split("### Phase Coverage Matrix", 1)[1]
    assert "11.5" in matrix, "Phase Coverage Matrix must have an 11.5 row"


def test_phase_count_prose_not_a_bare_14():
    t = _text()
    # the mode-detection prose must not claim a bare "14 phases" count
    assert "run all 14 phases" not in t, "count prose must be reworded for 0.5 + 11.5"


def test_phase_11_5_section_exists_and_conditional():
    t = _text()
    assert "### Phase 11.5:" in t, "Phase 11.5 section heading must exist"
    head = t.split("### Phase 11.5:", 1)[1].split("###", 1)[0]
    assert "CONDITIONAL" in head, "Phase 11.5 must be marked CONDITIONAL"
```

- [ ] **Step 2: Run — verify all fail**

Run: `python -m pytest tests/skills/optimization-audit/test_phase_numbering_consistency.py -v`
Expected: FAIL (no Phase 11.5 yet).

- [ ] **Step 3: Add Phase 11.5 to SKILL.md**

After the Phase 11 section and before Phase 12, insert:

```markdown
### Phase 11.5: Numeric Reproducibility & Determinism (Audit mode) — CONDITIONAL

Only run this phase if the codebase performs floating-point reductions, uses BLAS/LAPACK/FFT or
compiled numeric kernels (numba, Cython, C extensions, GPU), or ships numeric goldens. Skip it
entirely otherwise — a web backend, a SQL pipeline, or a string-processing service has nothing here.

Load `templates/numeric-reproducibility.md` for the full reference. The core hazard: a numeric
result can differ across CPUs, across SIMD/GPU code paths, and across library versions even with
"the same" source, because reordering a floating-point reduction or letting hardware/library
dispatch pick a fused path changes the result bits. Any bit-identity claim must be scoped to the
environment where it was verified, or the reference redefined so no dispatcher can vary it.

**Output:** Numeric-reproducibility findings — reduction-order hazards, dispatched-fused-op
portability claims, un-fenced library-version drift, and any redefine-the-reference decision.
```

- [ ] **Step 4: Update the four other consistency locations (by content)**

1. Phase-order line (`**Phase order:**`): insert `11.5` between `11` and `12`.
2. Conditional-skip instruction (`Skip conditional phases (8, 9, 10, 11)`): → `(8, 9, 10, 11, 11.5)`.
3. Mode-detection count prose (`run all 14 phases`): reword to `run all applicable phases (0–13, plus conditional 0.5 and 11.5)`.
4. Important-Rules `- **Conditional phases.**` bullet: append `Phase 11.5 (Numeric Reproducibility) only if the codebase does floating-point reductions, uses BLAS/LAPACK/FFT or compiled numeric kernels, or ships numeric goldens.`
5. Phase Coverage Matrix: add row `| Phase 11.5: Numeric Reproducibility (if applicable) | [X checks] | [Y findings] | [summary] |` after the Phase 11 row.

- [ ] **Step 5: Write `templates/numeric-reproducibility.md`**

Full content per spec §5.2 — a reference template mirroring the depth/format of the existing templates (`## <Heading>` sections, per-language cues, `» e.g.` illustrations). Sections, each with a grep/structural cue and a stated check:

- **Reduction-order sensitivity** — flag any vectorize / add-a-batch-axis refactor that reduces (sum/mean/dot) along an axis whose inputs may be non-contiguous or reordered; require an explicit contiguity/order re-assertion before the reduction and a bitwise oracle test at multiple shapes. *» e.g.* fancy-indexing a middle axis returned a non-contiguous array, turning a pairwise sum into a sequential sum — 1–2 ulp drift, no exception.
- **Dispatched fused ops break portable bit-identity** — before asserting a compiled/JIT kernel matches a reference *everywhere*, check whether the reference routes through a CPU-dispatched fused path (FMA, AVX-512 vs AVX2, GPU atomics). Scope the claim to the machine, or redefine the reference.
- **BLAS/LAPACK calls are shape-dependent — do not batch them blind** — probe for bit-identity before batching (`corrcoef`, matrix products, solves); sometimes the right answer is not to batch, documented.
- **Library-version numeric drift** — a bit-identity claim about a batched-vs-per-item or hand-replicated-vs-library call must be re-verified on every pinned CI version via a version-fence test that runs the real library call and compares, so a bump fails loudly.
- **Substitution edge cases** — cheap-form substitutions of a numeric identity must special-case their singularities with a dedicated test (e.g. `exp(i·angle(x))` → `conj(x)/|x|` diverges at `x=0`).
- **Conditioning, not precision** — a surprisingly large delta on a *derived* column may be the transform's conditioning, not a bug; trace to the upstream primitive and check *that* bound.
- **P5 — redefine-the-reference-once** — the sanctioned exit: author one new reference formulation (explicit ops, fixed & documented reduction order, no dispatched fused ops in the hot path), bound the new implementation against the old with a *stated, tested* tolerance (report the measured max next to the bound), add a decision-level no-flip gate on the **full corpus**; when replacing an external dependency, enumerate its known defects as documented divergences with named tests and freeze a dev-only golden against the old dependency before dropping it.

- [ ] **Step 6: Write `test_numeric_reproducibility.py`**

```python
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3] / "plugins/mad-scientist-skills/skills/optimization-audit"
TEMPLATE = ROOT / "templates/numeric-reproducibility.md"
SKILL = ROOT / "SKILL.md"

REQUIRED = [
    "reduction-order", "FMA", "BLAS", "version-fence", "redefine", "conditioning",
]


def test_template_exists_and_covers_hazards():
    t = TEMPLATE.read_text(encoding="utf-8").lower()
    missing = [k for k in REQUIRED if k.lower() not in t]
    assert not missing, f"numeric-reproducibility.md missing: {missing}"


def test_phase_11_5_loads_the_template():
    s = SKILL.read_text(encoding="utf-8")
    body = s.split("### Phase 11.5:", 1)[1].split("###", 1)[0]
    assert "templates/numeric-reproducibility.md" in body
```

- [ ] **Step 7: Run all Task-1 tests green**

Run: `python -m pytest tests/skills/optimization-audit/test_phase_numbering_consistency.py tests/skills/optimization-audit/test_numeric_reproducibility.py -v`
Expected: all pass.

---

### Task 2: Equivalence verification template + Phase 12 rename/extension

Implements spec §4.1 (Phase 12 rename), §4.4 (equivalence sub-section), §5.1 (P2/P3).

**Files:**
- Create: `plugins/mad-scientist-skills/skills/optimization-audit/templates/equivalence-verification.md`
- Modify: `SKILL.md` (rename Phase 12; add equivalence sub-section that loads the template)
- Create: `tests/skills/optimization-audit/test_equivalence_discipline.py`

- [ ] **Step 1: Write the failing test**

```python
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3] / "plugins/mad-scientist-skills/skills/optimization-audit"
SKILL = ROOT / "SKILL.md"
TEMPLATE = ROOT / "templates/equivalence-verification.md"


def test_phase_12_renamed():
    s = SKILL.read_text(encoding="utf-8")
    assert "Profiling, Benchmarking & Equivalence Posture" in s


def test_equivalence_template_exists_and_covers_oracle_discipline():
    t = TEMPLATE.read_text(encoding="utf-8").lower()
    for k in ["oracle", "production scale", "mutation", "probe", "bitwise"]:
        assert k in t, f"equivalence-verification.md missing: {k}"


def test_phase_12_loads_equivalence_template():
    s = SKILL.read_text(encoding="utf-8")
    p12 = s.split("Profiling, Benchmarking & Equivalence Posture", 1)[1]
    assert "templates/equivalence-verification.md" in p12
```

- [ ] **Step 2: Run — verify fail.** `python -m pytest tests/skills/optimization-audit/test_equivalence_discipline.py -v` → FAIL.

- [ ] **Step 3: Rename Phase 12 heading** `### Phase 12: Profiling & Benchmarking Posture` → `### Phase 12: Profiling, Benchmarking & Equivalence Posture` (update the phase-order references if any name the phase; the number is unchanged).

- [ ] **Step 4: Add the equivalence sub-section** under Phase 12:

```markdown
#### Equivalence posture (output-preserving optimizations)

Load `templates/equivalence-verification.md`. Any change that alters *how* a result is computed —
vectorize, batch, parallelize, cache, memoize, swap algorithm, JIT — must prove it yields the
**same** result, not merely a faster one. Speed is necessary, never sufficient, evidence that an
optimization is correct. Checks: an oracle test (the pre-optimization implementation kept test-only)
compared over a battery at production scale; whole-output final compare with the equality the
contract demands (bitwise for exactness; a stated, tested tolerance otherwise); mutation-verify the
oracle both directions; probe-first for platform-dependent numeric identities.
```

- [ ] **Step 5: Write `templates/equivalence-verification.md`** — full content per spec §5.1 (oracle-exists, whole-output-production-scale compare, equality-matches-contract, mutation-verify-both-directions, probe-first; cross-stack illustrations: SQL rows, parallel reduce, quantized model, memoized fn).

- [ ] **Step 6: Run Task-2 tests green.**

---

### Task 3: Phase 12 measurement rigor (P9–P13, P15, P17, P18) + D4/D6 detection + ALG P23/P24

Implements spec §4.4 (measurement bullets, D4, D6) and §4.3 (P23/P24 authoring in ALG template).

**Files:**
- Modify: `SKILL.md` (Phase 12 measurement bullets + D6 detection cue)
- Modify: `templates/algorithm-complexity.md` (P23/P24 authoring guidance)
- Create: `tests/skills/optimization-audit/test_measurement_rigor.py`

- [ ] **Step 1: Failing test**

```python
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3] / "plugins/mad-scientist-skills/skills/optimization-audit"
ALG = ROOT / "templates/algorithm-complexity.md"

def test_phase_12_measurement_bullets_present():
    p12 = (ROOT / "SKILL.md").read_text(encoding="utf-8").split(
        "Profiling, Benchmarking & Equivalence Posture", 1)[1]
    for cue in ["fixed-cost", "count=0", "warm", "noise floor",
                "op-count", "shape inventory", "instrumentation", "known-broken shim"]:
        assert cue.lower() in p12.lower(), f"missing measurement cue: {cue}"

def test_alg_template_has_guard_authoring_guidance():
    a = ALG.read_text(encoding="utf-8").lower()
    assert "threshold constant" in a and "size-ladder" in a
```

- [ ] **Step 2: Run — fail.**

- [ ] **Step 3: Add the measurement-rigor bullets** to Phase 12 (one concise bullet each): P9 fixed-cost-floor (`count=0` first), P10 warm-vs-cold, P11 budget-granularity, P12 op-count guards (counter/spy, not wall-clock), P13 instrumentation-no-op test (coupled to P12), P15 noise floor, P17 shape inventory, P18 profiling posture (`tottime` + cumulative; a library `tottime` hotspot → find a cacheable design input). Add the **D6** eroded-guard detection cue: run the known-broken shim a scale/complexity guard rejects, confirm it still fails, flag a collapsed separation margin (cross-ref the ALG template for the fix).

- [ ] **Step 4: Add P23/P24 authoring guidance** to `algorithm-complexity.md`: a guard and its does-the-guard-work companion share **one named threshold constant** (not two drifting literals); a scale/complexity guard's **size-ladder** must be wide enough for the asserted growth term to dominate before the threshold is tightened (fix the ladder, not just the threshold).

- [ ] **Step 5: Run Task-3 tests green.**

---

### Task 4: Phase 0 detection + hazard greps (D1, D3, P2, P7) + fixtures

Implements spec §3 (D1/D3), §4.2 (Phase 0 greps).

**Files:**
- Modify: `SKILL.md` (Phase 0: D1 sharpening, D3 row, P2 candidate grep, P7 grep)
- Create: `tests/skills/optimization-audit/conftest.py` (the `extract_pattern` fixture; **no `__init__.py`** in this dir)
- Create: `tests/skills/optimization-audit/test_detection_catalog.py`
- Create: `tests/skills/optimization-audit/test_phase0_hazard_greps.py`

- [ ] **Step 1: Write failing tests that EXTRACT the pattern from the shipped table (not a copy)**

The negative-fixture tests must guard the **actual** grep that ships, so they parse the regex out of the named SKILL.md table cell and assert THAT against both fixtures. A hand-copied regex would guard the copy, letting a broken table grep ship green (OAED-PLAN-01). The new patterns (D3, P7, P2) are authored Python-`re`-compatible so the guard can compile them.

Shared helper as a **dir-local conftest fixture** — `tests/skills/optimization-audit/conftest.py`. pytest loads `conftest.py` by path (not by module import), so the hyphenated directory name is irrelevant and no cross-file import is needed (OAED-PLAN-03). **This test directory has NO `__init__.py`** (unlike `tests/skills/c4/`): `optimization-audit` is not a valid Python package name, so an `__init__.py` here would break collection. The test modules load via pytest's default prepend mode; the root `conftest.py`/`pytest.ini` pin the rootdir.

```python
# tests/skills/optimization-audit/conftest.py
import re
from pathlib import Path
import pytest

SKILL_PATH = (Path(__file__).resolve().parents[3]
              / "plugins/mad-scientist-skills/skills/optimization-audit/SKILL.md")

@pytest.fixture
def extract_pattern():
    """Return a helper that compiles the regex from the Phase-0 table row containing row_key.

    row_key: a stable, unique substring of the row's Issue column.
    col: the 0-based cell index of the Pattern column in that table.
    Splits on UNescaped '|' only (so a pattern's own '\\|' alternation survives),
    strips the wrapping backticks, then un-escapes '\\|' -> '|' before compiling.
    Raises StopIteration if the row is absent — the RED state before it is added.
    """
    def _extract(row_key: str, col: int) -> re.Pattern:
        text = SKILL_PATH.read_text(encoding="utf-8")
        row = next(l for l in text.splitlines()
                   if l.lstrip().startswith("|") and row_key in l)
        cells = [c.strip() for c in re.split(r"(?<!\\)\|", row.strip().strip("|"))]
        return re.compile(cells[col].strip("`").replace(r"\|", "|"))
    return _extract
```

Per-pattern fixtures + assertions (pytest injects `extract_pattern` by name — no import). The executor sets each `row_key` to a stable Issue-column substring of the row it adds, and `col` to that table's Pattern-column index, in the step that adds the row:

```python
# D3 — wide copy/select then narrow read (dataframe angle)
D3_WASTE = "wide = fetch(); df = wide.copy(); use(df['a'])"   # full copy, few fields
D3_OK    = "df = fetch()[['a', 'b']]; use(df['a'])"           # narrowed at source
def test_d3_pattern_discriminates(extract_pattern):
    rx = extract_pattern(row_key="<D3 Issue-column text>", col=<pattern-col idx>)
    assert rx.search(D3_WASTE)
    assert not rx.search(D3_OK)

# P7 — catch-and-continue around a mutation / version-flippable assumption
P7_WASTE = "try:\n    arr[mask] = nan\nexcept ValueError:\n    warnings.warn('skip')"
P7_OK    = "try:\n    risky()\nexcept ValueError:\n    raise"   # re-raises, not warn-continue
def test_p7_pattern_discriminates(extract_pattern):
    rx = extract_pattern(row_key="<P7 Issue-column text>", col=<pattern-col idx>)
    assert rx.search(P7_WASTE)
    assert not rx.search(P7_OK)

# P2 — recompute-shape marker (grep only surfaces the candidate; structural confirm is separate)
P2_WASTE = "result = np.vectorize(f)(xs)"                      # vectorize marker, no parity test
P2_OK    = "for x in xs:\n    out.append(f(x))"               # plain scalar loop, nothing to flag
def test_p2_pattern_discriminates(extract_pattern):
    rx = extract_pattern(row_key="<P2 Issue-column text>", col=<pattern-col idx>)
    assert rx.search(P2_WASTE)
    assert not rx.search(P2_OK)
```

`test_detection_catalog.py` also asserts each of D1–D6's cue text is present in SKILL.md. All extraction tests are **red-first**: before the rows exist, `extract_pattern(...)` raises `StopIteration`. When the executor adds each row (Steps 3–6), they set that pattern's `row_key`/`col` to the row's actual Issue text and Pattern-column index.

- [ ] **Step 2: Run — fail.**

- [ ] **Step 3: Sharpen D1** — extend the existing loop-invariant grep rows and the "Redundant setup in per-item function calls" row to name expensive-setup verbs (design/compile/connect/allocate/load) and add the profiling cue (call-count ≫ distinct-input count) as a pointer to Phase 12.

- [ ] **Step 4: Add the D3 row** — extend the existing `SELECT *` checks (ORM/DB/ETL rows) with the dataframe copy-then-narrow angle + the "narrow read follows" structural cue; Low/context severity. Do **not** add a duplicate SQL row.

- [ ] **Step 5: Add the P2 candidate grep** — a new Phase 0 category "Optimization without a parity test": grep surfaces a recompute-shape marker (vectorize/batch/parallelize/JIT), then a **structural** confirm (per the Ingestion-no-op "Structural analysis — not just grep" precedent) checks whether a matching oracle/parity test exists before flagging.

- [ ] **Step 6: Add the P7 grep** — new category "Silent degradation on env/version change": catch-and-continue around a mutation or an assumption an upgrade can flip (e.g. a caught error on an in-place write followed by warn/log/continue); warn-and-skip on a correctness path is a bug, not a feature. Positive + negative fixtures required (§8).

- [ ] **Step 7: Run Task-4 tests green** — including the negative fixtures (no false-positive on legitimate code).

---

### Task 5: Phase 1 consumer enumeration (P8) + Phase 2 D2 structural check

Implements spec §4.3 (P8, D2).

**Files:**
- Modify: `SKILL.md` (Phase 1 discovery step; Phase 2 D2 check)
- Create: `tests/skills/optimization-audit/test_discovery_and_structural.py`

- [ ] **Step 1: Failing test** — assert Phase 1 has a "consumer enumeration" / "blast radius" step and Phase 2 has the "same transform, same source, ≥2 sites" D2 check.
- [ ] **Step 2: Run — fail.**
- [ ] **Step 3: Add P8** to Phase 1: an optimization to shared/hot-path code must enumerate every consumer and validate across all of them before landing; the blast radius is the consumer set, not the edited function; a value-changing finding gets its own durable record.
- [ ] **Step 4: Add D2** to Phase 2: detect the same transform applied to the same source in ≥2 sites (identical resample/parse/normalize/join on the same input key across separate code paths); recommend computing once per larger unit of work and sharing; lands via P2 (oracle on the shared intermediate).
- [ ] **Step 5: Run green.**

---

### Task 6: Phase 13 report sections + Important Rules (P1, P3, P19, P20)

Implements spec §4.5, §4.6.

**Files:**
- Modify: `SKILL.md` (Phase 13 report; Important Rules)
- Create: `tests/skills/optimization-audit/test_report_governance.py`

- [ ] **Step 1: Failing test** — assert the audit-mode report template contains an "Optimization vs Scope-Decision Classification" section and a "Regressions / trade-offs accepted" section; assert Important Rules contain the P1 (output-preserving vs scope-decision), P19 (correctness fix gets its own cycle), and P20 (diff as-built vs approved plan) rules; assert the shared findings-table base columns are unchanged (schema note still present).
- [ ] **Step 2: Run — fail.**
- [ ] **Step 3: Add report sections** (P1 classification + P3 regressions/trade-offs; P8/P19 durable-record note; P20 plan-diff finding). Leave the shared findings-table columns untouched.
- [ ] **Step 4: Add the three Important Rules** (P1 referencing ADR-004; P19; P20).
- [ ] **Step 5: Run green.**

---

### Task 7: Cache immutability (P6)

Implements spec §4.7.

**Files:**
- Modify: `templates/caching-strategies.md` (after the bounded-key section)
- Modify: `SKILL.md` (Phase 6 checks + a Phase 0 grep for cached-collection-returned-then-mutated)
- Create: `tests/skills/optimization-audit/test_cache_immutability.py`

- [ ] **Step 1: Failing test** — assert the CACHE template covers "immutable or defensively copied" + identity-keyed-cache staleness, and Phase 6 references it.
- [ ] **Step 2: Run — fail.**
- [ ] **Step 3: Add P6 content** — a shared cached object handed back must be immutable or defensively copied (copy only where an external API demands mutability); an identity-keyed cache must never serve a modified-content path by the original key (score on own content; prefer a structural guarantee over a comment); Phase 0 grep for "cached array/collection returned then mutated downstream".
- [ ] **Step 4: Run green.**

---

### Task 8: Cross-skill pointers (MBO, unbiased-review, final-review)

Implements spec §6.

**Files:**
- Modify: `measure-before-optimize/SKILL.md`
- Modify: `unbiased-review/SKILL.md`
- Modify: `final-review/SKILL.md`
- Create: `tests/skills/optimization-audit/test_cross_skill_pointers.py`

- [ ] **Step 1: Failing test** — assert MBO references an output-snapshot / equivalence check deferring to `equivalence-verification.md`; assert `unbiased-review` and `final-review` each mention verifying a byte-identical/no-flip optimization claim at production scale + separated behavior-changing record.
- [ ] **Step 2: Run — fail.**
- [ ] **Step 3: Add the MBO pointer** (one addition to workflow + "What this skill is NOT for": a pre-change gate on a numeric function should also capture an output snapshot for a post-change equivalence check, deferring to `equivalence-verification.md`; MBO stays timing-first).
- [ ] **Step 4: Add the review-skill mirror** to `unbiased-review` and `final-review`: a reviewer verifying a "byte-identical"/"no-flip" optimization claim confirms (a) the parity gate ran at production scale, not a smoke sample, and (b) any behavior-changing part was separated out with its own record.
- [ ] **Step 5: Run green + confirm `tests/test_agents_md_awareness.py` still passes** (these edits must not break any CLAUDE.md+AGENTS.md pairing).

---

### Task 9: ADR-004

Implements spec §7.

**Files:**
- Create: `docs/adrs/ADR-004-output-preserving-optimization.md`

- [ ] **Step 1: Write ADR-004** (Nygard format, per `docs/adrs/ADR-TEMPLATE.md`). Decision = the approved sentence verbatim (Global Constraints). Context: the four skills that enforce it (optimization-audit, measure-before-optimize, unbiased-review, final-review); the detection→verification chain. Alternatives: no ADR (rejected — cross-skill policy, four consumers); a looser tolerance instead of redefine-the-reference (rejected — see P5). Consequences: positive (a change to *what* is computed can no longer hide in a perf commit); neutral (ADR-003 took 003 as the migration landed first). Related: the equivalence-verification + numeric-reproducibility templates, the P1 Important Rule, the review-skill mirror.
- [ ] **Step 2: Confirm links resolve by eye** (prose artifact, no test).

---

### Task 10: Version bump 1.27.0 + CHANGELOG

Implements Global Constraints.

**Files:**
- Modify: `plugins/mad-scientist-skills/.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `README.md`, `CHANGELOG.md`

- [ ] **Step 1:** `git grep -nF "1.26.0"` to find every declaration (exclude `CHANGELOG.md` history).
- [ ] **Step 2:** Bump each to `1.27.0`; keep the two manifest descriptions byte-identical (extend both with the new capabilities if the description enumerates skills).
- [ ] **Step 3:** Add a dated `## [1.27.0] - 2026-09-29` CHANGELOG section (Added: detection catalog D1–D6; equivalence-verification + numeric-reproducibility templates; conditional Phase 11.5; P1/P3/P19/P20 governance; P6–P24 subset; cross-skill pointers; ADR-004) + the footer compare-link.
- [ ] **Step 4:** `git grep -nF "1.26.0"` returns nothing outside history; `python -m pytest tests/test_version_consistency.py -q` green.

---

### Task 11: Dogfood validation (not committed)

Implements spec §8 (test-before-ship).

- [ ] **Step 1:** Run the new Phase 0 greps against the `silly-kicks` working tree; confirm they fire on the real finds (D1 filter-redesign, D3 wide-copy-then-narrow, P7 catch-and-continue, P2 recompute-shape marker). D2 is a **Phase 2 structural** check, not a grep — it is validated by its Task 5 unit test, not this grep dogfood (OAED-PLAN-02).
- [ ] **Step 2:** Run P7 and D3 against a **non-numeric** repo (e.g. this repo, or any web/CLI project); confirm an acceptable false-positive rate (they misfire on general code — that is where the rate shows).
- [ ] **Step 3:** If false positives are excessive, tighten the regex + fixtures (loop back to Task 4) before proceeding. Record the dogfood result in the PR description; nothing from this task is committed.

---

### Task 12: Pre-commit gate + single commit (approval-gated)

- [ ] **Step 1:** Full suite green — `python -m pytest -q`.
- [ ] **Step 2:** `/final-review`. This feature edits SKILL.md prose/templates but no C4 model input (`architecture.dsl`), so architecture.html is expected unchanged; if the regen diffs, investigate before committing.
- [ ] **Step 3:** Show the full diff + file list. Confirm the spec (`docs/specs/…-design.md`) and this plan (`docs/plans/…-plan.md`) are included, and `.serena/` is not.
- [ ] **Step 4:** Commit only on explicit maintainer approval — one coherent commit for the whole feature (spec, plan, ADR-004, SKILL.md, both new templates, ALG + CACHE edits, cross-skill edits, tests, version bump). Message: `feat(optimization-audit): equivalence + discovery (D1-D6, P1-P24 subset) (v1.27.0)` with the Co-Authored-By trailer.
- [ ] **Step 5:** Push + PR + (post-merge) `git tag v1.27.0` — each a separate explicit gate.

---

## Self-Review

**Spec coverage** (§2.1 in-scope table → task):
- D1–D6 → Tasks 3 (D4/D6), 4 (D1/D3), 5 (D2). ✓
- D7 → present already (no task; named in Task 4's D-catalog note). ✓
- P1/P2/P3 → Tasks 2 (P2 template), 6 (P1/P3 report + rule). ✓
- P4/P5 → Task 1. ✓
- P6 → Task 7. P7 → Task 4. P8 → Task 5. ✓
- P9–P13, P15, P17, P18 → Task 3. ✓
- P19/P20 → Task 6. P23/P24 → Task 3 (ALG). ✓
- Cross-skill (deliverables 6,7) → Task 8. ADR-004 → Task 9. ✓
- Tests (6 suites) → Tasks 1–8. Version → Task 10. Dogfood → Task 11. ✓
- Deferred (P14/P16/P21/P22) → correctly absent. ✓

**Placeholder scan:** test code and content specs are concrete; the two template files' full prose is specified by section (§5.1/§5.2 authority) and written in Tasks 1/2. Task 4's grep guards **extract** the pattern from the named SKILL.md table cell (`extract_pattern`) and assert it against both fixtures — no hand-copied regex, so a broken table grep fails the guard (OAED-PLAN-01). The only executor-supplied values are each row's `row_key` (a stable Issue-column substring) and Pattern-column index, named in the step that adds the row.

**Type/name consistency:** test files all under `tests/skills/optimization-audit/`; `Path(__file__).resolve().parents[3]` used consistently to reach the repo root from that depth; template filenames (`equivalence-verification.md`, `numeric-reproducibility.md`) spelled identically in SKILL.md loads and tests.
