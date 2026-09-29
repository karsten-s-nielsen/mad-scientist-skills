# Observability Audit Skill Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Create a two-mode (Planning/Audit), two-tier (Standard/Enterprise) observability audit skill that evaluates a system's telemetry, logging, metrics, tracing, alerting, and monitoring maturity.

**Architecture:** Follows the `security-audit` skill pattern exactly — a single `SKILL.md` containing all phase definitions with severity classification, plus 7 template reference files loaded on-demand per phase. The skill is labeled **beta**.

**Tech Stack:** Markdown skill files, grep patterns for anti-pattern detection, framework-specific configuration references for OTel, logging, metrics, tracing, and alerting.

**Design doc:** `docs/specs/2026-03-08-observability-audit-design.md`

**Reference implementation:** `plugins/mad-scientist-skills/skills/security-audit/` (same directory structure, same tier/mode/phase conventions)

---

## Task 1: Create SKILL.md — Frontmatter, Overview, Modes, Severity, Phase 0-1

**Files:**
- Create: `plugins/mad-scientist-skills/skills/observability-audit/SKILL.md`

**Step 1: Create directory and SKILL.md**

Create the file with the following structure. Model after `security-audit/SKILL.md` lines 1-138.

**Frontmatter** (YAML):
- `name: observability-audit`
- `description:` Comprehensive observability audit with two modes and two tiers (beta). Planning mode designs telemetry strategy, SLIs/SLOs, and instrumentation architecture. Audit mode scans code and infrastructure for observability gaps including logging, metrics, tracing, alerting, pipeline monitoring, and ML model drift detection. Each phase has Standard (free/open-source tools, always actionable) and Enterprise (paid observability platforms, aspirational checklist) tiers. Use when asked to "observability audit", "check monitoring", "find blind spots", "audit telemetry", "design observability", or "review instrumentation".

**Section: Overview** — describe the skill as a comprehensive observability audit with two modes and two tiers. Label as **beta**.

**Section: When to use this skill** — trigger phrases and contexts (before designing a new system, on existing code, before production deployment, after adding new services/pipelines).

**Section: Mode detection** — table with signals mapping to Planning/Audit/Both. Match the format at `security-audit/SKILL.md:28-38`.

**Section: Severity classification** — 4-level table (Critical/High/Medium/Low) with observability-specific criteria. Match format at `security-audit/SKILL.md:40-49`.

**Section: Phase 0 — Anti-Pattern Scan (Audit mode)**

Fast grep-based scan for observability anti-patterns. Analogous to security-audit Phase 0 (dangerous code patterns).

Standard tier grep patterns table:

| Pattern | Language | Risk |
|---------|----------|------|
| `print(` used for debugging/monitoring output | Python | Unstructured, lost on restart, no levels/context |
| `console.log(` used for operational output | JS/TS | Same as above |
| `System.out.println(` | Java | Same as above |
| `fmt.Println(` / `log.Println(` (stdlib) | Go | No structured fields, no levels |
| `except:` or `except Exception:` without logging | Python | Swallowed errors — silent failures |
| `catch (e) {}` or `catch (e) { }` (empty catch) | JS/TS | Same |
| `catch (Exception e) {}` | Java | Same |
| `# TODO.*log\|# FIXME.*monitor\|# HACK.*metric` | Any | Acknowledged observability debt |
| `logging.disable\|logging.NOTSET` | Python | Logging intentionally disabled |
| `time.sleep(` in retry loops without backoff/metrics | Python | Unmonitored retry, no failure visibility |
| `@app.route` / `@router` without middleware/decorator for request metrics | Python (Flask/FastAPI) | Unmonitored endpoints |
| `app.use(` or `router.` without morgan/pino/winston middleware | Node.js (Express) | Unmonitored HTTP requests |
| `pass` in exception handler | Python | Silent error swallowing |
| `logger = logging.getLogger()` (root logger) | Python | Undifferentiated log source |
| hardcoded metric names with high-cardinality values (user IDs, request IDs in metric names) | Any | Cardinality explosion |

Enterprise tier: list SAST/linting tools that detect observability anti-patterns (SonarQube custom rules, Semgrep observability rulesets, ESLint no-console rule, pylint logging-not-lazy).

**Section: Phase 1 — Discovery (Both modes)**

Match `security-audit/SKILL.md:112-138` structure but for observability surface:

- Read `CLAUDE.md`, `README.md`, architecture docs
- Identify tech stack, frameworks, language versions
- Map the **observability surface**:
  - Services and entry points (APIs, workers, scheduled jobs, consumers)
  - Data stores and caches
  - External integrations (third-party APIs, SaaS services)
  - Existing telemetry: logging framework, metrics library, tracing SDK
  - Existing backends: where do logs/metrics/traces go today?
  - Deployment model: containers, serverless, VMs, managed services
  - CI/CD pipeline: build, test, deploy stages
  - Data pipelines: ETL/ELT, dbt, Airflow, Spark, etc.
  - ML models: training, inference, validation (if any)
