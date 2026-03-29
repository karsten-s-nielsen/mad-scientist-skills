# Error Tolerance Checklist

## Purpose

Answer: "When users make errors — and they will — does the interface prevent, detect, and recover from them effectively at every stage?"

## Pre-audit checklist

Before auditing, identify:

- [ ] The destructive or irreversible actions in the interface
- [ ] The most common user errors reported or observed
- [ ] Which inputs accept free-form text vs. constrained choices
- [ ] Whether undo/redo is available and at what granularity

## Wood & Byrne 7-Layer Defense Framework

Scott D. Wood's extension of GOMS to error prediction (dissertation, University of Michigan, 2000; published with Mike Byrne, CogSci 2002) provides a systematic framework for designing error-tolerant interfaces. Each layer corresponds to a stage in the lifecycle of an erroneous performance.

### Layer Reference

| Layer | Stage | Goal | Design Mechanisms | Audit Question |
|-------|-------|------|-------------------|----------------|
| **1. Prevention** | Before error | Eliminate the error class entirely | Input constraints, type restrictions, disabled invalid options, required fields, impossible states made unrepresentable | Can this error happen at all? If yes, why hasn't a design constraint eliminated it? |
| **2. Reduction** | Before error | Minimize opportunities for error | Smart defaults, auto-fill, progressive disclosure, step minimization, disambiguation, clear labeling | Has the design minimized the number of places this error can occur? |
| **3. Detection** | After commission | Help user notice the error | Inline validation, visual state changes, confirmation dialogs, preview before commit, diff views | If the user makes this error, will they know? How quickly? |
| **4. Identification** | After detection | Help user understand what went wrong | Specific error messages ("Email format invalid" not "Error"), field-level highlighting, contextual help, error codes with explanations | Does the user know WHAT went wrong and WHY? |
| **5. Correction** | After identification | Make fixing easy and discoverable | Edit-in-place, undo button, "fix this" links, pre-populated correction forms, suggested corrections | Can the user fix the error without starting over? |
| **6. Resumption** | After correction | Return to task without losing context | State preservation after error, no page reload on validation failure, draft saving, scroll position maintained, back button works | After fixing the error, is the user back where they were? Or did they lose context? |
| **7. Mitigation** | Unrecoverable | Minimize damage when all else fails | Soft delete (trash), version history, audit trail, confirmation on irreversible actions, auto-save, backups | If the worst happens, how bad is it? Can the damage be undone? |

### Layer Interaction

Layers are not independent — they form a cascading defense:

```
User action
  → Layer 1 (Prevention): Can the error be made impossible?
    → YES: Error eliminated. Done.
    → NO: Error is possible. Proceed to Layer 2.
  → Layer 2 (Reduction): Is the opportunity minimized?
    → Error still occurs sometimes. Proceed to Layer 3.
  → Layer 3 (Detection): Does the user notice?
    → YES: Proceed to Layer 4.
    → NO: Error goes undetected. CRITICAL gap.
  → Layer 4 (Identification): Does the user understand?
    → YES: Proceed to Layer 5.
    → NO: User is confused and stuck. HIGH gap.
  → Layer 5 (Correction): Can they fix it?
    → YES: Proceed to Layer 6.
    → NO: User must start over. HIGH gap.
  → Layer 6 (Resumption): Can they resume?
    → YES: Task continues. Error handled.
    → NO: Context lost. User frustration. MEDIUM gap.
  → Layer 7 (Mitigation): Last resort.
    → Damage minimized. Or not.
```

**Key insight:** A gap at Layer 3 (Detection) is almost always worse than a gap at Layer 1 (Prevention). Undetected errors compound — the user continues working on a wrong foundation, making the eventual recovery much more expensive.

## Rasmussen's Skills-Rules-Knowledge (SRK) Framework

Jens Rasmussen's 1983 taxonomy classifies human performance into three cognitive levels. Each level produces different error types requiring different defenses.

### SRK Error Classification

| Level | Cognitive Mode | Error Type | Mechanism | Example | Best Defense Layers |
|-------|---------------|-----------|-----------|---------|---------------------|
| **Skill-based** | Automatic, habitual | **Slips** — correct intention, wrong execution | Motor error, attention capture, habit intrusion | Clicking "Delete" instead of adjacent "Edit" because muscle memory overshoots | L1 (Prevention): separate destructive actions physically. L3 (Detection): confirmation dialog |
| **Rule-based** | Pattern matching | **Mistakes** — wrong rule selected | Strong-but-wrong rule fires because context resembles a familiar situation | Applying a date filter meant for "match date" to "upload date" because both say "Date" | L2 (Reduction): differentiate contexts visually. L4 (Identification): show which rule applied |
| **Knowledge-based** | Conscious reasoning | **Errors** — wrong mental model | User's understanding of the system is fundamentally incorrect | User expects "Archive" to delete data because their previous tool used that word for deletion | L1 (Prevention): use unambiguous vocabulary. L3 (Detection): preview of what will happen |

