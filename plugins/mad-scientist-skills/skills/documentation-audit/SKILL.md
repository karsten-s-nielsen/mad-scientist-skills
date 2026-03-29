---
name: documentation-audit
description: Comprehensive documentation audit with two modes and a single tier. Planning mode designs documentation strategy, content type maps, learning paths, and scaffolding architecture. Audit mode evaluates linguistic precision (Strunk & White, Google/Microsoft style guides), structural taxonomy (Diataxis quadrant classification, Good Docs Project), pedagogical scaffolding (Carroll's Minimalism, Cognitive Load Theory, Merrill's First Principles, Lemov techniques), cross-document consistency, repository architecture (README, CONTRIBUTING, CHANGELOG, API docs), audience calibration (expert blind spot, information scent), and content freshness. Single tier — documentation evaluation tools are methodology-based, not software-licensed. Grounded in classical composition (Strunk & White), enterprise style standards (Google, Microsoft), Diataxis framework (Procida), Cognitive Load Theory (Sweller, Chandler & Sweller), minimalist instruction (Carroll), first principles of instruction (Merrill), teaching techniques (Lemov), and information foraging (Pirolli & Card). Use when asked to "doc audit", "documentation review", "docs review", "check the docs", "documentation quality", "doc quality check", "review documentation", "plan the docs", "documentation strategy", or "what docs do we need".
---

# Documentation Audit

A comprehensive documentation audit with two modes and a single tier:

**Modes:**
- **Planning** (before docs exist) — documentation strategy design, content type mapping, learning path architecture, scaffolding strategy
- **Audit** (on existing docs) — linguistic precision, structural taxonomy, pedagogical effectiveness, consistency, repository architecture, audience calibration, completeness and freshness

**Single tier:** Unlike security auditing, documentation evaluation is methodology-based (style guide application, framework classification, cognitive load analysis), not tool-licensed. Vale, markdownlint, and the analytical frameworks are all free/open-source. The value is in the analytical framework, not the scanner.

**Core question:** "Does this documentation teach effectively?"

## Academic foundations

This skill synthesizes seven research threads into a single audit methodology:

1. **Classical Composition** (Strunk & White 1918/1959) — Omit needless words, active voice, positive form, specific/concrete language, parallel construction. The foundational linguistic layer beneath all documentation quality.

2. **Enterprise Style Standards** (Google Developer Documentation Style Guide; Microsoft Writing Style Guide) — Second person, conditions before instructions, timeless language, inclusive terminology, global accessibility. The enforceable ruleset layer with Vale automation support.

3. **Structural Taxonomy** (Procida, Diataxis Framework 2017+; augmented by Good Docs Project) — Four epistemic quadrants (Tutorial, How-To, Reference, Explanation) based on study vs. work and practical vs. theoretical axes. Quadrant pollution detection. Augmented with Good Docs Project templates for changelogs, READMEs, ADRs, troubleshooting, and migration guides.

4. **Cognitive Load Theory** (Sweller 1988; Chandler & Sweller 1992; Willingham 2009) — Intrinsic/extraneous/germane load taxonomy. Split-attention effect: code samples separated from their explanations force readers to cross-reference, consuming working memory. Guidance fading effect: novices need explicit scaffolding; discovery-style documentation actively harms new users. Forgetting curve (Ebbinghaus 1885): documentation must support elaborative retrieval, not just initial comprehension.

5. **Minimalism & Instructional Design** (Carroll 1990; Merrill 2002; Gagné 1965) — Carroll's four minimalist principles for software instruction: immediate meaningful tasks, minimize passive instruction, support error recognition/recovery, self-contained modules. Merrill's five first principles: task-centered, activation, demonstration, application, integration.

