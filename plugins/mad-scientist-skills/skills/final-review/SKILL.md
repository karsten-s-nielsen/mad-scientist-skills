---
name: final-review
description: Pre-commit quality gate — reviews all code and documentation for consistency, best practices, and completeness, then generates or updates the C4 architecture diagram. Use before committing, or when you want a thorough quality check of the project. Triggers on phrases like "final review", "pre-commit check", "review everything before commit", or "make sure everything is up to date".
---

# Final Review

A comprehensive pre-commit quality gate that ensures code, documentation, and architecture diagrams are consistent, complete, and follow professional standards.

## When to use this skill

- Before committing or pushing changes
- After completing a feature or significant refactor
- When the user says "final review", "check everything", "make sure it's all up to date", or "review before commit"
- Periodically to catch documentation drift

## Review process

Execute all phases in order. Do NOT skip phases. Do NOT claim completion without evidence.

### Phase 1: Codebase Discovery

Explore the project to understand its current state:

- Read the project's `CLAUDE.md`, `AGENTS.md`, `README.md`, and any other root-level documentation
- Identify the tech stack, project structure, and architectural patterns
- Note the testing framework and how tests are run
- Identify all configuration files (`package.json`, `pyproject.toml`, `tsconfig.json`, etc.)

### Phase 2: Code Quality Review

Review all source code as a professional software architect:

- **Consistency**: Naming conventions, file organization, import patterns, error handling patterns
- **Best practices**: SOLID principles, DRY, proper error handling, security (OWASP top 10)
- **Dead code**: Unused imports, unreachable code, commented-out blocks, orphaned files
- **Type safety**: Missing types, `any` usage, incomplete interfaces
- **Dependencies**: Unused dependencies, outdated versions with known vulnerabilities
- **Tests**: Coverage gaps, missing edge cases, outdated test assertions

For deeper analysis, run the specialized audit skills from this plugin:

- **`security-audit`** — STRIDE threat modeling, infrastructure hardening, supply chain audit, secrets scanning
- **`observability-audit`** — logging, metrics, tracing, alerting, SLI/SLO coverage
- **`optimization-audit`** — algorithm efficiency, database queries, caching, concurrency, cloud cost
- **`cognitive-interface-audit`** — usability, mental model alignment, cognitive load, accessibility (if UI exists)
- **`documentation-audit`** — linguistic precision, structural taxonomy, audience calibration, completeness

For each issue found, categorize by severity:

| Severity | Action | Examples |
|----------|--------|---------|
| **Critical** | Must fix before commit | Security vulnerability, broken functionality, data loss risk |
| **High** | Should fix before commit | Inconsistent patterns, missing error handling, poor naming |
| **Medium** | Note for future | Minor style inconsistency, potential optimization |
| **Low** | Track in backlog | Best practice deviation, minor polish |

### Phase 2.5: Architectural Decision Review

Scan the change for architectural decisions that future maintainers will reasonably ask "why?" about. Decisions matching any of these patterns are ADR-worthy:

- Introduces, removes, or replaces a cross-cutting dependency
- Changes a schema ownership or grants model
- Hard-codes a workaround for a platform constraint (Databricks Serverless, MSYS path handling, etc.)
- Introduces a naming, identifier, or path convention with downstream consumers
- Reimplements an algorithm to avoid a dependency
- Introduces a defense-in-depth control or security boundary

For each decision matched, ask: "Is this documented in an ADR?"

- **No ADR exists**: prompt the user to draft one using the project's ADR template (commonly `docs/adrs/ADR-TEMPLATE.md` or `docs/superpowers/adrs/ADR-TEMPLATE.md`) before commit. If the user approves, draft the ADR inline during final-review.
- **Stale ADR exists**: update the existing ADR's Status field and Consequences section to reflect the current change.
- **Current ADR exists**: confirm and move to Phase 3.

This sub-phase is a prompt, not a block. Operator judgment decides whether a decision rises to ADR-worthiness. The check is a decision inventory, not a gate.

### Phase 3: Documentation Review

Ensure all documentation reflects the current state of the code:

- **README.md**: Installation instructions still work? Features list accurate? Examples current? API docs match actual endpoints?
- **CLAUDE.md**: Project instructions still valid? Architecture section matches reality? Test commands work?
- **AGENTS.md**: If present, does it reflect current file structure?
- **Code comments**: Do they match what the code actually does? Any TODO/FIXME/HACK comments that should be resolved?
- **API documentation**: Do endpoint docs match actual request/response shapes?
- **Configuration docs**: Do documented env vars match what the code actually reads?
- **Changelog**: Is the `CHANGELOG` updated for this change? (Version consistency and the bump itself are handled in **Phase 3.5**.)

Fix any documentation that has drifted from the code. Documentation must describe what IS, not what WAS.

### Phase 3.5: Release Hygiene — version bump and TODO

Run this when the change is being **released** — a version bump is intended, or `CHANGELOG`'s `[Unreleased]` section has accumulated entries. If it is genuinely not a release (a WIP checkpoint the user named as such), skip it and say so. If unsure whether this is a release, ask.

**No unapproved deferrals.** Nothing is deferred, dropped, added to a TODO, or left as a follow-up without the user's explicit approval — this is the author-side of `unbiased-review`'s Hard rule 8 (which `/review-impl` enforces), and a standing rule everywhere. A new backlog entry *is* deferred scope: confirm the user approved it before writing it, and never grow the backlog just to make a release read clean.

**Version bump — everywhere, once, the repo's own way:**

**Single-source first.** The best bump is the one with nothing to sync. If the version is single-sourced — e.g. hatch `[tool.hatch.version]` reading one `_version.py`, with `[project] version` dynamic and `__version__` derived — bumping that one file is the whole job. If instead the same number is hand-typed across several files, the real fix is to *single-source it* (delete the duplication), not to add a script that syncs copies; reserve a sync script for version strings you genuinely cannot derive from package metadata (IaC, wheel URLs, deploy scripts). Then:

1. **Find the mechanism before editing any version string.** Prefer a procedure the repo documents (its `CLAUDE.md`, a `RELEASING.md`). Otherwise discover it: a bump tool or script — a `version` in `pyproject.toml` `[project]`/`[tool.*]`, `.bumpversion.cfg`, `scripts/bump*`, a `Makefile` `bump`/`release` target, `npm`/`poetry`/`hatch version`.
2. **If a script or tool owns the version, run it — do not hand-edit the files it manages.** Editing a subset by hand is the recurring corruption: some files move, the rest silently lag. (luxury-lakehouse: edit `pyproject.toml`, then `uv run python scripts/bump_wheel.py` propagates the wheel version to every consumer — deploy scripts, Terraform, PEP-723 scripts — and `bump_wheel.py --check` is the CI gate that catches a stale one. Hand-editing those consumers is wrong.)
3. **If there is no script, update EVERY file that declares the version — all of them.** Do not work from memory of "the N files": find them with `git grep -nF "<current-version>"` (excluding `CHANGELOG`/history) and update each real declaration. (silly-kicks has no bump script and carries the version in several files; missing one is the classic release bug.)
4. **Verify the bump landed everywhere.** After bumping, `git grep -nF "<old-version>"` must return nothing outside history/changelog; run the bump tool's `--check` if it has one. A stray old version is a partial bump — the exact failure this step exists to prevent.
5. If you had to discover the procedure rather than read it, offer to record it (in the repo's `CLAUDE.md` or a `RELEASING.md`) so the next release doesn't re-derive it.

Match each version-bearing file's existing format; never guess it.

**TODO / backlog document — maintain at release:**

If the repo has a TODO / backlog / roadmap doc:

1. **Replace the top summary; keep no history.** These docs open with a "Last updated" / "Current (unreleased)" style block. Replace it wholesale with *only* the current release's summary — do not append, and do not keep prior releases' summaries. Git and the `CHANGELOG` hold history.
2. **Remove completed items entirely.** Every item shipped in this release is deleted from its section (on-deck, tech-debt, research — whatever the repo calls them). Leaving a shipped item in place — marked done, ticked, struck through, or moved to a "Completed" section — is **banned**. The convention is *no breadcrumbs on shipped work*.
3. **Preserve the document's shape.** Keep its headings, ordering, and any legend, and match its style; if the repo has a TODO-format test (e.g. silly-kicks' `tests/test_todo_md_format.py`, which guards the shape without pinning specific IDs precisely so shipped entries can leave), it must still pass. Read the doc's own structure and match it — do not impose a new one.

