# Task Model Analysis

## Purpose

Answer: "Does the interface's task structure match how users actually think about their tasks?"

## Pre-audit checklist

Before auditing, identify:

- [ ] The 3-5 primary user tasks this interface supports
- [ ] The user expertise spectrum (novice to expert) for each task
- [ ] Which tasks are performed frequently vs. rarely
- [ ] Any task sequences that require cross-screen coordination
- [ ] The current error rate or user complaint patterns (if available)

## GOMS Framework Reference

GOMS (Goals, Operators, Methods, Selection rules) — Card, Moran & Newell, 1983. A computational framework for modeling human task decomposition in interfaces.

| Element | Definition | Example |
|---------|-----------|---------|
| **Goal** | What the user wants to achieve | "Find how a specific player performed in last week's match" |
| **Operator** | Atomic action the user performs | Click button, type text, read label, scan list, scroll page |
| **Method** | Sequence of operators that achieves a goal | Navigate to player page → select match → read stats |
| **Selection rule** | How the user chooses between alternative methods | "If I know the player name, use search. If browsing, use the roster list." |

### Hierarchical Task Decomposition

Users decompose goals into sub-goals, sub-goals into methods, methods into operators. The interface should mirror this natural hierarchy:

```
Goal: Compare two players' passing accuracy
  Sub-goal 1: Find Player A's stats
    Method: Search by name → Select match → Read passing %
  Sub-goal 2: Find Player B's stats
    Method: Same sequence for Player B
  Sub-goal 3: Compare the values
    Method: Remember Player A's value (working memory) → read Player B's value → compare
```

**Audit red flag:** If sub-goal 3 requires the user to *remember* a value from a previous screen, the interface is forcing a working memory burden. The fix is side-by-side comparison or persistent selection.

### Task Decomposition Worksheet

For each core task identified in Phase 1, complete this worksheet:

```
Task: [name]
User goal (in user's words, not system terms): ___
User's expected sequence (how they'd describe it to a colleague): ___
Interface's actual sequence (count every click/input/decision): ___
Divergence points (where interface forces a different path): ___
Working memory demands (information user must hold across steps): ___
Selection rules (where multiple paths exist): ___
Default method (most prominent/discoverable path): ___
Expert shortcut (keyboard, URL, saved filter): ___
```

## User Expertise Spectrum

Every interface serves users across a spectrum. The task model must accommodate all levels without degrading for any.

### Level 1: Kiosk / First-Time User

**Mental model:** None. Learning the system's vocabulary and structure for the first time.