6. **Instructional Techniques** (Lemov, *Teach Like a Champion 3.0*, 2021) — Ten techniques applied at two levels. Content quality heuristics: Take the Steps/guidance fading (#21), Knowledge Organizers/front-loaded prerequisites (#5), Retrieval Practice/elaborative recall (#7), Right Is Right/precision over approximation (#16), Begin with the End/measurable objectives (4 Ms). Audit methodology: Exemplar Planning/write the ideal before auditing (#1), Plan for Error/pre-plan error hypotheses (#2), Active Observation/sequential focused passes (#9), Everybody Writes/formative before summative (#38), Exit Ticket/define session outcomes before starting (#26), Standardize the Format/consistent observation instruments (#8), Stretch It/six-category follow-up questions (#17).

7. **Information Foraging** (Pirolli & Card 1999) — Users follow "information scent" — cues that predict whether a navigation path leads to their goal. Weak scent (ambiguous labels, implementation-oriented vocabulary) causes users to choose wrong paths or abandon the documentation. Applied to navigation labels, cross-document linking, and search discoverability.

**Key references:**
- Strunk & White, *The Elements of Style* (1918; 4th ed. 1999)
- Google Developer Documentation Style Guide (developers.google.com/style)
- Microsoft Writing Style Guide (learn.microsoft.com/style-guide)
- Procida, *Diataxis* (diataxis.fr)
- Wayne, "My Problem With the Four-Document Model" (2023) — Diataxis critique
- Good Docs Project (thegooddocsproject.dev) — templates for non-Diataxis types
- Sweller, "Cognitive Load During Problem Solving" (*Cognitive Science*, 1988)
- Chandler & Sweller, "The Split-Attention Effect" (*Journal of Experimental Psychology*, 1992)
- Carroll, *The Nurnberg Funnel* (MIT Press, 1990)
- Merrill, "First Principles of Instruction" (*ETR&D*, 2002)
- Gagné, *The Conditions of Learning* (1965)
- Lemov, *Teach Like a Champion 3.0* (Jossey-Bass, 2021)
- Lemov, *The Coach's Guide to Teaching* (John Catt, 2020)
- Pirolli & Card, "Information Foraging" (*Psychological Review*, 1999)
- Willingham, *Why Don't Students Like School?* (2009)
- Wolf, *Reader, Come Home* (2018) — attention crisis / neuroplastic skimming
- Ebbinghaus, *Über das Gedächtnis* (1885) — forgetting curve
- Nuthall, *The Hidden Lives of Learners* (2007) — 3-encounter learning threshold
- Brown, Roediger & McDaniel, *Make It Stick* (2014) — retrieval practice
- Leroy, "Why Is It So Hard to Do My Work?" (*Human Factors*, 2009) — attention residue
- Hinds, "The Curse of Expertise" (*Journal of Experimental Psychology: Applied*, 1999) — expert blind spot
- Chi, Glaser & Feltovich, "Categorization and Representation of Physics Problems" (*Cognitive Science*, 1981)

## When to use this skill

- When the user says "doc audit", "documentation review", "docs review", "check the docs", "documentation quality", "doc quality check", "review documentation", "plan the docs", "documentation strategy", or "what docs do we need"
- Before writing documentation for a new project (planning mode) — to design content type maps, learning paths, and scaffolding strategy
- On existing documentation (audit mode) — to find linguistic imprecision, structural pollution, pedagogical gaps, and consistency violations
- Before shipping a new version, API, or user-facing feature with documentation
- After user complaints about confusion, inability to complete tasks from docs, or onboarding friction
- When documentation exists but feels "off" — users still ask questions the docs should answer

## Mode detection

Determine which mode to operate in based on the project state:

| Signal | Mode | Rationale |
|--------|------|-----------|
| User says "plan the docs", "documentation strategy", "what docs do we need" | **Planning** | Design documentation architecture before writing |
| User says "audit the docs", "review documentation", "check doc quality" | **Audit** | Evaluate existing documentation |
| No documentation exists yet | **Planning** | Nothing to audit — design the strategy |
| Documentation files exist | **Audit** | Concrete artifacts to evaluate |
| Docs exist + "redesign the doc structure" | **Both** | Audit current state, plan improvements |

When in doubt, ask the user. If both modes apply, run all 10 phases.

## Severity classification

Every finding must be assigned a severity based on documentation impact:

| Severity | Criteria | Action | SLA |
|----------|----------|--------|-----|
| **Critical** | Documentation is actively misleading — procedures that cause data loss, security instructions that create vulnerabilities, wrong API signatures that produce silent failures. Missing docs for critical safety/security paths | Fix immediately | Block release |
| **High** | Users cannot complete core tasks from the docs alone. Major quadrant pollution. Missing prerequisites causing predictable failures. Systematic passive voice obscuring the responsible agent. No verification commands on destructive operations | Fix before next release | 1 sprint |
| **Medium** | Users succeed but with unnecessary friction. Style guide violations, inconsistent formatting, missing cross-references, suboptimal chunking, vague abstractions, incomplete worked examples | Schedule fix | 2 sprints |
| **Low** | Best practice deviation, minor polish. Sentence length, minor vocabulary inconsistency, missing alt text on decorative images, optional metadata | Track in backlog | Best effort |

## Audit process

Execute all applicable phases in order. Skip phases marked for a mode you are not running. Do NOT skip applicable phases. Do NOT claim completion without evidence.

**Phase order:** 0 → 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8 → 9

---

### Phase 0: Anti-Pattern Scan (Audit mode)

Fast grep-based scan for common documentation anti-patterns. Runs first to catch obvious issues before deeper analysis. Each match requires manual review — some patterns are intentional in specific contexts.

**Scope:** Phase 0 scans **user-facing documentation only**. Internal development docs (files under `docs/plans/`, `docs/specs/`, `docs/decisions/`, ADRs) are exempt from style checks — they serve the development team, not end users. Still scan internal docs for structural anti-patterns (missing verification commands, walls of text) but not for linguistic style (trivializing language, passive voice).

#### Linguistic anti-patterns

| Pattern | Issue | Severity |
|---------|-------|----------|
| Passive voice: "was performed", "is configured by", "are managed by", "was created", "is included", "is retained", "are assigned", "is handled by", "is maintained" | Obscures the agent — reader cannot determine who/what performs the action (Strunk & White Rule 10). **Note:** These grep patterns are a sample, not comprehensive. For full passive voice detection, use Vale with the Google or Microsoft style package | Medium |
| "in order to", "the fact that", "due to the fact that", "it should be noted that", "in a [adj] manner" | Needless words — padding that slows comprehension (Strunk & White Rule 13) | Medium |
| "currently", "recently", "now", "new in version X", "will soon", "latest" | Temporal language that decays — docs should describe the product as-is (Google Style Guide: timeless language) | Medium |
| "whitelist", "blacklist", "master/slave", "sanity check", "dummy value" | Non-inclusive language (Google/Microsoft inclusive language guidelines) | High |
| "click here", bare URLs as link text, "see above", "as mentioned" | Inaccessible link text / directional language that fails for screen readers and reflow (Google Style Guide; WCAG) | High |
| "simply", "just", "obviously", "easily", "of course" | Implicit assumptions — each hides an unstated prerequisite or trivializes difficulty (Carroll's Minimalism — support error recognition) | Medium |

#### Structural anti-patterns

| Pattern | Issue | Severity |
|---------|-------|----------|
| Code blocks in files named/structured as conceptual or explanatory docs (e.g., `architecture.md`, `concepts/`, `explanation/`) | Executable code in explanation = likely quadrant pollution (Diataxis) — confirm in Phase 2 | Medium |
| Step-by-step numbered procedures in files named/structured as reference docs (e.g., `api/`, `reference/`, `config-reference.md`) | Procedural content in reference = likely quadrant pollution (Diataxis) — confirm in Phase 2 | Medium |
| Paragraph-length text with no heading for >500 words | Wall of text — exceeds working memory capacity without structural aids (Sweller — extraneous load) | Medium |
| API/CLI/config reference sections containing "why" or "background" discussions | Explanatory content in reference = likely quadrant pollution (Diataxis) — confirm in Phase 2 | Medium |
| Tutorial/guide with no verification step after complex configuration | Missing "Check for Understanding" — reader has no way to confirm success (Lemov #7; Carroll — error recognition) | High |
| `<img` without `alt=` | Missing alt text — accessibility violation (WCAG 1.1.1) | High |

#### Grep patterns for anti-pattern detection

| Pattern | What it catches |
|---------|-----------------|
| `in order to`, `the fact that`, `due to the fact that`, `it should be noted that` | Needless word padding (Strunk & White Rule 13) |
| `simply`, `just`, `obviously`, `easily`, `of course` | Trivializing language that hides prerequisites (Carroll) |
| `currently`, `recently`, `will soon`, `new in version`, `latest` | Temporal language that decays (Google Style Guide) |
| `whitelist`, `blacklist`, `master/slave`, `sanity check`, `dummy` | Non-inclusive terminology (Google/Microsoft) |
| `click here`, `see above`, `as mentioned` | Directional/inaccessible link text (WCAG) |
| `was performed`, `is configured by`, `are managed by`, `was created`, `is included`, `is retained`, `are assigned` | Passive voice obscuring the agent — sample patterns, not comprehensive (Strunk & White Rule 10) |
| Numbered steps in files under `reference/`, `api/`, or named `*-reference.md` | Procedural content in reference (Diataxis pollution) |
| Code blocks in files under `concepts/`, `explanation/`, or named `architecture.md` | Executable code in explanation (Diataxis pollution) |
| `<img` without `alt=` | Missing alt text (WCAG 1.1.1) |

For each finding: record file path, line number, pattern matched, severity, and the framework that identifies the violation.

**Output:** Anti-pattern findings table with file paths, severity, and framework attribution.

---

### Phase 1: Discovery (Both modes)

Explore the project to understand its documentation surface:

- Read `CLAUDE.md`, `README.md`, `CONTRIBUTING.md`, and any documentation config (mkdocs.yml, docusaurus.config.js, conf.py, etc.)
- Inventory all documentation files by type (md, rst, adoc, ipynb, inline docstrings)
- Identify the documentation tech stack (Sphinx, MkDocs, Docusaurus, plain markdown, etc.)
- Map **audiences**: who reads these docs? (first-time user, regular developer, contributor, operator/admin)
- Identify **core user tasks**: the 3-5 things readers primarily come to the docs to do
- Assess **documentation maturity**: none → minimal (README only) → partial (some guides) → comprehensive (structured doc set)
- Catalog the **constraint landscape**: what determines scope (API surface, feature count, audience breadth, team size)
- Note **documentation conventions** already in use (admonition styles, code annotation patterns, section templates)
- Check for existing style guide or documentation standards (Vale config, markdownlint config, custom rules)
- Identify **multiple surfaces**: does the project have docs in multiple locations (repo, hosted site, wiki, HF Hub, npm/PyPI page)?
- Classify each document as **user-facing** or **internal**: user-facing docs (README, tutorials, guides, API reference) are subject to all audit phases; internal docs (implementation plans, design specs, ADRs, meeting notes) are exempt from linguistic style checks (Phases 0 and 3) but are still checked for freshness (Phase 8) and structural consistency (Phase 5)

#### Documentation file inventory guide

Systematically catalog all documentation artifacts:

| File Type | Where to Find | What to Note |
|-----------|---------------|-------------|
| **Markdown** (`.md`) | Repo root, `docs/`, `wiki/`, `.github/` | Primary documentation format for most projects |
| **reStructuredText** (`.rst`) | `docs/`, `source/` | Common in Python projects using Sphinx |
| **AsciiDoc** (`.adoc`) | `docs/` | Used in some enterprise projects |
| **Jupyter notebooks** (`.ipynb`) | Repo root, `notebooks/`, `examples/` | Executable documentation — verify code cells still run |
| **Inline docstrings** | Source code files | API documentation extracted by generators |
| **OpenAPI/Swagger** (`.yaml`, `.json`) | `api/`, repo root | API specification — check if published and current |
| **Configuration comments** | Config files (`.env.example`, `config.yaml`) | Often the only documentation for configuration options |
| **Hosted docs** | External URLs referenced in README | Check for bidirectional linking with repo |

#### Documentation maturity levels

| Level | Characteristics | Typical Indicators | Risk Profile |
|-------|----------------|-------------------|--------------|
| **None** | No documentation exists | No README, no inline docs, no comments beyond boilerplate | Critical — users have zero entry point |
| **Minimal** | README only, possibly auto-generated | Single README with project name and basic description; no installation steps, no usage examples | High — users can discover but not use the project |
| **Partial** | Some guides, incomplete coverage | README + a few how-tos or a tutorial; API partially documented; gaps in coverage | Medium — users succeed on documented paths, fail on undocumented ones |
| **Comprehensive** | Structured doc set with multiple types | Diataxis-aligned content types; consistent style; cross-references; maintained changelog | Low — maintenance and freshness are the primary risks |

#### Audience spectrum

Every documentation set serves readers across a spectrum. The audit must evaluate fit at each level:

| Level | Mental Model | Reading Behavior | Documentation Requirement |
|-------|-------------|-----------------|--------------------------|
| **First-time user** | No pre-existing model. Learning the project's vocabulary and purpose | Scans README, follows tutorial if one exists, gives up quickly if blocked | Self-explanatory entry point, guided quick start, minimal jargon |
| **Regular developer** | Functional model. Knows the API, seeks specific answers | Goes directly to reference or how-to guides, uses search | Consistent structure, accurate reference, good information scent |
| **Contributor** | Expert model. Understands internals, wants to change the codebase | Reads CONTRIBUTING, architecture docs, ADRs, reviews CI/CD setup | Dev environment setup, coding standards, PR process, design rationale |
| **Operator/Admin** | Operational model. Deploys, configures, monitors | Seeks deployment guides, configuration reference, troubleshooting | Runbooks, config reference, monitoring setup, upgrade procedures |

**Output:** Documentation surface summary listing all files, audiences, core tasks, maturity level, and identified risk areas.

---

### Phase 2: Diataxis Classification (Both modes)

Load `templates/diataxis-checklist.md` for the full quadrant classification guide, pollution detection patterns, and Good Docs Project extensions.

**Planning mode:** Design the content type map:
- Which documents should be tutorials (learning-oriented, guided)?
- Which should be how-tos (task-oriented, assume competence)?
- Which should be reference (information-oriented, austere, authoritative)?
- Which should be explanation (understanding-oriented, discursive, connects concepts)?
- What document types are needed that don't fit the four quadrants (changelogs, READMEs, ADRs, troubleshooting, migration guides)?

#### Diataxis quadrant summary

| Quadrant | Orientation | Reader Mode | Key Characteristic | Pollution Signal |
|----------|-------------|-------------|-------------------|------------------|
| **Tutorial** | Learning-oriented | Study | Guarantees a successful outcome through guided steps | Reference tables, exhaustive options, architectural digressions |
| **How-To** | Task-oriented | Work | Assumes competence; solves a specific problem | Foundational teaching, conceptual explanations, "why" discussions |
| **Reference** | Information-oriented | Work | Austere, factual, authoritative; mirrors the product architecture | Instructional language, opinions, narrative, step-by-step procedures |
| **Explanation** | Understanding-oriented | Study | Discursive; addresses "why" not "how"; connects concepts | Procedural steps, executable code, numbered instructions |

#### Non-quadrant types (Good Docs Project)

Not all documentation fits the Diataxis quadrants. The Good Docs Project provides templates for:

| Type | Purpose | When Needed |
|------|---------|-------------|
| **README** | Project entry point — first impression, quick orientation | Every project |
| **Changelog** | Versioned history of changes (Added, Changed, Deprecated, Removed, Fixed, Security) | Any versioned project |
| **ADR (Architecture Decision Record)** | Records the "why" behind significant technical decisions | Projects with non-obvious architectural choices |
| **Troubleshooting guide** | Problem-solution pairs for common failure modes | Any project with user-reported issues |
| **Migration guide** | Step-by-step upgrade between versions with breaking changes | Any project with breaking version changes |

**Audit mode:** Classify and evaluate each existing document.

**Important:** READMEs, CHANGELOGs, ADRs, troubleshooting guides, and migration guides are **non-quadrant types** (Good Docs Project). Do NOT classify them into a Diataxis quadrant or flag them for "quadrant pollution." Evaluate them against their Good Docs Project template instead. A README that contains tutorial steps, reference tables, and explanatory context is doing its job as a gateway document — not polluting quadrants.

| Check | What to look for | Severity if violated |
|-------|-----------------|---------------------|
| Quadrant identity | Can the document be classified into exactly one Diataxis quadrant? (Skip for non-quadrant types — READMEs, CHANGELOGs, ADRs, etc.) | High (if unclassifiable) |
| Tutorial contract | Tutorials guarantee a successful learning outcome. Does this one? Does it reach a working result? | High |
| Tutorial pollution | Does the tutorial contain reference tables, exhaustive option lists, or architectural digressions? | High |
| How-to title | Does the title state the task explicitly (preferably "How to...")? Vague noun titles = weak scent | Medium |
| How-to focus | Does the how-to contain foundational teaching or conceptual explanations? | Medium |
| Reference austerity | Is reference content purely factual — no instructional language, no opinions, no narrative? | Medium |
| Reference structure | Does reference structure mirror the product/API architecture? | Medium |
| Explanation scope | Does explanation content address "why" not "how"? No procedural steps, no executable code? | Medium |
| Missing types | Are any of the four quadrants completely absent from the doc set? | High |
| Non-quadrant types | Are changelogs, READMEs, troubleshooting, ADRs needed but missing? | Medium |
| Separation strategy | Does mixing types cause navigation fragmentation, or is mixing intentional and well-managed? | Medium |

#### Pollution detection patterns

Quadrant pollution is the most common Diataxis violation. These patterns identify likely pollution for confirmation:

| In This Quadrant | This Content Is Pollution | Why It Harms |
|-----------------|--------------------------|-------------|
| **Tutorial** | Complete API reference table | Overwhelms the learner with options they don't need yet (Sweller — extraneous load) |
| **Tutorial** | Architectural explanation of how the system works internally | Breaks the learning flow — reader must context-switch from "doing" to "understanding" |
| **How-to** | Step-by-step foundational teaching ("First, let's understand what X means...") | Reader came to solve a problem, not to learn — wastes time for competent users |
| **How-to** | Exhaustive list of all options when only one is needed for the task | Option overload — reader must evaluate irrelevant alternatives (Hick's Law) |
| **Reference** | Opinions ("We recommend using X") or narrative ("This was designed because...") | Violates reference austerity — reader expects facts, not guidance |
| **Reference** | Numbered procedural steps | Reader expects lookup, not instruction — wrong reading mode |
| **Explanation** | `pip install`, `docker run`, or any executable command | Reader is in study mode, not work mode — executable code implies action |
| **Explanation** | Step-by-step numbered instructions | Procedural content belongs in tutorials or how-tos |

**Output:** Classification table mapping each document to its quadrant, with pollution findings and missing type gaps.

---

### Phase 3: Linguistic Precision (Audit mode)

Load `templates/linguistic-rules.md` for the full Strunk & White, Google, and Microsoft rule reference with grep patterns and permitted exceptions.

**Scope:** Phase 3 applies to **user-facing documentation only** (as classified in Phase 1). Internal docs (plans, specs, ADRs) are exempt — they serve the development team and applying user-facing style rules to them produces false positives.

**Automation note:** Many linguistic checks can be automated with [Vale](https://vale.sh/) using the Google or Microsoft style packages. If a `.vale.ini` exists in the repo, run Vale first and triage its output before manual review. If no Vale config exists, recommend adding one as a Phase 9 finding.

| Check | Rule Source | Severity |
|-------|-----------|----------|
| Active voice enforcement (with exceptions: emphasizing object, actor irrelevant, avoiding blame) | Strunk & White Rule 10 | Medium |
| Needless word patterns: "the fact that", "in order to", "He/it is [noun] who/that", "used for [noun] purposes" | Strunk & White Rule 13 | Medium |
| Positive form: "not" where direct antonym exists; hedges: "not very", "not often" | Strunk & White Rule 11 | Medium |
| Specific/concrete language: flag "various", "several", "aspects", "issues", "things" without referents | Strunk & White Rule 12 | Medium |
| Parallel construction in lists: mixed gerunds, infinitives, and noun phrases | Strunk & White Rule 15 | Medium |
| Conditions before instructions: "Run X if Y" → "If Y, run X" | Google Style Guide | Medium |
| Second person: use "you" for instructions, not "we" or "the user" | Google Style Guide | Low |
| Tense consistency within sections | Strunk & White Rule 17 | Low |
| Sentence length: >26 words flagged for translation accessibility | Google Style Guide | Low |
| Right Is Right (Lemov #16): explanations that "round up" — giving the gist without specifics needed to act | Lemov | High |
| Specific vocabulary: natural-language approximations where precise technical terms exist and would reduce ambiguity | Lemov #16 sub-type 3 | Medium |
| Leaner language: documentation that requires re-reading because structure buries the key fact | Lemov #16 sub-type 4; Strunk & White Rule 13 | Medium |
| Weak sentence endings: "however", "also", "as well", "etc." | Strunk & White Rule 18 | Low |
| Filler nouns: "case", "character", "nature", "factor", "feature" as abstract nouns | Strunk & White Ch. V | Low |
| Dangling modifiers: participial phrase at sentence start not referring to grammatical subject | Strunk & White Rule 7 | Medium |
| Comma splices: two independent clauses joined by only a comma | Strunk & White Rule 5 | Low |

#### Grep patterns for linguistic violations

| Pattern | What it catches |
|---------|-----------------|
| `in order to`, `the fact that`, `due to the fact that` | Needless words (Rule 13) |
| `not un`, `not in`, `not dis` (double negatives) | Positive form violations (Rule 11) |
| `various`, `several`, `aspects`, `issues`, `things` (without referent in same sentence) | Vague abstractions (Rule 12) |
| Lines >120 words with no heading | Wall of text (Sweller — extraneous load) |
| Bulleted lists mixing gerund ("Running..."), infinitive ("To run..."), and noun ("The runner...") starts | Parallel construction violations (Rule 15) |
| `Run X if Y` (instruction before condition) | Conditions-before-instructions violation (Google) |
| `we `, `the user `, `one should` in instructional context | Second person violation (Google) |
| `however.`, `also.`, `as well.`, `etc.` at sentence end | Weak endings (Rule 18) |

#### Sweller's load taxonomy — documentation implications

| Load Type | Source | Documentation Goal |
|-----------|--------|-------------------|
| **Intrinsic** | Inherent concept complexity (domain-determined) | Cannot reduce — but can scaffold with progressive disclosure and worked examples |
| **Extraneous** | Poor writing (documentation-determined) | **Eliminate.** This is the audit's primary target — needless words, split attention, walls of text |
| **Germane** | Productive learning (schema-building) | **Maximize.** Consistent vocabulary, elaborative hooks, and retrieval practice help readers build accurate mental models |

**Output:** Linguistic findings with rule attribution, file paths, and recommended corrections.

---

### Phase 4: Pedagogical Scaffolding (Both modes)

Load `templates/pedagogical-scaffolding.md` for the full Carroll, CLT, Merrill, and Lemov reference with documentation-specific examples and annotated work samples.

**Planning mode:** Design the learning path:
- What prerequisites must readers have before each document?
- What order should documents be read in?
- What scaffolding strategy will be used (progressive disclosure, prerequisites block, guided tutorials)?
- Where should process-oriented worked examples (showing reasoning) be used vs. product-oriented (showing result)?

**Audit mode:**

| Check | Framework | Severity |
|-------|-----------|----------|
| **Begin with the End:** Does each tutorial/guide state a measurable objective? Can the reader know whether they achieved it? | Lemov (4 Ms); Merrill (task-centered) | High |
| **Knowledge Organizers:** Are prerequisites front-loaded at the beginning, not buried? Is there a retrievable reference block (glossary, prerequisites, "what you need to know")? | Lemov #5; CLT | High |
| **Guidance Fading:** Do tutorials scaffold explicitly for novices (step-by-step with verification)? Do advanced docs assume appropriate expertise without over-scaffolding? | Sweller (guidance fading); Lemov #21 | High |
| **Worked examples:** Are examples process-oriented (showing reasoning and decision process) or product-oriented (showing only the final result)? For complex/ill-structured domains, process-oriented is required | CLT (worked example effect) | Medium |
| **Verification commands:** After complex configuration steps, can the reader confirm success? (e.g., `curl`, `ping`, health check, expected output) | Lemov #7 (Check for Understanding); Carroll (error recognition) | High |
| **Cognitive chunking:** Are dense sections broken into manageable pieces? >3 new concepts introduced before any practice? | CLT (intrinsic load management); Sweller | Medium |
| **Split-attention avoidance:** Are code samples annotated inline (comments, adjacent explanation) rather than in separate paragraphs requiring cross-referencing? | Chandler & Sweller 1992 | Medium |
| **Elaborative hooks:** Does the doc connect to adjacent concepts, enabling retrieval beyond rote recall? ("This uses the same pattern as...", "Compare with...", "Why not X?") | Brown, Roediger & McDaniel (elaboration); Lemov #7 | Medium |
| **Attention design:** Given neuroplastic skimming (Wolf 2018), is critical information structurally unavoidable — not just visually prominent but in the procedural path? | Wolf; Leroy (attention residue) | Medium |
| **Immediate meaningful tasks:** Does the doc get the reader doing real work quickly, or does it front-load passive instruction? | Carroll's Minimalism | Medium |
| **Error recovery:** Does the doc anticipate common errors and guide recovery? Are failure modes documented alongside success paths? | Carroll's Minimalism; Lemov #2 (Plan for Error) | High |
| **Application prompts:** Does the doc include prompts for the reader to produce output (code, configuration), not just read? | Merrill (Application principle); Lemov #38 (Everybody Writes) | Medium |
| **Integration:** Does the doc help readers connect new knowledge to their existing practice or to other parts of the system? | Merrill (Integration principle) | Low |

#### Walkthrough test (critical tutorials and quick starts)

For the 1-2 most important procedural documents (typically the Quick Start and any deployment guide), the auditor should **actually execute the documented commands** in a clean environment and verify each step produces the documented result. Reading documentation is insufficient — Carroll's Minimalism principle #3 (error recognition) requires testing the path a reader will follow.

| Step | What to do | What to record |
|------|-----------|----------------|
| 1 | Follow the documented steps exactly as written (no prior knowledge, no shortcuts) | Where you got stuck, where instructions were ambiguous, where output didn't match |
| 2 | Note every unstated prerequisite you needed (tools, accounts, permissions, environment) | Each gap is an assumed context finding (Phase 7) |
| 3 | Note every step where you couldn't verify success (no expected output shown) | Each gap is a verification command finding (this phase) |
| 4 | Note every step where an error occurred that the docs don't address | Each gap is an error recovery finding (this phase) |

If a walkthrough is not feasible (no local environment, external service dependencies), note it as a limitation in the Phase 9 report and recommend the project owner run it.

#### Retrieval support (Ebbinghaus, Nuthall, Brown et al.)

Documentation must support not just initial comprehension but long-term retention. Three research findings are directly applicable:

| Finding | Source | Documentation Implication |
|---------|--------|--------------------------|
| **Forgetting curve** | Ebbinghaus 1885 | Without retrieval cues, readers forget ~70% of new information within 24 hours. Documentation must be findable for re-reading, not just readable the first time |
| **3-encounter threshold** | Nuthall 2007 | Learners need at least 3 encounters with a concept to retain it. Key concepts should appear in tutorial, reference, AND how-to — not just once |
| **Retrieval practice** | Brown, Roediger & McDaniel 2014 | Actively recalling information strengthens memory more than re-reading. Verification commands, "check your understanding" prompts, and application exercises serve as retrieval practice |

#### Reading experience thresholds

Documentation readability directly affects task completion. These thresholds identify when documentation structure creates unnecessary cognitive burden:

| Threshold | Reader Impact | Documentation Requirement |
|-----------|--------------|--------------------------|
| **>3 paragraphs before first action** | Reader disengages — Carroll's "minimize passive instruction" violated | Move background to an explanation doc; start with the task |
| **>5 new terms before any are defined** | Working memory overload — reader cannot hold undefined terms while reading ahead | Define terms inline on first use, or front-load a glossary block |
| **>10 steps without verification** | Reader accumulates uncertainty — no way to know if they're on track | Insert "Check: you should see..." after every 3-5 steps |
| **>500 words without a heading** | Wall of text — reader loses structural orientation | Break into sections with descriptive headings |
| **>3 levels of nested lists** | Visual hierarchy collapses — reader cannot track nesting depth | Flatten or restructure into sub-sections |
| **Code block >30 lines without annotation** | Reader must parse code unaided — split-attention effect (Chandler & Sweller) | Add inline comments or break into annotated segments |

#### Carroll's four minimalist principles

John Carroll's *The Nurnberg Funnel* (1990) established four principles for software instruction that directly apply to documentation quality:

| Principle | Documentation Application | Violation Indicator |
|-----------|--------------------------|---------------------|
| **Immediate meaningful tasks** | Get the reader doing real work in the first section, not reading background | Tutorial begins with 3+ paragraphs of explanation before any action |
| **Minimize passive instruction** | Reduce reading-to-doing ratio; every paragraph should move toward an action | Long conceptual preambles before each step |
| **Support error recognition/recovery** | Anticipate common errors; document failure modes alongside success paths | No "If you see this error..." sections; no troubleshooting |
| **Self-contained modules** | Each document can be read independently without required sequential reading | Doc assumes reader has read previous docs without linking or summarizing |

#### Guidance fading spectrum

Documentation must calibrate scaffolding to the reader's expertise level. Over-scaffolding experts wastes their time; under-scaffolding novices causes failure.

| Document Type | Novice Scaffolding | Expert Scaffolding | Violation |
|--------------|-------------------|-------------------|-----------|
| **Tutorial** | Full: numbered steps, verification after each step, expected output shown | Minimal: link to quick-start, assume tool familiarity | Tutorial without verification = novice failure (Lemov #7) |
| **How-to** | Moderate: prerequisites listed, key decisions explained | Minimal: task title + steps + result | How-to with full teaching = quadrant pollution (Diataxis) |
| **Reference** | Low: glossary links for domain terms | None: austere, factual, authoritative | Reference with narrative = quadrant pollution (Diataxis) |
| **Explanation** | Moderate: connects to practical examples | Low: assumes conceptual vocabulary | Explanation with step-by-step = quadrant pollution (Diataxis) |

#### Merrill's First Principles — documentation diagnostic

| Principle | Audit Check | Missing Indicator |
|-----------|------------|-------------------|
| **Task-centered** | Does the doc organize around a real task, not an abstract concept? | Document title is a noun ("Configuration") not a verb ("How to configure...") |
| **Activation** | Does the doc connect to what the reader already knows? | No "Prerequisites" or "Before you begin" section |
| **Demonstration** | Does the doc show the concept in action, not just describe it? | No code samples, no screenshots, no worked examples |
| **Application** | Does the doc prompt the reader to produce output? | Reader only reads — never types, never verifies, never decides |
| **Integration** | Does the doc connect to the broader system or the reader's practice? | No "See also", no "Next steps", no cross-references |

**Output:** Pedagogical scaffolding assessment with framework attribution, gap analysis, and recommended fixes.

---

### Phase 5: Structural Consistency (Audit mode)

Cross-document consistency checks:

| Check | What to look for | Severity |
|-------|-----------------|----------|
| Vocabulary alignment | Same concept uses same term everywhere — not "workspace" in one doc and "project" in another | High |
| Action vocabulary | Same operation uses same label (not "install" in one doc, "set up" in another, "deploy" in a third) | High |
| Heading hierarchy | Consistent heading levels across similar documents (H1 for page title, H2 for sections, H3 for subsections) | Medium |
| Formatting patterns | Admonitions, callout boxes, code annotations used consistently | Medium |
| Template adherence | Do similar document types follow the same structural template? | Medium |
| Code block formatting | Consistent language tags, consistent use of highlighting/annotations | Low |
| Link format consistency | Relative vs absolute, trailing slashes, anchor style | Low |
| Date/version format | Consistent date formats (ISO 8601 preferred), version references | Low |
| Tone/register consistency | No mixing informal ("basically it just does X") and formal ("implements the observer pattern") across related docs | Medium |
| Partial pattern application | If a UX/doc pattern (cross-references, admonitions, code annotations) appears in some docs but not all equivalent docs, flag as inconsistency | High |
| Empty states | "Coming soon" / placeholder / stub pages without content — either write them or remove them | Medium |

#### Tone/register spectrum

Documentation should maintain a consistent register within each document type:

| Document Type | Expected Register | Violation Example |
|--------------|-------------------|-------------------|
| **Tutorial** | Conversational but precise — guides the reader step by step | Formal academic prose in a tutorial; casual slang in a tutorial |
| **How-to** | Direct and professional — assumes competence, minimal explanation | Over-explaining basics to experienced readers |
| **Reference** | Austere and factual — no opinions, no narrative, no filler | "This awesome feature lets you..." in API docs |
| **Explanation** | Discursive and thoughtful — explores "why", connects ideas | Bullet-point lists without connecting prose |
| **README** | Welcoming but efficient — first impression, scannable | Dense technical jargon in the opening paragraph |

#### Grep patterns for consistency violations

| Pattern | What it catches |
|---------|-----------------|
| Multiple distinct admonition styles across docs (`> **Note:**`, `> [!NOTE]`, `:::note`, `!!! note`) | Admonition format inconsistency |
| Varying heading level patterns for equivalent document types | Heading hierarchy drift |
| Mix of relative (`./guide.md`) and absolute (`https://...`) internal links | Link format inconsistency |
| Different code block language tags for the same language (`bash` vs `shell` vs `sh`) | Code block formatting inconsistency |
| Inconsistent date formats across docs (MM/DD/YYYY, YYYY-MM-DD, "March 2024") | Date format inconsistency |
| Same concept with different names across files (e.g., "workspace" vs "project" vs "environment") | Vocabulary alignment failure |

**Output:** Consistency findings table with pattern, locations, and recommended standard.

---

### Phase 6: Repository Architecture (Audit mode)

Load `templates/repo-architecture.md` for the full essential file checklist with required sections per file.

Evaluate the repository's documentation infrastructure — not just content, but the structural files that enable discoverability, contribution, and trust.

| File | Required Sections | Severity if Missing |
|------|------------------|---------------------|
| **README.md** | Project name, description, status badges, quick start, installation, prerequisites, usage examples, license | Critical (if missing entirely); High (if incomplete) |
| **CONTRIBUTING.md** | Dev environment setup, coding standards, commit conventions, test requirements, PR process, code review expectations | Medium |
| **SECURITY.md** | Vulnerability disclosure policy, supported versions, reporting process | High (for public repos) |
| **CODE_OF_CONDUCT.md** | Community standards | Low |
| **CHANGELOG.md** / release notes | Versioned change history with categories (Added, Changed, Deprecated, Removed, Fixed, Security) | Medium |
| **LICENSE** | Present and correctly identified | High |
| **API documentation** | Coverage relative to public API surface (every public endpoint, function, class documented) | High |

#### Inline documentation coverage (Python, TypeScript, Java)

For codebases with a public API, estimate docstring/JSDoc coverage of public functions:

```bash
# Python: compare public function count to docstring count
grep -r "def [a-z]" src/ --include="*.py" | grep -v "def _" | wc -l    # public functions
grep -r '"""' src/ --include="*.py" | wc -l                              # docstrings (rough)
```

The ratio gives a rough coverage estimate. Flag if <50% of public functions have docstrings. Do NOT flag private/internal functions (prefixed with `_`) — only public API surface matters.

#### Anti-patterns

| Pattern | Issue | Severity |
|---------|-------|----------|
| Monolithic AGENTS.md/CLAUDE.md that merely restates directory structure or obvious tech stack | Token waste — duplicates discoverable information (>20% token cost inflation) | Medium |
| Auto-generated docs committed without review (default Swagger UI, typedoc defaults) | False sense of completeness — generated docs often lack context, examples, and error documentation | Medium |
| Documentation in wiki/external system with no repo-level pointer | Discoverable documentation only by those who know where to look | High |
| Outdated badges (broken CI badge, wrong version, dead links) | Misleading project status signals | Medium |

#### README quality rubric

The README is the documentation entry point — it forms the reader's first mental model of the project. Evaluate against these minimum quality standards:

| Section | Required Content | Severity if Missing |
|---------|-----------------|---------------------|
| **Title & description** | Clear project name, one-sentence purpose, what problem it solves | Critical |
| **Status indicators** | CI badges, version badge, license badge — all current and non-broken | Medium |
| **Quick start** | Minimum viable path from zero to working: install, configure, run | High |
| **Prerequisites** | Runtime, language version, OS, required accounts/keys | High |
| **Installation** | Copy-pasteable commands that work on a clean machine | High |
| **Usage examples** | At least one realistic example showing the primary use case | High |
| **Configuration** | Environment variables, config files, required secrets (without values) | Medium |
| **License** | License type stated with link to LICENSE file | High |
| **Contributing** | Link to CONTRIBUTING.md or inline contribution guide | Low |

**Output:** Repository architecture findings with file inventory, missing sections, and anti-pattern flags.

---

### Phase 7: Audience Calibration (Audit mode)

Load `templates/audience-calibration.md` for the expert blind spot audit worksheet, reading level guide, information scent scoring, and assumed context checklist.

Evaluate whether the documentation is calibrated to its actual audience — not the audience the author imagines. The most common calibration failure is the expert blind spot (Hinds 1999): authors assume knowledge they possess is common knowledge.

| Check | What to look for | Severity |
|-------|-----------------|----------|
| **Expert blind spot** | For each domain-specific term, can both domain experts AND newcomers interpret it? If either audience cannot interpret a displayed term, it requires a tooltip, glossary entry, or inline explanation | High |
| **Glossary completeness** | If the project uses 3+ domain-specific terms, is there a glossary? Cross-reference every unique term against the glossary — any gap means the help system exists but doesn't cover that term | Medium |
| **Reading level** | Is vocabulary appropriate for stated audience? Flag academic jargon in user-facing docs, oversimplification in API reference | Medium |
| **Assumed context** | Does the doc assume tools, environment, OS, or knowledge the reader may not have? Each "simply run X" hides an unstated prerequisite | High |
| **Information scent** (Pirolli & Card) | Do navigation labels use goal-oriented vocabulary? Would a target user predict the content behind each label? Score every top-level navigation label: Strong / Medium / Weak | High |
| **Progressive disclosure** | Can novices complete core tasks without encountering expert-only content? Can experts skip beginner material efficiently? | Medium |
| **Expertise spectrum** | Does the documentation serve at least two levels (newcomer + experienced)? Are different paths available or clearly marked? | Medium |
| **Cultural/regional assumptions** | Hemisphere-specific season references, culturally specific metaphors, US-centric date formats, imperial units without metric | Low |
| **Safe, successful, known** (Lemov Principle 5) | Does the documentation make readers feel safe to try (acknowledges failure points), successful (provides early wins), and known (acknowledges different reader profiles)? | Medium |

#### Per-label scent scoring table

Complete for every top-level navigation item in the documentation:

| Navigation Label | Target User Goal | Scent Strength | Issue (if Weak/Medium) |
|-----------------|------------------|----------------|------------------------|
| [label] | [what goal does the user expect this leads to?] | Strong / Medium / Weak | [why the label fails to predict content] |

Labels that use implementation vocabulary, abbreviations, or domain jargon without context score Weak for newcomers. Goal-oriented labels ("Getting Started", "API Reference", "How to Deploy") score Strong.

#### Information Scent Analysis (Pirolli & Card)

Documentation navigation labels are not just organizational — they are *scent cues* that predict whether the reader's goal lies behind that link. Weak scent causes wrong choices, backtracking, and abandonment.

| Check | What to look for | Severity |
|-------|-----------------|----------|
| Label-goal alignment | Does each navigation label use the reader's goal vocabulary, not the author's implementation vocabulary? (e.g., "Getting Started" vs "Setup Module") | High |
| Scent strength | Would the target reader predict the content behind this label? Would they choose it from a list of alternatives? | High |
| Scent continuity | Does each page provide scent trails (links, "see also", related pages) to logically adjacent content? | Medium |
| Between-patch cost | How many clicks and page loads are required to move between related content on different pages? | Medium |
| Dead-end detection | Does any documentation page lack outbound links to related content? (dead-end patches force the reader back to the navigation root) | Medium |

#### Documentation navigation anti-patterns

| Pattern | Issue | Severity |
|---------|-------|----------|
| Documentation table of contents that mirrors the codebase directory structure instead of reader goals | Implementation-oriented navigation — readers think in tasks, not in file paths | High |
| "Overview" or "Introduction" pages with no actionable content or onward links | Low-scent entry points that waste the reader's first click | Medium |
| Nested documentation hierarchy deeper than 3 levels | Readers lose orientation beyond 3 levels (Miller 1956 — path depth exceeds chunk capacity) | Medium |
| Search-only navigation with no browsable structure | Forces readers to know the right keywords before they can find content | High |
| Multiple unlinked documentation surfaces (repo README, hosted docs, wiki) with no cross-references | Documentation archipelago — readers find one island and miss the others | High |

#### Expert Blind Spot Audit (Hinds 1999)

For each domain-specific term or concept used in the documentation, complete this structured check:

| Term/Concept | Newcomer | Experienced Dev | Both Fail? | Required Fix |
|-------------|----------|-----------------|------------|-------------|
| [term] | Can interpret? Y/N | Can interpret? Y/N | If either N | Glossary entry / inline definition / tooltip |

If either audience cannot interpret a term, it requires at minimum: (1) an inline definition or glossary link, (2) a contextual example, or (3) a "Prerequisites" block listing what the reader must already know. Terms that fail for *both* audiences are Critical — they are opaque to everyone except the author.

**Glossary completeness check:** If the project has a glossary, cross-reference every unique domain term, API concept, and abbreviation against the glossary index. Any term used in the documentation without a corresponding glossary entry is a gap — the help system exists but doesn't cover that term. An incomplete glossary is itself a blind spot: the author assumed certain terms were obvious because they were obvious *to the author*.

#### Assumed context checklist

For each procedural document, inventory every implicit assumption:

| Assumption Type | Example | How to Surface |
|----------------|---------|---------------|
| **Tool availability** | "Run `docker compose up`" assumes Docker is installed | Prerequisites block listing required tools with versions |
| **Environment** | "Open your terminal" assumes Unix-like OS | State OS requirements; provide OS-specific alternatives |
| **Prior knowledge** | "Configure your OAuth callback URL" assumes OAuth understanding | Link to prerequisite concept doc or external resource |
| **Access/permissions** | "Deploy to production" assumes deployment access | State required permissions or roles |
| **File state** | "Edit `config.yaml`" assumes the file exists and the reader knows its location | Provide file path; mention if it needs to be created first |

**Output:** Audience calibration findings with expert blind spot inventory, scent scores, and assumed context list.

---

### Phase 8: Completeness & Freshness (Audit mode)

| Check | What to look for | Severity |
|-------|-----------------|----------|
| Broken links | Internal and external links that 404 or redirect to unexpected locations | High |
| Outdated content | References to deprecated APIs, old UI screenshots, removed features, archived dependencies | High |
| Missing documentation gaps | Public API endpoints without docs, features without how-tos, error codes without troubleshooting | High |
| Implicit assumption inventory | Every "simply", "just", "obviously" hides an unstated prerequisite — inventory them | Medium |
| Cross-reference completeness | Do related docs link to each other bidirectionally? | Medium |
| Changelog currency | Is the changelog up to date with the latest release? | Medium |
| Example code freshness | Do code examples use current API versions? Do they run against the current codebase? | High |
| Screenshot freshness | Do screenshots match the current UI? | Medium |
| Dependency documentation | Are documented dependency versions current? Do installation instructions work with the latest versions? | High |

#### Coverage gap analysis

For each public-facing component, verify documentation exists:

| Component Type | Documentation Required | How to Detect Gaps |
|---------------|----------------------|-------------------|
| **Public API endpoints** | Each endpoint documented with method, path, parameters, response, errors | Compare route definitions against API docs |
| **CLI commands** | Each command documented with flags, arguments, examples, exit codes | Compare CLI parser against docs |
| **Configuration options** | Each option documented with type, default, valid values, effect | Compare config schema/env vars against docs |
| **Error codes/messages** | Each user-facing error documented with cause, fix, prevention | Grep for error strings and cross-reference with troubleshooting docs |
| **UI features** | Each user-visible feature mentioned in at least one how-to or tutorial | Compare page/component list against documentation index |
| **Breaking changes** | Each breaking change documented in changelog with migration steps | Compare version tags against changelog entries |

#### Staleness detection heuristics

| Signal | What it indicates | Action |
|--------|-------------------|--------|
| File not modified in >6 months but references active features | Content may be stale — verify against current codebase | Cross-reference with git log |
| Version numbers in prose that don't match current release | Outdated version references | Update or remove version-specific language |
| Links to external docs with date-stamped URLs (e.g., `/v2/` when `/v3/` exists) | Dependency documentation drift | Verify links resolve to current versions |
| Screenshots with UI elements that no longer exist | Visual documentation decay | Re-capture or remove |
| Import statements or CLI commands that reference renamed/removed packages | Code example rot | Run examples against current codebase |

**Output:** Completeness and freshness findings with specific gaps, broken links, and outdated content.

---

### Phase 9: Findings Report (Both modes)

Generate the final report. The format depends on the mode.

#### Planning mode report

Present the documentation strategy:

```markdown
## Documentation Strategy — [Project Name]

### Documentation Surface Summary
- Files: [count and list]
- Audiences: [first-time / regular / contributor / operator breakdown]
- Core tasks: [3-5 primary reader goals]
- Documentation maturity: [none / minimal / partial / comprehensive]
- Identified risk areas: [gaps, missing types, audience mismatches]

### Content Type Map (Diataxis)
| Document | Quadrant | Status | Priority |
|----------|----------|--------|----------|
| [doc name] | Tutorial / How-To / Reference / Explanation | Exists / Needed / Planned | High / Medium / Low |

### Learning Path Design
| Audience | Entry Point | Prerequisites | Progression |
|----------|-------------|---------------|-------------|
| [audience type] | [first doc to read] | [what they must know] | [reading order] |

### Scaffolding Strategy
| Document | Scaffolding Approach | Worked Example Type | Verification Method |
|----------|---------------------|---------------------|---------------------|
| [doc] | [explicit / guided / open-ended] | [process / product] | [command / expected output / screenshot] |

### Documentation Checklist
- [ ] Content type map designed for all core user tasks
- [ ] Audience spectrum considered (newcomer to expert)
- [ ] Prerequisites identified and front-loaded for each document
- [ ] Style guide selected (Google / Microsoft / custom)
- [ ] Template structure defined for each document type
- [ ] Verification commands planned for procedural content
- [ ] Cross-reference strategy defined
```

#### Audit mode report

Present concrete findings with documentation impact assessment:

```markdown
## Documentation Audit Report — [Project Name]

### Executive Summary
- Total findings: X
- Critical: X | High: X | Medium: X | Low: X
- Fixed during audit: X
- Remaining: X
- Primary documentation risk: [summary of biggest issue]
- Documentation maturity: [none / minimal / partial / comprehensive]

> **Counting rule:** When multiple phase-level findings consolidate into fewer root-cause findings, the summary MUST show both counts — e.g., "High: 3 findings (7 instances)". The reader will encounter instance-level detail first (Phase 0 tables) before reaching the consolidated view (Phase 9). Stating only the consolidated count creates a comprehension gap: the reader counts N severity rows in phase tables and cannot reconcile with a smaller summary number.

### Findings
| # | Severity | Phase | File:Line | Description | Framework | Status |
|---|----------|-------|-----------|-------------|-----------|--------|
| 1 | Critical | Phase 6 | README.md | Missing entirely — no project documentation entry point | Repo Architecture | Open |
| 2 | High | Phase 4 | tutorial.md:42 | Tutorial ends without a working result — contract violation | Diataxis (Tutorial); Lemov (Begin with the End) | Recommended |

> **Schema note:** The base columns (#, Severity, Phase, File:Line, Description, Status) are shared across all audit skills. The Framework column is specific to documentation-audit and cognitive-interface-audit.

### Diataxis Classification
| Document | Assigned Quadrant | Pollution? | Issues |
|----------|------------------|------------|--------|
| [doc] | Tutorial / How-To / Reference / Explanation / Non-quadrant | Yes/No | [summary] |

### Pedagogical Assessment
| Document | Objective? | Prerequisites? | Verification? | Scaffolding? | Issues |
|----------|-----------|----------------|---------------|-------------|--------|
| [doc] | Y/N | Y/N | Y/N | Appropriate/Over/Under | [summary] |

### Phase Coverage Matrix
| Phase | Checks Run | Findings | Key Result |
|-------|-----------|----------|------------|
| Phase 0: Anti-Patterns | [X patterns scanned] | [Y findings] | [summary] |
| Phase 1: Discovery | [X files inventoried] | [Y risk areas] | [summary] |
| Phase 2: Diataxis | [X docs classified] | [Y pollution findings] | [summary] |
| Phase 3: Linguistic | [X rules checked] | [Y violations] | [summary] |
| Phase 4: Pedagogical | [X checks] | [Y gaps] | [summary] |
| Phase 5: Consistency | [X checks] | [Y violations] | [summary] |
| Phase 6: Repo Architecture | [X files checked] | [Y missing] | [summary] |
| Phase 7: Audience | [X checks] | [Y findings] | [summary] |
| Phase 8: Completeness | [X checks] | [Y findings] | [summary] |

### Documentation Maturity Rating
- **Checks passed**: X/Y (Z% coverage)
- **Overall**: [Excellent / Good / Needs Work / Critical Gaps]
- **Strongest area**: [phase/area]
- **Weakest area**: [phase/area]

### Ready for users: Yes / No (with blockers)
```

#### Finding deduplication

Before finalizing the report, check whether any findings across phases share a root cause. The same issue often appears in multiple phases under different frameworks — e.g., "prerequisites not front-loaded" may appear as a Knowledge Organizer gap (Phase 4, Lemov #5) and an assumed context finding (Phase 7, Carroll). Consolidate into a single finding and note which phases identified it:

```
| # | Severity | Phases | File | Description | Frameworks | Status |
| 7 | Medium | 4, 7 | README.md | Prerequisites not front-loaded — uv requirement in Tech Stack, not Quick Start | Lemov #5; Carroll | Open |
```

This prevents inflated finding counts that undermine report credibility.

---

## Audit methodology (Lemov-derived)

These techniques from Lemov's observation framework govern *how* the auditor works, not *what* they evaluate:

| Technique | Application | Violation |
|-----------|-------------|-----------|
| **Exemplar Planning** (#1) | Before assessing a document, write the ideal version of the specific element being assessed. Compare against the exemplar, not an internalized standard | Judging docs against "I would have written it differently" without a concrete reference |
| **Plan for Error** (#2) | Before reading, predict the 3 most likely documentation failures for this document type. Then look for them | Starting the audit with no hypotheses — passive reading misses systematic issues |
| **Active Observation** (#9) | Conduct sequential passes with a single focus per pass (first pass: structure only, second pass: linguistic precision, third pass: pedagogical scaffolding). Written tracking. Deferred analysis after observation completes | Trying to catch everything in a single read — attention splits degrade detection accuracy |
| **Standardize the Format** (#8) | Use consistent tables and checklists for every document. Same column headers, same severity scale | Ad hoc notes that cannot be compared across documents |
| **Everybody Writes** (#38) | Formative before summative — explore what *might* be unclear before judging whether it meets the standard | Jumping to severity ratings before understanding the author's intent |
| **Stretch It** (#17) | For each finding, ask six follow-up questions: How? Why? What if? What's another example? What's the evidence? What's the counterargument? | Surface-level findings without root cause analysis |
| **Exit Ticket** (#26) | Define session outcomes before starting the audit. What specific questions must be answered by the end? | Open-ended "review the docs" with no success criteria |

## Important rules

- **Fix as you go.** Don't just report — remediate. Fix Critical and High issues during the audit.
- **Evidence-based claims.** Every finding must include file path, line number, or specific evidence. Never say "users will find this confusing" without identifying the specific cognitive mechanism.
- **Framework attribution.** Each finding references the specific framework that identifies it (Strunk & White, Diataxis, CLT, Lemov, Pirolli & Card, Carroll). This distinguishes a documentation audit from generic editorial feedback.
- **Right Is Right.** Do not "round up" findings. If documentation is approximately correct but missing specifics a reader needs to act, that is a finding.
- **Exemplar Planning.** Before assessing a document, write the ideal version of the specific element being assessed. Compare against the exemplar, not an internalized standard.
- **Active Observation.** Conduct sequential passes with a single focus per pass. Written tracking. Deferred analysis after observation completes.
- **Formative before summative.** Explore what *might* be unclear before judging whether it meets the standard.
- **No assumptions.** Read the actual documentation files. Don't assume docs are good because the codebase is well-structured.
- **Scope awareness.** Don't flag auto-generated documentation (Swagger/OpenAPI, typedoc) for style violations unless the generation templates themselves can be improved.
- **Respect intentional choices.** If a documentation structure departs from Diataxis intentionally (e.g., Python's deliberate pragmatic mixing), evaluate whether the mixing is *managed* rather than flagging it categorically.
- **The documentation should be invisible.** The best outcome is readers completing tasks without thinking about the documentation at all. Every finding should point toward that goal.
- **Report self-consistency.** The audit report is itself documentation. Before finalizing, verify: every count in the Executive Summary is reconcilable with the detailed tables, severity labels in phase tables match findings table, no number requires the reader to trust the author's grouping logic without explanation.
