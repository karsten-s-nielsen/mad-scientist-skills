# Optimization Audit Skill Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Create a single-tier, two-mode optimization audit skill with 14 phases (0-13) and 8 templates, marked as beta.

**Architecture:** Mirrors security-audit and observability-audit structure — SKILL.md defines methodology with phased audit process, templates provide language-specific patterns and tools. Single tier (no Standard/Enterprise split). Conditional phases skip irrelevant categories.

**Tech Stack:** Markdown (SKILL.md + 8 templates), Structurizr DSL (architecture.dsl update)

---

## Context

**Existing skill patterns to follow:**
- `plugins/mad-scientist-skills/skills/security-audit/SKILL.md` — two-tier, 13 phases (0-12)
- `plugins/mad-scientist-skills/skills/observability-audit/SKILL.md` — two-tier, 13 phases (0-12), beta label
- Both use: YAML frontmatter, mode detection table, severity classification, grep pattern tables, template references, report templates

**Key difference for optimization-audit:**
- **Single tier** — no Standard/Enterprise split in phase sections
- **14 phases** (0-13) — one more than the other skills
- **4 conditional phases** (8, 9, 10, 11) — skip if not applicable
- **ROI column** in findings — effort vs impact estimation
- **Beta label** in title, frontmatter description, and README

**Research reference:** `docs/specs/2026-03-08-optimization-audit-research.md` — 20 categories with complete grep patterns, tools, and metrics

**Design reference:** `docs/specs/2026-03-08-optimization-audit-design.md` — approved phase structure, templates, severity classification

---

### Task 1: SKILL.md — Frontmatter, Introduction, Mode Detection, Severity (lines 1-60)

**Files:**
- Create: `plugins/mad-scientist-skills/skills/optimization-audit/SKILL.md`

**Content specification:**

```markdown
---
name: optimization-audit
description: Comprehensive optimization audit with two modes (beta). Planning mode designs performance strategy, capacity planning, and scaling architecture. Audit mode scans code and infrastructure for performance anti-patterns, inefficient algorithms, N+1 queries, missing caching, concurrency issues, and resource waste. Single tier — optimization tools are overwhelmingly free/open-source. Use when asked to "optimization audit", "performance review", "find bottlenecks", "optimize this", "check efficiency", or "resource audit".
---

# Optimization Audit (beta)
```

- Introduction paragraph: two modes, single tier, core question ("Is this system using resources efficiently?")
- Mode detection table (same format as observability-audit): Planning/Audit/Both based on signals
- Severity classification table: Critical/High/Medium/Low with optimization-specific criteria from design doc
- Audit process instruction: "Execute all applicable phases in order..."

**Pattern to follow:** Lines 1-55 of `plugins/mad-scientist-skills/skills/observability-audit/SKILL.md`

---

### Task 2: SKILL.md — Phase 0: Anti-Pattern Scan (Audit mode)

**Files:**
- Modify: `plugins/mad-scientist-skills/skills/optimization-audit/SKILL.md`

**Content specification:**

Phase 0 is the workhorse. Comprehensive grep-based scan organized by category. Use patterns from research doc Categories 1-4, 20. Structure:

**Grep pattern tables by category:**

1. **Algorithm anti-patterns** — nested loops, linear search in loops, regex compilation in loops, string concat in loops, missing early termination
2. **Memory anti-patterns** — unbounded caches (`@lru_cache` without maxsize, `Map`/`Set` without eviction), goroutine/thread leaks, global mutable state, missing `removeEventListener`
3. **Concurrency anti-patterns** — blocking calls in async (`time.sleep` in `async def`, `requests.get` in async), sequential awaits in loops, unbounded goroutine fan-out
4. **Database anti-patterns** — N+1 queries (Django `.objects.all()` in loop, SQLAlchemy `session.query` in loop, ActiveRecord without `.includes`), `SELECT *`, queries in loops, `LIKE '%term%'`
5. **Logging overhead** — debug logging in production config, eager string evaluation in log calls, per-iteration logging

Each pattern: Language | Pattern (regex) | Issue | Severity

**Output:** Anti-pattern findings table with file paths, category, and severity.

