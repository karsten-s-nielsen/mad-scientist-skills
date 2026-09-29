# Algorithm & Data Structure Efficiency Reference

Actionable reference for Phase 2 of the optimization audit. Covers Big-O analysis, data structure selection, per-language profiling tools, hot path identification, common algorithmic improvements, vectorization patterns, and a systematic complexity analysis checklist.

## Purpose

Answer: "Are the algorithms and data structures in this codebase appropriate for the problem size and access patterns?"

## Checklist

Before auditing, identify:

- [ ] What the expected input sizes are (current and projected growth)
- [ ] Which code paths are hot paths (high frequency or user-facing latency)
- [ ] Whether profiling data exists (CPU profiles, flame graphs)
- [ ] What data structures are used for core collections (lists, maps, sets, trees)
- [ ] Whether any known performance complaints or SLA violations exist
- [ ] What language-specific profiling tools are available in the project

---

## Big-O Quick Reference

| Complexity | Name | Example Operations | Acceptable When |
|------------|------|-------------------|-----------------|
| O(1) | Constant | Hash map lookup, array index access, stack push/pop | Always acceptable. Ideal for hot paths. |
| O(log n) | Logarithmic | Binary search, balanced BST lookup, heap insert/extract | Acceptable for large datasets. Scales to billions. |
| O(n) | Linear | Array scan, linked list traversal, single-pass aggregation | Acceptable for most workloads. Watch for hidden constants and repeated calls. |
| O(n log n) | Linearithmic | Merge sort, heap sort, efficient comparison-based sorting | Acceptable for sorting up to millions of elements. |
| O(n^2) | Quadratic | Nested loops over same collection, bubble sort, naive string matching | Only acceptable for small n (<1000). Red flag on hot paths. |
| O(2^n) | Exponential | Brute-force subset enumeration, naive recursive Fibonacci | Almost never acceptable except for n < 20. Use DP or memoization. |
| O(n!) | Factorial | Brute-force permutations, naive TSP | Only acceptable for n < 12. Always seek heuristics. |

### Scale Reference

| n | O(n) | O(n log n) | O(n^2) | O(2^n) |
|---|------|-----------|--------|--------|
| 100 | 100 | 664 | 10,000 | 1.27 x 10^30 |
| 1,000 | 1,000 | 9,966 | 1,000,000 | Infeasible |
| 10,000 | 10,000 | 132,877 | 100,000,000 | -- |
| 1,000,000 | 1,000,000 | 19,931,569 | 10^12 (hours) | -- |

**Rule of thumb:** If n can exceed 10,000 in production, O(n^2) is a performance bug. If n can exceed 1,000, O(n^2) on a hot path is a code smell.

---

## Data Structure Selection Guide

| Data Structure | Best For | Avoid When | Key Operations |
|---------------|----------|------------|----------------|
| **Array / List** | Sequential access, index-based lookup, iteration | Frequent mid-insertion; membership testing on large collections | Index: O(1), Append: O(1)*, Search: O(n) |
| **Hash Map / Dict** | Key-value lookup, counting, grouping, deduplication | Ordered iteration required; very small datasets (<10) | Get/Set/Delete: O(1) avg |
| **Hash Set** | Membership testing, deduplication, intersection/union | Need sorted iteration | Add/Remove/Contains: O(1) avg |
| **Heap / Priority Queue** | Top-K extraction, scheduling, median finding | Random access by key; full sorted iteration | Insert: O(log n), Extract min/max: O(log n), Peek: O(1) |
| **Balanced BST / TreeMap** | Sorted iteration, range queries, ordered key-value | Only need lookup (hash map is faster) | Get/Set/Delete: O(log n), Range: O(log n + k) |
| **Trie** | Prefix search, autocomplete, IP routing | General key-value storage | Insert/Search: O(m) where m = key length |
| **Graph (adj. list)** | Relationships, shortest path, dependency resolution | Simple parent-child (use tree) | Add edge: O(1), BFS/DFS: O(V + E) |
| **Queue / Deque** | FIFO processing, BFS, sliding window | Random access needed | Enqueue/Dequeue: O(1) |

