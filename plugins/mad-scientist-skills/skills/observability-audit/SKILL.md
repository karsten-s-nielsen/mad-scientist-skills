---
name: observability-audit
description: Comprehensive observability audit with two modes and two tiers (beta). Planning mode designs telemetry strategy, SLIs/SLOs, and instrumentation architecture. Audit mode scans code and infrastructure for observability gaps including logging, metrics, tracing, alerting, pipeline monitoring, and ML model drift detection. Each phase has Standard (free/open-source tools, always actionable) and Enterprise (paid observability platforms, aspirational checklist) tiers. Use when asked to "observability audit", "check monitoring", "find blind spots", "audit telemetry", "design observability", or "review instrumentation".
---

# Observability Audit

A comprehensive observability skill with two modes and two tiers:

**Modes:**
- **Planning** (before code exists) — telemetry strategy, SLI/SLO design, instrumentation architecture
- **Audit** (on existing code) — scanning for observability gaps in logging, metrics, tracing, alerting, pipelines, and ML models

**Tiers** (applied within each phase):
- **Standard** — free/open-source tools, code-level patterns, OpenTelemetry-native. Always actionable for any developer.
- **Enterprise** — paid observability platforms (Datadog, New Relic, Splunk, etc.). Serves as a professional checklist documenting what enterprise teams should implement.

**Core question:** "Can you see what your system is doing?"

## When to use this skill

- When the user says "observability audit", "check monitoring", "find blind spots", "audit telemetry", "design observability", or "review instrumentation"
- Before designing a new system (planning mode) — to define telemetry strategy and SLIs/SLOs early
- On an existing codebase (audit mode) — to find and fix observability gaps
- Before a production deployment — to validate monitoring and alerting posture
- After adding new services, data pipelines, or ML models
- When investigating production incidents caused by insufficient observability

## Mode detection

Determine which mode to operate in based on the project state:

| Signal | Mode | Rationale |
|--------|------|-----------|
| User says "design observability", "telemetry strategy", "define SLOs" | **Planning** | Architecture-level analysis before code |
| User says "audit", "check monitoring", "find blind spots" | **Audit** | Code and infrastructure scanning |
| No source code exists yet (only docs, diagrams, RFCs) | **Planning** | Nothing to scan — design telemetry instead |
| Source code and/or infrastructure files exist | **Audit** | Concrete artifacts to analyze |
| Both code and a request to "design observability" | **Both** | Run planning phases on architecture, audit phases on code |

When in doubt, ask the user. If both modes apply, run all 13 phases.

## Severity classification

Every finding must be assigned a severity:

| Severity | Criteria | Action | SLA |
|----------|----------|--------|-----|
| **Critical** | Complete blind spot on a critical path, no alerting on user-facing failures, silent data loss, no error tracking | Fix immediately | Block release |
| **High** | Missing tracing on key services, no SLOs on critical endpoints, unstructured logging in production, no correlation IDs | Fix before next release | 1 sprint |
| **Medium** | Incomplete metric coverage, missing dashboard drill-downs, no log rotation, weak sampling strategy | Schedule fix | 2 sprints |
| **Low** | Naming convention inconsistencies, missing metadata labels, dashboard cosmetic issues, documentation gaps | Track in backlog | Best effort |

## Audit process

Execute all applicable phases in order. Skip phases marked for a mode you are not running. Do NOT skip applicable phases. Do NOT claim completion without evidence.

---

### Phase 0: Anti-Pattern Scan (Audit mode)

Fast grep-based scan for observability anti-patterns. Runs first to catch obvious issues before deeper analysis.

#### Standard tier

Scan all source files for these patterns. Each match requires manual review — some may be intentional (e.g., `print()` in a CLI tool).

| Pattern | Language | Risk |
|---------|----------|------|
| `print(` | Python | Debug output instead of structured logging |
| `console.log(` | JS/TS | Debug output instead of structured logging |
| `System.out.println(` | Java | Debug output instead of structured logging |
| `fmt.Println(` / `log.Println(` | Go | Unstructured logging, no level or context |
| `except:` / `except Exception:` without logging | Python | Swallowed exception — silent failure |
| `catch (e) {}` | JS/TS | Empty catch block — silent failure |
| `catch (Exception e) {}` | Java | Empty catch block — silent failure |
| `pass` in exception handler | Python | Swallowed exception — silent failure |
| `# TODO.*log\|# FIXME.*monitor\|# HACK.*metric` | Any | Acknowledged observability debt |
| `logging.disable\|logging.NOTSET` | Python | Logging intentionally disabled |
| `time.sleep(` in retry loops | Python | Retry without backoff metrics or visibility |
| `@app.route` / `@router` without request metrics middleware | Python (Flask/FastAPI) | HTTP endpoints without request metrics |
| `app.use(` / `router.` without morgan/pino/winston | JS (Express) | HTTP endpoints without request logging |
| `logger = logging.getLogger()` | Python | Root logger — undifferentiated log source |
| Hardcoded values in metric names (e.g., `counter_user_123`) | Any | High-cardinality metric labels, cardinality explosion |

