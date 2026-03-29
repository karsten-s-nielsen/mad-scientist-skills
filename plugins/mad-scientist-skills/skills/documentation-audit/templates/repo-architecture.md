# Repository Architecture Checklist

## Purpose

Answer: "Does this repository have the documentation infrastructure users and contributors expect?"

## Pre-audit checklist

Before auditing, identify:

- [ ] Which essential files exist at the repo root (README, LICENSE, CONTRIBUTING, SECURITY, CHANGELOG)
- [ ] Whether the project is versioned and has release history
- [ ] The public API surface (endpoints, CLI commands, config options)

## Essential Files

### README.md

- **Severity if missing:** Critical
- **Required sections:** Project name + one-line description (not marketing copy), status badges (CI, coverage, version, license — must be current and not broken), quick start (< 5 minutes to first success), installation (prerequisites listed, OS-aware, version-pinned), usage examples (runnable, not pseudocode), contributing pointer (link to CONTRIBUTING.md), license (named, linked)
- **Common deficiencies:** Marketing language instead of technical description, outdated badges, quick start that takes >15 minutes, installation that assumes a specific OS without stating it, examples that don't actually run

### CONTRIBUTING.md

- **Severity if missing:** Medium
- **Required sections:** Dev environment setup (step-by-step with verification), coding standards (or link to linter config), commit message conventions, test coverage requirements, PR process, code review expectations
- **Common deficiencies:** "Fork and submit a PR" with no setup instructions, assumes familiarity with the project's toolchain

### SECURITY.md

- **Severity if missing:** High (for public repos)
- **Required sections:** Vulnerability disclosure policy (email, not public issue), supported versions, reporting process, expected response time
- **Common deficiencies:** Missing entirely, or points to a generic email with no process

### CODE_OF_CONDUCT.md

- **Severity if missing:** Low
- **Required sections:** Community standards, enforcement process

### CHANGELOG.md

- **Severity if missing:** Medium
- **Required sections:** Versioned entries with categories: Added, Changed, Deprecated, Removed, Fixed, Security. Each entry: imperative mood, link to PR/issue, version header with ISO 8601 date
- **Format reference:** Keep a Changelog (keepachangelog.com)

### LICENSE

- **Severity if missing:** High
- **Required:** Present, correctly identified, matches package metadata

### API Documentation

- **Severity if missing:** High (when public API exists)
- **Required:** Coverage relative to public API surface — every public endpoint, function, class documented. Parameters, return types, error codes, usage examples

## Anti-Patterns

| Pattern | Issue | Severity | Fix |
|---------|-------|----------|-----|
| Monolithic AGENTS.md or CLAUDE.md that restates directory structure | Token waste — duplicates discoverable information. Inflates LLM context by >20% | Medium | Keep only non-discoverable information: undocumented gotchas, non-obvious conventions, module-specific architectural landmines |
| Auto-generated docs committed without review | False sense of completeness — generated docs lack context, examples, error documentation | Medium | Review and supplement generated output. Add examples, error codes, and usage context |
| Documentation in wiki/external system with no repo-level pointer | Discoverable only by those who know where to look | High | Add a "Documentation" section to README.md linking to external docs |
| Outdated badges (broken CI badge, wrong version, dead links) | Misleading project status signals | Medium | Automate badge generation or remove stale badges |
| README that starts with a logo and marketing tagline | Wastes prime real estate — first 3 lines should tell the reader what this project IS | Low | Lead with: project name, one-sentence description, then badges. Logo can follow |