### Language-Specific Choices

| Need | Python | JS/TS | Go | Java | Rust |
|------|--------|-------|-----|------|------|
| Hash map | `dict` | `Map` / `{}` | `map[K]V` | `HashMap<K,V>` | `HashMap<K,V>` |
| Hash set | `set` | `Set` | `map[K]struct{}` | `HashSet<T>` | `HashSet<T>` |
| Sorted map | `SortedDict` (sortedcontainers) | -- | -- | `TreeMap<K,V>` | `BTreeMap<K,V>` |
| Heap | `heapq` | -- (manual/lib) | `container/heap` | `PriorityQueue<T>` | `BinaryHeap<T>` |
| Thread-safe map | `dict` + lock | -- | `sync.Map` | `ConcurrentHashMap` | `DashMap` |

---

## Per-Language Profiling Tools

### Python

| Tool | Purpose | Quick Start |
|------|---------|-------------|
| **py-spy** | Sampling profiler, flame graphs | `pip install py-spy && py-spy record -o profile.svg -- python app.py` |
| **scalene** | CPU + memory + GPU, line-level | `pip install scalene && scalene --html --outfile profile.html app.py` |
| **cProfile** | Built-in deterministic profiler | `python -m cProfile -s cumulative app.py` |
| **line_profiler** | Line-by-line CPU time | `pip install line_profiler && kernprof -l -v app.py` (decorate with `@profile`) |
| **memray** | High-performance memory profiler | `pip install memray && memray run app.py && memray flamegraph memray-*.bin` |

```python
# cProfile programmatic usage
import cProfile, pstats
profiler = cProfile.Profile()
profiler.enable()
# ... code to profile ...
profiler.disable()
pstats.Stats(profiler).sort_stats("cumulative").print_stats(20)
```

### JavaScript / TypeScript

| Tool | Purpose | Quick Start |
|------|---------|-------------|
| **clinic.js** | Suite: flame, bubbleprof, doctor | `npm i -g clinic && clinic flame -- node server.js` |
| **0x** | Flame graph generation | `npm i -g 0x && 0x server.js` |
| **Chrome DevTools** | Performance tab, heap snapshots | F12 > Performance > Record > Analyze flame chart |
| **Node --prof** | V8 profiling log | `node --prof app.js && node --prof-process isolate-*.log` |

### Go

| Tool | Purpose | Quick Start |
|------|---------|-------------|
| **pprof** | CPU, memory, goroutine profiling | Import `net/http/pprof`, then `go tool pprof http://localhost:6060/debug/pprof/profile?seconds=30` |
| **benchstat** | Statistical benchmark comparison | `go test -bench=. -count=10 > old.txt` (change code) `go test -bench=. -count=10 > new.txt && benchstat old.txt new.txt` |

```go
// Enable pprof HTTP endpoint
import _ "net/http/pprof"
go func() { http.ListenAndServe("localhost:6060", nil) }()

// pprof commands: top10, web (flame graph), list <func>
```

### Java

| Tool | Purpose | Quick Start |
|------|---------|-------------|
| **async-profiler** | Low-overhead sampling | `./asprof -d 30 -f profile.html <pid>` |
| **JFR** | Built-in since JDK 11 | `java -XX:StartFlightRecording=duration=60s,filename=rec.jfr -jar app.jar` |
| **VisualVM** | Visual profiling and heap analysis | `visualvm` -- connect to local/remote JVM |

```bash
# async-profiler: CPU, allocation, and wall-clock modes
./asprof -d 30 -f flamegraph.svg <pid>       # CPU
./asprof -e alloc -d 30 -f alloc.html <pid>  # Allocations
./asprof -e wall -d 30 -f wall.html <pid>    # Wall-clock (includes I/O)
```

### Rust

