# Cognitive Load Assessment

## Purpose

Answer: "Is the interface consuming more working memory than the task inherently requires?"

## Pre-audit checklist

Before auditing, identify:

- [ ] The screens or views with the highest information density
- [ ] Which tasks require users to hold intermediate results in memory
- [ ] The number of simultaneous options presented at key decision points
- [ ] Whether progressive disclosure is used anywhere in the interface

## Sweller's Cognitive Load Theory (CLT)

John Sweller's cognitive load theory (1988) distinguishes three types of load. The audit's primary target is **extraneous load** — cognitive overhead caused by poor design rather than inherent task complexity.

### Load Taxonomy

| Load Type | Source | Controllable? | Design Goal |
|-----------|--------|---------------|-------------|
| **Intrinsic** | Inherent task complexity. Determined by the domain and the learner's expertise | Not directly — but can be managed through scaffolding | Scaffold with progressive disclosure. Break complex tasks into learnable chunks |
| **Extraneous** | Poor design. Interface decisions that consume working memory without advancing the task | **Yes — this is the audit's primary target** | **Eliminate.** Every instance is a design deficiency |
| **Germane** | Productive learning. Cognitive effort spent building accurate mental models and schemas | Yes — design can encourage or discourage it | **Maximize.** Consistent patterns, meaningful grouping, clear feedback all promote schema building |

### Examples by Load Type

| Scenario | Load Type | Why |
|----------|-----------|-----|
| Comparing two complex statistical distributions | Intrinsic | The comparison is inherently complex regardless of interface |
| Having to remember a value from Page A while on Page B | Extraneous | Interface design forces unnecessary recall |
| Learning that blue = home team, red = away team consistently | Germane | User builds a reusable schema |
| Scrolling back and forth to cross-reference two tables | Extraneous | Interface could place them side-by-side |
| Figuring out which of 12 similar buttons is the right one | Extraneous | Interface could group/label better |
| Understanding that "xT" means expected threat after seeing it with a tooltip | Germane | User learns domain vocabulary in context |

## NASA-TLX Scoring Guide

The NASA Task Load Index (Hart & Staveland, 1988) is a 6-dimension subjective workload assessment. While originally designed for human subjects testing, its dimensions provide a structured framework for expert evaluation of interface cognitive demands.

### Dimensions

| Dimension | Scale | What to evaluate | High score means |
|-----------|-------|-----------------|-----------------|
| **Mental Demand** | 1 (Low) — 20 (High) | How much thinking, deciding, calculating, remembering, searching is required to complete the task? | Interface demands excessive cognitive processing |
| **Physical Demand** | 1 (Low) — 20 (High) | How much clicking, scrolling, typing, mouse movement is required? | Interface demands excessive physical interaction |
| **Temporal Demand** | 1 (Low) — 20 (High) | How much time pressure does the user feel? Is the pace imposed by the system (timeouts, auto-refresh, loading delays)? | System creates urgency or forces waiting |
| **Effort** | 1 (Low) — 20 (High) | How hard does the user have to work to accomplish their level of performance? | Disproportionate effort for the task |
| **Performance** | 1 (Good) — 20 (Poor) | How successful is the user in accomplishing the task? (Note: scale is inverted) | Users feel they failed or got an incomplete result |
| **Frustration** | 1 (Low) — 20 (High) | How insecure, discouraged, irritated, stressed is the experience? | Interface creates negative emotional response |

### Scoring Procedure (Expert Evaluation)

1. Select the 3-5 most critical user tasks (from Phase 2)
2. Walk through each task step-by-step in the actual interface
3. Score each dimension 1-20 based on your expert assessment
4. Calculate the unweighted average across dimensions
5. Flag any single dimension scoring >15 (regardless of average)

### Interpretation

| Average Score | Rating | Action |
|--------------|--------|--------|
| 1-5 | **Low load** | Interface handles cognitive demands well |
| 6-10 | **Moderate load** | Acceptable for expert users; may overwhelm novices |
| 11-15 | **High load** | Redesign needed — significant extraneous load present |
| 16-20 | **Critical load** | Task is likely failing for most users |

## Information Density Heuristics

Quantitative thresholds for detecting cognitive overload. These are guidelines, not hard rules — context matters (a stock trading terminal has different norms than a consumer app).

### Per-Screen Thresholds