For each finding: record file path, line number, pattern matched, and whether it is a true positive or intentional usage. Flag true positives as Critical or High.

#### Enterprise tier

Integrate with static analysis tools for deeper observability coverage:

| Tool | Purpose | Configuration |
|------|---------|---------------|
| SonarQube custom rules | Flag missing logging in catch blocks, dead code paths | Custom quality profile with observability rules |
| Semgrep observability rulesets | Pattern-based detection of observability anti-patterns | `semgrep --config p/logging` |
| ESLint `no-console` | Flag `console.log` usage in production code | `.eslintrc` with `no-console: error` |
| pylint `logging-not-lazy` | Flag lazy string formatting in logging calls | `.pylintrc` with `logging-not-lazy` enabled |

Document which tool is configured and whether it runs in CI.

**Output:** Anti-pattern findings table with file paths, risk classification, and true/false positive status.

---

### Phase 1: Discovery (Both modes)

Explore the project to understand its observability surface:

- Read `CLAUDE.md`, `README.md`, `AGENTS.md`, and any architecture docs
- Identify the tech stack, frameworks, and language versions
- Map the **observability surface**:
  - Services and entry points: APIs, workers, cron jobs, event consumers
  - Data stores: databases, caches, queues, object storage
  - External integrations: third-party APIs, SaaS services, cloud provider services
  - Existing telemetry: logging libraries, metrics clients, tracing SDKs
  - Observability backends: Prometheus, Grafana, Jaeger, ELK, cloud-native services
  - Deployment model: containers, serverless, VMs, managed services
  - CI/CD pipeline: build, test, deploy stages
  - Data pipelines: ETL/ELT jobs, dbt models, Airflow DAGs, Spark jobs
  - ML models: training pipelines, inference endpoints, model registries
  - Critical user paths: checkout, authentication, data submission, search
  - Team operational maturity: on-call practices, incident history, runbook coverage

**Output:** An observability surface summary listing all services, telemetry, backends, and critical paths.

---

### Phase 2: Instrumentation Foundation (Both modes)

Evaluate the OpenTelemetry SDK setup, exporters, collector configuration, and auto-instrumentation.

Load `templates/otel-instrumentation.md` for the full OTel reference with language-specific setup patterns.

**Planning mode:** Evaluate the planned instrumentation approach:
- Which telemetry signals? (traces, metrics, logs)
- Which OTel SDKs and auto-instrumentation libraries?
- How will telemetry be exported? (direct export, collector, agent)
- What resource attributes will identify services?
- Is there a collector topology plan? (sidecar, gateway, agent)

**Audit mode:**

#### Standard tier

| Check | What to look for | Severity if missing |
|-------|-----------------|---------------------|
| OTel SDK installed | `opentelemetry-sdk`, `@opentelemetry/sdk-node`, `go.opentelemetry.io/otel` in dependencies | High |
| SDK properly initialized | `TracerProvider`, `MeterProvider`, `LoggerProvider` configured at startup | High |
| Exporter configured | OTLP exporter or backend-specific exporter (Prometheus, Jaeger) | High |
| Resource attributes set | `service.name`, `service.version`, `deployment.environment` on all telemetry | Medium |
| Auto-instrumentation enabled | HTTP, database, and messaging auto-instrumentation libraries installed | Medium |
| Context propagation configured | W3C TraceContext or B3 propagation across service boundaries | High |
| Shutdown hook registered | Graceful flush of telemetry on process exit | Medium |
| Collector deployed | OTel Collector running as sidecar or gateway for telemetry routing | Medium |

#### Enterprise tier

| Platform | Purpose | Integration check |
|----------|---------|-------------------|
| Datadog Agent | Unified APM, metrics, logs collection | `dd-trace` library, `DD_*` environment variables |
| New Relic APM | Full-stack observability with AI correlation | `newrelic` agent package, `NEW_RELIC_LICENSE_KEY` |
| Dynatrace OneAgent | Automatic full-stack instrumentation | OneAgent deployed, `DT_*` environment variables |
| AWS X-Ray | AWS-native distributed tracing | X-Ray SDK or OTel with X-Ray exporter |
| Azure Monitor | Azure-native application insights | Application Insights SDK, connection string |
| Google Cloud Trace | GCP-native distributed tracing | Cloud Trace SDK or OTel with GCP exporter |

**Output:** Instrumentation assessment with gaps and recommended configuration.

---

### Phase 3: Structured Logging (Audit mode)

Verify log format, levels, correlation IDs, and that PII/secrets are excluded from logs.

Load `templates/structured-logging.md` for the full logging reference with framework-specific patterns.

#### Standard tier