- Identify critical paths: which request flows or data flows absolutely must be observable?
- Note the team's operational maturity: is there an on-call rotation? Incident response process?

**Output:** Observability surface summary listing all services, existing telemetry, backends, and critical paths.

**Step 2: Verify file exists and frontmatter is valid**

Run: `head -5 plugins/mad-scientist-skills/skills/observability-audit/SKILL.md`
Expected: YAML frontmatter with name and description.

---

## Task 2: SKILL.md — Phases 2-5

**Files:**
- Modify: `plugins/mad-scientist-skills/skills/observability-audit/SKILL.md`

Append Phases 2-5 to the SKILL.md file.

**Section: Phase 2 — Instrumentation Foundation (Both modes)**

Load `templates/otel-instrumentation.md` for full reference.

**Planning mode:** Evaluate the planned instrumentation approach:
- Which instrumentation standard? (OpenTelemetry, vendor SDK, custom)
- Signal types needed? (logs, metrics, traces — the three pillars)
- Export strategy? (direct SDK export, Collector, agent-based)
- Backend selection? (self-hosted vs managed, cost tier)
- Auto-instrumentation coverage? (HTTP, DB, messaging)

**Audit mode:** Check existing instrumentation:

Standard tier checks table:

| Check | What to look for | Severity |
|-------|-----------------|----------|
| OTel SDK installed | `opentelemetry-sdk`, `@opentelemetry/sdk-node`, `go.opentelemetry.io/otel` in dependency files | High |
| SDK properly initialized | `TracerProvider`, `MeterProvider`, `LoggerProvider` configured at startup | High |
| Exporter configured | At least one exporter (OTLP, console, file, Prometheus) | Critical |
| Resource attributes set | `service.name`, `service.version`, `deployment.environment` | High |
| Auto-instrumentation enabled | HTTP, database, and messaging libraries instrumented | Medium |
| Context propagation configured | W3C TraceContext or B3 propagator set | High |
| Shutdown hook registered | `TracerProvider.shutdown()` called on process exit (prevents data loss) | Medium |
| Collector deployed (if used) | OTel Collector running with appropriate receivers, processors, exporters | Medium |

Enterprise tier table: Datadog Agent, New Relic APM, Dynatrace OneAgent, AWS X-Ray, Azure Monitor Application Insights, Google Cloud Trace.

**Section: Phase 3 — Structured Logging (Audit mode)**

Load `templates/structured-logging.md` for full reference.

Standard tier checks table:

| Check | What to look for | Severity |
|-------|-----------------|----------|
| Structured format (JSON) | Logs emitted as JSON, not free-text | High |
| Log levels used correctly | DEBUG/INFO/WARNING/ERROR/CRITICAL with clear policy | Medium |
| Correlation IDs present | `trace_id`, `span_id`, or custom `request_id` in log entries | High |
| Contextual fields | Service name, environment, user ID (if applicable) in every log entry | Medium |
| No PII in logs | Passwords, tokens, SSNs, emails not logged in plain text | High |
| No secrets in logs | API keys, connection strings not present in log output | Critical |
| Centralized log aggregation | Logs shipped to a central location (not just local files/stdout) | High |
| Log rotation configured | File-based logs have rotation and retention policies | Medium |
| Error logs include stack traces | Exceptions logged with full traceback | Medium |
| Request/response logging | HTTP requests logged with method, path, status, duration (not body) | Medium |

Grep patterns for common logging issues (per-framework):

| Language | Pattern | Issue |
|----------|---------|-------|
| Python | `logging.basicConfig()` without `format=` JSON | Unstructured log output |
| Python | `logger.exception(` without context fields | Missing correlation |
| Python | `logging.warning(f".*{password\|secret\|token\|key}` | PII/secret in logs |
| Node.js | `console.log\|console.error\|console.warn` (in production code) | No structured logging |
| Node.js | `morgan('dev')` (in production) | Verbose unstructured access logs |
| Java | `System.out.println\|System.err.println` | No logging framework |
| Go | `log.Printf\|log.Println` (stdlib) without structured logger | No structured fields |

Enterprise tier table: Splunk, Datadog Logs, Grafana Loki Cloud, AWS CloudWatch Logs, Azure Monitor Logs, Elastic Cloud.

**Section: Phase 4 — Metrics & SLIs/SLOs (Both modes)**

Load `templates/metrics-sli-slo.md` for full reference.

**Planning mode:** Define SLIs, SLOs, and key metrics:
- What are the service's SLIs? (availability, latency, throughput, error rate)
- What SLO targets are appropriate? (99.9%, 99.95%, etc.)
- Which methodology? RED (Request/Error/Duration) for request-driven services, USE (Utilization/Saturation/Errors) for resources

**Audit mode:**

Standard tier checks table:

