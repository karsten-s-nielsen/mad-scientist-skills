# Reviewing work (human and LLM)

The full multi-pass protocol behind the compact version in `SKILL.md`.

- **A single LLM review pass is a sample, not a verdict.** Replicated audits of the same claim agree only a
  fraction of the time. For anything that gates a commit, a submission, or a stakeholder-facing claim, run
  **≥3 independent passes and report their agreement.**
- **Bigger ≠ more precise.** Pick the reviewer model by measured precision, not tier. **Pin the model id and
  prompt/skill version** in every review record; re-check after any model upgrade (per-check regression is
  real and large).
- **Do not OR-union independent checkers by default** — the union only adds false positives; measure which
  single layer dominates per check type and route to it.
- **Grade a review by whether it named the *exact* issue and stayed silent on sound sections**, not by whether
  it flagged *something* (broad over-flagging saturates recall for free).
- **Probe omissions explicitly.** The failures that slip past adversarial review are flaws of *absence* (no
  normalisation, no stratification, no gate). Ask "what is missing / never tested?"
- **Calibrate reviewers with a seeded set** ("ReviewBench"): a handful of proposals/specs with known planted
  flaws, hard distractors (look flawed, are sound) and valid anchors; score exact-set match and
  false-positive rate.
- **A blinded outside human read catches the *category* of problem, not the *severity*.** Two trained experts
  tend to agree on *which* flaw exists far more than on *how bad* it is — don't over-read a single "accept."
- **When reviewing another session's spec/plan/impl:** execute the proposed code against real fixtures, lint
  the literal code, anchor-verify every cited path, scope the next round from where blockers came, and grep
  for the sibling of any defect you find. An unapproved deferral or quality cut is a finding, not something to
  bless.
