---
name: optimization-audit
description: Comprehensive optimization audit with two modes and a single tier. Planning mode designs performance strategy, capacity planning, and scaling architecture. Audit mode scans code and infrastructure for performance anti-patterns, inefficient algorithms, N+1 queries, missing caching, concurrency issues, and resource waste. Single tier — optimization tools are overwhelmingly free/open-source. Use when asked to "optimization audit", "performance review", "find bottlenecks", "optimize this", "check efficiency", or "resource audit".
---

# Optimization Audit

A comprehensive optimization skill with two modes and a single tier:

**Modes:**
- **Planning** (before code exists) — performance strategy, capacity planning, scaling architecture, data access design
- **Audit** (on existing code) — scanning for performance anti-patterns, inefficient algorithms, N+1 queries, missing caching, concurrency issues, and resource waste

**Single tier:** Unlike the security and observability audits, optimization tools are overwhelmingly free/open-source (profilers, EXPLAIN, load testers, linters). Enterprise APM platforms are already covered by the observability-audit skill, so a Standard/Enterprise split would duplicate coverage.

**Core question:** "Is this system using resources efficiently?"

## When to use this skill

- When the user says "optimization audit", "performance review", "find bottlenecks", "optimize this", "check efficiency", or "resource audit"
- Before designing a new system (planning mode) — to define performance strategy, capacity planning, and scaling architecture early
- On an existing codebase (audit mode) — to find and fix performance anti-patterns and resource waste
- Before a production deployment — to validate performance posture
- After adding new services, data pipelines, or performance-sensitive features
- When investigating production performance incidents or cost overruns

## Mode detection

Determine which mode to operate in based on the project state:

| Signal | Mode | Rationale |
|--------|------|-----------|
| User says "design for performance", "plan scaling", "capacity planning" | **Planning** | Architecture-level performance strategy |
| User says "audit", "optimize", "find bottlenecks", "performance review" | **Audit** | Code and infrastructure scanning |
| No source code exists yet (only docs, diagrams, RFCs) | **Planning** | Nothing to profile — design the strategy |
| Source code and/or infrastructure files exist | **Audit** | Concrete artifacts to analyze |
| Both code and a request to "plan performance" | **Both** | Run planning phases on architecture, audit phases on code |

When in doubt, ask the user. If both modes apply, run all 14 phases.

## Severity classification

Every finding must be assigned a severity:

| Severity | Criteria | Action | SLA |
|----------|----------|--------|-----|
| **Critical** | Causes outages, OOM crashes, connection exhaustion, quadratic algorithms on user-facing paths, unbounded memory growth | Fix immediately | Block release |
| **High** | Measurable performance degradation >2x expected; N+1 queries, missing indexes on production queries, no connection pooling, missing compression | Fix before next release | 1 sprint |
| **Medium** | Suboptimal but functional; oversized resources, missing caching, debug logging in production, suboptimal serialization | Schedule fix | 2 sprints |
| **Low** | Best practice deviation; naming conventions, minor allocation patterns, potential micro-optimizations | Track in backlog | Best effort |

## Audit process

Execute all applicable phases in order. Skip phases marked for a mode you are not running. Skip conditional phases (8, 9, 10, 11) when their preconditions are not met. Do NOT skip applicable phases. Do NOT claim completion without evidence.

**Phase order:** 0 → 0.5 → 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8 → 9 → 10 → 11 → 12 → 13

---

### Phase 0: Anti-Pattern Scan (Audit mode)

Fast grep-based scan for performance anti-patterns across all categories. Runs first to catch obvious issues before deeper analysis. This is the workhorse phase — most optimization audit value comes from grep-able anti-patterns.

Scan all source files for these patterns. Each match requires manual review — some may be intentional. Organize findings by category.

#### Algorithm anti-patterns

| Language | Pattern | Issue | Severity |
|----------|---------|-------|----------|
| Python | `for .* in .*:\s*for .* in .*:` (nested loops over same/related collections) | Potential O(n^2) | High |
| Python | `if .* in list_var` inside a loop | O(n) lookup per iteration; use set | High |
| Python | `re\.compile\(` inside function body (not module level) | Regex recompilation per call | Medium |
| Python | `re\.(match\|search\|findall\|sub)\(` inside a `for\|while` loop without pre-compiled pattern | Regex recompilation per iteration | High |
| Python | `str += ` or `string = string + ` in a loop | O(n^2) string building | Medium |
| JS/TS | `array\.indexOf\(` or `array\.includes\(` inside a loop | O(n) lookup per iteration; use Set | High |
| JS/TS | `string += ` in a loop | String concatenation overhead | Medium |
| JS/TS | `new RegExp\(` inside a loop | Regex recompilation per iteration | High |
| Java | `new String\(\)` or `"" \+` in a loop | StringBuilder not used | Medium |
| Go | `strings\.Contains\(` or linear search inside a loop | Use map for O(1) lookup | High |
| Go | `append\(` without pre-allocating slice capacity | Repeated reallocation | Medium |
| Any | `.sort()` when only min/max/top-K needed | Use heap / partial sort | Medium |
| Any | `(a+)+\|(a\|a)+\|(a\|b)*a(a\|b)*` regex patterns | Catastrophic backtracking (ReDoS) risk | Critical |

#### Memory anti-patterns

| Language | Pattern | Issue | Severity |
|----------|---------|-------|----------|
| Python | `@lru_cache` without `maxsize` (or `maxsize=None`) | Unbounded cache | Critical |
| Python | `global ` + mutable data structures | Global state that grows unboundedly | High |
| Python | `df = pd\.read_csv\(` on large files without `chunksize` | Entire file loaded into memory | High |
| Python | `\.append\(` or `\.extend\(` inside a loop accumulating `list[dict]` with >100K expected items | Unbounded list-of-dicts accumulation; use columnar lists, chunked writes, or per-partition processing | High |
| Python/Spark | `spark\.table\(.*\)\.toPandas\(\)` without `.filter\(\)` or `.select\(\)` | Full-table pull to driver; filter or aggregate before `.toPandas()` | Critical |
| Python | `pd\.concat\(` on a list accumulated in a loop, followed by a single write | Batch accumulation OOM; write per partition/chunk with `del` + `gc.collect()` | High |
| Python | Loading all files/partitions into memory before processing any | Batch-load-all anti-pattern; use load-process-release (Splitter pattern) one partition at a time | High |
| JS/TS | `addEventListener\(` without corresponding `removeEventListener` | Event listener leak | High |
| JS/TS | `setInterval\(` without `clearInterval` | Timer leak | High |
| JS/TS | `new Map\(\)` or `new Set\(\)` used as cache without eviction | Unbounded growth | High |
| Go | `go func\(\)` without context cancellation or done channel | Goroutine leak | Critical |
| Go | `make\(` with `0` capacity for slices that grow large | Repeated reallocation | Medium |
| Java | `static.*Map\|static.*List\|static.*Set` without size limit | Static collection leak | High |
| Java | `ThreadLocal` without `remove()` in finally block | Thread-local memory leak | High |
| Rust | `Box::leak\|mem::forget` | Intentional leak — verify intentional | Medium |
| Any | `.*cache.*=.*\{\}` or `.*cache.*= new Map` without TTL/max entries | Unbounded cache | Critical |

#### Concurrency anti-patterns

| Language | Pattern | Issue | Severity |
|----------|---------|-------|----------|
| Python | `time\.sleep\(` inside `async def` | Blocking the event loop | Critical |
| Python | `requests\.\(get\|post\)` inside `async def` | Sync HTTP in async context | Critical |
| Python | `open\(` (file I/O) inside `async def` without `aiofiles` | Sync file I/O in async context | High |
| JS/TS | `await` inside `for` loop (sequential awaits) | Should use `Promise.all()` for parallel | High |
| JS/TS | `new Promise` with blocking operations | Blocking the event loop | Critical |
| Go | `sync\.Mutex` with large critical sections | Lock contention | High |
| Go | `go func\(\)` in a loop without `semaphore` or `errgroup` | Unbounded goroutine fan-out | High |
| Java | `synchronized` on broad scope | Coarse-grained locking | High |
| Java | `Executors\.newFixedThreadPool\(1\)` | Artificially serialized execution | Medium |
| Any | `Lock\(\)` or `mutex` acquired in nested fashion | Deadlock risk | Critical |

#### Database anti-patterns

| Language | Pattern | Issue | Severity |
|----------|---------|-------|----------|
| Python (Django) | `.objects.all()` in template or loop without `.select_related()` / `.prefetch_related()` | N+1 query | Critical |
| Python (Django) | `for obj in queryset:.*obj\.related_field` | N+1 query via lazy loading | Critical |
| Python (SQLAlchemy) | `session\.query\(` inside a `for` loop | N+1 query | Critical |
| Ruby (ActiveRecord) | `.each do.*\.association_name` without `.includes()` | N+1 query | Critical |
| Java (Hibernate/JPA) | `@ManyToOne` or `@OneToMany` with default `FetchType.EAGER` or lazy without batch | N+1 / over-fetching | High |
| Any ORM | `SELECT \*` or `model.objects.all()` when specific columns suffice | Over-fetching | Medium |
| Any | `INSERT INTO` inside a `for\|while\|each` loop | Row-by-row insert instead of batch | High |
| Any | `execute\(` or `query\(` inside a loop body | Potential N+1 | High |
| SQL | `LIKE '%term%'` | Leading wildcard prevents index use | High |
| SQL | `ORDER BY.*OFFSET \d+` with large offset | Inefficient pagination; use cursor/keyset | High |
| Python | `psycopg2\.connect\(` or `create_engine\(` inside request handler | New connection per request | Critical |
| Node.js | `new Pool\(\)` or `createConnection\(` inside request handler | Pool per request | Critical |
| Go | `sql\.Open\(` inside handler instead of at startup | New pool per request | Critical |
| Java | `DriverManager\.getConnection\(` without connection pool | No pooling | Critical |