| Check | What to look for | Severity |
|-------|-----------------|----------|
| RED metrics for request-driven services | Request rate, Error rate, Duration (histogram) per endpoint | High |
| USE metrics for resources | Utilization, Saturation, Errors for CPU, memory, disk, connections | Medium |
| Custom business metrics | Domain-specific counters/gauges (orders processed, items indexed, etc.) | Medium |
| Metric types correct | Counters for totals, gauges for current values, histograms for distributions | Medium |
| SLIs defined | At least availability and latency SLIs for critical services | High |
| SLOs documented | Target percentages with measurement windows | High |
| Error budgets tracked | Remaining error budget visible and alerting when low | Medium |
| Metric naming conventions | Consistent naming (e.g., `http_request_duration_seconds`, not `latency`) | Low |
| No high-cardinality labels | Metric labels don't include user IDs, request IDs, or unbounded values | High |
| Metric exposition endpoint | `/metrics` (Prometheus) or OTLP export configured | High |

Enterprise tier table: Datadog Metrics, Grafana Cloud Mimir, AWS CloudWatch Metrics, Azure Monitor Metrics, New Relic Metrics, SLO platforms (Nobl9, Datadog SLOs).

**Section: Phase 5 — Distributed Tracing (Audit mode)**

Load `templates/distributed-tracing.md` for full reference.

Standard tier checks table:

| Check | What to look for | Severity |
|-------|-----------------|----------|
| Trace context propagation | W3C TraceContext (`traceparent` header) or B3 headers propagated across service boundaries | Critical |
| Spans on critical paths | Every service-to-service call, database query, and external API call produces a span | High |
| Span naming conventions | Descriptive names: `HTTP GET /api/users`, `DB SELECT users`, not `span1` | Medium |
| Span attributes | Relevant context: `http.method`, `http.status_code`, `db.statement` (sanitized), `rpc.method` | Medium |
| Error recording on spans | Exceptions set span status to ERROR with error message and stack trace | High |
| Sampling strategy | Head-based or tail-based sampling configured (not 100% in production) | Medium |
| Trace-to-log correlation | `trace_id` and `span_id` present in log entries | High |
| Cross-service trace completeness | End-to-end traces visible across all services in a request flow | High |
| Span events for key operations | Significant events within a span recorded (e.g., cache hit/miss, retry) | Low |
| Baggage propagation (if needed) | W3C Baggage used for cross-cutting concerns (tenant ID, feature flags) | Low |

Grep patterns for tracing issues:

| Language | Pattern | Issue |
|----------|---------|-------|
| Python | `requests.get\|requests.post` without OTel `requests` instrumentation | Untraced HTTP calls |
| Python | `psycopg2.connect\|sqlalchemy.create_engine` without OTel DB instrumentation | Untraced DB queries |
| Node.js | `fetch(\|axios.\|http.request(` without OTel HTTP instrumentation | Untraced HTTP calls |
| Any | `grpc.\|kafka.\|rabbitmq.\|redis.` without corresponding OTel instrumentation | Untraced messaging/cache |

Enterprise tier table: Grafana Tempo Cloud, Datadog APM, Honeycomb, AWS X-Ray, Azure Monitor (distributed tracing), Jaeger Cloud (Elastic).

---

## Task 3: SKILL.md — Phases 6-8

**Files:**
- Modify: `plugins/mad-scientist-skills/skills/observability-audit/SKILL.md`

Append Phases 6-8.

**Section: Phase 6 — Pipeline & Data Observability (Both modes)**

Load `templates/pipeline-observability.md` for full reference.

**Planning mode:** Design pipeline monitoring strategy:
- Which pipeline orchestrator? (Airflow, Dagster, Prefect, dbt, cron, Databricks Workflows)
- What data quality checks exist? (schema validation, row counts, freshness)
- How are pipeline failures surfaced? (email, Slack, PagerDuty)
- Is there data lineage tracking?

**Audit mode:**

Standard tier checks table:

| Check | What to look for | Severity |
|-------|-----------------|----------|
| Pipeline execution metrics | Duration, success/failure counts, row counts per stage/task | High |
| Data freshness monitoring | Source freshness checks (dbt `sources.yml`, custom staleness queries) | High |
| Data quality gates | Schema validation, null checks, uniqueness, referential integrity (dbt tests, Great Expectations) | High |
| Dead letter handling | Failed records quarantined, not silently dropped | High |
| Idempotency verification | Pipeline re-runs produce identical results (no duplicates) | Medium |
| dbt test results tracked | `run_results.json` parsed and emitted as metrics post-build | Medium |
| dbt model execution time | Per-model duration tracked for regression detection | Medium |
| Source system availability | Health checks or connectivity tests for upstream data sources | Medium |
| Data volume anomaly detection | Significant deviations in row counts flagged (e.g., 0 rows when expecting thousands) | High |
| Pipeline retry visibility | Retries logged with attempt count, backoff, and final outcome | Medium |

Grep patterns:

| Framework | Pattern | Issue |
|-----------|---------|-------|
| dbt | No `tests:` in `schema.yml` / `_schema.yml` | Untested models |
| dbt | No `freshness:` in `sources.yml` | No staleness detection |
| Airflow | `on_failure_callback` not set | Silent task failures |
| Airflow | `email_on_failure = False` without alternative alerting | No failure notification |
| Any | `except:` / `catch` with `continue` in data loop | Silently skipped records |
| Any | No row count logging after write operations | Invisible data volume |

