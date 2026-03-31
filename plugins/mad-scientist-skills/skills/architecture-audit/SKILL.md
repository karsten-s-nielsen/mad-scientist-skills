---
name: architecture-audit
description: Comprehensive architecture audit with two modes and a single tier (beta). Planning mode evaluates architectural patterns, bounded context decomposition, dependency direction, and SOLID compliance for new systems. Audit mode scans existing codebases for architectural drift, coupling violations, domain model quality, dependency direction violations, and structural anti-patterns. Grounded in Hexagonal Architecture (Cockburn), Domain-Driven Design (Evans/Vernon), Clean Architecture (Martin), SOLID principles, Enterprise Integration Patterns (Hohpe & Woolf), CQRS and Event Sourcing (Young/Fowler), Twelve-Factor App (Wiggins), and API-First Design. Use when asked to "architecture audit", "review architecture", "check dependencies", "assess coupling", "evaluate structure", "SOLID audit", "domain model review", or "twelve-factor check".
---

# Architecture Audit (beta)

A comprehensive architecture audit skill with two modes and a single tier:

**Modes:**
- **Planning** (before code exists) — architectural pattern selection, bounded context decomposition, dependency direction design, SOLID compliance strategy
- **Audit** (on existing code) — scanning for architectural drift, coupling violations, domain model anti-patterns, dependency direction violations, and structural decay

**Single tier:** Architecture analysis is methodology-based — the value is in the analytical framework (dependency graphs, coupling metrics, pattern detection), not in paid tooling. The few tools referenced (import-linter, deptry, Madge) are free/open-source.

**Beta:** This skill is under active development. Phase coverage and detection patterns will expand based on field testing. Findings should be reviewed with appropriate skepticism — architectural assessment requires more judgment than grep-based vulnerability scanning.

**Core question:** "Does the structure of this codebase support its evolution?"

## Academic and practitioner foundations

This skill synthesizes eleven architectural traditions:

| Tradition | Key Author(s) | Core Contribution | Primary Phases |
|-----------|---------------|-------------------|----------------|
| **Hexagonal Architecture** (Ports & Adapters) | Cockburn (2005) | Dependency inversion at application boundaries; driving/driven port distinction | Phase 2, Phase 3 |
| **Domain-Driven Design** | Evans (2003), Vernon (2013) | Bounded contexts, ubiquitous language, strategic/tactical patterns, aggregate design | Phase 4, Phase 5 |
| **Clean Architecture** | Martin (2017) | The Dependency Rule — source code dependencies point only inward; four concentric rings | Phase 2, Phase 3 |
| **SOLID Principles** | Martin (2000s) | Five object-oriented design principles for maintainable, extensible code | Phase 6 |
| **Enterprise Integration Patterns** | Hohpe & Woolf (2003) | Messaging patterns for distributed systems; Splitter, Aggregator, Content-Based Router, Pipes and Filters | Phase 4 |
| **Coupling and Cohesion** | Constantine & Yourdon (1979), Martin (package principles) | Afferent/efferent coupling, Stable Dependencies Principle, cohesion classification | Phase 7 |
| **CQRS** | Young (2010), Fowler | Separate read and write models; command handlers mutate state, query handlers are side-effect-free | Phase 2, Phase 8 |
| **Event Sourcing** | Young (2010), Fowler | Store domain events as the source of truth; derive current state by replaying events | Phase 2, Phase 8 |
| **Twelve-Factor App** | Wiggins (2011, Heroku) | Twelve principles for building portable, resilient, cloud-native applications | Phase 8 |
| **API-First Design** | Swagger/OpenAPI community | Design the API contract before implementation; spec drives code generation and testing | Phase 2, Phase 8 |
| **Architectural Decision Records** | Nygard (2011) | Lightweight documentation of significant architectural decisions with context, consequences, and status | Phase 9 |

## When to use this skill

- When the user says "architecture audit", "review architecture", "check dependencies", "assess coupling", "evaluate structure", "SOLID audit", or "domain model review"
- Before designing a new system (planning mode) — to select appropriate architectural patterns and decomposition strategy
- On an existing codebase (audit mode) — to find structural decay, coupling violations, and architectural drift
- Before a major refactoring — to understand the current architecture and identify safe change boundaries
- When onboarding to a new codebase — to build a structural mental model
- After significant feature additions — to detect whether new code respects established architectural boundaries

## Mode detection

Determine which mode to operate in based on the project state:

| Signal | Mode | Rationale |
|--------|------|-----------|
| User says "design architecture", "plan structure", "select patterns" | **Planning** | Architecture-level design before code |
| User says "audit", "review architecture", "check coupling" | **Audit** | Code and structure scanning |
| No source code exists yet (only docs, diagrams, RFCs) | **Planning** | Nothing to scan — design the architecture |
| Source code and/or infrastructure files exist | **Audit** | Concrete artifacts to analyze |
| Both code and a request to "redesign architecture" | **Both** | Run planning phases on target architecture, audit phases on current code |

When in doubt, ask the user. If both modes apply, run all phases.

## Severity classification

Every finding must be assigned a severity:

| Severity | Criteria | Action | SLA |
|----------|----------|--------|-----|
| **Critical** | Architectural violation that causes concrete harm: circular dependencies preventing independent deployment, domain logic in infrastructure making testing impossible, coupling that forces shotgun surgery across modules for any change | Fix immediately | Block release |
| **High** | Structural decay that degrades maintainability: dependency direction violations, god modules with multiple responsibilities, cross-context coupling through internal tables, anemic domain model hiding business rules in service layers | Fix before next release | 1 sprint |
| **Medium** | Architectural impurity that increases cognitive load but doesn't block work: inconsistent pattern application, missing abstractions at layer boundaries, unused interfaces, partial SOLID compliance | Schedule fix | 2 sprints |
| **Low** | Best practice deviation, cosmetic structural issues, documentation gaps | Track in backlog | Best effort |

## Audit process

Execute all applicable phases in order. Skip phases marked for a mode you are not running. Do NOT skip applicable phases. Do NOT claim completion without evidence.