**GOMS characteristics:**
- High operator count (visual search dominates — scanning for labels, buttons, links)
- No compiled methods (every step requires conscious attention)
- No selection rules (doesn't know alternatives exist)
- Heavy reliance on recognition over recall

**Design requirements:**
- Self-explanatory labels — no jargon, no abbreviations, no assumed knowledge
- Guided workflows — clear "what do I do next?" at every step
- Minimal choices per step — reduce decision paralysis
- Prominent "help" and "back" affordances
- Progressive disclosure — don't show everything at once
- Good empty states — "Start here" is better than a blank screen

**Audit check:** Can someone who has never seen this interface complete the core task in their first session without external help?

### Level 2: Regular User

**Mental model:** Functional. Knows the vocabulary, common paths, and what to expect.

**GOMS characteristics:**
- Methods forming — sequences becoming habitual
- Selection rules emerging — starting to choose between paths
- Some compiled sequences (login, navigation, common filters)
- Mix of recognition and recall

**Design requirements:**
- Consistent patterns that reinforce developing methods — same action, same location, same feedback
- Predictable navigation — don't rearrange menus or move buttons
- Feedback that confirms their developing mental model
- Reasonable defaults that match common use cases
- Recent/frequent items for fast access

**Audit check:** After 5 sessions, can the user complete common tasks 50% faster than their first session? (If not, the interface isn't learnable.)

### Level 3: Power User

**Mental model:** Expert. Has compiled methods for all common tasks. Thinks in terms of the system's capabilities.

**GOMS characteristics:**
- Low operator count (compiled motor sequences, keyboard shortcuts)
- Fast selection rules (instant method choice based on context)
- Keyboard-dominant interaction
- Recall-based navigation (knows where everything is)

**Design requirements:**
- Don't slow them down — no unnecessary confirmation dialogs on routine actions
- Keyboard shortcuts for frequent actions
- Batch operations (select multiple, bulk edit)
- Customizable defaults and saved views
- URL-based deep linking (bookmark specific views/filters)
- Command palette or search-based navigation

**Audit check:** Can a power user complete their daily workflow using only the keyboard? Are there unnecessary speed bumps on routine paths?

### Graceful Degradation

The interface must serve all three levels simultaneously:
- Power-user shortcuts must not confuse first-timers (hidden behind keyboard shortcuts, advanced menus)
- First-timer guidance must not impede power users (dismissible, remembers preferences)
- Regular users must not hit a "cliff" where the interface suddenly becomes complex (progressive disclosure, not a binary novice/expert mode)

## Signs of Task Model Mismatch

These indicators suggest the interface's task model diverges from users' mental models:

| Indicator | What it means | Where to look |
|-----------|--------------|---------------|
| Users consistently click the wrong button first | Button labels or positions don't match expected action | User testing, analytics (click heatmaps) |
| Users navigate to the wrong page for a task | Navigation labels don't map to user goals | Navigation analytics, support tickets |
| Users ask "where do I find X?" for core features | Feature is discoverable only by developers who know the code structure | Support tickets, onboarding feedback |
| Users create workarounds (copy-paste to spreadsheet, screenshots) | Interface doesn't support a task the user considers core | User observation, support tickets |
| Users make the same error repeatedly | The error is predicted by the task model — the interface's affordance suggests the wrong action | Error logs, user testing |
| High abandonment on a specific step | Step is either confusing, overwhelming, or doesn't match the user's expected sequence | Analytics (funnel analysis) |
| Users describe the system differently than developers | Vocabulary mismatch — interface uses implementation terms, not user domain terms | User interviews |

## Norman's Gulf Analysis

Donald Norman's Gulfs of Execution and Evaluation (*The Design of Everyday Things*, 1988/2013) provide a structural diagnostic for how well the interface bridges the gap between user intent and system capability.

### Gulf of Execution

**Definition:** The gap between what the user wants to do and the actions the interface provides.

**Narrow gulf (good):** User's goal maps directly to an available action.
- "I want to find Messi" → Type "Messi" in search → Results appear
- Gulf width: 1 translation step

**Wide gulf (finding):** User must translate their goal through multiple indirections.
- "I want to find Messi" → Select competition → Select season → Select team → Scroll through players
- Gulf width: 4 translation steps

### Gulf of Evaluation

**Definition:** The gap between the system's actual state and the user's understanding of that state.

**Narrow gulf (good):** System output is immediately interpretable.
- Display: "Player A is in the 85th percentile for passing accuracy"
- Gulf width: 0 (user understands immediately)

**Wide gulf (finding):** User must translate system output to derive meaning.
- Display: "cosine distance: 0.23"
- Gulf width: high (user must know what cosine distance is, what scale it uses, and whether 0.23 is good or bad)

### Gulf Width Diagnostic Worksheet

For each core task:

```
Task: [name]
Gulf of Execution:
  User intent (in their words): ___
  Closest available action: ___
  Translation steps required: ___
  Gulf width: Narrow (<2 steps) / Medium (2-3) / Wide (>3) / Unbridgeable (action doesn't exist)

Gulf of Evaluation:
  System output: ___
  User's interpretation requirement: ___
  External knowledge required: ___
  Gulf width: Narrow (self-explanatory) / Medium (needs context) / Wide (needs expertise) / Opaque (no interpretation possible)
```

### Gulf Reduction Strategies

| Gulf | Reduction Strategy | Example |
|------|-------------------|---------|
| Execution (wide) | Add direct search | Player search instead of filter cascade |
| Execution (wide) | Add cross-page linking | Click player name on any page → opens their profile |
| Execution (wide) | Reduce filter cascade depth | Smart defaults, "quick filters", URL deep linking |
| Evaluation (wide) | Add interpretive labels | "0.23 (very similar)" or color band: green/yellow/red |
| Evaluation (wide) | Add reference values | "League average: 0.45" next to player's value |
| Evaluation (wide) | Add percentile context | "Top 15% of midfielders" instead of raw metric |
| Evaluation (wide) | Show derivation | "Based on 23 matches in Premier League 2024-25" |

## Cognitive Walkthrough Template

The Cognitive Walkthrough (Wharton et al. 1994) is a structured method for evaluating an interface step-by-step from the user's perspective. Unlike GOMS task decomposition (which maps the *structure* of tasks), the walkthrough evaluates the *experience* of performing them — catching compound issues that emerge between individually-acceptable design decisions.

### When to Use

- For the top 2-3 most critical user tasks identified in Phase 1/2
- Especially for multi-page workflows where context carries across screens
- When individual element analysis (Phase 0, 3, 5) has not revealed enough issues to explain user confusion

### Walkthrough Procedure

For each step in the task:

1. **Will the user try to achieve the right effect?** (Does the user's goal match what the interface expects at this point?)
2. **Will the user notice the correct action is available?** (Is the right control visible, or must they search?)
3. **Will the user associate the correct action with their goal?** (Does the label/icon/position communicate its purpose?)
4. **After performing the action, will the user understand the feedback?** (Is the system response interpretable?)

### Walkthrough Recording Template

```
Walkthrough: [Task name]
User profile: [Kiosk / Regular / Power]
Starting point: [Page/screen where the user begins]

Step 1: [Description]
  Goal at this point: [What the user is trying to accomplish]
  Available actions: [What the interface offers]
  User's likely action: [What they'll probably do]
  System response: [What happens]
  Q1 (right effect?): [Yes/No — explanation]
  Q2 (action visible?): [Yes/No — explanation]
  Q3 (action-goal association?): [Yes/No — explanation]
  Q4 (feedback interpretable?): [Yes/No — explanation]
  Issues: [Any Gulf of Execution/Evaluation problems]

Step 2: [Description]
  ...

Compound issues found: [Issues that only emerge from the sequence, not visible in individual element analysis]
```

## Domain-Specific Cognitive Demands

Every domain has unique cognitive demands beyond generic usability. Identifying these early ensures the audit evaluates domain-relevant issues, not just generic UI patterns.

### Identification Template

For the application's domain, identify 3-5 unique cognitive demands:

| Demand | Description | Interface Support Required | Audit Focus |
|--------|-------------|---------------------------|-------------|
| [e.g., Spatial reasoning] | [Users must interpret 2D spatial layouts] | [Pitch visualization, coordinate systems] | [Check spatial consistency, orientation] |
| [e.g., Statistical literacy] | [Users must interpret probabilistic metrics] | [Context, uncertainty, reference values] | [Check Gulf of Evaluation for all metrics] |
| [e.g., Temporal reasoning] | [Users must reason about event sequences over time] | [Timeline, event markers, temporal context] | [Check temporal navigation, event density] |

### Common Domain Categories

| Domain | Typical Cognitive Demands |
|--------|--------------------------|
| **Analytics / BI** | Statistical interpretation, scale direction, aggregation boundaries, data coverage awareness |
| **Medical** | Risk communication, false positive/negative interpretation, urgency classification |
| **Financial** | Temporal comparison, risk assessment, regulatory compliance awareness |
| **Geographic / Mapping** | Spatial orientation, scale awareness, projection distortion |
| **Scientific** | Unit conversion, measurement uncertainty, experimental design context |
| **Creative / Design** | Visual hierarchy, brand consistency, audience awareness |

## Common Task Model Anti-Patterns

| Anti-Pattern | Description | Fix |
|-------------|-------------|-----|
| **Implementation-Driven Structure** | Pages organized by database tables or code modules, not user goals | Reorganize around user tasks |
| **Feature Soup** | Every feature equally prominent — no hierarchy of importance | Progressive disclosure; core tasks front and center |
| **Wizard Overuse** | Forcing linear steps when the user's mental model is non-linear | Allow out-of-order completion with clear status |
| **Hidden Defaults** | System applies important defaults the user doesn't know about | Make defaults visible and overridable |
| **Expert Blind Spot** | Interface assumes domain knowledge that regular users lack. The designer's expertise creates assumptions about what's "obvious" (Hinds 1999). **Structured check:** For each domain-specific metric displayed, ask: (1) Can a domain-only user (no data science) interpret it? (2) Can a data-science-only user (no domain) interpret it? If either answer is "no," the metric needs a tooltip, inline explanation, or contextual help. Metrics opaque to *both* audiences are Critical | Add contextual help, tooltips, reference values. Test with users outside the design team's expertise level. See Expert Blind Spot Audit table in SKILL.md Phase 2 |
| **Frankenflow** | Task requires visiting 3+ unrelated pages to complete one logical operation | Consolidate related operations |
| **Gulf of Execution Cascade** | Core task requires >3 filter selections before any content appears | Add search, deep links, smart defaults, or "quick access" shortcuts |
| **Opaque Evaluation** | System shows numeric outputs without interpretive context — user sees the number but cannot judge its meaning | Add reference values, percentile context, verbal labels, or calibration anchors |