**Pattern to follow:** Phase 0 of observability-audit SKILL.md (lines 58-100) — but single tier (no Enterprise subsection)

---

### Task 3: SKILL.md — Phase 1: Discovery (Both modes)

**Files:**
- Modify: `plugins/mad-scientist-skills/skills/optimization-audit/SKILL.md`

**Content specification:**

Explore the project to understand its performance surface:
- Read project docs (CLAUDE.md, README.md, etc.)
- Identify tech stack, frameworks, language versions
- Map the **performance surface**:
  - Services and entry points
  - Data stores and access patterns
  - External integrations and latency-sensitive paths
  - Existing performance tooling (profilers, load tests, benchmarks)
  - Deployment model (containers, serverless, VMs)
  - Data pipelines (ETL/ELT, dbt, Spark, Airflow)
  - Frontend (if applicable): framework, build tooling, CDN
  - Workload characteristics: request-driven, batch, streaming, mixed
  - Current performance baselines (if documented): p50/p95/p99 latency, throughput
  - Known performance issues or technical debt

**Output:** Performance surface summary.

---

### Task 4: SKILL.md — Phase 2: Algorithm & Data Structure Efficiency (Audit mode)

**Files:**
- Modify: `plugins/mad-scientist-skills/skills/optimization-audit/SKILL.md`

**Content specification:**

Reference `templates/algorithm-complexity.md` for per-language profiling tools and patterns.

Check table (8-10 rows):
- Unnecessary nested loops (O(n²) where O(n) achievable)
- Linear search on large collections (list where set/map applies)
- Repeated computation without memoization
- Inefficient sorting (full sort when top-K needed)
- String concatenation in loops
- Unbounded collection growth
- Inappropriate data structure choice
- Missing early termination
- Quadratic string operations (regex in loops)

Grep pattern table per language (Python, JS/TS, Java, Go, Rust).

**Output:** Algorithm findings with Big-O analysis and suggested improvement.

---

### Task 5: SKILL.md — Phases 3-4: Memory Management + Concurrency (Audit mode)

**Files:**
- Modify: `plugins/mad-scientist-skills/skills/optimization-audit/SKILL.md`

**Content specification:**

**Phase 3: Memory Management**
Reference `templates/concurrency-patterns.md` (memory section).

Check table (8-10 rows): memory leaks, excessive allocation, unbounded caches, goroutine/thread leaks, closure captures, copy vs reference, object pooling, GC pressure.

Grep patterns: `@lru_cache` without maxsize, `addEventListener` without `removeEventListener`, `go func()` without context, `setInterval` without `clearInterval`, `static.*Map` without size limit, `pd.read_csv` without chunksize.

**Phase 4: Concurrency & Parallelism**
Reference `templates/concurrency-patterns.md`.

Check table (8-10 rows): thread pool sizing, async/await correctness, lock contention, deadlock potential, race conditions, connection pool exhaustion, fan-out without backpressure, missing cancellation propagation.

Grep patterns: `time.sleep` in `async def`, `requests.get` in async, `await` in for loop (JS), unbounded `go func()`, `synchronized` on broad scope.

**Output per phase:** Findings table with file paths, issue type, severity.

---

### Task 6: SKILL.md — Phases 5-6: Database + Caching (Both modes)

**Files:**
- Modify: `plugins/mad-scientist-skills/skills/optimization-audit/SKILL.md`

**Content specification:**

**Phase 5: Database & Query Optimization**
Reference `templates/database-optimization.md`.

Planning mode: connection pooling strategy, indexing approach, query patterns, read replica strategy, pagination design.

Audit mode check table (10-12 rows): N+1 queries, missing indexes, SELECT *, unbounded queries, missing EXPLAIN analysis, inefficient JOINs, queries in loops, unused indexes, missing connection pooling, suboptimal schema, full table scans, lock contention from long transactions.

Grep patterns: Django `.objects.all()` without `select_related`, SQLAlchemy `session.query` in loop, `INSERT INTO` in loop, `LIKE '%term%'`, `OFFSET` with large values, `DriverManager.getConnection` without pool.

**Phase 6: Caching Strategy**
Reference `templates/caching-strategies.md`.

