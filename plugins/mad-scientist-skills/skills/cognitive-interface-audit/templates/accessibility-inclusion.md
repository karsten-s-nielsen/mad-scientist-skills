# Accessibility & Inclusion

## Purpose

Answer: "Can all users — regardless of ability, device, or demographic background — use this interface effectively?"

## Pre-audit checklist

Before auditing, identify:

- [ ] The target WCAG conformance level (A, AA, or AAA)
- [ ] Whether the interface has been tested with a screen reader
- [ ] The primary input methods (mouse, keyboard, touch, voice)
- [ ] Any known demographic or regional user groups

## WCAG 2.1 AA Checklist (Automated + Manual)

The Web Content Accessibility Guidelines (WCAG) 2.1 Level AA is the widely accepted baseline for accessibility. This checklist covers the most impactful criteria with framework-specific audit patterns.

### Perceivable (Principle 1)

Users must be able to perceive all information and UI components.

| Criterion | WCAG | What to check | Severity |
|-----------|------|---------------|----------|
| Text alternatives for images | 1.1.1 | Every `<img>` has meaningful `alt` text (not just `alt=""` unless decorative) | High |
| Captions for video/audio | 1.2.2 | Pre-recorded media has synchronized captions | High |
| Color contrast — normal text | 1.4.3 | Foreground/background ratio ≥ 4.5:1 for text <24px | High |
| Color contrast — large text | 1.4.3 | Foreground/background ratio ≥ 3:1 for text ≥24px or bold ≥18.5px | Medium |
| Color not sole indicator | 1.4.1 | No information conveyed by color alone — always paired with text, icon, pattern, or position | High |
| Text resize | 1.4.4 | Interface usable at 200% browser zoom without loss of content or functionality | Medium |
| Reflow | 1.4.10 | Content reflows to single column at 320px width (no horizontal scrolling for text) | Medium |
| Non-text contrast | 1.4.11 | UI components and graphical objects have ≥ 3:1 contrast against background | Medium |
| Text spacing | 1.4.12 | Content readable with increased line-height (1.5x), letter-spacing (0.12em), word-spacing (0.16em) | Low |

### Operable (Principle 2)

Users must be able to operate all UI components and navigation.

| Criterion | WCAG | What to check | Severity |
|-----------|------|---------------|----------|
| Keyboard accessible | 2.1.1 | All functionality available via keyboard (Tab, Enter, Space, Escape, Arrow keys) | Critical |
| No keyboard traps | 2.1.2 | User can navigate away from every component using keyboard | Critical |
| Focus visible | 2.4.7 | Visible focus indicator on all interactive elements when navigating by keyboard | High |
| Focus order | 2.4.3 | Tab order follows logical reading/interaction order | High |
| Skip navigation | 2.4.1 | "Skip to main content" link available for keyboard users | Medium |
| Page titles | 2.4.2 | Each page has a descriptive, unique `<title>` | Medium |
| Link purpose | 2.4.4 | Link text describes destination (not "click here") | Medium |
| Heading structure | 2.4.6 | Headings describe content and follow hierarchical order (h1 → h2 → h3) | Medium |
| Pointer gestures | 2.5.1 | Multi-point or path-based gestures have single-pointer alternative | Medium |
| Target size | 2.5.5 | Interactive targets are at least 44x44 CSS pixels | Medium |
| Motion actuation | 2.5.4 | Motion-triggered actions (shake, tilt) can be disabled and have alternative | Low |
| Timing adjustable | 2.2.1 | Time limits can be extended or disabled (10x minimum extension) | High |

### Understandable (Principle 3)

Users must be able to understand information and UI operation.

| Criterion | WCAG | What to check | Severity |
|-----------|------|---------------|----------|
| Language of page | 3.1.1 | Page `lang` attribute set correctly | Medium |
| Error identification | 3.3.1 | Errors identified and described to user in text | High |
| Labels or instructions | 3.3.2 | Form inputs have visible labels (not just placeholders) | High |
| Error suggestion | 3.3.3 | Error messages suggest how to fix the problem | Medium |
| Error prevention | 3.3.4 | Submissions that cause legal/financial commitments can be reviewed, confirmed, or reversed | High |
| Consistent navigation | 3.2.3 | Navigation appears in same relative order across pages | High |
| Consistent identification | 3.2.4 | Components with same function have same label across pages | High |

### Robust (Principle 4)

Content must be robust enough for diverse user agents and assistive technologies.

| Criterion | WCAG | What to check | Severity |
|-----------|------|---------------|----------|
| Valid HTML | 4.1.1 | No duplicate IDs, proper nesting, complete start/end tags | Medium |
| Name, role, value | 4.1.2 | All UI components have accessible name, role, and value (via native HTML or ARIA) | High |
| Status messages | 4.1.3 | Status messages (success, error, progress) announced to assistive tech without receiving focus | High |

## Grep Patterns for Automated Detection

### HTML / JSX

