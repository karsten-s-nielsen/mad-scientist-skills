# Optimization Audit Skill — Design

**Date:** 2026-03-08
**Branch:** `feature/optimization-audit-skill`
**Status:** Approved
**Maturity:** Beta

---

## Purpose

A comprehensive optimization audit skill that evaluates a system's resource efficiency, performance characteristics, and cost posture. Mirrors the `security-audit` and `observability-audit` skill patterns: two modes (Planning/Audit), phased execution with severity classification, evidence-based findings, and a final report.

Unlike the other audit skills, this one is **single tier** — optimization tools (profilers, EXPLAIN, load testers, linters) are overwhelmingly free/open-source, making a Standard/Enterprise split unnecessary.

**Security audit asks:** "Can attackers exploit this?"
**Observability audit asks:** "Can operators see what's happening?"
**Optimization audit asks:** "Is this system using resources efficiently?"

---

## Modes

| Signal | Mode | Rationale |
|--------|------|-----------|
| User says "optimize", "performance review", "resource efficiency" | **Audit** | Code and infrastructure analysis |
| User says "design for performance", "plan scaling", "capacity planning" | **Planning** | Architecture-level performance strategy |
| No source code exists yet (only docs, diagrams, RFCs) | **Planning** | Nothing to profile — design the strategy |
| Source code exists with some/no optimization | **Audit** | Concrete artifacts to analyze |
| Both code and a request to "plan performance" | **Both** | Run all phases |

When in doubt, ask the user. If both modes apply, run all 14 phases.

---

## Single Tier Rationale

The two-tier (Standard/Enterprise) pattern used by security-audit and observability-audit makes sense when there is a clear divide between free and paid tooling ecosystems. For optimization:

- **Profilers** are free: py-spy, pprof, async-profiler, Chrome DevTools, perf
- **Database analysis** is free: EXPLAIN ANALYZE, pg_stat_statements, django-debug-toolbar
- **Load testing** is free: k6, locust, wrk, hey
- **Container analysis** is free: dive, hadolint, docker history
- **Cost analysis tools** vary, but the methodology is the same regardless of tool

Enterprise optimization platforms (Datadog APM, New Relic, Dynatrace) are already covered by the observability-audit skill. A separate tier here would duplicate that coverage.

---

## Severity Classification

| Severity | Criteria | Action | SLA |
|----------|----------|--------|-----|
| **Critical** | Causes outages, OOM crashes, connection exhaustion, quadratic algorithms on user-facing paths, unbounded memory growth | Fix immediately | Block release |
| **High** | Measurable performance degradation >2x expected; N+1 queries, missing indexes on production queries, no connection pooling, missing compression | Fix before next release | 1 sprint |
| **Medium** | Suboptimal but functional; oversized resources, missing caching, debug logging in production, suboptimal serialization | Schedule fix | 2 sprints |
| **Low** | Best practice deviation; naming conventions, minor allocation patterns, potential micro-optimizations | Track in backlog | Best effort |

---

## Phase Structure (14 phases, 0-13)

| Phase | Name | Mode | Purpose |
|-------|------|------|---------|
| 0 | Anti-Pattern Scan | Audit | Fast grep for known performance anti-patterns across all categories |
| 1 | Discovery | Both | Map system, tech stack, deployment model, workload profile |
| 2 | Algorithm & Data Structure Efficiency | Audit | Big-O analysis, data structure selection, hot path review |
| 3 | Memory Management | Audit | Leak detection, unbounded caches, allocation patterns, GC pressure |
| 4 | Concurrency & Parallelism | Audit | Thread/goroutine pools, async correctness, lock contention, backpressure |
| 5 | Database & Query Optimization | Both | N+1, indexing, connection pooling, EXPLAIN analysis, ORM patterns |
| 6 | Caching Strategy | Both | Cache layers, invalidation, hit ratios, memoization, HTTP caching |
| 7 | Serialization & Network | Audit | Data format, compression, protocol optimization, payload sizing |
| 8 | Frontend & API Optimization | Audit | Bundle size, Core Web Vitals, API response shaping, pagination |
| 9 | Data Pipeline Efficiency | Both | Batch/stream, incremental processing, storage formats, partitioning |
| 10 | Container & Startup Optimization | Audit | Image size, build caching, cold start, multi-stage builds |
| 11 | Cloud Cost & Right-Sizing | Both | Resource utilization, auto-scaling, storage tiering, spot/reserved |
| 12 | Profiling & Benchmarking Posture | Both | Performance test suite, regression detection, performance budgets |
| 13 | Findings Report | Both | Final report with severity, impact quantification, ROI estimates |