### Phase 4: Architecture Diagram

Generate or update the C4 architecture diagram by following the `c4` skill from this plugin. **Read and follow the c4 skill's SKILL.md in full** — including its rendering workflow (Structurizr DSL export via structurizr.war + plantuml.jar, requires Java 21+).

1. **Analyze the codebase** to identify:
   - Actors/users of the system
   - The system boundary and its purpose
   - External systems and dependencies
   - Containers: deployable units (apps, services, databases, queues)
   - Key components within major containers
   - Communication protocols between elements

2. **Generate `architecture.html`** in the project root following the c4 skill's templates and rendering workflow:
   - Include System Context (Level 1) — always
   - Include Container diagram (Level 2) — always
   - Include Component diagram (Level 3) — if the project has sufficient internal complexity
   - Include Dynamic diagram — if there are key user flows worth documenting
   - Include Deployment diagram — if infrastructure is defined (Docker, cloud config, etc.)

3. **If `architecture.html` already exists**, regenerate it to reflect the current state of the codebase. The diagram must match reality, not a previous snapshot.

4. **Reference from README.md** — Ensure the project's README links to the architecture diagram. If no reference exists, add an "Architecture" section with a link. Use this pattern:

   ```markdown
   ## Architecture

   Open [`architecture.html`](architecture.html) in a browser to explore the C4 architecture diagrams (System Context, Container, Component, etc.).
   ```

   Place it after the project description or installation section — wherever it fits naturally in the existing README structure. If an architecture section already exists, verify the link is correct and the description matches which diagram levels are included.

### Phase 5: Verification Summary

Present a structured summary to the user:

```
## Final Review Summary

### Code Quality
- [x] Naming conventions consistent
- [x] Error handling patterns uniform
- [ ] Found 2 warnings (see details below)

### Documentation
- [x] README.md up to date
- [x] CLAUDE.md accurate
- [ ] Updated API docs to match new endpoint

### Architecture Diagram
- [x] architecture.html generated/updated
- Levels included: Context, Container, Component

### Architectural Decisions
- [x] Decision inventory scanned (Phase 2.5)
- [x] ADRs up to date / drafted where needed

### Release Hygiene (if this is a release)
- [x] Version bumped to X.Y.Z — verified no stale old version remains (bump script run, or every version-bearing file updated)
- [x] TODO/backlog: top summary replaced with this release only; N completed items removed entirely; structure intact
- [x] Nothing deferred or added to the backlog without approval

### Issues Found
| # | Severity | File | Issue | Status |
|---|----------|------|-------|--------|
| 1 | High | src/api.ts:42 | Missing error handler on async route | Fixed |
| 2 | High | README.md | Outdated install command | Fixed |
| 3 | Low | src/utils.ts:15 | Could extract to shared helper | Noted |

### Ready to commit: Yes / No (with blockers)
```

## Important rules

- **Fix as you go.** Don't just report — remediate. Fix Critical and High issues during the review.
- **No unapproved deferrals.** Nothing is deferred, dropped, added to a TODO, or left as a follow-up without the user's explicit approval. Surface it and ask — do not pre-decide it (Phase 3.5).
- **Version bump is all-or-nothing.** If the repo has a bump script/tool, run it and never hand-edit the files it owns; otherwise update every file that declares the version and verify no stale version remains (Phase 3.5).
- **Evidence-based claims.** Every "up to date" claim must come from actually reading the file and comparing to code.
- **No assumptions.** Read the actual files. Don't assume README is correct because it existed before your changes.
- **Architecture diagram is mandatory.** Every final review produces or updates `architecture.html`.
- **Respect existing style.** Match the project's conventions, don't impose new ones.