Enterprise tier table: Monte Carlo, Atlan, Elementary Cloud, dbt Cloud, Datafold, Soda Cloud, Great Expectations Cloud.

**dbt artifact parsing pattern** (zero-dependency, generalizable):
After `dbt run` or `dbt test`, parse `target/run_results.json`:
- Per-model execution time → OTel counter or gauge
- Test pass/fail counts → OTel counter
- Failure details → OTel event or log entry
- Source freshness → OTel gauge

**Section: Phase 7 — ML/Model Observability (Both modes) — CONDITIONAL**

Run this phase only if ML models, analytical models, or data pipelines with statistical/predictive outputs are detected. Skip otherwise.

Load `templates/ml-model-observability.md` for full reference.

**Planning mode:** Design model monitoring strategy:
- Which models are in production? (classification, regression, recommendation, analytics)
- What is the ground truth availability? (immediate, delayed, never)
- What drift detection methods are appropriate?
- How are model versions tracked?

**Audit mode:**

Standard tier checks table:

| Check | What to look for | Severity |
|-------|-----------------|----------|
| Model version tracking | Model registry (MLflow, Weights & Biases, custom) with version aliases | High |
| Input distribution monitoring | Feature distributions tracked and compared to training baseline | High |
| Output distribution monitoring | Prediction distributions tracked for drift | High |
| Drift detection method | At least one statistical method configured (PSI, KS test, Wasserstein, CUSUM) | High |
| Performance metrics logged | Accuracy, precision, recall, F1, RMSE, or domain-specific metrics tracked over time | High |
| Hard constraint validation | Domain invariants checked (e.g., probabilities sum to 1, values within physical bounds) | Medium |
| Reference baselines stored | Training-time distributions saved for comparison | Medium |
| Model prediction latency | Inference time tracked as histogram metric | Medium |
| A/B or shadow deployment | Champion/challenger comparison before full rollout | Low |
| Data slice analysis | Performance tracked per important segment (not just aggregate) | Low |

**Statistical drift detection methods** (generalizable from research):

| Method | Use Case | Complexity | Implementation |
|--------|----------|------------|----------------|
| **PSI** (Population Stability Index) | Compare two distributions binned into buckets | Low | `scipy` + `numpy`, ~20 lines |
| **CUSUM** (Cumulative Sum) | Detect sustained small shifts over time | Low | Pure Python, ~10 lines, O(n) |
| **KS Test** (Kolmogorov-Smirnov) | Two-sample distribution comparison | Low | `scipy.stats.ks_2samp()` |
| **Wasserstein Distance** | Quantify magnitude of distribution shift | Low | `scipy.stats.wasserstein_distance()` |
| **Hard Constraints** | Domain invariants (sums, bounds, ranges) | Trivial | Simple assertions |
| **CBPE** (Confidence-Based Performance Estimation) | Estimate performance without ground truth | Medium | NannyML library |

Enterprise tier table: Arize AI, Fiddler, WhyLabs Cloud, NannyML Cloud, Evidently Cloud, Seldon Deploy, AWS SageMaker Model Monitor, Azure ML Model Monitoring.

**Section: Phase 8 — Alerting & Incident Detection (Both modes)**

Load `templates/alerting-runbooks.md` for full reference.

**Planning mode:** Design alerting strategy:
- Which signals should trigger alerts? (error rate, latency, saturation, SLO burn rate)
- Who receives alerts? (on-call rotation, team channel, specific individuals)
- What is the escalation path?
- Are there runbooks for common incidents?

**Audit mode:**

Standard tier checks table:

| Check | What to look for | Severity |
|-------|-----------------|----------|
| Alerts on golden signals | Error rate, latency, traffic, saturation alerts configured | Critical |
| SLO-based alerting | Multi-window burn rate alerts (not just threshold) | High |
| Alert routing configured | Alerts reach a human (Slack, email, PagerDuty) with clear ownership | Critical |
| Escalation path defined | Unacknowledged alerts escalate after N minutes | High |
| Runbooks exist for critical alerts | Each high-severity alert has a documented response procedure | High |
| Alert noise managed | Signal-to-noise ratio tracked; noisy alerts tuned or suppressed | Medium |
| Symptom-based (not cause-based) | Alerts on user-visible symptoms, not internal causes | Medium |
| Alert inhibition/grouping | Related alerts grouped to avoid storm fatigue | Medium |
| Heartbeat/dead-man's-switch | Alert when expected signals stop arriving | High |
| Alert testing | Alerts tested periodically (fire drill, chaos engineering) | Low |

Anti-patterns to flag:
- Alerts with > 50% false positive rate
- Alerts that nobody has responded to in 30+ days
- Email-only alerting for critical services
- Threshold alerts without hysteresis (flapping)
- Alerts on cause instead of symptom (e.g., "CPU high" instead of "latency exceeded SLO")