| Tool | Purpose | Quick Start |
|------|---------|-------------|
| **cargo flamegraph** | Flame graph generation | `cargo install flamegraph && cargo flamegraph --bin my_binary` |
| **perf** | Hardware performance counters | `perf record --call-graph dwarf -- ./binary && perf report` |
| **criterion** | Statistical benchmarking | Add `criterion` dev-dependency, create bench file |

```rust
// criterion benchmark example
use criterion::{criterion_group, criterion_main, Criterion};

fn bench_lookup(c: &mut Criterion) {
    let data = prepare_data();
    c.bench_function("lookup", |b| b.iter(|| lookup(&data, "key")));
}
criterion_group!(benches, bench_lookup);
criterion_main!(benches);
```

### .NET

| Tool | Purpose | Quick Start |
|------|---------|-------------|
| **dotnet-trace** | Cross-platform tracing | `dotnet tool install -g dotnet-trace && dotnet-trace collect --process-id <pid>` |
| **BenchmarkDotNet** | Micro-benchmarking framework | Add NuGet package, annotate with `[Benchmark]`, run in Release |

```csharp
// BenchmarkDotNet example
[MemoryDiagnoser]
public class Benchmarks
{
    [Benchmark(Baseline = true)]
    public int DictLookup() => _dict["key_5000"];

    [Benchmark]
    public int ListSearch() => _list.First(x => x.Key == "key_5000").Value;
}
```

---

## Hot Path Identification

The 80/20 rule: roughly 20% of code consumes 80% of CPU/memory. Finding that 20% is the first step.

### Methodology

1. **Profile under realistic load** -- use production-like data volumes and access patterns
2. **Capture a flame graph** -- use the tools above to generate SVG or interactive HTML
3. **Identify the widest bars** -- width = time (CPU) or count (allocations). Widest bars at the bottom are entry points; follow the widest path upward
4. **Confirm with line-level profiling** -- use line_profiler (Python), async-profiler (Java), or equivalent

### Flame Graph Patterns

| Visual Pattern | Meaning | Action |
|---------------|---------|--------|
| Wide plateau at top | Single function consuming most CPU | Optimize: better algorithm, caching, or batch I/O |
| Wide bar with many narrow children | Function called many times, small per-call cost | Reduce call count: batch, cache results |
| Deep narrow tower | Deep call stack, small total cost | Usually fine unless excessive abstraction |
| Wide bar labeled I/O function | I/O bound (network, disk, database) | Optimize query, add caching, or parallelize I/O |
| Wide bar labeled GC/malloc | Memory allocation pressure | Reduce allocations: reuse objects, pools, pre-allocate |

---

## Common Algorithmic Improvements

### 1. Nested Loop to Hash Join / Set Lookup

**BAD** -- O(n * m) nested loop:
```python
# Python: O(n * m) -- scans orders for every customer
matches = []
for customer in customers:
    for order in orders:
        if order["customer_id"] == customer["id"]:
            matches.append((customer, order))
```

**GOOD** -- O(n + m) hash join:
```python
# Python: O(n + m) -- build index, then look up
order_index = {}
for order in orders:
    order_index.setdefault(order["customer_id"], []).append(order)

matches = []
for customer in customers:
    for order in order_index.get(customer["id"], []):
        matches.append((customer, order))
```

**BAD** -- O(n * m) in JavaScript:
```javascript
// JavaScript: O(n * m)
const matches = [];
for (const customer of customers) {
    for (const order of orders) {
        if (order.customerId === customer.id) {
            matches.push({ customer, order });
        }
    }
}
```

**GOOD** -- O(n + m) with Map:
```javascript
// JavaScript: O(n + m)
const ordersByCustomer = new Map();
for (const order of orders) {
    if (!ordersByCustomer.has(order.customerId)) {
        ordersByCustomer.set(order.customerId, []);
    }
    ordersByCustomer.get(order.customerId).push(order);
}
const matches = [];
for (const customer of customers) {
    for (const order of ordersByCustomer.get(customer.id) ?? []) {
        matches.push({ customer, order });
    }
}
```

