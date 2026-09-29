# Observability Audit Skill — Design

**Date:** 2026-03-08
**Branch:** `feature/observability-audit-skill`
**Status:** Approved
**Maturity:** Beta

---

## Purpose

A comprehensive observability audit skill that evaluates a system's ability to detect, diagnose, and respond to production issues. Mirrors the `security-audit` skill pattern: two modes (Planning/Audit), two tiers (Standard/Enterprise), phased execution with severity classification, evidence-based findings, and a final report.

**Security audit asks:** "Can attackers exploit this?"
**Observability audit asks:** "Can operators see what's happening?"

---

## Modes

| Signal | Mode | Rationale |
|--------|------|-----------|
| User says "design observability", "plan monitoring", "telemetry strategy" | **Planning** | Architecture-level analysis before code |
| User says "audit observability", "check monitoring", "find blind spots" | **Audit** | Code and infrastructure scanning |
| No telemetry code exists yet (only docs, diagrams, RFCs) | **Planning** | Nothing to scan — design the strategy |
| Source code exists with some/no instrumentation | **Audit** | Concrete artifacts to analyze |
| Both code and a request to "design observability" | **Both** | Run all phases |

When in doubt, ask the user. If both modes apply, run all 13 phases.

---

## Tiers

- **Standard** — free/open-source tools, code-level patterns, always actionable for any developer.
- **Enterprise** — paid services (APM, SIEM, managed observability platforms), compliance tooling. Serves as a professional checklist documenting what enterprise teams should implement.

---

## Severity Classification

| Severity | Criteria | Action | SLA |
|----------|----------|--------|-----|
| **Critical** | Complete blind spot on critical production path (no error monitoring, no health checks, no alerting) | Fix immediately | Block release |
| **High** | Significant gap that delays incident response > 30 min (no distributed tracing, no structured logging, print-based debugging) | Fix before next release | 1 sprint |
| **Medium** | Partial visibility, defense-in-depth gap (missing SLOs, no correlation IDs, default metrics only) | Schedule fix | 2 sprints |
| **Low** | Best practice deviation, optimization opportunity (missing dashboards, suboptimal sampling, no cardinality controls) | Track in backlog | Best effort |

---

## Phase Structure (13 phases, 0-12)

| Phase | Name | Mode | Purpose |
|-------|------|------|---------|
| 0 | Anti-Pattern Scan | Audit | Grep for `print()` debugging, bare `except`, missing error context, no-op loggers |
| 1 | Discovery | Both | Map system, tech stack, deployment model, telemetry surface |
| 2 | Instrumentation Foundation | Both | OTel SDK setup, exporters, collector config, auto-instrumentation coverage |
| 3 | Structured Logging | Audit | Log format (JSON), levels, correlation IDs, sensitive data exclusion |
| 4 | Metrics & SLIs/SLOs | Both | RED/USE methodology, SLI definitions, SLO targets, custom metrics |
| 5 | Distributed Tracing | Audit | Context propagation, span design, sampling strategy, trace completeness |
| 6 | Pipeline & Data Observability | Both | ETL/ELT health, data quality monitoring, freshness, dbt artifact parsing |
| 7 | ML/Model Observability | Both | Drift detection (PSI, CUSUM, KS test), validation, performance tracking |
| 8 | Alerting & Incident Detection | Both | Alert quality, noise ratio, escalation paths, runbooks |
| 9 | Dashboard & Visualization | Audit | Operational views, information hierarchy, golden signals visibility |
| 10 | Health Checks & Readiness | Audit | Liveness/readiness probes, dependency health, graceful degradation |
| 11 | Cost & Cardinality Management | Both | Telemetry volume, high-cardinality prevention, tier-appropriate backends |
| 12 | Findings Report | Both | Final report with tier coverage matrix |

**Notes:**
- Phase 7 (ML/Model) is optional — only runs if ML models or data pipelines with analytical outputs are detected.
- Phase 6 (Pipeline) covers both traditional ETL and modern data platforms (dbt, Airflow, Dagster, Prefect, Spark, cron scripts).

---

## Templates (7 reference files)