### SRK-Specific Design Guidance

**For skill-based errors (slips):**
- Separate destructive controls from frequent controls (distance and visual distinction)
- Make undo always available for routine actions
- Don't place "Delete" next to "Edit" or "Cancel" next to "Confirm"
- Use different interaction modalities for different severity levels (click for low risk, click + confirm for medium, type-to-confirm for high)

**For rule-based errors (mistakes):**
- Make context differences visually obvious (if two screens look similar but behave differently, add strong visual differentiation)
- Show what rule the system is applying ("Filtered by: match date" not just "Filtered")
- Provide context-specific labels (not generic "Submit" on every form)
- When users switch between similar contexts, highlight what changed

**For knowledge-based errors (wrong mental model):**
- Use domain-standard vocabulary, not system-specific terms
- Show previews of what will happen before irreversible actions
- Provide conceptual help (not just procedural help) — explain what the system IS, not just how to click through it
- Use progressive disclosure to teach the model incrementally

## Reason's Error Mechanisms

James Reason's taxonomy (1990) identified two mechanisms that Wood found particularly relevant to interface error prediction:

### Similarity Matching

**Mechanism:** A wrong-but-similar rule fires because the interface makes two different contexts look too similar.

**Audit procedure:**
1. Identify all pairs of screens or workflows that look visually similar
2. For each pair, determine: do they behave the same way?
3. If they look similar but behave differently → **High risk**. Users will apply the mental model from one to the other.

**Fix:** Add strong visual differentiators — different color accents, different header styles, context labels, or distinct layout patterns for functionally different screens.

### Frequency Gambling

**Mechanism:** The most-used routine executes even when the current context demands a different action. The user's motor program runs on autopilot.

**Audit procedure:**
1. Identify the most frequently performed action on each screen
2. Identify contexts where that same action has a different (especially destructive) meaning
3. If the most common action and a dangerous action share the same position/appearance → **Critical risk**

**Fix:** Make the dangerous variant visually distinct. Change button color, position, or label in the dangerous context. Add a speed bump (confirmation) specifically for the rare-but-dangerous case.

**Example:** A "Confirm" button that usually means "proceed to next step" but on one specific screen means "permanently delete all data." Users who have clicked "Confirm" 500 times will click it a 501st time on autopilot.

## Per-Task Error Tolerance Worksheet

For each critical task path:

```
Task: [name]
Most likely error class:
  - SRK level: [Skill / Rule / Knowledge]
  - Mechanism: [Slip / Similarity matching / Frequency gambling / Wrong model]
  - Scenario: [What specifically goes wrong]

Defense layer coverage:
  L1 Prevention:   [Present / Missing / Partial] — [description]
  L2 Reduction:    [Present / Missing / Partial] — [description]
  L3 Detection:    [Present / Missing / Partial] — [description]
  L4 Identification: [Present / Missing / Partial] — [description]
  L5 Correction:   [Present / Missing / Partial] — [description]
  L6 Resumption:   [Present / Missing / Partial] — [description]
  L7 Mitigation:   [Present / Missing / Partial] — [description]

First uncovered layer: [number] — this is the audit's priority finding
Overall error tolerance rating: [Strong / Adequate / Weak / No defense]
```

## Framework-Specific Error Tolerance Patterns

### Streamlit

| Error Type | Prevention (L1) | Detection (L3) | Recovery (L5-L6) |
|-----------|-----------------|-----------------|-------------------|
| Wrong filter selection | `st.selectbox` with sane default | Active filter display in sidebar | Filter reset button; URL preserves state |
| Data entry error | Input validation via `st.number_input` min/max | `st.warning` on invalid input | Keep form values on rerun (session_state) |
| Accidental navigation | No destructive nav without save prompt | `st.session_state` dirty flag | Draft preservation in session_state |
| Chart misinterpretation | Clear axis labels, units, and titles | Tooltip on hover with exact values | Toggle between chart types for verification |

### React

| Error Type | Prevention (L1) | Detection (L3) | Recovery (L5-L6) |
|-----------|-----------------|-----------------|-------------------|
| Form submission error | Client-side validation, disabled submit until valid | Field-level error messages | Preserve form state on error, scroll to first error |
| Navigation loss | `beforeunload` handler on dirty forms | Visual dirty indicator (unsaved changes dot) | Auto-save or draft recovery |
| API failure | Optimistic UI with rollback | Error boundary with user-friendly message | Retry button with exponential backoff |
| State inconsistency | Reducer pattern (single source of truth) | DevTools / state inspector in development | State reset to last known good |
