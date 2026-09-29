# Optimization Audit Skill — Research

**Date:** 2026-03-08
**Status:** Research Complete
**Purpose:** Comprehensive catalog of industry-standard optimization audit categories for a generally-applicable "optimization-audit" skill.

**Security audit asks:** "Can attackers exploit this?"
**Observability audit asks:** "Can operators see what's happening?"
**Optimization audit asks:** "Is this system using resources efficiently?"

---

## Category 1: Algorithm & Data Structure Efficiency

**Audit question:** "Are algorithms and data structures appropriate for the problem size and access patterns?"

### What to Check

| Check | What to look for | Severity |
|-------|-----------------|----------|
| Unnecessary nested loops | O(n^2) or worse where O(n) or O(n log n) is achievable | High |
| Linear search on large collections | Sequential scan where hash map / set / binary search applies | High |
| Repeated computation | Same expensive calculation performed multiple times without caching | Medium |
| Inefficient sorting | Sorting entire collection when only top-K needed (use heap) | Medium |
| String concatenation in loops | Building strings with `+=` in a loop instead of `StringBuilder` / `join()` / `strings.Builder` | Medium |
| Unbounded collection growth | Lists, maps, or caches that grow without eviction or size limits | High |
| Inappropriate data structure | Using list where set provides O(1) lookup; using map where array suffices | Medium |
| Redundant traversals | Multiple passes over the same collection that could be merged into one | Low |
| Missing early termination | Loops that continue after the answer is found | Low |
| Quadratic string operations | Regex compilation inside loops, repeated `in` checks on lists | Medium |

### Common Anti-Patterns (grep targets)

| Language | Pattern | Issue |
|----------|---------|-------|
| Python | `for .* in .*:\s*for .* in .*:` (nested loops over same/related collections) | Potential O(n^2) |
| Python | `if .* in list_var` inside a loop | O(n) lookup per iteration; use set |
| Python | `re.compile` inside a loop or function body | Regex recompilation overhead |
| Python | `str += ` or `string = string + ` in a loop | O(n^2) string building |
| JS/TS | `array.indexOf(` or `array.includes(` inside a loop | O(n) lookup per iteration; use Set |
| JS/TS | `string += ` in a loop | String concatenation overhead |
| Java | `new String\(\)` or `"" \+` in a loop | StringBuilder not used |
| Go | `strings\.Contains\(` or linear search inside a loop | Use map for O(1) lookup |
| Go | `append\(` without pre-allocating slice capacity | Repeated reallocation |
| Any | `.sort()` when only min/max/top-K needed | Use heap / partial sort |

### Key Metrics

- Time complexity of hot paths (Big-O)
- CPU flame graph hotspots
- Allocation rate and GC pressure

### Industry Tools (free/open-source)

| Tool | Language | Purpose |
|------|----------|---------|
| `py-spy` | Python | Sampling profiler, flame graphs |
| `scalene` | Python | CPU + memory + GPU profiler |
| `cProfile` / `profile` | Python | Deterministic profiler |
| `clinic.js` (0x, bubbleprof) | Node.js | Flame graphs, async bottleneck detection |
| `pprof` | Go | CPU, memory, goroutine profiling |
| `perf` | Linux/C/C++/Rust | Hardware performance counters |
| `async-profiler` | Java/JVM | Low-overhead sampling profiler |
| `cargo flamegraph` | Rust | Flame graph generation |
| `Visual Studio Profiler` | .NET | CPU, memory, async profiling |

---

## Category 2: Memory Management

**Audit question:** "Is memory allocated efficiently, freed promptly, and sized appropriately?"

### What to Check

| Check | What to look for | Severity |
|-------|-----------------|----------|
| Memory leaks | Objects retained beyond their useful lifetime (event listeners, closures, global caches) | Critical |
| Excessive allocation | Allocating large objects in hot paths, creating objects that could be pooled or reused | High |
| Buffer sizing | Buffers too small (frequent resizing) or too large (wasted memory) | Medium |
| Large object retention | Holding references to large objects (DataFrames, images, response bodies) longer than needed | High |
| Unbounded caches | In-memory caches without TTL or max-size eviction | Critical |
| Goroutine / thread leaks | Goroutines, threads, or async tasks spawned but never joined or canceled | Critical |
| Closure captures | Closures inadvertently capturing large objects or entire scopes | Medium |
| Copy vs reference | Unnecessary deep copies of large data structures | Medium |
| Object pooling absence | Frequently created and destroyed expensive objects (DB connections, HTTP clients, buffers) | High |
| GC pressure | High allocation rate causing frequent garbage collection pauses | Medium |

### Common Anti-Patterns (grep targets)

| Language | Pattern | Issue |
|----------|---------|-------|
| Python | `global ` + mutable data structures | Global state that grows unboundedly |
| Python | `@lru_cache` without `maxsize` (or `maxsize=None`) | Unbounded cache |
| Python | `df = pd.read_csv\(` on very large files without `chunksize` | Entire file loaded into memory |
| JS/TS | `addEventListener\(` without corresponding `removeEventListener` | Event listener leak |
| JS/TS | `setInterval\(` without `clearInterval` | Timer leak |
| JS/TS | `new Map\(\)` or `new Set\(\)` used as cache without eviction | Unbounded growth |
| Go | `go func\(\)` without context cancellation or done channel | Goroutine leak |
| Go | `make\(` with `0` capacity for slices that grow large | Repeated reallocation |
| Java | `static.*Map\|static.*List\|static.*Set` without size limit | Static collection leak |
| Java | `ThreadLocal` without `remove()` in finally block | Thread-local memory leak |
| Rust | `Box::leak\|mem::forget` | Intentional leak (verify intentional) |
| Any | `.*cache.*=.*\{\}` or `.*cache.*= new Map` without TTL/max entries | Unbounded cache |

### Key Metrics

- Heap usage over time (steady growth = leak)
- Allocation rate (bytes/sec)
- GC pause frequency and duration
- Resident Set Size (RSS) vs Virtual Size (VSZ)

### Industry Tools

| Tool | Language | Purpose |
|------|----------|---------|
| `tracemalloc` | Python | Track memory allocations |
| `objgraph` | Python | Object reference graph, leak detection |
| `memray` | Python | High-performance memory profiler |
| Chrome DevTools / `--inspect` | Node.js | Heap snapshots, allocation timeline |
| `heaptrack` | C/C++ | Heap profiling, leak detection |
| `pprof` (heap) | Go | Heap allocation profiling |
| `VisualVM` / `JFR` | Java | Heap analysis, allocation tracking |
| `valgrind` (massif) | C/C++/Rust | Memory usage profiling |

---

## Category 3: Concurrency & Parallelism

**Audit question:** "Are concurrent operations safe, efficient, and non-blocking?"

### What to Check

| Check | What to look for | Severity |
|-------|-----------------|----------|
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

### Common Anti-Patterns (grep targets)

