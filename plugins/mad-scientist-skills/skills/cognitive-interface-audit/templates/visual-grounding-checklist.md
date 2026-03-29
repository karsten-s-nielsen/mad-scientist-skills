# Visual Grounding Checklist

## Purpose

Answer: "Does the interface provide sufficient visual information for the user to maintain situation awareness and complete tasks efficiently?"

## Pre-audit checklist

Before auditing, identify:

- [ ] Which system state changes are user-initiated vs. automatic
- [ ] The feedback mechanisms for each user action (visual, auditory, haptic)
- [ ] Whether the interface shows real-time collaborative or automated updates
- [ ] The latency profile of key operations (instant, <1s, >1s, >10s)

## Gergle's Grounding Theory

Darren Gergle's research (CollabLab, Northwestern; CHI Academy 2026) demonstrates that shared visual information affects task performance through two distinct mechanisms:

### Mechanism 1: Situation Awareness

**Definition:** The user's perception and comprehension of the current state of the system.

**Three levels** (Endsley 1995, applied to interface design):

| Level | Question | Example | When it fails |
|-------|---------|---------|---------------|
| **Perception** | Can the user see what state the system is in? | Is the filter active? Is the data loading? Is there an error? | Hidden state changes, silent failures, no loading indicators |
| **Comprehension** | Does the user understand what the state means? | What does "3 items selected" imply for the next action? | Ambiguous indicators, missing context, jargon-heavy labels |
| **Projection** | Can the user anticipate what will happen next? | If I click "Apply", what will change? | No preview, no undo warning, surprising side effects |

### Mechanism 2: Conversational Grounding

**Definition:** The shared context between user and system that enables efficient communication.

Gergle's key finding: **not just the availability but the form of visual information differentially affects performance.** Two interfaces can show the same data but ground the user differently based on layout, timing, and visual structure.

**Grounding costs** (Clark & Brennan 1991, adapted for UI):

| Cost | Description | UI Manifestation |
|------|-------------|-----------------|
| **Formulation** | Effort to express an intention | Complex filter construction, multi-step form entry |
| **Production** | Effort to execute the action | Number of clicks, precision required, scroll distance |
| **Reception** | Effort to perceive the system's response | Small visual changes, buried feedback, slow rendering |
| **Understanding** | Effort to comprehend the response | Ambiguous results, unclear error messages, missing context |
| **Repair** | Effort to fix a misunderstanding | Going back, clearing state, re-entering data |

### Gergle's Key Findings for Interface Design

| Finding | Citation | Audit Implication |
|---------|----------|-------------------|
| Delayed visual feedback degrades collaborative performance | Gergle, Kraut & Fussell 2006 | Feedback latency thresholds must be respected (see below) |
| Display characteristics differentially affect spatial tasks | Gergle 2006 | Layout decisions should be evaluated per task type, not one-size-fits-all |
| Visual information form matters more than availability | Gergle et al. 2013 | Showing data is not enough — HOW it's shown determines effectiveness |
| Age-related bias can be embedded in computational systems | Gergle et al. (CHI 2018, Best Paper) | Data visualizations must be evaluated for demographic bias |
| Model positionality affects design outcomes | Gergle et al. (CHI 2022, Best Paper HM) | Audit should consider whose perspective the interface privileges |

## Feedback Latency Thresholds

Based on Nielsen (1993) response time limits, validated by Gergle's visual feedback research:

| Threshold | User Perception | Required Design Response |
|-----------|----------------|------------------------|
| **<100ms** | "Instantaneous" — direct manipulation | Visual acknowledgment of user action (button press state, hover effect, toggle change). No loading indicator needed |
| **100ms-1s** | "System is responding" — noticeable but tolerable | Show immediate acknowledgment (button disables, spinner appears). User maintains feeling of control |
| **1s-10s** | "System is working" — user's attention may wander | Show progress indicator (spinner, progress bar, skeleton screen). User needs assurance the system hasn't frozen |
| **>10s** | "Am I still connected?" — user questions system health | Show progress percentage, estimated time remaining, or allow background processing with notification. Consider allowing the user to continue other tasks |

### Audit Procedure for Latency