| Check | What to look for | Severity if missing |
|-------|-----------------|---------------------|
| JSON log format | Structured JSON output — not plaintext `print` statements | High |
| Consistent log levels | Appropriate use of DEBUG, INFO, WARN, ERROR, FATAL | Medium |
| Correlation IDs | `trace_id`, `span_id`, or `request_id` in every log line | High |
| Contextual fields | `service`, `environment`, `user_id` (hashed), `endpoint` in log context | Medium |
| No PII in logs | No email, name, address, SSN, phone number in log output | Critical |
| No secrets in logs | No API keys, tokens, passwords, connection strings in log output | Critical |
| Centralized aggregation | Logs shipped to a central store (ELK, Loki, CloudWatch) | High |
| Log rotation configured | File-based logs have rotation and retention policies | Medium |
| Stack traces on errors | Exceptions logged with full stack trace at ERROR level | Medium |
| Request/response logging | HTTP request method, path, status code, duration logged | High |

#### Grep patterns for logging issues

| Language | Pattern | Issue |
|----------|---------|-------|
| Python | `print(\|sys\.stdout\.write(` | Unstructured output instead of logging |
| Python | `logging\.debug\(f"\|logging\.info\(f"` | f-string in logging (lazy evaluation bypassed) |
| Python | `except.*:\s*pass` | Swallowed exception without logging |
| JS/TS | `console\.(log\|warn\|error)\(` | Console output instead of structured logger |
| Java | `System\.out\.print\|System\.err\.print` | Stdout instead of logging framework |
| Java | `e\.printStackTrace()` | Stack trace to stderr instead of logger |
| Go | `fmt\.Print\|log\.Print` | Unstructured logging, no levels |

#### Enterprise tier

| Platform | Purpose | Integration check |
|----------|---------|-------------------|
| Splunk | Log aggregation with search and analytics | Splunk forwarder or HEC endpoint configured |
| Datadog Logs | Unified logs with APM correlation | `dd-trace` log injection, Datadog Agent log collection |
| Grafana Loki Cloud | Managed Loki for log aggregation | Loki push endpoint, Promtail or Alloy agent |
| CloudWatch Logs | AWS-native log aggregation | CloudWatch agent or SDK log group configuration |
| Azure Monitor Logs | Azure-native log analytics | Log Analytics workspace, diagnostic settings |
| Elastic Cloud | Managed Elasticsearch for log analysis | Filebeat or Elastic Agent, index lifecycle policies |

**Output:** Logging findings table with file paths, issue type, and remediation.

---

### Phase 4: Metrics & SLIs/SLOs (Both modes)

Define and validate metrics using RED/USE methodology, SLI/SLO definitions, and error budgets.

Load `templates/metrics-sli-slo.md` for the full metrics reference with RED/USE patterns and SLO calculation examples.

**Planning mode:** Design the metrics and SLO strategy:
- Which SLIs will measure user happiness? (availability, latency, throughput, correctness)
- What SLO targets are appropriate? (99.9%, 99.95%, etc.)
- Which methodology applies? RED for request-driven, USE for resource-driven
- How will error budgets be calculated and consumed?
- What custom business metrics are needed?

**Audit mode:**

#### Standard tier

| Check | What to look for | Severity if missing |
|-------|-----------------|---------------------|
| RED metrics (request-driven) | Rate, Error rate, Duration on all HTTP/gRPC endpoints | High |
| USE metrics (resource-driven) | Utilization, Saturation, Errors on CPU, memory, disk, connections | Medium |
| Custom business metrics | Domain-specific counters (orders, signups, payments) | Medium |
| Correct metric types | Counter for totals, Gauge for current values, Histogram for distributions | Medium |
| SLIs defined | Measurable indicators tied to user-facing behavior | High |
| SLOs documented | Target percentages with measurement windows (e.g., 99.9% over 30 days) | High |
| Error budgets tracked | Remaining error budget calculated and visible | Medium |
| Naming conventions | Consistent prefix, snake_case, units in name (e.g., `http_request_duration_seconds`) | Low |
| No high-cardinality labels | Labels limited to bounded sets — no user IDs, email, request IDs | High |
| Exposition endpoint | `/metrics` endpoint (Prometheus) or push exporter configured | High |

#### Enterprise tier

| Platform | Purpose | Integration check |
|----------|---------|-------------------|
| Datadog Metrics | Managed metrics with anomaly detection | StatsD/DogStatsD client, Datadog Agent |
| Grafana Cloud Mimir | Managed Prometheus-compatible long-term storage | Remote write endpoint, Mimir data source |
| CloudWatch Metrics | AWS-native metrics with alarms | CloudWatch SDK, custom metrics namespace |
| Azure Monitor Metrics | Azure-native metrics and autoscale | Application Insights, custom metrics API |
| New Relic Metrics | Full-stack metrics with AI correlation | Dimensional metrics API, New Relic agent |
| SLO platforms | Dedicated SLO tracking and error budget management | Nobl9, Datadog SLOs, Google SLO Generator |