**Critical judgment rule:** Architecture assessment requires more contextual judgment than security or optimization scanning. A pattern that is an anti-pattern in one context (anemic domain model in a complex business system) may be entirely appropriate in another (DataFrame-centric analytics pipeline where the domain IS the data transformation). Before flagging a finding, ask: "Does this structural choice cause concrete harm in THIS codebase, or am I applying a pattern prescriptively?" If the latter, downgrade to Low or omit entirely.

---

### Phase 0: Anti-Pattern Scan (Audit mode)

Fast grep-based scan for structural anti-patterns. Runs first to catch obvious architectural violations before deeper analysis.

| Pattern | Language | Risk |
|---------|----------|------|
| Circular imports between packages | Python (`from pkg_a import ... # in pkg_b` AND `from pkg_b import ... # in pkg_a`) | Circular dependency — prevents independent evolution |
| `import` from infrastructure in domain | Python (domain/model files importing `sqlalchemy`, `boto3`, `psycopg2`, `requests`, `flask`, `fastapi`, `django.db`, `pyspark`) | Dependency direction violation — domain depends on infrastructure |
| God module by line count | Any file >800 lines (excluding generated code, test files, and configuration) | Single Responsibility violation — module has multiple reasons to change |
| God class by method count | Class with >15 public methods | Interface Segregation violation — class serves too many clients |
| Feature envy imports | Module that imports >5 names from a single sibling module | Possible misplaced responsibility — logic may belong in the imported module |
| `TYPE_CHECKING` guard overuse | Python (`if TYPE_CHECKING:` with >10 imports) — may indicate the module depends on too many other modules | High afferent coupling — possible structural boundary issue |
| Mixed abstraction levels | Module containing both high-level orchestration (`main()`, `run_pipeline()`) and low-level utility functions (`parse_date()`, `validate_schema()`) | Abstraction level mixing — split into orchestration and utility modules |
| Barrel file re-exports | `__init__.py` with >20 re-exports (`from .module import ...`) | Artificial coupling — importers depend on everything via the barrel |
| Raw SQL in domain/application layer | `SELECT`, `INSERT`, `UPDATE`, `DELETE` strings outside of dedicated repository/data-access modules | Data access concern leaked into domain or application layer |
| Hardcoded infrastructure in business logic | URLs, connection strings, table names, bucket names, queue names as string literals in non-configuration modules | Infrastructure concern leaked into business logic |

For each finding: record file path, line number, pattern matched, and whether it is a true positive or an acceptable pattern for this codebase. Flag true positives with appropriate severity.

**Output:** Anti-pattern findings table with file paths, risk classification, and true/false positive status.

---

### Phase 1: Discovery (Both modes)

Explore the project to understand its architectural surface:

- Read `CLAUDE.md`, `README.md`, `AGENTS.md`, and any architecture docs (ADRs, C4 diagrams, design documents)
- Identify the tech stack, frameworks, language versions, and build system
- Map the **architectural surface**:
  - Package/module structure: top-level directories, their declared purposes, entry points
  - Build artifacts: what gets deployed? (wheel, Docker image, serverless function, static site)
  - Layer identification: are there named layers? (domain, application, infrastructure, presentation, ingestion, transformation, serving)
  - External dependencies: frameworks, databases, cloud services, third-party APIs
  - Internal dependency direction: which packages import from which?
  - Configuration management: how are settings, feature flags, and environment-specific values handled?
  - Test structure: how are tests organized relative to source? Unit vs integration separation?
- Identify the **intended architecture** (from docs, CLAUDE.md, naming conventions, or team conventions):
  - Is there a stated architectural pattern? (hexagonal, layered, clean, modular monolith, microservices, pipeline/medallion)
  - Are there stated layer rules? ("workflows has zero Spark imports", "domain never imports infrastructure")
  - Are there boundary enforcement mechanisms? (import linting, module structure, CI checks)
- Note the **project archetype**: This determines which architectural patterns are appropriate:
  - **Business application** (web app, API service, SaaS): Hexagonal/Clean + DDD tactical patterns are high-value
  - **Data platform** (ETL pipelines, analytics, ML): Medallion architecture + EIP patterns are native; hexagonal applies selectively to serving layers
  - **CLI tool / library**: Minimal architecture needed; focus on public API surface and backward compatibility
  - **Infrastructure / platform**: Separation of policy and mechanism; plugin architectures
  - **Hybrid**: Identify which archetype applies to which subsystem

**Output:** Architectural surface summary listing packages, layers, intended patterns, dependency directions, and project archetype classification.

---

### Phase 2: Architectural Pattern Detection (Audit mode)

Identify which architectural pattern(s) the codebase actually implements (regardless of what documentation claims). Pattern detection is evidence-based — look at import graphs and module structure, not comments or README aspirations.

#### Detection signals

| Pattern | Positive Signals | Negative Signals |
|---------|-----------------|------------------|
| **Hexagonal / Ports & Adapters** | `Protocol` or `ABC` definitions used as interfaces; separate `adapters/` or `infrastructure/` directories; domain modules with zero framework imports; constructor injection of dependencies; composition root wiring | Domain modules importing `sqlalchemy`, `boto3`, `requests` directly; no interface definitions; concrete classes instantiated inline |
| **Clean Architecture** | Concentric ring structure (entities → use cases → interface adapters → frameworks); strict inward dependency direction; use case classes/functions as the primary API | Outer ring classes imported by inner rings; framework types used in entity definitions |
| **Layered / N-Tier** | Named layers (presentation, business, data access) with each layer calling only the next; ORM models shared between layers | Skip-layer calls (presentation calling data access directly); mixed concerns within layers |
| **Medallion / Data Pipeline** | Bronze/silver/gold (or raw/staging/mart) directory structure; transformation logic in SQL or DataFrame operations; orchestration separate from transformation | Pipeline code mixed with serving/UI code; no clear data quality progression |
| **Modular Monolith** | Feature-organized modules with explicit public APIs; inter-module communication through defined interfaces; each module deployable independently in principle | God module that everything imports; circular dependencies between modules |
| **CQRS** | Separate command and query models or handlers; distinct write-path (commands → aggregates → event store or database) and read-path (queries → optimized read models or projections); command handlers that never return domain data; query handlers that never mutate state | Single model used for both reads and writes; query methods on entities that also trigger side effects |
| **Event Sourcing** | Event store (append-only log of domain events); current state derived by replaying events; event classes named in past tense (`OrderPlaced`, `PaymentReceived`); projection/read-model builders that subscribe to events; snapshot mechanism for performance | Mutable state persisted directly to database; no event log; updates overwrite previous state |
| **API-First** | OpenAPI/AsyncAPI/GraphQL schema files (`openapi.yaml`, `schema.graphql`) that exist BEFORE or alongside implementation; code generation from specs (`openapi-generator`, `datamodel-code-generator`, `graphql-codegen`); contract tests that validate implementation against spec | API routes defined only in code with no spec; spec generated FROM code as an afterthought (code-first, not API-first) |
| **No discernible pattern** | Flat file structure; imports in all directions; business logic mixed with infrastructure; no naming conventions | (This is itself a finding at Medium severity) |

