# Linguistic Rules Reference

## Purpose

Answer: "Does every sentence earn its place?"

## Pre-audit checklist

Before auditing, identify:

- [ ] Whether the project has an existing style guide or Vale config
- [ ] The target audience's expected reading level
- [ ] Which documents are user-facing (subject to style checks) vs. internal (exempt)

This reference provides grep-testable patterns for common linguistic anti-patterns in technical documentation. Rules are drawn from three authoritative sources:

1. **Strunk & White** — *The Elements of Style* (rules of composition and word usage)
2. **Google Developer Documentation Style Guide** — audience-focused technical writing standards
3. **Microsoft Writing Style Guide** — tone, inclusivity, and globalization standards

Each rule includes a regex pattern for automated detection, an example violation, and its corrected form. Rules marked "requires manual check" need human judgment; the regex serves only as a heuristic signal.

---

## Strunk & White Rules

### Rule 5 — No Comma Splice

- **Pattern:** `,[^"]*\b(he|she|it|they|we|I|the|this|that|these|those|a|an)\b`
- **Violation:** "The server crashed, the logs were lost."
- **Corrected:** "The server crashed, and the logs were lost." / "The server crashed; the logs were lost."
- **Exception:** Comma-separated short imperative clauses: "Click Save, then close the dialog."

### Rule 7 — Dangling Modifier

- **Pattern:** `-ing\b.*,` (sentence-initial participial phrase)
- **Violation:** "Running the migration, the database was corrupted."
- **Corrected:** "Running the migration, the team corrupted the database." / "While the team ran the migration, the database was corrupted."
- **Exception:** Established gerund phrases where the subject is unambiguous from context.

### Rule 10 — Use Active Voice

- **Pattern:** `\b(was|were|is|are|been|being)\s+(performed|configured|created|managed|executed|implemented|deployed|updated|generated|established)\b`
- **Violation:** "The deployment was performed by the CI pipeline."
- **Corrected:** "The CI pipeline performed the deployment."
- **Exception:** See Permitted Exceptions section below.

### Rule 11 — Put Statements in Positive Form

- **Pattern (double negatives):** `\bnot\s+(un|in|im|ir|dis|a)\w+` — flags double negatives where an antonym exists
- **Pattern (hedging negatives):** `\bnot\s+(very|often|always|entirely|completely)\b`
- **Violation:** "He did not remember" / "not infrequently"
- **Corrected:** "He forgot" / "frequently"
- **Exception:** Deliberate litotes for rhetorical emphasis in release notes or changelogs.

### Rule 12 — Use Specific, Concrete Language

- **Pattern:** `\b(various|several|aspects|issues|things|areas|elements|stuff|certain|appropriate)\b`
- **Violation:** "There are various issues with the configuration."
- **Corrected:** "The configuration contains three syntax errors and one missing required field."
- **Exception:** Introductory sentences that immediately follow with specifics: "Several factors affect performance: CPU, memory, and I/O."

### Rule 13 — Omit Needless Words

- **Pattern:** `\b(in order to|the fact that|due to the fact that|it should be noted|for the purpose of|he is a man who|she is a woman who|the question as to whether|used for .* purposes|in a .* manner)\b`
- **Violation:** "In order to deploy, run the script." / "Due to the fact that the server crashed..."
- **Corrected:** "To deploy, run the script." / "Because the server crashed..."
- **Exception:** Legal or compliance text where exact phrasing is mandated.

### Rule 15 — Use Parallel Construction

- **Pattern:** Detect list items mixing verb forms (requires manual check) — look for lists where items alternate between gerunds (`-ing`), infinitives (`to + verb`), and bare imperatives
- **Violation:** "The system handles: logging errors, to retry failed requests, and validates input."
- **Corrected:** "The system handles: logging errors, retrying failed requests, and validating input."
- **Exception:** Mixed-form lists that are direct quotations from external specifications.

### Rule 17 — Tense Consistency