**Output:** Metrics and SLO assessment with gaps, missing SLIs, and recommended targets.

---

### Phase 5: Distributed Tracing (Audit mode)

Verify context propagation, span design, sampling strategy, and trace completeness.

Load `templates/distributed-tracing.md` for the full tracing reference with span design patterns and sampling strategies.

#### Standard tier

| Check | What to look for | Severity if missing |
|-------|-----------------|---------------------|
| Context propagation | W3C TraceContext or B3 headers propagated across service boundaries | Critical |
| Spans on critical paths | Every user-facing request produces a trace with spans for key operations | High |
| Span naming conventions | `<verb> <resource>` format (e.g., `GET /api/users`, `SELECT users`) | Medium |
| Span attributes | Relevant context on spans (HTTP method, status, DB statement, queue name) | Medium |
| Error recording on spans | `span.record_exception()` and `span.set_status(ERROR)` on failures | High |
| Sampling strategy configured | Head or tail sampling with appropriate rate (not 100% in production) | Medium |
| Trace-to-log correlation | `trace_id` present in log lines for cross-signal navigation | High |
| Cross-service trace completeness | Traces span full request lifecycle across all services | High |
| Span events | Key milestones recorded as span events (e.g., cache hit/miss, retry) | Low |
| Baggage propagation | Cross-cutting concerns (tenant ID, feature flags) propagated via baggage | Low |

#### Grep patterns for tracing issues

| Language | Pattern | Issue |
|----------|---------|-------|
| Python | `requests\.(get\|post\|put)\(` without instrumentation | HTTP calls without trace propagation |
| Python | `tracer\.start_span\(` without `with` or `end()` | Span leak — never closed |
| JS/TS | `fetch\(\|axios\.\|http\.request\(` without instrumentation | HTTP calls without trace propagation |
| Go | `http\.Get\(\|http\.Post\(` without injected context | HTTP calls without trace propagation |
| Any | `span\.set_attribute\(.*user_id\|.*email` | PII in span attributes |

#### Enterprise tier

| Platform | Purpose | Integration check |
|----------|---------|-------------------|
| Grafana Tempo Cloud | Managed distributed tracing with TraceQL | Tempo data source, trace-to-metrics pipeline |
| Datadog APM | Full-stack tracing with flame graphs | `dd-trace` library, APM enabled in agent |
| Honeycomb | High-cardinality event exploration | Honeycomb SDK or OTel exporter |
| AWS X-Ray | AWS-native tracing with service map | X-Ray daemon, sampling rules |
| Azure Monitor Traces | Azure-native distributed tracing | Application Insights, correlation headers |
| Jaeger Cloud | Managed Jaeger for trace storage and analysis | Jaeger agent or OTel exporter |

**Output:** Tracing findings table with gaps, missing spans, and propagation issues.

---

### Phase 6: Pipeline & Data Observability (Both modes)

Evaluate ETL/ELT pipeline health monitoring, data quality gates, and freshness tracking.

Load `templates/pipeline-observability.md` for the full pipeline monitoring reference with framework-specific patterns.

**Planning mode:** Design the pipeline monitoring strategy:
- Which pipelines are critical? (revenue, compliance, user-facing)
- What freshness SLAs exist for downstream consumers?
- How will data quality be measured and enforced?
- Where should dead letter queues be implemented?
- How will pipeline failures be surfaced and alerted on?

**Audit mode:**

#### Standard tier

| Check | What to look for | Severity if missing |
|-------|-----------------|---------------------|
| Execution metrics | Pipeline duration, row counts, success/failure rate tracked | High |
| Freshness monitoring | Table/dataset freshness compared to expected SLA | High |
| Data quality gates | Schema validation, null checks, uniqueness, range checks in pipeline | High |
| Dead letter handling | Failed records routed to DLQ with metadata for investigation | High |
| Idempotency verification | Pipelines produce consistent results on re-run | Medium |
| dbt test results exposed | `dbt test` outcomes published as metrics or alerts | Medium |
| Model execution time | dbt model or transformation step duration tracked | Medium |
| Source availability checks | Upstream source health verified before pipeline runs | Medium |
| Volume anomaly detection | Row count compared to historical baseline, alerting on significant deviation | Medium |
| Retry visibility | Retry attempts logged with backoff duration and outcome | Medium |

#### Grep patterns per framework

| Framework | Pattern | Issue |
|-----------|---------|-------|
| dbt | `models/` without corresponding `tests/` or `schema.yml` tests | Untested dbt models |
| dbt | `run_results.json` not parsed for metrics | Missing execution telemetry — parse zero-dependency `run_results.json` for duration, status, row counts |
| Airflow | `@dag` / `@task` without `on_failure_callback` | Silent DAG failures |
| Airflow | `retries=0` or missing `retries` | No retry on transient failures |
| Generic | `try:.*except.*pass` around data operations | Silent data processing failures |
| Generic | `INSERT\|COPY\|MERGE` without row count validation | Unverified write operations |

