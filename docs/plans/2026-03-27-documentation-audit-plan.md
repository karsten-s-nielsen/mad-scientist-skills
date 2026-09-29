# Documentation Audit Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create a documentation-audit skill that evaluates repository documentation quality across linguistic precision, structural taxonomy (Diataxis), pedagogical scaffolding (CLT/Carroll/Lemov), consistency, repo architecture, audience calibration, and content freshness.

**Architecture:** Single SKILL.md with 10 phased audit process (Phases 0-9), two modes (Planning/Audit), single tier. Six domain-specific templates plus one portable audit-methodology template. Follows the established pattern from cognitive-interface-audit and optimization-audit skills.

**Tech Stack:** Markdown only — this is a Claude Code skill plugin. No runtime code, no tests. Validation is by invoking the skill against a target repository.

---

## File Structure

| File | Responsibility | Est. Lines |
|------|---------------|-----------|
| **Create:** `plugins/mad-scientist-skills/skills/documentation-audit/SKILL.md` | Main skill: frontmatter, academic foundations, mode detection, severity classification, phases 0-9, important rules | ~750 |
| **Create:** `plugins/mad-scientist-skills/skills/documentation-audit/templates/diataxis-checklist.md` | Diataxis quadrant classification guide, pollution detection, Good Docs Project extensions | ~150 |
| **Create:** `plugins/mad-scientist-skills/skills/documentation-audit/templates/linguistic-rules.md` | Strunk & White + Google/Microsoft rules with grep patterns and permitted exceptions | ~180 |
| **Create:** `plugins/mad-scientist-skills/skills/documentation-audit/templates/pedagogical-scaffolding.md` | Carroll + CLT + Merrill + Lemov content heuristics with annotated work samples | ~200 |
| **Create:** `plugins/mad-scientist-skills/skills/documentation-audit/templates/repo-architecture.md` | Essential file checklist with required sections, anti-patterns | ~100 |
| **Create:** `plugins/mad-scientist-skills/skills/documentation-audit/templates/audience-calibration.md` | Expert blind spot worksheet, info scent scoring, assumed context checklist | ~130 |
| **Create:** `plugins/mad-scientist-skills/skills/documentation-audit/templates/audit-methodology.md` | Portable Lemov audit methodology (reusable by other audit skills) | ~180 |
| **Modify:** `plugins/mad-scientist-skills/.claude-plugin/plugin.json` | Add documentation-audit to plugin description, bump version | ~10 lines changed |

All paths are relative to the repo root: `D:/Development/karstenskyt__mad-scientist-skills/`

---

### Task 1: Create directory structure and SKILL.md frontmatter + foundations

**Files:**
- Create: `plugins/mad-scientist-skills/skills/documentation-audit/SKILL.md`

- [ ] **Step 1: Create the skill directory**

```bash
mkdir -p plugins/mad-scientist-skills/skills/documentation-audit/templates
```

- [ ] **Step 2: Write SKILL.md — frontmatter, introduction, academic foundations, mode detection, severity classification**

Write the first ~120 lines of SKILL.md covering:
- Frontmatter (name, description with full academic citation list)
- Skill introduction (modes, single tier, core question)
- Academic foundations (7 numbered research threads with citations)
- Key references list
- "When to use this skill" trigger list
- Mode detection table
- Severity classification table

The frontmatter `description` field must include all trigger phrases and framework names so Claude Code's skill matcher can find it. Follow the pattern from cognitive-interface-audit SKILL.md lines 1-3.

Reference the design spec at `docs/specs/2026-03-27-documentation-audit-design.md` for the exact content of each section.

- [ ] **Step 3: Commit**

```bash
git add plugins/mad-scientist-skills/skills/documentation-audit/SKILL.md
git commit -m "feat(documentation-audit): add SKILL.md frontmatter, foundations, mode detection, severity (v1.11.0-wip)"
```

---

### Task 2: Write SKILL.md Phase 0 (Anti-Pattern Scan) and Phase 1 (Discovery)

**Files:**
- Modify: `plugins/mad-scientist-skills/skills/documentation-audit/SKILL.md`

- [ ] **Step 1: Append the audit process header and Phase 0**

