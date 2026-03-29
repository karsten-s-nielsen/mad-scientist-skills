# Pipeline & Data Observability Reference

End-to-end observability guide for data pipelines covering health signals, orchestrator-specific monitoring, data quality gates, freshness tracking, volume anomaly detection, and pipeline tracing with OpenTelemetry.

## Purpose

Answer: "Can we detect pipeline failures, data quality issues, and freshness problems before they impact downstream consumers?"

## Checklist

Before auditing, identify:

- [ ] Which orchestrator is used (Airflow, Dagster, Prefect, dbt Cloud, cron)
- [ ] Which data stores are involved (warehouse, lake, object storage, streaming)
- [ ] Which data testing framework is in place (dbt tests, Great Expectations, Soda, custom)
- [ ] What alerting and notification channels exist (PagerDuty, Slack, email, OpsGenie)
- [ ] Whether an observability backend is deployed (Datadog, Grafana, New Relic, OpenTelemetry Collector)
- [ ] What SLAs or SLOs exist for data freshness and pipeline completion

---

## Pipeline Health Signals

| Signal | What to measure | Why it matters | Alert threshold example |
|--------|----------------|----------------|------------------------|
| Execution duration | Wall-clock time per pipeline run | Detect regressions, resource contention | >2x median of last 14 days |
| Success/failure rate | Pass/fail ratio over rolling window | Spot reliability degradation | <95% over 24h |
| Row counts per stage | Rows read, transformed, written at each step | Catch silent data loss or duplication | >30% deviation from baseline |
| Data freshness | Time since last successful load per table | Detect stale data before consumers notice | Exceeds SLA (e.g., >2h for hourly) |
| Schema drift | Column additions, removals, type changes | Prevent downstream breakage | Any unexpected change |
| Resource usage | CPU, memory, I/O, query slots consumed | Capacity planning, cost control | >80% sustained utilization |
| Retry count | Number of automatic retries per task | Flaky tasks masking real failures | >2 retries per run |
| Queue/backlog depth | Pending runs or tasks waiting to execute | Detect scheduling bottlenecks | Growing backlog over 3+ intervals |

---

## dbt Observability

### Parsing `run_results.json`

After every `dbt run` or `dbt test`, dbt writes results to `target/run_results.json`. Parse this file to extract per-model execution time, test pass/fail counts, and failure details.

```python
import json
from pathlib import Path

def parse_run_results(path="target/run_results.json"):
    data = json.loads(Path(path).read_text())
    models, tests_passed, tests_failed, failures = [], 0, 0, []
    for r in data["results"]:
        node = r["unique_id"]
        status = r["status"]
        elapsed = r.get("execution_time", 0)
        if node.startswith("model."):
            models.append({"model": node, "status": status, "seconds": round(elapsed, 2)})
        elif node.startswith("test."):
            if status == "pass":
                tests_passed += 1
            else:
                tests_failed += 1
                failures.append({"test": node, "status": status, "message": r.get("message", "")})
    print(f"Models: {len(models)} | Tests passed: {tests_passed} | Tests failed: {tests_failed}")
    for m in sorted(models, key=lambda x: x["seconds"], reverse=True)[:5]:
        print(f"  {m['model']}: {m['seconds']}s ({m['status']})")
    for f in failures:
        print(f"  FAIL: {f['test']} — {f['message'][:120]}")
    return {"models": models, "tests_passed": tests_passed, "tests_failed": tests_failed, "failures": failures}
```

### Source Freshness Configuration

Define freshness thresholds in `sources.yml` so `dbt source freshness` can detect stale upstream data before running transformations.

```yaml
# models/staging/sources.yml
version: 2
sources:
  - name: raw_payments
    database: analytics
    schema: raw
    loaded_at_field: _loaded_at
    freshness:
      warn_after: {count: 2, period: hour}
      error_after: {count: 6, period: hour}
    tables:
      - name: transactions
        freshness:
          warn_after: {count: 1, period: hour}
          error_after: {count: 3, period: hour}
      - name: refunds
      - name: customers
        freshness:
          warn_after: {count: 12, period: hour}
          error_after: {count: 24, period: hour}
```