| Language | Pattern | Issue |
|----------|---------|-------|
| Python | `time\.sleep\(` inside `async def` | Blocking the event loop |
| Python | `requests\.\(get\|post\)` inside `async def` | Sync HTTP in async context |
| Python | `open\(` (file I/O) inside `async def` without `aiofiles` | Sync file I/O in async context |
| Python | `ThreadPoolExecutor\(max_workers=` (check if sizing is reasonable) | Thread pool misconfiguration |
| JS/TS | `await` inside `for` loop (sequential awaits) | Should use `Promise.all()` for parallel |
| JS/TS | `new Promise` with blocking operations | Blocking the event loop |
| Go | `sync\.Mutex` with large critical sections | Lock contention |
| Go | `go func\(\)` in a loop without `semaphore` or `errgroup` | Unbounded goroutine fan-out |
| Java | `synchronized` on broad scope | Coarse-grained locking |
| Java | `Executors\.newFixedThreadPool\(1\)` | Artificially serialized execution |
| Any | `Lock\(\)` or `mutex` acquired in nested fashion | Deadlock risk |
| Any | `global\|static\|shared` mutable state without lock | Race condition risk |

### Key Metrics

- Thread/goroutine count over time
- Lock contention time (% of wall time spent waiting on locks)
- Connection pool utilization (active/idle/waiting)
- Event loop latency (Node.js, Python asyncio)
- Context switch rate

### Industry Tools

| Tool | Language | Purpose |
|------|----------|---------|
| `asyncio.debug` mode | Python | Detect blocking calls in async context |
| `clinic.js bubbleprof` | Node.js | Async bottleneck visualization |
| Go race detector (`-race`) | Go | Runtime race condition detection |
| `ThreadSanitizer` (TSan) | C/C++/Rust | Data race detection |
| `jstack` / `async-profiler` | Java | Thread dump analysis, lock contention |
| Tokio Console | Rust (Tokio) | Async task inspection |
| `py-spy` with `--subprocesses` | Python | Multi-process profiling |

---

## Category 4: Database Query Optimization

**Audit question:** "Are database queries efficient, properly indexed, and not generating unnecessary load?"

### What to Check

| Check | What to look for | Severity |
|-------|-----------------|----------|
| N+1 queries | Loop that executes a query per iteration instead of batch/join | Critical |
| Missing indexes | Queries filtering or joining on non-indexed columns; full table scans | Critical |
| SELECT * usage | Fetching all columns when only a few are needed | Medium |
| Unbounded queries | Queries without LIMIT or pagination on potentially large result sets | High |
| Missing EXPLAIN analysis | Complex queries not analyzed with EXPLAIN/EXPLAIN ANALYZE | High |
| Inefficient JOINs | Cartesian products, joining on non-indexed columns, unnecessary JOINs | High |
| Query in loop (batch vs row-by-row) | Individual INSERTs/UPDATEs instead of batch operations | High |
| Unused indexes | Indexes that exist but are never used by any query (write overhead for no benefit) | Medium |
| Over-indexing | Too many indexes on write-heavy tables, slowing down inserts/updates | Medium |
| Missing connection pooling | New connection per request instead of reusing pooled connections | Critical |
| Suboptimal schema | Wrong column types, missing constraints, denormalization needed but absent | Medium |
| Full table scans on large tables | Sequential scans where index scan is possible | High |
| Lock contention from long transactions | Transactions held open longer than necessary | High |
| Missing read replicas | All queries hitting the primary database; reads not offloaded | Medium |

### Common Anti-Patterns (grep targets)

| Language | Pattern | Issue |
|----------|---------|-------|
| Python (Django) | `.objects.all()` in template or loop without `.select_related()` / `.prefetch_related()` | N+1 query |
| Python (Django) | `for obj in queryset:.*obj\.related_field` | N+1 query via lazy loading |
| Python (SQLAlchemy) | `session\.query\(` inside a `for` loop | N+1 query |
| Python (SQLAlchemy) | `relationship\(` without `lazy='joined'` or `lazy='subquery'` when always accessed | Lazy loading N+1 |
| Ruby (ActiveRecord) | `.each do.*\.association_name` without `.includes()` | N+1 query |
| Java (Hibernate/JPA) | `@ManyToOne` or `@OneToMany` with default `FetchType.EAGER` or lazy without batch | N+1 / over-fetching |
| Any ORM | `SELECT \*` or `model.objects.all()` when specific columns suffice | Over-fetching |
| Any | `INSERT INTO` inside a `for\|while\|each` loop | Row-by-row insert |
| Any | `execute\(` or `query\(` inside a loop body | Potential N+1 |
| SQL | `SELECT.*FROM.*WHERE.*NOT IN \(SELECT` | Subquery vs JOIN performance |
| SQL | `LIKE '%term%'` | Leading wildcard prevents index use |
| SQL | `ORDER BY.*OFFSET \d+` with large offset | Inefficient pagination (use cursor/keyset) |

### Key Metrics

- Queries per request (N+1 detection)
- Query execution time (p50, p95, p99)
- Slow query log entries
- Table scan ratio (seq_scan / total scans)
- Index hit ratio
- Connection pool utilization (active/idle/max)
- Lock wait time
- Rows examined vs rows returned ratio

### Industry Tools

| Tool | Language/DB | Purpose |
|------|-------------|---------|
| `EXPLAIN ANALYZE` | PostgreSQL | Query plan analysis |
| `EXPLAIN` | MySQL | Query plan analysis |
| `django-debug-toolbar` | Django | Query count, duplicates, timing |
| `nplusone` | Python (Django/SQLAlchemy) | Automatic N+1 detection |
| `bullet` | Ruby on Rails | N+1 query detection |
| `pganalyze` | PostgreSQL | Query performance monitoring |
| `pt-query-digest` | MySQL | Slow query log analysis |
| `pg_stat_statements` | PostgreSQL | Query statistics |
| `EXPLAIN QUERY PLAN` | SQLite | Query plan analysis |
| `mongosh` `explain()` | MongoDB | Query plan analysis |

---

## Category 5: Connection & Resource Pooling

**Audit question:** "Are expensive resources (connections, clients, buffers) pooled, reused, and properly configured?"

### What to Check

| Check | What to look for | Severity |
|-------|-----------------|----------|
| Database connection pooling | Connection pool configured with appropriate min/max/idle settings | Critical |
| HTTP client reuse | Single HTTP client instance reused across requests (not creating per request) | High |
| gRPC channel reuse | gRPC channels shared and reused, not created per call | High |
| Pool size tuning | Pool max size based on workload, not arbitrary defaults | High |
| Idle connection management | Idle connections reclaimed after timeout, not held forever | Medium |
| Connection leak detection | Connections borrowed but never returned to the pool | Critical |
| Health check on pooled connections | Pool validates connections before handing them out (test-on-borrow or background validation) | Medium |
| DNS resolution caching | DNS lookups not repeated per connection for same hostname | Low |
| File descriptor limits | `ulimit` / file descriptor limits appropriate for connection count | Medium |
| Socket reuse (keep-alive) | HTTP keep-alive enabled; TCP connections reused | Medium |

### Common Anti-Patterns (grep targets)

| Language | Pattern | Issue |
|----------|---------|-------|
| Python | `psycopg2.connect\(` or `create_engine\(` inside request handler (not at module level) | New connection per request |
| Python | `requests.Session\(\)` created per request instead of reused | Session per request |
| Python | `aiohttp.ClientSession\(\)` inside a loop | Session per iteration |
| Node.js | `new Pool\(\)` or `createConnection\(` inside request handler | Pool per request |
| Node.js | `new http.Agent\(\)` per request | Agent not reused |
| Go | `http.Get\(` (uses `http.DefaultClient` without configured transport) | No connection pooling control |
| Go | `sql.Open\(` inside handler instead of at startup | New pool per request |
| Java | `DriverManager.getConnection\(` without connection pool (HikariCP, c3p0) | No pooling |
| Any | `max_connections=1` or very low pool sizes | Artificial bottleneck |