Add after the severity classification section:
- Audit process header with phase order (0 → 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8 → 9)
- Phase 0: Anti-Pattern Scan (Audit mode) — two tables: linguistic anti-patterns (6 rows) and structural anti-patterns (6 rows). Each row has: pattern, issue with framework attribution, severity. Output specification.

Content is fully specified in the design spec Phase 0 section. Reproduce it in full — do not summarize or abbreviate.

- [ ] **Step 2: Append Phase 1 (Discovery)**

Add Phase 1: Discovery (Both modes) — bulleted list of 10 discovery items (read docs, inventory files, identify tech stack, map audiences, identify core tasks, assess maturity, catalog constraints, note conventions, check for existing style guide, identify multiple surfaces). Output specification.

Content is fully specified in the design spec Phase 1 section.

- [ ] **Step 3: Commit**

```bash
git add plugins/mad-scientist-skills/skills/documentation-audit/SKILL.md
git commit -m "feat(documentation-audit): add Phase 0 anti-pattern scan and Phase 1 discovery"
```

---

### Task 3: Write SKILL.md Phase 2 (Diataxis Classification) and Phase 3 (Linguistic Precision)

**Files:**
- Modify: `plugins/mad-scientist-skills/skills/documentation-audit/SKILL.md`

- [ ] **Step 1: Append Phase 2 (Diataxis Classification)**

Add Phase 2: Diataxis Classification (Both modes):
- `Load templates/diataxis-checklist.md` reference
- Planning mode: 5 design questions
- Audit mode: check table with 11 rows (quadrant identity, tutorial contract, tutorial pollution, how-to title, how-to focus, reference austerity, reference structure, explanation scope, missing types, non-quadrant types, separation strategy)
- Output specification

Content is fully specified in the design spec Phase 2 section.

- [ ] **Step 2: Append Phase 3 (Linguistic Precision)**

Add Phase 3: Linguistic Precision (Audit mode):
- `Load templates/linguistic-rules.md` reference
- Check table with 16 rows covering: active voice, needless words, positive form, specific/concrete language, parallel construction, conditions before instructions, second person, tense consistency, sentence length, Right Is Right, specific vocabulary, leaner language, weak sentence endings, filler nouns, dangling modifiers, comma splices
- Each row has: check description, rule source attribution, severity
- Output specification

Content is fully specified in the design spec Phase 3 section.

- [ ] **Step 3: Commit**

```bash
git add plugins/mad-scientist-skills/skills/documentation-audit/SKILL.md
git commit -m "feat(documentation-audit): add Phase 2 Diataxis classification and Phase 3 linguistic precision"
```

---

### Task 4: Write SKILL.md Phase 4 (Pedagogical Scaffolding) and Phase 5 (Structural Consistency)

**Files:**
- Modify: `plugins/mad-scientist-skills/skills/documentation-audit/SKILL.md`

- [ ] **Step 1: Append Phase 4 (Pedagogical Scaffolding)**

Add Phase 4: Pedagogical Scaffolding (Both modes):
- `Load templates/pedagogical-scaffolding.md` reference
- Planning mode: 4 design questions
- Audit mode: check table with 13 rows covering: Begin with the End, Knowledge Organizers, Guidance Fading, Worked examples, Verification commands, Cognitive chunking, Split-attention avoidance, Elaborative hooks, Attention design, Immediate meaningful tasks, Error recovery, Application prompts, Integration
- Each row has: check description with bold label, framework attribution, severity
- Output specification

Content is fully specified in the design spec Phase 4 section.

- [ ] **Step 2: Append Phase 5 (Structural Consistency)**

Add Phase 5: Structural Consistency (Audit mode):
- Check table with 11 rows covering: vocabulary alignment, action vocabulary, heading hierarchy, formatting patterns, template adherence, code block formatting, link format consistency, date/version format, tone/register consistency, partial pattern application, empty states
- Output specification

Content is fully specified in the design spec Phase 5 section.

- [ ] **Step 3: Commit**

```bash
git add plugins/mad-scientist-skills/skills/documentation-audit/SKILL.md
git commit -m "feat(documentation-audit): add Phase 4 pedagogical scaffolding and Phase 5 structural consistency"
```

---

### Task 5: Write SKILL.md Phases 6-8 (Repo Architecture, Audience Calibration, Completeness)