#### HTTP N+1 anti-patterns

| Language | Pattern | Issue | Severity |
|----------|---------|-------|----------|
| Python | `requests\.(get\|post\|put\|delete)\(` inside a `for\|while` loop | N+1 HTTP API calls — sequential per-item requests instead of batch | High |
| Python | `fetch_url\(` or custom HTTP wrapper inside a `for\|while` loop | N+1 via abstracted HTTP calls | High |
| Python | `httpx\.(get\|post)\(` inside a `for\|while` loop (not async) | N+1 via httpx sync client | High |
| Python | `session\.(get\|post)\(` inside a `for\|while` loop without concurrency | Sequential HTTP session calls | High |
| JS/TS | `axios\.(get\|post)\(` or `fetch\(` inside a `for\|forEach\|map` loop | N+1 API calls; should batch or parallelize | High |
| Go | `http\.Get\(` or `client\.Do\(` inside a `for` loop | Sequential HTTP requests | High |
| Any | Per-item API calls where batch endpoint exists | N+1 over network instead of database | High |

This is the network equivalent of N+1 database queries. Common in data ingestion pipelines that fetch per-record or per-match data from REST APIs. The fix is typically batch endpoints, concurrent requests (`asyncio`/`httpx.AsyncClient`/goroutine fan-out), or Scatter-Gather patterns.

#### Ingestion no-op waste anti-patterns

Ingestion pipelines that unconditionally re-fetch, re-parse, and re-write data even when nothing has changed. Unlike compute pipelines (which typically have incremental skip guards), ingestion layers are often written for correctness (idempotent `replaceWhere`) without any check for whether the data already exists. On scheduled runs, this turns every no-op into a full re-ingest, wasting minutes to hours of compute, network, and Delta transaction overhead.

**Structural analysis — not just grep:** These anti-patterns require understanding the pipeline's control flow, not just matching a regex. For each ingestion module, trace the `main()` function and answer:
1. Does it check whether data already exists in the target table before fetching from the source?
2. If all data exists, does it short-circuit (return early) or continue with fetch/parse/write?
3. How many HTTP requests, file reads, `df.count()` calls, and Delta writes occur on a no-op run?

| Language | Pattern | Issue | Severity |
|----------|---------|-------|----------|
| Python/Spark | Ingestion pipeline with `write_delta_table()` or `replaceWhere` but no preceding check against `spark.table()` or `spark.catalog.tableExists()` to skip already-ingested partitions | Missing incremental skip guard — every run re-fetches, re-parses, and re-writes all data regardless of whether it changed | High |
| Python | `fetch_url\(` or `requests\.get\(` for data source files inside a loop without first checking if the target partition exists in Delta | Unconditional download — network I/O wasted on data that will be overwritten with identical content | High |
| Python | `ET\.parse\(` or `ET\.iterparse\(` on large XML/JSON files without checking if target partition exists | Unconditional parse — CPU-intensive parsing of files whose data is already in Delta | High |
| Python/Spark | Multiple `validate_dataframe()` → `df.count()` calls that execute on every run even when no new data exists | Unnecessary Spark DAG execution — each `df.count()` triggers a full Spark job with scheduling overhead (1-3 seconds on serverless) | Medium |
| Python/Spark | `write_delta_table(..., replace_where=...)` executed unconditionally for partitions whose data has not changed | Unnecessary Delta transaction — creates new data files, transaction log entries, and metadata even for identical data | Medium |
| Python | Third-party library data fetcher (e.g., `statsbombpy`, `kloppy`) called unconditionally inside a loop without skip guard | Library-mediated download — the HTTP calls are hidden inside the library but still hit the network on every run | High |
| Python | Sequential `for` loop over all data sources (matches, competitions, files) where the loop body downloads + writes each one, but no early termination when all are already loaded | Sequential no-op loop — wall clock scales linearly with source count even when there is nothing to do | High |

**The fix pattern** (established in compute pipelines, must be applied to ingestion):

```python
existing: set[str] = set()
full_table = f"{catalog}.{schema}.{table_name}"
if spark.catalog.tableExists(full_table):
    existing = {
        str(row["partition_key"])
        for row in spark.table(full_table)
        .select("partition_key").distinct().collect()
    }
new_ids = [pid for pid in all_ids if str(pid) not in existing]
if not new_ids:
    logger.info("All %d partitions already ingested — skipping", len(existing))
    return
```

**Expected impact:** No-op runs that take 5-36 minutes per pipeline drop to <30 seconds (just the existence check).

**Audit instruction:** For every ingestion module (not compute/analytics), verify that this pattern or an equivalent exists. If the pipeline unconditionally re-downloads and re-writes on every scheduled run, flag it as High severity. Count the total HTTP requests, `df.count()` calls, and Delta writes that occur on a no-op run and include these numbers in the finding.

#### Loop-invariant computation anti-patterns

A function called inside a loop where some or all of its arguments are constant across iterations. The invariant portion should be computed once outside the loop and the result reused. This is the algebraic equivalent of factoring out a constant: `f(invariant, x_i)` → precompute `c = partial_f(invariant)`, then call `c(x_i)` per iteration.

**Severity scale:**
- **Critical**: N > 1000 iterations (batch compute, frame-level pipelines, large-dataset loops)
- **Important**: 10 < N < 1000 iterations
- **Minor**: N ≤ 10 iterations

| Language | Pattern | Issue | Severity |
|----------|---------|-------|----------|
| Python | `for .* in .*:.*\w+\(.*grid\|matrix\|model\|table\|config\b` (same non-loop variable passed to a function on every iteration) | Loop-invariant argument — compute the invariant factor once outside the loop | Scales with N |
| Python | `for .* in .*:.*\w+ \* \w+_grid \* \w+_grid` or `\w+ \* \w+ \* \w+` where two of three operands are non-loop variables | Redundant multiplication of constant factors per iteration; hoist `constant = a * b` before loop | Scales with N |
| Python | `for .* in .*:.*np\.(dot\|matmul\|einsum)\(.*\)` where one operand does not change between iterations | Matrix/tensor operation with invariant operand; precompute or cache the invariant contraction | Critical (>1000 iters) |
| Python | `for .* in .*:.*\.predict\(\|\.transform\(\|\.encode\(` where the model/transformer and non-varying input arrays are loop-invariant | ML inference call with invariant model and partial invariant input; batch the varying inputs instead | Critical (>1000 iters) |
| JS/TS | `for .* of .*\) \{.*const .* = .*\(.*\)` where the inner `const` depends only on outer-scope variables | Re-derived constant inside loop body; hoist to loop preamble | Scales with N |
| Any | `for .* in .*:.*= f(A, B)` where A and B are never reassigned in the loop body | Pure function call with loop-invariant arguments on every iteration | Scales with N |

**Audit instruction:** For every loop over a large collection (tracking frames, event sequences, batch items), inspect every function call in the loop body and classify each argument as loop-varying or loop-invariant. If a called function accepts M arguments and K ≥ 1 are invariant, flag the call and recommend restructuring to compute the invariant factor once. Pay particular attention to multiplication chains (e.g., `ppcf * grid_A * grid_B` where `grid_A * grid_B` is a constant tensor) and to any function that loads, parses, or constructs data structures from non-varying inputs.

#### Logging overhead anti-patterns

| Language | Pattern | Issue | Severity |
|----------|---------|-------|----------|
| Python | `logging\.debug\(f"` or `logging\.debug\(".*"\.format\(` | Eager string evaluation in debug | Medium |
| Python | `logger\.\w+\(.*json\.dumps\(` | Expensive serialization even when log level disabled | Medium |
| Java | `logger\.debug\("" \+` | String concatenation even if debug is off; use `{}` placeholders | Medium |
| Any | `log\.\w+\(` inside `for\|while\|each` (high-iteration loop body) | Per-iteration logging overhead | High |
| Config | `level.*DEBUG\|level.*TRACE\|LOG_LEVEL.*debug` in production config | Debug logging in production | High |
| Python | `traceback\.print_exc\(\)\|traceback\.format_exc\(\)` for handled exceptions | Unnecessary stack trace | Medium |

For each finding: record file path, line number, pattern matched, category, severity, and whether it is a true positive or intentional usage.

**Output:** Anti-pattern findings table organized by category with file paths, severity, and true/false positive classification.

---

### Phase 0.5: Documentation & Tech Debt Scan (Audit mode)

Scan project documentation for **already-known** performance concerns. Code-level grep patterns (Phase 0) catch what's visible in source files, but many performance risks are documented in planning files rather than flagged by anti-pattern grep — especially scaling risks, N+1 patterns over HTTP (not ORM), deferred compute, and architectural bottlenecks.

#### Files to scan

Search for these files (case-insensitive) in the project root and `docs/` directory:

| File | Purpose |
|------|---------|
| `TODO.md`, `TODO.txt`, `TODO` | Active task and tech debt tracking |
| `ROADMAP.md` | Future development plans, often including performance strategies |
| `PLAN.md` | Implementation plans with performance decisions |
| `TECH_DEBT.md`, `DEBT.md` | Explicit tech debt tracking |
| `CHANGELOG.md` | Recent performance-related changes |
| `docs/plans/*.md` | Phase-specific implementation plans |
| `CLAUDE.md`, `AGENTS.md` | May contain performance standards and budgets |

#### Keywords to grep