1. Identify every user-initiated action in the interface
2. Measure (or estimate) response time for each
3. Check that the feedback mechanism matches the latency threshold
4. Flag any action >100ms without visual acknowledgment (High severity)
5. Flag any action >1s without progress indicator (High severity)
6. Flag any action >10s without progress/estimation (Critical severity)

## Joint Action Storyboard Framework

Gergle et al. (CSCW 2021) — a structured method for visualizing communication grounding costs in interactive workflows.

### How to Use

1. **Select a critical workflow** (from Phase 2 task model mapping)
2. **Draw each step as a panel** — what the user sees, what they do, what changes
3. **For each panel, score the grounding cost:**

| Grounding Dimension | Score 1 (Low) | Score 3 (Medium) | Score 5 (High) |
|--------------------|----|----|----|
| **State visibility** | System state is immediately obvious | State requires scanning to determine | State is hidden or ambiguous |
| **Action clarity** | Next action is obvious from visual cues | Next action requires reading instructions | Next action requires external knowledge |
| **Feedback immediacy** | Response appears within 100ms | Response appears within 1-10s | Response is delayed >10s or absent |
| **Context continuity** | User maintains visual context across steps | Minor context shift (scroll, tab switch) | Major context loss (page reload, navigation) |
| **Recovery cost** | One-click undo or back | Multi-step recovery | Must restart from beginning |

4. **Sum scores per panel** — panels scoring >15 are grounding hotspots
5. **Total across workflow** — workflows scoring >50 need redesign

### Storyboard Template

```
Panel 1: [Step name]
  User sees: [description of visible state]
  User does: [action taken]
  System responds: [what changes visually]
  Grounding cost: State[_] + Action[_] + Feedback[_] + Context[_] + Recovery[_] = [total]
  Notes: [any issues identified]

Panel 2: [Step name]
  ...
```

## State Visibility Checklist

Every system state must be visually communicated to the user:

| State | Must be visible | How to communicate |
|-------|----------------|-------------------|
| **Loading** | Always | Spinner, skeleton, progress bar |
| **Empty** | Always | "No data" message with explanation and next step |
| **Error** | Always | Red/orange indicator + specific message + recovery action |
| **Success** | After user action | Green indicator or toast + what succeeded |
| **Filtered** | When filters are active | Active filter badges, "Showing X of Y", clear all button |
| **Selected** | When items are selected | Highlight, count badge, action bar |
| **Modified (unsaved)** | When user has unsaved changes | Dirty indicator (dot, asterisk), save prompt on navigation |
| **Stale** | When data may be outdated | "Last updated: [timestamp]", refresh button |
| **Offline** | When connectivity is lost | Banner or indicator, queue actions for when online |
| **Permission-limited** | When user can't perform an action | Disabled state with tooltip explaining why |
| **Paginated** | When viewing a subset | "Page X of Y", total count, navigation controls |
| **Sorted** | When data is ordered | Sort indicator on column header, sort direction arrow |

## Constraint Visibility (Vicente & Rasmussen EID)

Ecological Interface Design (Vicente & Rasmussen, *IEEE SMC*, 1992) argues that effective interfaces make the work domain's constraints visible — not just the system's controls. When users cannot see *why* certain data is available or unavailable, they form incorrect mental models about what the system represents.

### Abstraction Hierarchy

EID's abstraction hierarchy describes five levels at which users need to understand the work domain:

| Level | Question | Interface Must Show |
|-------|---------|-------------------|
| **Functional purpose** | Why does this system exist? | Clear value proposition on landing page / first interaction |
| **Abstract function** | What principles govern the domain? | Relationships between metrics, domain model visibility |
| **Generalized function** | What processes produce the outputs? | Data pipeline provenance, model descriptions |
| **Physical function** | How is data collected and processed? | Data source labels, collection methodology |
| **Physical form** | What raw data exists? | Data coverage indicators, available vs total counts |

### Constraint Visibility Checklist