Run freshness checks as a CI gate:

```bash
dbt source freshness --select source:raw_payments
# Exit code 1 if any source exceeds error_after threshold
```

### dbt Test Result Tracking

Track test results over time to detect flaky tests and quality regressions:

| Pattern | How | Purpose |
|---------|-----|---------|
| Store test results | `dbt test --store-failures` | Write failing rows to the warehouse for investigation |
| Severity levels | `severity: warn` vs `severity: error` | Non-blocking vs blocking failures |
| Custom generic tests | `tests/generic/` directory | Reusable domain-specific validations |
| Test selection | `dbt test --select tag:critical` | Run critical tests first, fast feedback |
| CI integration | Fail PR if `dbt test` exits non-zero | Prevent merging data quality regressions |

### dbt Fusion Native OTLP (Preview)

dbt Fusion (the Rust-based dbt runtime) includes native OpenTelemetry trace export. When available, this will emit spans for each model and test execution without custom instrumentation. This is in preview as of March 2026 — track the dbt Fusion release notes for GA availability. Consider it a future option rather than a production-ready solution today.

---

## Airflow Observability

### Task-Level Callbacks

Use `on_failure_callback` and `on_success_callback` to send structured alerts on task completion:

```python
from airflow.models import TaskInstance

def on_failure_alert(context: dict):
    ti: TaskInstance = context["task_instance"]
    dag_id = ti.dag_id
    task_id = ti.task_id
    execution_date = context["execution_date"]
    exception = context.get("exception", "unknown")
    # Send to Slack, PagerDuty, or custom webhook
    payload = {
        "dag": dag_id,
        "task": task_id,
        "execution_date": str(execution_date),
        "error": str(exception)[:500],
        "log_url": ti.log_url,
    }
    send_alert(payload)  # your alerting function

# Apply at DAG level (inherited by all tasks)
with DAG(
    "my_pipeline",
    default_args={"on_failure_callback": on_failure_alert},
    # ...
) as dag:
    pass
```

### DAG and Task Instance Metrics

| Metric | Source | What to monitor |
|--------|--------|-----------------|
| DAG run duration | `dag_run` table / StatsD | Trend over time, detect regressions |
| Task duration | `task_instance` table / StatsD | Per-task execution time |
| Task retries | `task_instance.try_number` | Flaky tasks retrying frequently |
| SLA misses | `sla_miss` table | Tasks exceeding defined SLAs |
| Pool slot usage | Pool configuration | Detect resource contention |
| Scheduler heartbeat | `scheduler_heartbeat` | Scheduler health |
| DAG bag parse time | StatsD `dag_processing.total_parse_time` | Slow parsing blocks scheduling |

### SLA Misses

```python
with DAG("my_pipeline", default_args={"sla": timedelta(hours=2)}):
    # Tasks that exceed 2 hours from the DAG run's execution_date
    # will generate SLA miss records
    extract = PythonOperator(task_id="extract", python_callable=extract_fn, sla=timedelta(minutes=30))
```

### Airflow + OpenTelemetry

Airflow 2.7+ supports native OpenTelemetry integration:

```ini
# airflow.cfg
[traces]
otel_on = True
otel_host = otel-collector
otel_port = 4318
otel_ssl_active = False
```

This emits spans per task instance, enabling distributed tracing across DAG runs.

---

## Dagster / Prefect Observability

### Dagster

| Feature | What it provides | Observability value |
|---------|-----------------|---------------------|
| Asset materialization events | Timestamp + metadata per asset update | Data freshness, lineage |
| Asset observations | Check external state without materializing | Freshness without re-running |
| Run status sensors | React to run success/failure programmatically | Custom alerting, downstream triggers |
| Built-in Dagster UI | Timeline, asset graph, run history | Visual debugging |
| Dagster+ (Cloud) | Alerts, insights, cost tracking | Managed observability |