Search each file for these keywords (case-insensitive):

`performance`, `optimize`, `optimization`, `bottleneck`, `slow`, `latency`, `throughput`, `OOM`, `out of memory`, `memory`, `N+1`, `scale`, `scaling`, `cache`, `caching`, `index`, `indexing`, `timeout`, `budget`, `cost`, `expensive`, `heavy`, `vectorize`, `parallelize`, `batch`, `sequential`, `iterrows`, `toPandas`, `collect()`, `TODO`, `FIXME`, `HACK`, `tech debt`

#### What to extract

For each match, record:

| Field | Description |
|-------|-------------|
| Source file | Which documentation file |
| Item ID | TODO #, issue number, or section heading |
| Description | The documented performance concern |
| Current status | Active, deferred, resolved, or planned |
| Related code | File paths or module names mentioned |

#### Why this phase exists

- **N+1 over HTTP** may not match ORM-focused grep patterns but is documented in TODO files
- **OOM risks at scale** are invisible in code that works fine at current volume but documented as known debt
- **Deferred compute** (e.g., provisioned columns not yet populated) is intentional but worth surfacing
- **Planned optimizations** (caching layers, horizontal scaling) provide context for audit findings

#### Integration with later phases

Findings from this phase should be **cross-referenced** in the final report (Phase 13). For each code-level finding, note whether it was already tracked in documentation. For documented concerns not caught by code scanning, add them to the findings with source attribution.

**Output:** Table of documented performance concerns with status, related code paths, and cross-reference notes for later phases.

---

### Phase 1: Discovery (Both modes)

Explore the project to understand its performance surface:

- Read `CLAUDE.md`, `README.md`, `AGENTS.md`, and any architecture docs
- Read `TODO.md`, `ROADMAP.md`, `PLAN.md`, and `TECH_DEBT.md` if they exist — note any documented performance concerns (these feed into Phase 0.5 cross-referencing)
- Identify the tech stack, frameworks, and language versions
- Map the **performance surface**:
  - Services and entry points: APIs, workers, cron jobs, event consumers
  - Data stores: databases, caches, queues, object storage
  - External integrations: third-party APIs, SaaS services, cloud provider services
  - Deployment model: containers, serverless, VMs, managed services
  - Workload profile: request-driven, batch, streaming, event-driven, mixed
  - Traffic patterns: steady-state, bursty, diurnal, seasonal
  - Existing performance baselines: SLAs, SLOs, latency targets, throughput targets
  - Performance-sensitive paths: checkout, search, real-time feeds, data ingestion
  - Data pipeline components: ETL/ELT jobs, dbt models, Airflow DAGs, Spark jobs
  - Frontend assets: JS bundles, CSS, images, CDN configuration
  - Infrastructure-as-code: Terraform, CloudFormation, Pulumi, Kubernetes manifests
  - Profiling and benchmarking tooling: existing load tests, profilers, performance budgets

**Output:** A performance surface summary listing all services, data stores, deployment model, workload profile, and performance-sensitive paths.

---

### Phase 2: Algorithm & Data Structure Efficiency (Audit mode)

Evaluate algorithm complexity and data structure selection on hot paths.

Load `templates/algorithm-complexity.md` for the full Big-O reference with per-language profiling tools and data structure selection guide.

| Check | What to look for | Severity if missing |
|-------|-----------------|---------------------|
| Unnecessary nested loops | O(n^2) or worse where O(n) or O(n log n) is achievable | High |
| Linear search on large collections | Sequential scan where hash map / set / binary search applies | High |
| Repeated computation | Same expensive calculation performed multiple times without caching | Medium |
| Inefficient sorting | Sorting entire collection when only top-K needed (use heap) | Medium |
| String concatenation in loops | Building strings with `+=` instead of `StringBuilder` / `join()` / `strings.Builder` | Medium |
| Unbounded collection growth | Lists, maps, or caches that grow without eviction or size limits | High |
| Inappropriate data structure | Using list where set provides O(1) lookup; using map where array suffices | Medium |
| Redundant traversals | Multiple passes over same collection that could merge into one | Low |
| Missing early termination | Loops that continue after the answer is found | Low |
| Quadratic string operations | Regex compilation inside loops, repeated `in` checks on lists | Medium |

#### Grep patterns

| Language | Pattern | Issue |
|----------|---------|-------|
| Python | `for .* in .*:\s*for .* in .*:` | Potential O(n^2) |
| Python | `if .* in list_var` inside a loop | O(n) lookup per iteration |
| Python | `re\.compile\(` inside function body | Regex recompilation per call |
| Python | `str += ` in a loop | O(n^2) string building |
| JS/TS | `array\.indexOf\(` or `array\.includes\(` inside a loop | O(n) lookup per iteration |
| Go | `strings\.Contains\(` inside a loop | Linear search per iteration |
| Go | `append\(` without pre-allocating capacity | Repeated reallocation |
| Any | `.sort()` when only min/max/top-K needed | Use heap / partial sort |

**Output:** Algorithm and data structure findings with Big-O assessment and recommended alternatives.

---

### Phase 3: Memory Management (Audit mode)

Evaluate memory allocation patterns, leak potential, cache sizing, and GC pressure.

| Check | What to look for | Severity if missing |
|-------|-----------------|---------------------|
| Memory leaks | Objects retained beyond useful lifetime (event listeners, closures, global caches) | Critical |
| Excessive allocation | Allocating large objects in hot paths; objects that could be pooled or reused | High |
| Buffer sizing | Buffers too small (frequent resizing) or too large (wasted memory) | Medium |
| Large object retention | Holding references to large objects (DataFrames, images, response bodies) longer than needed | High |
| Unbounded caches | In-memory caches without TTL or max-size eviction | Critical |
| Goroutine / thread leaks | Goroutines, threads, or async tasks spawned but never joined or canceled | Critical |
| Closure captures | Closures inadvertently capturing large objects or entire scopes | Medium |
| Copy vs reference | Unnecessary deep copies of large data structures | Medium |
| Object pooling absence | Frequently created/destroyed expensive objects (DB connections, HTTP clients, buffers) | High |
| GC pressure | High allocation rate causing frequent garbage collection pauses | Medium |
| Scale-aware memory risk | `.toPandas()`, `.collect()`, or full-table loads that work at current volume but will OOM at 2-5x data growth | High |
| Batch accumulation before write | Accumulating all data (via `pd.concat()`, list append, or loading all files) before a single write instead of per-partition write-and-release | High |
| Missing per-partition release | Processing multiple partitions without `del` + `gc.collect()` between partitions; peak memory = sum of all partitions instead of max single partition | High |
| Missing memory budget documentation | No documented limits for in-memory operations (e.g., max rows for `.toPandas()`, max payload size) | Medium |
| Memory budget violation for remote compute containers | Dataset or model loaded into memory without verifying that its size fits within the execution environment's RAM. Remote compute containers (HF Jobs, Lambda, Fargate, Databricks serverless UDFs) have fixed, non-configurable memory limits that differ from the developer's local machine. Severity: Critical when dataset_size > 50% of container RAM; High when dataset_size > 25%. Mitigations: column-selective loading (`usecols`, `.select()`), streaming/chunked reads, per-partition processing with release, or a larger container class. | Critical when >50% RAM |

**Scale-aware assessment:** For each `.toPandas()`, `.collect()`, `pd.read_csv()`, `pd.concat()`, or similar full-load operation, estimate whether the current data volume is close to a memory cliff. Check project documentation (TODO, ROADMAP) for known OOM risks. A function that works at 3M rows but will OOM at 6M is a High finding even if it works today. **Any code that accumulates data from multiple partitions/files into memory before writing must be flagged regardless of current data size** — the pattern itself is the anti-pattern, not the volume. The fix is always the Splitter pattern: load one partition, process, write, release, repeat.

#### Grep patterns

| Language | Pattern | Issue |
|----------|---------|-------|
| Python | `@lru_cache` without `maxsize` (or `maxsize=None`) | Unbounded cache |
| Python | `global ` + mutable data structures | Global state that grows unboundedly |
| Python | `df = pd\.read_csv\(` without `chunksize` | Entire file in memory |
| JS/TS | `addEventListener\(` without `removeEventListener` | Event listener leak |
| JS/TS | `setInterval\(` without `clearInterval` | Timer leak |
| JS/TS | `new Map\(\)` or `new Set\(\)` as cache without eviction | Unbounded growth |
| Go | `go func\(\)` without context cancellation | Goroutine leak |
| Go | `make\(` with `0` capacity for slices that grow large | Repeated reallocation |
| Java | `static.*Map\|static.*List\|static.*Set` without size limit | Static collection leak |
| Java | `ThreadLocal` without `remove()` in finally | Thread-local memory leak |
| Any | `.*cache.*=.*\{\}` without TTL/max entries | Unbounded cache |
| Python | `pd\.read_csv\(\|pd\.read_parquet\(\|pd\.read_json\(` loading an entire dataset without `usecols=`, `chunksize=`, or a preceding size check | Full dataset loaded without column pruning or size verification — may exceed container RAM | Critical (>50% RAM) |
| Python | `\.load_dataset\(\|load_from_disk\(\|Dataset\.from_` without `.select_columns(` or a memory size assertion | HF/Arrow dataset loaded in full without column pruning — remote container RAM may be insufficient | Critical (>50% RAM) |
| Python | `torch\.load\(\|np\.load\(\|joblib\.load\(` without a preceding `os\.path\.getsize\(` or documented size check against container RAM | Large artifact loaded without verifying it fits in container memory | High |
| Any | `# TODO.*memory\|# FIXME.*OOM\|# NOTE.*RAM\|# WARN.*size` near a data-loading call | Acknowledged memory risk — verify container RAM budget is documented and enforced | High |