### Key Metrics

- Pool size (active/idle/max)
- Connection wait time
- Connection acquisition failures
- Pool exhaustion events
- Connection lifetime distribution

### Industry Tools

| Tool | Purpose |
|------|---------|
| HikariCP metrics | Java connection pool monitoring |
| pgBouncer | PostgreSQL connection pooling proxy |
| PgCat | Modern PostgreSQL connection pooler |
| ProxySQL | MySQL connection pooler and query router |
| Redis connection pool metrics | Built-in `INFO` command |

---

## Category 6: Caching Strategies

**Audit question:** "Are cacheable operations identified and cached at the right layer with appropriate invalidation?"

### What to Check

| Check | What to look for | Severity |
|-------|-----------------|----------|
| Missing cache for repeated expensive operations | Same database query, API call, or computation executed repeatedly with same inputs | High |
| Cache invalidation correctness | Stale data served after the source of truth changes | Critical |
| Cache sizing | Cache too small (constant eviction, low hit rate) or too large (memory waste) | Medium |
| TTL appropriateness | TTL too short (frequent cache misses) or too long (stale data) | Medium |
| Cache stampede protection | Thundering herd when cache expires (all requests hit backend simultaneously) | High |
| Memoization opportunities | Pure functions called repeatedly with same arguments without memoization | Medium |
| HTTP cache headers | Missing `Cache-Control`, `ETag`, `Last-Modified` headers on cacheable responses | Medium |
| CDN configuration | Static assets and cacheable API responses not served from CDN | Medium |
| Multi-layer caching | Missing L1 (in-process) + L2 (distributed) caching for high-traffic paths | Low |
| Cache warming | Cold start after deployment with no cache pre-warming strategy | Low |
| Serialization overhead | Cache serialization format too verbose or slow (e.g., JSON for large binary data) | Low |

### Common Anti-Patterns (grep targets)

| Language | Pattern | Issue |
|----------|---------|-------|
| Python | Expensive function without `@lru_cache` / `@cache` decorator | Missing memoization |
| Python | `redis.get\(` with `redis.set\(.*ex=None` | Cache without expiry |
| JS/TS | No `Cache-Control` header in API response middleware | Missing HTTP cache headers |
| Any | `cache.delete\(` or `cache.invalidate\(` absent after write operations | Missing cache invalidation |
| Any | Identical query or API call appearing in multiple code paths | Cacheable operation not cached |
| HTTP | `Cache-Control: no-cache, no-store` on all responses (including static assets) | Over-restrictive caching |
| HTTP | No `ETag` or `Last-Modified` on GET responses | Missing conditional request support |

### Key Metrics

- Cache hit ratio (hits / (hits + misses)) -- target >90% for most caches
- Cache eviction rate
- Cache latency (get/set p50, p99)
- Origin load reduction (% of requests served from cache)
- TTL effectiveness (% of entries expiring vs evicted)
- Memory usage by cache

### Industry Tools

| Tool | Purpose |
|------|---------|
| Redis `INFO stats` | Hit/miss ratio, memory usage |
| Memcached `stats` | Hit/miss ratio, eviction counts |
| Varnish | HTTP reverse proxy cache with detailed metrics |
| CDN analytics (CloudFront, Cloudflare) | Cache hit ratio, origin requests |
| `django-cachalot` | Django ORM query caching |
| `@tanstack/query` (React Query) | Client-side data caching with deduplication |

---

## Category 7: Serialization & Data Transfer

**Audit question:** "Is data serialized, deserialized, and transferred efficiently?"

### What to Check

| Check | What to look for | Severity |
|-------|-----------------|----------|
| Serialization format choice | JSON vs Protobuf vs MessagePack vs Avro for the use case | Medium |
| Over-serialization | Serializing and deserializing data that will just be passed through | High |
| Large payload transfer | Transferring entire objects when only a subset of fields is needed | High |
| Compression on wire | Response compression (gzip, brotli, zstd) not enabled for API responses | High |
| Repeated serialization | Same object serialized multiple times in a request lifecycle | Medium |
| Schema evolution overhead | Serialization format doesn't handle schema changes gracefully | Low |
| String encoding | Unnecessary encoding/decoding cycles (UTF-8/16/32 conversions) | Low |
| Deep copy via serialization | Using serialize/deserialize as a deep copy mechanism | Medium |
| Base64 bloat | Binary data Base64-encoded in JSON (33% overhead) where binary transport is available | Medium |
| Date/time parsing | Parsing timestamps from strings repeatedly instead of using epoch/native types | Low |

### Common Anti-Patterns (grep targets)

| Language | Pattern | Issue |
|----------|---------|-------|
| Python | `json\.dumps\(.*json\.loads\(` in sequence (round-trip) | Unnecessary serialization |
| Python | `pickle\.dumps\|pickle\.loads` for data transfer (vs msgpack/protobuf) | Slow, insecure serialization |
| JS/TS | `JSON\.parse\(JSON\.stringify\(` (deep clone via JSON) | Performance-expensive deep copy |
| Any | `base64` encoding of large binary payloads in JSON responses | 33% overhead; use binary format |
| Any | Response without `Content-Encoding: gzip\|br\|zstd` header | Missing compression |
| Any | `for .* in .*: .*\.to_json\(\)\|\.to_dict\(\)` | Per-item serialization in loop |

### Key Metrics

- Serialization/deserialization time per request
- Payload size (before/after compression)
- Compression ratio
- Bandwidth consumption

### Industry Tools

| Tool | Purpose |
|------|---------|
| Protocol Buffers (protobuf) | Compact binary serialization |
| MessagePack | Efficient binary alternative to JSON |
| Apache Avro | Schema-based serialization for data pipelines |
| `zstd` / `brotli` / `gzip` | Compression algorithms (zstd offers best speed/ratio trade-off) |
| Browser DevTools Network tab | Payload size, compression analysis |

---

## Category 8: Data Loading Patterns

**Audit question:** "Is data loaded at the right granularity -- not too eagerly and not too lazily?"

### What to Check

| Check | What to look for | Severity |
|-------|-----------------|----------|
| N+1 query problem | ORM lazy-loading related objects one at a time in a loop | Critical |
| Over-fetching | Loading all columns/fields when only a few are needed | Medium |
| Under-fetching | Multiple round trips to load data that could come in one request | High |
| Eager loading overhead | Loading large related datasets that may not be used | Medium |
| Pagination absence | Loading entire collections instead of paginating | High |
| Offset-based pagination on large datasets | Using OFFSET for deep pagination (performance degrades linearly) | High |
| Missing cursor/keyset pagination | Large datasets paginated with offset instead of cursor | Medium |
| Unnecessary data transformation | ETL steps that transform data not used downstream | Medium |
| Speculative loading | Pre-loading data "just in case" without evidence it is needed | Low |
| Streaming vs buffering | Buffering entire large result set in memory instead of streaming/iterating | High |

### Common Anti-Patterns (grep targets)