Enterprise tier table: PagerDuty, OpsGenie, xMatters, Datadog Monitors, Grafana Alerting (Cloud), AWS CloudWatch Alarms + SNS, incident.io, FireHydrant.

---

## Task 4: SKILL.md — Phases 9-12 and Important Rules

**Files:**
- Modify: `plugins/mad-scientist-skills/skills/observability-audit/SKILL.md`

Append Phases 9-12 and the Important Rules section.

**Section: Phase 9 — Dashboard & Visualization (Audit mode)**

Standard tier checks table:

| Check | What to look for | Severity |
|-------|-----------------|----------|
| Golden signals dashboard | Error rate, latency, traffic, saturation visible at a glance | High |
| Service overview dashboard | All services with health status on a single pane | Medium |
| On-call dashboard | Current issues, recent alerts, SLO status for the on-call engineer | Medium |
| Request flow visualization | End-to-end request path visible (trace waterfall or service map) | Medium |
| Time range controls | Dashboards support flexible time ranges for investigation | Low |
| Dashboard-to-trace drill-down | Click from dashboard metric to related traces | Medium |
| Dashboard-to-log drill-down | Click from dashboard metric to related logs | Medium |
| No vanity dashboards | Every dashboard has a clear audience and purpose | Low |
| Dashboard as code | Dashboard definitions version-controlled (Grafana JSON, Terraform) | Medium |
| Data freshness indicator | Dashboards show when data was last updated | Low |

Enterprise tier table: Grafana Cloud, Datadog Dashboards, New Relic Dashboards, Looker, AWS CloudWatch Dashboards, Azure Workbooks.

**Section: Phase 10 — Health Checks & Readiness (Audit mode)**

Standard tier checks table:

| Check | What to look for | Severity |
|-------|-----------------|----------|
| Liveness probe | `/health` or `/healthz` endpoint returning 200 when process is alive | Critical |
| Readiness probe | `/ready` endpoint returning 200 only when dependencies are available | High |
| Dependency health checks | Database, cache, queue, external API connectivity verified in readiness probe | High |
| Startup probe (containers) | Separate probe for slow-starting applications | Medium |
| Health check includes version | Response includes service version and build info | Low |
| Graceful shutdown | Process handles SIGTERM, drains in-flight requests, then exits | High |
| Circuit breaker on dependencies | Downstream failures don't cascade (circuit breaker, bulkhead) | Medium |
| Timeout configuration | HTTP clients, database connections, and external calls have explicit timeouts | High |
| Retry with backoff | Transient failures retried with exponential backoff and jitter | Medium |
| Health check monitoring | External monitoring polls health endpoints (uptime monitoring) | High |

Grep patterns:

| Framework | Pattern | Issue |
|-----------|---------|-------|
| Flask/FastAPI/Express | No `/health` or `/healthz` route defined | Missing liveness probe |
| Python `requests` | `requests.get(` without `timeout=` | No timeout, hangs forever |
| Node.js `axios` | `axios.get(` without `timeout:` | Same |
| Kubernetes | `livenessProbe:` / `readinessProbe:` absent in pod spec | Container has no health monitoring |
| Docker Compose | No `healthcheck:` in service definition | Container has no health monitoring |
| Any | `signal.signal(signal.SIGTERM` absent | No graceful shutdown |

Enterprise tier table: synthetic monitoring (Datadog Synthetics, Pingdom, Checkly), chaos engineering (Gremlin, Chaos Monkey, Litmus), multi-region health (Route 53 health checks, Azure Traffic Manager).

**Section: Phase 11 — Cost & Cardinality Management (Both modes)**

**Planning mode:** Design cost-conscious telemetry architecture:
- Dual-export pattern: `OTEL_MODE` env var for personal (S3+DuckDB) vs enterprise (Grafana Cloud/Datadog)
- Sampling strategy: head-based vs tail-based, sampling rates per service
- Retention policy: how long to keep each signal type?
- Cardinality budget: what labels are allowed on metrics?

**Audit mode:**

Standard tier checks table:

| Check | What to look for | Severity |
|-------|-----------------|----------|
| No high-cardinality metric labels | Labels don't include user IDs, request IDs, UUIDs, timestamps, or unbounded values | High |
| Sampling configured for traces | Not sending 100% of traces in high-volume production | Medium |
| Log level appropriate for production | Not running DEBUG level in production (excessive volume) | High |
| Retention policies set | Logs, metrics, and traces have defined retention periods | Medium |
| Cost monitoring for telemetry | Monthly cost of observability backends tracked | Medium |
| Collector processing pipeline | OTel Collector uses processors (batch, filter, attributes) to reduce volume | Medium |
| Metric aggregation at source | Pre-aggregated where possible (histograms, summaries) vs raw events | Low |
| Unused metrics identified | Metrics that no dashboard or alert references | Low |
| Tier-appropriate backend | Backend cost matches the system's budget and scale | Medium |
| Export fan-out configured | Dual export to cheap storage + rich platform when needed | Low |

Enterprise tier: observability cost management platforms (Chronosphere, Calyptia, Cribl), managed collector services, committed-use discounts.

