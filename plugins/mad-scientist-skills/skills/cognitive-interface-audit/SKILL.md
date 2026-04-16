---
name: cognitive-interface-audit
description: Comprehensive cognitive interface audit with two modes and a single tier. Planning mode designs task models, user expertise mapping, and error tolerance strategy. Audit mode evaluates mental model alignment (Norman's Gulfs), consistency (Gestalt), error tolerance (Wood 7-layer defense), cognitive load (NASA-TLX, Dual-Process), visual grounding (Gergle), trust calibration (Lee & See), data visualization integrity (Kirk, Cleveland & McGill, Brewer ColorBrewer palette enforcement), ecological constraint visibility (Vicente & Rasmussen EID), and accessibility. Single tier — cognitive evaluation tools are methodology-based, not software-licensed. Grounded in GOMS (Card, Moran & Newell), error-tolerant design (Wood & Byrne), visual grounding theory (Gergle, Kraut & Fussell), data visualization design (Kirk), information foraging (Pirolli & Card), and ecological interface design (Vicente & Rasmussen). Use when asked to "UI audit", "UX review", "cognitive audit", "mental model check", "usability review", or "interface audit".
---

# Cognitive Interface Audit

A comprehensive cognitive interface audit with two modes and a single tier:

**Modes:**
- **Planning** (before UI exists) — task model design, user expertise mapping, error tolerance strategy, information architecture
- **Audit** (on existing UI) — mental model alignment, consistency, error tolerance, cognitive load, visual grounding, accessibility

**Single tier:** Unlike security auditing, cognitive interface evaluation is methodology-based (GOMS analysis, heuristic evaluation, NASA-TLX scoring), not tool-licensed. No paid software is required. The value is in the analytical framework, not the scanner.

**Core question:** "Does the interface think the way the user thinks?"

## Academic foundations

This skill synthesizes seven research threads into a single audit methodology:

1. **Task Model & Error Tolerance** (Card, Moran & Newell 1983; Wood & Byrne 2002; Rasmussen 1983) — GOMS models predict how users decompose tasks. Wood's 7-layer defense framework predicts where errors occur and what defenses are needed at each stage. Rasmussen's SRK framework classifies errors by cognitive level (skill-based slips, rule-based misapplication, knowledge-based wrong mental model), each requiring different design countermeasures.

2. **Visual Grounding & Common Ground** (Gergle, Kraut & Fussell 2004/2013; Gergle et al. 2021) — Shared visual information affects task performance through two distinct mechanisms: situation awareness (does the user understand system state?) and conversational grounding (does the interface provide enough shared context?). Not just availability but the *form* of visual information differentially affects performance. The Joint Action Storyboard framework maps each interaction to its grounding cost.

3. **Cognitive Load** (Sweller 1988; Hart & Staveland 1988; Kahneman 2011) — Every interface decision either consumes or conserves working memory. NASA-TLX provides structured evaluation across 6 dimensions. Sweller's distinction between intrinsic load (inherent task complexity), extraneous load (poor design), and germane load (productive learning) guides where to invest and where to cut. Kahneman's Dual-Process Theory (System 1/System 2) identifies where interfaces force slow, deliberate processing when fast, intuitive processing could suffice.

4. **Gulf Analysis & Action Theory** (Norman 1988/2013) — Norman's Gulfs of Execution and Evaluation provide a structural diagnostic for interface fit. The Gulf of Execution measures the gap between what the user wants to do and what the interface lets them do. The Gulf of Evaluation measures the gap between system state and user understanding. Wider gulfs mean harder-to-use interfaces.

5. **Information Foraging** (Pirolli & Card 1999) — Users follow "information scent" — cues that predict whether a navigation path leads to their goal. Weak scent (ambiguous labels, implementation-oriented vocabulary) causes users to choose wrong paths or abandon the interface. Scent analysis evaluates navigation labels, cross-page links, and between-patch travel cost.

6. **Trust Calibration** (Lee & See 2004) — For interfaces displaying model-derived or automated outputs, users must develop *appropriate* trust — neither over-trusting (blind acceptance) nor under-trusting (ignoring valid outputs). Trust calibration requires visibility of model provenance, uncertainty, sample size, and known limitations.

7. **Ecological Interface Design** (Vicente & Rasmussen 1992) — EID argues that interfaces should make the work domain's constraints and relationships visible, not just the system's controls. The abstraction hierarchy (functional purpose → abstract function → generalized function → physical function → physical form) determines what users need to see at each level. When constraints are invisible (e.g., "why are only 20 matches available?"), users cannot calibrate their expectations or detect anomalies.

**Convergence:** Brinck, Gergle & Wood, *Usability for the Web: Designing Web Sites that Work* (Morgan Kaufmann, 2001) — the two primary research threads (Wood's error tolerance, Gergle's grounding) converge in a single prior collaboration: a "pervasive usability" framework with stage-by-stage checklists.

**Key references:**
- Card, Moran & Newell, *The Psychology of Human-Computer Interaction* (1983) — GOMS
- Norman, *The Design of Everyday Things* (1988; revised 2013) — Gulf of Execution/Evaluation
- Wood & Byrne, "A Cognitive Approach to Designing Human Error Tolerant Interfaces" (2002) — 7-layer defense
- Wood, "Modeling Human Error for Experimentation, Training, and Error-Tolerant Design" (IITSEC 2002)
- Gergle, Kraut & Fussell, "Action as Language in a Shared Visual Space" (*CHI*, 2004) — visual grounding in collaborative tasks
- Gergle, Kraut & Fussell, "Using Visual Information for Grounding and Awareness" (*HCI*, 2013) — journal expansion of the 2004 work
- Gergle et al., "Joint Action Storyboards" (CSCW 2021) — grounding cost visualization
- Brinck, Gergle & Wood, *Usability for the Web* (Morgan Kaufmann, 2001)
- Rasmussen, "Skills, Rules, and Knowledge" (*IEEE SMC*, 1983) — SRK framework
- Hart & Staveland, "Development of NASA-TLX" (1988) — cognitive load measurement
- Sweller, "Cognitive Load During Problem Solving" (*Cognitive Science*, 1988)
- Kahneman, *Thinking, Fast and Slow* (2011) — Dual-Process Theory (System 1/System 2)
- Cleveland & McGill, "Graphical Perception" (*JASA*, 1984) — visual encoding effectiveness ranking
- Pirolli & Card, "Information Foraging" (*Psychological Review*, 1999)
- Lee & See, "Trust in Automation" (*Human Factors*, 2004) — trust calibration
- Wertheimer, *Laws of Organization in Perceptual Forms* (1923) — Gestalt principles
- Hutchins, *Cognition in the Wild* (1995) — distributed cognition
- Vicente & Rasmussen, "Ecological Interface Design: Theoretical Foundations" (*IEEE SMC*, 1992) — EID
- Burns & Hajdukiewicz, *Ecological Interface Design* (CRC Press, 2004)
- Evans, *Domain-Driven Design: Tackling Complexity in the Heart of Software* (Addison-Wesley, 2003) — Ubiquitous Language
- Miller, "The Magical Number Seven, Plus or Minus Two" (*Psychological Review*, 1956) — working memory limits
- Cowan, "The Magical Number 4 in Short-Term Memory" (*Behavioral and Brain Sciences*, 2001) — revised Miller's 7±2 to ~4 chunks
- Nielsen, "10 Usability Heuristics for User Interface Design" (1994)
- Hick, "On the Rate of Gain of Information" (*Quarterly Journal of Experimental Psychology*, 1952) — choice reaction time
- Friedman, Kahn & Borning, "Value Sensitive Design and Information Systems" (2006) — designing for human values including bias
- Harrower & Brewer, "ColorBrewer.org: An Online Tool for Selecting Colour Schemes for Maps" (*The Cartographic Journal*, 2003) — scientifically validated colour palettes (sequential, diverging, qualitative) designed in Munsell perceptual colour space
- Olson & Brewer, "An Evaluation of Color Selections to Accommodate Map Users with Color-Vision Impairments" (*Annals of the Association of American Geographers*, 1997) — empirical colorblind safety evaluation of cartographic palettes

## When to use this skill

- When the user says "UI audit", "UX review", "cognitive audit", "mental model check", "usability review", "interface audit", or "check the UI"
- Before designing a new interface (planning mode) — to define task models and error tolerance strategy
- On an existing UI (audit mode) — to find mental model misalignment, cognitive overload, and error traps
- Before shipping a new page, workflow, or user-facing feature
- After user complaints about confusion, errors, or abandonment
- When onboarding users with different expertise levels (kiosk vs power user)

## Mode detection

Determine which mode to operate in based on the project state:

| Signal | Mode | Rationale |
|--------|------|-----------|
| User says "design the UI", "plan the interface", "task model" | **Planning** | Architecture-level UI design |
| User says "audit", "review the UI", "check usability", "why are users confused" | **Audit** | Existing interface evaluation |
| No UI code exists yet (wireframes, specs, or nothing) | **Planning** | Nothing to scan — design the task model |
| UI code exists (Streamlit, React, HTML, Gradio, etc.) | **Audit** | Concrete interface to evaluate |
| Both code and a request to "redesign the workflow" | **Both** | Audit current state, plan improvements |

When in doubt, ask the user. If both modes apply, run all 10 phases.

## Severity classification

Every finding must be assigned a severity based on cognitive impact:

| Severity | Criteria | Action | SLA |
|----------|----------|--------|-----|
| **Critical** | Users cannot complete core tasks. Systematic mental model mismatch — the interface's workflow contradicts how users think about the task. No error recovery path exists for common mistakes | Fix immediately | Block release |
| **High** | Users frequently make errors or abandon tasks. Significant cognitive overhead on primary workflows. Error recovery exists but is non-obvious or lossy | Fix before next release | 1 sprint |
| **Medium** | Users succeed but with unnecessary friction. Inconsistent patterns cause momentary confusion. Error recovery works but requires extra steps | Schedule fix | 2 sprints |
| **Low** | Minor polish, best practice deviation, or optimization for power users. Does not impede task completion | Track in backlog | Best effort |

## Audit process

Execute all applicable phases in order. Skip phases marked for a mode you are not running. Do NOT skip applicable phases. Do NOT claim completion without evidence.

**Phase order:** 0 → 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8 → 9

---

### Phase 0: Anti-Pattern Scan (Audit mode)

Fast grep-based scan for common cognitive interface anti-patterns. Runs first to catch obvious issues before deeper analysis. Each match requires manual review — some patterns are intentional in specific contexts.

#### Streamlit patterns

| Pattern | Issue | Severity |
|---------|-------|----------|
| `st.button(` with label containing "Delete" / "Remove" / "Clear" / "Reset" without preceding confirmation logic | Destructive action without confirmation (Wood Layer 1: Prevention) | High |
| `st.error(` with hardcoded string and no `st.button` or link in the same block | Error message without recovery guidance (Wood Layer 5: Correction) | High |
| `st.write("Error` or `st.write("Failed` | Informal error display — no structured error handling (Wood Layer 4: Identification) | Medium |
| `st.empty()` with no subsequent `.write` / `.markdown` / `.dataframe` call | Potential dead-end placeholder (no content rendered) (Gergle feedback — system gives no state indication) | Low |
| `st.columns(` with 5+ columns | Cognitive overload — too many parallel elements per viewport (Miller 1956 — working memory chunk limit; Sweller extraneous load) | Medium |
| `st.selectbox(` or `st.multiselect(` with inline list of 20+ items | Option overload without search/filter affordance (Miller 1956; Hick's Law — decision time grows with options) | Medium |
| `st.form_submit_button(` without corresponding `st.success` / `st.error` / `st.toast` in the form handler | Missing submit feedback — user doesn't know if action succeeded | High |
| Long-running operation (SQL query, API call, computation) without `st.spinner` or `st.status` wrapper | Missing progress indicator — user perceives system as frozen | High |
| Different `st.success` / `st.toast` / `st.balloons` patterns across pages for equivalent actions | Inconsistent success feedback (Consistency violation) | Medium |
| `st.page_link` or `st.switch_page` targets that don't match any registered page | Orphaned navigation — link to nowhere | Critical |
| `st.sidebar` with 10+ interactive widgets | Sidebar cognitive overload — too many controls (Miller 1956; Sweller extraneous load) | Medium |
| `st.metric(` with `delta` but no `delta_color` specification | Ambiguous delta direction — user must guess if up is good or bad (Norman Gulf of Evaluation; Kahneman Dual-Process — System 1 expects up = good) | Medium |
| `st.tabs(` with 6+ tabs | Tab overload — exceeds (Miller 1956 — working memory chunk limit) | Medium |

#### React / JSX patterns

| Pattern | Issue | Severity |
|---------|-------|----------|
| `window.confirm(` | Native confirm dialog — no custom styling, poor UX, breaks flow (Norman Gulf of Execution — dialog vocabulary may not match user intention) | Medium |
| `window.alert(` or `alert(` | Native alert — blocks thread, no structured error handling (Wood Layer 4: Identification; Gergle feedback interruption) | Medium |
| `onClick` on `<div>` or `<span>` without `role="button"` and `tabIndex` | Non-semantic interactive element — keyboard/screen reader inaccessible | High |
| `<img` without `alt` attribute | Missing image alt text — screen reader blind spot | High |
| Form `onSubmit` without corresponding loading/success/error state management | Missing form feedback | High |
| `useEffect(` with `fetch` / API call and no loading state | Data fetch without loading indicator | Medium |
| `dangerouslySetInnerHTML` | XSS risk AND potential layout surprise (cross-concern: security + cognitive) | Critical |
| `<button` with only an icon (no `aria-label` and no visible text) | Unlabeled action — user must guess the icon's meaning | High |
| `disabled={true}` without tooltip or explanation of why | Disabled control without explanation — user cannot learn requirement (Norman Gulf of Execution — user cannot determine how to enable the control) | Medium |

#### Gradio patterns

| Pattern | Issue | Severity |
|---------|-------|----------|
| `gr.Dropdown` with >100 choices and no `filterable=True` | Option overload without search — user must scroll through hundreds of items (Miller 1956; Hick's Law) | Medium |
| `fn=` callback with no corresponding `gr.update` or loading state | Missing processing feedback — user doesn't know computation is running | High |
| Multiple `gr.Tab` objects referencing the same function without distinguishing state | Shared state confusion — tabs appear independent but mutate shared state | High |
| `gr.Plot` or `gr.Image` without `label=` parameter | Unlabeled visualization — screen reader and cognitive accessibility gap | Medium |
| `gr.Blocks` with >6 `gr.Tab` children | Tab overload — exceeds (Miller 1956 — working memory chunk limit) | Medium |
| `gr.Markdown` with >3 paragraphs of instruction before first interactive element | Wall of text before action — users skip instructions and guess (Sweller extraneous load; Pirolli & Card — users skip dense text to follow action scent) | Medium |
| HF Space with `gr.Blocks` or `gr.Interface` on free-tier (zero-GPU or CPU) and no startup notification or cold-start warning | Cold-start container wake-up takes 30-60s with generic "Building" status — user has no ETA, no retry affordance, no explanation of why it's slow (Gergle — system state visibility; Norman Gulf of Evaluation) | Medium |

#### General UI patterns (any framework)

| Pattern | Issue | Severity |
|---------|-------|----------|
| Same action concept with different labels across files (e.g., "Save" / "Submit" / "Apply" / "Update" for the same operation type) | Inconsistent action vocabulary — violates GOMS selection rule consistency | High |
| Color-only status indicators (`color:` / `background:` with red/green/yellow but no text/icon status) | Color-only differentiation — fails for color-blind users (8% of males) (WCAG 1.4.1 Use of Color) | High |
| Perceptually non-uniform colormap (`cmap="jet"`, `"hot"`, `"rainbow"`, `"hsv"`, or custom `LinearSegmentedColormap` without perceptual validation) | Non-validated colormaps create false magnitude boundaries at hue transitions — viewers perceive artificial bands that do not exist in the data. Must use a ColorBrewer palette (Harrower & Brewer 2003), viridis family, or cividis. Grep: `cmap=["']?(jet\|hot\|rainbow\|hsv)` / `colorscale=["']?(Jet\|Hot\|Rainbow\|HSV)` | High |
| Hardcoded pixel-based layouts without responsive breakpoints | Fixed layout — breaks on different screen sizes (WCAG 1.4.10 Reflow) | Medium |
| `placeholder=` used as the only label for form inputs | Placeholder-as-label — disappears on focus, fails accessibility (WCAG 3.3.2 Labels; Nielsen Heuristic 6 Recognition over Recall) | High |
| Modal/dialog without visible close button or escape key handler | Trapped modal — no obvious exit (Wood Layer 6: Resumption failure) | Critical |
| `cursor: pointer` on non-interactive elements | False affordance — element looks clickable but isn't (Norman — perceived affordance mismatch) | Medium |
| Navigation menu items without visual indication of current page/section | Missing "you are here" indicator — user loses orientation (Nielsen Heuristic 1 Visibility of System Status; Pirolli & Card patch location) | High |
| Tooltip-only labels on primary actions (not supplementary information) | Essential information hidden behind hover — mobile-hostile, discoverable only by accident (Nielsen Heuristic 6 Recognition over Recall) | Medium |
| Numeric metric display without interpretive context (no delta, no reference value, no "good/bad" indication) | Metrics without context — user sees a number but cannot judge its meaning (Gulf of Evaluation) | High |
| Raw identifiers in progressive disclosure (expanders, accordions, "show more" sections) | Tables inside expanders/accordions are still user-facing — scan them for the same raw ID exposure, missing labels, and formatting issues as primary views. Progressive disclosure hides complexity, it does not make it invisible (Norman Gulf of Evaluation — the user still sees the output and must interpret it) | Medium |
| Counter-intuitive scale direction (lower value = more intense/better) without direction indicator | Scale direction mismatch — System 1 expects "higher = more" but metric inverts this (Dual-Process) | Medium |

For each finding: record file path, line number, pattern matched, severity, the Wood defense layer violated (if applicable), and whether it is a true positive or intentional usage.

**Output:** Anti-pattern findings table organized by framework with file paths, severity, and cognitive impact classification.

---

### Phase 1: Discovery (Both modes)

Explore the project to understand its cognitive interface surface:

- Read `CLAUDE.md`, `README.md`, and any design docs or wireframes
- Identify the UI tech stack (Streamlit, React, Vue, Angular, Gradio, HTML/CSS, etc.)
- Map the **cognitive surface**:
  - **Pages / screens**: List every distinct view the user encounters
  - **User types**: Who uses this interface? What is their expertise level? (kiosk/first-time, regular, power user)
  - **Core tasks**: What are the 3-5 things users primarily come to do?
  - **Task frequency**: Which tasks are performed daily vs weekly vs rarely?
  - **Decision points**: Where must users make choices? How many options at each point?
  - **Data density**: Which screens present the most information? How much data per viewport?
  - **Error-prone paths**: Which workflows are most likely to produce user errors? (complex, multi-step, irreversible)
  - **Navigation structure**: How do users move between screens? Linear, hub-and-spoke, free-form?
  - **Feedback mechanisms**: How does the system communicate success, failure, progress, and state changes?
  - **External dependencies**: Does the UI depend on external data, APIs, or other systems that introduce latency or failure modes?
  - **Collaborative features**: Do multiple users interact with the same data? (affects grounding requirements)
  - **Domain vocabulary**: What specialized terms does the interface use? Do they match the users' domain language?
  - **Multiple surfaces**: Does the project span multiple platforms (web app + mobile, main app + demo + documentation, HF Hub + Streamlit)? If so, map all surfaces and their roles — multi-surface coherence will be evaluated in Phase 8.
  - **Domain-specific cognitive demands**: Identify 3-5 cognitive demands unique to this domain (e.g., spatial reasoning for maps, statistical literacy for analytics, temporal reasoning for timelines). These inform what the interface must support beyond generic usability.
  - **Constraint landscape** (EID): What constraints determine data availability? (e.g., only certain competitions have tracking data, model outputs are scoped to training data). Map constraints that users need to understand to avoid false expectations. These are evaluated in Phase 6.

**Output:** Cognitive surface summary listing all pages, user types, core tasks, and identified risk areas for deeper analysis.

---

### Phase 2: Task Model Mapping (Both modes)

Apply GOMS-based analysis to decompose user tasks and identify where the interface's task structure diverges from users' mental models.

Load `templates/task-model-analysis.md` for the full GOMS methodology reference, user expertise spectrum guide, and task decomposition worksheet.

**Planning mode:** Design the task model before building:
- What are the user's top-level goals? (not features — goals)
- How does the user mentally decompose each goal into sub-tasks?
- What is the natural sequence of operations for each sub-task?
- Where do users have selection rules (multiple methods to achieve the same goal)?
- Which method should the interface make default? (frequency-based: most common method = easiest path)

**Audit mode:** Evaluate the existing task model:

| Check | What to look for | Severity if misaligned |
|-------|-----------------|----------------------|
| Goal-task alignment | Do page titles and section headers match user goals (not implementation concepts)? | High |
| Task decomposition match | Does the interface's step sequence match how users naturally think about the task? | Critical |
| Operation granularity | Are individual operations (clicks, selections, inputs) at the right level — not too atomic, not too bundled? | Medium |
| Selection rule clarity | When multiple paths exist, is the most common one most prominent? | High |
| Vocabulary alignment | Do labels, buttons, and headers use the user's domain language, not developer jargon? | High |
| Progressive complexity | Can novices complete core tasks without encountering power-user features? | High |
| Chunk boundaries | Are related operations grouped together? Do logical chunks fit within working memory (4 +/- 1 items per group)? (Cowan 2001, revising Miller 1956) | Medium |
| Interruption recovery | If the user is interrupted mid-task, can they resume without starting over? (Wood Layer 6: Resumption; GOMS resumption operators) | High |
| Global search | For systems with >5 distinct entities (players, products, documents), can users search by name instead of navigating filter cascades? (Pirolli & Card — filter cascades increase between-patch travel cost) | High |

#### Norman's Gulf Analysis

For each core task, evaluate the two structural gaps between user and interface (Norman 1988/2013):

| Gulf | Question | Narrow (good) | Wide (finding) |
|------|---------|---------------|----------------|
| **Execution** | Can the user express their intention using the available controls? | User's action maps directly to system action (search by name, click to view) | User must translate their goal through multiple indirections (select competition → select season → select team → find player) |
| **Evaluation** | Can the user understand the system's response? | System state is immediately interpretable ("Player A is 23% better than average") | User must translate system output to derive meaning ("cosine distance: 0.23" — is that good?) |

**Gulf width diagnostic:** If completing a core task requires >3 translation steps between user intent and interface action, the Gulf of Execution is too wide. If understanding a core output requires domain expertise the target user doesn't have, the Gulf of Evaluation is too wide.

Load `templates/task-model-analysis.md` for the full Norman's Gulf worksheet and cognitive walkthrough template.

#### Cognitive Walkthrough (critical tasks only)

For the top 2-3 most critical user tasks identified in Discovery, walk through the complete scenario step by step. Each walkthrough MUST include at least 5 steps with the 4-question protocol. At least one walkthrough MUST be from a kiosk/first-time user perspective. This catches **compound issues** — interaction effects between individually-acceptable design decisions that only emerge in sequence.

For each step, answer four questions:
1. Will the user know what to do? (Gulf of Execution)
2. Will they see the correct action is available?
3. Will they associate the correct action with their goal?
4. After performing the action, will they understand the feedback? (Gulf of Evaluation)

Record the walkthrough as:

| Step | User Goal | User Action | System Response | Gulf Issue (if any) |
|------|-----------|-------------|-----------------|---------------------|

#### User expertise spectrum

Every interface serves users across a spectrum. The audit must evaluate task model fit at each level:

| Level | Mental Model | GOMS Characteristics | Design Requirement |
|-------|-------------|---------------------|-------------------|
| **Kiosk / First-time** | No pre-existing model. Learning the system's vocabulary and structure | High operator count, no compiled methods, heavy reliance on visual search | Self-explanatory labels, guided workflows, minimal choices per step |
| **Regular** | Functional model. Knows the vocabulary and common paths | Methods forming, selection rules emerging, some compiled sequences | Consistent patterns that reinforce developing methods, predictable navigation |
| **Power user** | Expert model. Has compiled methods for all common tasks | Low operator count, fast selection rules, keyboard shortcuts, batch operations | Don't slow them down. Provide shortcuts, keyboard navigation, bulk actions, customizable defaults |

The interface must **degrade gracefully** across all three levels. A power-user shortcut must not confuse a first-timer. A first-timer's guided flow must not impede a power user.

#### Expert Blind Spot Audit

For each domain-specific metric or term displayed in the interface, complete this structured check:

| Metric/Term | Domain-Only User (no data science) | Data-Science-Only User (no domain) | Both Fail? | Required Fix |
|-------------|----|----|----|----|
| [metric] | Can interpret? Y/N | Can interpret? Y/N | If either N | Tooltip / inline explanation / contextual help |

If either audience cannot interpret a displayed metric, it requires at minimum: (1) a tooltip or inline explanation defining the term, (2) a reference value or interpretive label, or (3) a link to documentation. Metrics that fail for *both* audiences are Critical — they are opaque to everyone except the designer.

**Glossary completeness check (Hinds 1999 — Expert Blind Spot):** If the interface has a glossary or help system, cross-reference every unique metric label, chart axis label, and column header against the glossary index. Any displayed label without a corresponding glossary/tooltip entry is a gap — the help system exists but doesn't cover that term. An incomplete glossary is itself a blind spot: the designer assumed certain terms were obvious because they were obvious *to the designer*.

**Output:** Task model analysis for each core task, with expertise spectrum evaluation and identified misalignment points.

---

### Phase 3: Consistency & Convention (Audit mode)

Evaluate whether the interface uses the same patterns for the same operations, and leverages existing user knowledge (platform conventions, domain standards).

| Check | What to look for | Severity if violated |
|-------|-----------------|---------------------|
| Action vocabulary | Same operation uses the same label everywhere (not "Save" on one page and "Submit" on another) | High |
| Icon consistency | Same icon means the same thing everywhere. No icon used for two different actions | High |
| Layout patterns | Similar pages have similar layouts. Data tables, forms, and detail views follow the same template | Medium |
| Color semantics | Colors convey the same meaning everywhere (red = error/danger, green = success, etc.) | High |
| Data colour association consistency | When colour encodes data categories (not UI states), the same colour must represent the same category across all pages. Reusing the same colour for a different data category on a different page is worse than no colour at all — viewers carry learned associations between pages (Kirk Ch9: "Once a colour stands for something, preserve that association") | High |
| Interaction patterns | Same gesture/click pattern produces same type of result (e.g., clicking a row always opens detail) | High |
| Platform conventions | Interface follows platform norms (web: links are blue/underlined, buttons look clickable; mobile: swipe, pull-to-refresh) (Nielsen Heuristic 4 Consistency and Standards) | Medium |
| Domain conventions | Interface follows domain-specific conventions (e.g., in soccer analytics: pitch orientation, color coding by team, standard stat abbreviations) (Nielsen Heuristic 4; GOMS compiled methods from domain experience) | High |
| Error message format | All errors use the same structure (icon + message + recovery action) (Nielsen Heuristic 9; Wood Layer 4 Identification) | Medium |
| Loading patterns | Progress indication uses the same mechanism throughout (spinner, skeleton, progress bar) | Medium |
| Empty states | "No data" scenarios handled consistently across all views | Medium |
| Navigation patterns | Back/forward/breadcrumb behavior is predictable and consistent | High |
| Keyboard shortcuts | If shortcuts exist, they follow platform conventions (Ctrl+S = save, Escape = cancel/close) (Nielsen Heuristic 4; GOMS motor method transfer) | Medium |
| Partial pattern application | If a UX pattern (cross-page links, toast feedback, contextual help, academic citations) appears on some pages but not all equivalent pages, flag as a consistency finding (GOMS Selection Rules — users develop an expectation from the pages where the pattern exists, then that expectation is violated on the pages where it doesn't). A pattern on 3 of 11 pages is worse than no pattern | High |
| Sidebar spatial stability | Do sidebar controls remain stable, or do they appear/disappear based on main-area selections (e.g., radio button changes which sidebar widgets are visible)? Appearing/disappearing controls violate spatial stability and break developing motor patterns (Gestalt Common Fate) | High |

#### Gestalt perceptual checks

Apply Gestalt principles (Wertheimer 1923) as explicit consistency diagnostics. These principles describe how users *perceive* grouping and relationships — violations cause perceptual confusion independent of logical correctness.

| Principle | Audit Check | Violation Example | Severity |
|-----------|------------|-------------------|----------|
| **Proximity** | Are related controls physically grouped together? | Filter controls split between sidebar and main area for the same data view | High |
| **Similarity** | Do visually identical elements behave identically? | Two messages use the same `st.info` styling but one means "please select" and the other means "no data exists" | High |
| **Common Region** | Are related items enclosed in a shared container? | Tab content and its associated filters lack a shared visual boundary | Medium |
| **Figure-Ground** | Can the user distinguish interactive elements from background? | Low-contrast buttons or links that blend into surrounding text | Medium |
| **Continuity** | Do related items follow a visual flow? | Navigation items arranged in a way that breaks reading order | Low |

#### Ubiquitous language consistency (Evans)

When an application operates in a specialized domain (sports analytics, finance, healthcare, logistics), the same concept must use the same term everywhere — UI labels, code variable names, database column names, documentation, tooltips, and glossary entries. Inconsistent naming creates cognitive friction: the user must maintain a mental translation table between synonyms, which consumes working memory (Sweller Cognitive Load Theory — extraneous load from synonym resolution).

| Check | What to look for | Severity |
|-------|-----------------|----------|
| Cross-surface synonym detection | Does the same concept use different names across UI, code, database, and documentation? (e.g., "match" in UI, "game" in database, "fixture" in docs, "event" in code) Build a term concordance table mapping each domain concept to its name in each artifact layer | High |
| Metric label-to-column alignment | Do metric labels displayed to users match the column names in the underlying data model? Misalignment forces developers to maintain translation mappings and users to guess which data backs which label | Medium |
| Glossary completeness | If a glossary exists, does every domain-specific term in the UI appear in it? If no glossary exists and the domain has >10 specialized terms, flag the absence as a finding | Medium |
| Abbreviation consistency | Are abbreviations used consistently? (e.g., "xG" vs "Expected Goals" vs "expected_goals" — pick one canonical form and use it everywhere, with the full form in tooltips) | Medium |
| Documentation-UI vocabulary drift | Do README, architecture docs, and API docs use the same terms as the UI? Drift between documentation and interface confuses users who read docs before using the product | Medium |

**Term concordance table** (complete for every domain concept that appears in the UI):

| Domain Concept | UI Label | Code Variable | Database Column | Documentation | Glossary Entry | Consistent? |
|---------------|----------|---------------|-----------------|---------------|----------------|-------------|
| [concept] | [label] | [var name] | [column name] | [doc term] | [yes/no] | [yes/no] |

Flag any row where the terms are not consistent as a finding. Severity: High if the inconsistency spans UI-to-database (user sees one name, data uses another); Medium if it spans code-to-documentation only.

#### Grep patterns for consistency violations

| Pattern | What it catches |
|---------|-----------------|
| Multiple distinct `st.success(` / `st.error(` / `st.warning(` / `st.toast(` message formats across pages | Inconsistent feedback patterns |
| Varying `st.button(` labels for semantically equivalent actions across pages | Action vocabulary drift |
| Inconsistent `st.header` / `st.subheader` / `st.title` hierarchy across pages | Heading level inconsistency |
| Mix of `st.dataframe` and `st.table` for similar data displays | Display component inconsistency |
| Different date/number formatting across pages | Data formatting inconsistency |
| Same concept with different variable name prefixes across page state modules (e.g., `sm_xg` vs `pc_expected_goals`) | Ubiquitous language violation — synonym in code |
| Glossary or `help_text` that uses a different term than the metric label it describes | Glossary-UI vocabulary drift |

**Output:** Consistency findings table with pattern, locations, severity, and recommended standard.

---

### Phase 4: Error Tolerance (Both modes)

Evaluate every critical task path against Wood & Byrne's 7-layer defense framework. Classify error risks by Rasmussen's SRK level.

Load `templates/error-tolerance-checklist.md` for the full 7-layer framework reference, Rasmussen SRK classification guide, and Reason's error mechanism taxonomy.

**Planning mode:** Design error tolerance strategy:
- For each critical task, identify the most likely error classes (SRK level)
- Design defenses at each of the 7 layers
- Determine which errors are preventable by design constraints vs which need detection and recovery
- Plan the cost/benefit of each defense (some prevention measures add friction)

**Audit mode:** For each critical task path identified in Phase 2:

| Layer | Audit Question | What to check | Severity if missing |
|-------|---------------|---------------|---------------------|
| **1. Prevention** | Can this error class be eliminated by design constraints? | Input masks, disabled invalid options, type constraints, required fields, sane defaults | High |
| **2. Reduction** | Does the task model minimize opportunities for this error? | Step count minimization, progressive disclosure, smart defaults, auto-fill, disambiguation | Medium |
| **3. Detection** | Will the user notice something went wrong? | Inline validation, visual state changes, confirmation dialogs, diff views before commit | Critical |
| **4. Identification** | Can the user understand *what* went wrong? | Specific error messages (not "Something went wrong"), field-level validation, contextual help | High |
| **5. Correction** | Is fixing the error straightforward and discoverable? | Edit-in-place, undo button, "fix this" links, pre-populated correction forms | High |
| **6. Resumption** | Can the user return to their task without losing context? | State preservation after error, no page reload on validation failure, draft saving, back button works | High |
| **7. Mitigation** | When all else fails, is damage minimized? | Soft delete (trash), version history, audit trail, confirmation on irreversible actions | Critical for destructive paths |

#### Rasmussen SRK error classification

Different cognitive levels produce different error types requiring different defenses:

| SRK Level | Error Type | Example | Best Defense Layers |
|-----------|-----------|---------|---------------------|
| **Skill-based** (slips) | Correct intention, wrong execution. Habitual action fires incorrectly | Clicking "Delete" instead of adjacent "Edit" button | Prevention (spacing/grouping), Detection (confirm dialog) |
| **Rule-based** (mistakes) | Wrong rule selected for the situation. User applies a familiar procedure in the wrong context | Applying a filter meant for one data view to a different view because the UI looks similar | Reduction (visual differentiation), Identification (clear context labels) |
| **Knowledge-based** (errors) | Wrong mental model. User fundamentally misunderstands what the system does or how it works | User expects "Save" to publish immediately because that's how their previous tool worked | Prevention (explicit state labels), Detection (preview before publish) |

#### Reason's error mechanisms

Two mechanisms from Reason's taxonomy that Wood identified as particularly relevant to interface design:

- **Similarity matching** — A wrong-but-similar rule fires because the interface makes two different contexts look too similar. *Audit:* identify pages or workflows that look alike but behave differently.
- **Frequency gambling** — The most-used routine executes even when context demands otherwise. *Audit:* identify workflows where the most common action is also the most dangerous in certain contexts (e.g., "Confirm" button always means "proceed" except on one screen where it means "delete permanently").

**Output:** Error tolerance assessment per critical task path, with SRK classification, defense layer gaps, and recommended fixes.

---

### Phase 5: Cognitive Load Assessment (Both modes)

Evaluate information density, decision complexity, and working memory demands across all screens.

Load `templates/cognitive-load-assessment.md` for the full NASA-TLX scoring guide, Sweller's cognitive load taxonomy, and information density heuristics.

**Planning mode:** Design for minimal extraneous load:
- What is the intrinsic complexity of each task? (irreducible — determined by the domain)
- Where will extraneous load creep in? (reducible — determined by the design)
- How can germane load be maximized? (productive — schema building, pattern recognition)
- What progressive disclosure strategy will be used? (show complexity only when needed)

**Audit mode:** Score each screen against cognitive load indicators:

| Check | What to look for | Threshold | Severity if exceeded |
|-------|-----------------|-----------|---------------------|
| Interactive elements per viewport | Buttons, inputs, selectors, toggles visible without scrolling | >15 interactive elements (Sweller extraneous load) | High |
| Decision points per task | Choices the user must make to complete a single task | >5 sequential decisions (Sweller extraneous load; Hick's Law) | High |
| Information density | Distinct data points visible simultaneously | >30 distinct values per viewport (Sweller extraneous load) | Medium |
| Visual hierarchy levels | Number of distinct heading/text sizes used on one screen | >4 levels (Sweller extraneous load; Nielsen Heuristic 8) | Medium |
| Required recall | Information user must remember from a previous screen to complete current task | Any cross-screen recall without reference (Nielsen Heuristic 6 Recognition over Recall) | High |
| Simultaneous comparisons | Number of items user must compare at once | >7 items (Miller 1956) | Medium |
| Mode indicators | Number of active modes/states the user must track | >3 simultaneous modes (Sweller extraneous load) | High |
| Text density | Paragraph-length instructions or descriptions | >3 sentences of instruction per action (Sweller extraneous load; Pirolli & Card — users skip dense text) | Medium |
| Data table columns | Visible columns in a data table | >10 columns without horizontal scroll (Miller 1956; Sweller extraneous load) | Medium |
| Filter/parameter count | Number of filters or parameters visible simultaneously | >8 without grouping/progressive disclosure (Miller 1956; Sweller extraneous load) | Medium |

#### NASA-TLX dimensions (for manual assessment)

When deeper evaluation is warranted, score each critical workflow on 6 dimensions (1-20 scale):

| Dimension | Question | High Score Indicates |
|-----------|---------|---------------------|
| **Mental Demand** | How much thinking, deciding, calculating, remembering, searching was required? | Interface demands too much cognitive processing |
| **Physical Demand** | How much clicking, scrolling, typing, mouse movement was required? | Interface demands too much physical interaction |
| **Temporal Demand** | How much time pressure did you feel? Was the pace imposed by the system? | System creates artificial urgency or slowness |
| **Effort** | How hard did you have to work to accomplish your level of performance? | Task completion requires disproportionate effort |
| **Performance** | How successful were you in accomplishing what you were asked to do? | Users feel they failed or got a partial result |
| **Frustration** | How insecure, discouraged, irritated, stressed was the experience? | Interface creates negative emotional response |

#### Sweller's load taxonomy — design implications

| Load Type | Source | Design Goal |
|-----------|--------|-------------|
| **Intrinsic** | Inherent task complexity (domain-determined) | Cannot reduce — but can scaffold with progressive disclosure |
| **Extraneous** | Poor design (interface-determined) | **Eliminate.** This is the audit's primary target |
| **Germane** | Productive learning (schema-building) | **Maximize.** Consistent patterns help users build accurate mental models |

#### Dual-Process Theory (Kahneman)

Evaluate whether the interface engages System 2 (slow, deliberate, effortful) when System 1 (fast, intuitive, automatic) could suffice:

| Check | System 2 Overload Indicator | Fix (shift to System 1) | Severity |
|-------|----------------------------|-------------------------|----------|
| Numeric outputs without interpretive cues | User must calculate whether "0.23" is good or bad | Add color bands, verbal labels ("above average"), or reference values | High |
| Counter-intuitive scale direction | Lower value = more intense (e.g., PPDA), violating "higher = more" intuition | Add direction indicator (arrow, "lower is better" label) | Medium |
| Raw identifiers instead of names | User must mentally map IDs to meaningful entities | Show human-readable names; provide ID on demand | Medium |
| Derived values without showing derivation | User must trust an opaque calculation | Show formula, components, or "based on N matches" context | Medium |
| Multiple units mixed without conversion | User must mentally convert between unit systems | Normalize to one system or show both with clear labels | Medium |

#### Visual Encoding Effectiveness (Cleveland & McGill)

For data-heavy interfaces, evaluate whether each visualization uses the perceptually appropriate encoding for its data relationship. Cleveland & McGill (1984) established a ranking of visual encodings by perceptual accuracy:

| Rank | Encoding | Best For | Common Misuse |
|------|----------|----------|---------------|
| 1 | Position along common scale | Quantity comparison | — (most accurate) |
| 2 | Position along non-aligned scales | Comparison with offset context | — |
| 3 | Length | Magnitude comparison (bar charts) | Stacked bars where inner segments are hard to compare |
| 4 | Angle / slope | Trends over time (line charts) | Radar/spider charts for precise comparison — angle encoding distorts perception |
| 5 | Area | Approximate magnitude (treemaps, bubbles) | Pie charts — area + angle combination is perceptually poor |
| 6 | Color saturation / hue | Categories or continuous spatial fields | Using color for quantitative comparison (hard to rank shades) |

**Common violations to flag:**
- Multiple metrics with incompatible scales on a shared axis (normalizing would fix)
- Radar/spider charts used for precise comparison (parallel coordinates or grouped bar charts are perceptually superior)
- Color as the sole differentiator for quantitative data (add text labels or position encoding)
- 3D effects that add no informational dimension

#### Chart Scalability / Degradation

For charts that render variable-length data, evaluate whether the encoding degrades gracefully as item count increases:

| Check | What to look for | Threshold | Severity |
|-------|-----------------|-----------|----------|
| Grouped bar chart readability | Do individual bars remain distinguishable as groups increase? | >8 groups: bars become slivers, labels overlap (Cleveland & McGill — length encoding degrades with density) | Medium |
| Legend overflow | Does the legend remain readable as series count increases? | >5 legend items: consider inline labels or small multiples (Cleveland & McGill — color hue encoding limit; Miller 1956) | Medium |
| Pie/donut chart slicing | Do small slices remain perceptible? | >5 categories: switch to horizontal bar chart (Cleveland & McGill — angle + area encoding ranks 4-5) | Medium |
| Scatter plot overplotting | Do points remain distinguishable as data density increases? | >100 points in view: add opacity, jitter, or density contours (Cleveland & McGill — position encoding degrades under overplotting) | Low |
| Label collision | Do axis labels, data labels, or annotations overlap at scale? | Any overlap at expected data volumes (Cleveland & McGill — position encoding unreliable when labels occlude data) | Medium |

Load `templates/cognitive-load-assessment.md` for the full Dual-Process and Cleveland & McGill reference with additional examples.

**Output:** Cognitive load assessment per screen with dimension scores, threshold violations, and extraneous load reduction recommendations.

---

### Phase 6: Visual Grounding, Feedback & Interpretation (Audit mode)

Evaluate whether the interface provides sufficient visual grounding for situation awareness, efficient task completion, and result interpretation. This phase distinguishes two cognitive processes:

- **Feedback** (Gergle): "Is the system working? What state is it in?" — mechanical grounding
- **Interpretation** (Norman's Gulf of Evaluation + Trust Calibration): "What does this result mean? Can I trust it?" — semantic grounding

Load `templates/visual-grounding-checklist.md` for the full Gergle grounding theory reference, feedback latency thresholds, Joint Action Storyboard methodology, and trust calibration checklist.

#### Feedback checks (Gergle)

| Check | What to look for | Severity if missing |
|-------|-----------------|---------------------|
| System state visibility | Can the user tell what state the system is in at a glance? (loading, ready, error, empty, filtered) | Critical |
| Action feedback | Every user action produces visible feedback within 100ms (click acknowledgment) and meaningful feedback within 1000ms (result or progress) | High |
| Progress indication | Operations >1 second show progress; operations >10 seconds show estimated time or percentage | High |
| State change visibility | When data changes, is the change visually highlighted? (not just silently updated) | Medium |
| Context preservation | After an action, does the user maintain their visual context? (no unexpected scroll jumps, page reloads, or focus changes) | High |
| Spatial stability | Do UI elements stay in the same position? Moving targets cause motor errors and disorientation | High |
| Error visibility | Error states are visually distinct from normal states — not just a small text change | High |
| Filter/selection visibility | Active filters and selections are always visible — user knows what subset of data they're seeing | Critical |
| Undo visibility | If undo is available, the affordance is visible immediately after the action (not buried in a menu) | Medium |
| Empty state messaging | When no data matches, the screen explains why and suggests next steps (not just a blank area) | High |
| Data freshness | If data can be stale, the last-updated timestamp is visible | Medium |
| Collaborative awareness | In multi-user contexts: who else is viewing/editing? Are changes by others visible in real-time? | High (if collaborative) |

#### Interpretation checks (Norman + Lee & See)

These checks evaluate whether users can *understand* and *trust* what the interface shows them — the Gulf of Evaluation:

| Check | What to look for | Severity if missing |
|-------|-----------------|---------------------|
| Result interpretability | Can the user understand what a displayed value means without external reference? | High |
| Calibration anchors | Are reference points provided for numeric outputs (e.g., "league average: 0.45", percentile rank)? | High |
| Data coverage visibility | Does the user know what subset of the data universe they're seeing (e.g., "3 of 5 competitions loaded")? | Medium |
| Scope indicators | Are aggregation boundaries clear (per-match vs per-season vs career)? | Medium |

#### Constraint visibility (EID — Vicente & Rasmussen)

Ecological Interface Design argues that users need to see the work domain's constraints, not just the system's controls. When constraints are invisible, users form incorrect mental models of what the data represents.

| Check | What to look for | Severity if missing |
|-------|-----------------|---------------------|
| Data coverage explanation | Does the interface explain *why* certain data/options are unavailable? (e.g., "Tracking data available for 20 of 380 matches" vs silently showing only 20) | High |
| Relationship visibility | Can users see how displayed metrics relate to each other without visiting multiple pages? (e.g., high VAEP correlation with DEFCON pressure) | Medium |
| Means-ends traceability | Can users trace from outcome to cause through the interface? (e.g., match result ← tactical pattern ← player movement) | Medium |
| Boundary explanation | When filtered/aggregated data shows unexpected results, does the interface explain the boundaries? (e.g., "Competition average based on 5 Bundesliga matches only") | High |
| Absence visibility | Are important absences surfaced? (e.g., "No 360 freeze frames for this competition" rather than silently hiding the pitch control page) | Medium |

#### Trust calibration (for model/ML interfaces)

If the interface displays model-derived outputs (predictions, embeddings, similarity scores, recommendations, computed metrics), evaluate trust calibration (Lee & See 2004):

| Check | What to look for | Severity if missing |
|-------|-----------------|---------------------|
| Model provenance | Can the user tell which model/algorithm produced this output? | Medium |
| Uncertainty indication | Does the output show confidence bounds, ranges, or uncertainty? | High |
| Sample size context | Does the user know how much data informs this output (e.g., "based on 23 matches")? | High |
| Limitation visibility | Are known model limitations surfaced near the output? | Medium |
| Calibration anchors | Are reference points provided (e.g., "average player similarity: 0.45")? | High |
| Appropriate trust | Can the user develop neither too much trust (blind acceptance) nor too little (ignoring valid outputs)? | High |

**Skip this section** for interfaces that display only user-entered data or simple lookups with no model/algorithm layer.

#### Feedback latency thresholds (Card, Moran & Newell 1983 Model Human Processor; cited via Nielsen)

| Threshold | User Perception | Design Requirement |
|-----------|----------------|-------------------|
| **<100ms** | Instantaneous | Direct manipulation feedback (button press, hover, toggle) |
| **100ms-1s** | System is working | Show acknowledgment (button state change, spinner start) |
| **1s-10s** | Noticeable delay | Show progress indicator (spinner, progress bar) |
| **>10s** | System might be broken | Show progress percentage, estimated time, or allow background processing with notification |

#### Joint Action Storyboard analysis

For complex multi-step workflows, apply Gergle's Joint Action Storyboard framework:

1. Map each step of the workflow as a panel in the storyboard
2. For each panel, identify the **grounding cost** — what cognitive work must the user do to understand the current state and determine their next action?
3. Flag panels where grounding cost is high: the user must remember information from previous panels, infer hidden state, or interpret ambiguous feedback
4. Reduce grounding cost by adding visual anchors: persistent state indicators, breadcrumbs, progress visualization, contextual summaries

**Output:** Visual grounding findings with feedback latency analysis, grounding cost hotspots, and recommended visual anchors.

#### Data visualization integrity (Kirk; Cleveland & McGill)

When the interface displays data through charts, graphs, or visual encodings, evaluate whether the visual representation is truthful and effective. Kirk's three principles (Trustworthy > Accessible > Elegant) parallel this skill's existing priority ordering. These checks apply to any chart, graph, or data-driven visual element in the interface.

| Check | What to look for | Source | Severity |
|-------|-----------------|--------|----------|
| Bar/area chart zero-baseline | Quantitative axis on bar charts and area charts must start at zero. Truncation distorts perceived proportional size — a bar twice as tall must represent twice the value | Kirk Principle 1 (Trustworthy); Cleveland & McGill 1984 | High |
| Shape sizing method | Bubble, circle, and proportional-shape charts must size marks by **area**, not diameter or radius. Diameter sizing inflates perceived differences by the square (a value 2× larger appears 4× larger) | Kirk Ch6; Stevens' Power Law | High |
| Chart-question alignment | Can the designer articulate "what question does this chart answer?" as a title or statement? Charts without an editorial purpose are visual noise | Kirk Ch5 (Editorial Thinking — Angle) | Medium |
| Data colour consistency | Same colour must represent the same data category across all charts on all pages. Reusing a colour for a different data association without re-explanation forces mental translation (extraneous load) | Kirk Ch9; Sweller CLT | High |
| Categorical palette limit | Nominal colour palettes exceeding ~12 distinct hues destroy legibility — viewers cannot reliably distinguish associations beyond this threshold | Kirk Ch9; Ware 2013 | Medium |
| Quantitative encoding method | Quantitative gradients should use lightness variation (light-to-dark of a single hue), not hue variation. Hue is a categorical attribute — using it for magnitude creates false perceptual ordering | Kirk Ch6 (Mackinlay ranking); Cleveland & McGill 1984 | Medium |
| Label overload | Charts carrying both axis scales AND direct value labels create redundant encoding that competes for attention. Use one method, or justify dual encoding for accessibility (redundant encoding for vision-impaired users) | Kirk Ch8 (Annotation) | Low |
| Annotation sufficiency | Charts missing axis titles, legends, or data source attribution impede the perceiving phase — viewers cannot decode what they see. Check: titles present? axes labelled? colour legend included? data source cited? | Kirk Ch8; this phase's existing "Result interpretability" check | High |
| Pie chart integrity | Pie chart sectors must sum to exactly 100% with mutually exclusive categories. Violation is a mathematical trust failure, not a stylistic preference | Kirk Ch6 | High |
| Diverging scale symmetry | Diverging colour scales must have symmetric lightness increments on both sides of the breakpoint. Asymmetric scales create false perceived bias toward one end | Kirk Ch9 | Medium |
| Editorial focus hierarchy | "If everything shouts, nothing is heard" (Kirk). Are editorially important data points visually distinguished from context via colour, size, or annotation? Equal visual weight across all elements = no hierarchy | Kirk Ch5 (Focus); Gestalt Figure-Ground | Medium |
| Colormap provenance | Continuous, sequential, and diverging colormaps must use a scientifically validated palette: **ColorBrewer** (Harrower & Brewer 2003), **viridis/magma/plasma/inferno** (matplotlib perceptually uniform), or **cividis** (colorblind-optimised). Non-validated colormaps (`hot`, `jet`, `rainbow`, `hsv`, custom `LinearSegmentedColormap` without perceptual audit) have irregular lightness gradients that create false magnitude boundaries and fail under colour-vision deficiency. Grep for `cmap=` / `colorscale=` / `color_continuous_scale=` and check each value against the validated allowlist | Kirk Ch9; Harrower & Brewer 2003 | High |
| Diverging colormap CVD safety | Diverging colormaps must pass ColorBrewer's colorblind filter. Three ColorBrewer diverging palettes — `RdYlGn`, `RdGy`, `Spectral` — fail under deuteranopia/protanopia because the green-red or grey-red endpoints collapse to near-identical perceived lightness. Safe diverging palettes: `RdBu`, `PiYG`, `PRGn`, `PuOr`, `BrBG`, `RdYlBu` | Kirk Ch9; Olson & Brewer 1997 | Medium |

**Practitioner note — two-tier colour enforcement:** Colormaps (continuous scales encoding magnitude) and semantic constants (discrete named colours encoding categories) require different validation approaches. Colormaps must be from a validated palette because perceptual uniformity across the gradient is non-negotiable — no human review can verify that 256 interpolated steps are evenly spaced in perception. Semantic constants (e.g., home/away team colours, credit category colours) can be custom-chosen for domain meaning and dark-theme contrast, but must pass a programmatic CVD distinguishability check (see Phase 7, "Semantic colour set CVD distinguishability"). This two-tier approach avoids forcing domain-meaningful colours into ColorBrewer's limited qualitative offering (only 3 of 8 qualitative palettes pass colorblind filter at 3+ classes) while still guaranteeing accessibility.

**Output:** Data visualization integrity findings with Kirk principle references, file paths, and remediation guidance.

---

### Phase 7: Accessibility & Inclusion (Audit mode)

Evaluate whether the interface is usable by people with different abilities, demographics, and devices.

Load `templates/accessibility-inclusion.md` for the full WCAG 2.1 AA checklist, demographic bias patterns, and assistive technology compatibility checks.

| Check | What to look for | Severity if missing |
|-------|-----------------|---------------------|
| Keyboard navigation | All interactive elements reachable and operable via keyboard (Tab, Enter, Escape, Arrow keys) (WCAG 2.1.1) | Critical |
| Focus indicators | Visible focus ring on all interactive elements when navigating by keyboard (WCAG 2.4.7) | High |
| Screen reader compatibility | All content has semantic HTML structure; images have alt text; form inputs have labels; ARIA roles where needed | High |
| Color contrast | Text meets WCAG AA contrast ratios (4.5:1 normal text, 3:1 large text) | High |
| Color-only indicators | No information conveyed by color alone — always paired with text, icon, or pattern | High |
| Red-green data opposition | Red-green pairings as the sole distinguisher for meaning-bearing data categories (beyond UI states) are a deuteranopia accessibility failure — ~5% of population affected. Substitute with blue-orange, purple-green, or Kirk's tested alternatives (deep pink / lime green) | Kirk Ch9; WCAG 1.4.1 | High |
| Redundant data encoding | When colour carries data meaning in charts, a secondary attribute (texture, symbol, positional grouping) should encode the same distinction for colour-deficient viewers | Kirk Ch9; WCAG 1.4.1 | Medium |
| Semantic colour set CVD distinguishability | When a page defines categorical semantic colours not drawn from a named colorblind-safe palette (e.g., custom hex constants for team colours, credit categories, action types), validate that all pairwise combinations remain perceptually distinguishable under deuteranopia and protanopia simulation. Programmatic check: simulate CVD via `colorspacious` (Python) or Chrome DevTools `Emulation.setEmulatedVisionDeficiency`, compute CIEDE2000 ΔE between all pairs — threshold ΔE > 20 for reliable discrimination. This validates the actual perceptual property (distinguishability) rather than palette membership, allowing domain-meaningful custom colours while guaranteeing accessibility. See Phase 6 practitioner note on two-tier colour enforcement | Olson & Brewer 1997; Kirk Ch9; WCAG 1.4.1 | Medium |
| Responsive layout | Interface functions on screen widths from 320px to 4K (WCAG 1.4.10) | Medium |
| Touch targets | Interactive elements are at least 44x44px on touch devices (WCAG 2.5.5 Level AAA; Apple HIG — widely adopted as AA best practice) | Medium |
| Text scaling | Interface remains usable at 200% browser zoom (WCAG 1.4.4) | Medium |
| Reduced motion | Respects `prefers-reduced-motion` — no essential information conveyed only through animation (WCAG 2.3.3 Level AAA — widely adopted as AA best practice) | Medium |
| Language clarity | Instructions use plain language; jargon is defined or has tooltips; reading level appropriate for audience (WCAG 3.1.5; Hinds 1999 Expert Blind Spot) | Medium |
| Glossary / help system | For interfaces using 3+ domain-specific terms (e.g., xG, VAEP, DEFCON, cosine distance), is there a glossary, tooltip system, or contextual help? Absence forces users to seek external documentation (high between-patch cost) | Medium (High for kiosk users) |
| Context-sensitive help | If a glossary or help panel exists, does it filter to terms relevant to the current page/view? A static glossary showing ALL terms on every page adds extraneous cognitive load (Sweller) — users must scan past irrelevant definitions to find what they need | Medium |
| Error messages | Errors are announced to screen readers (via `aria-live` or equivalent) | High |
| Time limits | If the interface has timeouts, users can extend or disable them (WCAG 2.2.1) | High |
| Demographic bias | Data visualizations don't embed bias (e.g., gendered defaults, culturally specific color meanings, age-biased interaction patterns) (Friedman et al. Value-Sensitive Design) | Medium |

#### Automated checks (grep-detectable)

| Pattern | Framework | Issue |
|---------|-----------|-------|
| `<img` without `alt=` | HTML/JSX | Missing alt text |
| `<input` without `<label` or `aria-label` | HTML/JSX | Unlabeled form field |
| `<div` or `<span` with `onClick` but no `role` / `tabIndex` | React/JSX | Non-semantic interactive element |
| `color:` with red/green/yellow as sole differentiator (no accompanying text or icon) | CSS | Color-only status indicator |
| `cmap=["']?(jet\|hot\|rainbow\|hsv)` or `colorscale=["']?(Jet\|Hot\|Rainbow\|HSV)` | Python/JS | Perceptually non-uniform colormap — false magnitude boundaries and colorblind failure (Harrower & Brewer 2003) |
| `outline: none` or `outline: 0` on focusable elements | CSS | Removed focus indicator |
| `user-select: none` on text content | CSS | Prevents text selection (assistive technology) |
| `tabindex="-1"` on interactive elements | HTML | Removed from keyboard tab order |
| `aria-hidden="true"` on content with visible text | HTML | Screen reader content hidden |

**Output:** Accessibility findings with WCAG criteria references, automated check results, and remediation steps.

---

### Phase 8: Information Architecture (Audit mode)

Evaluate the navigation structure, error recovery paths, and overall information organization.

| Check | What to look for | Severity if missing |
|-------|-----------------|---------------------|
| Navigation coherence | Every page is reachable from the main navigation. No orphan pages (Nielsen Heuristic 3; Pirolli & Card — dead-end patches) | High |
| Breadcrumb / location | User always knows where they are in the hierarchy (Nielsen Heuristic 1; Pirolli & Card patch location) | High |
| Back button behavior | Browser back button works as expected (no broken history states) (Nielsen Heuristic 3 User Control and Freedom) | Critical |
| Deep linking | Key views can be bookmarked and shared via URL (Pirolli & Card — bookmarks reduce between-patch cost) | Medium |
| Search / find | For interfaces with >10 pages or >100 items, search functionality exists (Pirolli & Card — direct access vs navigation foraging) | Medium |
| Progressive disclosure | Complex features are hidden behind expandable sections, not visible by default | Medium |
| Error recovery navigation | After an error, the user can navigate away and return without data loss (Wood Layer 6 Resumption) | High |
| Cross-reference links | Related information is linked (e.g., from a player stats page to that player's match history) (Pirolli & Card — within-patch scent trails) | Medium |
| Consistent hierarchy | Same number of clicks to reach equivalent-importance pages (GOMS — operator count parity for equivalent goals) | Medium |
| URL structure | URLs are human-readable and reflect the navigation hierarchy | Low |
| Help discoverability | Help, documentation, or tooltips are findable when the user is confused (Nielsen Heuristic 10; Pirolli & Card scent) | Medium |
| Onboarding | First-time users have a clear starting point (not a blank screen with too many options) (GOMS — kiosk user has no compiled methods; Nielsen Heuristic 7) | High |
| Onboarding discoverability | Is onboarding accessible from ALL entry points, not just the default landing page? Users arrive via bookmarks, shared links, or external search — if onboarding is only on the home page, most users never see it (Pirolli & Card Information Foraging — users who enter via a non-default patch have zero scent trail to the onboarding content) | High |

#### Information Scent (Pirolli & Card)

Navigation labels are not just organizational — they are *scent cues* that predict whether the user's goal lies behind that link. Weak scent causes wrong choices, backtracking, and abandonment.

| Check | What to look for | Severity |
|-------|-----------------|----------|
| Label-goal alignment | Does each navigation label use the user's goal vocabulary, not the developer's implementation vocabulary? (e.g., "Player Valuation" vs "Action Values") | High |
| Scent strength | Would the target user predict the content behind this label? Would they choose it from a list of alternatives? | High |
| Per-label scent scoring | Score every navigation label using the table below. Labels scoring "Weak" are findings | High |
| Scent continuity | Does each page provide scent trails (links, "see also", related pages) to logically adjacent content? | Medium |
| Between-patch cost | How many clicks and re-entries are required to move between related content on different pages? | Medium |

**Per-label scent scoring table** (complete for every top-level navigation item):

| Navigation Label | Target User Goal | Scent Strength | Issue (if Weak/Medium) |
|-----------------|------------------|----------------|------------------------|
| [label] | [what goal does the user expect this leads to?] | Strong / Medium / Weak | [why the label fails to predict content] |

Labels that use implementation vocabulary ("Action Values"), abbreviations ("Def. Pressure"), or domain jargon without context ("DEFCON") score Weak for kiosk users. Goal-oriented labels ("Compare Players", "Match Timeline") score Strong.

#### Navigation anti-patterns

| Pattern | Issue | Severity |
|---------|-------|----------|
| Hidden hamburger menu as only navigation on desktop | Desktop users expect visible navigation — hamburger is a mobile convention (Nielsen Heuristic 4 — hamburger is mobile convention) | Medium |
| More than 3 levels of nested navigation | Users lose orientation beyond 3 levels (Miller 1956 — path depth exceeds chunk capacity) | High |
| Navigation labels that are ambiguous without context (e.g., "Overview", "Details", "More") | Labels must be self-describing — user shouldn't need to click to understand (Pirolli & Card — zero information scent) | Medium |
| Pagination without alternative (no "show all" or "jump to page" option) | Users scanning for specific items are forced to page through sequentially (Pirolli & Card — forced sequential scanning increases cost) | Low |
| Tab-based navigation with dependent state (selecting Tab A changes what Tab B shows) | Hidden state coupling — user doesn't expect tab selection to affect other tabs (Gestalt Common Region — tabs perceived as independent) | High |

#### Multi-Surface Coherence (if applicable)

**Skip this section** if the project has only one user-facing surface.

If the project spans multiple user-facing surfaces (web app + mobile, main app + demo, app + documentation site, app + HF Hub artifacts), evaluate the coherence of the *ecosystem* using Hutchins' Distributed Cognition framework (1995):

| Check | What to look for | Severity if missing |
|-------|-----------------|---------------------|
| Role declaration | Does each surface explicitly explain its role and relationship to other surfaces? ("This is a lightweight demo — for full analysis, visit the main app") | High |
| Cross-linking | Can users navigate between surfaces? Is linking bidirectional? | High |
| Visual identity coherence | Do surfaces share enough visual identity (branding, color scheme, typography) that users recognize them as part of the same ecosystem? Three unrelated themes signals three unrelated products | Medium |
| Capability communication | Does each surface make clear what it can/cannot do vs other surfaces? Can users tell which surface has which data scope? | High |
| Inter-surface memory | Can users carry context (selections, filters, findings) between surfaces, or must they re-enter everything? | Medium |
| Vocabulary alignment | Do all surfaces use the same terms for the same concepts? | High |
| Capability confusion | Would a user who discovers the ecosystem through Surface B (e.g., HF Space demo) understand what Surface A (e.g., main Streamlit app) adds? | High |

**Distributed Cognition gap analysis:** For each pair of surfaces, identify: (1) what cognitive work the user must do to bridge between them, (2) what information is lost in the transition, and (3) whether the transition is discoverable or requires external knowledge.

**Output:** Information architecture findings with navigation map, identified dead ends, and restructuring recommendations.

---

### Phase 9: Findings Report (Both modes)

Generate the final report. The format depends on the mode.

#### Planning mode report

Present the task model design and cognitive interface strategy:

```markdown
## Cognitive Interface Strategy — [System Name]

### Cognitive Surface Summary
- Pages/screens: [count and list]
- User types: [kiosk/regular/power user breakdown]
- Core tasks: [3-5 primary user goals]
- Task frequency: [daily/weekly/rare distribution]
- Identified risk areas: [high complexity, error-prone, high data density]

### Task Model Design
| Goal | Sub-tasks | Operations | Default Method | Expert Shortcut |
|------|-----------|------------|----------------|-----------------|
| [User goal] | [Decomposition] | [Clicks/inputs] | [Primary path] | [Power user path] |

### Error Tolerance Strategy
| Critical Task | Most Likely Error (SRK) | Prevention | Detection | Recovery |
|--------------|------------------------|------------|-----------|----------|
| [Task name] | [Skill/Rule/Knowledge] | [Design constraint] | [Feedback mechanism] | [Undo/fix path] |

### Cognitive Load Budget
| Screen | Intrinsic Load | Extraneous Load Sources | Progressive Disclosure Plan |
|--------|---------------|------------------------|----------------------------|
| [Page] | [Inherent complexity] | [Design-added friction] | [What to hide by default] |

### Design Recommendations
| # | Area | Recommendation | Priority | Framework |
|---|------|----------------|----------|-----------|
| 1 | Task Model | [Specific recommendation] | Critical | GOMS |
| 2 | Error Tolerance | [Specific recommendation] | High | Wood 7-layer |

### Interface Design Checklist
- [ ] Task models designed for all core user goals
- [ ] User expertise spectrum considered (kiosk to power user)
- [ ] Error tolerance strategy for each critical task path
- [ ] Cognitive load budget per screen
- [ ] Consistency standards defined (vocabulary, layout, feedback)
- [ ] Visual grounding requirements specified (feedback latency, state visibility)
- [ ] Accessibility requirements defined (WCAG AA minimum)
- [ ] Information architecture designed with navigation map
```

#### Audit mode report

Present concrete findings with cognitive impact assessment:

```markdown
## Cognitive Interface Audit Report — [System Name]

### Executive Summary
- Total findings: X
- Critical: X (Y instances) | High: X | Medium: X | Low: X
- Fixed during audit: X
- Remaining: X
- Primary cognitive risk: [summary of biggest user-facing issue]

> **Counting rule:** When multiple phase-level findings consolidate into fewer root-cause findings, the summary MUST show both counts — e.g., "Critical: 2 findings (6 instances)". The reader will encounter the instance-level detail first (Phase 0 tables) before reaching the consolidated view (Phase 9). Stating only the consolidated count creates a Gulf of Evaluation: the reader counts N severity rows in a table and cannot reconcile with a smaller summary number. This is exactly the kind of System 1 / System 2 conflict this skill audits for.

### Findings
| # | Severity | Phase | File:Line | Description | Framework | Status |
|---|----------|-------|-----------|-------------|-----------|--------|
| 1 | Critical | Phase 4 | pages/edit.py:42 | Destructive action without confirmation — no Prevention or Detection layer | Wood L1/L3 | Fixed |
| 2 | High | Phase 2 | pages/search.py:18 | Search workflow requires 6 sequential decisions — exceeds cognitive load threshold | NASA-TLX | Recommended |

> **Schema note:** The base columns (#, Severity, Phase, File:Line, Description, Status) are shared across all audit skills. The Framework column is specific to cognitive-interface-audit and documentation-audit.

### Task Model Assessment
| Core Task | Model Alignment | Expertise Coverage | Issues |
|-----------|----------------|-------------------|--------|
| [Task] | Aligned / Misaligned | Kiosk: Y/N, Regular: Y/N, Power: Y/N | [Summary] |

### Error Tolerance Coverage
| Critical Task | L1 | L2 | L3 | L4 | L5 | L6 | L7 | SRK Level |
|--------------|----|----|----|----|----|----|----|-----------|
| [Task] | [tick/gap] per layer | | | | | | | [S/R/K] |

### Cognitive Load Heatmap
| Screen | Elements | Decisions | Data Points | Load Rating |
|--------|----------|-----------|-------------|-------------|
| [Page] | [count] | [count] | [count] | Low/Medium/High/Critical |

### NASA-TLX Scores (critical workflows)
| Workflow | Mental | Physical | Temporal | Effort | Performance | Frustration | Average |
|----------|--------|----------|----------|--------|-------------|-------------|---------|
| [Task] | [1-20] | [1-20] | [1-20] | [1-20] | [1-20] | [1-20] | [avg] |

### Multi-Surface Coherence (if applicable)
| Surface | Role | Cross-Links | Visual Identity | Issues |
|---------|------|-------------|-----------------|--------|
| [Surface] | [Primary/Demo/Docs] | [To/From which surfaces] | [Consistent/Divergent] | [Summary] |

### Phase Coverage Matrix
| Phase | Checks Run | Findings | Key Result |
|-------|-----------|----------|------------|
| Phase 0: Anti-Patterns | [X patterns scanned] | [Y findings] | [summary] |
| Phase 1: Discovery | [X surfaces mapped] | [Y risk areas] | [summary] |
| Phase 2: Task Model | [X tasks analyzed] | [Y misalignments] | [summary] |
| Phase 3: Consistency | [X checks] | [Y violations] | [summary] |
| Phase 4: Error Tolerance | [X task paths x 7 layers] | [Y gaps] | [summary] |
| Phase 5: Cognitive Load | [X screens scored] | [Y overloaded] | [summary] |
| Phase 6: Visual Grounding | [X checks] | [Y findings] | [summary] |
| Phase 7: Accessibility | [X checks] | [Y findings] | [summary] |
| Phase 8: Info Architecture | [X checks] | [Y findings] | [summary] |

### Cognitive Interface Maturity Rating
- **Checks passed**: X/Y (Z% coverage)
- **Overall**: [Excellent / Good / Needs Work / Critical Gaps]
- **Strongest area**: [phase/area]
- **Weakest area**: [phase/area]

### Ready for users: Yes / No (with blockers)
```

---

## Important rules

- **Fix as you go.** Don't just report — remediate. Fix Critical and High issues during the audit.
- **Evidence-based claims.** Every finding must include file path, line number, or specific evidence. Never say "users probably find this confusing" without identifying the specific cognitive mechanism (SRK level, defense layer, load type).
- **User-centered, not developer-centered.** Evaluate the interface from the user's perspective, not the developer's. "It works" is not the same as "users can complete their task efficiently and without errors."
- **Expertise spectrum awareness.** Every task model finding must consider the full spectrum (kiosk to power user). A feature that delights power users may paralyze first-timers.
- **Framework attribution.** Each finding should reference the specific framework that identifies it (GOMS, Wood 7-layer, NASA-TLX, Gergle grounding). This is what distinguishes a cognitive audit from generic UX feedback.
- **Quantify cognitive cost.** Where possible, count: elements per viewport, decisions per task, steps to recover from an error, milliseconds of feedback delay. Numbers are more actionable than "this feels heavy."
- **No assumptions.** Read the actual UI code. Render pages if possible. Don't assume the interface works well because the framework has good defaults.
- **Respect the design intent.** If a design choice is intentional (e.g., data density is high because users are analysts who need it), note it and evaluate whether the density is *managed* (progressive disclosure, filters, good hierarchy) rather than flagging density itself as a problem.
- **Scope awareness.** Don't flag framework-managed UX as a finding (e.g., Streamlit's built-in error handling, React's form state management) unless the developer has overridden it poorly.
- **Prioritize.** Fix Critical and High findings. Track Medium and Low in the backlog. A perfect Phase 7 (accessibility) doesn't matter if Phase 2 (task model) has Critical misalignments.
- **The interface should be invisible.** The best outcome of this audit is that users complete tasks without thinking about the interface at all. Every finding should point toward that goal.
- **Report self-consistency (eat your own dog food).** The audit report is itself an interface — it has readers, mental models, and Gulfs of Evaluation. Before finalizing, verify: (1) every count in the Executive Summary is reconcilable with the detailed tables the reader encounters first, (2) severity labels in phase tables match their consolidated severity in the findings table (or escalation is explicitly noted), (3) no number requires the reader to "just trust the author's grouping logic" without explanation. If the report would fail its own Phase 5 (Dual-Process) or Phase 3 (Consistency) checks, fix it.