| Language | Pattern | Issue |
|----------|---------|-------|
| Python (Django) | `\.objects\.all\(\)` without `.only()`, `.values()`, or `.defer()` | Over-fetching |
| Python (Django) | Accessing `related_object.field` in a loop without `.select_related()` | N+1 |
| Python (SQLAlchemy) | `query.all()` without `.options(joinedload())` for relationships | N+1 potential |
| GraphQL | No `dataloader` or batch resolver for nested fields | N+1 at resolver level |
| REST API | No `?fields=` sparse fieldset support | Over-fetching by default |
| Any | `OFFSET (\d{4,})` (offset > 1000) | Deep offset pagination |
| Any | `.fetchall\(\)` or `.to_list\(\)` on large query results | Entire result in memory |

### Key Metrics

- Queries per page/request
- Bytes transferred per request vs bytes used
- Pagination depth distribution
- Time to first byte (TTFB)

### Industry Tools

| Tool | Purpose |
|------|---------|
| `django-debug-toolbar` | Query count, duplicate detection |
| `nplusone` | Automatic N+1 detection (Django, SQLAlchemy) |
| GraphQL `dataloader` | Batch and deduplicate resolver queries |
| Apollo Studio | GraphQL query performance analysis |

---

## Category 9: Network & Transport Optimization

**Audit question:** "Is network communication efficient, compressed, and using modern protocols?"

### What to Check

| Check | What to look for | Severity |
|-------|-----------------|----------|
| Response compression | gzip/brotli/zstd compression enabled on HTTP responses | High |
| HTTP/2 or HTTP/3 | Modern HTTP protocol enabled for multiplexing and header compression | Medium |
| Keep-alive connections | TCP keep-alive and HTTP keep-alive enabled, not closing connections per request | High |
| DNS optimization | DNS prefetch, connection preconnect for known external hosts | Low |
| TLS session resumption | TLS session tickets or session cache configured | Low |
| Request batching | Multiple small API calls that could be batched into one | Medium |
| Chatty APIs | Too many round trips for a single user action | High |
| Payload size | Excessively large request/response bodies | Medium |
| Geographic latency | Users far from servers with no CDN or edge compute | Medium |
| WebSocket vs polling | Long-polling or frequent polling where WebSocket is more efficient | Medium |
| gRPC streaming | Unary RPC calls in a loop where streaming would be more efficient | Medium |
| TCP tuning | Default TCP settings on high-throughput servers | Low |

### Common Anti-Patterns (grep targets)

| Language | Pattern | Issue |
|----------|---------|-------|
| Server config | `gzip off\|compress: false\|compression: false` | Compression disabled |
| Server config | `keepalive_timeout 0\|Connection: close` | Keep-alive disabled |
| JS (frontend) | `fetch\(\)` in a `for\|forEach\|map` loop | Sequential API calls, should batch |
| JS (frontend) | `setInterval\(.*fetch\|poll` with short interval | Consider WebSocket/SSE |
| Nginx | `http2 off` or missing `http2` directive | HTTP/2 not enabled |
| Any | Multiple sequential `GET` requests on page load | Should batch or use GraphQL |

### Key Metrics

- Response time by geography (latency percentiles)
- Bandwidth utilization
- Compression ratio
- Connection reuse ratio
- DNS lookup time
- TLS handshake time
- Requests per connection

### Industry Tools

| Tool | Purpose |
|------|---------|
| `lighthouse` | Web performance audit (compression, protocol, caching) |
| `WebPageTest` | Multi-location performance testing with waterfall |
| `curl -w` (timing format) | Detailed timing breakdown (DNS, TLS, TTFB) |
| `h2load` | HTTP/2 load testing |
| `wrk` / `hey` / `k6` | HTTP load testing |
| Browser DevTools Network tab | Request waterfall, compression, protocol |

---

## Category 10: Frontend & Client-Side Performance

**Audit question:** "Is the client-side fast, resource-efficient, and providing a good user experience?"

### What to Check

| Check | What to look for | Severity |
|-------|-----------------|----------|
| Bundle size | JavaScript bundle too large, not code-split | High |
| Tree-shaking | Dead code not eliminated from production bundles | Medium |
| Code splitting | Monolithic bundle instead of route-based splitting | High |
| Image optimization | Unoptimized images (no WebP/AVIF, no responsive sizes, no lazy loading) | High |
| Render-blocking resources | CSS/JS blocking initial render without `async` / `defer` | High |
| Font loading | Custom fonts blocking text rendering (no `font-display: swap`) | Medium |
| Third-party scripts | Heavy third-party scripts loaded synchronously | High |
| DOM complexity | Excessive DOM nodes (>1500) or deep nesting (>32 levels) | Medium |
| Layout thrashing | Reading and writing DOM layout properties in alternation | High |
| Unnecessary re-renders | React/Vue components re-rendering when props haven't changed | Medium |
| Missing virtual scrolling | Rendering thousands of list items instead of virtualizing | High |
| Service worker caching | No offline/cache-first strategy for static assets | Low |
| Core Web Vitals | LCP, FID/INP, CLS not meeting thresholds | High |

### Common Anti-Patterns (grep targets)

| Language | Pattern | Issue |
|----------|---------|-------|
| HTML | `<script src=` without `async\|defer\|type="module"` | Render-blocking script |
| HTML | `<img ` without `loading="lazy"` (below fold) | Eager image loading |
| HTML | `<img ` without `srcset` or `<picture>` | No responsive images |
| CSS | `@import url\(` in CSS (not preprocessor) | Render-blocking cascade |
| React | Component without `React.memo\|useMemo\|useCallback` on expensive renders | Unnecessary re-renders |
| React | `useEffect\(\(\) =>.*fetch` without cleanup/caching | Missing data caching |
| JS | `document\.querySelectorAll\(` inside `requestAnimationFrame\|scroll\|resize` handler | Layout thrashing |
| JS | `import ` (static import) of large libraries not needed on initial load | Should be dynamic `import()` |
| Webpack/Vite | No `splitChunks\|manualChunks` configuration | Missing code splitting |
| CSS | `* \{` universal selector | Performance-impacting CSS |

### Key Metrics (Core Web Vitals + extras)

| Metric | Target | What it measures |
|--------|--------|-----------------|
| LCP (Largest Contentful Paint) | < 2.5s | Loading performance |
| INP (Interaction to Next Paint) | < 200ms | Responsiveness |
| CLS (Cumulative Layout Shift) | < 0.1 | Visual stability |
| FCP (First Contentful Paint) | < 1.8s | Perceived load speed |
| TTFB (Time to First Byte) | < 800ms | Server responsiveness |
| Total Bundle Size (JS) | < 200KB gzipped (initial) | Transfer efficiency |
| Total Transfer Size | < 1MB (initial page load) | Overall page weight |

### Industry Tools

| Tool | Purpose |
|------|---------|
| Lighthouse (Chrome DevTools) | Comprehensive performance audit |
| WebPageTest | Multi-location real browser testing |
| `bundlephobia` | npm package size analysis |
| `webpack-bundle-analyzer` / `rollup-plugin-visualizer` | Bundle composition analysis |
| `source-map-explorer` | Bundle size by module |
| Chrome DevTools Performance tab | Runtime performance profiling |
| `react-scan` | React render performance analysis |
| Core Web Vitals (CrUX) | Real user metrics from Chrome |

---