### 2. Linear Search to Set/Map Lookup

**BAD** -- O(n) per lookup:
```python
# Python: O(n) list scan per iteration
allowed_ids = [1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
for item in items:
    if item.id in allowed_ids:  # O(n) list scan each time
        process(item)
```

**GOOD** -- O(1) per lookup:
```python
# Python: O(1) set lookup per iteration
allowed_ids = {1, 2, 3, 5, 8, 13, 21, 34, 55, 89}
for item in items:
    if item.id in allowed_ids:  # O(1) set lookup
        process(item)
```

**BAD** -- O(n) in Go:
```go
// Go: O(n) linear scan per lookup
allowed := []string{"admin", "editor", "viewer"}
for _, user := range users {
    for _, role := range allowed {
        if user.Role == role { grant(user); break }
    }
}
```

**GOOD** -- O(1) in Go:
```go
// Go: O(1) map lookup
allowed := map[string]struct{}{"admin": {}, "editor": {}, "viewer": {}}
for _, user := range users {
    if _, ok := allowed[user.Role]; ok { grant(user) }
}
```

### 3. Full Sort to Heap for Top-K

**BAD** -- O(n log n) to find top 10:
```python
# Python: sorts entire list just to get top 10
top_10 = sorted(scores, reverse=True)[:10]
```

**GOOD** -- O(n log k) with heap:
```python
# Python: O(n log k) where k=10
import heapq
top_10 = heapq.nlargest(10, scores)
```

**BAD** -- O(n log n) in Java:
```java
// Java: sorts entire list
Collections.sort(scores, Comparator.reverseOrder());
List<Integer> top10 = scores.subList(0, 10);
```

**GOOD** -- O(n log k) in Java:
```java
// Java: min-heap of size k
PriorityQueue<Integer> heap = new PriorityQueue<>(10);
for (int score : scores) {
    heap.offer(score);
    if (heap.size() > 10) heap.poll();
}
```

### 4. String Concatenation in Loop to Builder/Join

**BAD** -- O(n^2) string concatenation:
```python
result = ""
for item in items:
    result += str(item) + ","  # New string allocated each iteration
```

**GOOD** -- O(n) with join:
```python
result = ",".join(str(item) for item in items)
```

**BAD** -- O(n^2) in Java:
```java
String result = "";
for (String item : items) {
    result += item + ",";  // Immutable String forces copy each time
}
```

**GOOD** -- O(n) with StringBuilder:
```java
StringBuilder sb = new StringBuilder();
for (String item : items) {
    if (sb.length() > 0) sb.append(",");
    sb.append(item);
}
String result = sb.toString();
```

**BAD** -- O(n^2) in Go:
```go
result := ""
for _, item := range items {
    result += item + ","  // Strings are immutable, each += copies
}
```

**GOOD** -- O(n) with strings.Builder:
```go
var b strings.Builder
for i, item := range items {
    if i > 0 { b.WriteString(",") }
    b.WriteString(item)
}
result := b.String()
```

### 5. DataFrame Filter Inside Loop to Pre-Built Index

The most dangerous hidden O(n²) in data science code. It doesn't look like a nested loop, but `df[df["col"] == val]` is a full O(n) scan, and calling it m times inside a loop creates O(n×m) behavior. On large DataFrames (tracking data, event logs, time series), this turns seconds into hours.

**Why it's dangerous:** Unit tests pass instantly because synthetic fixtures have ~100 rows. The O(n²) only manifests at production scale (millions of rows). Code reviewers often rate it "Minor: performance concern" because the loop body looks simple — but the DataFrame scan is the hidden inner loop.

**BAD** — O(n×m) DataFrame filter per iteration:
```python
# Python/Pandas: looks like O(m) but is actually O(n×m)
# Each df[df["frame"] == frame] scans the entire 3M-row DataFrame
for event in events:  # m = ~1,500 events
    frame = event["frame"]
    period = event["period"]
    # This is O(n) — scans ALL 3M rows every time!
    frame_data = tracking_df[
        (tracking_df["frame"] == frame) & (tracking_df["period"] == period)
    ]
    closest_player = frame_data.loc[
        frame_data["distance_to_ball"].idxmin(), "player_id"
    ]
    results.append({"event_id": event["id"], "player": closest_player})
# Total: 1,500 events × 3,000,000 row scans = 4.5 BILLION comparisons
```