#### Pattern consistency check

Once the dominant pattern is identified, check whether it is applied consistently:

| Check | What to look for | Severity |
|-------|-----------------|----------|
| Pattern coverage | What percentage of modules follow the detected pattern? A pattern applied to 3 of 12 modules is worse than no pattern — it creates false expectations | High (if <50% coverage) |
| Pattern mixing | Are multiple architectural patterns mixed in the same layer? (e.g., some modules use repository pattern, others call the database directly in the same layer) | Medium |
| Stated vs actual | Does the documented/intended architecture match the detected pattern? Drift between stated and actual architecture is a finding | High |
| Boundary enforcement | Is the pattern enforced by tooling (import-linter, custom lint rules, CI checks) or only by convention? Convention-only enforcement decays over time | Medium |
| Framework coupling depth | For the primary framework (Django, Flask, Taipy, React, etc.): can the business logic (data fetching, computation, validation) be extracted and tested without the framework running? If the framework's state/binding model (e.g., Taipy module-level variables, Django ORM, React hooks) is interleaved with business logic in the same functions, the application is framework-locked — swapping or upgrading the framework requires rewriting business logic, not just adapters. Assess by checking whether test files for framework-coupled modules require the framework or can run standalone | Medium |

**Output:** Detected architectural pattern(s) with evidence, consistency assessment, framework coupling depth, and stated-vs-actual drift findings.

---

### Phase 3: Dependency Direction Analysis (Both modes)

Verify that source code dependencies flow in the intended direction. This is the mechanical heart of Clean and Hexagonal architecture — violations here undermine all other architectural properties.

**Planning mode:** Design the dependency direction policy:
- Which packages are "inner" (domain, application logic) and which are "outer" (infrastructure, frameworks)?
- What is the dependency rule? (All dependencies point inward? Each layer only imports from the layer below?)
- How will the rule be enforced? (import-linter, custom CI check, code review convention)

**Audit mode:**

#### Dependency graph construction

Build the inter-package import graph. For Python projects:

1. List all first-party packages (top-level directories under `src/` or equivalent)
2. For each package, list all imports from other first-party packages
3. Draw the directed graph: edge from A → B means "A imports from B"
4. Identify the intended direction (from Phase 1 discovery)
5. Flag edges that violate the intended direction

#### Violation detection

| Check | What to look for | Severity |
|-------|-----------------|----------|
| Upward dependency | Inner layer importing from outer layer (domain importing from infrastructure, application importing from presentation) | Critical |
| Circular dependency | Package A imports B and B imports A (directly or transitively) | Critical |
| Skip-layer dependency | Presentation layer importing directly from data access, bypassing application/service layer | High |
| Framework leak into domain | Domain entities or value objects importing framework types (`sqlalchemy.Column`, `django.db.models.Model`, `pydantic.BaseModel` used as domain entity base in a hexagonal app) | High |
| Concrete dependency where abstraction exists | Code depending on a concrete adapter class when a Protocol/ABC port exists for it | Medium |
| Transitive dependency explosion | Package that transitively depends on >70% of all other packages | Medium |

**Note on Pydantic in domain layers:** `pydantic.BaseModel` as a domain value object base is a gray area. In a strict hexagonal interpretation, the domain should not depend on Pydantic (a third-party library). In practice, Pydantic provides validation and immutability that serve domain concerns. Flag only if the project's stated architecture explicitly forbids third-party imports in the domain layer; otherwise, note as informational.

#### Tools for automated analysis

| Tool | Language | Purpose | Command |
|------|----------|---------|---------|
| `import-linter` | Python | Define and enforce import rules between packages | `lint-imports` (configure in `.importlinter`) |
| `deptry` | Python | Find unused, missing, and transient dependencies | `deptry .` |
| `Madge` | JS/TS | Dependency graph visualization and circular dependency detection | `madge --circular src/` |
| `cargo-depgraph` | Rust | Dependency graph visualization | `cargo depgraph` |
| `go mod graph` | Go | Module dependency graph | `go mod graph` |

**Output:** Dependency direction findings with import graph edges, violation classification, and recommended restructuring.

---

### Phase 4: Bounded Context Assessment (Both modes)

Evaluate whether the codebase has clear bounded context boundaries, whether those boundaries are respected, and whether the inter-context integration patterns are appropriate. This phase applies DDD strategic patterns — it does NOT require that the codebase uses DDD tactical patterns (entities, aggregates, repositories).

**Planning mode:** Design the bounded context decomposition:
- What are the natural subdomains? (Core, Supporting, Generic — per Evans/Vernon)
- Which bounded contexts map to which subdomains?
- What are the context mapping relationships? (Shared Kernel, Customer-Supplier, Conformist, Anti-Corruption Layer, Open Host Service)
- How will context boundaries be enforced in code? (separate packages, separate repos, separate deployments)

**Audit mode:**

#### Context boundary detection