| Metric | Threshold | Severity | Rationale |
|--------|-----------|----------|-----------|
| Interactive elements per viewport | >15 | High | Exceeds comfortable scanning capacity |
| Distinct data points visible simultaneously | >30 | Medium | Information overload without grouping |
| Decision points per task step | >3 | High | Choice overload at individual steps |
| Sequential decisions per complete task | >7 | High | Exceeds working memory span for decision chain |
| Visual hierarchy levels on one screen | >4 | Medium | Too many levels — unclear what's most important |
| Text paragraphs before first interactive element | >2 | Medium | Wall of text before action — users skip to action |
| Data table columns visible without scrolling | >10 | Medium | Too many columns to scan effectively |
| Navigation items at one level | >7 | Medium | Miller's Law (Miller 1956) — more than 7 items need grouping |
| Filters visible simultaneously | >8 | Medium | Filter overload — need grouping or progressive disclosure |
| Form fields visible without scrolling | >10 | Medium | Long forms intimidate — group into sections |

### Cross-Screen Thresholds

| Metric | Threshold | Severity | Rationale |
|--------|-----------|----------|-----------|
| Information user must remember from a previous screen | Any | High | Extraneous load — interface should carry context forward |
| Steps to undo an action | >2 | High | Recovery should be immediate (Ctrl+Z or one click) |
| Pages visited to complete one logical task | >3 | Medium | Task should be co-located unless inherently multi-phase |
| Times user must re-enter the same information | Any | High | Interface should remember and pre-fill |

## Progressive Disclosure Patterns

Progressive disclosure is the primary tool for managing intrinsic load without adding extraneous load.

### Disclosure Levels

| Level | What to show | When to show | Mechanism |
|-------|-------------|-------------|-----------|
| **Level 0** | Core task elements only | Always visible | Main page content |
| **Level 1** | Common options and secondary actions | On request (one click) | Expandable sections, dropdown menus, sidebars |
| **Level 2** | Advanced options, configuration, edge cases | On explicit request | Settings page, advanced mode toggle, modal dialogs |
| **Level 3** | Raw data, debugging info, system internals | Only when needed | Developer tools, export to CSV, API docs |

### Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| **Everything at Level 0** | All features visible at once — cognitive overload | Move secondary features to Level 1+ |
| **Everything at Level 2** | Core features buried — discoverability failure | Promote core features to Level 0 |
| **Progressive concealment** | Features hidden with no indication they exist | Always show the trigger/label, hide the content |
| **Inconsistent nesting** | Sometimes one click to expand, sometimes two — unpredictable | Standardize disclosure interaction across the interface |
| **Disclosure amnesia** | Expanded sections collapse on page navigation or refresh | Remember disclosure state in session |

## Dual-Process Theory (Kahneman)

Daniel Kahneman's Dual-Process Theory (*Thinking, Fast and Slow*, 2011) distinguishes two cognitive systems:

| System | Characteristics | Interface Implications |
|--------|----------------|----------------------|
| **System 1** (fast) | Automatic, intuitive, effortless. Pattern recognition, spatial perception, emotional response | Color coding, spatial grouping, familiar icons, directional indicators (up = good), pre-attentive visual features |
| **System 2** (slow) | Deliberate, analytical, effortful. Calculation, comparison, logical reasoning | Raw numbers, multi-step calculations, unfamiliar scales, counter-intuitive metrics |

### Dual-Process Audit Checks

The audit question: "Is the interface engaging System 2 when System 1 could suffice?"

| Check | System 2 Overload Indicator | System 1 Fix | Severity |
|-------|----------------------------|--------------|----------|
| **Raw numeric outputs** | User must calculate whether a number is good/bad/average | Add color bands (green/yellow/red), verbal labels ("above average"), or sparkline context | High |
| **Counter-intuitive scales** | Lower value = more intense/better, violating "higher = more" System 1 expectation | Add explicit direction indicator ("lower is better", downward arrow) or invert the scale | Medium |
| **Raw identifiers** | User must mentally map IDs to meaningful entities | Show human-readable names; provide ID on demand | Medium |
| **Unlabeled axes** | User must infer what a chart dimension represents | Add clear axis labels with units | Medium |
| **Opaque aggregations** | User must guess aggregation boundaries (per-match? per-season? career?) | Show scope explicitly ("Season 2024-25, 23 matches") | Medium |
| **Missing pre-attentive cues** | User must read and compare numbers that could be color-coded or spatially arranged | Use color, size, position, or grouping for at-a-glance comparison | Low |
| **Multiple unit systems** | User must mentally convert between unit systems (e.g., yards and meters, different coordinate systems) | Normalize to one system or show both with clear labels | Medium |

### When System 2 is Appropriate

Not all System 2 engagement is bad. For *analytical tasks* (detailed comparison, hypothesis testing, data exploration), System 2 engagement is expected and productive — this is **germane load** in Sweller's taxonomy. The audit target is System 2 engagement that provides no analytical value — extraneous cognitive effort caused by poor presentation choices.

## Visual Encoding Effectiveness (Cleveland & McGill)

