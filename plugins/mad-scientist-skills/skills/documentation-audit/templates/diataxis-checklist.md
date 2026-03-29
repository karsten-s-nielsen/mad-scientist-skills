# Diataxis Classification Checklist

## Purpose

Answer: "Is each document the right type, and does it stay in its lane?"

## Pre-audit checklist

Before classifying, identify:

- [ ] All documentation files and their apparent purpose
- [ ] Whether the project uses an explicit documentation framework
- [ ] Which documents are user-facing vs. internal/development
- [ ] Any non-quadrant types needed (README, changelog, ADR, troubleshooting)

Diataxis (Procida, 2017+) organizes documentation along two axes: **study vs. work** (the user's context) and **practical vs. theoretical** (the knowledge type). Every document should occupy exactly one quadrant. When a document drifts into a neighboring quadrant, it serves neither purpose well — this is **quadrant pollution**.

**Important:** Not all documents are Diataxis documents. READMEs, CHANGELOGs, ADRs, troubleshooting guides, migration guides, and FAQs are **non-quadrant types** (see Good Docs Project Extensions below). Do NOT classify them into a Diataxis quadrant or flag them for quadrant pollution. A README that contains tutorial steps, reference tables, and explanatory context is doing its job as a gateway document — evaluate it against the Good Docs Project README template, not against Diataxis purity rules.

## The Four Quadrants

| Quadrant | User State | Knowledge Type | Contract | Language Markers | Structural Markers | Common Violations |
|----------|-----------|----------------|----------|-----------------|-------------------|-------------------|
| **Tutorial** | At Study | Practical | Teacher guarantees a learning outcome — the reader *will* reach a working result by following every step | "In this tutorial, we will..." / "First, let's..." / "You should now see..." | Numbered steps leading to a single concrete result; verification after each milestone; no branching paths | Reference tables, exhaustive option lists, architecture explanations, digressions into "why" |
| **How-To** | At Work | Practical | Assumes competence — the reader already understands the domain and needs task-specific directions | Imperative verbs; "Prerequisites:" section; "To [achieve goal], run..." | Goal-oriented steps; title states the task ("How to..."); no foundational teaching; may list alternatives | Foundational teaching ("What is X?"), conceptual explanations, lengthy background sections |
| **Reference** | At Work | Theoretical | Austere, authoritative, product-led — the reader consults it, not reads it end-to-end | Third person; declarative sentences; no "we" or "you"; formal register | Mirrors product/API/CLI structure; tables of parameters, signatures, return types; alphabetical or structural ordering | Instructional language ("you should..."), opinions, narrative flow, procedural steps, "we recommend" |
| **Explanation** | At Study | Theoretical | Discursive — addresses "why" something works the way it does, explores context and trade-offs | Connective phrases; "The reason for this is..."; "Historically,..."; "An alternative approach would be..." | Historical context, analogies, trade-off discussions, architectural rationale, comparison of approaches | Procedural steps, executable code blocks, API tables, "run this command" |

## Quadrant Classification Decision Tree

For each document, walk through these questions in order. Stop at the first match.

1. **Does it teach a newcomer through guided steps to a working result?**
   - The reader has no prior competence. The document takes full responsibility for the outcome.
   - Classification: **Tutorial**

2. **Does it help a competent user achieve a specific real-world goal?**
   - The reader already knows what they want. The document provides directions, not education.
   - Classification: **How-To Guide**

3. **Does it describe the machinery (API, CLI, config, data model) for consultation?**
   - The reader looks up specific facts. The document is structured by the product, not by tasks.
   - Classification: **Reference**

4. **Does it explain why something works the way it does, or discuss trade-offs?**
   - The reader wants understanding, not instructions. The document is discursive and connective.
   - Classification: **Explanation**

5. **Does it not fit any of the above?**
   - The document may be a non-quadrant type. See [Good Docs Project Extensions](#good-docs-project-extensions) below.
   - If it still does not fit, it may be a hybrid that needs splitting.

## Quadrant Identification Signals

Use these grep-friendly patterns for initial classification during bulk triage.

**Tutorial signals:**
- `In this tutorial` / `we will build` / `we will create` / `by the end of this`
- `First, let's` / `Now let's` / `You should now see`
- Numbered steps with verification checkpoints ("Confirm that...")

**How-To signals:**
- Title matches `How to ...` / `Deploying ...` / `Configuring ...` / `Setting up ...`
- `Prerequisites:` section present
- Imperative verbs without teaching: "Run...", "Add...", "Configure..."

**Reference signals:**
- Tables of parameters, flags, methods, fields, return types
- No first or second person — third person or impersonal throughout
- Structure mirrors the product (one heading per endpoint, command, config key)

**Explanation signals:**
- `The reason for this` / `Historically` / `The trade-off` / `compared to`
- Paragraphs connected by "because", "therefore", "however", "alternatively"
- No numbered procedural steps; no executable code blocks

## Pollution Detection Patterns

When a document drifts from its assigned quadrant into another, readers get neither the focused guidance nor the reference precision they need. Each pollution type has characteristic signals.

| Pollution Type | Signal (what to grep/look for) | Example | Fix |
|---------------|-------------------------------|---------|-----|
| **Tutorial → Reference** | Tables of all options, exhaustive parameter lists, or API signatures inside a tutorial | A "Getting Started" tutorial that lists every CLI flag after showing the first command | Extract the reference table into a dedicated reference page; link to it with "For the full list of options, see [Reference]" |
| **Tutorial → Explanation** | Paragraphs explaining *why* the architecture works this way, historical context, or design rationale mid-tutorial | A setup tutorial that spends 500 words on why the framework chose this configuration format | Move the explanation to a dedicated "Understanding X" page; keep the tutorial focused on "do this, then this" |
| **How-To → Tutorial** | Foundational teaching ("What is X?"), definitions of basic concepts, or explanations of prerequisites the reader should already know | A deployment how-to that opens with "Docker is a containerization platform that..." | Remove the teaching; add a "Prerequisites: familiarity with Docker" line and link to an introductory tutorial |
| **How-To → Explanation** | Extended rationale, trade-off discussions, or "why we chose this approach" sections inside procedural content | A migration how-to that includes three paragraphs comparing the old and new architecture | Move the rationale to an explanation page; in the how-to, link to it with "For background on this change, see [Explanation]" |
| **Reference → How-To** | Procedural steps ("First, configure X. Then, run Y."), numbered instructions, or task-oriented sequences in reference material | An API reference page that includes a multi-step "Getting Started" workflow between endpoint descriptions | Extract the procedure into a how-to guide; keep the reference page as pure lookup |
| **Reference → Explanation** | Narrative paragraphs explaining "why" a parameter exists, design rationale, or opinion ("we recommend") in reference material | A configuration reference that includes "We chose YAML over JSON because..." after the config key table | Move the rationale to an explanation page; in the reference, state only the facts — what the parameter does, its type, its default |
| **Explanation → Reference** | API tables, parameter signatures, or exhaustive option lists embedded in a conceptual discussion | An architecture explanation that includes a full table of every database column and its type | Link to the reference page for specifics; in the explanation, mention only the key fields relevant to the point being made |
| **Explanation → How-To** | Procedural steps, imperative commands ("run this"), or task-oriented instructions inside a conceptual discussion | A "Why we use event sourcing" explanation that ends with "To set up event sourcing, run `npm install ...`" | Extract the procedure into a how-to guide; end the explanation with a link: "Ready to implement? See [How to set up event sourcing]" |

### Intentional Mixing vs. Accidental Pollution

Not all quadrant mixing is a defect. Some projects (notably Python's documentation) deliberately blend quadrant types within single pages as a conscious editorial strategy. Before flagging pollution, verify:

1. **Is the mixing managed?** Does the document use clear visual or structural separation (callout boxes, "Background" sidebars, collapsible sections) to signal the shift?
2. **Is there a stated rationale?** A style guide or contribution doc that explains the mixing strategy means it is intentional.
3. **Does the mixing serve the reader?** If a brief "why" aside in a tutorial prevents a common misconception, it may be net positive even though it technically crosses quadrant boundaries.

If all three answers are "yes," note the mixing as an **observation**, not a **finding**.

### Missing Quadrant Check

A complete documentation set should have coverage across all four quadrants. After classifying every document, check:

- **No tutorials?** New users have no guided entry point — they must learn by reading reference or reverse-engineering how-tos. Severity: **High**.
- **No how-tos?** Competent users cannot find task-oriented directions — they must piece together procedures from reference pages. Severity: **High**.
- **No reference?** Users have nowhere to look up specific facts (parameters, signatures, config keys) — they must search through tutorials or how-tos. Severity: **High**.
- **No explanation?** Users cannot understand *why* the system works this way — they have facts but no conceptual framework. Severity: **Medium** (less urgent but erodes long-term comprehension).

## Good Docs Project Extensions

Not all documentation fits the four Diataxis quadrants. The Good Docs Project (thegooddocsproject.dev) provides templates for document types that serve structural or operational roles rather than epistemic ones.

| Type | Purpose | Required Sections | Diataxis Relationship |
|------|---------|-------------------|----------------------|
| **README** | Gateway document — first contact for new visitors; orients and routes to other docs | Project name and description, quick start (or link to tutorial), installation, usage summary, contributing link, license | Not a quadrant document — it is a **routing layer** that links to tutorials, how-tos, and reference. Should not itself be a tutorial |
| **CHANGELOG** | Version history — communicates what changed between releases, for users deciding whether to upgrade | Version heading, date, categorized entries (Added, Changed, Deprecated, Removed, Fixed, Security) per Keep a Changelog | Not a quadrant document — it is a **temporal record**. May link to migration guides (how-to) or explanations of breaking changes |
| **ADR** | Architecture Decision Record — captures the context, decision, and consequences of a significant technical choice | Title with sequential number, Status, Context, Decision, Consequences (positive and negative) | Closest to **Explanation** (addresses "why"), but distinct because it is time-stamped and immutable once accepted |
| **Troubleshooting Guide** | Error recovery — helps users diagnose and resolve known failure modes | Symptom-based headings, diagnostic steps, resolution steps, when to escalate | Closest to **How-To** (task-oriented), but organized by symptoms rather than goals. Users arrive via error messages, not intentions |
| **Migration Guide** | Version transitions — guides users from version N to version N+1 with specific procedural steps | Prerequisites (current version, backups), step-by-step migration procedure, breaking changes, rollback procedure | A specialized **How-To** with additional context from **Explanation** (why the change was made). Intentional mixing is acceptable here |
| **FAQ** | Common questions — aggregates frequently asked questions with concise answers | Question-and-answer pairs grouped by topic | A **routing document** — each answer should be brief and link to the canonical source (tutorial, how-to, reference, or explanation) rather than duplicating content |

## Classification Worksheet

For each document in the documentation set, complete one row. Use the decision tree above and the pollution detection patterns to fill in each column.

| Document | Assigned Quadrant | Confidence (High/Med/Low) | Pollution Found? | Action Required |
|----------|------------------|--------------------------|-----------------|-----------------|
| | | | | |
| | | | | |
| | | | | |
| | | | | |
| | | | | |

**Confidence guide:**
- **High** — The document cleanly fits one quadrant with no pollution signals detected
- **Med** — The document fits a quadrant but contains minor pollution that can be fixed in place
- **Low** — The document spans multiple quadrants and may need to be split into separate documents

**Action categories:**
- **None** — Document is correctly classified and clean
- **Clean** — Remove pollution (move offending content to the correct quadrant document)
- **Split** — Document serves two quadrants and should become two documents
- **Reclassify** — Document is labeled or filed as one type but is actually another
- **Create** — A needed document type is missing from the documentation set entirely