| Check | What to look for | Severity |
|-------|-----------------|----------|
| Implicit bounded contexts | Identify logical contexts by examining package structure, naming patterns, and import clusters. Each cluster of modules that share vocabulary and imports but are independent from other clusters is likely a bounded context | Informational |
| Context boundary violations | Code in one context importing internals (non-public modules, private functions, internal data structures) from another context | High |
| Shared mutable state | Global variables, singleton caches, or shared database tables modified by multiple contexts without a clear ownership model | High |
| Anti-corruption layer at external boundaries | When consuming external APIs or third-party data, is there a translation layer that normalizes the external model to internal domain vocabulary? Or does the external schema propagate unchanged through the codebase? | Medium |
| Ubiquitous language consistency | Does each context use consistent terminology internally? Do different contexts use different terms for the same concept (acceptable) or the same term for different concepts (a bug)? | Medium |
| Shared Kernel scope | If contexts share code (common libraries, shared models), is the shared kernel explicitly identified and minimized? Overgrown shared kernels couple contexts that should be independent | Medium |

#### Subdomain classification (Planning mode or retrospective)

For each identified bounded context or major module:

| Context / Module | Subdomain Type | Justification | Investment Implication |
|-----------------|----------------|---------------|----------------------|
| [name] | Core / Supporting / Generic | [why this classification] | [build from scratch / build pragmatically / buy or use off-the-shelf] |

**Core domains** deserve the best engineering, the richest domain models, and the deepest domain expert collaboration. **Supporting subdomains** should be built pragmatically — correct and maintainable, but not over-engineered. **Generic subdomains** should use existing solutions (libraries, SaaS, open-source tools) — building custom solutions for generic problems is a strategic misallocation.

#### Context map (Planning mode or retrospective)

For each pair of bounded contexts that communicate:

| Upstream Context | Downstream Context | Relationship | Evidence |
|-----------------|-------------------|--------------|----------|
| [name] | [name] | Shared Kernel / Customer-Supplier / Conformist / ACL / OHS / Published Language / Separate Ways | [how the integration works in code] |

Flag relationships where:
- Downstream context has no ACL and directly uses upstream's internal types (Conformist where ACL would be better)
- Shared Kernel is large (>20 classes or >500 lines) — should be minimized
- Context boundary is unclear — modules could belong to either context

#### Cross-deployment contract validation

When Context A publishes a schema (dbt contract, OpenAPI spec, protobuf, Avro) consumed by Context B in a separately-deployed process, check whether **both sides** validate against the contract:

| Check | What to look for | Severity |
|-------|-----------------|----------|
| Write-side contract enforcement | Does the publishing context enforce its schema at build/deploy time? (e.g., dbt `contract: enforced`, OpenAPI schema validation middleware, protobuf compile step) | High (if no write-side enforcement) |
| Read-side contract validation | Does the consuming context validate its queries/access against the published schema at build or test time? Or does it use raw strings (SQL, column names, field access) with no compile-time or test-time check? A column rename on the write side that passes write-side CI but silently breaks the consumer is a contract gap | High (if consumers use unvalidated raw access) |
| Contract drift detection | Is there a mechanism (shared schema definition, contract test, CI cross-check) that detects when the consumer's expectations diverge from the publisher's schema? | Medium |

This check is especially important for data platforms where dbt models publish schemas consumed by application-layer SQL queries — the dbt contract validates the write side, but the read-side SQL is often unvalidated raw strings.

**Output:** Bounded context map with boundaries, subdomain classifications, integration patterns, and boundary violation findings.

---

### Phase 5: Domain Model Quality (Audit mode)

Evaluate the quality of the domain model. This phase adapts its expectations to the project archetype detected in Phase 1.

**For business applications** (where domain logic is the core value):

| Check | What to look for | Severity |
|-------|-----------------|----------|
| Anemic domain model | Domain entities are data-only classes (all fields, no behavior) with all business logic in separate service classes. The entities are glorified DTOs. Note: this is only a finding if there ARE business rules that should live on the entities — some domains genuinely have thin models | High (if business rules exist outside entities) |
| Primitive obsession | Domain concepts represented as raw strings, ints, or floats instead of typed value objects. E.g., `price: float` instead of `Money(amount, currency)`, `email: str` instead of `EmailAddress(value)`. Each primitive that carries domain rules (validation, formatting, comparison) is a candidate for a value object | Medium |
| Missing invariant enforcement | Business rules that should be enforced at construction time are instead checked externally (validation in a separate service rather than in the constructor/factory). Invariant violations should be impossible to construct, not caught at call sites | High |
| Oversized aggregates | Aggregate roots that contain or reference too many entities, causing transaction contention and performance issues. Vernon's rule: aggregates should be as small as possible while still protecting their invariants | Medium |
| Missing domain events | State changes that should notify other parts of the system are instead handled by procedural orchestration (service A directly calls service B after modifying an entity, rather than publishing an event) | Medium |
| Repository interface in wrong layer | Repository interfaces defined in the infrastructure layer instead of the domain/application layer. The interface should be in the domain (defining what the domain needs); the implementation should be in infrastructure (providing it) | High |

**For data platforms** (where transformations and pipelines are the core value):

| Check | What to look for | Severity |
|-------|-----------------|----------|
| Computation mixed with I/O | Pure analytical functions (statistics, ML inference, geometry) importing I/O libraries (database clients, HTTP, file system). Analytical functions should accept data (DataFrames, arrays) and return data — the caller handles I/O | High |
| Missing computation isolation | No separation between pure computation modules and pipeline orchestration modules. Computation should be independently testable without Spark, database, or network | High |
| Schema as implicit contract | Data contracts between pipeline stages exist only as runtime DataFrame column access (string keys). No explicit schema definition (Pydantic model, dbt contract, protobuf/avro schema) at stage boundaries | Medium |
| Configuration as code | Pipeline configuration (table names, partition keys, thresholds, feature lists) hardcoded in business logic instead of externalized as configuration objects | Medium |
| Workflow metadata model | If the platform has workflow/pipeline metadata (execution config, cost estimates, monitoring thresholds), evaluate whether it uses structured models (Pydantic, dataclass) or untyped dicts | Medium |
| Data access centralization | For applications that consume published data (mart tables, API responses), are read queries centralized in dedicated data-access modules (repository classes, query builders, typed query functions), or scattered as raw SQL/column-name strings across application logic? A connection manager that provides `execute_query(sql)` is not centralization — it centralizes the *connection*, not the *queries*. True centralization means a column rename requires changing one file, not grep-replacing across 14 state modules | High (if >10 queries scattered across >3 modules) |
| Framework coupling in presentation | For applications with a UI framework (Taipy, Streamlit, Django, React), can the data-fetching and computation logic be tested without the framework running? If state modules mix SQL queries, analytical computation, and framework state mutation in single functions, the business logic is untestable without the framework — a separation-of-concerns violation even when the framework is the intended deployment target | Medium |

