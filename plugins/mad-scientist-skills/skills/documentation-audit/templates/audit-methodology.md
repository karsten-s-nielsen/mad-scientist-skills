# Audit Methodology Reference

## Purpose

This template codifies HOW to conduct an effective documentation audit — not what to check (that's in the SKILL.md phases) but how to observe, record, and analyze findings with methodological rigor. Derived from Lemov's instructional techniques (*Teach Like a Champion 3.0*, 2021), adapted for documentation auditing.

## Pre-audit checklist

Before starting, define:

- [ ] The specific questions this audit must answer (Exit Ticket)
- [ ] The 3 most likely documentation failures for this project type (Plan for Error)
- [ ] The pass sequence order (structure first, then language, then pedagogy)

**This template is portable** — it can be loaded by any audit skill (security-audit, optimization-audit, cognitive-interface-audit, observability-audit) to improve audit execution quality.

## Exemplar Planning (Lemov #1)

Before auditing any document element, write the ideal version first.

**Why it works:**
- Frees working memory for defect detection — you stop holding "what good looks like" in your head and can allocate full attention to perceiving what's actually on the page
- Prevents inattentional blindness (Chabris & Simons) — you only see deviations from a standard you've committed to writing. Errors you haven't predicted are invisible
- Increases follow-through 3x (Clear, *Atomic Habits*) — specifying what right looks like in advance is an implementation intention

**How to apply:**
1. Before auditing a tutorial, write a 2-3 sentence exemplar of what its introduction should contain
2. Before auditing a reference page, write the exemplar entry for one representative item
3. Compare actual documentation against the written exemplar, not against an internalized sense of quality
4. Bounded scope: write exemplars for the 2-3 most critical document types, not every document

**The written-not-mental distinction is load-bearing.** An exemplar in your head competes for working memory with the observation task. An exemplar on paper (or screen) frees that capacity entirely.

## Plan for Error (Lemov #2)

Before starting an audit pass, predict the 3-5 most likely documentation defects.

**Why it works:**
- Predicted errors get detected and acted on. Unpredicted errors get "buried" — the auditor sees them but doesn't act because no corrective response was pre-planned
- Planning the corrective action in advance makes deviation from the audit plan feel like following a plan rather than abandoning one
- The expert-novice perceptual gap (Chi, Glaser & Feltovich 1981): experts categorize problems by deep structure; novices by surface features. Planning errors by framework category (not "typo" but "expert blind spot") improves diagnostic accuracy

**How to apply:**
1. Before each audit pass, write 3-5 error hypotheses: "I expect to find [error type] because [reasoning]"
2. Write if/then contingencies: "If I find [error type], I will [corrective action]"
3. Track error frequency as a histogram — tick marks against the pre-planned list — not as a narrative list
4. After the pass, review the histogram: which error categories had the highest frequency? That's the systemic issue

## Standardize the Format (Lemov #8)

Design audit instruments so the auditor always looks in the same place for the same data.

**Why it works:**
- Observation is data collection. Inconsistent formats consume working memory on search rather than analysis
- "The more consistent the appearance and placement of the data, the more you will be able to focus on what it's telling you. You perceive more accurately, remember more of what you see, and think more productively about it" (Lemov)

**How to apply:**
- Use the same structured worksheet for every document reviewed — same criteria in the same positions
- When reviewing multiple documents of the same type, use a comparison grid with fixed columns
- For audit reports, use the Phase 9 report template consistently — readers develop expectations about where to find information

## Active Observation (Lemov #9)

Conduct sequential passes with a single focus per pass.

**Three observation options:**
1. **Immediate remediation**: Fix Critical/High issues as you find them (good for urgent defects)
2. **Deferred analysis**: Complete the full observation pass, then analyze patterns (good for systemic issues — you see the full picture before acting)
3. **Targeted deep attention**: Focus on specific documents or sections only (good for complex or high-risk content)

**Why single-focus passes:**
Working memory cannot effectively evaluate linguistic precision, structural taxonomy, pedagogical scaffolding, and consistency simultaneously. Each pass reduces to one question: "Does this document [one specific criterion]?"

**Written tracking is mandatory:**
"Working memory is small; even the slightest distractions cause us to forget what we're trying to remember. In an environment as complex as a codebase, there's really no such thing as taking mental notes." (Lemov)

**Error tracking as histogram:**
Track the NATURE of errors via tick marks against a pre-planned list (from Plan for Error). By the time you finish a pass, you have a frequency distribution showing where documentation quality breaks down systematically — not just a list of individual defects.

## Everybody Writes / Formative Before Summative (Lemov #38)

Explore what MIGHT be unclear before judging whether documentation MEETS the standard.

**The formative/summative distinction:**
- **Formative questions** (exploratory): "What might a developer misunderstand here?" / "What questions does this doc leave unanswered?" / "What would confuse someone seeing this for the first time?"
- **Summative questions** (judgmental): "Does this document meet the completeness standard?" / "Is this tutorial contract fulfilled?"

**Why formative first:**
Formative exploration produces more useful findings than binary pass/fail assessment. The "might" framing lowers stakes and opens analytical thinking — you notice possibilities rather than rendering verdicts.

**How to apply:**
Before filling in the audit checklist (summative), read the document with a formative lens. Take notes on what MIGHT be confusing, missing, or misleading. Then use those formative notes to inform the checklist assessment. The formative pass takes 2-3 minutes; the improvement in finding quality is substantial.

## Stretch It / Follow-Up Questions (Lemov #17)

When reviewing findings with documentation authors, use six categories of follow-up questions:

| Category | Question Pattern | Purpose |
|----------|-----------------|---------|
| **How or why** | "Why did you choose this approach over X?" | Tests whether the author understands the reasoning, or just wrote what worked |
| **Another way** | "Can you explain this for a reader who doesn't know the domain?" | Forces perspective-taking — exposes expert blind spots |
| **Better word** | "Is 'process' the right term, or is this specifically a thread, goroutine, daemon?" | Pushes from natural language to precise technical vocabulary |
| **Evidence** | "What would go wrong if someone skipped step 4?" | Separates assertion from tested knowledge — reveals gaps in the author's own understanding |
| **Integrate** | "How does this relate to the error handling in the adjacent section?" | Tests cross-document coherence |
| **New setting** | "Does this still hold in a multi-region deployment?" | Tests generality — reveals documentation that is accidentally narrow |

**Directedness spectrum:**
- Nondirective: "Say more about the failure case" (open-ended — reveals what the author thinks is important)
- Semi-directive: "Tell me more about what happens when the connection pool is exhausted" (guided — tests a specific hypothesis)
- Fully directive: "Explain the exact error message and recovery steps for a pool exhaustion scenario" (precise — demands specific content)

Choose directedness based on whether you want to discover gaps (nondirective) or confirm specific hypotheses (directive).

## Exit Ticket / Session Boundaries (Lemov #26)

Define what the audit session should answer BEFORE starting.

**The Snodgrass inversion:** Write the "exit ticket" first — what specific questions should you be able to answer after this audit pass? This forces clarity about the session's objective before diving into documents.

**Three-pile sort at session end:**
Categorize each finding: **Clear Pass** / **Needs Revision** / **Critical Defect**. The Critical Defect pile is addressed first in the next session or communicated to the author immediately.

**Performance vs. learning caveat:**
A document that passes an expert audit does not mean users will successfully execute the procedures. Audit review (expert judgment) and user testing (actual readers attempting tasks) measure different things. An audit organization that relies only on expert review, without any user testing loop, is systematically misreading "apparent adequacy" as usability.