## Category 11: API Response Optimization

**Audit question:** "Are API responses shaped, sized, and delivered efficiently?"

### What to Check

| Check | What to look for | Severity |
|-------|-----------------|----------|
| Pagination | Large collections returned without pagination | Critical |
| Cursor-based pagination | Large datasets using offset instead of cursor/keyset pagination | High |
| Sparse fieldsets | API returns all fields when clients only need a subset | Medium |
| Response compression | gzip/brotli not enabled on API responses | High |
| GraphQL query complexity | No depth/cost limiting on GraphQL queries | High |
| Over-fetching aggregation | Multiple API calls where one aggregated endpoint would suffice | Medium |
| ETags / conditional requests | No support for `If-None-Match` / `304 Not Modified` | Medium |
| API versioning overhead | Maintaining old API versions with translation layers | Low |
| Streaming for large responses | Large result sets fully buffered instead of streamed (NDJSON, SSE) | Medium |
| Batch endpoints | No batch API for operations frequently called in rapid succession | Medium |

### Common Anti-Patterns (grep targets)

| Language | Pattern | Issue |
|----------|---------|-------|
| Any API | `return .*\.all\(\)\|return .*find\(\{\}\)` (no limit/pagination) | Unbounded response |
| Django | `serializer_class =` without `fields = ` specification | Serializing all fields |
| FastAPI | `response_model=` returning full model when subset would do | Over-fetching |
| Express | `res\.json\(results\)` without pagination metadata | Missing pagination |
| GraphQL | No `depthLimit\|costAnalysis\|queryComplexity` middleware | Unbounded query depth |
| Any | No `Link` header or `next_cursor` in paginated responses | Incomplete pagination |

### Key Metrics

- Response payload size (p50, p95)
- Requests per user action (should be minimal)
- Cache hit ratio for conditional requests (304 vs 200)
- API latency by endpoint (p50, p95, p99)
- Bandwidth per request

### Industry Tools

| Tool | Purpose |
|------|---------|
| `graphql-depth-limit` | GraphQL query depth limiting |
| `graphql-query-complexity` | GraphQL cost analysis |
| `graphql-rate-limit` | GraphQL rate limiting |
| JSON:API spec | Sparse fieldsets, pagination standards |
| OpenAPI Generator | Generate efficient API clients |

---

## Category 12: Container & Build Optimization

**Audit question:** "Are container images lean, builds fast, and deployments efficient?"

### What to Check

| Check | What to look for | Severity |
|-------|-----------------|----------|
| Multi-stage builds | Application image contains build tools, compilers, dev dependencies | High |
| Base image selection | Using full OS image (ubuntu, debian) instead of slim/distroless/alpine | High |
| Layer ordering | Frequently changing layers (code) not last in Dockerfile | Medium |
| Dependency caching | Package install layer not cached (dependencies reinstalled on every code change) | High |
| `.dockerignore` | `node_modules`, `.git`, `__pycache__`, test files, docs included in build context | Medium |
| Image size | Image > 500MB for a typical application | Medium |
| Pinned versions | Base image using `latest` instead of pinned digest or version | Medium |
| Unnecessary files | Docs, tests, source maps, dev configs in production image | Low |
| Build cache utilization | CI/CD not caching Docker layers between builds | Medium |
| Health check defined | No HEALTHCHECK instruction in Dockerfile | Medium |
| Non-root user | Container running as root | Medium (also security) |
| Resource limits | No CPU/memory limits in orchestrator config | High |

### Common Anti-Patterns (grep targets)

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

### Key Metrics

- Image size (MB)
- Build time (cold, warm/cached)
- Layer count and largest layers
- Time to pull image
- Cold start time

### Industry Tools

| Tool | Purpose |
|------|---------|
| `dive` | Docker image layer analysis |
| `docker history` | Layer size breakdown |
| `hadolint` | Dockerfile linting |
| `trivy` | Image vulnerability scanning + size analysis |
| `docker-slim` (SlimToolkit) | Automatic image minification |
| `ko` | Go container image builder (distroless) |
| `jib` | Java container image builder (no Dockerfile) |
| `BuildKit` | Improved Docker build with better caching |
| `depot.dev` / GitHub Actions cache | Remote Docker layer caching |

---

## Category 13: Cold Start & Startup Optimization

**Audit question:** "Does the application start quickly and handle cold starts gracefully?"

### What to Check

| Check | What to look for | Severity |
|-------|-----------------|----------|
| Lambda/serverless cold start | Initialization code that runs on every cold start (loading ML models, connecting to services) | High |
| Container startup time | Application takes > 30s to become ready | High |
| Eager initialization | Loading all resources at startup instead of lazy-initializing on first use | Medium |
| Provisioned concurrency (serverless) | Frequently invoked functions without provisioned concurrency | Medium |
| Connection establishment at startup | Database/cache connections not initialized until first request | Medium |
| Module import time | Heavy module imports at top level (large frameworks, ML libraries) | Medium |
| Class loading (JVM) | Large classpath with unnecessary JARs | Medium |
| Warm-up endpoints | No warm-up mechanism after deployment | Low |
| Readiness probe alignment | Application marked ready before it can actually handle requests | High |
| Dependency initialization order | Sequential initialization of independent resources | Medium |

### Common Anti-Patterns (grep targets)

| Language | Pattern | Issue |
|----------|---------|-------|
| Python (Lambda) | `import (tensorflow\|torch\|pandas\|sklearn)` at module top level in handler | Heavy imports on cold start |
| Python | `load_model\(\)` at module level without lazy initialization | Model loaded on every cold start |
| Node.js (Lambda) | `require\('aws-sdk'\)` importing entire SDK | Should import only needed service client |
| Java | Large classpath without `GraalVM native-image` or `CDS` | Slow JVM startup |
| Any | `time\.sleep\|Thread\.sleep` in startup sequence | Artificial startup delay |

### Key Metrics

- Cold start time (p50, p95, p99)
- Warm start time
- Time to ready (container)
- Memory allocated vs used at startup
- Initialization cost breakdown (by component)

### Industry Tools

| Tool | Purpose |
|------|---------|
| AWS Lambda Power Tuning | Optimal memory/timeout configuration |
| `importtime` (Python `-X importtime`) | Module import timing |
| GraalVM `native-image` | AOT compilation for fast JVM startup |
| AWS SnapStart | JVM snapshot for Lambda cold start reduction |
| Spring Boot `spring-boot-startup-actuator` | Startup time breakdown |

---

## Category 14: Data Pipeline Optimization

**Audit question:** "Are data pipelines processing data efficiently with appropriate batch/stream trade-offs?"

### What to Check

| Check | What to look for | Severity |
|-------|-----------------|----------|
| Batch vs streaming mismatch | Using batch for near-real-time requirements, or streaming for overnight analytics | High |
| Full recomputation vs incremental | Reprocessing entire dataset when only new/changed records need processing | High |
| Data skew | Uneven partition sizes causing some tasks to take much longer than others | High |
| Shuffle operations | Unnecessary shuffles in distributed computation (Spark: repartition, groupByKey) | High |
| Over-partitioning | Too many small files/partitions (worse than under-partitioning for read performance) | Medium |
| Under-partitioning | Too few partitions causing memory pressure on individual workers | Medium |
| Storage format | Row-format (CSV, JSON) for analytical queries instead of columnar (Parquet, ORC) | High |
| Compression | Uncompressed data in storage or transit | Medium |
| Predicate pushdown | Filtering after read instead of pushing predicates down to storage layer | High |
| Column pruning | Reading all columns from wide tables when only a few are needed | Medium |
| Materialization strategy | Recomputing expensive intermediate results instead of materializing them | Medium |
| Idempotency | Pipeline not safe to re-run (produces duplicates or corrupts state) | High |
| Dead letter handling | Failed records silently dropped instead of quarantined for investigation | High |
| Retry strategy | No retry with backoff for transient failures | Medium |
| Window/watermark tuning | Stream processing windows too large (latency) or too small (overhead) | Medium |