- **Pattern:** Detect tense shifts within a section (requires manual check) — look for past-tense verbs (`-ed`) and present-tense verbs within the same paragraph describing the same action
- **Violation:** "The function calculates the hash. It returned the digest."
- **Corrected:** "The function calculates the hash. It returns the digest."
- **Exception:** Describing historical context followed by current behavior: "v1 used MD5. v2 uses SHA-256."

### Rule 18 — Place Emphatic Words at End

- **Pattern:** `(however|also|as well|too|etc)\.\s*$` — weak sentence endings
- **Violation:** "The API supports pagination, however." / "The config supports JSON, YAML, etc."
- **Corrected:** "However, the API supports pagination." / "The config supports JSON and YAML."
- **Exception:** "etc." is acceptable when an exhaustive list would be impractical and the pattern is clear to the reader.

---

## Google Developer Documentation Style Guide Rules

### Conditions Before Instructions

- **Pattern:** `\b(click|run|enter|type|select|open|press)\b.*\b(if|when|unless|before|after)\b`
- **Violation:** "Click Submit if you are ready to deploy."
- **Corrected:** "When you are ready to deploy, click Submit."

### Use Second Person

- **Pattern:** `\bwe\s+(can|should|must|need|will|are|have|recommend)\b`
- **Violation:** "We need to configure the server."
- **Corrected:** "You need to configure the server." / "Configure the server."

### Use Timeless Language

- **Pattern:** `\b(currently|now|new|recently|soon|latest|upcoming|at this time|at the moment)\b`
- **Violation:** "The API now supports pagination."
- **Corrected:** "The API supports pagination."

### Use Inclusive Terminology

- **Pattern:** `\b(whitelist|blacklist|master|slave|sanity\s*check|dummy|grandfather|man-?hours?|guys|cripple|blind\s*spot|kill|hang|abort|native)\b`
- **Violation:** "Add the IP to the whitelist."
- **Corrected:** "Add the IP to the allowlist."

### Sentence Length

- **Pattern:** Count words per sentence (automated: split on `[.!?]`, count tokens > 26)
- **Violation:** "The configuration file that is located in the root directory of the project and is used by the build system to determine which modules to include must be updated before deploying." (33 words)
- **Corrected:** "The build system reads the configuration file from the project root directory. Update this file before deploying to specify which modules to include."

### Descriptive Link Text

- **Pattern:** `\[(click here|here|this page|this link|this article|link|read more)\]`
- **Violation:** "For details, see [this page](url)."
- **Corrected:** "For details, see [Configuring TLS](url)."

### Meaningful Alt Text

- **Pattern (empty):** `!\[\s*\]\(` — empty alt text
- **Pattern (generic):** `!\[(image|screenshot|picture|photo|icon)\]\(` — generic alt text
- **Violation:** `![screenshot](deploy.png)`
- **Corrected:** `![Deployment pipeline showing three stages: build, test, and release](deploy.png)`

### Code Formatting

- **Pattern:** `` [^`]\b(true|false|null|nil|None|undefined|NaN|stderr|stdout|stdin)\b[^`] `` — common literals not in code font
- **Violation:** "Set the value to true."
- **Corrected:** "Set the value to `true`."

---

## Microsoft Writing Style Guide Rules

### Contractions Are OK

- **Pattern:** `\b(do not|does not|is not|are not|was not|were not|will not|cannot|could not|should not|would not|have not|has not|had not)\b` — flag for possible contraction
- **How it differs from Google:** Google permits but does not encourage contractions; Microsoft actively recommends them.

### UI Terminology

- **Pattern:** `\b(click on|hit|punch|push)\b` (when describing UI interaction)
- **How it differs from Google:** Google uses "click" broadly; Microsoft distinguishes "select" (for options/checkboxes) from "enter" (for text input).

### Bias-Free Communication

- **Pattern:** `\b(normal\s+user|crazy|insane|lame|crippled|blind\s+to|deaf\s+to|dumb\s+terminal)\b`
- **How it differs from Google:** Microsoft provides more detailed guidance on disability-related language than Google.