#### Enterprise tier

| Platform | Purpose | Integration check |
|----------|---------|-------------------|
| Monte Carlo | Data observability with automated anomaly detection | Monte Carlo agent, warehouse integration |
| Atlan | Data catalog with lineage and quality monitoring | Atlan connector, metadata sync |
| Elementary Cloud | dbt-native data observability and alerting | `elementary` dbt package, cloud dashboard |
| dbt Cloud | Managed dbt with built-in monitoring and alerting | dbt Cloud project, job monitoring |
| Datafold | Data diff and regression testing for pipelines | Datafold CI integration, data diff on PRs |
| Soda Cloud | Data quality monitoring with SodaCL checks | `soda-core` library, Soda Cloud connection |

**Output:** Pipeline observability findings with gap analysis and recommended monitoring.

---

### Phase 7: ML/Model Observability (Both modes) — CONDITIONAL

**Only execute this phase if ML or analytical models are detected in the project** (e.g., scikit-learn, TensorFlow, PyTorch, XGBoost, MLflow, model serving endpoints, prediction APIs).

Load `templates/ml-model-observability.md` for the full model monitoring reference with drift detection methods and alerting patterns.

**Planning mode:** Design the model monitoring strategy:
- Which models are in production? What are their prediction types?
- What does model degradation look like for this domain?
- How will drift be detected? (input drift, concept drift, prediction drift)
- What hard constraints must predictions satisfy?
- How will model versions be tracked and compared?

**Audit mode:**

#### Standard tier

| Check | What to look for | Severity if missing |
|-------|-----------------|---------------------|
| Model version tracking | Model version, training date, and feature set recorded with predictions | High |
| Input distribution monitoring | Feature distributions compared to training baseline | High |
| Output distribution monitoring | Prediction distribution tracked for drift | High |
| Drift detection method | Statistical test or threshold configured for drift alerting | High |
| Performance metrics tracked | Accuracy, precision, recall, F1, AUC (or domain-specific) monitored over time | High |
| Hard constraint validation | Business rule violations caught (e.g., negative price, probability > 1.0) | Critical |
| Reference baselines stored | Training data statistics saved for comparison | Medium |
| Prediction latency tracked | Inference time measured as histogram metric | Medium |
| A/B or shadow deployment | Canary or shadow mode for new model versions | Medium |
| Data slice analysis | Performance monitored across important segments (geography, user type) | Medium |

#### Statistical drift detection methods

| Method | Type | Use case | Sensitivity |
|--------|------|----------|-------------|
| PSI (Population Stability Index) | Distribution comparison | Categorical and binned continuous features | Medium |
| CUSUM (Cumulative Sum) | Sequential analysis | Detecting gradual drift in streaming predictions | High |
| KS Test (Kolmogorov-Smirnov) | Distribution comparison | Continuous feature drift detection | Medium |
| Wasserstein Distance | Distribution comparison | Numerical feature drift with magnitude awareness | Medium |
| Hard Constraints | Rule-based | Business rule violations (output must be in range) | Immediate |
| CBPE (Confidence-Based Performance Estimation) | Performance estimation | Estimating model accuracy without ground truth labels | Medium |

#### Enterprise tier

| Platform | Purpose | Integration check |
|----------|---------|-------------------|
| Arize AI | ML observability with drift detection and explainability | Arize SDK, model logging integration |
| Fiddler | Model performance management and explainability | Fiddler client, model registration |
| WhyLabs Cloud | Data and ML monitoring with whylogs profiles | `whylogs` library, WhyLabs API key |
| NannyML Cloud | Performance estimation without ground truth | `nannyml` library, cloud dashboard |
| Evidently Cloud | ML monitoring dashboards and reports | `evidently` library, cloud workspace |
| SageMaker Model Monitor | AWS-native model monitoring with baseline comparison | Model monitor schedule, baseline constraints |
| Azure ML Model Monitor | Azure-native model monitoring | Azure ML workspace, data collector |

**Output:** Model observability findings with drift detection gaps and monitoring recommendations.

---

### Phase 8: Alerting & Incident Detection (Both modes)

Evaluate alert quality, routing, escalation paths, and runbook coverage.

Load `templates/alerting-runbooks.md` for the full alerting reference with alert design patterns and runbook templates.

**Planning mode:** Design the alerting strategy:
- Which signals should trigger alerts? (SLO burn rate, error rate spikes, latency degradation)
- What is the escalation path? (on-call engineer -> team lead -> incident commander)
- How will alert fatigue be managed? (grouping, inhibition, severity-based routing)
- What runbooks are needed for each alertable condition?
- How will alerts be tested and validated?

**Audit mode:**

#### Standard tier

