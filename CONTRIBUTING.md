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
        ├── templates/      # Optional output templates
        └── *.py            # Optional runtime scripts the skill invokes
```

Each skill is self-contained in its own directory. The skill name must be lowercase and hyphenated (e.g., `security-audit`, `optimization-audit`).

A skill directory ships **verbatim** to everyone who installs the plugin, so it should
hold only what the skill needs at runtime. Tests therefore live in a top-level `tests/`
tree that mirrors the skill path:

```
conftest.py                 # puts each skill dir on sys.path for its tests
pytest.ini                  # pins rootdir so that conftest is always found
tests/
└── skills/
    └── <skill-name>/       # mirrors plugins/<plugin>/skills/<skill-name>/
```

Because the tests no longer sit beside the module they exercise, they cannot import it
as a sibling — the root `conftest.py` handles that. Add a skill to its tuple when that
skill ships an importable Python module.

Run the suite with `python -m pytest tests -q`; the `pytest` CI job gates it on every
PR. Any `python -m pytest` invocation works from any directory, because `pytest.ini`
anchors `rootdir` at the repo root and pytest loads the conftest from there. Running a
test file as a bare script (`python tests/skills/c4/test_matcher.py`) does **not** work
— that path never reaches the conftest, so the import fails.

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

## Skill Categories

mad-scientist-skills contains two categories of skills plus a review gate:

| Category | When it fires | Examples | Output |
|---|---|---|---|
| **Retrospective audit** | After code exists — "audit this codebase for X" | `architecture-audit`, `cognitive-interface-audit`, `documentation-audit`, `observability-audit`, `optimization-audit`, `security-audit` | Prioritised findings report |
| **Pre-change gate** | Before a code change — "about to modify this function" | `measure-before-optimize` (peer to `optimization-audit`) | Before/after delta, regression flag |
| **Review gate** | After a change, before commit — "final review before shipping" | `final-review` | Structured pre-commit checklist |

When adding a new skill, decide its category first. Retrospective audits and pre-change gates often come in **peer pairs** (e.g., `measure-before-optimize` ↔ `optimization-audit`): the pre-change gate captures a baseline and prevents regressions; the retrospective audit finds issues in code that already exists. A peer pair must have **distinct trigger descriptions** so the Skill tool can select between them without ambiguity — `measure-before-optimize`'s description begins with "Pre-change measurement gate," while `optimization-audit`'s begins with "Comprehensive optimization audit."

## Architectural Decision Records

Significant architectural decisions — ones future contributors will reasonably ask "why?" about — are documented in `docs/adrs/` using the Michael Nygard format captured in `docs/adrs/ADR-TEMPLATE.md`. The `final-review` skill Phase 2.5 scans for decisions that warrant an ADR and prompts for one before commit.

**When to write an ADR:**

- Introducing a new skill category (e.g., adding pre-change gates alongside retrospective audits — see `ADR-001`)
- Establishing a naming convention that future skills will follow (e.g., the `<action>-before-<phase>` peer-skill pattern)
- Changing an existing skill's trigger scope in a way that affects plugin identity
- Adopting a cross-cutting policy (e.g., "all audit skills must have a Planning mode", or "tests live outside skill directories" — see `ADR-002`)
- Retiring or deprecating a skill that users may already depend on

**When NOT to write an ADR:**

- Adding a new phase to an existing skill if it fits the existing thematic pattern
- Fixing a false positive or broken phase output
- Documentation-only changes
- Routine skill refinement (clearer prose, better examples, updated templates)

**Existing ADRs:** `docs/adrs/ADR-*.md`. **Template:** `docs/adrs/ADR-TEMPLATE.md`.

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
| `refactor` | Restructuring with no change to runtime behaviour (e.g. moving tests out of the shipped payload) |

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