| Pattern | Issue | WCAG |
|---------|-------|------|
| `<img` without `alt=` | Missing text alternative | 1.1.1 |
| `<img alt="">` on non-decorative image | Empty alt on meaningful image | 1.1.1 |
| `<input` without associated `<label` or `aria-label` | Unlabeled form field | 3.3.2 |
| `placeholder=` as only label for `<input` | Placeholder-as-label (disappears on focus) | 3.3.2 |
| `<a` with `href` containing only icon child (no text, no `aria-label`) | Unlabeled link | 2.4.4 |
| `<button` with only icon child (no text, no `aria-label`) | Unlabeled button | 4.1.2 |
| `onClick` on `<div>` or `<span>` without `role="button"` and `tabIndex` | Non-semantic interactive element | 2.1.1, 4.1.2 |
| `tabindex` value > 0 | Positive tabindex overrides natural order | 2.4.3 |
| `tabindex="-1"` on visible interactive element | Removed from keyboard tab order | 2.1.1 |
| `aria-hidden="true"` on element containing visible text | Content hidden from screen readers | 4.1.2 |
| `role="presentation"` on interactive element | Interactive element marked as decorative | 4.1.2 |
| `<h1` to `<h6` in non-sequential order (e.g., h1 → h3 skipping h2) | Heading hierarchy broken | 2.4.6 |

### CSS

| Pattern | Issue | WCAG |
|---------|-------|------|
| `outline: none` or `outline: 0` on `:focus` | Removed focus indicator | 2.4.7 |
| `user-select: none` on text content | Text not selectable (assistive tech barrier) | — |
| `display: none` or `visibility: hidden` on content that should be screen-reader accessible | Content hidden from all including assistive tech | 4.1.2 |
| Color values used without text/icon accompaniment for status | Color-only indicator | 1.4.1 |
| `font-size` in absolute units (`px`) without relative alternative | May not scale with browser zoom | 1.4.4 |
| `max-width` or `overflow: hidden` on text containers without ellipsis | Text may be clipped at zoom | 1.4.4 |
| `animation` without `prefers-reduced-motion` media query | Motion sensitivity not respected | 2.3.1 |

### Streamlit-Specific

| Pattern | Issue | WCAG |
|---------|-------|------|
| `st.image(` without `caption=` parameter | Image without alt text equivalent | 1.1.1 |
| `st.plotly_chart(` or `st.altair_chart(` without accessible title/description | Chart without text alternative | 1.1.1 |
| `st.color_picker` as sole input mechanism for categorical data | Color-only interaction | 1.4.1 |

## Demographic Bias Assessment

Based on Gergle et al. (CHI 2018 Best Paper; CHI 2022 Best Paper Honorable Mention):

### Bias Categories to Evaluate

| Category | What to look for | Example |
|----------|-----------------|---------|
| **Age bias** | Interface assumes digital-native interaction patterns (swipe, multi-touch, small text) | Data-dense dashboards with tiny labels that assume young eyes |
| **Gender bias** | Default avatars, pronouns, or color coding that assumes gender | Pink/blue color schemes for demographic data |
| **Cultural bias** | Color meanings, date formats, reading direction, iconography that assumes Western conventions | Red = danger (in West); Red = luck/prosperity (in East Asia) |
| **Ability bias** | Interaction patterns that require specific physical capabilities | Drag-and-drop as only mechanism for reordering |
| **Expertise bias** | Interface assumes domain knowledge without scaffolding | Statistical abbreviations (xG, VAEP, xT) without tooltips |
| **Data representation bias** | Visualization choices that advantage certain groups or perspectives | Bar charts that always show the same group first; default sort that privileges certain demographics |

### Evaluation Procedure

1. **Identify all user-facing data visualizations**
2. For each, ask: "Whose perspective does the default view privilege?"
3. Check: are defaults neutral, or do they embed a viewpoint?
4. Check: can the user change the perspective (sort, filter, group by)?
5. Flag any visualization where the default view systematically advantages or disadvantages a demographic group

## Assistive Technology Compatibility

### Screen Reader Basics

| Requirement | How to verify | Fix |
|------------|---------------|-----|
| All interactive elements have accessible names | Check `aria-label`, `aria-labelledby`, or visible text | Add `aria-label` or associate a `<label>` |
| Dynamic content updates are announced | Check for `aria-live` regions | Add `aria-live="polite"` to status update containers |
| Modal dialogs trap focus correctly | Tab through modal — focus should not leave until closed | Add focus trap logic |
| Error messages are associated with fields | Check for `aria-describedby` linking error to input | Add `aria-describedby` pointing to error element |
| Form validation results are announced | Check that validation messages appear in `aria-live` region | Wrap validation feedback in `aria-live` container |

### Keyboard Navigation Matrix

For each page, verify these keyboard interactions work:

| Key | Expected Behavior |
|-----|-------------------|
| Tab | Move to next interactive element in logical order |
| Shift+Tab | Move to previous interactive element |
| Enter | Activate button/link, submit form |
| Space | Activate button, toggle checkbox, select option |
| Escape | Close modal/dialog, cancel action, deselect |
| Arrow keys | Navigate within widget (dropdown, radio group, tab bar, slider) |
| Home/End | Move to first/last item in list or start/end of text |

### Testing Tools (Free)

| Tool | Purpose | How to use |
|------|---------|-----------|
| **axe DevTools** (browser extension) | Automated WCAG checking | Run on each page; review violations |
| **Lighthouse Accessibility** (Chrome DevTools) | Automated WCAG scoring | DevTools → Lighthouse → Accessibility |
| **WAVE** (browser extension) | Visual accessibility evaluation | Highlights issues directly on the page |
| **Colour Contrast Analyser** (desktop app) | Precise contrast ratio checking | Eyedropper tool for any color pair |
| **NVDA** (Windows screen reader, free) | Screen reader testing | Navigate interface with screen reader active |
| **VoiceOver** (macOS/iOS built-in) | Screen reader testing | Cmd+F5 to activate; navigate with VO keys |
| **Keyboard only** | Manual keyboard testing | Unplug mouse; complete every task with keyboard |