**Files:**
- Modify: `plugins/mad-scientist-skills/skills/documentation-audit/SKILL.md`

- [ ] **Step 1: Append Phase 6 (Repository Architecture)**

Add Phase 6: Repository Architecture (Audit mode):
- `Load templates/repo-architecture.md` reference
- Essential files table (7 rows: README, CONTRIBUTING, SECURITY, CODE_OF_CONDUCT, CHANGELOG, LICENSE, API docs) with required sections and severity
- Anti-patterns table (4 rows: monolithic AGENTS.md, auto-generated docs without review, docs in external system with no pointer, outdated badges)
- Output specification

Content is fully specified in the design spec Phase 6 section.

- [ ] **Step 2: Append Phase 7 (Audience Calibration)**

Add Phase 7: Audience Calibration (Audit mode):
- `Load templates/audience-calibration.md` reference
- Check table with 9 rows covering: expert blind spot, glossary completeness, reading level, assumed context, information scent, progressive disclosure, expertise spectrum, cultural/regional assumptions, safe/successful/known
- Output specification

Content is fully specified in the design spec Phase 7 section.

- [ ] **Step 3: Append Phase 8 (Completeness & Freshness)**

Add Phase 8: Completeness & Freshness (Audit mode):
- Check table with 9 rows covering: broken links, outdated content, missing documentation gaps, implicit assumption inventory, cross-reference completeness, changelog currency, example code freshness, screenshot freshness, dependency documentation
- Output specification

Content is fully specified in the design spec Phase 8 section.

- [ ] **Step 4: Commit**

```bash
git add plugins/mad-scientist-skills/skills/documentation-audit/SKILL.md
git commit -m "feat(documentation-audit): add Phases 6-8 repo architecture, audience calibration, completeness"
```

---

### Task 6: Write SKILL.md Phase 9 (Findings Report) and Important Rules

**Files:**
- Modify: `plugins/mad-scientist-skills/skills/documentation-audit/SKILL.md`

- [ ] **Step 1: Append Phase 9 (Findings Report)**

Add Phase 9: Findings Report (Both modes):
- Planning mode report template (markdown code block) with sections: Documentation Surface Summary, Content Type Map, Learning Path Design, Scaffolding Strategy, Documentation Checklist
- Audit mode report template (markdown code block) with sections: Executive Summary, Findings table, Diataxis Classification table, Pedagogical Assessment table, Phase Coverage Matrix, Documentation Maturity Rating, Ready for users

Content is fully specified in the design spec Phase 9 section. Reproduce the full report templates — do not abbreviate.

- [ ] **Step 2: Append Important Rules**

Add the Important Rules section — 12 bulleted rules:
1. Fix as you go
2. Evidence-based claims
3. Framework attribution
4. Right Is Right
5. Exemplar Planning
6. Active Observation
7. Formative before summative
8. No assumptions
9. Scope awareness
10. Respect intentional choices
11. The documentation should be invisible
12. Report self-consistency

Content is fully specified in the design spec Important Rules section.

- [ ] **Step 3: Commit**

```bash
git add plugins/mad-scientist-skills/skills/documentation-audit/SKILL.md
git commit -m "feat(documentation-audit): add Phase 9 findings report and important rules"
```

---

### Task 7: Create templates/diataxis-checklist.md

**Files:**
- Create: `plugins/mad-scientist-skills/skills/documentation-audit/templates/diataxis-checklist.md`

- [ ] **Step 1: Write the Diataxis checklist template**

Write ~150 lines covering:

**Structure:**
```markdown
# Diataxis Classification Checklist

## Purpose
Answer: "Is each document the right type, and does it stay in its lane?"

## The Four Quadrants
[Table with 4 rows: Tutorial, How-To, Reference, Explanation — each with: user state (study/work), knowledge type (practical/theoretical), contract, language markers, structural markers, common violations]

## Quadrant Classification Decision Tree
[Flowchart-style decision tree: Does it teach a newcomer step-by-step? → Tutorial. Does it help a competent user achieve a specific goal? → How-To. Does it describe the machinery? → Reference. Does it explain why/context? → Explanation.]

## Pollution Detection Patterns
[Table: pollution type, signal, example, fix (extract to separate doc with hyperlink)]

## Good Docs Project Extensions
[Table covering non-quadrant document types: README, CHANGELOG, ADR, Troubleshooting Guide, Migration Guide, FAQ — each with: purpose, required sections, Diataxis relationship]

## Classification Worksheet
[Template table for auditor to fill: Document | Assigned Quadrant | Confidence | Pollution Found | Action Required]
```