**GOOD** — O(n + m) with pre-built dict:
```python
# Python/Pandas: build index once O(n), then O(1) lookups
# Pre-compute the answer for every (period, frame) in one pass
closest_by_frame: dict[tuple[int, int], str] = {}
for (period, frame), group in tracking_df.groupby(["period", "frame"]):
    if "distance_to_ball" in group.columns and not group.empty:
        closest_by_frame[(period, frame)] = group.loc[
            group["distance_to_ball"].idxmin(), "player_id"
        ]

# Now O(1) lookup per event
for event in events:
    player = closest_by_frame.get((event["period"], event["frame"]), None)
    results.append({"event_id": event["id"], "player": player})
# Total: 3,000,000 rows (once) + 1,500 dict lookups = 3,001,500 operations
```

**Alternative** — vectorized merge instead of loop:
```python
# Best: avoid the loop entirely with a merge/join
# Pre-compute closest player per frame as a DataFrame
closest_per_frame = (
    tracking_df.loc[tracking_df.groupby(["period", "frame"])["distance_to_ball"].idxmin()]
    [["period", "frame", "player_id"]]
    .rename(columns={"player_id": "closest_player"})
)
# Merge with events — no loop at all
results = events_df.merge(closest_per_frame, on=["period", "frame"], how="left")
```

**Detection checklist:**
- [ ] Any `df[df["col"] == variable]` inside a `for` loop? → **Always O(n²)**
- [ ] Any `.loc[]`, `.iloc[]`, or boolean mask indexing that depends on a loop variable? → Check if the DataFrame is large
- [ ] Is the outer loop over events/items and the inner DataFrame is tracking/time-series data (>100K rows)? → **Critical severity**, not Minor
- [ ] Could the filter be replaced by `groupby()` + dict, `set_index()` + `.loc[]`, or a merge/join? → Almost always yes

**Severity escalation rule:** On pipeline code that touches tracking data (millions of rows), DataFrame-filter-inside-loop is **always Critical**, never Minor. The scale of tracking data means O(n²) will always exceed pipeline timeouts.

### 6. Regex Compilation in Loop to Pre-Compiled

**BAD** -- recompiles on every iteration:
```python
for line in lines:
    match = re.search(r"\b\d{3}-\d{4}\b", line)  # Compiles each time
    if match:
        phone_numbers.append(match.group())
```

**GOOD** -- compile once at module level:
```python
PHONE_PATTERN = re.compile(r"\b\d{3}-\d{4}\b")
for line in lines:
    match = PHONE_PATTERN.search(line)
    if match:
        phone_numbers.append(match.group())
```

**BAD** -- recompiles in Go:
```go
for _, line := range lines {
    re := regexp.MustCompile(`\b\d{3}-\d{4}\b`)  // Compiles each iteration
    if re.MatchString(line) { /* ... */ }
}
```

**GOOD** -- compile at package level:
```go
var phonePattern = regexp.MustCompile(`\b\d{3}-\d{4}\b`)
for _, line := range lines {
    if phonePattern.MatchString(line) { /* ... */ }
}
```

---

## Vectorization Patterns

Applies to Python data processing with NumPy and Pandas. Vectorized operations execute in compiled C/Fortran and avoid Python interpreter overhead per element.

### Vectorized Arithmetic

**BAD** -- Python loop:
```python
result = []
for i in range(len(prices)):
    result.append(prices[i] * quantities[i] * (1 - discount_rate))
```

**GOOD** -- NumPy vectorized:
```python
import numpy as np
prices = np.array(prices)
quantities = np.array(quantities)
result = prices * quantities * (1 - discount_rate)
```

