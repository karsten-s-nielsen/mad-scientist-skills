# ADR-NNN: <Title>

| Field | Value |
|---|---|
| **Date** | YYYY-MM-DD |
| **Status** | Proposed / Accepted / Deprecated / Superseded by ADR-MMM |
| **Deciders** | <names> |

## Context

What problem are we solving? What constraints apply? What is the forcing function? Keep this to 2–4 short paragraphs. Include concrete details where relevant (existing skill inventory, plugin identity, release cadence, prior art, forcing incidents).

## Decision

What did we decide? One or two sentences, no hedging. A future contributor should be able to read this sentence in isolation and know what the decision was.

## Alternatives considered

| Option | Pros | Cons | Why rejected |
|---|---|---|---|
| A. <option> | <short list> | <short list> | <one line> |
| B. <option> | <short list> | <short list> | <one line> |
| C. <chosen> | <short list> | <short list> | — |

This section is the part future contributors wonder about most. Be concrete about what you looked at and why you did not choose it. If option A was rejected because of a semantic mismatch, name the mismatch. If option B was rejected because of skill-selection ambiguity, cite the description collision.

## Consequences

### Positive

- What gets better or becomes possible.
- Concrete capabilities unlocked for users or contributors.

### Negative

- What gets worse, what debt we accept, what we lose.
- What future contributors will need to understand or maintain because of this choice.

### Neutral

- Side effects worth noting but not valenced (e.g., version bump required, documentation surface expands).

## Project Guideline Amendment

Optional. Use this section only when the decision requires a documented change to a project guideline in `CONTRIBUTING.md`, `README.md`, a skill contract, or another governance document. Quote the exact rule being amended and note the scope of the change.

Example:
> CONTRIBUTING.md "Skill Categories" previously listed only retrospective audits. This ADR adds "pre-change gates" as a second category and requires future skills to declare their category in SKILL.md.

Omit this section if the decision does not require any guideline document to be amended.

## Related

Include only the categories that apply to this decision. Omit categories that are not relevant.

- **Commits:** `<sha>`, `<sha>`
- **Plugin files:** `plugins/mad-scientist-skills/skills/<skill-name>/SKILL.md`
- **Issues / PRs:** `#NNN`
- **ADRs:** supersedes `ADR-XXX`, superseded by `ADR-YYY`
- **Changelog:** `CHANGELOG.md` entry for `[X.Y.Z] - YYYY-MM-DD`
- **External references:** links to academic methodology, library docs, Claude Code plugin spec changes

## Notes

Optional. Use this section for supporting evidence, prior-art analysis, benchmark output, experiment results, or anything else that does not fit the sections above but would help a future contributor understand the decision.