Each section must contain the actual content — tables filled with real data, real patterns, real examples. No placeholders. The quadrant descriptions come from the Diataxis framework (Procida), pollution patterns from Hillel Wayne's critique and the design spec, and Good Docs extensions from the Good Docs Project template library.

- [ ] **Step 2: Commit**

```bash
git add plugins/mad-scientist-skills/skills/documentation-audit/templates/diataxis-checklist.md
git commit -m "feat(documentation-audit): add Diataxis classification checklist template"
```

---

### Task 8: Create templates/linguistic-rules.md

**Files:**
- Create: `plugins/mad-scientist-skills/skills/documentation-audit/templates/linguistic-rules.md`

- [ ] **Step 1: Write the linguistic rules template**

Write ~180 lines covering:

**Structure:**
```markdown
# Linguistic Rules Reference

## Purpose
Answer: "Does every sentence earn its place?"

## Strunk & White Rules (with grep patterns)
[Table with ~10 rows, each containing: Rule number, Rule name, Grep pattern (regex), Example violation, Corrected version, Permitted exceptions]

Key rules to include with regex:
- Rule 5 (comma splice): pattern for ", and" vs ", [independent clause]"
- Rule 7 (dangling modifier): opening -ing/-ed phrase
- Rule 10 (active voice): "was/were/is/are + past participle"
- Rule 11 (positive form): "not + adjective" where antonym exists
- Rule 12 (specific language): "various|several|aspects|issues|things|areas|elements"
- Rule 13 (needless words): "in order to|the fact that|due to the fact that|it should be noted|for the purpose of|in a .* manner"
- Rule 15 (parallel construction): list items mixing verb forms
- Rule 18 (emphatic position): sentences ending in "however|also|as well|too|etc"

## Google Developer Documentation Style Guide Rules
[Table with ~8 rows: conditions before instructions, second person, timeless language, inclusive terminology, sentence length, link text, alt text, code formatting]

## Microsoft Writing Style Guide Rules
[Table with ~5 rows: contractions (OK in docs), UI terminology, chatbot copy, bias-free communication, global-ready]

## Inclusive Language Substitutions
[Table: term to avoid | replacement | source (Google/Microsoft/alex)]

## Permitted Exceptions
[Bulleted list of when each rule may be intentionally violated — e.g., passive voice when emphasizing the object, "currently" when describing a known temporary state that is documented as temporary]
```

Each rule must include the actual regex pattern for grep-based detection and real before/after examples. The inclusive language table must list at least 15 specific substitutions.

- [ ] **Step 2: Commit**

```bash
git add plugins/mad-scientist-skills/skills/documentation-audit/templates/linguistic-rules.md
git commit -m "feat(documentation-audit): add linguistic rules template with grep patterns"
```

---

### Task 9: Create templates/pedagogical-scaffolding.md

**Files:**
- Create: `plugins/mad-scientist-skills/skills/documentation-audit/templates/pedagogical-scaffolding.md`

- [ ] **Step 1: Write the pedagogical scaffolding template**

Write ~200 lines covering:

**Structure:**
```markdown
# Pedagogical Scaffolding Reference

## Purpose
Answer: "Does this documentation teach effectively, or does it merely present information?"

## Carroll's Minimalism (1990)
[4 principles with documentation-specific interpretation and audit questions:
1. Immediate meaningful tasks — get reader doing real work immediately
2. Minimize passive instruction — cut pre-amble before action
3. Error recognition and recovery — anticipate failures, guide recovery
4. Self-contained modules — each section usable independently]

## Cognitive Load Theory (Sweller 1988)
[3-type taxonomy with documentation design implications:
- Intrinsic load: scaffold with progressive disclosure
- Extraneous load: ELIMINATE (the audit's primary target)
- Germane load: MAXIMIZE (productive schema building)

Split-Attention Effect (Chandler & Sweller 1992):
- Anti-pattern: code block followed by separate paragraph explaining it
- Fix: inline code comments, adjacent annotations, integrated explanation

Guidance Fading Effect (Sweller):
- Novices: explicit step-by-step with verification at each stage
- Intermediates: guided examples with some open-ended elements
- Experts: reference-style documentation, minimal scaffolding
- Anti-pattern: "explore the API" tutorial for first-time users]

## Merrill's First Principles of Instruction (2002)
[5 principles with documentation audit checks:
1. Task-centered: organized around user problems, not system features?
2. Activation: connects to what reader already knows?
3. Demonstration: provides worked examples (not just describes)?
4. Application: requires reader to produce output?
5. Integration: helps connect to existing practice?]

## Lemov Content Quality Techniques
[5 techniques with annotated work samples (good vs. deficient):

### Begin with the End (4 Ms)
- Deficient: "This guide covers authentication." (no measurable objective)
- Exemplar: "After completing this guide, you will be able to authenticate API requests using OAuth 2.0 tokens and handle token refresh." (measurable, specific)

### Knowledge Organizers (#5)
- Deficient: Prerequisites buried at step 7 ("You'll need Redis installed")
- Exemplar: Prerequisites block at document top with version requirements

### Take the Steps / Guidance Fading (#21)
- Deficient: "Configure the database connection and set up migrations"
- Exemplar: Step 1: create config file (show exact content). Step 2: verify connection (show exact command + expected output). Step 3: run migration (show command + expected output).

### Retrieval Practice / Elaborative Hooks (#7)
- Deficient: Procedure with no connection to concepts
- Exemplar: "This uses the same connection pooling pattern from the Database Setup guide. If your pool size seems too small, see Tuning Connection Pools."

### Right Is Right (#16)
- Deficient: "The function returns a list of objects" (rounds up)
- Exemplar: "The function returns a paginated list of User objects ordered by creation date, max 100 per page. Returns an empty array (not null) when no results match."]

## Worked Example Quality Assessment
[Table: Example Type | When Required | Audit Check
- Product-oriented (shows final result only) | Simple, well-structured tasks | Does the reader need to understand WHY this works?
- Process-oriented (shows reasoning + decisions) | Complex, ill-structured tasks | Does the example narrate the decision process?]

## Verification Command Checklist
[Table of verification patterns by technology:
- Web server: curl command with expected status code
- Database: query command with expected output
- Container: docker ps / health check with expected state
- API: request with expected response body
- Config file: validation command with expected output
- General: "You should see..." with specific expected output]
```

