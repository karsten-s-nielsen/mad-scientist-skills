# Attribution and identifiability

- **Player ≠ team until proven.** In football many "player" metrics are largely the team the player is in.
  Before attributing anything to an individual, fit a **crossed random-effects model**
  (`~ 1 + (1|team) + (1|player)`) or a team-mean-removed residual ICC, and report the **net-of-team** share
  with its interval.
- **Check identifiability first.** If (almost) no unit appears in more than one group — e.g. one keeper per
  team, few transfers — the individual and the group are non-identifiable and no honest per-individual claim
  is possible. Say "the population is required to answer this," don't force a ranking.
- **A transfer / mover test is the cleanest individual signal:** does the metric travel with the player across
  a club or league change? Distinguish what travels (selection, direction) from what resets (execution length).
- **"Own data buys description; the population buys a benchmark."** Do not present a within-group description
  as if it ranked the unit against the world.