```python
from dagster import asset, AssetObservation, Output

@asset
def orders(context):
    df = load_orders()
    context.log_event(
        AssetObservation(
            asset_key="orders",
            metadata={"row_count": len(df), "max_order_date": str(df["order_date"].max())},
        )
    )
    return Output(df, metadata={"row_count": len(df)})
```

### Prefect

| Feature | What it provides | Observability value |
|---------|-----------------|---------------------|
| Flow run states | Pending, Running, Completed, Failed, Cancelled | Lifecycle tracking |
| Task run states | Same granularity at task level | Pinpoint failures |
| Automations | Trigger actions on state changes | Alerting, remediation |
| Artifacts | Publish markdown, tables, links from flows | Rich run metadata |
| Events | Structured event stream for all activity | Audit trail, custom dashboards |

```python
from prefect import flow, task
from prefect.artifacts import create_markdown_artifact

@task
def validate_output(df):
    row_count = len(df)
    create_markdown_artifact(
        key="validation-report",
        markdown=f"## Validation\n- Row count: {row_count}\n- Null rate: {df.isnull().mean().max():.2%}",
    )
    if row_count == 0:
        raise ValueError("Zero rows produced — aborting pipeline")
```

### Sensor-Based Health Checks

Both Dagster and Prefect support sensor patterns that poll external systems and trigger pipelines or alerts:

```python
# Dagster sensor example
from dagster import sensor, RunRequest, SkipReason

@sensor(job=my_job, minimum_interval_seconds=300)
def source_freshness_sensor(context):
    last_modified = check_source_table_freshness("raw.events")
    if last_modified > timedelta(hours=1):
        return SkipReason(f"Source data is {last_modified} old — waiting for refresh")
    return RunRequest(run_key=f"events-{last_modified}")
```

---

## Data Quality Gates

### Pre/Post-Load Validation Patterns

| Stage | Validation | Action on failure |
|-------|-----------|-------------------|
| Pre-load (source) | Schema matches expected, file is non-empty, freshness OK | Skip load, alert |
| Mid-pipeline | Row counts within bounds, no unexpected nulls | Halt pipeline, alert |
| Post-load (target) | Primary keys unique, referential integrity intact, row count delta OK | Quarantine bad data, alert |
| Post-publish | Dashboard queries return data, API responses valid | Rollback, alert |

### Great Expectations Integration

```python
import great_expectations as gx

context = gx.get_context()
batch = context.sources.pandas_default.read_csv("output.csv")
results = batch.validate(
    expectation_suite="orders_suite",
    # Expectations defined in suite:
    # - expect_column_values_to_not_be_null("order_id")
    # - expect_column_values_to_be_unique("order_id")
    # - expect_column_values_to_be_in_set("status", ["pending", "shipped", "delivered", "cancelled"])
    # - expect_table_row_count_to_be_between(min_value=1000, max_value=500000)
)
if not results.success:
    raise RuntimeError(f"Data quality check failed: {results.statistics}")
```

### dbt Test Patterns

| Test type | YAML example | What it catches |
|-----------|-------------|-----------------|
| `not_null` | `- not_null: {column_name: order_id}` | Missing required values |
| `unique` | `- unique: {column_name: order_id}` | Duplicate records |
| `accepted_values` | `- accepted_values: {column_name: status, values: ['active','inactive']}` | Invalid enum values |
| `relationships` | `- relationships: {to: ref('customers'), field: customer_id}` | Broken foreign keys |
| Custom SQL | `tests/assert_positive_revenue.sql` | Domain-specific invariants |

Custom SQL test example:

```sql
-- tests/assert_no_negative_revenue.sql
-- This test fails if any rows are returned
select order_id, revenue
from {{ ref('fct_orders') }}
where revenue < 0
```

