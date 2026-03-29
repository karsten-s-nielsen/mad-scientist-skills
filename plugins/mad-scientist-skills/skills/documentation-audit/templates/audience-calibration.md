# Audience Calibration Reference

## Purpose

Answer: "Does this documentation meet readers where they are — not where the author assumes they are?"

## Pre-audit checklist

Before auditing, identify:

- [ ] The primary audience segments (newcomer, regular user, contributor, operator)
- [ ] Domain-specific terms used in the documentation
- [ ] Whether a glossary exists
- [ ] The navigation structure and entry points

## Expert Blind Spot Audit (Hinds 1999)

Experts systematically underestimate task difficulty for novices. In documentation, this manifests as:
- Terms used without definition (the author knows what they mean; the reader may not)
- Steps skipped (the author does them automatically; the reader doesn't know they exist)
- Context assumed (the author knows why; the reader only sees what)

### Expert Blind Spot Worksheet

For each domain-specific term, abbreviation, or metric used in the documentation:

| Term | Domain Expert Can Interpret? | Newcomer Can Interpret? | Both Fail? | Required Fix |
|------|-----|-----|------|------|
| [term] | Y/N | Y/N | If either N → fix | Tooltip / inline definition / glossary entry / contextual help |

**Classification:**
- Either audience fails → **High** — requires at minimum: inline explanation, reference value, or link to glossary
- Both audiences fail → **Critical** — the term is opaque to everyone except the author

### Glossary Completeness Check

1. Inventory every unique technical term, abbreviation, and acronym across all docs
2. Cross-reference against glossary/help system (if one exists)
3. Any displayed term without a corresponding glossary entry is a gap
4. An incomplete glossary is itself a blind spot — the author assumed certain terms were obvious because they were obvious to the author (Hinds 1999)

## Assumed Context Checklist

Every "simply", "just", "obviously", "easily" in documentation hides an unstated assumption. Inventory them:

| Assumption Category | What to Check | Example Violation |
|-------|------|------|
| Operating system | Do commands assume Unix/Mac? Windows users? | `export VAR=value` without noting Windows equivalent |
| Package manager | Does it assume npm? pip? brew? What if user has none? | "Install with `brew install tool`" — what about Linux/Windows? |
| Runtime version | Does it assume latest? Specify minimum? | "Run `node app.js`" without specifying Node.js version |
| Network access | Does it assume internet? Proxy? Firewall? | "Pull the Docker image" in an air-gapped environment |
| Permissions | Does it assume sudo/admin? What if not? | `sudo apt install` without noting permission requirement |
| Prior installation | Does it assume Docker/Git/Make/etc. installed? | "Run `make build`" without noting make must be installed |
| Domain knowledge | Does it assume REST/SQL/k8s concepts? | "Create a deployment manifest" — assumes Kubernetes knowledge |
| Prior documentation | Does it assume reader has read another doc first? | "As described in the Setup Guide..." — link? Which part? |

## Information Scent Scoring (Pirolli & Card 1999)

Users follow "information scent" — cues predicting whether a link leads to their goal. Navigation labels are scent cues.

### Per-Label Scoring Table

Score every top-level navigation label:

| Navigation Label | Target User Goal | Scent Strength | Issue (if Weak/Medium) |
|-----------------|------------------|----------------|------------------------|
| [label] | [what goal does the user expect this leads to?] | Strong / Medium / Weak | [why the label fails to predict content] |

**Scoring criteria:**
- **Strong**: Label uses the user's goal vocabulary. User would confidently click. ("Getting Started", "API Reference", "How to Deploy")
- **Medium**: Label is related but requires inference. User might click or might not. ("Resources", "Guides", "Advanced")
- **Weak**: Implementation/developer vocabulary, abbreviations, or jargon without context. User has no idea what's behind the link. ("Modules", "Core", "Internals", "Utils")

**Labels that use implementation vocabulary score Weak for newcomers.** Goal-oriented labels score Strong.

## Expertise Spectrum Design

| Level | Mental Model | Documentation Need | Design Requirement |
|-------|-------------|-------------------|-------------------|
| **Newcomer** | No pre-existing model. Learning vocabulary and structure | Self-explanatory, guided, minimal choices per step | Quick-start tutorial, glossary, prerequisites listed, verification at each step |
| **Regular** | Functional model. Knows vocabulary, common paths | Consistent patterns, predictable navigation | How-to guides, searchable reference, cross-links between related topics |
| **Expert** | Compiled methods. Wants efficiency, not explanation | Don't slow them down — shortcuts, density, batch operations | API reference, advanced config, CLI reference, troubleshooting |

The documentation must degrade gracefully across all three levels. An expert shortcut must not confuse a newcomer. A newcomer's guided flow must not impede an expert.

## Safe, Successful, Known (Lemov Principle 5)

Documentation builds trust through three mechanisms:

| Mechanism | Audit Check | Deficient Example | Exemplar |
|-----------|------------|-------------------|----------|
| **Safe** | Does the doc acknowledge failure points proactively? | Step fails silently; reader doesn't know if they did it wrong | "If you see `ConnectionRefused`, check that Redis is running: `redis-cli ping` should return `PONG`" |
| **Successful** | Does the doc provide early wins before tackling complexity? | Tutorial starts with the hardest integration | Tutorial begins with a working "Hello World" in 3 steps, then layers complexity |
| **Known** | Does the doc acknowledge different reader profiles? | One-size-fits-all language | "If you're coming from Django, the middleware pattern here works similarly..." / "For ops engineers: skip to the Deployment section" |