**Output:** Memory management findings with leak risk assessment and remediation recommendations.

---

### Phase 4: Concurrency & Parallelism (Audit mode)

Evaluate thread/goroutine pools, async correctness, lock contention, and backpressure mechanisms.

Load `templates/concurrency-patterns.md` for the full concurrency reference with thread pool sizing formulas and Enterprise Integration Patterns.

| Check | What to look for | Severity if missing |
|-------|-----------------|---------------------|
| Thread pool sizing | Thread pool size appropriate for workload (CPU-bound: ~core count; I/O-bound: higher) | High |
| Async/await correctness | Blocking calls inside async functions; missing `await`; sync I/O in async context | Critical |
| Lock contention | Coarse-grained locks that serialize concurrent operations | High |
| Deadlock potential | Lock ordering violations, nested lock acquisition | Critical |
| Race conditions | Shared mutable state accessed without synchronization | Critical |
| Connection pool exhaustion | All connections in use, new requests blocked or rejected | Critical |
| Worker pool saturation | All workers busy, incoming work queued unboundedly | High |
| Unnecessary serialization | Sequential processing where parallel would be safe and faster | Medium |
| Fan-out without backpressure | Spawning unbounded concurrent operations (e.g., 10K goroutines hitting same API) | High |
| Context / cancellation propagation | Long-running operations not respecting cancellation signals | Medium |

#### Grep patterns

| Language | Pattern | Issue |
|----------|---------|-------|
| Python | `time\.sleep\(` inside `async def` | Blocking the event loop |
| Python | `requests\.\(get\|post\)` inside `async def` | Sync HTTP in async context |
| Python | `open\(` inside `async def` without `aiofiles` | Sync file I/O in async context |
| Python | `ThreadPoolExecutor\(max_workers=` | Verify sizing is reasonable |
| JS/TS | `await` inside `for` loop | Sequential awaits; use `Promise.all()` |
| Go | `sync\.Mutex` with large critical sections | Lock contention |
| Go | `go func\(\)` in a loop without semaphore/errgroup | Unbounded fan-out |
| Java | `synchronized` on broad scope | Coarse-grained locking |
| Java | `Executors\.newFixedThreadPool\(1\)` | Artificially serialized |
| Any | `Lock\(\)` or `mutex` acquired in nested fashion | Deadlock risk |
| Any | `global\|static\|shared` mutable state without lock | Race condition risk |

**Output:** Concurrency findings with contention analysis and recommended patterns.

---

### Phase 5: Database & Query Optimization (Both modes)

Evaluate query efficiency, indexing strategy, connection pooling, and ORM patterns.

Load `templates/database-optimization.md` for the full database optimization reference with N+1 detection per ORM, EXPLAIN analysis, and connection pooling guidance.

**Planning mode:** Design the data access strategy:
- Which queries will be on the critical path? (latency-sensitive vs background)
- What indexing strategy is appropriate for the access patterns?
- How will connection pooling be configured? (pool size, idle management)
- What ORM patterns will prevent N+1 queries? (eager loading, batch fetching)
- What pagination strategy? (cursor/keyset for large datasets, offset for small)
- Where are read replicas appropriate?

**Audit mode:**

| Check | What to look for | Severity if missing |
|-------|-----------------|---------------------|
| N+1 queries | Loop that executes a query per iteration instead of batch/join | Critical |
| Missing indexes | Queries filtering or joining on non-indexed columns; full table scans | Critical |
| SELECT * usage | Fetching all columns when only a few are needed | Medium |
| Unbounded queries | Queries without LIMIT or pagination on potentially large result sets | High |
| Missing EXPLAIN analysis | Complex queries not analyzed with EXPLAIN/EXPLAIN ANALYZE | High |
| Inefficient JOINs | Cartesian products, joining on non-indexed columns, unnecessary JOINs | High |
| Query in loop | Individual INSERTs/UPDATEs instead of batch operations | High |
| Unused indexes | Indexes that exist but are never used by any query | Medium |
| Over-indexing | Too many indexes on write-heavy tables, slowing inserts/updates | Medium |
| Missing connection pooling | New connection per request instead of reusing pooled connections | Critical |
| Full table scans on large tables | Sequential scans where index scan is possible | High |
| Lock contention from long transactions | Transactions held open longer than necessary | High |
| Missing read replicas | All queries hitting the primary; reads not offloaded | Medium |
| Offset-based pagination on large datasets | Using OFFSET for deep pagination (degrades linearly) | High |

#### Grep patterns

| Language | Pattern | Issue |
|----------|---------|-------|
| Python (Django) | `.objects.all()` without `.select_related()` / `.prefetch_related()` | N+1 query |
| Python (Django) | `for obj in queryset:.*obj\.related_field` | N+1 via lazy loading |
| Python (SQLAlchemy) | `session\.query\(` inside a `for` loop | N+1 query |
| Python (SQLAlchemy) | `relationship\(` without `lazy='joined'` or `lazy='subquery'` when always accessed | Lazy loading N+1 |
| Ruby (ActiveRecord) | `.each do.*\.association_name` without `.includes()` | N+1 query |
| Java (Hibernate/JPA) | `@ManyToOne` or `@OneToMany` with default fetch or lazy without batch | N+1 / over-fetching |
| Any ORM | `SELECT \*` when specific columns suffice | Over-fetching |
| Any | `INSERT INTO` inside a `for\|while\|each` loop | Row-by-row insert |
| Any | `execute\(` or `query\(` inside a loop body | Potential N+1 |
| SQL | `LIKE '%term%'` | Leading wildcard prevents index use |
| SQL | `ORDER BY.*OFFSET \d+` with large offset | Inefficient pagination |
| SQL | `SELECT.*FROM.*WHERE.*NOT IN \(SELECT` | Subquery vs JOIN performance |
| Python | `psycopg2\.connect\(` or `create_engine\(` inside request handler | New connection per request |
| Python | `requests\.Session\(\)` created per request | Session per request |
| Node.js | `new Pool\(\)` or `createConnection\(` inside request handler | Pool per request |
| Go | `sql\.Open\(` inside handler | New pool per request |
| Java | `DriverManager\.getConnection\(` without pool | No connection pooling |
| Any | `max_connections=1` or very low pool sizes | Artificial bottleneck |

Note: For N+1 patterns over HTTP (REST API calls in loops instead of ORM queries in loops), see **Phase 0 → HTTP N+1 anti-patterns**. The same principle applies — batch or parallelize instead of sequential per-item requests.

**Output:** Database optimization findings with query analysis, indexing gaps, and connection pooling assessment.

---

### Phase 6: Caching Strategy (Both modes)

Evaluate cache layers, invalidation correctness, hit ratios, memoization, and HTTP caching.

Load `templates/caching-strategies.md` for the full caching reference with 5-layer cache architecture, invalidation patterns, and stampede protection.

**Planning mode:** Design the caching strategy:
- Which operations are cacheable? (read-heavy, stable data, expensive computations)
- What cache layers are needed? (L1 in-process, L2 distributed, CDN, HTTP, browser)
- What invalidation strategy? (TTL, event-driven, write-through, write-behind)
- How will cache stampede be prevented? (singleflight, probabilistic early expiry, locking)
- What are the consistency requirements? (eventual consistency acceptable? TTL tolerance?)

**Audit mode:**

| Check | What to look for | Severity if missing |
|-------|-----------------|---------------------|
| Missing cache for repeated expensive operations | Same DB query, API call, or computation repeated with same inputs | High |
| Cache invalidation correctness | Stale data served after source of truth changes | Critical |
| Cache sizing | Cache too small (constant eviction) or too large (memory waste) | Medium |
| TTL appropriateness | TTL too short (frequent misses) or too long (stale data) | Medium |
| Cache stampede protection | Thundering herd when cache expires (all requests hit backend) | High |
| Memoization opportunities | Pure functions called repeatedly with same arguments without memoization | Medium |
| HTTP cache headers | Missing `Cache-Control`, `ETag`, `Last-Modified` on cacheable responses | Medium |
| CDN configuration | Static assets and cacheable API responses not served from CDN | Medium |
| Multi-layer caching | Missing L1 (in-process) + L2 (distributed) for high-traffic paths | Low |
| Cache warming | Cold start after deployment with no pre-warming strategy | Low |

#### Grep patterns

| Language | Pattern | Issue |
|----------|---------|-------|
| Python | Expensive function without `@lru_cache` / `@cache` decorator | Missing memoization |
| Python | `redis\.get\(` with `redis\.set\(.*ex=None` | Cache without expiry |
| JS/TS | No `Cache-Control` header in API response middleware | Missing HTTP cache headers |
| HTTP | `Cache-Control: no-cache, no-store` on all responses including static assets | Over-restrictive caching |
| HTTP | No `ETag` or `Last-Modified` on GET responses | Missing conditional request support |
| Any | `cache\.delete\(` or `cache\.invalidate\(` absent after write operations | Missing cache invalidation |
| Any | Identical query or API call appearing in multiple code paths | Cacheable operation not cached |

**Output:** Caching strategy findings with hit ratio analysis, invalidation gaps, and recommended cache layers.

---

### Phase 7: Serialization & Network (Audit mode)

Evaluate data serialization format, compression, protocol optimization, and payload sizing.