### Global-Ready Writing

- **Pattern:** `\b(out of the box|under the hood|at the end of the day|low-hanging fruit|boil the ocean|move the needle|circle back|deep dive|best of breed|apples? to (apples?|oranges?))\b`
- **How it differs from Google:** Google mentions localization; Microsoft provides a comprehensive global-ready checklist.

### Oxford Comma Required

- **Pattern:** `\b\w+,\s+\w+\s+(and|or)\s+\w+\b` — list of 3+ items without Oxford comma (requires manual verification of missing comma before conjunction)
- **How it differs from Google:** Google also requires the Oxford comma; Microsoft explicitly mandates it in all contexts including UI strings.

---

## Inclusive Language Substitutions

| Term to Avoid | Replacement | Source |
|---------------|-------------|--------|
| whitelist | allowlist | Google Developer Documentation Style Guide |
| blacklist | denylist, blocklist | Google Developer Documentation Style Guide |
| master (branch) | main | Google Developer Documentation Style Guide, Microsoft Writing Style Guide |
| slave | replica, secondary, worker | Google Developer Documentation Style Guide, Microsoft Writing Style Guide |
| master/slave | primary/replica, leader/follower, controller/agent | Google Developer Documentation Style Guide |
| sanity check | confidence check, coherence check, quick verification | Google Developer Documentation Style Guide |
| dummy value | placeholder value, sample value, test value | Google Developer Documentation Style Guide |
| grandfathered | legacy, exempt | Microsoft Writing Style Guide |
| man-hours | person-hours, engineering hours | Microsoft Writing Style Guide |
| guys | everyone, folks, people, team | Microsoft Writing Style Guide |
| cripple | disable, impair, limit | Microsoft Writing Style Guide, alex linter |
| blind spot | oversight, gap, unexamined area (in prose context) | alex linter |
| kill (a process) | stop, terminate, end, cancel | Google Developer Documentation Style Guide, alex linter |
| hang (a process) | stop responding, become unresponsive, freeze | alex linter |
| abort | cancel, stop, end, halt | Google Developer Documentation Style Guide, alex linter |
| native (feature) | built-in, integrated | alex linter |

---

## Permitted Exceptions

When rules may be intentionally violated — each exception must be documented with the rationale in the audit report.

- **Passive voice is permitted when:**
  - Emphasizing the object over the actor: "The configuration file is loaded at startup" — the file matters more than the loader
  - The actor is genuinely unknown or irrelevant: "The vulnerability was discovered in 2019"
  - Avoiding blaming the user: "50 merge conflicts were found" is preferable to "You created 50 merge conflicts"
  - Describing system behavior from the user's perspective: "Your request is being processed"

- **"currently" is permitted when:**
  - Describing a known temporary state that is documented as temporary and has a linked tracking issue (e.g., "The API currently returns XML — see #1234 for JSON migration")
  - The word is removed once the temporary state resolves

- **Code identifiers are exempt from inclusive language rules when:**
  - The term appears in code-font (backticks) and references an actual identifier in source code that uses the legacy term: `` `master` branch in the `legacy-auth` repository``
  - Prose surrounding the code reference must use the inclusive alternative: "the primary branch (`master`) in the legacy-auth repository"
  - New code and new documentation must always use inclusive terms

- **Quotations are exempt when:**
  - Quoting external sources, specifications, or error messages that use non-inclusive language
  - The quotation is clearly attributed and set apart (blockquote or inline quotes)
  - Commentary surrounding the quotation uses inclusive language

- **Vague quantifiers ("several", "various") are permitted when:**
  - Immediately followed by a specific enumeration: "Several factors affect latency: network round-trip time, serialization overhead, and queue depth"
  - The exact count is genuinely unknown and an approximation is more honest than a fabricated number

- **Sentence length may exceed 26 words when:**
  - The sentence contains a code example or command that cannot be broken without losing clarity
  - The sentence is a single list introduced by a colon (the list items add length but not complexity)