**For libraries and CLIs:**

| Check | What to look for | Severity |
|-------|-----------------|----------|
| Public API surface clarity | Is the public API explicitly defined (`__all__`, re-exports in `__init__.py`, documented entry points)? Or is everything implicitly public? | High |
| Backward compatibility surface | Are internal implementation details accessible to external consumers? Can you change internals without breaking the public API? | High |
| Plugin/extension architecture | If the library supports extensions, is there a well-defined extension point (Protocol, ABC, hook system)? Or do extensions require monkey-patching? | Medium |

**Output:** Domain model quality findings with anti-pattern classification, affected modules, and restructuring recommendations.

---

### Phase 6: SOLID Compliance (Audit mode)

Systematically evaluate compliance with each SOLID principle. These are design-level checks — they require reading code structure, not just grepping patterns.

| Principle | Check | What to look for | Severity |
|-----------|-------|-----------------|----------|
| **S — Single Responsibility** | Module/class reason-to-change count | Does the module/class have more than one reason to change? A module handling both HTTP request parsing AND database access has two responsibilities. Count distinct concerns per module | High (if >2 responsibilities) |
| **S — Single Responsibility** | Module name accuracy | Does the module name accurately describe ALL of its contents? If you need to say "and" to describe what a module does, it has multiple responsibilities | Medium |
| **O — Open/Closed** | Extension vs modification | When adding new behavior (new data source, new report type, new validation rule), does the developer extend existing code (new class, new module, new configuration entry) or modify existing code (adding `elif` branches, editing switch statements)? Frequent modification of the same module for different features indicates OCP violation | Medium |
| **O — Open/Closed** | Strategy/plugin patterns | Are variation points designed for extension? (Strategy pattern, plugin registration, decorator chains, configuration-driven behavior) | Low |
| **L — Liskov Substitution** | Subtype behavioral contracts | Do subclasses honor the contracts of their parent classes? Common violations: subclass methods raising exceptions the parent doesn't, subclass narrowing input types, subclass weakening postconditions | High (if violations cause runtime errors) |
| **L — Liskov Substitution** | Protocol/ABC compliance | Do all implementations of a Protocol or ABC satisfy the interface contract? Can every adapter be swapped without changing calling code? | Medium |
| **I — Interface Segregation** | Fat interfaces | Are there interfaces (Protocol, ABC) with methods that some implementors don't need? An implementor that raises `NotImplementedError` for some methods signals a fat interface | Medium |
| **I — Interface Segregation** | Client-specific interfaces | Do clients depend on the narrowest interface that serves their needs, or on a broad interface where they use only a fraction of the methods? | Low |
| **D — Dependency Inversion** | Concrete dependencies | Do high-level modules depend on low-level modules directly, or through abstractions (Protocol, ABC, interface)? In a well-inverted design, the domain defines what it needs (port), and infrastructure provides it (adapter) | High |
| **D — Dependency Inversion** | Composition root existence | Is there a single location (composition root, bootstrap, main) where concrete implementations are assembled and injected? Or are concrete classes instantiated throughout the codebase? | Medium |

#### SOLID in data pipelines — calibrated expectations

SOLID principles apply differently to data pipelines than to business applications:

- **SRP**: A pipeline module that ingests, transforms, and writes is often acceptable as a single responsibility ("ingest source X"). The alternative (separate modules for fetch, transform, write) can over-fragment simple ETL.
- **OCP**: dbt's model system is inherently open/closed — add new models without modifying existing ones. Spark `applyInPandas` functions are naturally closed — they process one group at a time, unaware of what other groups exist.
- **LSP**: Less applicable in pipeline code where inheritance is rare. Check Protocol compliance instead.
- **ISP**: Relevant when pipeline frameworks define hook/callback interfaces — the interface should not force implementors to provide hooks they don't use.
- **DIP**: Most relevant at the boundary between orchestration and computation. Orchestration should depend on computation abstractions, not concrete implementations.

**Output:** SOLID compliance findings per principle with affected modules, violation classification, and restructuring recommendations.

---

### Phase 7: Coupling and Cohesion Analysis (Audit mode)

Measure the structural quality of module boundaries.

#### Coupling indicators

| Check | What to look for | Severity |
|-------|-----------------|----------|
| Afferent coupling (Ca) — incoming | Count how many other modules depend on this module. High Ca means the module is heavily depended upon — changes are expensive. Ca >10 for non-utility modules is a smell | Medium (for awareness) |
| Efferent coupling (Ce) — outgoing | Count how many other modules this module depends on. High Ce means the module knows too much — it has too many reasons to change due to external changes. Ce >10 for non-orchestration modules is a smell | Medium |
| Instability (I = Ce / (Ca + Ce)) | Modules with high instability (I near 1.0) should depend on modules with low instability (I near 0.0). A stable module (many dependents, few dependencies) depending on an unstable module (few dependents, many dependencies) violates the Stable Dependencies Principle | High |
| Circular dependency chains | A → B → C → A. Circular chains prevent independent deployment, testing, and evolution. Every cycle must be broken, typically by introducing an interface (DIP) or extracting a shared module | Critical |
| Connascence of meaning | Multiple modules sharing implicit knowledge (magic strings, status codes, column names) without a shared constant or type definition. Changes to the implicit knowledge require coordinated changes across all modules | Medium |
| Stamp coupling | Modules passing large data structures (entire DataFrames, config objects) when only a few fields are needed. The receiver is coupled to the full structure's schema even though it uses a fraction | Low |

#### Cohesion indicators

