# Output contract

Two outputs per review. The full report is the durable record; the paste-back block is what travels
to the other terminal.

## Full report

Path: `reviews/YYYY-MM-DD-<slug>-<type>.md`, where `<type>` is `spec` / `plan` / `impl`, plus `-r2`,
`-r3` for later rounds. Echo the absolute path — the other session reads it directly.

Header, always, because a later round needs it to compute what changed:

```markdown
**Artifact** <path> (<N> lines, <staged|committed|working>)
**Repo** <repo> @ <short-sha>
**Artifact sha256** <hash>
**Reviewed** <date> · <methods used>
**Round** 1  (or: 2 — prior: reviews/<file>.md)
**Verdict** <VERDICT> — <one line>
```

Sections in order:

1. **Assessment** — a few paragraphs. What the artifact does well, specifically enough to prove you
   read it; the verification tally; where the blocking items sit. A review that lists only defects on
   a strong artifact is miscalibrated and will be discounted wholesale.
2. **BLOCKING** — each with: the quoted claim or location, the evidence, the concrete consequence of
   shipping, and **Resolved when:** a testable condition.
3. **SHOULD FIX** — same shape, consequence may be long-term rather than immediate.
4. **CONSIDER** — table form is fine; these are cheap notes, not arguments.
5. **Could not verify** — what you could not check, why, and what would be needed. Plus a line
   confirming nothing was written to the target and nothing was executed inside it.
6. **Verification appendix** — the claim-by-claim table, `exact` / `wrong` / `imprecise`. This is what
   makes the whole report credible: it shows the same rigour applied to the claims that held up.

Findings carry stable IDs (`D1-SPEC-03`). Numbering continues across rounds, never restarts.

## Paste-back block

Terminal only, fenced, self-contained — the author may see nothing but this:

```
── PASTE BACK ─────────────────────────────────────────────
REVIEW: <type> / <slug>
VERDICT: <VERDICT> — <one line>
Method: <what was verified, how; the tally>

BLOCKING
1. <location> — <defect>. <consequence>. <resolution>.

SHOULD FIX
3. <defect + evidence>

CONSIDER: <one-liners, semicolon separated>

COULD NOT VERIFY: <what and why>

Nothing was written to your tree; no test was run inside it.
FULL REPORT: <absolute path>
───────────────────────────────────────────────────────────
```

Keep it dense. Every line should carry a `file:line`, a number, or a consequence. Prose that could be
deleted without losing information should be.

## Tone

Write for a competent author who will act on it, and who will notice both flattery and padding.

- Lead with the claim, then the evidence. Never the reverse.
- Quote what the artifact said before saying what is wrong with it.
- When the artifact is right about something you doubted, say so — it is information.
- When you disagree with a documented decision, say that you are disagreeing with one.
- Credit the artifact's own arguments when they support your finding. "Your line 95 argument applies
  to the tests themselves" lands better than an external standard, and it is more honest about where
  the reasoning came from.
- No hedging on verified facts. No apologies. No "it might be worth considering whether perhaps".
