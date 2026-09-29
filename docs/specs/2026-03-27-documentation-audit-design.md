# Documentation Audit Skill — Design

**Date:** 2026-03-27
**Branch:** `feature/documentation-audit-skill`
**Status:** Approved
**Maturity:** v1.0

---

## Purpose

A comprehensive documentation audit skill that evaluates a repository's documentation quality across linguistic precision, structural taxonomy, pedagogical effectiveness, consistency, architecture, audience calibration, and content freshness. Mirrors the existing audit skill patterns: two modes (Planning/Audit), phased execution with severity classification, evidence-based findings, and a final report.

This skill is **single tier** — documentation evaluation is methodology-based (style guide application, framework classification, cognitive load analysis), not tool-licensed. Vale, markdownlint, and the analytical frameworks are all free/open-source.

**Security audit asks:** "Can attackers exploit this?"
**Observability audit asks:** "Can operators see what's happening?"
**Optimization audit asks:** "Is this system using resources efficiently?"
**Cognitive-interface audit asks:** "Does the interface think the way the user thinks?"
**Documentation audit asks:** "Does this documentation teach effectively?"

---

## Academic Foundations

Seven research threads synthesized into a single audit methodology:

1. **Classical Composition** (Strunk & White 1918/1959) — Omit needless words, active voice, positive form, specific/concrete language, parallel construction. The foundational linguistic layer.

2. **Enterprise Style Standards** (Google Developer Documentation Style Guide; Microsoft Writing Style Guide) — Second person, conditions before instructions, timeless language, inclusive terminology, global accessibility. The enforceable ruleset layer with Vale automation support.

3. **Structural Taxonomy** (Procida, Diataxis Framework 2017+; augmented by Good Docs Project) — Four epistemic quadrants (Tutorial, How-To, Reference, Explanation) based on study vs. work and practical vs. theoretical axes. Quadrant pollution detection. Augmented with Good Docs Project templates for changelogs, READMEs, ADRs, troubleshooting, and migration guides.

4. **Cognitive Load Theory** (Sweller 1988; Chandler & Sweller 1992; Willingham 2009) — Intrinsic/extraneous/germane load taxonomy. Split-attention effect. Guidance fading effect: novices need explicit scaffolding; discovery-style documentation actively harms new users. Forgetting curve (Ebbinghaus 1885): documentation must support elaborative retrieval, not just initial comprehension.

5. **Minimalism & Instructional Design** (Carroll 1990; Merrill 2002; Gagné 1965) — Carroll's four minimalist principles for software instruction: immediate meaningful tasks, minimize passive instruction, support error recognition/recovery, self-contained modules. Merrill's five first principles: task-centered, activation, demonstration, application, integration.