| Check | What to look for | Severity |
|-------|-----------------|----------|
| Coincidental cohesion | Module groups unrelated functions that happen to be created at the same time. Classic: `utils.py` with 30 unrelated helpers | Medium |
| Logical cohesion | Module groups functions by technical category ("all validators", "all formatters") rather than by domain concept. Better: group by what they validate/format | Low |
| Functional cohesion (ideal) | Module groups everything needed for one well-defined purpose. All functions in the module contribute to a single task, and all functions needed for that task are in this module | Informational (positive finding) |
| God module | Module with >500 lines, >15 public functions, touching >3 distinct concerns. The canonical refactoring target | High |
| Orphaned code | Functions or classes defined in a module but never imported or called by any other code in the project. May indicate dead code or misplaced responsibility | Low |

#### Cross-deployment duplication

When a project has multiple independently-deployed contexts (e.g., a pipeline wheel and a containerized app, or a backend API and a frontend BFF), check for near-duplicate modules that exist in both contexts. This is architecturally worse than intra-context duplication because:
- The contexts have separate release cycles — a fix to the original may not propagate to the copy for weeks
- There is no shared build step — the copy can diverge silently with no CI check
- The duplication often includes infrastructure-coupled code (connection managers, auth flows, retry logic) where a bug in one copy becomes a security gap in the other

| Check | What to look for | Severity |
|-------|-----------------|----------|
| Vendored module copies | Modules that exist in two contexts with identical or near-identical content (>80% line similarity). Common pattern: an app that vendors a subset of a library's modules rather than importing the library. Check for identical filenames across context boundaries | High (if >200 lines duplicated) |
| Duplicated infrastructure code | Connection managers, auth token handlers, retry logic, or configuration loaders that are copy-pasted across contexts rather than shared via a common package or extracted into a library | High |
| Duplicated business logic | Computation functions, validation rules, or domain constants that appear in multiple contexts. The single-source-of-truth principle applies across deployment boundaries, not just within a single package | Medium |

For each finding: identify both copies, measure the line count, and assess the sync risk (how likely is one copy to drift from the other without detection).

#### Automated coupling analysis

For Python projects, build a dependency matrix:

1. For each first-party package, count imports to/from every other package
2. Present as a matrix: rows = importing package, columns = imported package, cells = import count
3. Flag cells that violate expected dependency direction (from Phase 3)
4. Identify clusters (groups of packages that import each other heavily) — these are natural bounded context candidates

**Output:** Coupling/cohesion findings with metrics, cross-deployment duplication inventory, and recommended boundary restructuring.

---

### Phase 8: CQRS, Event Sourcing, Twelve-Factor & API-First (Both modes) — CONDITIONAL

**Skip the CQRS and Event Sourcing sub-sections** if Phase 2 detected no signals for those patterns. **Always run the Twelve-Factor checklist** for any deployed application — the twelve factors represent operational best practices independent of architectural pattern. **Run the API-First sub-section** if the project exposes APIs (REST, GraphQL, gRPC) regardless of whether an OpenAPI spec was detected.

#### CQRS Correctness (if detected)

| Check | What to look for | Severity |
|-------|-----------------|----------|
| Command/query separation | Command handlers (write path) never return domain data beyond an ID or acknowledgement. Query handlers (read path) never mutate state. If a single handler both reads and writes, the CQRS boundary is violated | High |
| Read model staleness | How are read models (projections) updated after commands? Synchronously (simple, consistent, but coupled) or asynchronously via events (decoupled, but eventually consistent)? If async: is the eventual consistency documented and communicated to users? | Medium |
| Projection rebuild capability | Can read models be rebuilt from scratch by replaying events or re-reading the write store? If a projection is corrupted or a new projection is added, is there a rebuild mechanism? | High |
| Command validation | Are commands validated before reaching the domain model? (input validation in the command handler, not just in the aggregate). Invalid commands should be rejected before they trigger domain logic | Medium |

#### Event Sourcing Correctness (if detected)

| Check | What to look for | Severity |
|-------|-----------------|----------|
| Event immutability | Events in the event store are never modified or deleted. Updates are represented as new events, not mutations of existing ones | Critical |
| Event versioning | When event schemas change, is there a migration or upcasting strategy? Old events must remain deserializable after schema evolution. Common approaches: upcasters that transform old event shapes to current, or multi-version deserialization | High |
| Snapshot strategy | For aggregates with long event streams (>1000 events), is there a snapshot mechanism to avoid replaying the full stream on every load? | Medium (if long streams exist) |
| Idempotent event handlers | Event consumers/projectors must handle duplicate delivery gracefully. Check for idempotency keys or deduplication logic | High |
| Event store as source of truth | The event store (not the read models, not a cache) must be the authoritative source of truth. Verify that recovery procedures rebuild state from events, not from projections | Critical |
| Temporal queries | Can the system answer "what was the state at time T?" by replaying events up to T? This is a key benefit of event sourcing — verify it is preserved, not accidentally undermined by mutable snapshots | Medium |

#### Twelve-Factor App Assessment

The Twelve-Factor methodology (Wiggins, 2011) defines twelve principles for building portable, resilient, cloud-native applications. Evaluate each factor — even projects not explicitly following twelve-factor benefit from the checklist, as the factors represent hard-won operational wisdom.