| Check | What to look for | Severity if missing |
|-------|-----------------|---------------------|
| Alerts on golden signals | Latency, traffic, errors, saturation have alert rules | Critical |
| SLO-based alerting | Burn rate alerts on error budget consumption | High |
| Alert routing configured | Alerts reach the right team (Slack, email, PagerDuty, OpsGenie) | High |
| Escalation path defined | Unacknowledged alerts escalate after timeout | High |
| Runbooks linked to alerts | Every alert includes a link to its runbook | Medium |
| Alert noise management | Duplicate suppression, grouping, minimum duration before firing | Medium |
| Symptom-based alerts | Alerts on user-facing symptoms, not internal causes | Medium |
| Inhibition and grouping | Related alerts grouped, child alerts inhibited when parent fires | Low |
| Heartbeat / dead-man's-switch | Alerting on the absence of expected signals (e.g., no data received) | High |
| Alert testing | Alert rules tested with synthetic data or chaos experiments | Medium |

#### Anti-patterns to flag

- **Alert on every error**: Should alert on error *rate*, not individual errors
- **Missing severity levels**: All alerts at same priority — no differentiation
- **No runbook**: Alert fires but responder has no guidance
- **Threshold without baseline**: Static threshold without understanding normal behavior
- **Alert on cause, not symptom**: "CPU high" instead of "latency SLO breached"
- **No grouping**: 50 alerts fire for one incident

#### Enterprise tier

| Platform | Purpose | Integration check |
|----------|---------|-------------------|
| PagerDuty | Incident management with escalation policies | PagerDuty integration key, escalation policy |
| OpsGenie | Alert management with on-call scheduling | OpsGenie API key, team routing rules |
| xMatters | Intelligent alert routing and collaboration | xMatters integration, on-call groups |
| Datadog Monitors | Metric, log, and APM-based alerting | Monitor definitions, notification channels |
| Grafana Alerting | Unified alerting across Prometheus, Loki, Tempo | Alert rules, contact points, notification policies |
| CloudWatch Alarms | AWS-native metric and composite alarms | Alarm definitions, SNS topics, action configuration |
| incident.io | Incident management with Slack-native workflow | incident.io integration, severity definitions |
| FireHydrant | Incident management with runbook automation | FireHydrant integration, service catalog |

**Output:** Alerting findings table with gaps, missing runbooks, and noise assessment.

---

### Phase 9: Dashboard & Visualization (Audit mode)

Verify that operational dashboards provide actionable views with appropriate drill-down capability.

#### Standard tier

| Check | What to look for | Severity if missing |
|-------|-----------------|---------------------|
| Golden signals dashboard | Latency, traffic, errors, saturation visible at a glance | High |
| Service overview dashboard | Health status of all services in one view | Medium |
| On-call dashboard | Current incidents, recent alerts, error budget status | Medium |
| Request flow visualization | Request path across services with latency breakdown | Medium |
| Time range controls | Dashboards support flexible time ranges and comparison | Low |
| Dashboard-to-trace drill-down | Click from dashboard panel to related traces | Medium |
| Dashboard-to-log drill-down | Click from dashboard panel to related logs | Medium |
| No vanity dashboards | Dashboards drive action — not just total request counts with no context | Low |
| Dashboard as code | Dashboard definitions in version control (Grafonnet, Terraform, JSON) | Medium |
| Data freshness indicator | Dashboard shows when data was last updated | Low |

#### Enterprise tier

| Platform | Purpose | Integration check |
|----------|---------|-------------------|
| Grafana Cloud | Managed dashboards with unified data sources | Grafana Cloud instance, provisioned dashboards |
| Datadog Dashboards | Full-stack dashboards with APM and log correlation | Dashboard definitions, template variables |
| New Relic Dashboards | NRQL-powered dashboards with drill-down | Dashboard JSON, NRQL queries |
| Looker | Business intelligence with observability data | LookML models, explores for telemetry data |
| CloudWatch Dashboards | AWS-native dashboards with cross-account support | Dashboard definitions, widget configuration |
| Azure Workbooks | Azure-native interactive reports | Workbook templates, KQL queries |

**Output:** Dashboard assessment with gaps and recommended views.

---

### Phase 10: Health Checks & Readiness (Audit mode)

Verify that services implement proper health probes, dependency checks, and graceful degradation.

#### Standard tier

| Check | What to look for | Severity if missing |
|-------|-----------------|---------------------|
| Liveness probe | Endpoint confirming the process is running (e.g., `/healthz`) | High |
| Readiness probe | Endpoint confirming the service can accept traffic (e.g., `/readyz`) | High |
| Dependency health checks | Readiness probe verifies database, cache, and downstream service connectivity | High |
| Startup probe | Separate probe for slow-starting services to avoid premature restarts | Medium |
| Version in health response | Service version, commit SHA, or build ID in health check response | Low |
| Graceful shutdown | In-flight requests drained before process exit | High |
| Circuit breaker on dependencies | Failed dependency calls trigger circuit breaker to prevent cascading failure | Medium |
| Timeout configuration | All external calls have explicit timeouts (HTTP, DB, gRPC) | High |
| Retry with backoff | Retries use exponential backoff with jitter, not fixed intervals | Medium |
| Health check monitoring | Health endpoints monitored externally (uptime checks, synthetic probes) | Medium |

