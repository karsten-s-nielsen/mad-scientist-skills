# Contributing

Thank you for your interest in contributing to mad-scientist-skills! This project is a collection of Claude Code audit skills, and contributions that add new skills, sharpen existing ones, or fix false positives are very welcome.

## Prerequisites

- [Claude Code](https://claude.ai/code) with plugin support enabled
- Git

## Repository Structure

Skills live under the following path inside the plugin directory:

```
plugins/mad-scientist-skills/
└── skills/
    └── <skill-name>/
        ├── SKILL.md        # Skill definition (YAML frontmatter + body)
        └── templates/      # Optional output templates
```

Each skill is self-contained in its own directory. The skill name must be lowercase and hyphenated (e.g., `security-audit`, `optimization-audit`).

## Skill File Format

`SKILL.md` uses YAML frontmatter followed by a Markdown body.

**Frontmatter**

```yaml
---
name: my-skill-name
description: One-sentence description of what this skill audits.
---
```

**Body structure**

The Markdown body should include, in order:

1. **Title** — `# My Skill Name` matching the frontmatter `name`
2. **Triggers** — conditions or slash commands that invoke the skill
3. **Mode detection** — how the skill determines its operating context
4. **Severity** — severity levels used in findings (Critical / High / Medium / Low)
5. **Phases** — numbered audit phases with clear goals and outputs
6. **Important rules** — constraints the skill must follow (e.g., no false positives, cite evidence, token limits)

## Commit Conventions

This project follows [Conventional Commits](https://www.conventionalcommits.org/).

```
<type>(<scope>): <short description>
```

| Type | Use for |
|------|---------|
| `feat` | New skill or significant new capability |
| `fix` | Correcting a false positive, broken phase, or wrong output |
| `docs` | README, CONTRIBUTING, or inline documentation changes |

The **scope** should be the skill name:

```
feat(security-audit): add prompt-injection detection phase
fix(optimization-audit): remove false positive for list comprehensions
docs(contributing): clarify skill file format
```

## Testing

Before opening a PR, test your skill against at least one real repository:

1. **Install locally** — copy the plugin directory into your Claude Code plugins path.
2. **Invoke on a real repo** — run the skill against a non-trivial codebase (not a toy example).
3. **Verify findings** — confirm that every reported finding is backed by actual evidence in the code.
4. **Check for false positives** — review findings manually; a skill that cries wolf is worse than no skill.

A finding is only valid if you can point to a specific file and line that justifies it. If you cannot, the skill needs refinement before it ships.

## PR Process

1. Fork the repository and create a feature branch from `main`:
   ```
   git checkout -b feat/my-new-skill
   ```
2. Make your changes following the skill file format and commit conventions above.
3. Test the skill against a real repository (see Testing section).
4. Open a pull request against `main` with a clear description of what the skill audits and what testing you performed.
5. Address any review feedback.

Please read our [Code of Conduct](CODE_OF_CONDUCT.md) before contributing.