### Boolean Indexing

**BAD** -- loop-based filtering:
```python
high_value = []
for _, row in df.iterrows():
    if row["amount"] > 1000 and row["status"] == "active":
        high_value.append(row)
high_value_df = pd.DataFrame(high_value)
```

**GOOD** -- Pandas boolean indexing:
```python
high_value_df = df[(df["amount"] > 1000) & (df["status"] == "active")]
```

### Apply vs Vectorized

**BAD** -- `apply` with Python function (interpreter per row):
```python
df["total"] = df.apply(lambda row: row["price"] * row["qty"] * (1 + row["tax"]), axis=1)
```

**GOOD** -- vectorized column operations:
```python
df["total"] = df["price"] * df["qty"] * (1 + df["tax"])
```

### NumPy Broadcasting

**BAD** -- explicit loop to normalize:
```python
row_means = [np.mean(matrix[i]) for i in range(matrix.shape[0])]
normalized = np.zeros_like(matrix)
for i in range(matrix.shape[0]):
    normalized[i] = matrix[i] - row_means[i]
```

**GOOD** -- broadcasting:
```python
normalized = matrix - matrix.mean(axis=1, keepdims=True)
```

### String Operations in Pandas

**BAD** -- loop-based:
```python
results = []
for val in df["name"]:
    results.append(val.strip().lower().replace(" ", "_"))
df["clean_name"] = results
```

**GOOD** -- Pandas str accessor:
```python
df["clean_name"] = df["name"].str.strip().str.lower().str.replace(" ", "_", regex=False)
```

### Performance Comparison

| Operation | Python Loop | NumPy/Pandas | Speedup |
|-----------|------------|--------------|---------|
| Element-wise arithmetic (1M) | ~500ms | ~5ms | ~100x |
| Boolean filtering (1M rows) | ~2s | ~20ms | ~100x |
| String operations (100K rows) | ~1s | ~100ms | ~10x |
| Apply with simple math (1M) | ~5s | ~5ms | ~1000x |
| iterrows (100K rows) | ~10s | ~10ms | ~1000x |

---

## Guard authoring — scale/complexity guards that keep discriminating

A test that asserts an algorithm's growth (an O(n) vs O(n²) guard, an anti-rot check, a liveness gate) is only useful while it can still fail for the regression it exists for.

- **P23 — one named threshold constant.** A guard and its "does-the-guard-work" companion test must share **one named threshold constant**, not two independent literals that can drift apart. If the guard says `assert exponent < GATE` and its self-test hard-codes `1.5`, a later tweak to one leaves the other stale.
- **P24 — a wide-enough size-ladder.** A scale guard's size ladder must be large enough for the asserted growth term to **dominate** before the threshold is tightened. When a known-broken shim barely fails/passes, fix the **ladder**, not just the threshold — measure where the higher-order term dominates.
  - *» e.g.* on a `(8, 16, 32)` ladder a broken O(n²) shim measured exponent 1.486 (under a 1.5 gate = false pass); moving to `(16, 32, 64)` put the shim at 1.649 vs the real 1.000, cleanly separated by a 1.2 gate. "The ladder, not only the threshold, carries the separation."

The **detection** half — periodically running that known-broken shim to confirm the guard still fails — lives in `optimization-audit/SKILL.md` Phase 12 (cue D6).

## Complexity Analysis Checklist

Systematic approach for reviewing hot paths during Phase 2.

### Step 1: Identify Hot Paths

- [ ] Run profiler with production-like data and load
- [ ] Capture flame graph
- [ ] List top 10 functions by cumulative CPU time
- [ ] List top 10 functions by memory allocation
- [ ] Note functions appearing in both lists

### Step 2: Analyze Each Hot Function