| Factor | Check | What to look for | Severity if violated |
|--------|-------|-----------------|---------------------|
| **I. Codebase** | One codebase, many deploys | Is there a single repo tracked in version control with multiple deployment targets (dev, staging, prod)? Or are there forked codebases per environment? | Medium |
| **II. Dependencies** | Explicitly declare and isolate | Are all dependencies declared in a manifest (`requirements.txt`, `pyproject.toml`, `package.json`, `go.mod`)? Is there a lockfile? Does the app assume system-level packages exist without declaring them? | High |
| **III. Config** | Store config in the environment | Is configuration (credentials, resource handles, per-deploy values) stored in environment variables or platform-native config, not in code? Grep for hardcoded URLs, connection strings, or API endpoints outside of config modules | High |
| **IV. Backing services** | Treat as attached resources | Can the app swap a local database for a cloud-managed one by changing a config value alone? Or is the backing service hardcoded (e.g., `localhost:5432` without env override)? | Medium |
| **V. Build, release, run** | Strict separation | Is there a clear distinction between build (compile/bundle), release (build + config), and run (execute in environment)? Or does the run stage also build or configure? | Medium |
| **VI. Processes** | Stateless processes | Does the app store session state, caches, or temporary files in local process memory/filesystem expecting them to persist across requests or restarts? Sticky sessions, local file uploads without external storage | High |
| **VII. Port binding** | Export services via port binding | Does the app self-host its HTTP/gRPC service (e.g., `uvicorn`, `gunicorn`, embedded Jetty), or does it rely on runtime injection into a web server? | Low |
| **VIII. Concurrency** | Scale out via processes | Can the app scale horizontally by running multiple identical processes? Or does it rely on in-process threading for all concurrency with shared mutable state? | Medium |
| **IX. Disposability** | Fast startup, graceful shutdown | Does the app start in <30 seconds? Does it handle SIGTERM gracefully (drain connections, finish in-flight work)? | High |
| **X. Dev/prod parity** | Keep environments similar | Are there significant differences between development and production environments (different databases, different OS, mocked services in dev)? | Medium |
| **XI. Logs** | Treat logs as event streams | Does the app write structured logs to stdout, or does it manage its own log files, rotation, and shipping? | Medium |
| **XII. Admin processes** | Run as one-off processes | Are database migrations, data fixes, and maintenance tasks runnable as one-off commands in the same environment as the app? Or do they require special access, manual SQL, or separate tooling? | Low |

**Twelve-Factor in data platforms — calibrated expectations:**
- Factor VI (stateless processes) applies differently: pipeline tasks are inherently stateful during execution (they hold DataFrames in memory). The check is whether state persists *between* task executions — it should not (use Delta tables, not local files).
- Factor IX (disposability) is critical for serverless pipelines — tasks must be safe to kill and restart at any point.
- Factor X (dev/prod parity) is often violated in data platforms (local DuckDB vs production Spark). Flag only if the divergence causes bugs that escape to production.

#### Deployment constraint inventory

For projects deploying to multiple targets with different runtime constraints (serverless functions, GPU containers, edge devices, HF Spaces, managed clusters), check whether constraints are documented and whether the code structure accounts for them:

| Check | What to look for | Severity |
|-------|-----------------|----------|
| Constraint documentation | Are per-target runtime constraints (memory limits, CPU, network access, filesystem access, available libraries, execution timeouts) documented in CLAUDE.md, ADRs, or deployment docs? For multi-target projects, a table mapping target → constraints is the minimum | Medium (if >2 targets and no documentation) |
| Code-constraint alignment | Does the code structure account for documented constraints? E.g., if UDF executors have a 1 GB memory limit, are group sizes bounded? If serverless has no internet, do UDF bodies avoid HTTP calls? If a container has 16 GB RAM, are datasets verified to fit before loading? | High (if code violates documented constraints) |
| Constraint propagation | When a function is shared across deployment targets with different constraints, does the code degrade gracefully or fail fast when a constraint is hit? Or does it silently OOM / timeout / hang? | Medium |

#### API-First Assessment (if detected or applicable)

| Check | What to look for | Severity |
|-------|-----------------|----------|
| Spec existence | Does an OpenAPI, AsyncAPI, or GraphQL schema file exist? Is it the source of truth (API-first) or generated from code (code-first)? | High (if API exists but no spec) |
| Spec-code synchronization | If a spec exists, does the implementation match it? Are there endpoints in code not in the spec, or spec endpoints not implemented? | High |
| Contract testing | Are there tests that validate the implementation against the spec? (e.g., `schemathesis`, `dredd`, `openapi-core` validation middleware) | Medium |
| Versioning strategy | For public APIs: is there a versioning strategy (URL path, header, query param)? Are deprecated versions documented with sunset timelines? | Medium |
| Consumer-driven contracts | For internal APIs: do consumers define their expectations via contract tests (Pact, Spring Cloud Contract)? Or does the provider define the contract unilaterally? | Low |

**Output:** CQRS/ES correctness findings, twelve-factor compliance table, API-first assessment. Each twelve-factor violation includes the factor number, current state, and recommended remediation.

---

### Phase 9: Architectural Decision Records (Both modes)

Evaluate whether significant architectural decisions are documented and whether the code matches documented decisions.

**Planning mode:** Establish ADR practices:
- Where will ADRs be stored? (`docs/decisions/`, `docs/adr/`)
- What template will be used? (Nygard format: Title, Status, Context, Decision, Consequences)
- What decisions warrant an ADR? (Architectural patterns, technology choices, integration strategies, deprecated approaches)

**Audit mode:**

| Check | What to look for | Severity |
|-------|-----------------|----------|
| ADR existence | Are there any architectural decision records? (`docs/decisions/`, `docs/adr/`, ADR sections in README or CLAUDE.md) | Medium (if significant decisions exist undocumented) |
| Decision-code alignment | For each documented decision: does the code match? If CLAUDE.md says "workflows has zero Spark imports" — verify this is true | High (if code contradicts documented decisions) |
| Undocumented significant decisions | Are there architectural choices (technology selection, pattern adoption, boundary placement) that are not documented anywhere? | Medium |
| Superseded decisions | Are there ADRs or documented decisions that have been superseded by later code changes without updating the documentation? | Medium |
| Decision rationale | Do documented decisions include the "why" (context, constraints, trade-offs), not just the "what"? A decision without rationale cannot be evaluated when circumstances change | Low |
| CLAUDE.md as ADR source | Many projects encode architectural decisions in CLAUDE.md or similar AI-assistant context files. These should be treated as authoritative ADRs and validated against the code | High (if CLAUDE.md contradicts code) |

**Output:** ADR coverage assessment with documented decisions, undocumented decisions, and decision-code alignment findings.

---

### Phase 10: Findings Report (Both modes)

Generate the final report. The format depends on the mode.

#### Planning mode report

Present the architectural design and recommendations:

```markdown
## Architecture Plan — [System Name]

### Project Archetype
- Classification: [Business Application / Data Platform / CLI/Library / Infrastructure / Hybrid]
- Justification: [why this classification]

### Architectural Surface
- Packages: [list with purposes]
- External dependencies: [frameworks, databases, cloud services]
- Intended pattern: [hexagonal / clean / layered / medallion / modular monolith]

### Bounded Context Decomposition
| Context | Subdomain Type | Responsibility | Integration Pattern |
|---------|---------------|----------------|-------------------|
| [name] | Core / Supporting / Generic | [what it owns] | [ACL / Shared Kernel / OHS / etc.] |

### Dependency Direction Policy
- Rule: [e.g., "All dependencies point inward: infrastructure → application → domain"]
- Enforcement: [import-linter / CI check / code review convention]

### Architectural Pattern Rationale
| Decision | Pattern | Why | Alternatives Considered |
|----------|---------|-----|------------------------|
| [decision] | [pattern] | [justification] | [what was rejected and why] |

### SOLID Strategy
| Principle | Application Strategy | Key Extension Points |
|-----------|---------------------|---------------------|
| [S/O/L/I/D] | [how it applies to this project] | [where extensibility matters] |

### Design Checklist
- [ ] Bounded contexts identified and scoped
- [ ] Dependency direction policy documented
- [ ] Architectural pattern selected with rationale
- [ ] Layer boundaries defined with enforcement plan
- [ ] Shared kernel minimized and explicitly identified
- [ ] Anti-corruption layers designed for external integrations
- [ ] Extension points identified for anticipated changes
- [ ] CQRS applicability evaluated (separate read/write models if query patterns diverge from write patterns)
- [ ] Event sourcing applicability evaluated (if audit trail, temporal queries, or event-driven integration are requirements)
- [ ] Twelve-factor compliance reviewed for deployment targets
- [ ] API contract strategy selected (API-first with spec, or code-first with generated spec)
```

#### Audit mode report

Present concrete findings with fix status:

```markdown
## Architecture Audit Report — [System Name]

### Executive Summary
- Total findings: X
- Critical: X | High: X | Medium: X | Low: X
- Fixed during audit: X
- Remaining: X

### Detected Architecture
- Dominant pattern: [detected pattern with evidence]
- Consistency: [X% of modules follow the pattern]
- Stated vs actual drift: [summary]

### Findings
| # | Severity | Phase | File:Line | Description | Status |
|---|----------|-------|-----------|-------------|--------|
| 1 | Critical | Phase 3 | src/domain/order.py:5 | Domain imports sqlalchemy — dependency direction violation | Fixed |
| 2 | High | Phase 5 | src/models/user.py | Anemic domain model — 12 fields, 0 methods, all logic in UserService | Open |

> **Schema note:** The base columns (#, Severity, Phase, File:Line, Description, Status) are shared across all audit skills.

### Dependency Direction Summary
| Source Package | Target Package | Direction | Violation? |
|---------------|---------------|-----------|------------|
| [pkg] | [pkg] | [→] | [Yes/No] |

### Bounded Context Assessment
| Context | Boundary Clarity | Violations | Integration Pattern | Assessment |
|---------|-----------------|------------|--------------------|-----------|
| [name] | Clear / Fuzzy / Missing | [count] | [pattern] | [healthy / needs attention / critical] |

### SOLID Compliance Summary
| Principle | Compliance | Key Findings |
|-----------|-----------|-------------|
| Single Responsibility | X/Y modules compliant | [summary] |
| Open/Closed | [assessment] | [summary] |
| Liskov Substitution | [assessment] | [summary] |
| Interface Segregation | [assessment] | [summary] |
| Dependency Inversion | [assessment] | [summary] |

### Coupling Metrics
| Package | Ca (in) | Ce (out) | I (instability) | Assessment |
|---------|---------|---------|-----------------|-----------|

### Phase Coverage
| Phase | Status | Findings |
|-------|--------|----------|
| Phase 0: Anti-Pattern Scan | [X patterns scanned / Y findings] | [summary] |
| Phase 2: Pattern Detection | [detected pattern(s)] | [consistency %] |
| Phase 3: Dependency Direction | [X violations / Y edges] | [summary] |
| Phase 4: Bounded Contexts | [X contexts / Y violations] | [summary] |
| Phase 5: Domain Model | [archetype-appropriate assessment] | [summary] |
| Phase 6: SOLID | [per-principle summary] | [summary] |
| Phase 7: Coupling/Cohesion | [key metrics] | [summary] |
| Phase 8: CQRS/ES/12-Factor/API-First | [applicable / skipped] | [summary] |
| Phase 9: ADRs | [X documented / Y undocumented] | [summary] |

### Architectural Health Rating
- **Structural integrity**: [Strong / Adequate / Decaying / Critical]
- **Evolution readiness**: [Ready / Cautious / Risky / Blocked]
- **Overall**: [summary assessment with key recommendations]
```

---

## Important rules

- **Fix as you go.** Don't just report — remediate Critical and High issues during the audit when the fix is safe and straightforward (e.g., moving an import, extracting a module). Leave Medium and Low for the backlog.
- **Evidence-based claims.** Every finding must include file path, line number, or specific evidence (import graph edge, coupling metric). Never say "probably has coupling issues."
- **No assumptions.** Read the actual code, import statements, and module structure. Don't assume architecture from naming alone — a `domain/` directory may still import `sqlalchemy`.
- **Verify fixes.** After fixing an architectural violation, re-check that the fix doesn't introduce a new violation (e.g., breaking a circular import by moving code may create a new dependency direction issue).
- **Respect existing patterns.** If the project has established architectural patterns, extend them rather than introducing competing patterns.
- **Archetype-appropriate expectations.** A data pipeline is not a business application. Don't flag DataFrame-centric processing as an "anemic domain model" in a platform where the domain IS data transformation. Apply Phase 5 checks appropriate to the detected project archetype.
- **Judgment over prescription.** Architecture assessment requires more nuance than vulnerability scanning. A pattern that is wrong in one codebase may be right in another. Always include the "why" with findings, and downgrade or omit findings where the structural choice is defensible for the project's context.
- **Beta awareness.** This skill is under active development. Coverage will expand based on field testing. If you encounter an architectural pattern or anti-pattern not covered by the current phases, note it as an observation and flag it for skill improvement.
- **Prioritize.** Fix Critical and High findings. Track Medium and Low in the backlog. Don't let perfect architecture be the enemy of shipping.