Cleveland & McGill's landmark paper "Graphical Perception" (*JASA*, 1984) established an empirically-validated ranking of visual encodings by perceptual accuracy. For data-heavy interfaces, each visualization should use the most accurate encoding available for its data relationship.

### Encoding Hierarchy (ranked by perceptual accuracy)

| Rank | Encoding | Perceptual Accuracy | Best For | Common Misuse |
|------|----------|-------------------|----------|---------------|
| 1 | Position along common scale | Highest | Comparing quantities (bar chart, dot plot, scatter plot) | — |
| 2 | Position along non-aligned scales | High | Comparison with offset context (small multiples) | — |
| 3 | Length | Good | Magnitude comparison (simple bar charts) | Stacked bars where inner segments are hard to compare |
| 4 | Angle / slope | Moderate | Trends over time (line charts) | Radar/spider charts — angle encoding distorts magnitude perception |
| 5 | Area | Poor | Approximate magnitude (treemaps, bubble charts) | Pie charts — area + angle combination performs poorly |
| 6 | Color saturation / hue | Lowest for quantitative | Categories (nominal) or continuous spatial fields (heatmaps) | Using color intensity for precise quantitative comparison |

### Audit Procedure

For each data visualization in the interface:
1. Identify the *data relationship* being communicated (comparison, trend, distribution, part-to-whole, spatial)
2. Identify the *visual encoding* used
3. Check whether a higher-ranked encoding could represent the same relationship
4. Flag mismatches where a lower-ranked encoding is used when a higher-ranked alternative exists

### Common Violations

| Violation | Issue | Fix |
|-----------|-------|-----|
| Radar/spider chart for precise comparison | Angle encoding (rank 4) when position (rank 1) is available | Use grouped bar chart or parallel coordinates |
| Bar chart with multiple metrics on incompatible scales | Small-magnitude metrics visually compressed next to large ones | Normalize, use separate charts, or use dual-axis with clear labeling |
| Pie chart for >5 categories | Area + angle encoding with many small slices | Use horizontal bar chart (position encoding) |
| Heatmap as only view of quantitative data | Color encoding (rank 6) with no text overlay | Add numeric labels or provide table view alongside |
| 3D effects on 2D data | Perspective distortion adds no informational value | Remove 3D; use flat 2D encoding |

### Chart Scalability / Degradation

Cleveland & McGill's ranking evaluates encoding *type*, but encoding effectiveness also degrades as data volume increases. A grouped bar chart is perceptually excellent for 4 groups but becomes a color field at 20. The audit must evaluate not just which encoding is used but whether it remains effective at the data volumes the interface produces.

| Chart Type | Degradation Threshold | What Happens | Fix |
|------------|----------------------|--------------|-----|
| Grouped bar chart | >8 groups | Individual bars become slivers, impossible to compare across groups | Paginate, aggregate, or switch to heatmap |
| Stacked bar chart | >5 segments | Inner segments (non-baseline) become unreadable | Show top-N + "Other", or switch to small multiples |
| Pie / donut chart | >5 slices | Small slices are imperceptible | Switch to horizontal bar chart |
| Scatter plot | >100 points in view | Overplotting hides distribution shape | Add opacity, jitter, or switch to density contours |
| Legend | >5 items | Legend becomes primary reading task instead of chart | Use inline labels, small multiples, or interactive highlight |
| Axis labels | Variable-length text | Labels overlap or rotate to unreadability | Abbreviate, rotate 45°, or switch to horizontal bars |

**Audit procedure:** For each chart, determine the maximum data volume it will render (not the current volume — the maximum). Check whether the encoding remains effective at that scale.

## Working Memory Management Checklist

| Check | Extraneous Load Source | Fix |
|-------|----------------------|-----|
| Does the user need to remember data from a previous screen? | Cross-screen recall | Carry forward in context panel, breadcrumb, or summary |
| Does the user need to translate between formats? (e.g., code to label, ID to name) | Format translation | Show human-readable labels; provide ID only on demand |
| Does the user need to calculate something mentally? (e.g., time difference, percentage) | Mental arithmetic | Pre-compute and display the derived value |
| Does the user need to compare items by scrolling back and forth? | Spatial separation of related items | Side-by-side comparison view |
| Does the user need to hold a mental model of system state? | Hidden state | Show state explicitly (status indicators, active filters, selection count) |
| Does the user need to read documentation to use a feature? | Deferred explanation | Contextual help, tooltips, inline examples |
| Does the user need to map between terminology systems? | Vocabulary mismatch | Use the user's domain vocabulary consistently |
| Does the user need to judge whether a numeric value is "good" or "bad"? | Missing interpretive context (System 2 when System 1 could suffice) | Add reference values, percentile rank, color coding, or verbal labels |