### Common Anti-Patterns (grep targets)

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
| Any | Writing to CSV/JSON for analytics instead of Parquet | Suboptimal storage format |
| Any | `for row in` iteration over large dataset instead of vectorized ops | Row-by-row processing |

### Key Metrics

- Pipeline execution time (wall clock, CPU time)
- Data throughput (rows/sec, bytes/sec)
- Partition skew ratio (max partition size / median)
- Shuffle bytes read/written
- Storage efficiency (compression ratio, file format)
- Freshness (time from source update to downstream availability)
- Cost per pipeline run

### Industry Tools

| Tool | Purpose |
|------|---------|
| Spark UI / Spark History Server | Job/stage/task analysis, shuffle metrics |
| dbt timing (`run_results.json`) | Per-model execution time |
| Apache Airflow Gantt chart | Task parallelism visualization |
| `EXPLAIN` (data warehouse) | Query plan analysis for warehouse queries |
| AWS Glue job metrics | Spark job monitoring on Glue |
| Databricks Job metrics | Spark/SQL job monitoring |
| Delta Lake `DESCRIBE HISTORY` | Table change history, operation metrics |

---

## Category 15: Cloud Resource Right-Sizing & Cost

**Audit question:** "Are cloud resources appropriately sized for the workload, and are cost optimization opportunities being missed?"

### What to Check

| Check | What to look for | Severity |
|-------|-----------------|----------|
| Over-provisioned compute | CPU utilization consistently < 20%, memory < 30% | High |
| Under-provisioned compute | CPU > 80% sustained, OOM kills, throttling | Critical |
| Right instance type | General-purpose instances for compute-heavy or memory-heavy workloads | Medium |
| Auto-scaling configuration | No auto-scaling, or scaling thresholds too conservative/aggressive | High |
| Spot/preemptible usage | Fault-tolerant workloads not using spot instances (60-90% savings) | High |
| Reserved capacity | Steady-state workloads on on-demand pricing without reservations or savings plans | High |
| Storage tiering | Infrequently accessed data on expensive hot storage tier | High |
| Idle resources | Running resources during off-hours (dev/staging environments) | High |
| Orphaned resources | Detached EBS volumes, unused Elastic IPs, stale snapshots, empty load balancers | Medium |
| Egress optimization | Cross-region or cross-AZ traffic that could be localized | Medium |
| Serverless vs always-on | Always-on instances for bursty/infrequent workloads | Medium |
| License costs | Commercial software (Oracle, SQL Server) where open-source alternatives exist | Medium |
| Oversized databases | RDS instance with 10% CPU utilization | High |
| Oversized caches | ElastiCache/Redis cluster with < 20% memory utilization | Medium |

### Common Anti-Patterns (grep targets)

| Language | Pattern | Issue |
|----------|---------|-------|
| Terraform | `instance_type = ".*xlarge\|.*2xlarge\|.*4xlarge"` (verify against utilization) | Potentially oversized |
| Terraform | No `autoscaling_group` or `auto_scaling_configuration` | Missing auto-scaling |
| Terraform | `storage_type = "gp2"` | Should be `gp3` (cheaper, better performance) |
| Terraform | `engine = "oracle-\|sqlserver-"` | Commercial DB license costs |
| Terraform | `deletion_protection = false` on production resources | Risk of accidental deletion |
| Kubernetes | `resources.requests.cpu` >> actual usage | Over-provisioned pods |
| Kubernetes | No `HorizontalPodAutoscaler` for variable workloads | Missing auto-scaling |
| AWS CloudFormation | `InstanceType: .*\.xlarge` without justification | Potentially oversized |
| docker-compose | No `deploy.resources.limits` (memory/CPU) | Unbounded resource usage |

### Key Metrics

- CPU utilization (average, p95)
- Memory utilization (average, peak)
- Monthly cloud spend by service
- Cost per transaction / request / pipeline run
- Reserved instance utilization (% of reserved capacity used)
- Spot interruption rate

### Industry Tools

| Tool | Purpose |
|------|---------|
| AWS Cost Explorer / AWS Compute Optimizer | Cost analysis and right-sizing recommendations |
| Azure Advisor | Cost and performance recommendations |
| GCP Recommender | VM, disk, and commitment recommendations |
| `infracost` | Terraform cost estimation in CI/CD |
| Kubecost | Kubernetes cost monitoring and right-sizing |
| Spot.io / Cast.ai | Automated spot instance management |
| CloudHealth / Apptio | Multi-cloud cost management |
| `kubectl top pods` / Metrics Server | Real-time resource usage |

---

## Category 16: Auto-Scaling & Elasticity

**Audit question:** "Can the system scale up to meet demand and scale down to save cost?"

### What to Check

| Check | What to look for | Severity |
|-------|-----------------|----------|
| Horizontal scaling capability | Application can run multiple instances (stateless, or with shared session store) | Critical |
| Auto-scaling triggers | Scaling based on relevant metrics (request rate, queue depth, CPU) not just CPU | High |
| Scale-up speed | Time from trigger to new instance serving traffic | High |
| Scale-down policy | Aggressive scale-down with cool-down to prevent thrashing | Medium |
| Minimum instances | Minimum count set to avoid cold-start latency for first users | Medium |
| Maximum instances | Maximum set with cost alerts to prevent runaway scaling | High |
| Scaling metrics lag | Metrics used for scaling have too much delay to be effective | Medium |
| Stateful components | Session affinity, local file storage, in-memory state preventing scaling | High |
| Database scaling | Database is the bottleneck but has no read replicas or sharding strategy | High |
| Queue-based scaling | Worker count not tied to queue depth | Medium |

### Common Anti-Patterns (grep targets)

| Language | Pattern | Issue |
|----------|---------|-------|
| Code | `session\[` or `flask\.session\[` with default (in-memory) session store | Stateful; can't scale horizontally |
| Code | File writes to local filesystem in request handler | Local state prevents scaling |
| Terraform/K8s | `min_size = .*max_size` (same value) | Auto-scaling disabled |
| Terraform | `cooldown = 0\|cooldown_period = 0` | No scale-down cooldown; thrashing |
| K8s HPA | Only `cpu` target without custom metrics | Scaling on wrong signal |

### Key Metrics

- Scale-up latency (trigger to ready)
- Instances/pods over time
- Request rate vs instance count correlation
- Cost during peak vs off-peak
- Scaling events per day

### Industry Tools

| Tool | Purpose |
|------|---------|
| KEDA (Kubernetes Event-Driven Autoscaler) | Scale on queue depth, cron, custom metrics |
| AWS Auto Scaling | Predictive + reactive scaling |
| GKE Autopilot | Automated pod-level right-sizing |
| Azure VMSS | Virtual machine scale sets |
| `k6` / `locust` | Load testing to validate scaling behavior |