**Conditional phases:**
- Phase 8 (Frontend): Only if frontend code exists (HTML, CSS, JS/TS, React, Vue, Angular, Svelte)
- Phase 9 (Pipeline): Only if ETL/ELT, dbt, Spark, Airflow, Dagster, Prefect, or similar pipeline tools detected
- Phase 10 (Container): Only if Dockerfiles, docker-compose, or Kubernetes manifests exist
- Phase 11 (Cloud Cost): Only if IaC (Terraform, CloudFormation, Pulumi) or cloud deployment configuration exists

---

## Templates (8 reference files)

| Template | Key Content |
|----------|-------------|
| `algorithm-complexity.md` | Big-O analysis patterns, data structure selection guide, per-language profiling tools, hot path identification |
| `database-optimization.md` | N+1 detection per ORM, indexing strategy, EXPLAIN analysis, connection pooling, batch operations, query patterns |
| `caching-strategies.md` | 5-layer cache architecture, invalidation patterns, HTTP caching (Cache-Control, ETag), CDN, memoization, stampede protection |
| `concurrency-patterns.md` | Thread pool sizing, async/await correctness, lock contention, backpressure, EIP patterns (Scatter-Gather, Splitter) |
| `frontend-performance.md` | Core Web Vitals, bundle optimization, code splitting, image optimization, rendering patterns, virtual scrolling |
| `pipeline-efficiency.md` | Batch/stream trade-offs, incremental processing, storage formats (Parquet/Delta), partitioning, skew, dbt optimization |
| `cloud-cost-optimization.md` | Right-sizing methodology, auto-scaling, spot/reserved instances, storage tiering, scale-to-zero, cost estimation tools |
| `profiling-benchmarking.md` | Performance testing methodology, regression detection, performance budgets, load testing, per-language profiling tools |

---

## Key Design Decisions

1. **Single tier** — optimization tools are overwhelmingly free. Enterprise APM is covered by observability-audit. No duplication.
2. **Measurement-first** — optimization is relative, not binary. Every finding quantifies impact ("N+1 adds ~200ms/page") not just "found issue."
3. **ROI-oriented reporting** — findings estimate effort vs impact: quick wins (5 min fix, 10x gain) vs structural changes (multi-sprint, 2x gain).
4. **Fix obvious wins, benchmark structural changes** — add missing index? Yes. Rewrite concurrency model? Recommend benchmark first.
5. **Phase 0 is the workhorse** — most optimization audit value comes from grep-able anti-patterns. Comprehensive per-language pattern tables.
6. **Conditional phases** — skip irrelevant phases (frontend, pipeline, container, cloud) to keep signal-to-noise high.
7. **Mirrors audit skill suite structure** — two modes, phased execution, severity classification, fix-as-you-go, evidence-based claims. Consistency across security/observability/optimization.
8. **Generalizable patterns from luxury-lakehouse** — vectorization, N+1 detection, 5-layer caching, EIP patterns, scale-to-zero, incremental processing, storage format selection, dead letter patterns — all generalized for broad applicability.

---

## File Structure

```
plugins/mad-scientist-skills/skills/optimization-audit/
├── SKILL.md
└── templates/
    ├── algorithm-complexity.md
    ├── database-optimization.md
    ├── caching-strategies.md
    ├── concurrency-patterns.md
    ├── frontend-performance.md
    ├── pipeline-efficiency.md
    ├── cloud-cost-optimization.md
    └── profiling-benchmarking.md
```