| Check | What to look for | Severity if missing |
|-------|-----------------|---------------------|
| **Data coverage** | Does the interface explain what fraction of the total data universe is visible? (e.g., "Tracking data: 20 of 380 matches") | High |
| **Absence explanation** | When a feature, page, or data subset is unavailable, does the interface explain *why*? (vs silently hiding or showing empty state) | High |
| **Boundary markers** | Are aggregation/comparison boundaries explicit? (e.g., "Average based on 5 Bundesliga matches" vs "Average: 0.45") | Medium |
| **Relationship visibility** | Can users see how displayed metrics relate to each other without navigating to separate pages? | Medium |
| **Constraint source** | Can users tell whether a limitation is from data availability, model scope, or system design? | Medium |

## Trust Calibration (Lee & See)

John D. Lee and Katrina A. See's "Trust in Automation" (*Human Factors*, 2004) establishes that appropriate trust in automated/model-derived outputs requires visibility of three properties: **performance** (how well does the system work?), **process** (how does it work?), and **purpose** (why was it designed this way?).

### When Trust Calibration Applies

This section applies whenever the interface displays outputs from:
- Machine learning models (predictions, embeddings, similarity scores, classifications)
- Statistical models (computed metrics, derived values, aggregations over uncertain data)
- Recommendation algorithms (suggested items, ranked lists)
- Automated decision systems (alerts, flags, risk scores)

**Skip this section** for interfaces that display only user-entered data, simple lookups, or raw measurements with no model/algorithm layer.

### Trust Calibration Checklist

| Check | Trust Dimension | What to look for | Severity if missing |
|-------|----------------|-----------------|---------------------|
| **Model provenance** | Process | Can the user tell which model/algorithm produced this output? | Medium |
| **Uncertainty indication** | Performance | Does the output show confidence bounds, ranges, or uncertainty? (e.g., "xG: 0.23 ± 0.05") | High |
| **Sample size context** | Performance | Does the user know how much data informs this output? (e.g., "based on 23 matches") | High |
| **Limitation visibility** | Purpose | Are known model limitations surfaced near the output? (e.g., "tracking data available for 7 of 38 matches") | Medium |
| **Calibration anchors** | Performance | Are reference points provided for numeric outputs? (e.g., "league average: 0.45") | High |
| **Temporal validity** | Performance | Is the model's training data currency visible? (e.g., "model trained on 2024-25 data") | Medium |
| **Failure modes** | Process | When the model produces low-confidence or out-of-distribution results, is this communicated? | High |
| **Comparability scope** | Purpose | Are comparison boundaries clear? (e.g., "similarity computed within midfielders only" vs "all positions") | Medium |

### Trust Miscalibration Patterns

| Pattern | Risk | Fix |
|---------|------|-----|
| **Over-trust** — Precise-looking numbers with no uncertainty | Users treat model outputs as ground truth | Add confidence intervals, show model limitations, use softer language ("estimated", "approximately") |
| **Under-trust** — Model outputs presented identically to raw data | Users ignore valuable computed insights because they look like just another number | Differentiate model outputs visually; add provenance label |
| **Automation complacency** — Model always agrees with user's prior belief | Users stop checking because the model seems to confirm everything | Show cases where model disagrees with naive expectation |
| **Opaque aggregation** — Derived metric with no decomposition | Users cannot verify the output or understand what drives it | Show component breakdown or "how this was calculated" expandable |

## Visual Anchoring Patterns

Techniques to reduce grounding cost across multi-step workflows:

| Pattern | Purpose | When to use |
|---------|---------|------------|
| **Breadcrumbs** | Show position in hierarchy | Any navigation deeper than 2 levels |
| **Step indicator** | Show progress in multi-step workflow | Any workflow with 3+ sequential steps |
| **Persistent context panel** | Keep key information visible while details change | Master-detail layouts, drill-down analysis |
| **Sticky headers** | Keep column labels visible while scrolling data | Any data table taller than one viewport |
| **Active state highlighting** | Show which item/filter/tab is currently selected | Any selection-based navigation |
| **Mini-map / overview** | Show position within large content | Long documents, large data sets, complex visualizations |
| **Transition animations** | Show spatial relationship between views | Navigation between related content (slide in/out, expand/collapse) |
| **Persistent search/filter bar** | Keep the user's query visible while browsing results | Search results, filtered lists |
