# Reproducibility and provenance

- **One source of truth.** Export a definition once; every pipeline *reads* it. A re-derived copy drifts.
- **Quote the run, not a stale mart.** If a downstream store may not have recomputed, quote the owner-run
  script, and state the vintage of anything materialized.
- **Public data for anything external.** Explore on whatever data is best, but any number in a paper, deck,
  post or proposal must be recomputed on public/redistributable data and cited from that run; keep one
  multi-tier script and prove the refactor by reproducing the restricted results bit-for-bit.
- **Every headline number carries an audit pointer** — which validity/reliability check produced it and
  whether it passed. Keep an append-only run log (inputs, model/version, seed, result).
- **Verify the artifact you will ship, not the exit code.** Render/read what the reader will open; keep the
  check as a script.
- **Diagnostics must not mutate.** Probing a pipeline by monkey-patching and calling `run()`/`main()` also
  runs its writes and can corrupt the artifact — copy the pure helper, snapshot content, diff against the
  live copy.