| Check | What to look for | Severity if missing |
|-------|-----------------|---------------------|
| Serialization format choice | JSON vs Protobuf vs MessagePack vs Avro for the use case | Medium |
| Over-serialization | Serializing and deserializing data that will just be passed through | High |
| Large payload transfer | Transferring entire objects when only a subset of fields is needed | High |
| Response compression | gzip/brotli/zstd not enabled for API responses | High |
| Repeated serialization | Same object serialized multiple times in a request lifecycle | Medium |
| HTTP/2 or HTTP/3 | Modern HTTP protocol not enabled for multiplexing and header compression | Medium |
| Keep-alive connections | TCP/HTTP keep-alive disabled, creating connections per request | High |
| Request batching | Multiple small API calls that could be batched into one | Medium |
| Chatty APIs | Too many round trips for a single user action | High |
| Base64 bloat | Binary data Base64-encoded in JSON (33% overhead) where binary transport available | Medium |

#### Grep patterns

| Language | Pattern | Issue |
|----------|---------|-------|
| Python | `json\.dumps\(.*json\.loads\(` in sequence | Unnecessary serialization round-trip |
| Python | `pickle\.dumps\|pickle\.loads` for data transfer | Slow, insecure serialization |
| JS/TS | `JSON\.parse\(JSON\.stringify\(` | Deep clone via JSON — expensive |
| JS (frontend) | `fetch\(\)` in a `for\|forEach\|map` loop | Sequential API calls; should batch |
| JS (frontend) | `setInterval\(.*fetch\|poll` with short interval | Consider WebSocket/SSE |
| Server config | `gzip off\|compress: false\|compression: false` | Compression disabled |
| Server config | `keepalive_timeout 0\|Connection: close` | Keep-alive disabled |
| Nginx | `http2 off` or missing `http2` directive | HTTP/2 not enabled |
| Any | `base64` encoding of large binary payloads in JSON responses | 33% overhead; use binary format |
| Any | `for .* in .*: .*\.to_json\(\)\|\.to_dict\(\)` | Per-item serialization in loop |
| Any | Response without `Content-Encoding: gzip\|br\|zstd` header | Missing compression |

**Output:** Serialization and network findings with payload analysis and compression recommendations.

---

### Phase 8: Frontend & API Optimization (Audit mode) — CONDITIONAL

**Only execute this phase if frontend code exists** (HTML, CSS, JS/TS, React, Vue, Angular, Svelte, or if the project serves API responses that shape client rendering).

Load `templates/frontend-performance.md` for the full frontend performance reference with Core Web Vitals, bundle optimization, and rendering patterns.

| Check | What to look for | Severity if missing |
|-------|-----------------|---------------------|
| Bundle size | JavaScript bundle too large, not code-split | High |
| Code splitting | Monolithic bundle instead of route-based splitting | High |
| Tree-shaking | Dead code not eliminated from production bundles | Medium |
| Image optimization | Unoptimized images (no WebP/AVIF, no responsive sizes, no lazy loading) | High |
| Render-blocking resources | CSS/JS blocking initial render without `async` / `defer` | High |
| Font loading | Custom fonts blocking text rendering (no `font-display: swap`) | Medium |
| Third-party scripts | Heavy third-party scripts loaded synchronously | High |
| Unnecessary re-renders | React/Vue components re-rendering when props haven't changed | Medium |
| Missing virtual scrolling | Rendering thousands of list items instead of virtualizing | High |
| Core Web Vitals | LCP, INP, CLS not meeting thresholds | High |
| Pagination (API) | Large collections returned without pagination | Critical |
| Cursor-based pagination | Large datasets using offset instead of cursor/keyset pagination | High |
| Sparse fieldsets | API returns all fields when clients only need a subset | Medium |
| GraphQL query complexity | No depth/cost limiting on GraphQL queries | High |

#### Grep patterns

| Language | Pattern | Issue |
|----------|---------|-------|
| HTML | `<script src=` without `async\|defer\|type="module"` | Render-blocking script |
| HTML | `<img ` without `loading="lazy"` (below fold) | Eager image loading |
| HTML | `<img ` without `srcset` or `<picture>` | No responsive images |
| CSS | `@import url\(` in CSS (not preprocessor) | Render-blocking cascade |
| CSS | `* \{` universal selector | Performance-impacting CSS |
| React | Component without `React.memo\|useMemo\|useCallback` on expensive renders | Unnecessary re-renders |
| React | `useEffect\(\(\) =>.*fetch` without cleanup/caching | Missing data caching |
| JS | `document\.querySelectorAll\(` inside `requestAnimationFrame\|scroll\|resize` handler | Layout thrashing |
| JS | `import ` (static import) of large libraries not needed on initial load | Should be dynamic `import()` |
| Webpack/Vite | No `splitChunks\|manualChunks` configuration | Missing code splitting |
| Django | `serializer_class =` without `fields = ` specification | Serializing all fields |
| FastAPI | `response_model=` returning full model when subset would do | Over-fetching |
| Express | `res\.json\(results\)` without pagination metadata | Missing pagination |
| GraphQL | No `depthLimit\|costAnalysis\|queryComplexity` middleware | Unbounded query depth |
| Any API | `return .*\.all\(\)\|return .*find\(\{\}\)` without limit/pagination | Unbounded response |

**Output:** Frontend and API optimization findings with bundle analysis, Core Web Vitals assessment, and API response shaping recommendations.

---

### Phase 9: Data Pipeline Efficiency (Both modes) — CONDITIONAL

**Only execute this phase if data pipeline tools are detected** (dbt, Spark, Airflow, Dagster, Prefect, Pandas for ETL, or similar pipeline frameworks).

Load `templates/pipeline-efficiency.md` for the full pipeline efficiency reference with batch/stream trade-offs, incremental processing patterns, storage format selection, distributed execution (`applyInPandas`), synthetic partition keys, non-distributable computation classification, multi-pass architecture, and redundant computation detection.

**Planning mode:** Design the pipeline efficiency strategy:
- What are the latency requirements? (batch overnight, micro-batch hourly, near-real-time)
- Which pipelines should be incremental vs full rebuild?
- What storage format is appropriate? (Parquet for analytics, Delta/Iceberg for updates)
- How will data skew be detected and mitigated?
- What dead letter handling is needed for failed records?
- How will ingestion pipelines detect existing data and short-circuit on no-op runs? (skip guards)
- For large data sources (>1 GB per record/file), how will data be ingested without loading entirely into driver memory? (streaming download, Spark-native readers)

**Audit mode:**