---

## Category 17: Storage & I/O Optimization

**Audit question:** "Are storage operations efficient, using appropriate formats and access patterns?"

### What to Check

| Check | What to look for | Severity |
|-------|-----------------|----------|
| File format for analytics | Using CSV/JSON for analytical workloads instead of Parquet/ORC | High |
| Compression | Data stored uncompressed when compression would save significant storage | Medium |
| Read amplification | Reading entire files/objects when only a subset of data is needed | High |
| Write amplification | Small writes causing disproportionate I/O (random writes to SSD, frequent small files in object storage) | Medium |
| Storage class selection | Hot storage for cold data (S3 Standard vs S3 Glacier, Premium vs Standard SSD) | High |
| Disk I/O bottleneck | Application disk-bound (I/O wait > 20%) | High |
| Object storage patterns | Too many small objects (< 1MB) in S3/GCS, or too few large objects | Medium |
| Temporary file cleanup | Temp files created but never deleted | Medium |
| Synchronous file I/O | Blocking file operations on the request path | High |
| Log file growth | Application logs growing without rotation or archival | Medium |
| Database storage engine | InnoDB vs MyISAM, or wrong index type for access pattern | Medium |

### Common Anti-Patterns (grep targets)

| Language | Pattern | Issue |
|----------|---------|-------|
| Python | `open\(.*'w'\)` in a hot path or request handler | Synchronous file I/O on request path |
| Python | `to_csv\(\)` for data used analytically downstream | Should use Parquet |
| Any | `tmpfile\|tempfile\|mktemp` without cleanup/context manager | Temp file leak |
| SQL | `TEXT\|BLOB` column type for frequently queried data | Full table scan on large text |
| Terraform | `storage_type = "io1\|gp2"` (outdated or expensive) | Suboptimal storage type |
| Terraform | `transition.*days = ` not configured in S3 lifecycle | No storage tiering |

### Key Metrics

- IOPS consumed vs provisioned
- I/O wait percentage
- Storage cost per GB by tier
- Read/write throughput (MB/s)
- Object count and size distribution (object storage)

### Industry Tools

| Tool | Purpose |
|------|---------|
| `iostat` / `iotop` | Disk I/O analysis |
| `fio` | Storage benchmark tool |
| S3 Storage Lens / S3 Analytics | Object storage usage and access pattern analysis |
| `parquet-tools` / `pyarrow` | Parquet file inspection |
| Delta Lake `OPTIMIZE` | Small file compaction |
| `ncdu` / `du` | Disk usage analysis |

---

## Category 18: Profiling & Benchmarking

**Audit question:** "Is there a systematic approach to measuring and tracking performance?"

### What to Check

| Check | What to look for | Severity |
|-------|-----------------|----------|
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

### Common Anti-Patterns (grep targets)

| Language | Pattern | Issue |
|----------|---------|-------|
| Test config | No `performance\|benchmark\|load-test\|perf` directory or config | Missing performance tests |
| CI config | No performance test step in CI/CD pipeline | No regression detection |
| Any | `# TODO.*performance\|# TODO.*benchmark\|# FIXME.*slow` | Acknowledged performance debt |
| Test files | `time\.sleep\|Thread\.sleep` in performance tests | Artificial delays invalidate results |

### Key Metrics

- Response time percentiles (p50, p95, p99) by endpoint
- Throughput (requests/sec at various concurrency levels)
- Error rate under load
- Resource utilization under load (CPU, memory, connections)
- Performance trend over time (regression detection)

### Industry Tools

| Tool | Language | Purpose |
|------|----------|---------|
| `k6` | Any | Modern load testing with JavaScript scripts |
| `locust` | Python | Distributed load testing |
| `wrk` / `wrk2` | Any | HTTP benchmarking |
| `hey` | Any | HTTP load generator |
| `ab` (Apache Bench) | Any | Simple HTTP benchmarking |
| `pytest-benchmark` | Python | Micro-benchmarking in pytest |
| `hyperfine` | CLI | Command-line benchmarking |
| `Benchmark.js` | JS | JavaScript micro-benchmarking |
| `JMH` (Java Microbenchmark Harness) | Java | JVM micro-benchmarking |
| `BenchmarkDotNet` | .NET | .NET benchmarking |
| Grafana k6 Cloud | Any | Managed load testing with analytics |
| `artillery` | Any | Load testing and monitoring |
| `gatling` | JVM | High-performance load testing |
| Continuous Benchmark (GitHub Action) | Any | Performance regression detection in CI |

---

## Category 19: Logging & Debug Output in Production

**Audit question:** "Is production logging efficient, not generating unnecessary I/O or storage cost?"

### What to Check

| Check | What to look for | Severity |
|-------|-----------------|----------|
| Debug logging in production | DEBUG or TRACE level enabled in production configuration | High |
| Verbose logging in hot paths | Logging inside tight loops or per-item in bulk operations | High |
| Log argument evaluation | Expensive operations in log arguments that execute even when log level is disabled | Medium |
| Excessive stack traces | Stack traces logged for expected/handled exceptions | Medium |
| Log volume | Log output > 1GB/day for a single service without clear justification | Medium |
| Synchronous logging | Logging that blocks the request thread (synchronous file write, network call) | High |
| Duplicate log entries | Same event logged at multiple levels or locations | Low |
| Missing log sampling | High-frequency events logged at 100% instead of sampled | Medium |

### Common Anti-Patterns (grep targets)

| Language | Pattern | Issue |
|----------|---------|-------|
| Python | `logging\.debug\(f"` or `logging\.debug\(".*"\.format\(` | Eager string evaluation in debug |
| Python | `logger\.\w+\(.*json\.dumps\(` | Expensive serialization even if log level is disabled |
| Java | `logger\.debug\("" \+` | String concatenation even if debug is off; use `{}` placeholders |
| Any | `log\.\w+\(` inside `for\|while\|each` (high-iteration loop body) | Per-iteration logging overhead |
| Config | `level.*DEBUG\|level.*TRACE\|LOG_LEVEL.*debug` in production config | Debug logging in production |
| Python | `traceback\.print_exc\(\)\|traceback\.format_exc\(\)` for handled exceptions | Unnecessary stack trace |

### Key Metrics

- Log volume (GB/day, lines/sec)
- Log storage cost (monthly)
- Log write latency (impact on request latency)
- Log level distribution (DEBUG should be 0% in production)

### Industry Tools

| Tool | Purpose |
|------|---------|
| Log level configuration (per-module) | Enable DEBUG only for the module being investigated |
| Structured logging with lazy evaluation | `logger.debug("msg %s", expensive_fn)` vs `f"msg {expensive_fn()}"` |
| Log sampling (OTel Collector, Fluent Bit) | Sample high-volume log sources |
| Vector / Fluent Bit pipeline | Filter/transform/route logs before storage |

---

## Category 20: Regex & String Processing

**Audit question:** "Are string operations and regex patterns efficient and not causing performance bottlenecks?"

### What to Check

