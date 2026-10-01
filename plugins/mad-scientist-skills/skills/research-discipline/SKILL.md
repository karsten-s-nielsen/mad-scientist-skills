---
name: research-discipline
description: Use when designing or validating a quantitative metric, model, or ranking, when pre-registering an analysis, or before shipping a research claim or write-up to a paper, deck, post, or proposal — pre-registers the E1–E7 metric-design anti-patterns, the validity ladder (construct → face → predictive → robustness), and the multi-pass review protocol. Also use when scrutinising a research metric or empirical claim for soundness. Triggers on "design a metric", "validate this metric/model/ranking", "is this metric sound", "pre-register this analysis", "research claim", "efficacy without an outcome label", or an analytics write-up headed for external publication.
---

# Research discipline

A portable discipline for building, validating, reviewing, and shipping quantitative football-analytics
claims — metrics, models, rankings, research write-ups. Adopt it as a **pre-registration gate**: before
fitting or comparing anything, walk the anti-patterns and the validity ladder and record your answers; use
the multi-pass protocol for reviews and the defect smell-test as a pre-ship check.

It is a **checklist, not a rulebook** — every threshold and exclusion is a *documented, defensible choice*,
not a law. When you deviate, say so and why, and keep the completed checklist with the work.

The E1–E6 taxonomy below is from Rahimian (2026); E7 is our own observability extension. Full citations and
provenance are in [`references/sources.md`](references/sources.md).

## Metric-design anti-patterns (E1–E7)

A metric proposal must clear all seven before it is called validated. Each has a published or in-house anchor.

- **E1 — Learning the provider's label instead of measuring the construct.** If the supervised target *is* a
  vendor's event label (or it leaks in as a feature), you have re-implemented the vendor, not measured the
  thing. A provider label may be a *footnote sanity check*, never the target or the definition.
- **E2 — Ignoring defensive block type.** Cross-team or cross-player comparison of a defensive quantity
  without conditioning on block (low / medium / high) mixes regimes. Report within-block.
- **E3 — Validating only through immediate turnovers.** A single binary outcome (ball regained now / not) is a
  thin, often near-zero-base-rate validation. Use multiple channels: threat/danger reduction, forced-backward
  passes, delay, retention, second balls.
- **E4 — Treating a case study as sufficient evidence.** Clips and narrated examples *illustrate*; they do not
  *validate*. The evidence is the systematic, stratified analysis with intervals.
- **E5 — Ranking without opportunity normalisation.** Raw counts — and per-90 alone — do not remove an
  opportunity-volume confound (a team that faces more of a situation accrues more of the count). Normalise per
  opportunity (per opponent possession, per minute of relevant opponent possession, etc.).
- **E6 — One formula across all game phases.** Pooling a metric across attacking phase (build-up / create /
  finish) hides phase-specific behaviour. Report per phase, or justify pooling.
- **E7 — Computing a metric on unobserved positions.** Broadcast tracking interpolates off-camera players; a
  metric averaged over interpolated positions measures the vendor's imputation model. Gate on the per-player
  detection flag, condition on where the ball is, and **report the observability rate as a result, not a
  footnote**. (Optical / in-stadium tracking is exempt — verify which you have.)

E2 and E6 are two faces of the same failure (unconditioned pooling); test the two axes **independently** — a
metric can pass one and fail the other.

## The validity ladder (compact)

Climb **construct validity → face validity → predictive validity → robustness**, and report all four. Do not
skip to a single outcome-AUC — it is a poor lens for value metrics, and even sound baselines can score below
chance on it.

**Pre-register the direction and the decision rule before you see the numbers.** Freeze the gate (effect
floor, `n_min`, expected sign) so a result cannot move the bar it must clear.

The full ladder — grain cross-checks, the plant / scramble / ceiling controls that an ICC alone cannot
replace, and bootstrapping the unit of analysis — is in [`references/validity-ladder.md`](references/validity-ladder.md).

## Reviewing: the multi-pass protocol (compact)

A single LLM review pass is a **sample, not a verdict**. Replicated audits of the same claim agree only a
fraction of the time. For anything that gates a commit, a submission, or a stakeholder-facing claim, run **≥3
independent passes and report their agreement.**

- **Pick the reviewer model by measured precision, not tier.** Pin the model id and prompt/skill version in
  every review record, and re-check after any model upgrade (per-check regression is real and large).
- **Do not OR-union independent checkers by default** — the union only adds false positives; measure which
  single layer dominates per check type and route to it.
- **Probe omissions explicitly.** The failures that slip past adversarial review are flaws of *absence* (no
  normalisation, no stratification, no gate). Ask "what is missing / never tested?"

The full protocol — grading by exactness, ReviewBench calibration, the blinded-human category-not-severity
finding, and how to review another session's spec / plan / implementation — is in
[`references/reviewing.md`](references/reviewing.md).

## Deeper references

- [`references/validity-ladder.md`](references/validity-ladder.md) — validation and statistics: the full
  ladder, efficacy without an outcome label, grain cross-checks, ICC controls, bootstrapping the unit,
  pre-registration.
- [`references/attribution.md`](references/attribution.md) — attribution and identifiability: player ≠ team,
  crossed random effects, the transfer test, description vs benchmark.
- [`references/data-preflight.md`](references/data-preflight.md) — data-quality preflight: observability /
  censoring, coordinate-frame agreement, schema landmines, fail-closed defaults.
- [`references/reproducibility.md`](references/reproducibility.md) — reproducibility and provenance: one source
  of truth, quote the run, the public-tier recompute, audit pointers, verify the artifact, diagnostics must
  not mutate.
- [`references/reviewing.md`](references/reviewing.md) — reviewing work, human and LLM: the full multi-pass
  protocol.
- [`references/defect-smell-test.md`](references/defect-smell-test.md) — the pre-ship smell test for common
  implementation / analysis defects.
- [`references/sources.md`](references/sources.md) — citations and provenance.

---

*This is a working discipline, loaded while you do the research — not a retrospective audit. It has no
Planning / Audit modes and no coverage matrix; it is a pre-registration checklist you keep with the work.*