Planning mode: cache layer design (L1-L5), invalidation strategy, TTL policy, HTTP cache headers, CDN strategy.

Audit mode check table (8-10 rows): missing cache for repeated operations, cache invalidation correctness, cache sizing, TTL appropriateness, stampede protection, memoization opportunities, HTTP cache headers, CDN configuration.

Grep patterns: expensive function without `@lru_cache`/`@cache`, `redis.set` without expiry, no `Cache-Control` header, no `ETag` support, `cache.delete` absent after writes.

**Output per phase:** Findings table + recommendations.

---

### Task 7: SKILL.md — Phases 7-8: Serialization/Network + Frontend/API (Audit mode)

**Files:**
- Modify: `plugins/mad-scientist-skills/skills/optimization-audit/SKILL.md`

**Content specification:**

**Phase 7: Serialization & Network**

Check table (8-10 rows): serialization format choice, over-serialization, large payload transfer, missing compression, repeated serialization, base64 bloat, keep-alive connections, HTTP/2 or HTTP/3, request batching, chatty APIs.

Grep patterns: `JSON.parse(JSON.stringify(` for deep clone, `pickle.loads`/`pickle.dumps`, missing `Content-Encoding`, `gzip off`/`compress: false`, `fetch()` in for loop (client), `Connection: close`.

**Phase 8: Frontend & API Optimization (conditional — only if frontend exists)**

Reference `templates/frontend-performance.md`.

Check table (10-12 rows): bundle size, tree-shaking, code splitting, image optimization, render-blocking resources, font loading, third-party scripts, DOM complexity, layout thrashing, unnecessary re-renders, virtual scrolling, Core Web Vitals.

Grep patterns: `<script src=` without `async`/`defer`, `<img` without `loading="lazy"`, `import` of large libraries, React component without `memo`/`useMemo`, no `splitChunks` config.

API response checks: pagination, sparse fieldsets, compression, GraphQL query complexity, ETags/conditional requests, batch endpoints.

**Output per phase:** Findings table.

---

### Task 8: SKILL.md — Phases 9-11: Pipeline + Container + Cloud (conditional phases)

**Files:**
- Modify: `plugins/mad-scientist-skills/skills/optimization-audit/SKILL.md`

**Content specification:**

**Phase 9: Data Pipeline Efficiency (conditional — only if pipelines detected)**
Reference `templates/pipeline-efficiency.md`.

Planning mode: batch vs stream, incremental processing, storage format, partitioning strategy.

Audit mode check table (10-12 rows): full recomputation vs incremental, data skew, unnecessary shuffles, over/under-partitioning, row format for analytics, missing compression, predicate pushdown, column pruning, materialization strategy, idempotency, dead letter handling.

Grep patterns: `groupByKey()`, `collect()` on large datasets, `toPandas()`, dbt `materialized='table'` without incremental, `pd.read_csv` without `chunksize`, `df.apply` on row axis, writing CSV for analytics.

**Phase 10: Container & Startup Optimization (conditional — only if Dockerfiles/K8s exist)**

Check table (8-10 rows): multi-stage builds, base image selection, layer ordering, dependency caching, `.dockerignore`, image size, pinned versions, health check, non-root user, resource limits.

Grep patterns: `FROM ubuntu:latest`, `COPY . .` before `RUN install`, `RUN apt-get install` without `--no-install-recommends`, `RUN pip install` without `--no-cache-dir`, no `USER` instruction, `RUN npm install` instead of `npm ci`.

Cold start checks: heavy module imports in Lambda handlers, model loading at module level, sequential initialization.

**Phase 11: Cloud Cost & Right-Sizing (conditional — only if IaC/cloud config exists)**
Reference `templates/cloud-cost-optimization.md`.

Planning mode: instance type selection, auto-scaling strategy, spot/reserved mix, storage tiering, scale-to-zero candidates.

Audit mode check table (10-12 rows): over-provisioned compute, right instance type, auto-scaling configuration, spot/preemptible usage, reserved capacity, storage tiering, idle resources, orphaned resources, serverless vs always-on, oversized databases.

Grep patterns: Terraform `instance_type` with large sizes, no `autoscaling_group`, `storage_type = "gp2"`, K8s `resources.requests.cpu` >> usage, no `HorizontalPodAutoscaler`, `min_size = max_size`.

