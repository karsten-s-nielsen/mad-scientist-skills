# mad-scientist-skills

![Mad Scientist Skills](assets/mad-scientist.jpg)

[![CI](https://github.com/karsten-s-nielsen/mad-scientist-skills/actions/workflows/ci.yml/badge.svg)](https://github.com/karsten-s-nielsen/mad-scientist-skills/actions/workflows/ci.yml)
[![Version](https://img.shields.io/badge/version-1.23.0-blue)](CHANGELOG.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[Claude Code](https://docs.anthropic.com/en/docs/claude-code) skills are slash-command capabilities that extend Claude Code with specialized knowledge. Install this plugin to get 9 skills for architecture auditing, architecture diagramming, code security analysis, performance optimization, pre-change measurement gating, observability assessment, documentation evaluation, cognitive interface review, and pre-commit quality checks.

## Skills

| Skill | Description | Invoke |
|-------|-------------|--------|
| **architecture-audit** | Assess architectural patterns, dependency direction, bounded contexts, SOLID compliance, and structural health (beta) | `/mad-scientist-skills:architecture-audit` |
| **c4** | Generate interactive C4 architecture diagrams as self-contained HTML | `/mad-scientist-skills:c4` |
| **cognitive-interface-audit** | Find usability problems, mental model gaps, cognitive overload, and accessibility violations | `/mad-scientist-skills:cognitive-interface-audit` |
| **documentation-audit** | Evaluate documentation quality, structure, clarity, completeness, and audience fit | `/mad-scientist-skills:documentation-audit` |
| **final-review** | Pre-commit quality gate with code review, documentation check, and architecture diagram | `/mad-scientist-skills:final-review` |
| **measure-before-optimize** | Pre-change measurement gate for perf-sensitive functions — captures baseline and verifies regression stays within threshold | `/mad-scientist-skills:measure-before-optimize` |
| **observability-audit** | Assess monitoring maturity across logging, metrics, tracing, alerting, and SLI/SLO coverage | `/mad-scientist-skills:observability-audit` |
| **optimization-audit** | Find performance bottlenecks in algorithms, queries, caching, concurrency, and cloud cost | `/mad-scientist-skills:optimization-audit` |
| **security-audit** | Identify vulnerabilities via threat modeling, code scanning, dependency audit, and infrastructure review | `/mad-scientist-skills:security-audit` |

## Prerequisites

- **[Claude Code](https://docs.anthropic.com/en/docs/claude-code)** — the AI coding assistant this plugin extends. Install it first.
- **Java 21+** — required only by the c4 skill for local Structurizr/PlantUML rendering. Both `structurizr.war` and `plantuml.jar` are auto-downloaded on first use.
- **Graphviz** — also required only by the c4 skill, and a hard prerequisite on par with Java: PlantUML's C4 layout is `dot`-based, and without it PlantUML emits a "Cannot find Graphviz" placeholder **with exit code 0** rather than failing outright. Install with `winget install -e --id Graphviz.Graphviz` (Windows), `brew install graphviz` (macOS), or `apt install graphviz` (Debian/Ubuntu). Verify with `java -jar ~/.claude/tools/plantuml.jar -testdot` — **not** `which dot`, since PlantUML resolves `dot` through its own search paths and an installed Graphviz that is absent from `PATH` works fine.

All other skills have no external dependencies.

> **Safety note:** All audit skills perform read-only analysis — they scan your code and produce a findings report but do not modify files. Only `final-review` and `c4` produce output files (`architecture.html`, `architecture.dsl`).

## Installation

Add the marketplace (one-time):

```
/plugin marketplace add karsten-s-nielsen/mad-scientist-skills
```

Install the plugin:

```
/plugin install mad-scientist-skills@mad-scientist-skills
```

Verify by invoking any skill:

```
/mad-scientist-skills:security-audit
```

To uninstall:

```
/plugin uninstall mad-scientist-skills@mad-scientist-skills
```

**Troubleshooting:**
- **"Unknown command /plugin"** — update Claude Code to the latest version (plugin support is required).
- **Marketplace add fails** — check your internet connection. The marketplace name must be exactly `karsten-s-nielsen/mad-scientist-skills`.
- **Plugin install fails** — try removing and re-adding the marketplace, then install again.

## Quick Start

Run a security audit on your current project:

```
/mad-scientist-skills:security-audit
```

Or ask naturally: *"Run a security audit on this project"*

Each audit skill scans your codebase phase-by-phase and produces a severity-rated findings report:

| # | Severity | Phase | File:Line | Description | Status |
|---|----------|-------|-----------|-------------|--------|
| 1 | High | Phase 4 | src/auth.py:42 | Hardcoded credential in source code | Open |
| 2 | Medium | Phase 3 | Dockerfile:1 | Container running as root user | Open |

Critical and High issues are fixed during the audit when possible. The full report includes a maturity rating and deployment readiness assessment.

## Skill Details

<details>
<summary><strong>architecture-audit</strong> — Architecture Audit (beta: patterns, dependencies, bounded contexts, SOLID, coupling)</summary>

Two-mode, single-tier architecture analysis: **planning** (before code) and **audit** (existing code). Grounded in Hexagonal Architecture (Cockburn), Domain-Driven Design (Evans/Vernon), Clean Architecture (Martin), SOLID principles, Enterprise Integration Patterns (Hohpe & Woolf), CQRS/Event Sourcing (Young/Fowler), Twelve-Factor App (Wiggins), API-First Design, and Architectural Decision Records (Nygard).

### Coverage

| Phase | Area | Planning | Audit |
|-------|------|:--------:|:-----:|
| 0 | Anti-pattern scanning (circular imports, god modules, framework leaks, mixed abstractions) | | x |
| 1 | Architectural surface discovery | x | x |
| 2 | Architectural pattern detection (hexagonal, clean, layered, medallion, CQRS, event sourcing, API-first) | | x |
| 3 | Dependency direction analysis | x | x |
| 4 | Bounded context assessment (DDD strategic patterns) | x | x |
| 5 | Domain model quality (archetype-adapted) | | x |
| 6 | SOLID compliance | | x |
| 7 | Coupling and cohesion analysis | | x |
| 8 | CQRS, event sourcing, twelve-factor, API-first (conditional) | x | x |
| 9 | Architectural decision records | x | x |
| 10 | Findings report | x | x |

### Usage

Ask naturally ("Architecture audit this project", "Review the architecture", "SOLID audit") or invoke directly:

```
/mad-scientist-skills:architecture-audit
```

</details>

<details>
<summary><strong>c4</strong> — C4 Architecture Diagrams (rendering pipeline, diagram types, templates)</summary>

Generates interactive, self-contained HTML architecture diagrams using the [C4 model](https://c4model.com/) and [Structurizr DSL](https://docs.structurizr.com/dsl).

### Rendering pipeline

Structurizr DSL → structurizr.war export → PlantUML C4 → plantuml.jar → SVG → embedded HTML

### What it produces

A single HTML file with:
- Tabbed navigation between C4 diagram levels, ordered as the DSL declares them
- Embedded SVGs (no CDN or runtime dependencies), with repeated text styling hoisted into shared CSS classes — roughly 35% smaller than the raw PlantUML output, pixel for pixel identical
- Copyable Structurizr DSL source panel
- Dark theme — open in any browser

Assembly also prints non-fatal readability warnings: views above ~15 element boxes, element descriptions above 200 characters, and any container or software system whose decomposition renders in no view.

A companion `.dsl` source file for version control.

### Diagram types

| Level | What it shows |
|-------|---------------|
| **System Context** | People, your system, and external dependencies |
| **Container** | Applications, databases, queues, and their protocols |
| **Component** | Internal structure of a single container |
| **Dynamic** | Numbered interaction flows for specific scenarios |
| **Deployment** | Infrastructure, cloud regions, subnets, and scaling |

### Without Java

If Java 21+ is not available, the skill saves the `.dsl` source file. You can render it later with any Structurizr-compatible tool, including the [Structurizr web editor](https://structurizr.com).

### Assembler script

Includes `c4_assemble.py` — cleans rendered SVGs and assembles them into the HTML viewer. Auto-detects views from SVG filenames and verifies each SVG is clean before embedding. A non-fatal coverage lint warns when a software system declares containers, or a container declares components, that no view renders.

### Templates

| Template | Purpose |
|----------|---------|
| `system-context.md` | System Context diagram (Level 1) — people, systems, dependencies |
| `container.md` | Container diagram (Level 2) — applications, databases, protocols |
| `component.md` | Component diagram (Level 3) — internal container structure |
| `dynamic.md` | Dynamic diagram — numbered interaction flows |
| `deployment.md` | Deployment diagram — infrastructure, cloud regions, scaling |

### Usage

Ask naturally ("Create a C4 diagram for this project") or invoke directly:

```
/mad-scientist-skills:c4
```

</details>

<details>
<summary><strong>cognitive-interface-audit</strong> — Cognitive Interface Audit (coverage, frameworks, templates)</summary>

Two-mode, single-tier cognitive interface analysis: **planning** (before UI) and **audit** (existing UI). Grounded in seven academic research threads: task modeling and error tolerance (GOMS, Wood & Byrne, Rasmussen), visual grounding (Gergle, Kraut & Fussell), cognitive load (Sweller, Kahneman), gulf analysis (Norman), information foraging (Pirolli & Card), trust calibration (Lee & See), and ecological interface design (Vicente & Rasmussen). Also applies Kirk data visualization integrity, Cleveland & McGill visual encoding, Gestalt perceptual principles, and WCAG 2.1 AA accessibility standards.

### Coverage

| Phase | Area | Planning | Audit |
|-------|------|:--------:|:-----:|
| 0 | UI anti-pattern scanning (inconsistent labels, missing feedback, dead-end states) | | x |
| 1 | Cognitive surface discovery | x | x |
| 2 | Task model mapping (GOMS analysis, user expertise spectrum) | x | x |
| 3 | Consistency & convention | | x |
| 4 | Error tolerance (Wood 7-layer defense, Rasmussen SRK) | x | x |
| 5 | Cognitive load assessment (NASA-TLX, Sweller CLT) | x | x |
| 6 | Visual grounding, feedback & interpretation (Gergle grounding theory, Kirk data visualization integrity, Vicente & Rasmussen EID) | | x |
| 7 | Accessibility & inclusion (WCAG 2.1 AA, Kirk colour accessibility, demographic bias) | | x |
| 8 | Information architecture | | x |
| 9 | Findings report | x | x |

### Templates

| Template | Purpose |
|----------|---------|
| `task-model-analysis.md` | GOMS methodology, Norman's Gulfs, cognitive walkthrough, Dual-Process Theory, Cleveland & McGill visual encoding, user expertise spectrum |
| `error-tolerance-checklist.md` | Wood 7-layer defense, Rasmussen SRK, Reason's error mechanisms |
| `cognitive-load-assessment.md` | NASA-TLX scoring, Sweller CLT, information density heuristics, chart scalability/degradation |
| `visual-grounding-checklist.md` | Gergle grounding theory, feedback latency, Joint Action Storyboards, Trust Calibration, EID constraint visibility |
| `accessibility-inclusion.md` | WCAG 2.1 AA checklist, demographic bias, assistive technology |

### Usage

Ask naturally ("Audit the UI for this project", "Check usability", "Mental model review") or invoke directly:

```
/mad-scientist-skills:cognitive-interface-audit
```

</details>

<details>
<summary><strong>documentation-audit</strong> — Single-Tier Documentation Audit (coverage, frameworks, templates)</summary>

Two-mode, single-tier documentation analysis: **planning** (before docs exist) and **audit** (existing docs). Grounded in nine research threads: classical composition (Strunk & White), enterprise style standards (Google/Microsoft), structural taxonomy (Diataxis, Good Docs Project), Cognitive Load Theory (Sweller, Chandler & Sweller), minimalist instruction (Carroll), instructional techniques (Lemov), information foraging (Pirolli & Card), tactical empathy (Voss), and data visualization pedagogy (Kirk simplify-vs-clarify).

### Coverage

| Phase | Area | Planning | Audit |
|-------|------|:--------:|:-----:|
| 0 | Anti-pattern scanning (passive voice, needless words, inclusive language, structural pollution) | | x |
| 1 | Documentation surface discovery | x | x |
| 2 | Diataxis classification (quadrant identity, pollution detection, missing types) | x | x |
| 3 | Linguistic precision (Strunk & White, Google/Microsoft style rules, Voss empathy) | | x |
| 4 | Pedagogical scaffolding (CLT, Carroll, Merrill, Lemov techniques, Kirk simplify-vs-clarify) | x | x |
| 5 | Structural consistency (vocabulary, formatting, Voss voice tones, template adherence) | | x |
| 6 | Repository architecture (README, CONTRIBUTING, SECURITY, CHANGELOG, API docs) | | x |
| 7 | Audience calibration (expert blind spot, information scent, assumed context) | | x |
| 8 | Completeness & freshness (broken links, outdated content, missing gaps) | | x |
| 9 | Findings report | x | x |

### Templates

| Template | Purpose |
|----------|---------|
| `diataxis-checklist.md` | Quadrant classification, pollution detection, Good Docs Project extensions |
| `linguistic-rules.md` | Strunk & White rules, Google/Microsoft rules, grep patterns, inclusive language |
| `pedagogical-scaffolding.md` | Carroll's Minimalism, CLT, Merrill's First Principles, Lemov techniques with annotated work samples |
| `repo-architecture.md` | Essential file checklist with required sections |
| `audience-calibration.md` | Expert blind spot worksheet, information scent scoring, assumed context checklist |
| `audit-methodology.md` | Portable Lemov audit methodology (reusable by other audit skills) |

### Usage

Ask naturally ("Audit the docs", "Documentation review", "Check doc quality") or invoke directly:

```
/mad-scientist-skills:documentation-audit
```

</details>

<details>
<summary><strong>final-review</strong> — Pre-Commit Quality Gate (review phases, severity levels)</summary>

Reviews your entire project before you commit.

### What it does

1. **Codebase discovery** — reads project docs, identifies tech stack and architecture
2. **Code quality review** — consistency, best practices, dead code, type safety, security
3. **Documentation review** — ensures README, CLAUDE.md, and API docs match the actual code
4. **Architecture diagram** — generates or updates `architecture.html` using the c4 skill
5. **Verification summary** — structured report with issues found, fixes applied, and commit readiness

### Usage

Ask naturally ("Final review", "Check everything before commit") or invoke directly:

```
/mad-scientist-skills:final-review
```

</details>

<details>
<summary><strong>measure-before-optimize</strong> — Pre-Change Measurement Gate (workflow phases, parameters, optimization-audit comparison)</summary>

Captures a performance baseline before a change, waits for the change, re-measures, and reports the delta against the budget and a configurable regression threshold. Peer skill to `optimization-audit` — this one is pre-change, the other is retrospective.

### When to use

- Before modifying a function with a `pytest-benchmark` test
- Before modifying a function listed in a project's performance baselines file (e.g. `docs/performance-baselines.md`)
- Before modifying a function flagged as a hot path in `CLAUDE.md` or similar documents

### Workflow

1. **Identify** — locates the matching benchmark for the function being modified
2. **Capture baseline** — runs `pytest-benchmark` with `--benchmark-json` to a scratch file in `tempfile.gettempdir()` (never writes to the project root)
3. **Yield** — exits so the main agent can make the code change
4. **Re-measure** — runs the same benchmark after the change
5. **Compare and report** — delta in median and p95, position vs budget, regression threshold check

### Parameters

| Parameter | Default | Description |
|---|---|---|
| `baselines_file` | `docs/performance-baselines.md` | Path to the project's baselines file |
| `regression_threshold` | `10%` | Percent regression that escalates to user prompt |
| `budget_enforcement` | `warn` | `warn` (report and ask) or `block` (halt execution) |
| `benchmark_rounds` | `3` | `pytest-benchmark --benchmark-min-rounds` |

### Comparison to optimization-audit

| Attribute | optimization-audit | measure-before-optimize |
|---|---|---|
| Timing | Retrospective (after code exists) | Pre-change gate |
| Trigger | "Audit this codebase for perf issues" | "About to touch a measured function" |
| Scope | Whole codebase | Single function / small change |
| Action | Recommends fixes | Gates the change |

### Usage

Ask naturally ("Measure before I optimize this", "Check the baseline first") or invoke directly:

```
/mad-scientist-skills:measure-before-optimize
```

</details>

<details>
<summary><strong>observability-audit</strong> — Two-Tier Observability Audit (coverage, tiers, templates)</summary>

Two-mode, two-tier observability analysis: **planning** (before code) and **audit** (existing code/infra). Each phase has **Standard** (free/open-source tools) and **Enterprise** (paid observability platforms) tiers.

> **Standard vs Enterprise tier:** Some skills offer two tiers. Standard uses free/open-source tools and is always actionable. Enterprise lists paid platform recommendations (Datadog, Splunk, etc.) as an aspirational checklist.

### Coverage

| Phase | Area | Planning | Audit |
|-------|------|:--------:|:-----:|
| 0 | Anti-pattern scanning (print debugging, swallowed errors) | | x |
| 1 | Observability surface mapping | x | x |
| 2 | Instrumentation foundation (OpenTelemetry) | x | x |
| 3 | Structured logging | | x |
| 4 | Metrics & SLIs/SLOs | x | x |
| 5 | Distributed tracing | | x |
| 6 | Pipeline & data observability | x | x |
| 7 | ML/model observability (conditional) | x | x |
| 8 | Alerting & incident detection | x | x |
| 9 | Dashboard & visualization | | x |
| 10 | Health checks & readiness | | x |
| 11 | Cost & cardinality management | x | x |
| 12 | Findings report | x | x |

### Templates

| Template | Purpose |
|----------|---------|
| `otel-instrumentation.md` | OTel SDK setup, auto-instrumentation, exporters, Collector config |
| `structured-logging.md` | JSON logging, correlation IDs, PII scrubbing, log shipping |
| `metrics-sli-slo.md` | RED/USE methodology, SLI/SLO design, burn rate alerting |
| `distributed-tracing.md` | Context propagation, span design, sampling strategies |
| `pipeline-observability.md` | ETL/ELT health, dbt artifact parsing, data quality gates |
| `ml-model-observability.md` | Drift detection (PSI, CUSUM, KS test), model validation |
| `alerting-runbooks.md` | Alert design, runbook templates, escalation paths |

### Usage

Ask naturally ("Audit observability for this project", "Design telemetry strategy") or invoke directly:

```
/mad-scientist-skills:observability-audit
```

</details>

<details>
<summary><strong>optimization-audit</strong> — Single-Tier Optimization Audit (coverage, phases, templates)</summary>

Two-mode, single-tier optimization analysis: **planning** (before code) and **audit** (existing code/infra). Single tier because optimization tools are overwhelmingly free/open-source (profilers, EXPLAIN, load testers, linters).

### Coverage

| Phase | Area | Planning | Audit |
|-------|------|:--------:|:-----:|
| 0 | Anti-pattern scanning (algorithm, memory, concurrency, database, HTTP N+1, PyTorch/ML training, ingestion no-op waste, loop-invariant computation, logging) | | x |
| 0.5 | Documentation & tech debt scan (TODO/ROADMAP/PLAN keyword search) | | x |
| 1 | Performance surface discovery | x | x |
| 2 | Algorithm & data structure efficiency | | x |
| 3 | Memory management | | x |
| 4 | Concurrency & parallelism | | x |
| 5 | Database & query optimization | x | x |
| 6 | Caching strategy | x | x |
| 7 | Serialization & network | | x |
| 8 | Frontend & API optimization (conditional) | | x |
| 9 | Data pipeline efficiency (conditional) | x | x |
| 10 | Container & startup optimization (conditional) | | x |
| 11 | Cloud cost & right-sizing (conditional) | x | x |
| 12 | Profiling & benchmarking posture | x | x |
| 13 | Findings report | x | x |

### Templates

| Template | Purpose |
|----------|---------|
| `algorithm-complexity.md` | Big-O analysis, data structure selection, per-language profiling tools, redundant setup / cross-iteration caching red flags |
| `database-optimization.md` | N+1 detection, indexing strategies, query plans, connection pooling |
| `caching-strategies.md` | Cache architecture, invalidation patterns, stampede protection, HTTP caching |
| `concurrency-patterns.md` | Thread pool sizing, async/await correctness, lock contention, backpressure |
| `frontend-performance.md` | Core Web Vitals, bundle optimization, image optimization, API responses |
| `pipeline-efficiency.md` | Batch/streaming trade-offs, incremental processing, ingestion skip guards, Spark/dbt tuning, distributed execution (`applyInPandas`), redundant computation detection, loop-invariant computation in batch loops, remote container memory budget violations |
| `profiling-benchmarking.md` | Load testing tools, micro-benchmarking, regression detection in CI |
| `cloud-cost-optimization.md` | Right-sizing, auto-scaling, storage tiering, driver-vs-executor cost analysis, FinOps practices |

### Usage

Ask naturally ("Optimization audit this project", "Find bottlenecks", "Performance review") or invoke directly:

```
/mad-scientist-skills:optimization-audit
```

</details>

<details>
<summary><strong>security-audit</strong> — Two-Tier Security Audit (coverage, tiers, templates)</summary>

Two-mode, two-tier security analysis: **planning** (before code) and **audit** (existing code/infra). Each phase has **Standard** (free tools) and **Enterprise** (paid services) tiers.

### Coverage

| Phase | Area | Planning | Audit |
|-------|------|:--------:|:-----:|
| 0 | Anti-pattern scanning (incl. ML deserialization) | | x |
| 1 | Security surface mapping | x | x |
| 2 | STRIDE threat modeling (incl. cross-organizational boundaries) | x | |
| 3 | Infrastructure security (incl. confidential computing) | | x |
| 4 | OWASP Top 10 code scanning | | x |
| 4b | ML/AI model security (serialization, provenance, poisoning) | | x |
| 4c | HTML/SVG sanitizer bypass (regex denylists, XSS) | | x |
| 5 | Web security headers | | x |
| 6 | API boundary security | | x |
| 7 | Authentication & session management | x | x |
| 8 | Supply chain & dependency audit | | x |
| 9 | Secrets management | x | x |
| 10 | Data classification & AI regulatory compliance | x | x |
| 11 | Monitoring & incident response | x | x |
| 12 | Findings report | x | x |

### Templates

| Template | Purpose |
|----------|---------|
| `stride-threat-model.md` | STRIDE categories, trust boundaries (incl. cross-organizational), severity scoring |
| `infrastructure-hardening.md` | Cloud-agnostic + AWS/Azure/GCP/K8s hardening, confidential computing, privacy-preserving computation |
| `dependency-audit.md` | Per-ecosystem audit commands, lockfile integrity, SBOM |
| `web-security-headers.md` | HTTP security headers with framework-specific examples |
| `api-security-checklist.md` | Input validation, rate limiting, JWT security |
| `auth-session-checklist.md` | Password hashing, session management, OAuth/OIDC |

### Usage

Ask naturally ("Security audit this project", "Threat model the API") or invoke directly:

```
/mad-scientist-skills:security-audit
```

</details>

## Architecture

Open [`architecture.html`](architecture.html) in a browser to explore the C4 architecture diagrams — a tabbed, dark-themed viewer with embedded SVGs for System Context and Container levels. The companion [`architecture.dsl`](architecture.dsl) contains the Structurizr DSL source for version control.

## Adding Skills

To extend the plugin with your own skill:

1. Create a directory under `plugins/mad-scientist-skills/skills/`:

```
plugins/mad-scientist-skills/skills/
  my-new-skill/
    SKILL.md          # Skill definition (see CONTRIBUTING.md for format)
    templates/        # Optional supporting templates
```

2. Write `SKILL.md` with YAML frontmatter (`name`, `description`) and the skill body. See any existing skill for the pattern.

3. Commit, push, and re-install the plugin for the skill to be available:

```
/plugin uninstall mad-scientist-skills@mad-scientist-skills
/plugin install mad-scientist-skills@mad-scientist-skills
```

The skill is then available via `/mad-scientist-skills:my-new-skill`.

## Glossary

<details>
<summary>Expand term definitions</summary>

| Term | Definition |
|------|-----------|
| **C4 model** | A four-level approach to architecture diagramming: Context, Container, Component, Code ([c4model.com](https://c4model.com/)) |
| **Claude Code skill** | A slash-command capability bundled in a Claude Code plugin. Skills extend Claude Code with specialized knowledge and workflows |
| **Cognitive Load Theory** | Framework for managing how much information a reader must hold in working memory (Sweller 1988) |
| **Diataxis** | Documentation framework classifying content into four types: Tutorial, How-To, Reference, Explanation ([diataxis.fr](https://diataxis.fr)) |
| **GOMS** | Goals, Operators, Methods, Selection rules — a model for predicting how users accomplish tasks (Card, Moran & Newell 1983) |
| **Information Foraging** | Theory of how users follow navigation cues to find information, analogous to animals foraging for food (Pirolli & Card 1999) |
| **Norman's Gulfs** | The Gulf of Execution (gap between intent and interface) and Gulf of Evaluation (gap between system state and understanding) |
| **OWASP Top 10** | The ten most critical web application security risks ([owasp.org/Top10](https://owasp.org/Top10/)) |
| **SLI / SLO** | Service Level Indicator (a measured metric) and Service Level Objective (a target for that metric) — core reliability engineering concepts |
| **STRIDE** | Threat modeling framework: Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege |
| **Structurizr DSL** | Text-based notation for defining C4 architecture diagrams ([docs.structurizr.com/dsl](https://docs.structurizr.com/dsl)) |
| **Two-tier audit** | Some skills offer Standard (free tools) and Enterprise (paid platforms) tiers with different recommendations |

</details>

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup, skill file format, and PR process.

## Support

> *"En Del Af Noget Større"* (A Part of Something Bigger)

This project is, and always will be, free and open source. If you find value in this work, I encourage you to consider a donation to **Scottish Football for Rwanda** rather than any personal gift. I am volunteering as a goalkeeper coach in Rwanda in June 2026 — 100% of donations go directly to local kids, coaches, and community organizations.

[![Donate](https://img.shields.io/badge/Donate-JustGiving-E42C64?style=flat-square)](https://www.justgiving.com/page/gk-coach-karsten-for-rwanda)

## Academic Attribution

This project's audit methodologies are grounded in published academic research. See [`NOTICE.md`](NOTICE.md) for full citations of all referenced frameworks, theories, and algorithms.

## License

[MIT](LICENSE)