**Section: Phase 12 — Findings Report (Both modes)**

**Planning mode report template:**

```markdown
## Observability Strategy — [System Name]

### Observability Surface Summary
- Services: [list]
- Current telemetry: [list]
- Critical paths: [list]
- Deployment model: [description]

### Instrumentation Plan
| Service | Logs | Metrics | Traces | Method |
|---------|------|---------|--------|--------|

### SLI/SLO Definitions
| Service | SLI | Target SLO | Measurement |
|---------|-----|------------|-------------|

### Alerting Strategy
| Signal | Threshold | Routing | Runbook |
|--------|-----------|---------|---------|

### Cost Estimate
| Tier | Stack | Monthly Cost |
|------|-------|-------------|

### Observability Design Checklist
- [ ] Instrumentation standard selected (OTel recommended)
- [ ] Three pillars covered (logs, metrics, traces)
- [ ] SLIs and SLOs defined for critical services
- [ ] Alerting strategy with escalation paths
- [ ] Dashboard plan for operators
- [ ] Cost tier selected with budget
- [ ] Pipeline observability (if applicable)
- [ ] Model monitoring (if applicable)
```

**Audit mode report template:**

```markdown
## Observability Audit Report — [System Name]

### Executive Summary
- Total findings: X
- Critical: X | High: X | Medium: X | Low: X
- Fixed during audit: X
- Remaining: X

### Findings
| # | Severity | Phase | File:Line | Description | Status |
|---|----------|-------|-----------|-------------|--------|

### Tier Coverage
| Phase | Standard | Enterprise |
|-------|----------|------------|
| Phase 0: Anti-Patterns | [X patterns scanned / Y findings] | [Linting tool: configured/not] |
| Phase 2: Instrumentation | [OTel SDK: yes/no] | [APM: configured/not] |
| Phase 3: Logging | [X/10 checks passed] | [Log platform: configured/not] |
| Phase 4: Metrics/SLOs | [X/10 checks passed] | [Metrics platform: configured/not] |
| Phase 5: Tracing | [X/10 checks passed] | [Tracing platform: configured/not] |
| Phase 6: Pipeline | [X/10 checks passed] | [Data observability: configured/not] |
| Phase 7: ML/Model | [X/10 checks passed] | [ML monitoring: configured/not] |
| Phase 8: Alerting | [X/10 checks passed] | [Incident platform: configured/not] |
| Phase 9: Dashboards | [X/10 checks passed] | [Dashboard platform: configured/not] |
| Phase 10: Health Checks | [X/10 checks passed] | [Synthetic monitoring: configured/not] |
| Phase 11: Cost/Cardinality | [X/10 checks passed] | [Cost management: configured/not] |

### Observability Maturity Rating
- **Standard tier**: X/Y checks passed (Z% coverage)
- **Enterprise tier**: X/Y controls configured (Z% coverage)
- **Overall**: [Observable / Partially Observable / Significant Blind Spots / Flying Blind]

### Ready for production: Yes / No (with blockers)
```

**Section: Important Rules**

Match the style at `security-audit/SKILL.md:708-719`:

- **Fix as you go.** When audit mode finds a Critical or High issue that you can fix (add a health check, configure structured logging, add a missing OTel exporter), fix it immediately.
- **Evidence-based claims.** Every finding must include file path, line number, or specific evidence. Never say "probably needs monitoring."
- **No assumptions.** Read the actual code, configs, and deployment files. Don't assume telemetry exists because a library is in `requirements.txt`.
- **Verify fixes.** After fixing an observability gap, re-run the check to confirm.
- **Respect existing patterns.** If the project uses a specific logging framework or metrics library, extend it rather than introducing a new one.
- **Scope awareness.** Don't flag managed-service observability as missing (e.g., AWS Lambda has built-in CloudWatch metrics).
- **Phase 7 is conditional.** Only run ML/Model Observability if ML models or analytical pipelines are detected.
- **Two-tier awareness.** Standard tier checks are always actionable — fix issues found. Enterprise tier items serve as a professional reference — document which are applicable and which are configured, but don't block releases on Enterprise items the team hasn't adopted yet.

**Step 2: Verify complete SKILL.md**

Run: `wc -l plugins/mad-scientist-skills/skills/observability-audit/SKILL.md`
Expected: approximately 400-600 lines.

---

## Task 5: Create template — `otel-instrumentation.md`

**Files:**
- Create: `plugins/mad-scientist-skills/skills/observability-audit/templates/otel-instrumentation.md`