**Output per phase:** Findings table.

---

### Task 9: SKILL.md — Phases 12-13: Profiling Posture + Findings Report

**Files:**
- Modify: `plugins/mad-scientist-skills/skills/optimization-audit/SKILL.md`

**Content specification:**

**Phase 12: Profiling & Benchmarking Posture**
Reference `templates/profiling-benchmarking.md`.

Planning mode: performance testing strategy, regression detection approach, performance budgets.

Audit mode check table (8-10 rows): performance test suite exists, baseline metrics documented, performance regression detection in CI, load testing, stress testing, profiling artifacts, performance budget defined, realistic test data, soak testing, comparative benchmarks.

Grep patterns: no `performance`/`benchmark`/`load-test` directory, no performance step in CI config, `# TODO.*performance`/`# FIXME.*slow` comments.

**Phase 13: Findings Report**

Two report templates:

**Planning mode report** — performance strategy document:
- Performance surface summary
- Capacity planning recommendations
- Caching strategy design
- Scaling strategy design
- Performance budget definitions
- Optimization checklist

**Audit mode report** — concrete findings:
- Executive summary (total findings by severity, fixed during audit, remaining)
- Findings table: #, Severity, Phase, File:Line, Description, Impact, ROI (effort/gain), Status
- Phase coverage matrix: Phase | Checks Passed | Findings | Key Gap
- Quick wins section: findings fixable in <5 min with >2x improvement
- Optimization maturity rating: Optimized / Partially Optimized / Significant Waste / No Performance Discipline
- Ready for production: Yes / No (with blockers)