---

## Dead Letter Pattern

Quarantine failed records instead of dropping them silently or halting the entire pipeline.

| Component | Purpose | Implementation |
|-----------|---------|----------------|
| Dead letter table/queue | Store records that failed validation or transformation | Dedicated table with error metadata |
| Error metadata | Understand why the record failed | Error reason, timestamp, source record ID, pipeline run ID |
| Monitoring | Detect quality degradation | Alert when dead letter rate exceeds threshold |
| Reprocessing | Fix and replay failed records | Periodic job to retry or manual review |

```sql
-- Dead letter table schema
CREATE TABLE dead_letter_orders (
    dl_id           BIGINT GENERATED ALWAYS AS IDENTITY,
    source_record_id TEXT,
    error_reason    TEXT,
    failed_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    pipeline_run_id TEXT,
    raw_payload     JSONB,
    reprocessed     BOOLEAN DEFAULT FALSE
);

-- Insert failed records during transformation
INSERT INTO dead_letter_orders (source_record_id, error_reason, pipeline_run_id, raw_payload)
SELECT
    order_id,
    CASE
        WHEN amount IS NULL THEN 'null_amount'
        WHEN amount < 0 THEN 'negative_amount'
        WHEN customer_id IS NULL THEN 'null_customer'
    END,
    '{{ run_id }}',
    to_jsonb(t.*)
FROM staging_orders t
WHERE amount IS NULL OR amount < 0 OR customer_id IS NULL;
```

**Dead letter volume alerting:**

```sql
-- Alert query: dead letter rate over last hour
SELECT
    COUNT(*) AS dead_letter_count,
    COUNT(*)::FLOAT / NULLIF((SELECT COUNT(*) FROM staging_orders WHERE loaded_at > NOW() - INTERVAL '1 hour'), 0) AS dead_letter_rate
FROM dead_letter_orders
WHERE failed_at > NOW() - INTERVAL '1 hour';
-- Alert if dead_letter_rate > 0.05 (5%)
```

---

## Data Freshness Monitoring

### Staleness Thresholds

Define freshness SLIs per table based on how frequently the source updates and how tolerant consumers are of stale data:

| Table | Update frequency | Warn threshold | Error threshold | Consumer impact |
|-------|-----------------|---------------|-----------------|-----------------|
| `fct_orders` | Hourly | 2 hours | 4 hours | Dashboards show stale revenue |
| `dim_customers` | Daily | 26 hours | 48 hours | Customer segments outdated |
| `fct_events` | Real-time/micro-batch | 15 minutes | 1 hour | Alerting and anomaly detection delayed |
| `dim_products` | Weekly | 8 days | 14 days | Product catalog stale |

### Freshness Check Query

```sql
-- Generic freshness check: find tables that exceed their SLA
WITH freshness_sla AS (
    SELECT 'fct_orders'    AS table_name, INTERVAL '4 hour'  AS max_staleness
    UNION ALL
    SELECT 'dim_customers' AS table_name, INTERVAL '48 hour' AS max_staleness
    UNION ALL
    SELECT 'fct_events'    AS table_name, INTERVAL '1 hour'  AS max_staleness
),
actual_freshness AS (
    SELECT 'fct_orders'    AS table_name, MAX(updated_at) AS last_updated FROM fct_orders
    UNION ALL
    SELECT 'dim_customers' AS table_name, MAX(updated_at) AS last_updated FROM dim_customers
    UNION ALL
    SELECT 'fct_events'    AS table_name, MAX(event_time) AS last_updated FROM fct_events
)
SELECT
    s.table_name,
    a.last_updated,
    NOW() - a.last_updated AS staleness,
    s.max_staleness,
    CASE WHEN NOW() - a.last_updated > s.max_staleness THEN 'STALE' ELSE 'OK' END AS status
FROM freshness_sla s
JOIN actual_freshness a ON s.table_name = a.table_name
ORDER BY staleness DESC;
```

