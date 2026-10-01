# Data-quality preflight

Run before any spatial computation.

- **Observability / censoring.** Establish the detection rate and how it depends on context (ball position,
  phase, block). Condition on it; gate metrics on it; report it (E7).
- **Coordinate-frame agreement.** A derived quantity (pressure, possession side, defensive-line height) must
  agree with the provider's own flag; a silent frame/orientation error manufactures a player-independent null.
  Add a fail-loud pre-flight that asserts the agreement. Normalise orientation (attacking direction) before
  any spatial math.
- **Schema landmines are per-provider and must be checked, not assumed.** Signed vs unsigned angles; capped
  distance columns; fields that are populated only on some event types; fields that are entirely null in one
  data tier; near-synonym column names. Verify field semantics against the provider's own documentation, not
  by guessing from values.
- **Fail closed on the unknown.** An unclassified provider, a null detection flag on a detection-aware feed, a
  missing pitch dimension → raise, do not default to "observed" or to a standard value. Provide one explicit,
  *general* opt-out flag for a caller who knowingly wants the ungated behaviour — never a silent relaxation
  and never a consumer-specific carve-out.