**Important rules section** (end of SKILL.md):
- Fix as you go (Critical/High)
- Evidence-based claims (file path, line number, or evidence required)
- Quantify impact (don't just say "slow" — measure or estimate)
- ROI-oriented (effort vs gain for each finding)
- Benchmark before structural changes
- Conditional phases — skip irrelevant ones
- No assumptions — read actual code
- Respect existing patterns

---

### Task 10: Template — algorithm-complexity.md

**Files:**
- Create: `plugins/mad-scientist-skills/skills/optimization-audit/templates/algorithm-complexity.md`

**Content specification (~500-600 lines):**

1. **Big-O Quick Reference** — common complexities with real-world examples
2. **Data Structure Selection Guide** — when to use array/list, hash map/set, heap, tree, trie, graph
3. **Per-Language Profiling Tools** — with setup commands and example usage:
   - Python: py-spy, scalene, cProfile, line_profiler
   - JS/TS: clinic.js, 0x, Chrome DevTools
   - Go: pprof (CPU, memory, goroutine)
   - Java: async-profiler, JFR, VisualVM
   - Rust: cargo flamegraph, perf
   - .NET: dotnet-trace, BenchmarkDotNet
4. **Hot Path Identification** — methodology for finding the 20% of code consuming 80% of resources
5. **Common Algorithmic Improvements** — with GOOD/BAD code examples per language:
   - Nested loop → hash join
   - Linear search → set/map lookup
   - Full sort → heap for top-K
   - String concat in loop → builder/join
   - Regex compilation → pre-compiled
6. **Vectorization Patterns** — NumPy/Pandas vectorized ops vs Python loops (from luxury-lakehouse patterns)
7. **Complexity Analysis Checklist** — systematic approach to reviewing hot paths

Source: Research doc Categories 1, 20.

---

### Task 11: Template — database-optimization.md

**Files:**
- Create: `plugins/mad-scientist-skills/skills/optimization-audit/templates/database-optimization.md`

**Content specification (~500-600 lines):**

1. **N+1 Query Detection** — per ORM with GOOD/BAD code:
   - Django: `select_related()`, `prefetch_related()`, `Prefetch()` objects
   - SQLAlchemy: `joinedload()`, `subqueryload()`, `selectinload()`
   - ActiveRecord: `.includes()`, `.joins()`, `.preload()`
   - Hibernate/JPA: `@BatchSize`, `JOIN FETCH`, EntityGraph
   - Prisma: `include`, `select`
2. **Indexing Strategy** — when to index, composite indexes, covering indexes, partial indexes, index-only scans
3. **EXPLAIN Analysis Guide** — reading EXPLAIN output for PostgreSQL, MySQL, SQLite, MongoDB
4. **Connection Pooling** — per language/framework:
   - Python: SQLAlchemy pool config, psycopg2 pool, Django CONN_MAX_AGE
   - Node.js: pg Pool, knex pool config
   - Go: sql.DB MaxOpenConns/MaxIdleConns
   - Java: HikariCP configuration
5. **Batch Operations** — INSERT batching, bulk UPDATE, UPSERT patterns
6. **Pagination Patterns** — offset vs cursor/keyset with performance comparison
7. **Query Optimization Patterns** — covering indexes, materialized views, denormalization trade-offs, read replicas
8. **Connection Pool Sizing Formula** — connections = ((core_count * 2) + effective_spindle_count) for PostgreSQL

Source: Research doc Categories 4, 5, 8.

---

### Task 12: Template — caching-strategies.md

**Files:**
- Create: `plugins/mad-scientist-skills/skills/optimization-audit/templates/caching-strategies.md`

**Content specification (~450-550 lines):**

1. **5-Layer Cache Architecture** (from luxury-lakehouse, generalized):
   - L1: In-process (lru_cache, Guava Cache, node-cache) — microseconds
   - L2: Distributed (Redis, Memcached) — low milliseconds
   - L3: HTTP (Cache-Control, ETag, Last-Modified) — varies
   - L4: CDN (CloudFront, Cloudflare, Fastly) — edge latency
   - L5: Precomputed/Materialized (materialized views, precomputed tables) — zero at read time
2. **Cache Invalidation Patterns** — TTL, event-driven, write-through, write-behind, cache-aside
3. **Stampede Protection** — lock-based, probabilistic early expiration, stale-while-revalidate
4. **HTTP Caching** — Cache-Control directives, ETag/Last-Modified, conditional requests, Vary header
5. **Memoization Patterns** — per language with GOOD/BAD code:
   - Python: `@lru_cache(maxsize=N)`, `@cache`, `cachetools`
   - JS/TS: `memoize`, `Map`-based with WeakRef
   - Go: `sync.Map`, custom with `sync.RWMutex`
   - Java: Caffeine, Guava Cache
6. **Cache Metrics** — hit ratio, eviction rate, latency, memory usage
7. **When NOT to Cache** — write-heavy data, security-sensitive data, rapidly changing data, low-latency sources

Source: Research doc Category 6, luxury-lakehouse 5-layer caching pattern.

---

### Task 13: Template — concurrency-patterns.md

**Files:**
- Create: `plugins/mad-scientist-skills/skills/optimization-audit/templates/concurrency-patterns.md`

**Content specification (~450-550 lines):**

1. **Thread Pool Sizing** — CPU-bound (~core count), I/O-bound (core count * ratio of wait/compute time), formulas per language
2. **Async/Await Correctness** — per language with GOOD/BAD code:
   - Python: `asyncio` event loop blocking, `aiohttp` vs `requests`, `aiofiles`
   - JS/TS: `Promise.all()` vs sequential awaits, `for await...of` streams
   - Go: goroutine patterns, `errgroup`, context cancellation
   - Java: CompletableFuture, virtual threads (JDK 21+)
   - Rust: Tokio task spawning, `tokio::spawn` vs `join!`
3. **Lock Contention Reduction** — lock-free data structures, read-write locks, lock striping, CAS operations
4. **Backpressure Patterns** — bounded queues, semaphores, rate limiting, token bucket
5. **Enterprise Integration Patterns for Throughput** (from luxury-lakehouse, generalized):
   - Splitter: break large work into parallelizable units
   - Scatter-Gather: fan-out work, collect results
   - Content-Based Router: route by type for specialized processing
   - Claim Check: pass reference instead of large payload
6. **Connection Pool Patterns** — database, HTTP, gRPC channel reuse
7. **Race Condition Detection** — Go race detector, ThreadSanitizer, Python GIL considerations
8. **Concurrency Testing** — stress testing concurrent paths, chaos approaches

Source: Research doc Categories 3, 5, luxury-lakehouse EIP patterns.

---

### Task 14: Template — frontend-performance.md

**Files:**
- Create: `plugins/mad-scientist-skills/skills/optimization-audit/templates/frontend-performance.md`

**Content specification (~450-550 lines):**

1. **Core Web Vitals** — LCP, INP, CLS with targets, measurement, and improvement strategies
2. **Bundle Optimization** — code splitting (route-based, component-based), tree-shaking, dynamic imports, per bundler config (webpack, Vite, esbuild, Rollup)
3. **Image Optimization** — format selection (WebP, AVIF), responsive images (`srcset`, `<picture>`), lazy loading, compression
4. **Rendering Performance** — React memo/useMemo/useCallback, Vue computed, virtual scrolling, layout thrashing prevention
5. **Font Loading** — `font-display: swap`, preloading, FOUT vs FOIT, variable fonts
6. **Third-Party Script Management** — async/defer, Partytown, performance budgets for third-party
7. **API Response Optimization** — pagination, sparse fieldsets, compression, GraphQL depth limiting, batch endpoints, ETags
8. **Performance Tools** — Lighthouse, WebPageTest, bundlephobia, webpack-bundle-analyzer, Chrome DevTools Performance tab, react-scan
9. **Performance Budgets** — defining and enforcing limits on bundle size, transfer size, LCP, INP

Source: Research doc Categories 10, 11.

---

### Task 15: Template — pipeline-efficiency.md

**Files:**
- Create: `plugins/mad-scientist-skills/skills/optimization-audit/templates/pipeline-efficiency.md`

**Content specification (~450-550 lines):**

1. **Batch vs Streaming Decision Matrix** — latency requirements, data volume, processing complexity
2. **Incremental Processing** — dbt incremental models with `is_incremental()`, Delta Lake MERGE, append-only patterns
3. **Storage Format Selection** — CSV vs JSON vs Parquet vs ORC vs Delta/Iceberg with trade-off matrix
4. **Partitioning Strategy** — time-based, hash-based, range-based, partition pruning, predicate pushdown
5. **Data Skew Detection and Mitigation** — salting, repartitioning, broadcast joins for small tables
6. **Spark/PySpark Optimization** — avoid `groupByKey` (use `reduceByKey`), avoid `collect()`, partition tuning, broadcast variables, persist/cache, AQE
7. **dbt Optimization** — incremental models, model materialization strategy, `run_results.json` parsing for execution time analysis (from luxury-lakehouse pattern)
8. **Vectorized Operations** — Pandas `apply` vs vectorized, NumPy broadcasting, avoiding row-by-row processing
9. **Dead Letter Patterns** — quarantine failed records, retry with backoff, DLQ monitoring
10. **Pipeline Cost Estimation** — per-run cost calculation methodology

Source: Research doc Category 14, luxury-lakehouse dbt/Delta patterns.

---

### Task 16: Template — cloud-cost-optimization.md

**Files:**
- Create: `plugins/mad-scientist-skills/skills/optimization-audit/templates/cloud-cost-optimization.md`

**Content specification (~450-550 lines):**

1. **Right-Sizing Methodology** — CPU/memory utilization analysis, recommendation thresholds (>80% under-provisioned, <20% over-provisioned)
2. **Auto-Scaling Patterns** — HPA (Kubernetes), AWS Auto Scaling, KEDA for event-driven, scaling metrics selection, cooldown periods, min/max configuration
3. **Spot/Preemptible Instances** — when to use, interruption handling, mixed instance strategies, Spot Fleet/Instance Group
4. **Reserved/Savings Plans** — commitment analysis, utilization tracking, break-even calculations
5. **Storage Tiering** — S3 tiers (Standard/IA/Glacier), EBS types (gp3 vs gp2 vs io2), lifecycle policies
6. **Scale-to-Zero** — serverless candidates, KEDA scale-to-zero, dev/staging environment scheduling (from luxury-lakehouse pattern)
7. **Cost Estimation Tools** — infracost (Terraform), Kubecost, AWS Cost Explorer, Azure Advisor, GCP Recommender
8. **Orphaned Resource Detection** — detached volumes, unused Elastic IPs, stale snapshots, empty load balancers
9. **Egress Optimization** — cross-region traffic, VPC endpoints, CDN offloading
10. **FinOps Practices** — tagging strategy, cost allocation, showback/chargeback, budget alerts

Source: Research doc Categories 15, 16, 17, luxury-lakehouse scale-to-zero pattern.

---

### Task 17: Template — profiling-benchmarking.md

**Files:**
- Create: `plugins/mad-scientist-skills/skills/optimization-audit/templates/profiling-benchmarking.md`

**Content specification (~400-500 lines):**

1. **Performance Testing Methodology** — load testing, stress testing, soak testing, spike testing, with when to use each
2. **Load Testing Tools** — with setup and example scripts:
   - k6: JavaScript-based, developer-friendly
   - locust: Python-based, distributed
   - wrk/wrk2: C-based, high-performance HTTP
   - hey: Go-based, simple HTTP load
   - artillery: YAML-based, scenarios
   - gatling: JVM-based, Scala DSL
3. **Micro-Benchmarking** — per language:
   - Python: pytest-benchmark, timeit
   - JS: Benchmark.js
   - Go: testing.B, benchstat
   - Java: JMH
   - Rust: criterion, cargo bench
   - .NET: BenchmarkDotNet
4. **Performance Regression Detection in CI** — Continuous Benchmark GitHub Action, storing baselines, alerting on degradation
5. **Profiling Methodology** — CPU profiling, memory profiling, I/O profiling, flame graph interpretation
6. **Performance Budgets** — defining limits (response time, bundle size, memory), enforcing in CI
7. **Realistic Test Data** — representative volumes, data distribution, edge cases
8. **Results Interpretation** — p50/p95/p99 percentiles, throughput curves, identifying bottleneck type (CPU/memory/I/O/network)

Source: Research doc Category 18.

---

### Task 18: Plugin Metadata and Documentation Updates

**Files:**
- Modify: `plugins/mad-scientist-skills/.claude-plugin/plugin.json` — update description to include optimization-audit, bump version to 1.2.0
- Modify: `.claude-plugin/marketplace.json` — update descriptions to include optimization-audit, bump version to 1.2.0
- Modify: `README.md` — add optimization-audit to skills table, add collapsible details section
- Modify: `architecture.dsl` — add `optimizationAuditSkill` container and relationship

**plugin.json changes:**
- Version: `1.1.0` → `1.2.0`
- Description: add "optimization auditing (beta: algorithm efficiency, database queries, caching, concurrency, pipelines, cloud cost, profiling)" or similar

**marketplace.json changes:**
- Both top-level and plugin-level descriptions updated
- Version: `1.1.0` → `1.2.0`

**README.md changes:**
- Skills table: add row for optimization-audit with description and invoke command
- Add collapsible `<details>` section matching the style of security-audit and observability-audit sections
- Phase coverage table (14 phases, Planning/Audit columns)
- Templates table (8 templates)
- Update project description line to include optimization auditing

**architecture.dsl changes:**
- Add container: `optimizationAuditSkill = container "optimization-audit Skill" "Single-tier optimization audit covering algorithm efficiency, database queries, caching, concurrency, pipelines, cloud cost, and profiling (beta)" "SKILL.md, 8 templates"`
- Add relationship: `claudeCode -> optimizationAuditSkill "Invokes" "/mad-scientist-skills:optimization-audit"`
- Update workspace and system descriptions to include optimization auditing

---

### Task 19: Architecture Diagram Regeneration

**Files:**
- Regenerate: `architecture.html`

**Process:**
1. Clean temp directory: `rm -rf /tmp/c4-render && mkdir -p /tmp/c4-render`
2. Export DSL: `java -jar plugins/mad-scientist-skills/skills/c4/structurizr.war export -workspace architecture.dsl -format plantuml/c4plantuml -output /tmp/c4-render`
3. Render SVGs: `java -jar plugins/mad-scientist-skills/skills/c4/plantuml.jar -tsvg /tmp/c4-render/*.puml`
4. Assemble HTML: `python plugins/mad-scientist-skills/skills/c4/c4_assemble.py /tmp/c4-render architecture.html`
5. Verify the HTML file contains the new optimization-audit container in the Container diagram