| Template | Key Content |
|----------|-------------|
| `otel-instrumentation.md` | OTel SDK setup per language/framework, auto-instrumentation packages, custom attribute namespaces, exporter config |
| `structured-logging.md` | JSON logging patterns, correlation IDs, log level policy, framework-specific setup, PII scrubbing |
| `metrics-sli-slo.md` | RED (Request/Error/Duration), USE (Utilization/Saturation/Errors), SLI/SLO design, metric types (counter/gauge/histogram) |
| `distributed-tracing.md` | Context propagation (W3C TraceContext, B3), span naming, attribute conventions, sampling strategies |
| `pipeline-observability.md` | ETL/ELT monitoring, dbt `run_results.json` parsing, data freshness, quality gates, dead letter patterns |
| `ml-model-observability.md` | PSI, CUSUM, KS test, Wasserstein distance, hard constraints, reference baselines, NannyML CBPE, Evidently AI |
| `alerting-runbooks.md` | Alert design principles, noise reduction, symptom-based alerting, runbook templates, escalation paths |

---

## Standard vs Enterprise Tier Matrix

| Phase | Standard (free, always actionable) | Enterprise (paid, aspirational checklist) |
|-------|-----------------------------------|--------------------------------------------|
| Instrumentation | OTel SDK + console/file/S3 exporter | Datadog APM, New Relic, Dynatrace |
| Logging | Python `logging` + JSON formatter, ELK self-hosted | Splunk, Datadog Logs, Grafana Loki Cloud |
| Metrics | Prometheus + Grafana (self-hosted), OTel Collector | Datadog Metrics, Grafana Cloud Mimir, CloudWatch |
| Tracing | Jaeger/Zipkin (self-hosted), OTel Collector to S3 | Grafana Tempo Cloud, Datadog APM, Honeycomb |
| Pipeline | dbt artifact parsing, custom OTel counters | Monte Carlo, Atlan, Elementary Cloud, dbt Cloud |
| ML/Model | Evidently AI (OSS), WhyLogs, scipy-based drift | NannyML Cloud, Arize AI, Fiddler, WhyLabs Cloud |
| Alerting | Alertmanager, Grafana alerts | PagerDuty, OpsGenie, Datadog Monitors, xMatters |
| Dashboards | Grafana (self-hosted), DuckDB + notebooks | Grafana Cloud, Datadog Dashboards, Looker |

---

## Generalizable Patterns (extracted from luxury-lakehouse research)

Domain-agnostic patterns baked into the relevant phases/templates:

1. **Dual-export architecture** — `OTEL_MODE` env var pattern for cost-tier switching (Phase 2, 11)
2. **Layer-by-layer instrumentation** — each system layer (ingestion, transformation, serving) gets dedicated telemetry (Phase 2)
3. **Custom attribute namespaces** — when no OTel semantic conventions exist, define structured `<domain>.*` attributes (Phase 5)
4. **Statistical process control for drift** — PSI, CUSUM, KS test, Wasserstein, hard constraints (Phase 7)
5. **dbt artifact parsing** — zero-dependency post-run parsing of `run_results.json` (Phase 6)
6. **Cost-conscious observability** — S3 + DuckDB personal tier, enterprise backends for teams (Phase 11)
7. **Reference baselines** — stored as seeds/config, used for drift comparison (Phase 7)

---

## File Structure

```
plugins/mad-scientist-skills/skills/observability-audit/
├── SKILL.md
└── templates/
    ├── otel-instrumentation.md
    ├── structured-logging.md
    ├── metrics-sli-slo.md
    ├── distributed-tracing.md
    ├── pipeline-observability.md
    ├── ml-model-observability.md
    └── alerting-runbooks.md
```

---

## Key Design Decisions

1. **Mirrors security-audit structure** — same two-mode, two-tier, phased pattern for consistency across the skill suite.
2. **Phase 7 (ML/Model) is conditional** — only runs when ML models or analytical outputs are detected. Not all systems have ML.
3. **Fix-as-you-go** — Critical/High findings get remediated during the audit, not just reported.
4. **Evidence-based claims** — every finding requires file path, line number, or specific evidence. No "probably needs monitoring."
5. **Framework-agnostic with framework-specific patterns** — SKILL.md covers the methodology; templates contain language/framework-specific grep patterns and configuration snippets.
6. **OTel-first but not OTel-only** — OpenTelemetry is the recommended instrumentation standard, but the audit accommodates systems using proprietary SDKs (Datadog Agent, New Relic Agent, etc.).
