# Validation and statistics

The full validity ladder behind the compact version in `SKILL.md`.

- **The validation ladder:** construct validity → face validity → predictive validity → robustness. Report
  all four; do not skip to a single outcome-AUC (a poor lens for value metrics — even sound baselines can
  score below chance on it).
- **Efficacy without an outcome column is legitimate.** If no clean success label exists, a well-posed
  descriptive or structural question needs none — say so, don't invent a proxy that reintroduces E3.
- **Report the metric at the grain the claim lives at, and cross-check grains.** A match-mean ICC and an
  action-level ICC are different quantities; aggregation *inflates* reliability (fewer, averaged units shrink
  within-unit noise). A correlation can flip sign between the finest and the aggregated grain — check both
  before reporting either.
- **An ICC alone licenses nothing.** Always run the controls: a positive plant (inject a known effect — does
  it recover?), a scramble (destroy the effect — does it read ~0?), and a ceiling. Report them.
- **Bootstrap by resampling the unit of analysis** (match id, proposal id, keeper id — not raw rows), with a
  fixed seed, and report the interval, not a point estimate.
- **Pre-register the direction and the decision rule before you see the numbers.** Freeze the gate (effect
  floor, `n_min`, expected sign) so a result cannot move the bar it must clear.
