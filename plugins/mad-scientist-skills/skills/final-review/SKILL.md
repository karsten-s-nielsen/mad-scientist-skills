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

### Phase 3: Documentation Review

Ensure all documentation reflects the current state of the code:

- **README.md**: Installation instructions still work? Features list accurate? Examples current? API docs match actual endpoints?
- **CLAUDE.md**: Project instructions still valid? Architecture section matches reality? Test commands work?
- **AGENTS.md**: If present, does it reflect current file structure?
- **Code comments**: Do they match what the code actually does? Any TODO/FIXME/HACK comments that should be resolved?
- **API documentation**: Do endpoint docs match actual request/response shapes?
- **Configuration docs**: Do documented env vars match what the code actually reads?
- **Changelog/version**: Are version numbers consistent across all files that declare them?

Fix any documentation that has drifted from the code. Documentation must describe what IS, not what WAS.

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
- **Evidence-based claims.** Every "up to date" claim must come from actually reading the file and comparing to code.
- **No assumptions.** Read the actual files. Don't assume README is correct because it existed before your changes.
- **Architecture diagram is mandatory.** Every final review produces or updates `architecture.html`.
- **Respect existing style.** Match the project's conventions, don't impose new ones.