| Check | What to look for | Severity if missing |
|-------|-----------------|---------------------|
| Batch vs streaming mismatch | Using batch for near-real-time, or streaming for overnight analytics | High |
| Full recomputation vs incremental | Reprocessing entire dataset when only new/changed records need processing | High |
| Data skew | Uneven partition sizes causing some tasks to take much longer | High |
| Shuffle operations | Unnecessary shuffles in distributed computation (Spark: repartition, groupByKey) | High |
| Storage format | Row-format (CSV, JSON) for analytical queries instead of columnar (Parquet, ORC) | High |
| Compression | Uncompressed data in storage or transit | Medium |
| Predicate pushdown | Filtering after read instead of pushing predicates to storage layer | High |
| Column pruning | Reading all columns from wide tables when only a few are needed | Medium |
| Materialization strategy | Recomputing expensive intermediate results instead of materializing them | Medium |
| Idempotency | Pipeline not safe to re-run (produces duplicates or corrupts state) | High |
| Dead letter handling | Failed records silently dropped instead of quarantined | High |
| Row-by-row processing | Python loops over DataFrames instead of vectorized operations | High |
| Ingestion no-op waste | Ingestion pipeline unconditionally re-fetches, re-parses, and re-writes all data on every scheduled run — even when all data already exists in the target table. Must check existing partitions and short-circuit. See Phase 0 "Ingestion no-op waste anti-patterns" for the fix pattern and audit instructions | High |
| Unconditional source download | Data source files (HTTP, cloud storage, UC Volume) downloaded on every run without first checking if the target Delta partition already exists. Trace the full `main()` flow: count HTTP requests, file reads, and Delta writes that execute on a no-op run where nothing is new | High |
| Multi-pass file parsing | Same large file (XML, JSON, CSV) parsed multiple times when a single pass could extract all needed data. Common with `ET.iterparse` where ball and player data are extracted in separate passes over the same file | Medium |
| Missing download cache for static sources | Pipeline downloads files from external URLs (GitHub, Figshare, S3) on every run when the source data is immutable. Should cache to local or cloud storage (UC Volume) on first download and read from cache thereafter | Medium |
| Batch accumulation before write | Collecting all partitions/files into memory (via `pd.concat()` list, dict accumulation, or loading all files) before a single write operation instead of per-partition write-and-release (Splitter/EIP pattern) | Critical |
| Full-table `.toPandas()` without filter | `spark.table(x).toPandas()` pulling entire tables to driver memory without `.filter()`, `.select()`, or `.limit()` — must filter to bounded subsets first | Critical |
| Missing partition-level release | Processing multiple data partitions without `del df` + `gc.collect()` between iterations; peak memory = sum of all partitions instead of max single partition | High |
| Schema merge on full overwrite | Using `mergeSchema=true` with `mode="overwrite"` — causes schema conflicts when column types change; use `overwriteSchema=true` for full overwrites | Medium |
| Driver-bound computation | Work pulled to driver via `.toPandas()` that could stay distributed via `applyInPandas` / `mapInPandas` grouped by natural partition key (match_id, game_id, user_id). Chunk-and-release fixes OOM but does not fix throughput — executors sit idle while the driver processes sequentially | High |
| Suboptimal group key for distributed execution | Using coarse grouping (e.g., `match_id`) when finer grouping (e.g., `(match_id, period)` or `(match_id, batch_id)`) would increase parallelism without breaking correctness. Apply the **formal decomposability test**: (1) loop body is independent per group — no cross-group state or ordering dependency, (2) final result is an aggregation (sum, count, mean, max) over per-group outputs, (3) aggregation is associative and commutative — partial results can be combined in any order. If all three hold, use finer group keys + Spark-native aggregation. When natural sub-groups don't exist, create **synthetic partition keys**: `batch_id = (monotonic_key / batch_size).cast("int")`. Size groups so `n_rows × n_cols × 8 bytes / n_groups < UDF_memory_limit` (1 GB on serverless) | Medium |
| Loop-invariant computation in batch loops | A function called N times inside a loop where K of its M arguments are loop-invariant (same value on every iteration). The invariant factor should be computed once before the loop and reused. Common pattern: `result_i = f(constant_grid_A * constant_grid_B, varying_x_i)` where `constant_grid_A * constant_grid_B` is recomputed N times instead of once. Severity: Critical when N > 1000 (frame-level or batch compute loops), Important when 10 < N ≤ 1000, Minor when N ≤ 10. | Critical (N > 1000) |
| Redundant setup in per-item function calls | A function called N times in a loop that repeats identical setup (DataFrame splits, coordinate conversions, model loading, matrix construction) on each call when input data is shared across calls. Should accept batched inputs (e.g., `(n, 2)` array of points instead of scalar pair) | High |
| Missing executor-side model caching | UDF loads ML model or large lookup table on every group invocation instead of caching at module level. On serverless (no broadcast variables), use a module-level `_model_cache: dict[str, object]` that lazy-loads from shared storage (UC Volume, S3, GCS) inside the UDF body. Spark reuses Python worker processes across groups, so the model is loaded once per executor, not once per group | Medium |
| Cache-eligible repeated computation across iterations | Same expensive computation (hierarchical clustering, spatial indexing, model loading) repeated for iterations sharing identical input data. Should cache by input hash or group key | Medium |
| Map-reduce decomposable loops | A loop that accumulates per-key sums/counts across iterations, where the loop body is independent per iteration. Apply the **formal decomposability test** (see "Suboptimal group key" above). Candidate for `applyInPandas` + Spark-native `groupBy().agg()` | High |
| Non-distributable computation | Operations that CANNOT be migrated to `applyInPandas` — identify these to avoid wasted refactoring effort. Criteria: (a) global operations requiring cross-group state (TF-IDF vectorization, global normalization, cross-source entity resolution), (b) training operations that need the full corpus for statistical validity, (c) operations where result depends on relative ordering across the full dataset. These must stay on the driver or use a single large executor. Document explicitly why distribution is not possible | Low (informational) |
| Multi-pass distributed architecture | Pipeline stages with different grouping requirements that should chain multiple `applyInPandas` calls with progressively coarser grouping. Example: credit assignment is per-event within a period (group by `(match_id, period)`), but value estimation needs all credits from a match (group by `match_id`). Each pass writes an intermediate Spark DataFrame; the next pass reads it with a coarser group key | Medium |
| Batch-ready inner function not exposed | A function called N times in a loop where the function's core computation (matrix operations, numerical integration) already supports array/batch inputs internally, but the wrapper function accepts only scalars. The batch version may only need to hoist setup and call the existing computation with stacked inputs — check the function's inner math, not just its public signature | High |
| Memory budget violation for remote compute containers | A dataset, model, or intermediate result is loaded into full memory inside a pipeline step without verifying it fits within the execution environment's RAM. Remote compute environments (HF Jobs GPU instances, Lambda, Fargate, Databricks serverless UDF executors) have fixed, non-configurable memory limits that may be substantially smaller than a developer's local machine or a Spark driver. Loading a 12 GB dataset on a 16 GB driver node leaves no headroom for Spark overhead and will OOM. Mitigations: column-selective loading, streaming/chunked reads, per-partition write-and-release, or selecting a larger container class. Severity: Critical when dataset_size > 50% of container RAM; High when dataset_size > 25% of container RAM. | Critical (>50% RAM) |
| Anti-corruption layer at ingestion boundaries | External data sources (third-party APIs, vendor feeds, open data) have their own schema conventions, naming, and semantics. If the external schema propagates unchanged through bronze into silver/gold, downstream code becomes coupled to the external vendor's model — a vendor rename or schema change breaks the entire pipeline. The bronze layer should normalize external schemas into the project's internal naming conventions and data types. Check: do column names in silver/gold tables match internal domain vocabulary, or do they preserve external vendor naming (e.g., `statsbomb_xg` vs `expected_goals`, `skillcorner_player_id` vs `player_id`)? | Medium |
| Cross-context data coupling | In multi-pipeline architectures, one pipeline directly reading another pipeline's intermediate (bronze/silver) tables creates hidden coupling. The correct pattern is consuming published interfaces — gold/mart tables with enforced contracts — not internal implementation artifacts. Check: do pipelines read from other pipelines' staging/intermediate tables, or only from their own raw inputs and shared gold tables? | High |

#### Grep patterns

| Language | Pattern | Issue |
|----------|---------|-------|
| Spark/PySpark | `groupByKey\(\)` instead of `reduceByKey\(\)` or `aggregateByKey\(\)` | Unnecessary shuffle, high memory |
| Spark/PySpark | `collect\(\)` on large datasets | Bringing all data to driver |
| Spark/PySpark | `repartition\(\d+\)` without clear justification | Unnecessary shuffle |
| Spark/PySpark | `\.toPandas\(\)` on large DataFrames | Converting distributed to local memory |
| dbt | `materialized='table'` on models that could be `incremental` | Full rebuild each run |
| dbt | No `is_incremental()` guard in incremental models | Not truly incremental |
| Pandas | `pd\.read_csv\(` for large files without `chunksize` or `usecols` | All data in memory |
| Pandas | `df\.apply\(` on row axis for vectorizable operations | Python-speed instead of C-speed |
| SQL | `INSERT INTO.*SELECT \*` without column specification | Over-fetching in ETL |
| Any | `to_csv\(\)` for data used analytically downstream | Should use Parquet |
| Any | `for row in` iteration over large dataset instead of vectorized ops | Row-by-row processing |
| Python | `all_.*\.append\(` or `results\.append\(` in a loop followed by `pd\.concat\(all_` | Batch accumulation; write per partition with `del` + `gc.collect()` |
| Python/Spark | `spark\.table\(.*\)\.toPandas\(\)` without preceding `.filter\(\)` or `.select\(\)` | Full-table pull to driver; filter first |
| Python | `json\.loads\(.*\.read\(\)\)` or `pd\.read_json\(` loading all files before processing | Load-all-then-process; use load-process-release per file |
| Python | `rows\.append\(\{` or `rows\.append\(dict\(` in a loop over >100K iterations | List-of-dicts accumulation; use chunked writes or columnar lists |
| Python/Spark | `option\("mergeSchema".*\).*mode\("overwrite"\)` | Schema merge on full overwrite; use `overwriteSchema` instead |
| Python/Spark | `for .* in .*:.*\.toPandas\(\)` followed by `spark\.createDataFrame\(` in same loop | Driver round-trip per iteration; use `applyInPandas` to keep data on executors |
| Python | `for i in range\(len\(df\)\):` calling a function that accepts DataFrame + scalar from that row | Potential batched-function-call optimization — pass all scalars at once via vectorized call |
| Python | `def .*\(.*df.*,.*x.*float.*,.*y.*float` (function accepting DataFrame + single point) | Candidate for batch version accepting `(n, 2)` array of points instead of scalar pair |
| Python | Same `groupby\(\)` or clustering/indexing call repeated inside a loop where input data doesn't change between iterations | Cache-eligible: pre-compute once outside loop or cache by input hash |
| Python | `for .* in .*:.*\w+ \* \w+_grid\|\w+_grid \* \w+` where `\w+_grid` is not the loop variable | Loop-invariant grid multiplication — hoist `constant = grid_A * grid_B` before loop |
| Python | `for .* in .*:.*\w+\(.*\w+_grid\b.*,.*\w+_grid\b` (non-loop variables passed to a function on every iteration) | Loop-invariant function arguments — factor out the invariant computation before the loop |
| Python/Spark | `write_delta_table\(` or `\.saveAsTable\(` or `replaceWhere` inside a `for` loop without a preceding `spark\.catalog\.tableExists\(` or `spark\.table\(.*\)\.select\(.*\)\.distinct\(\)\.collect\(\)` guard | Unconditional write — ingestion no-op waste; add skip guard before fetch+write loop |
| Python | `def main\(` in ingestion module where the function body contains `fetch_url\(` or `requests\.get\(` or library data fetcher (e.g., `sb\.matches\(`, `load_open_data\(`) but no `spark\.catalog\.tableExists` or equivalent existence check | Missing ingestion skip guard — every scheduled run re-downloads all data |
| Python | `ET\.iterparse\(` or `ET\.parse\(` called multiple times on the same file path within one function | Multi-pass XML parsing — merge into single pass to halve I/O |
| Python | `validate_dataframe\(` called inside a loop that runs on every no-op invocation | Unnecessary Spark DAG per iteration — skip the loop entirely when no new data exists |
| dbt/SQL | Gold/mart model with `source()` or `ref()` pointing to another pipeline's staging/intermediate model rather than a shared gold table | Cross-context data coupling — consume published interfaces, not implementation artifacts |
| Python | Column names in silver/gold writes that preserve vendor prefixes (e.g., `statsbomb_`, `skillcorner_`, `wyscout_`) instead of internal domain vocabulary | Missing anti-corruption layer — normalize external naming at ingestion boundary |

#### Ingestion no-op audit procedure

In addition to the grep patterns above, **perform a structural analysis of every ingestion module** (files whose purpose is fetching data from external sources and writing to bronze/raw Delta tables). For each module:

1. **Trace the `main()` function** end-to-end and identify the outermost loop over data sources (matches, competitions, files, etc.)
2. **Count no-op operations**: How many HTTP requests, file parses, `df.count()` calls, and Delta writes execute when ALL data already exists?
3. **Check for skip guard**: Does the module query the target Delta table for existing partition keys before entering the fetch loop?
4. **Check for early termination**: If all partitions exist, does the module return immediately or continue through the loop?
5. **Check for partial skip**: Even if some partitions are skipped, are there operations (like metadata table overwrites) that still execute unconditionally?

**Report format for each ingestion module:**

| Module | No-op HTTP calls | No-op file parses | No-op `df.count()` | No-op Delta writes | Has skip guard? | Estimated no-op wall clock |
|--------|------------------|--------------------|---------------------|---------------------|-----------------|---------------------------|

**Severity:** Any ingestion module where no-op wall clock exceeds 60 seconds is a High finding. Any module where no-op wall clock exceeds 5 minutes is a Critical finding if the pipeline runs on a schedule (daily/hourly).

#### Exhaustive `.iterrows()` / `.apply(axis=1)` enumeration

In addition to the grep patterns above, **enumerate ALL instances** of `.iterrows()`, `.itertuples()`, `df.apply(axis=1)`, and `for row in df` across the entire codebase. For each instance, classify it:

| Classification | Criteria | Severity |
|----------------|----------|----------|
| **Vectorizable — data transformation** | Loop body performs aggregation, filtering, dict building, or accumulation that can be replaced with `groupby()`, `melt()`, `merge()`, `set_index().to_dict()`, or vectorized numpy operations | High (>10K rows), Medium (<10K rows), Low (<100 rows) |
| **Vectorizable — lookup optimization** | Loop body contains a DataFrame filter like `df[df["key"] == val]` that can be replaced with pre-built `groupby().get_group()` | Medium (regardless of outer loop size) |
| **Domain-required — per-item function call** | Loop body calls a function with inherently per-item logic (physics model, geometry test, ML inference with no batch API) | Acceptable — but check FOUR things: (1) inner data fetching/lookup is optimizable, (2) the function repeats setup that could be hoisted/batched (see "Redundant setup in per-item function calls" above), (3) the loop is decomposable into independent groups for `applyInPandas` distribution, (4) the inner function's underlying computation already supports batch inputs (e.g., accepts `(n, 2)` array) that the wrapper doesn't expose — check the function's core math, not just its signature |
| **Orchestration loop** | Loop iterates over a small control set (competition-seasons, match IDs) to drive batch processing | Acceptable |
| **UI / display code** | Loop builds visualization data for <100 items | Low |

**Important severity calibration:** When a loop is classified as "domain-required" but contains an inner vectorizable lookup (e.g., a DataFrame filter inside the loop), rate the **lookup optimization** separately from the loop itself. The loop is Acceptable; the inner lookup is Medium. Do not rate the entire loop as High just because it uses `.iterrows()`.

**Output:** Data pipeline efficiency findings with processing pattern analysis and storage format recommendations.

---

### Phase 10: Container & Startup Optimization (Audit mode) — CONDITIONAL

**Only execute this phase if Dockerfiles, docker-compose files, or Kubernetes manifests exist.**

| Check | What to look for | Severity if missing |
|-------|-----------------|---------------------|
| Multi-stage builds | Application image contains build tools, compilers, dev dependencies | High |
| Base image selection | Using full OS image (ubuntu, debian) instead of slim/distroless/alpine | High |
| Layer ordering | Frequently changing layers (code) not last in Dockerfile | Medium |
| Dependency caching | Package install layer not cached (dependencies reinstalled on every code change) | High |
| `.dockerignore` | `node_modules`, `.git`, `__pycache__`, test files included in build context | Medium |
| Image size | Image > 500MB for a typical application | Medium |
| Pinned versions | Base image using `latest` instead of pinned digest or version | Medium |
| Build cache utilization | CI/CD not caching Docker layers between builds | Medium |
| Non-root user | Container running as root | Medium |
| Resource limits | No CPU/memory limits in orchestrator config | High |
| Cold start time | Application takes > 30s to become ready | High |
| Eager initialization | Loading all resources at startup instead of lazy-initializing | Medium |
| Startup probe alignment | Application marked ready before it can handle requests | High |

#### Grep patterns

| Language | Pattern | Issue |
|----------|---------|-------|
| Dockerfile | `FROM (ubuntu\|debian\|centos\|node):latest` | Unpinned, oversized base image |
| Dockerfile | `COPY \. \.` before `RUN .*install` | Invalidates dependency cache on any code change |
| Dockerfile | `RUN apt-get install` without `--no-install-recommends` | Extra packages installed |
| Dockerfile | `RUN pip install` without `--no-cache-dir` | pip cache stored in image |
| Dockerfile | No `USER` instruction | Running as root |
| Dockerfile | No `.dockerignore` file alongside Dockerfile | Build context bloat |
| Dockerfile | `RUN npm install` instead of `RUN npm ci` | Non-deterministic installs |
| docker-compose | No `deploy.resources.limits` | Missing resource limits |
| Kubernetes | No `resources.limits` in pod spec | Missing resource limits |
| Kubernetes | No `HorizontalPodAutoscaler` for variable workloads | Missing auto-scaling |
| Python (Lambda) | `import (tensorflow\|torch\|pandas\|sklearn)` at module top level | Heavy imports on cold start |
| Node.js (Lambda) | `require\('aws-sdk'\)` importing entire SDK | Should import only needed client |
| Any | `time\.sleep\|Thread\.sleep` in startup sequence | Artificial startup delay |

**Output:** Container and startup optimization findings with image analysis and cold start assessment.

---

### Phase 11: Cloud Cost & Right-Sizing (Both modes) — CONDITIONAL

**Only execute this phase if IaC (Terraform, CloudFormation, Pulumi), Kubernetes manifests, or cloud deployment configuration exists.**

Load `templates/cloud-cost-optimization.md` for the full cloud cost reference with right-sizing methodology, auto-scaling patterns, cost estimation tools, and driver-vs-executor cost analysis.

**Planning mode:** Design the cost optimization strategy:
- What is the workload profile? (steady-state, bursty, diurnal, batch)
- Where can spot/preemptible instances be used? (fault-tolerant workloads, batch jobs)
- What auto-scaling strategy? (reactive, predictive, queue-based)
- What storage tiering policy? (hot/warm/cold based on access frequency)
- Can any workloads scale to zero? (serverless, KEDA, scale-to-zero on idle)

**Audit mode:**

| Check | What to look for | Severity if missing |
|-------|-----------------|---------------------|
| Over-provisioned compute | CPU utilization consistently < 20%, memory < 30% | High |
| Under-provisioned compute | CPU > 80% sustained, OOM kills, throttling | Critical |
| Auto-scaling configuration | No auto-scaling, or scaling thresholds too conservative/aggressive | High |
| Spot/preemptible usage | Fault-tolerant workloads not using spot instances (60-90% savings) | High |
| Reserved capacity | Steady-state workloads on on-demand pricing without reservations | High |
| Storage tiering | Infrequently accessed data on expensive hot storage tier | High |
| Idle resources | Running resources during off-hours (dev/staging environments) | High |
| Orphaned resources | Detached volumes, unused IPs, stale snapshots, empty load balancers | Medium |
| Serverless vs always-on | Always-on instances for bursty/infrequent workloads | Medium |
| Oversized databases | RDS instance with < 10% CPU utilization | High |
| Horizontal scaling capability | Application stateful, preventing horizontal scale-out | High |
| Scale-down policy | No scale-down cooldown causing thrashing | Medium |
| Driver-vs-executor cost waste | Executors sitting idle while the driver processes data sequentially via `.toPandas()` loops. On managed Spark (Databricks, EMR, Dataproc), executors are already provisioned and billed — migrating computation to executors via `applyInPandas` / `mapInPandas` reduces wall-clock time without increasing cost, because the same cluster resources are utilized instead of wasted. Flag any pipeline where driver CPU is the bottleneck while executor CPU is near zero | High |

#### Grep patterns

| Language | Pattern | Issue |
|----------|---------|-------|
| Terraform | `instance_type = ".*xlarge\|.*2xlarge\|.*4xlarge"` (verify against utilization) | Potentially oversized |
| Terraform | No `autoscaling_group` or `auto_scaling_configuration` | Missing auto-scaling |
| Terraform | `storage_type = "gp2"` | Should be `gp3` (cheaper, better performance) |
| Terraform | `engine = "oracle-\|sqlserver-"` | Commercial DB license costs |
| Terraform | `transition.*days = ` not configured in S3 lifecycle | No storage tiering |
| Kubernetes | `resources.requests.cpu` >> actual usage | Over-provisioned pods |
| Kubernetes | No `HorizontalPodAutoscaler` for variable workloads | Missing auto-scaling |
| Terraform/K8s | `min_size = .*max_size` (same value) | Auto-scaling effectively disabled |
| Terraform | `cooldown = 0\|cooldown_period = 0` | No scale-down cooldown; thrashing |
| Code | `session\[` or `flask\.session\[` with default in-memory store | Stateful; can't scale horizontally |
| Code | File writes to local filesystem in request handler | Local state prevents scaling |
| docker-compose | No `deploy.resources.limits` | Unbounded resource usage |

**Output:** Cloud cost and right-sizing findings with resource utilization analysis and cost optimization recommendations.

---

### Phase 12: Profiling & Benchmarking Posture (Both modes)

Evaluate the maturity of performance testing, regression detection, and profiling practices.