| Check | What to look for | Severity |
|-------|-----------------|----------|
| Regex compilation in loops | Compiling the same regex pattern on every iteration | High |
| Catastrophic backtracking | Regex patterns vulnerable to ReDoS (nested quantifiers, overlapping alternatives) | Critical |
| String concatenation in loops | Building strings character-by-character or with `+=` | Medium |
| Unnecessary regex | Using regex for simple string operations (contains, startswith, split) | Low |
| Unicode handling | String operations not handling multi-byte characters correctly | Medium |
| String interning absence | Many identical strings allocated separately (common in parsing) | Low |
| Regex vs parser | Using regex to parse structured formats (HTML, JSON, XML) | Medium |

### Common Anti-Patterns (grep targets)

| Language | Pattern | Issue |
|----------|---------|-------|
| Python | `re\.(match\|search\|findall\|sub)\(` inside a `for\|while` loop (without pre-compiled pattern) | Recompilation per iteration |
| Python | `re\.compile\(` inside function body (not module level) | Recompilation per call |
| JS | `new RegExp\(` inside a loop | Recompilation per iteration |
| Any | `(a+)+\|(a\|a)+\|(a\|b)*a(a\|b)*` patterns | Catastrophic backtracking risk |
| Any | Regex with `.*` repeated multiple times | Backtracking risk |
| Python | `html.*re\.\|re\..*<.*>` | Parsing HTML with regex |
| Python | `json.*re\.\|re\..*{.*}` | Parsing JSON with regex |

### Key Metrics

- Regex execution time per pattern
- String operation frequency in profiler
- ReDoS vulnerability count (static analysis)

### Industry Tools

| Tool | Purpose |
|------|---------|
| `regex101.com` | Regex testing with performance analysis |
| `recheck` / `redos-detector` | ReDoS vulnerability detection |
| Semgrep `python.lang.security.audit.regex-dos` | Static ReDoS detection |
| `re2` library (Google) | Linear-time regex engine (no backtracking) |
| `hyperscan` (Intel) | High-performance regex matching |

---

## Summary: Phase Structure Recommendation

Based on the research, the optimization audit skill should follow the same two-mode (Planning/Audit), two-tier (Standard/Enterprise) pattern as the security and observability audits. Recommended phase structure:

| Phase | Name | Mode | Research Category | Purpose |
|-------|------|------|-------------------|---------|
| 0 | Anti-Pattern Scan | Audit | 1, 2, 3, 20 | Fast grep for known performance anti-patterns |
| 1 | Discovery | Both | All | Map system, tech stack, deployment, workload profile |
| 2 | Algorithm & Data Structure Efficiency | Audit | 1 | Big-O analysis, data structure selection, hot path review |
| 3 | Memory Management | Audit | 2 | Leak detection, allocation patterns, cache sizing |
| 4 | Concurrency & Parallelism | Audit | 3 | Thread pools, async correctness, lock contention |
| 5 | Database & Query Optimization | Both | 4, 5, 8 | N+1, indexing, connection pooling, query analysis |
| 6 | Caching Strategy | Both | 6 | Cache layers, invalidation, hit ratios, HTTP caching |
| 7 | Serialization & Network | Audit | 7, 9 | Data format, compression, protocol optimization |
| 8 | Frontend & API Optimization | Audit | 10, 11 | Bundle size, Core Web Vitals, API response shaping |
| 9 | Data Pipeline Efficiency | Both | 14 | Batch/stream, incremental, format, skew |
| 10 | Container & Startup Optimization | Audit | 12, 13 | Image size, build caching, cold start |
| 11 | Cloud Cost & Right-Sizing | Both | 15, 16, 17 | Resource utilization, auto-scaling, storage tiering |
| 12 | Profiling & Benchmarking Posture | Both | 18 | Performance testing, regression detection, budgets |
| 13 | Findings Report | Both | All | Final report with severity, impact, ROI estimates |

### Conditional Phases

- **Phase 8 (Frontend):** Only if frontend code exists (HTML, CSS, JS/TS, React, Vue, etc.)
- **Phase 9 (Data Pipeline):** Only if ETL/ELT, dbt, Spark, Airflow, or similar pipeline tools are detected
- **Phase 10 (Container):** Only if Dockerfiles, docker-compose, or Kubernetes manifests exist
- **Phase 11 (Cloud Cost):** Only if IaC or cloud deployment configuration exists

### Severity Classification (Optimization-Specific)

| Severity | Criteria | Action | SLA |
|----------|----------|--------|-----|
| **Critical** | Causes outages, OOM crashes, connection exhaustion, quadratic algorithms on user-facing paths, unbounded memory growth | Fix immediately | Block release |
| **High** | Measurable performance degradation > 2x expected; N+1 queries, missing indexes on production queries, no connection pooling, missing compression | Fix before next release | 1 sprint |
| **Medium** | Suboptimal but functional; oversized resources, missing caching, debug logging in production, suboptimal serialization | Schedule fix | 2 sprints |
| **Low** | Best practice deviation; naming conventions, minor allocation patterns, potential micro-optimizations | Track in backlog | Best effort |

### Templates (Recommended)

| Template | Primary Categories |
|----------|-------------------|
| `algorithm-complexity.md` | Big-O analysis, data structure selection, profiling tools per language |
| `database-optimization.md` | N+1 detection, indexing strategy, EXPLAIN analysis, connection pooling, ORM patterns |
| `caching-strategies.md` | Cache layers, invalidation patterns, HTTP caching, CDN, memoization |
| `concurrency-patterns.md` | Thread pool sizing, async/await correctness, lock contention, backpressure |
| `frontend-performance.md` | Core Web Vitals, bundle optimization, image optimization, rendering patterns |
| `pipeline-efficiency.md` | Batch/stream, incremental processing, storage formats, partitioning, skew |
| `cloud-cost-optimization.md` | Right-sizing, auto-scaling, spot instances, storage tiering, cost tools |
| `profiling-benchmarking.md` | Performance testing tools, regression detection, performance budgets, methodology |

---

## Key Design Decisions (Recommendations)

1. **Mirrors security-audit and observability-audit structure** -- two modes, two tiers, phased execution with severity classification. Consistency across the skill suite.

2. **Measurement-first philosophy** -- unlike security (which has binary pass/fail for many checks), optimization is relative. Every finding should quantify the impact: "N+1 query adds ~200ms per page load" not just "N+1 query found."

3. **ROI-oriented reporting** -- findings should estimate the effort vs impact trade-off: quick wins (5 min fix, 10x improvement) vs long-term investments (multi-sprint refactor, 2x improvement).

4. **Language-agnostic phases, language-specific templates** -- SKILL.md defines the methodology; templates contain per-language grep patterns, profiling tools, and code examples.

5. **Fix-as-you-go with caveats** -- optimization fixes can have unintended consequences (caching introduces staleness, parallelism introduces race conditions). The skill should fix obvious wins (add missing index, enable compression, fix N+1) but recommend benchmarking for structural changes.

6. **Phase 0 (Anti-Pattern Scan) is the workhorse** -- most optimization audit value comes from grep-able anti-patterns. This phase should be comprehensive with per-language pattern tables.

7. **Profiling phase validates grep findings** -- grep finds suspects; profiling confirms them. The skill should recommend profiling for any High/Critical finding that cannot be confirmed through static analysis alone.

8. **Conditional phases keep the audit focused** -- not every codebase has a frontend, data pipelines, or cloud infrastructure. Skip irrelevant phases to keep signal-to-noise high.