- [ ] **Determine Big-O** -- count nested loops over input-dependent collections (ignore constant-size loops)
- [ ] **Check hidden quadratic behavior** -- `.index()`, `.contains()`, `in list` inside a loop? String `+=` in loop?
- [ ] **Verify data structure choice** -- list where set/map gives O(1) lookup? Sort where heap suffices?
- [ ] **Check repeated computation** -- same expensive value calculated multiple times? Memoization applicable?
- [ ] **Check unnecessary work** -- loop continues after finding answer? Full collection processed when subset needed?
- [ ] **Measure input size range** -- what is n in production? O(n^2) at n=100 is fine; at n=100,000 it is a bug

### Step 3: Evaluate Improvements

- [ ] **Estimate improvement** -- O(n^2) to O(n) for n=10,000 is ~10,000x. Reducing constant factor 2x may not justify complexity.
- [ ] **Check trade-offs** -- more memory? Harder to maintain? Worth the complexity cost?
- [ ] **Prioritize by impact** -- 100x improvement in startup code matters less than 2x in a function called 1M times/sec

### Step 4: Validate

- [ ] **Benchmark before and after** -- use micro-benchmarking tools to measure actual improvement
- [ ] **Profile after change** -- verify hot path shifted as expected
- [ ] **Check for regressions** -- memory usage, latency in other paths, code complexity

### Red Flags Quick Reference

| Red Flag | Pattern | Fix |
|----------|---------|-----|
| Nested loop over two collections | `for x in A: for y in B:` with comparison | Build index/map, then look up |
| `.index()` / `.indexOf()` / `in list` in loop | O(n) search repeated m times | Convert to set or map |
| `.sort()` for top-K | Sorting entire collection | `heapq.nlargest` / PriorityQueue |
| String `+=` in loop | Quadratic string building | `join()` / StringBuilder / strings.Builder |
| `re.compile` / `new RegExp` in loop | Regex recompilation per iteration | Pre-compile at module/package level |
| `append` without capacity hint | Repeated reallocation | Pre-allocate with known/estimated size |
| Recursive without memoization | Exponential recomputation | `@lru_cache`, memo map, or iterative DP |
| Full copy before filter | Copies all, discards most | Filter in-place or use generator/iterator |
| Function called N times with shared setup | `for i in range(N): f(df, scalars[i])` where `f` re-derives subsets of `df` each call | Hoist shared setup (team splits, index builds) outside loop; create batch version accepting `(N, d)` array instead of scalar pair |
| Identical expensive computation across loop iterations | Same clustering, matrix factorization, or spatial index built for iterations sharing identical input | Cache by input key (frame ID, group ID) or input hash; pre-compute once outside loop |
| Map-reduce loop accumulated as Python list | `results = []; for group in groups: results.append(compute(group))` where final output is `sum`/`count`/`mean` over results | Apply reducing function directly (generator + `sum`/`mean`); in Spark: distribute via `applyInPandas` + `groupBy().agg()` |
| Batch-ready inner function hidden behind scalar wrapper | Function accepts `(df, x: float, y: float)` but its core math (matrix ops, numerical integration, NumPy broadcasting) already handles `(n, d)` arrays — the wrapper only exposes scalars | Look past the public signature at the internal computation; create a batch wrapper that hoists setup and passes stacked `(N, 2)` inputs — often 10-20x speedup with minimal code change |
| **DataFrame boolean mask filtering inside a loop** | `for item in items: subset = df[df["key"] == item["key"]]` — full DataFrame scan per iteration | Pre-build a dict/index: `lookup = dict(iter(df.groupby("key")))` or `df.set_index("key")`, then O(1) lookup per iteration. **This is the #1 hidden O(n²) in data science code** — it doesn't look like a nested loop, but `df[df["col"] == val]` is O(n) and calling it m times is O(n×m). On tracking data (millions of rows), this turns a 30-second pipeline into a 1-hour timeout. |
| Benchmark tests passing on synthetic data | Tests use 100-row fixtures but production has millions of rows — O(n²) is invisible at n=100 | Add at least one benchmark with production-scale data volume. A benchmark that passes on 100 rows but OOMs on 3M rows is a **false green**. For pipeline code touching tracking/event data, always include a scaling test. |