Load `templates/profiling-benchmarking.md` for the full profiling and benchmarking reference with per-language profiling tools, load testing methodology, and performance budget patterns.

**Planning mode:** Design the performance testing strategy:
- What performance baselines need to be established? (latency targets, throughput targets)
- Where should load tests run? (CI/CD, staging, production canary)
- What performance budgets should be enforced? (response time, bundle size, resource usage)
- How will performance regressions be detected? (CI gates, trend monitoring)

**Audit mode:**

| Check | What to look for | Severity if missing |
|-------|-----------------|---------------------|
| Performance test suite | Automated performance tests exist and run in CI/CD | High |
| Baseline metrics established | p50/p95/p99 latency baselines documented for key operations | High |
| Performance regression detection | CI/CD fails or alerts on performance degradation | High |
| Load testing | Load test scenarios cover realistic traffic patterns | Medium |
| Stress testing | System tested beyond expected peak to find breaking points | Medium |
| Profiling artifacts | CPU/memory profiles captured and analyzed for hot paths | Medium |
| Performance budget | Maximum response time, bundle size, or resource usage defined and enforced | Medium |
| Realistic test data | Load tests use representative data volumes and distributions | Medium |
| Soak testing | Extended-duration tests to detect memory leaks and resource exhaustion | Low |
| Comparative benchmarks | Performance tracked across versions / commits | Medium |

#### Grep patterns

| Language | Pattern | Issue |
|----------|---------|-------|
| Test config | No `performance\|benchmark\|load-test\|perf` directory or config | Missing performance tests |
| CI config | No performance test step in CI/CD pipeline | No regression detection |
| Any | `# TODO.*performance\|# TODO.*benchmark\|# FIXME.*slow` | Acknowledged performance debt |
| Test files | `time\.sleep\|Thread\.sleep` in performance tests | Artificial delays invalidate results |

**Output:** Profiling and benchmarking posture assessment with gaps and recommended tooling.

---

### Phase 13: Findings Report (Both modes)

Generate the final report. The format depends on the mode.

#### Planning mode report

Present the performance strategy and design recommendations:

```markdown
## Performance Strategy — [System Name]

### Performance Surface Summary
- Services: [list]
- Data stores: [list]
- Workload profile: [request-driven / batch / streaming / mixed]
- Traffic pattern: [steady / bursty / diurnal / seasonal]
- Performance-sensitive paths: [list]

### Data Access Strategy
| Path | Access Pattern | Caching | Pagination | Indexing |
|------|---------------|---------|------------|---------|
| Product search | Read-heavy, filtered | L1 + L2, 5min TTL | Cursor-based | Composite on (category, price) |

### Capacity Planning
| Component | Expected Load | Sizing | Scaling Strategy |
|-----------|--------------|--------|-----------------|
| API servers | 1K req/sec peak | 4x c5.xlarge | HPA on request rate |
| PostgreSQL | 500 queries/sec | r5.2xlarge | Read replicas for read load |

### Caching Strategy
| Layer | Technology | Scope | TTL | Invalidation |
|-------|-----------|-------|-----|-------------|
| L1 (in-process) | lru_cache | Per-instance | 60s | TTL expiry |
| L2 (distributed) | Redis | Shared | 5min | Event-driven on write |
| CDN | CloudFront | Global | 24hr | Cache-busting on deploy |

### Design Recommendations
| # | Area | Recommendation | Priority | ROI |
|---|------|----------------|----------|-----|
| 1 | Database | Implement connection pooling with pgBouncer | Critical | High effort / High gain |
| 2 | Caching | Add Redis L2 cache for product catalog | High | Medium effort / High gain |

### Performance Design Checklist
- [ ] Data access patterns identified for all critical paths
- [ ] Indexing strategy designed for query patterns
- [ ] Connection pooling configured for all data stores
- [ ] Caching layers defined with invalidation strategy
- [ ] Auto-scaling policy designed for workload profile
- [ ] Performance baselines and budgets defined
- [ ] Load testing plan created
- [ ] Storage format selected for analytical workloads (if applicable)
- [ ] Pagination strategy selected for all list endpoints
```

#### Audit mode report

Present concrete findings with fix status and ROI estimates:

```markdown
## Optimization Audit Report — [System Name]

### Executive Summary
- Total findings: X
- Critical: X | High: X | Medium: X | Low: X
- Fixed during audit: X
- Remaining: X
- Estimated performance improvement: [summary of key gains]

### Findings
| # | Severity | Phase | File:Line | Description | ROI (Effort/Gain) | Status |
|---|----------|-------|-----------|-------------|-------------------|--------|
| 1 | Critical | Phase 0 | src/api.py:42 | N+1 query in product listing (adds ~200ms/page) | Low effort / High gain | Fixed |
| 2 | High | Phase 5 | src/db.py:18 | Missing index on orders.user_id (full table scan) | Low effort / High gain | Fixed |
| 3 | Medium | Phase 6 | src/views.py:55 | Repeated API call without caching | Medium effort / Medium gain | Recommended |

> **Schema note:** The base columns (#, Severity, Phase, File:Line, Description, Status) are shared across all audit skills. The ROI (Effort/Gain) column is specific to optimization-audit.

### Quick Wins (fix in < 30 minutes, significant gain)
| # | Finding | Estimated Impact | Fix |
|---|---------|-----------------|-----|
| 1 | Add missing index on orders.user_id | ~10x query speedup | `CREATE INDEX idx_orders_user_id ON orders(user_id);` |
| 2 | Enable gzip compression on API responses | ~70% bandwidth reduction | Add compression middleware |

### Phase Coverage Matrix
| Phase | Checks Run | Findings | Key Result |
|-------|-----------|----------|------------|
| Phase 0: Anti-Patterns | [X patterns scanned] | [Y findings] | [summary] |
| Phase 0.5: Documentation Scan | [X files scanned] | [Y documented concerns] | [summary] |
| Phase 1: Discovery | [X surfaces mapped] | [Y findings] | [summary] |
| Phase 2: Algorithms | [X checks] | [Y findings] | [summary] |
| Phase 3: Memory | [X checks] | [Y findings] | [summary] |
| Phase 4: Concurrency | [X checks] | [Y findings] | [summary] |
| Phase 5: Database | [X checks] | [Y findings] | [summary] |
| Phase 6: Caching | [X checks] | [Y findings] | [summary] |
| Phase 7: Serialization | [X checks] | [Y findings] | [summary] |
| Phase 8: Frontend (if applicable) | [X checks] | [Y findings] | [summary] |
| Phase 9: Pipelines (if applicable) | [X checks] | [Y findings] | [summary] |
| Phase 10: Containers (if applicable) | [X checks] | [Y findings] | [summary] |
| Phase 11: Cloud Cost (if applicable) | [X checks] | [Y findings] | [summary] |
| Phase 12: Profiling Posture | [X checks] | [Y findings] | [summary] |

### Optimization Maturity Rating
- **Checks passed**: X/Y (Z% coverage)
- **Overall**: [Optimized / Mostly Optimized / Needs Optimization / Significant Waste]

### Phase 0.5 Cross-Reference
| Documented Concern | Source | Related Finding | Status |
|--------------------|--------|-----------------|--------|
| "N+1 sequential API calls" | TODO #3 | Finding #X (or: New — not caught by code scan) | Tracked |
| "OOM risk at 2x volume" | TODO #4 | Finding #Y (P1/P2 column projection) | Partially addressed |

### Documented Optimization Strategies (Not Yet Implemented)
If the project's ROADMAP or planning docs describe optimization strategies not yet in code, list them here for context. These are not findings — they are planned work that provides context for the audit results.

| Strategy | Source | Relevance to Audit |
|----------|--------|-------------------|
| Example: 5-layer caching architecture | ROADMAP.md | Explains why L2/L3 caching is absent (planned, not overlooked) |

### Ready for production: Yes / No (with blockers)
```

---

## Important rules

- **Fix as you go.** Don't just report — remediate. Fix Critical and High issues during the audit. Add missing indexes, enable compression, fix N+1 queries.
- **Evidence-based claims.** Every finding must include file path, line number, or specific evidence. Never say "probably slow."
- **Quantify impact.** Optimization is relative, not binary. Every finding should estimate the impact: "N+1 adds ~200ms/page" not just "N+1 found." Use Big-O analysis, EXPLAIN output, or measurement to back up claims.
- **ROI-oriented.** Findings must estimate effort vs impact. Quick wins (5 min fix, 10x gain) are prioritized over structural changes (multi-sprint, 2x gain).
- **Fix obvious wins, benchmark structural changes.** Add a missing index? Yes, fix it. Rewrite the concurrency model? Recommend benchmarking first, then fix.
- **No assumptions.** Read the actual code, configs, and infrastructure files. Don't assume performance is good because a framework is used.
- **Verify fixes.** After fixing a performance issue, re-run the check that found it to confirm the fix works.
- **Respect existing patterns.** If the project has established performance patterns, extend them rather than introducing new ones.
- **Conditional phases.** Phase 8 (Frontend) only if frontend code exists. Phase 9 (Pipeline) only if pipeline tools detected. Phase 10 (Container) only if Dockerfiles/K8s exist. Phase 11 (Cloud Cost) only if IaC/cloud config exists. Skip irrelevant phases to keep signal-to-noise high.
- **Scope awareness.** Don't flag managed-service built-in optimization as a finding (e.g., auto-scaling managed by a PaaS).
- **Single tier.** There is no Standard/Enterprise split. All checks are actionable with free/open-source tools.
- **Prioritize.** Fix Critical and High findings. Track Medium and Low in the backlog. Don't let perfect be the enemy of fast.
