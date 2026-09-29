# ADR-003: Documentation layout — split specs, plans, and ADRs

| Field | Value |
|---|---|
| **Date** | 2026-09-29 |
| **Status** | Accepted |
| **Deciders** | Karsten S. Nielsen |

## Context

`docs/plans/` historically held both `-design.md` (specs) and `-plan.md`, a flat
folder mixing two artifact types. A design doc therefore sat in a folder named
"plans" — the bundling that surfaced when a new optimization-audit design was
written to `docs/plans/`. Peer repos (silly-kicks) keep specs, plans, and ADRs as
three semantically-distinct directories.

This repo already half-anticipated the split: `documentation-audit/SKILL.md`
exempts `docs/specs/` as an internal-docs path, but no `docs/specs/` directory
existed — the reference was dangling.

`docs/superpowers/` is deliberately gitignored scratch (the `brainstorming` /
`writing-plans` skills default there; nothing under the path has ever been
committed). Any layout that tracks specs must not repurpose that scratch area.

## Decision

Tracked planning docs use three top-level, semantically-split directories:
`docs/specs/` (design docs and `-research.md`), `docs/plans/` (`-plan.md`),
`docs/adrs/` (ADRs). All are under `docs/` and committed. `docs/superpowers/`
remains gitignored scratch. Design and research docs never live in `docs/plans/`.

## Alternatives considered

| Option | Pros | Cons | Why rejected |
|---|---|---|---|
| A. Keep flat `docs/plans/` (both types) | Zero moves | Mixes artifact types; a design in a "plans" folder is exactly the bundling this fixes | Does not solve the problem |
| B. `docs/superpowers/{specs,plans,adrs}` (exact silly-kicks match) | Cross-repo path identity | Requires un-ignoring the deliberately-scratch `docs/superpowers/`, exposes never-committed scratch files, forces moving ADRs and rewriting every `docs/adrs/` cross-reference | Large blast radius; contradicts the scratch policy (Chesterton's Fence) |
| C. `docs/specs/` + `docs/plans/` + `docs/adrs/` top-level (chosen) | Makes reality match the repo's own `documentation-audit` reference to `docs/specs/`; no `.gitignore` change; ADRs unmoved; minimal and reversible | Contributors must learn the split; a docstring, a SKILL.md table, the `.gitignore` comment, and the staying plans' design-doc cross-references need updating | — |

## Consequences

### Positive

- Three artifact types (spec / plan / decision) are structurally distinct and self-evident from the path.
- The repo's own `documentation-audit` reference to `docs/specs/` is no longer dangling.
- A guard test (`tests/test_docs_layout.py`) makes the bundling structurally impossible to reintroduce — it asserts the six migrated basenames live in `docs/specs/` and that no `-design.md`/`-research.md` remains in `docs/plans/`.

### Negative

- Tooling or muscle-memory that assumed "all planning docs in `docs/plans/`" must learn the split. Call sites updated: the test-guard docstring, the `optimization-audit` doc-scan table, the `.gitignore` comment, and the seven design/research cross-references inside the staying `-plan.md` files.

### Neutral

- **No version bump.** `docs/` is not in the shipped plugin payload (the install cache holds only `.claude-plugin/` + `skills/`, per ADR-002), so the reorg reaches no installer and needs no release. A repo-scoped `CHANGELOG.md` entry records it.
- Git records the six moves as renames, so history is content-preserving.
- The concurrent optimization-audit feature carries its own ADR-004 (output-preserving optimization); this ADR takes 003 because the migration lands first.

## Project Guideline Amendment

None required beyond the `.gitignore` comment, which is amended to list `docs/specs/`
alongside `docs/plans/` and `docs/adrs/` as tracked project history. `CONTRIBUTING.md`
references only `docs/adrs/` and is unchanged.

## Related

- **Repo files:** `tests/test_docs_layout.py` (new guard), `.gitignore` (comment), `tests/test_agents_md_awareness.py` (docstring), `plugins/mad-scientist-skills/skills/optimization-audit/SKILL.md` (doc-scan table)
- **Moved files:** six `-design.md`/`-research.md` docs, `docs/plans/` → `docs/specs/`; plus design-doc cross-references repointed in five staying `-plan.md` files
- **Plan:** `docs/plans/2026-09-29-docs-layout-migration-plan.md`
- **ADRs:** ADR-004 (output-preserving optimization) lands in the concurrent optimization-audit PR
- **Changelog:** `CHANGELOG.md` repo-scoped entry (no version)
- **Template:** `docs/adrs/ADR-TEMPLATE.md`