Follow the template pattern from `security-audit/templates/web-security-headers.md`:
1. H1 title
2. Brief description
3. **Purpose** — "Does this application have proper OpenTelemetry instrumentation? Are the three pillars (logs, metrics, traces) covered?"
4. **Checklist** — pre-audit items (which language, framework, deployment model, existing telemetry)
5. **Main content sections:**
   - OTel SDK setup per language (Python, Node.js, Go, Java, .NET) with pip/npm/go install commands and initialization code
   - Auto-instrumentation packages table (HTTP clients, databases, messaging, gRPC per language)
   - Exporter configuration (OTLP, Prometheus, Console, File, S3)
   - OTel Collector configuration (receivers, processors, exporters, pipelines)
   - Resource attribute conventions (`service.name`, `service.version`, `deployment.environment`, `service.namespace`)
   - Custom attribute namespaces — when no semantic conventions exist, define `<domain>.*` attributes with examples
   - Dual-export pattern — `OTEL_MODE` env var, layered Collector configs for cost-tier switching
   - Framework-specific setup table (Django, Flask, FastAPI, Express, Next.js, Spring Boot, ASP.NET)
6. **Best practices**
7. **Anti-patterns**

---

## Task 6: Create template — `structured-logging.md`

**Files:**
- Create: `plugins/mad-scientist-skills/skills/observability-audit/templates/structured-logging.md`

**Purpose:** "Are logs structured, contextual, and shipped to a central location?"

**Key content:**
- JSON logging setup per framework (Python `logging` + `python-json-logger`, `structlog`, Node.js `pino`/`winston`, Go `zap`/`zerolog`, Java `logback` + `logstash-encoder`)
- Log level policy table (DEBUG/INFO/WARNING/ERROR/CRITICAL with what to log at each level)
- Correlation ID implementation (inject `trace_id`/`span_id` from OTel context into log entries)
- PII scrubbing patterns (field-level redaction, allowlist vs denylist approaches)
- Log shipping approaches (stdout → container runtime → aggregator, sidecar, agent, direct SDK)
- Log format comparison (JSON vs logfmt vs plain text — when to use each)
- Framework-specific examples with GOOD vs BAD code snippets
- Best practices, anti-patterns

---

## Task 7: Create template — `metrics-sli-slo.md`

**Files:**
- Create: `plugins/mad-scientist-skills/skills/observability-audit/templates/metrics-sli-slo.md`

**Purpose:** "Are the right things measured? Are SLIs and SLOs defined for critical services?"

**Key content:**
- RED methodology (Request rate, Error rate, Duration) — when to use, what to measure
- USE methodology (Utilization, Saturation, Errors) — for infrastructure/resources
- Metric types reference (Counter, Gauge, Histogram, Summary — when to use each, with examples)
- SLI design patterns (availability = successful requests / total requests, latency = requests < threshold / total requests)
- SLO target selection (99.9% = 8.77 hr/year downtime, 99.95% = 4.38 hr/year, etc.)
- Error budget calculation and burn rate alerting (multi-window, multi-burn-rate)
- Metric naming conventions (Prometheus naming: `<namespace>_<name>_<unit>`, e.g., `http_request_duration_seconds`)
- High-cardinality prevention (label value guidelines, metric explosion examples)
- OTel metrics SDK usage per language (Counter, Histogram examples)
- Best practices, anti-patterns

---

## Task 8: Create template — `distributed-tracing.md`

**Files:**
- Create: `plugins/mad-scientist-skills/skills/observability-audit/templates/distributed-tracing.md`

**Purpose:** "Can we trace a request end-to-end across all services and see where time is spent?"

**Key content:**
- Context propagation standards (W3C TraceContext — `traceparent` header format, B3 — `X-B3-TraceId` headers)
- Span naming conventions per signal type (HTTP: `HTTP GET /api/users`, DB: `SELECT users`, RPC: `grpc.UserService/GetUser`, messaging: `send topic.name`)
- Span attribute semantic conventions reference (from OpenTelemetry semantic conventions: `http.method`, `http.status_code`, `db.system`, `db.statement`, `rpc.method`, `messaging.system`)
- Span status and error recording (when to set `SpanStatusCode.ERROR`, recording exceptions)
- Sampling strategies (head-based: AlwaysOn, TraceIdRatioBased, ParentBased; tail-based: error-focused, latency-focused — OTel Collector tail_sampling processor)
- Trace-to-log correlation (injecting `trace_id` and `span_id` into log records)
- Span events vs child spans (when to use each)
- Baggage propagation (W3C Baggage for cross-cutting concerns)
- Framework-specific examples (Python, Node.js, Go)
- Best practices, anti-patterns

---

## Task 9: Create template — `pipeline-observability.md`

**Files:**
- Create: `plugins/mad-scientist-skills/skills/observability-audit/templates/pipeline-observability.md`

**Purpose:** "Can we detect pipeline failures, data quality issues, and freshness problems before they impact downstream consumers?"

**Key content:**
- Pipeline health signals (execution duration, success/failure rate, row counts, data freshness, schema drift)
- dbt observability: parsing `target/run_results.json` (zero-dependency, Python code example), `sources.yml` freshness configuration, test result tracking
- Airflow observability: `on_failure_callback`, DAG-level metrics, task instance metrics, SLA misses
- Dagster/Prefect observability: built-in asset/flow metrics, event-based monitoring
- Data quality gates: pre/post-load validation, Great Expectations integration, dbt test patterns
- Dead letter pattern: quarantine failed records with metadata (error reason, timestamp, source), monitor dead letter volume
- Data freshness monitoring: staleness thresholds, freshness SLIs, alerting on stale data
- Data volume anomaly detection: statistical baseline for expected row counts, alert on significant deviation
- Idempotency verification: re-run safety checks, deduplication patterns
- Pipeline-as-OTel-traces: model pipeline stages as spans in a single trace for end-to-end visibility
- Best practices, anti-patterns