### Freshness SLIs

Track freshness as an SLI (Service Level Indicator) and set SLOs:

- **SLI:** Percentage of checks where `staleness < max_staleness`
- **SLO:** 99.5% of freshness checks pass over a 30-day window
- **Error budget:** ~3.6 hours of allowed staleness violations per month

---

## Data Volume Anomaly Detection

### Statistical Baseline

Compare current row counts against a rolling baseline to detect unexpected drops, spikes, or zero-row loads:

```python
import json
from statistics import mean, stdev

def check_volume_anomaly(current_count: int, historical_counts: list[int], z_threshold: float = 3.0):
    """Flag anomalies using Z-score against historical baseline."""
    if len(historical_counts) < 7:
        print("Not enough history for anomaly detection — skipping")
        return False
    if current_count == 0:
        print("ALERT: Zero rows detected — pipeline may have produced no output")
        return True
    mu = mean(historical_counts)
    sigma = stdev(historical_counts)
    if sigma == 0:
        return current_count != mu
    z_score = (current_count - mu) / sigma
    is_anomaly = abs(z_score) > z_threshold
    if is_anomaly:
        direction = "above" if z_score > 0 else "below"
        print(f"ALERT: Row count {current_count} is {abs(z_score):.1f} std devs {direction} mean ({mu:.0f})")
    return is_anomaly
```

### Alerting Strategies

| Condition | Detection method | Severity |
|-----------|-----------------|----------|
| Zero rows produced | `count == 0` | Critical |
| Row count drop >50% | Percentage deviation from prior run | High |
| Row count Z-score >3 | Statistical outlier vs rolling 14-day baseline | High |
| Row count Z-score >2 | Moderate deviation | Warning |
| Monotonically increasing table shrinks | Current max(id) < previous max(id) | High |

---

## Idempotency Verification

Pipelines must be safe to re-run without producing duplicates or corrupting state.

### Re-Run Safety Patterns

| Pattern | How it works | When to use |
|---------|-------------|-------------|
| `MERGE` / upsert | Match on key, update existing, insert new | Slowly changing dimensions, event dedup |
| `replaceWhere` (Delta/Spark) | Overwrite only the affected partition | Partition-scoped incremental loads |
| `DELETE + INSERT` | Delete target partition, then insert | Simple partition replacement |
| `INSERT OVERWRITE` | Atomic partition replacement | Hive-style partitioned tables |
| Dedup on write | `SELECT DISTINCT` or `QUALIFY ROW_NUMBER()` before insert | Any pattern — defense in depth |

### Detecting Duplicates

```sql
-- Find duplicate primary keys in a target table
SELECT order_id, COUNT(*) AS occurrences
FROM fct_orders
GROUP BY order_id
HAVING COUNT(*) > 1
ORDER BY occurrences DESC
LIMIT 20;

-- Detect duplicates introduced by a specific pipeline run
SELECT order_id, COUNT(*) AS occurrences
FROM fct_orders
WHERE _loaded_at >= '{{ run_start }}'
GROUP BY order_id
HAVING COUNT(*) > 1;
```

### Idempotency Verification Query

```sql
-- Run the pipeline twice, then compare: counts should be identical
-- Before re-run
SELECT COUNT(*) AS row_count, SUM(amount) AS total_amount FROM fct_orders WHERE order_date = '2025-01-15';
-- After re-run (should match exactly)
SELECT COUNT(*) AS row_count, SUM(amount) AS total_amount FROM fct_orders WHERE order_date = '2025-01-15';
```

---

## Pipeline-as-OTel-Traces

Model each pipeline run as a single distributed trace with child spans per task or stage. This gives end-to-end visibility into pipeline execution in any OpenTelemetry-compatible backend (Jaeger, Tempo, Datadog, Honeycomb).

### Concept