6. **Instructional Techniques** (Lemov, *Teach Like a Champion 3.0*, 2021) — Ten techniques applied at two levels:
   - **Content quality heuristics:** Take the Steps/guidance fading (#21), Knowledge Organizers/front-loaded prerequisites (#5), Retrieval Practice/elaborative recall (#7), Right Is Right/precision over approximation (#16), Begin with the End/measurable objectives (4 Ms)
   - **Audit methodology:** Exemplar Planning/write the ideal before auditing (#1), Plan for Error/pre-plan error hypotheses (#2), Active Observation/sequential focused passes (#9), Everybody Writes/formative before summative (#38), Exit Ticket/define session outcomes before starting (#26), Standardize the Format/consistent observation instruments (#8), Stretch It/six-category follow-up questions (#17)

7. **Information Foraging** (Pirolli & Card 1999) — Users follow "information scent" cues predicting whether a navigation path leads to their goal. Applied to navigation labels, cross-document linking, and search discoverability.

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

---

## Modes

| Signal | Mode | Rationale |
|--------|------|-----------|
| User says "plan the docs", "documentation strategy", "what docs do we need" | **Planning** | Design documentation architecture before writing |
| User says "audit the docs", "review documentation", "check doc quality" | **Audit** | Evaluate existing documentation |
| No documentation exists yet | **Planning** | Nothing to audit — design the strategy |
| Documentation files exist | **Audit** | Concrete artifacts to evaluate |
| Docs exist + "redesign the doc structure" | **Both** | Audit current state, plan improvements |

When in doubt, ask the user. If both modes apply, run all phases.

---

## Single Tier Rationale

Documentation evaluation is methodology-based, not tool-licensed:
- **Linting** is free: Vale (Google/Microsoft packages), markdownlint, alex
- **Style guides** are free: Google, Microsoft, Splunk (open-source Vale rules)
- **Frameworks** are free: Diataxis, Good Docs Project templates
- **The value is in the analytical framework**, not the scanner

Enterprise documentation platforms (Readme.com, Gitbook, Confluence) don't change *what* to evaluate — only where the content lives.

---

## Severity Classification

| Severity | Criteria | Action | SLA |
|----------|----------|--------|-----|
| **Critical** | Documentation is actively misleading — procedures that cause data loss, security instructions that create vulnerabilities, wrong API signatures that produce silent failures. Missing docs for critical safety/security paths | Fix immediately | Block release |
| **High** | Users cannot complete core tasks from the docs alone. Major quadrant pollution. Missing prerequisites causing predictable failures. Systematic passive voice obscuring the responsible agent. No verification commands on destructive operations | Fix before next release | 1 sprint |
| **Medium** | Users succeed but with unnecessary friction. Style guide violations, inconsistent formatting, missing cross-references, suboptimal chunking, vague abstractions, incomplete worked examples | Schedule fix | 2 sprints |
| **Low** | Best practice deviation, minor polish. Sentence length, minor vocabulary inconsistency, missing alt text on decorative images, optional metadata | Track in backlog | Best effort |

---

## Phase Architecture

Execute all applicable phases in order. Skip phases marked for a mode you are not running. Do NOT skip applicable phases. Do NOT claim completion without evidence.

**Phase order:** 0 → 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8 → 9

### Phase 0: Anti-Pattern Scan (Audit mode)

Fast grep-based scan for common documentation anti-patterns. Each match requires manual review — some patterns are intentional in specific contexts.

**Linguistic anti-patterns:**

| Pattern | Issue | Severity |
|---------|-------|----------|
| Passive voice: "was performed", "is configured by", "are managed by", "was created" | Obscures the agent — reader cannot determine who/what performs the action (Strunk & White Rule 10) | Medium |
| "in order to", "the fact that", "due to the fact that", "it should be noted that", "in a [adj] manner" | Needless words — padding that slows comprehension (Strunk & White Rule 13) | Medium |
| "currently", "recently", "now", "new in version X", "will soon", "latest" | Temporal language that decays — docs should describe the product as-is (Google Style Guide: timeless language) | Medium |
| "whitelist", "blacklist", "master/slave", "sanity check", "dummy value" | Non-inclusive language (Google/Microsoft inclusive language guidelines) | High |
| "click here", bare URLs as link text, "see above", "as mentioned" | Inaccessible link text / directional language that fails for screen readers and reflow (Google Style Guide; WCAG) | High |
| "simply", "just", "obviously", "easily", "of course" | Implicit assumptions — each hides an unstated prerequisite or trivializes difficulty (Carroll's Minimalism — support error recognition) | Medium |

**Structural anti-patterns:**

| Pattern | Issue | Severity |
|---------|-------|----------|
| Code blocks in files named/structured as conceptual or explanatory docs (e.g., `architecture.md`, `concepts/`, `explanation/`) | Executable code in explanation = likely quadrant pollution (Diataxis) — confirm in Phase 2 | Medium |
| Step-by-step numbered procedures in files named/structured as reference docs (e.g., `api/`, `reference/`, `config-reference.md`) | Procedural content in reference = likely quadrant pollution (Diataxis) — confirm in Phase 2 | Medium |
| Paragraph-length text with no heading for >500 words | Wall of text — exceeds working memory capacity without structural aids (Sweller — extraneous load) | Medium |
| API/CLI/config reference sections containing "why" or "background" discussions | Explanatory content in reference = likely quadrant pollution (Diataxis) — confirm in Phase 2 | Medium |
| Tutorial/guide with no verification step after complex configuration | Missing "Check for Understanding" — reader has no way to confirm success (Lemov #7; Carroll — error recognition) | High |
| `<img` without `alt=` | Missing alt text — accessibility violation (WCAG 1.1.1) | High |

**Output:** Anti-pattern findings table with file paths, severity, and framework attribution.

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

**Output:** Documentation surface summary listing all files, audiences, core tasks, maturity level, and identified risk areas.

### Phase 2: Diataxis Classification (Both modes)

Load `templates/diataxis-checklist.md` for the full quadrant classification guide, pollution detection patterns, and Good Docs Project extensions.

**Planning mode:** Design the content type map:
- Which documents should be tutorials (learning-oriented, guided)?
- Which should be how-tos (task-oriented, assume competence)?
- Which should be reference (information-oriented, austere, authoritative)?
- Which should be explanation (understanding-oriented, discursive, connects concepts)?
- What document types are needed that don't fit the four quadrants (changelogs, READMEs, ADRs, troubleshooting, migration guides)?

**Audit mode:** Classify and evaluate each existing document:

| Check | What to look for | Severity if violated |
|-------|-----------------|---------------------|
| Quadrant identity | Can the document be classified into exactly one Diataxis quadrant? | High (if unclassifiable) |
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

**Output:** Classification table mapping each document to its quadrant, with pollution findings and missing type gaps.

### Phase 3: Linguistic Precision (Audit mode)

Load `templates/linguistic-rules.md` for the full Strunk & White, Google, and Microsoft rule reference with grep patterns and permitted exceptions.

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

**Output:** Linguistic findings with rule attribution, file paths, and recommended corrections.

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

**Output:** Pedagogical scaffolding assessment with framework attribution, gap analysis, and recommended fixes.

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

**Output:** Consistency findings table with pattern, locations, and recommended standard.

### Phase 6: Repository Architecture (Audit mode)

Load `templates/repo-architecture.md` for the full essential file checklist with required sections per file.

| File | Required Sections | Severity if Missing |
|------|------------------|---------------------|
| **README.md** | Project name, description, status badges, quick start, installation, prerequisites, usage examples, license | Critical (if missing entirely); High (if incomplete) |
| **CONTRIBUTING.md** | Dev environment setup, coding standards, commit conventions, test requirements, PR process, code review expectations | Medium |
| **SECURITY.md** | Vulnerability disclosure policy, supported versions, reporting process | High (for public repos) |
| **CODE_OF_CONDUCT.md** | Community standards | Low |
| **CHANGELOG.md** / release notes | Versioned change history with categories (Added, Changed, Deprecated, Removed, Fixed, Security) | Medium |
| **LICENSE** | Present and correctly identified | High |
| **API documentation** | Coverage relative to public API surface (every public endpoint, function, class documented) | High |

**Anti-patterns:**

| Pattern | Issue | Severity |
|---------|-------|----------|
| Monolithic AGENTS.md/CLAUDE.md that merely restates directory structure or obvious tech stack | Token waste — duplicates discoverable information (>20% token cost inflation) | Medium |
| Auto-generated docs committed without review (default Swagger UI, typedoc defaults) | False sense of completeness — generated docs often lack context, examples, and error documentation | Medium |
| Documentation in wiki/external system with no repo-level pointer | Discoverable documentation only by those who know where to look | High |
| Outdated badges (broken CI badge, wrong version, dead links) | Misleading project status signals | Medium |

**Output:** Repository architecture findings with file inventory, missing sections, and anti-pattern flags.

### Phase 7: Audience Calibration (Audit mode)

Load `templates/audience-calibration.md` for the expert blind spot audit worksheet, reading level guide, information scent scoring, and assumed context checklist.

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

**Output:** Audience calibration findings with expert blind spot inventory, scent scores, and assumed context list.

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

**Output:** Completeness and freshness findings with specific gaps, broken links, and outdated content.

### Phase 9: Findings Report (Both modes)

Generate the final report.

#### Planning mode report

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

```markdown
## Documentation Audit Report — [Project Name]

### Executive Summary
- Total findings: X
- Critical: X | High: X | Medium: X | Low: X
- Fixed during audit: X
- Remaining: X
- Primary documentation risk: [summary of biggest issue]
- Documentation maturity: [none / minimal / partial / comprehensive]

### Findings
| # | Severity | Phase | File:Line | Description | Framework | Status |
|---|----------|-------|-----------|-------------|-----------|--------|
| 1 | Critical | Phase 6 | README.md | Missing entirely — no project documentation entry point | Repo Architecture | Open |
| 2 | High | Phase 4 | tutorial.md:42 | Tutorial ends without a working result — contract violation | Diataxis (Tutorial); Lemov (Begin with the End) | Recommended |

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

---

## Templates

| File | Purpose |
|------|---------|
| `templates/diataxis-checklist.md` | Quadrant classification guide, pollution detection patterns, Good Docs Project extensions for non-quadrant types (changelogs, READMEs, ADRs, troubleshooting, migration guides) |
| `templates/linguistic-rules.md` | Strunk & White rules reference, Google/Microsoft key rules, grep-detectable patterns with regex, permitted exceptions |
| `templates/pedagogical-scaffolding.md` | Carroll's Minimalism principles, CLT taxonomy, Merrill's First Principles, Lemov content techniques with documentation-specific annotated work samples (exemplar vs. deficient) |
| `templates/repo-architecture.md` | Essential file checklist with required sections per file, anti-patterns, and severity |
| `templates/audience-calibration.md` | Expert blind spot audit worksheet, reading level guide, information scent scoring table, assumed context checklist |
| `templates/audit-methodology.md` | Portable Lemov audit methodology: Exemplar Planning, Plan for Error, Active Observation, Standardize the Format, Everybody Writes, Stretch It, Exit Ticket — reusable by other audit skills |

---

## Important Rules

- **Fix as you go.** When audit mode finds a Critical or High issue that you can fix, fix it immediately. Don't just report — remediate.
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

---

## Deliverables

| File | Est. Lines | Description |
|------|-----------|-------------|
| `skills/documentation-audit/SKILL.md` | 600-800 | Main skill file with frontmatter, foundations, phases 0-9, severity, mode detection, important rules |
| `skills/documentation-audit/templates/diataxis-checklist.md` | 100-150 | Quadrant guide + Good Docs extensions |
| `skills/documentation-audit/templates/linguistic-rules.md` | 150-200 | Strunk & White + Google/Microsoft patterns with regex |
| `skills/documentation-audit/templates/pedagogical-scaffolding.md` | 150-200 | Carroll + CLT + Merrill + Lemov content heuristics with annotated work samples |
| `skills/documentation-audit/templates/repo-architecture.md` | 80-120 | Essential file checklist |
| `skills/documentation-audit/templates/audience-calibration.md` | 100-150 | Expert blind spot + info scent + assumed context |
| `skills/documentation-audit/templates/audit-methodology.md` | 150-200 | Portable Lemov audit methodology |