---

## Task 10: Create template — `ml-model-observability.md`

**Files:**
- Create: `plugins/mad-scientist-skills/skills/observability-audit/templates/ml-model-observability.md`

**Purpose:** "Can we detect when models degrade, drift, or produce invalid outputs before they impact users?"

**Key content:**
- Model lifecycle monitoring (training → validation → deployment → production → retraining)
- Drift detection methods with code examples:
  - **PSI** (Population Stability Index): binned distribution comparison, threshold > 0.1 minor, > 0.2 significant. Python implementation (~20 lines, `numpy` only)
  - **CUSUM** (Cumulative Sum): sequential change detection, O(n), ~10 lines pure Python. Detects sustained small shifts that single-point thresholds miss
  - **KS Test**: `scipy.stats.ks_2samp(reference, current)`, p-value threshold
  - **Wasserstein Distance**: `scipy.stats.wasserstein_distance(reference, current)`, quantifies shift magnitude
  - **Hard Constraints**: domain-specific invariants (probabilities in [0,1], sums ≈ 1.0, physical bounds)
- Reference baselines: how to store and version training-time distributions (config files, seed data, Delta tables, model registry artifacts)
- Performance estimation without ground truth: NannyML CBPE concept and usage
- Open-source monitoring tools table (Evidently AI, NannyML, WhyLogs — all Apache 2.0, with integration paths)
- Model registry patterns: version tracking, Champion/Challenger aliases, A/B deployment
- Custom OTel attributes for ML: `model.name`, `model.version`, `model.input_count`, `model.output_mean`, `model.drift_psi`
- Input/output distribution tracking as OTel metrics
- Alert thresholds for drift signals
- Best practices, anti-patterns

---

## Task 11: Create template — `alerting-runbooks.md`

**Files:**
- Create: `plugins/mad-scientist-skills/skills/observability-audit/templates/alerting-runbooks.md`

**Purpose:** "When something breaks, do the right people know, and do they know what to do?"

**Key content:**
- Alert design principles:
  - Alert on symptoms, not causes ("latency > SLO" not "CPU > 80%")
  - Every alert must be actionable — if there's nothing to do, it's not an alert
  - Use multi-window burn rate alerting for SLOs (not simple threshold)
  - Prefer severity levels (page, ticket, log) with clear routing
- Alert quality metrics:
  - Signal-to-noise ratio (actionable alerts / total alerts)
  - Mean time to acknowledge (MTTA)
  - Alert fatigue indicators (alerts ignored, pages dismissed without action)
- SLO burn rate alerting: multi-window configuration (e.g., 1h window @ 14.4x burn, 6h window @ 6x burn), with Prometheus/Grafana rule examples
- Runbook template:
  ```
  # Alert: [Alert Name]
  ## Impact
  ## Diagnosis Steps
  ## Remediation
  ## Escalation
  ## Post-Incident
  ```
- Escalation path design: L1 (on-call) → L2 (team lead) → L3 (engineering manager) with time thresholds
- Alert grouping and inhibition: Alertmanager `group_by`, `inhibit_rules` examples
- Dead-man's-switch / heartbeat monitoring: alert when expected signal stops
- Chaos engineering for alert testing: periodic validation that alerts fire correctly
- On-call hygiene: rotation best practices, handoff checklists
- Best practices, anti-patterns

---

## Task 12: Update `plugin.json`

**Files:**
- Modify: `plugins/mad-scientist-skills/.claude-plugin/plugin.json`

Update the `description` field to include the new observability-audit skill:

```json
{
  "name": "mad-scientist-skills",
  "version": "1.0.0",
  "description": "C4 architecture diagrams (Structurizr DSL), two-tier security auditing (STRIDE, OWASP Top 10, web headers, API security, auth/session, supply chain), two-tier observability auditing (beta: instrumentation, logging, metrics, tracing, pipeline/ML monitoring, alerting, SLIs/SLOs), and pre-commit quality gate with architecture diagram generation",
  "author": {
    "name": "Karsten S. Nielsen"
  }
}
```

---

## Execution Notes

**Parallelization:** Tasks 5-11 (templates) are fully independent and can be dispatched in parallel. Task 12 (plugin.json) is independent of all other tasks. Tasks 1-4 (SKILL.md) are sequential.

**Optimal execution order:**
1. Task 1 (SKILL.md foundation)
2. Tasks 2, 3, 4 (SKILL.md phases — sequential, same file)
3. Tasks 5-11 (all templates — parallel) + Task 12 (plugin.json — parallel)

**No commits until user review.** All files remain as uncommitted changes per user instruction.