All annotated work samples must contain complete, realistic examples — not abstract descriptions. The deficient/exemplar pairs are the core value of this template (Lemov's "work samples instead of rubrics").

- [ ] **Step 2: Commit**

```bash
git add plugins/mad-scientist-skills/skills/documentation-audit/templates/pedagogical-scaffolding.md
git commit -m "feat(documentation-audit): add pedagogical scaffolding template with annotated work samples"
```

---

### Task 10: Create templates/repo-architecture.md

**Files:**
- Create: `plugins/mad-scientist-skills/skills/documentation-audit/templates/repo-architecture.md`

- [ ] **Step 1: Write the repo architecture template**

Write ~100 lines covering:

**Structure:**
```markdown
# Repository Architecture Checklist

## Purpose
Answer: "Does this repository have the documentation infrastructure users and contributors expect?"

## Essential Files
[For each file (README.md, CONTRIBUTING.md, SECURITY.md, CODE_OF_CONDUCT.md, CHANGELOG.md, LICENSE, API docs):
- Required sections (bulleted list)
- Severity if missing
- Common deficiencies to check for
- Template reference (link to Good Docs Project template where applicable)]

## README.md Deep Dive
[Detailed section breakdown:
- Project name + one-line description (not marketing copy)
- Status badges (CI, coverage, version, license — must be current)
- Quick start (< 5 minutes to first success)
- Installation (prerequisites listed, OS-aware, version-pinned)
- Usage examples (runnable, not pseudocode)
- Contributing pointer (link to CONTRIBUTING.md)
- License (named, linked)]

## Anti-Patterns
[Detailed descriptions:
- Monolithic AGENTS.md: what it is, why it's wasteful, what to do instead
- Auto-generated docs without review: what's missing, how to supplement
- External-only docs: why repo needs at least a pointer
- Stale badges: how to detect, how to fix]

## CHANGELOG Format (Keep a Changelog)
[Section categories: Added, Changed, Deprecated, Removed, Fixed, Security
- Each entry: imperative mood, links to PR/issue, version header with date]
```

- [ ] **Step 2: Commit**

```bash
git add plugins/mad-scientist-skills/skills/documentation-audit/templates/repo-architecture.md
git commit -m "feat(documentation-audit): add repository architecture checklist template"
```

---

### Task 11: Create templates/audience-calibration.md

**Files:**
- Create: `plugins/mad-scientist-skills/skills/documentation-audit/templates/audience-calibration.md`

- [ ] **Step 1: Write the audience calibration template**

Write ~130 lines covering:

**Structure:**
```markdown
# Audience Calibration Reference

## Purpose
Answer: "Does this documentation meet readers where they are — not where the author assumes they are?"

## Expert Blind Spot Audit (Hinds 1999)
[Worksheet table: Term/Metric | Domain Expert Can Interpret? | Newcomer Can Interpret? | Both Fail? | Required Fix
- Instructions: for each domain-specific term displayed in the documentation, complete this row
- If either audience cannot interpret, require: tooltip/inline explanation, reference value, or link to glossary
- Terms that fail for BOTH audiences are Critical — opaque to everyone except the author]

## Glossary Completeness Check
[Process:
1. Inventory every unique technical term, abbreviation, and acronym used across all docs
2. Cross-reference against glossary/help system
3. Any term without a glossary entry is a gap
4. An incomplete glossary is itself a blind spot — the author assumed certain terms were obvious]

## Assumed Context Checklist
[Table of assumption categories:
- Operating system (commands assume Unix/Mac — Windows users?)
- Package manager (assumes npm? pip? brew? What if user has none?)
- Runtime version (assumes latest? Specifies minimum?)
- Network access (assumes internet? Proxy? Firewall?)
- Permissions (assumes sudo/admin? What if not?)
- Prior tool installation (assumes Docker/Git/Make installed?)
- Domain knowledge (assumes user knows REST/SQL/k8s concepts?)
- Each "simply/just/obviously" hides one or more of these]

## Information Scent Scoring (Pirolli & Card 1999)
[Per-label scoring table: Navigation Label | Target User Goal | Scent Strength (Strong/Medium/Weak) | Issue
- Strong: user's goal vocabulary matches the label exactly
- Medium: label is related but requires inference
- Weak: implementation/developer vocabulary, abbreviations, jargon without context
- Every top-level navigation label must be scored]

## Expertise Spectrum Design
[Table: Level | Mental Model | Documentation Need | Design Requirement
- Newcomer: no pre-existing model | Self-explanatory, guided, minimal choices | Quick-start, glossary, prerequisites
- Regular: functional model, knows vocabulary | Consistent patterns, predictable navigation | How-to guides, searchable reference
- Expert: compiled methods, wants efficiency | Don't slow them down — shortcuts, density | API reference, advanced guides, configuration reference]

## Safe, Successful, Known (Lemov Principle 5)
[Audit checks:
- Safe: does the doc acknowledge failure points proactively? ("If you see error X, this is why")
- Successful: does the doc provide early wins before tackling complexity?
- Known: does the doc acknowledge different reader profiles? ("If you're coming from Python...", "If you're an ops engineer...")]
```

- [ ] **Step 2: Commit**

```bash
git add plugins/mad-scientist-skills/skills/documentation-audit/templates/audience-calibration.md
git commit -m "feat(documentation-audit): add audience calibration template with blind spot worksheet"
```

---

### Task 12: Create templates/audit-methodology.md

**Files:**
- Create: `plugins/mad-scientist-skills/skills/documentation-audit/templates/audit-methodology.md`

- [ ] **Step 1: Write the audit methodology template**

Write ~180 lines covering:

**Structure:**
```markdown
# Audit Methodology Reference

## Purpose
This template codifies HOW to conduct an effective audit — not what to check (that's in the SKILL.md phases) but how to observe, record, and analyze findings with rigor. Derived from Lemov's instructional techniques (Teach Like a Champion 3.0, 2021), adapted for documentation auditing.

This template is portable — it can be loaded by any audit skill to improve audit execution quality.

## Exemplar Planning (Lemov #1)
[Before auditing any document element, write the ideal version first.
- Why: frees working memory for defect detection (you stop holding "what good looks like" in your head); prevents inattentional blindness (you only see deviations from a standard you've committed to writing)
- How: for each document type being audited, write a 2-3 sentence exemplar of the specific element being assessed. Compare the actual document against the written exemplar, not against an internalized sense of quality
- Practical: write exemplars for the 2-3 most critical document types before starting. Don't exemplar every document — bounded scope (Lemov's recommendation: 1-2 per session)]

## Plan for Error (Lemov #2)
[Before starting an audit pass, predict the 3-5 most likely documentation defects.
- Why: predicted errors get detected and acted on; unpredicted errors get "buried" (the auditor sees them but doesn't act because the corrective response hasn't been pre-planned)
- How: write if/then contingencies: "If I find [error type], I will [corrective action]"
- Track error frequency as a histogram (tick marks against a pre-planned list) rather than as a narrative list — this reveals patterns faster
- The expert-novice gap (Chi, Glaser & Feltovich): auditors categorize defects by surface features ("typo", "missing section") when the deep structure matters ("expert blind spot", "quadrant pollution"). Planning for errors by framework category rather than surface category improves diagnostic accuracy]

## Standardize the Format (Lemov #8)
[Design audit instruments so the auditor always looks in the same place for the same data.
- Why: observation is data collection — inconsistent formats consume working memory on search rather than analysis
- How: use structured audit worksheets with fixed positions for each assessment criterion. When reviewing multiple documents, use the same template for each so findings are comparable
- The Lemov insight: "The more consistent the appearance and placement of the data, the more you will be able to focus on what it's telling you"]

## Active Observation (Lemov #9)
[Conduct sequential passes with a single focus per pass.
- Three options per pass:
  1. Immediate feedback: fix issues as you find them (good for Critical/High findings)
  2. Deferred analysis: complete the full observation pass, then analyze patterns (good for systemic issues)
  3. Targeted deep attention: focus on specific documents or sections only (good for complex content)
- Why single-focus passes: working memory cannot effectively evaluate linguistic precision, structural taxonomy, pedagogical scaffolding, and consistency simultaneously. Each pass reduces to one question
- Written tracking: "Working memory is small; even the slightest distractions cause us to forget. In an environment as complex as a codebase there's really no such thing as taking mental notes" (Lemov)
- Error tracking as histogram: track the NATURE of errors via tick marks against a pre-planned list. By the time you finish a pass, you have a frequency distribution of where understanding broke down]

## Everybody Writes / Formative Before Summative (Lemov #38)
[Explore what MIGHT be unclear before judging whether documentation MEETS the standard.
- Formative questions (exploratory): "What might a developer misunderstand here?" / "What questions does this doc leave unanswered?"
- Summative questions (judgmental): "Does this document meet the completeness standard?"
- Why formative first: formative exploration produces more useful findings than binary pass/fail. The "might" framing lowers stakes and opens analytical thinking
- Practical: before filling in the audit checklist (summative), read the document with a formative lens — take notes on what MIGHT be confusing, missing, or misleading. Then use those notes to inform the checklist assessment]

## Stretch It / Follow-Up Questions (Lemov #17)
[When reviewing findings with documentation authors, use the six-category taxonomy:
1. Ask how or why: "Why did you choose this approach over X?"
2. Ask for another way: "Can you explain this for a reader who doesn't know the domain?"
3. Ask for a better word: "Is 'process' the right term, or is this specifically a thread, goroutine, daemon?"
4. Ask for evidence: "What would go wrong if someone skipped step 4?"
5. Ask to integrate: "How does this relate to the error handling in the adjacent section?"
6. Apply in a new setting: "Does this still hold in a multi-region deployment?"

Directedness spectrum: nondirective ("say more") → semi-directive ("tell me more about the failure case") → fully directive ("explain what happens when the connection pool is exhausted")]

## Exit Ticket / Session Boundaries (Lemov #26)
[Define what the audit session should answer BEFORE starting.
- The Snodgrass inversion: write the "exit ticket" first — what specific questions should you be able to answer after this audit pass?
- Three-pile sort at session end: categorize each finding as Clear Pass / Needs Revision / Critical Defect. The Critical Defect pile is the first thing you address next session or communicate to the author
- Performance vs. learning caveat: a document that passes an audit does not mean users will successfully execute the procedures. User testing (equivalent to spaced retrieval practice) is the only way to confirm actual usability]
```

This template must be self-contained enough that another audit skill (security-audit, optimization-audit, etc.) could `Load templates/audit-methodology.md` and apply the methodology without needing the documentation-audit context.

- [ ] **Step 2: Commit**

```bash
git add plugins/mad-scientist-skills/skills/documentation-audit/templates/audit-methodology.md
git commit -m "feat(documentation-audit): add portable audit methodology template (Lemov techniques)"
```

---

### Task 13: Update plugin.json and final commit

**Files:**
- Modify: `plugins/mad-scientist-skills/.claude-plugin/plugin.json`

- [ ] **Step 1: Update plugin.json**

Read the current plugin.json. Update two fields:
- `version`: bump from `"1.10.0"` to `"1.11.0"`
- `description`: append to the existing description string: `, documentation auditing (Diataxis structural taxonomy, Strunk & White linguistic precision, Google/Microsoft style guide compliance, Cognitive Load Theory pedagogical scaffolding, Carroll's Minimalism, Lemov instructional techniques, information foraging, audience calibration, content freshness)`

Do NOT modify any other fields (name, author).

- [ ] **Step 2: Commit**

```bash
git add plugins/mad-scientist-skills/.claude-plugin/plugin.json
git commit -m "feat(documentation-audit): register skill in plugin.json, bump to v1.11.0"
```

---

### Task 14: Final review and validation

**Files:**
- All files created in Tasks 1-13

- [ ] **Step 1: Verify file structure**

```bash
find plugins/mad-scientist-skills/skills/documentation-audit -type f | sort
```

Expected output:
```
plugins/mad-scientist-skills/skills/documentation-audit/SKILL.md
plugins/mad-scientist-skills/skills/documentation-audit/templates/audience-calibration.md
plugins/mad-scientist-skills/skills/documentation-audit/templates/audit-methodology.md
plugins/mad-scientist-skills/skills/documentation-audit/templates/diataxis-checklist.md
plugins/mad-scientist-skills/skills/documentation-audit/templates/linguistic-rules.md
plugins/mad-scientist-skills/skills/documentation-audit/templates/pedagogical-scaffolding.md
plugins/mad-scientist-skills/skills/documentation-audit/templates/repo-architecture.md
```

- [ ] **Step 2: Verify SKILL.md structure**

Check that SKILL.md contains all required sections in order:
1. Frontmatter with name and description
2. Introduction with modes, single tier, core question
3. Academic foundations (7 threads)
4. Key references
5. When to use
6. Mode detection table
7. Severity classification table
8. Audit process header with phase order
9. Phases 0-9 (each with checks, outputs, framework attributions)
10. Important rules (12 items)

```bash
grep -n "^### Phase\|^## " plugins/mad-scientist-skills/skills/documentation-audit/SKILL.md
```

- [ ] **Step 3: Verify cross-references**

Check that every `Load templates/X.md` reference in SKILL.md has a corresponding file:

```bash
grep "Load \`templates/" plugins/mad-scientist-skills/skills/documentation-audit/SKILL.md
```

Each referenced template must exist in the templates/ directory.

- [ ] **Step 4: Verify plugin.json**

```bash
cat plugins/mad-scientist-skills/.claude-plugin/plugin.json
```

Confirm version is `"1.11.0"` and description includes `documentation auditing`.

- [ ] **Step 5: Run the documentation-audit skill against this repo as a smoke test**

Invoke the skill by asking: "Run a documentation audit on this repository"

Verify that:
- The skill is discoverable (appears in skill list)
- Phase 0 produces grep-based findings
- Phase 1 discovers the repo's documentation files
- The report format matches the template in Phase 9

This is a manual validation step — there are no automated tests for skill plugins.

- [ ] **Step 6: Final commit if any fixes were needed**

```bash
git add plugins/mad-scientist-skills/skills/documentation-audit/SKILL.md plugins/mad-scientist-skills/skills/documentation-audit/templates/
git commit -m "fix(documentation-audit): address review findings from smoke test"
```