#### Grep patterns per framework

| Framework | Pattern | Issue |
|-----------|---------|-------|
| Flask | No `/health` or `/healthz` route defined | Missing health endpoint |
| FastAPI | No `/health` or `/readyz` route defined | Missing health endpoint |
| Express | No `/health` or `/healthz` route defined | Missing health endpoint |
| Spring Boot | `management.endpoint.health.enabled=false` | Health endpoint disabled |
| Kubernetes | No `livenessProbe` or `readinessProbe` in deployment spec | Missing container probes |
| Docker Compose | No `healthcheck` in service definition | Missing container health check |

#### Enterprise tier

| Control | Purpose | Tool / Service |
|---------|---------|----------------|
| Synthetic monitoring | Simulate user journeys from multiple regions | Datadog Synthetics, Grafana Synthetic Monitoring, AWS Synthetics |
| Chaos engineering | Validate resilience by injecting failures | Gremlin, Litmus, Chaos Monkey, AWS FIS |
| Multi-region health aggregation | Unified health view across regions | Global load balancer health checks, Datadog global monitors |

**Output:** Health check findings with missing probes and degradation gaps.

---

### Phase 11: Cost & Cardinality Management (Both modes)

Evaluate telemetry cost control, cardinality management, and efficient data retention.

**Planning mode:** Design the telemetry cost strategy:
- Dual-export pattern: high-fidelity to local store, sampled to cloud backend
- Sampling strategy: head sampling for low-value traffic, tail sampling for errors and slow requests
- Retention tiers: hot (7 days), warm (30 days), cold (90 days), archive (1 year)
- Cardinality budget: maximum unique time series per service
- Cost allocation: tag telemetry by team/service for chargeback

**Audit mode:**

#### Standard tier

| Check | What to look for | Severity if missing |
|-------|-----------------|---------------------|
| No high-cardinality labels | Metric labels limited to bounded sets — no user IDs, UUIDs, IP addresses | High |
| Sampling configured | Trace sampling rate appropriate for traffic volume | Medium |
| Log level appropriate for environment | DEBUG in development, INFO/WARN in production | Medium |
| Retention policies defined | Logs, metrics, and traces have defined retention periods | Medium |
| Cost monitoring | Telemetry ingestion volume tracked and alerted on | Medium |
| Collector processing rules | OTel Collector filters, transforms, or aggregates before export | Low |
| Metric aggregation | Pre-aggregation at collector level for high-volume metrics | Low |
| Unused metrics identified | Metrics that exist but are not used in alerts or dashboards | Low |
| Tier-appropriate backend | Local/open-source backend for development, managed for production | Low |
| Export fan-out | Single collection point with multiple export destinations | Low |

#### Enterprise tier

| Platform | Purpose | Integration check |
|----------|---------|-------------------|
| Chronosphere | Observability cost management with control plane | Chronosphere Collector, usage analytics |
| Calyptia | Fluent Bit enterprise management and optimization | Calyptia Core, pipeline optimization |
| Cribl | Observability pipeline for routing, filtering, and cost control | Cribl Stream, data routing rules |
| Managed collectors | Vendor-managed OTel collectors with optimization | Grafana Alloy, Datadog Agent, New Relic Infrastructure |
| Committed-use discounts | Volume-based pricing for predictable telemetry costs | Vendor contracts, reserved capacity |

**Output:** Cost and cardinality findings with optimization recommendations.

---

### Phase 12: Findings Report (Both modes)

Generate the final report. The format depends on the mode.

#### Planning mode report

Present the telemetry strategy and design recommendations:

```markdown
## Observability Strategy — [System Name]

### Observability Surface Summary
- Services: [list]
- Data stores: [list]
- Pipelines: [list]
- ML models: [list, if any]
- Critical user paths: [list]

### SLI/SLO Definitions
| Service | SLI | SLO Target | Measurement Window | Error Budget |
|---------|-----|------------|-------------------|-------------|
| API Gateway | Availability (2xx / total) | 99.9% | 30 days | 43.2 min/month |
| Checkout | Latency p99 < 500ms | 99.5% | 30 days | 3.6 hr/month |

### Instrumentation Plan
| Signal | Tool | Export Strategy | Retention |
|--------|------|----------------|-----------|
| Traces | OTel SDK + Jaeger | Collector with tail sampling | 7 days hot, 30 days warm |
| Metrics | OTel SDK + Prometheus | Direct scrape + remote write | 90 days |
| Logs | Structured JSON + Loki | Promtail agent | 30 days hot, 90 days cold |

### Alerting Strategy
| Signal | Condition | Severity | Routing | Runbook |
|--------|-----------|----------|---------|---------|
| Error budget burn | > 5% consumed in 1 hour | Critical | PagerDuty on-call | /runbooks/error-budget.md |

### Design Recommendations
| # | Area | Recommendation | Priority |
|---|------|----------------|----------|
| 1 | Instrumentation | Adopt OTel SDK with auto-instrumentation | High |
| 2 | SLOs | Define availability and latency SLOs for all user-facing services | Critical |

### Observability Design Checklist
- [ ] OTel SDK and auto-instrumentation selected for all languages
- [ ] SLIs and SLOs defined for critical user paths
- [ ] Structured logging format standardized across services
- [ ] Trace context propagation configured across service boundaries
- [ ] Alerting strategy designed with escalation path
- [ ] Dashboard plan covering golden signals and service overview
- [ ] Cost and cardinality budget established
- [ ] Pipeline monitoring strategy defined (if applicable)
- [ ] Model monitoring strategy defined (if applicable)
```

#### Audit mode report

Present concrete findings with fix status:

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
| 1 | Critical | Phase 0 | src/api.py:42 | print() used instead of structured logging | Fixed |
| 2 | High | Phase 5 | src/service.py:18 | HTTP call without trace context propagation | Fixed |

> **Schema note:** The base columns (#, Severity, Phase, File:Line, Description, Status) are shared across all audit skills. Other skills add domain-specific columns (e.g., CWE for security-audit, Framework for documentation-audit).

### SLI/SLO Assessment
| Service | SLIs Defined | SLOs Documented | Error Budget Tracked | Gap |
|---------|-------------|----------------|---------------------|-----|
| API | Yes | No | No | Define SLO targets and error budget policy |

### Pipeline Observability (if applicable)
| Pipeline | Execution Metrics | Freshness Monitoring | Quality Gates | Gap |
|----------|------------------|---------------------|---------------|-----|

### ML Model Observability (if applicable)
| Model | Version Tracked | Drift Detection | Performance Monitored | Gap |
|-------|----------------|----------------|----------------------|-----|

### Tier Coverage Matrix
| Phase | Standard | Enterprise |
|-------|----------|------------|
| Phase 0: Anti-Patterns | [X patterns scanned / Y findings] | [Linting: configured/not configured] |
| Phase 2: Instrumentation | [X/8 checks passed] | [APM platform: configured/not configured] |
| Phase 3: Logging | [X/10 checks passed] | [Log platform: configured/not configured] |
| Phase 4: Metrics & SLOs | [X/10 checks passed] | [Metrics platform: configured/not configured] |
| Phase 5: Tracing | [X/10 checks passed] | [Tracing platform: configured/not configured] |
| Phase 6: Pipelines | [X/10 checks passed] | [Data platform: configured/not configured] |
| Phase 7: ML Models | [X/10 checks passed] | [ML platform: configured/not configured] |
| Phase 8: Alerting | [X/10 checks passed] | [Incident platform: configured/not configured] |
| Phase 9: Dashboards | [X/10 checks passed] | [Dashboard platform: configured/not configured] |
| Phase 10: Health Checks | [X/10 checks passed] | [Synthetic monitoring: configured/not configured] |
| Phase 11: Cost | [X/10 checks passed] | [Cost platform: configured/not configured] |

### Observability Maturity Rating
- **Standard tier**: X/Y checks passed (Z% coverage)
- **Enterprise tier**: X/Y controls configured (Z% coverage)
- **Overall**: [Observable / Partially Observable / Significant Blind Spots / Flying Blind]

### Ready for production: Yes / No (with blockers)
```

---

## Important rules

- **Fix as you go.** Don't just report — remediate. Fix Critical and High issues during the audit.
- **Evidence-based claims.** Every finding must include file path, line number, or specific evidence. Never say "probably missing monitoring."
- **No assumptions.** Read the actual code, configs, and infrastructure files. Don't assume observability exists because a framework is used.
- **Verify fixes.** After fixing an observability gap, re-run the check that found it to confirm the fix works.
- **Respect existing patterns.** If the project has established telemetry patterns, extend them rather than introducing new ones.
- **Scope awareness.** Don't flag managed-service built-in observability as a finding (e.g., CloudWatch metrics auto-collected by AWS Lambda).
- **Phase 7 is conditional.** Only execute the ML/Model Observability phase if ML models or analytical models are detected in the project.
- **Two-tier awareness.** Standard tier checks are always actionable — fix issues found. Enterprise tier items serve as a professional reference — document which are applicable and which are configured, but don't block releases on Enterprise items the team hasn't adopted yet.
- **Prioritize.** Fix Critical and High findings. Track Medium and Low in the backlog. Don't let perfect be the enemy of observable.
