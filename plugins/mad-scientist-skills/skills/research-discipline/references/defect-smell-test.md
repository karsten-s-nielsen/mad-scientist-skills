# Common implementation / analysis defects (pre-ship smell test)

- **Vacuous fixtures.** A test whose fixture never creates the condition under test passes for the wrong
  reason. Assert that a manipulation *measurably moves* the metric; build the fixture to genuinely trigger the
  branch (e.g. place a real undetected keeper, not merely omit the row).
- **Wrong-layer guards.** A guard validated at a different layer than the one it defends goes green while the
  defect ships. Pair each guard with the thing it guards; sweep for a second producer that skips it.
- **Silent zeros / honest-NaN.** Distinguish "measured zero" from "unmeasurable." Return NaN with a
  closed-vocabulary source token, never a bare 0 or 1, when the answer is unknown. `False` is a claim.
- **Derived exports hide omissions.** A derived copy cannot show what it dropped; every completeness check
  that measures the artifact against itself is circular. Name shape mismatches as data-loss risk.
- **Corrections leave a prose halo.** Overturning a numeric finding does not fix the surrounding sentences
  that assumed it; a number gate can't see a stale interpretation. Re-read the prose after any correction.
- **One-way scope ratchet.** If every refinement moves the headline the same direction, disclose it, and look
  for a quantity that should move the other way.
- **Exhaustiveness needs a gate.** A state named at one level and missing from a "complete" table is a bug;
  build the cross-table gate and confirm it reaches its own motivating case.