```
Pipeline Run (parent span)
├── Extract: source_a (child span, 45s)
├── Extract: source_b (child span, 30s)
├── Transform: staging_orders (child span, 120s)
│   ├── dbt model: stg_orders (child span, 60s)
│   └── dbt model: stg_payments (child span, 55s)
├── Test: data_quality_checks (child span, 15s)
│   ├── test: unique_order_id (child span, 3s)
│   └── test: not_null_amount (child span, 2s)
└── Load: publish_to_warehouse (child span, 90s)
```

### Implementation

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

# Setup (once at pipeline entry point)
provider = TracerProvider()
provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter(endpoint="otel-collector:4317")))
trace.set_tracer_provider(provider)
tracer = trace.get_tracer("data-pipeline")

def run_pipeline():
    with tracer.start_as_current_span("pipeline.daily_orders") as pipeline_span:
        pipeline_span.set_attribute("pipeline.run_id", run_id)
        pipeline_span.set_attribute("pipeline.trigger", "scheduled")

        with tracer.start_as_current_span("extract.source_a") as extract_span:
            rows = extract_source_a()
            extract_span.set_attribute("extract.row_count", rows)

        with tracer.start_as_current_span("transform.staging") as transform_span:
            result = run_dbt_models()
            transform_span.set_attribute("transform.models_run", result.model_count)
            transform_span.set_attribute("transform.tests_passed", result.tests_passed)

        with tracer.start_as_current_span("load.publish") as load_span:
            written = publish_to_warehouse()
            load_span.set_attribute("load.rows_written", written)
```

### Span Attributes Convention

Use consistent attribute names across pipelines for queryability:

| Attribute | Example value | Purpose |
|-----------|--------------|---------|
| `pipeline.name` | `daily_orders` | Identify the pipeline |
| `pipeline.run_id` | `run_2025-01-15T08:00:00` | Correlate all spans in one run |
| `pipeline.trigger` | `scheduled` / `manual` / `sensor` | How the run was initiated |
| `stage.type` | `extract` / `transform` / `test` / `load` | Pipeline phase |
| `stage.row_count` | `150000` | Rows processed in this stage |
| `stage.status` | `success` / `failed` / `skipped` | Outcome |
| `data.source` | `postgres.public.orders` | Source system and table |
| `data.target` | `snowflake.analytics.fct_orders` | Destination table |

---

## Best practices

- Instrument pipelines with health signals from day one — retrofitting observability is far more expensive
- Set freshness SLOs per table based on actual consumer requirements, not arbitrary thresholds
- Use dead letter tables instead of silently dropping bad records — you need to know what you are losing
- Run data quality tests as pipeline stages, not as separate out-of-band processes
- Track test results over time to detect flaky tests and quality regressions
- Model pipeline runs as OTel traces so you can query execution across stages in a single view
- Alert on trends (increasing duration, growing dead letter rate) not just hard failures
- Make all pipelines idempotent — re-runs should be safe by default
- Store row counts and execution metadata in a metrics table for historical comparison
- Use source freshness checks before running transformations to fail fast on stale inputs
- Correlate pipeline failures with infrastructure metrics (CPU, memory, query queue depth)

## Anti-patterns

- Relying solely on pipeline success/failure status without checking data quality
- Monitoring only the final output table while ignoring intermediate stages
- Setting alerting thresholds so sensitive that alert fatigue causes real issues to be ignored
- Using `SELECT COUNT(*)` as the only data quality check — it catches volume problems but misses content issues
- Running data quality checks only in production, not in CI against development builds
- Treating zero-row results as successful when the pipeline "completed without errors"
- Building custom monitoring infrastructure instead of leveraging orchestrator-native signals
- Skipping idempotency because "we only run the pipeline once" — retries and backfills are inevitable
- Logging errors to files on ephemeral compute without forwarding to a persistent observability backend
- Ignoring schema drift until a downstream dashboard breaks
