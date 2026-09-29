# Caching Strategies Reference

Comprehensive guide to cache architecture, invalidation patterns, stampede protection, HTTP caching, memoization, and cache observability. Use during Phase 6 (Caching Strategy) of the optimization audit.

## Purpose

Answer: "Are cacheable operations identified and cached at the right layer with appropriate invalidation?"

## Checklist

Before auditing, identify:

- [ ] What data stores exist (databases, APIs, file systems, object stores)
- [ ] Which operations are repeated with identical inputs
- [ ] What freshness requirements exist per data type (real-time, near-real-time, eventual)
- [ ] Whether a distributed cache (Redis, Memcached) is already deployed
- [ ] What HTTP caching headers are currently set
- [ ] Whether a CDN is in use and how it is configured
- [ ] What in-process caching is already applied (memoization, object caches)
- [ ] What the read-to-write ratio is for key data paths

---

## 5-Layer Cache Architecture

Each layer serves a different latency band and scope. Apply the highest layer that satisfies freshness requirements.

| Layer | What | Latency | Scope | Typical Hit Rate | When to Use |
|-------|------|---------|-------|------------------|-------------|
| **L1: In-Process** | `lru_cache`, Caffeine, `node-cache` | ~1-10 us | Per process | 60-95% | Pure functions, config, small reference data |
| **L2: Distributed** | Redis, Memcached, Hazelcast | ~0.5-5 ms | Cross-process | 80-99% | Session data, API responses, shared computed results |
| **L3: HTTP** | `Cache-Control`, `ETag`, `Last-Modified` | Variable | Per client/proxy | 40-90% | API responses, browser resources, reverse proxy |
| **L4: CDN** | CloudFront, Cloudflare, Fastly | ~5-50 ms (edge) | Global edge | 85-99% | Static assets, public API responses, media |
| **L5: Precomputed** | Materialized views, precomputed tables | ~0 at read | Per data store | 100% (by design) | Dashboards, reports, aggregations, search indexes |

### L1: In-Process Cache

Fastest possible cache — data lives in the same memory space as the application.

```python
# Python — functools (stdlib). ALWAYS set maxsize.
from functools import lru_cache

@lru_cache(maxsize=1024)
def get_user_permissions(user_id: int) -> list[str]:
    return db.query("SELECT permission FROM user_perms WHERE user_id = %s", user_id)
```

```java
// Java — Caffeine (recommended over Guava Cache for new projects)
Cache<Long, List<String>> permissionCache = Caffeine.newBuilder()
    .maximumSize(10_000)
    .expireAfterWrite(Duration.ofMinutes(5))
    .recordStats()
    .build();

List<String> perms = permissionCache.get(userId, id -> db.queryPermissions(id));
```

### L2: Distributed Cache

Shared across all application instances. Use for data too expensive to recompute per-process.

```python
# Python — Redis with explicit TTL
r = redis.Redis(host="cache.internal", port=6379, decode_responses=True)

def get_product_catalog(category_id: str) -> dict:
    cache_key = f"catalog:{category_id}"
    cached = r.get(cache_key)
    if cached:
        return json.loads(cached)
    catalog = db.query_catalog(category_id)
    r.set(cache_key, json.dumps(catalog), ex=300)  # 5 min TTL
    return catalog
```

### L3-L4: HTTP and CDN Caching

See the [HTTP Caching](#http-caching) section below.

### L5: Precomputed / Materialized

Zero read-time cost — the answer is already stored.

```sql
-- PostgreSQL — materialized view for dashboard aggregation
CREATE MATERIALIZED VIEW daily_sales_summary AS
SELECT date_trunc('day', created_at) AS sale_date, product_category,
       COUNT(*) AS order_count, SUM(total_amount) AS revenue
FROM orders GROUP BY 1, 2;

-- Refresh on schedule (e.g., every hour via cron or pg_cron)
REFRESH MATERIALIZED VIEW CONCURRENTLY daily_sales_summary;
```

---

## Cache Invalidation Patterns

Choose the pattern that matches your consistency requirements.

| Pattern | Consistency | Complexity | Write Latency | Best For |
|---------|------------|------------|---------------|----------|
| **TTL-based** | Eventual (bounded staleness) | Low | Low | Reference data, configs, public content |
| **Event-driven** | Near real-time | Medium | Medium | User-specific data, inventory, prices |
| **Write-through** | Strong | Medium | High (sync write) | Session data, auth tokens |
| **Write-behind** | Eventual | High | Low (async write) | Analytics, audit logs, non-critical updates |
| **Cache-aside** | Eventual | Low | Low | General purpose, most common pattern |

### TTL-Based Invalidation

```python
# GOOD — TTL matched to data freshness requirements
r.set("exchange_rate:USD_EUR", rate, ex=60)       # Financial: 1 min
r.set("product:123:details", details, ex=300)      # Catalog: 5 min
r.set("static:country_list", countries, ex=86400)  # Reference: 24 hr
```

```python
# BAD — no TTL (cache grows forever, data goes stale indefinitely)
r.set("exchange_rate:USD_EUR", rate)
r.set("product:123:details", details)
```

### Event-Driven Invalidation

```python
# GOOD — invalidate on write
def update_product(product_id: int, data: dict):
    db.execute("UPDATE products SET ... WHERE id = %s", product_id)
    r.delete(f"product:{product_id}:details")    # Invalidate specific key
    r.delete(f"catalog:{data['category_id']}")   # Invalidate parent collection
```

```python
# BAD — write to DB without invalidating cache
def update_product(product_id: int, data: dict):
    db.execute("UPDATE products SET ... WHERE id = %s", product_id)
    # Cache still serves stale data until TTL expires
```

### Write-Through

Write to cache and data store simultaneously. The cache is always up to date.

```python
# GOOD — write-through pattern
def save_session(session_id: str, data: dict):
    serialized = json.dumps(data)
    db.execute("UPSERT INTO sessions (id, data) VALUES (%s, %s)", session_id, serialized)
    r.set(f"session:{session_id}", serialized, ex=3600)
```

### Write-Behind (Write-Back)

Write to cache immediately, flush to data store asynchronously. Lower write latency but risks data loss if the process crashes before flush. Pattern: write to Redis immediately, buffer writes, periodically batch-insert to the database.

### Cache-Aside (Lazy Loading)

The most common pattern. Application manages cache reads and writes explicitly.

```python
# GOOD — cache-aside with TTL and error handling
def get_user_profile(user_id: int) -> dict:
    cache_key = f"user:{user_id}:profile"
    try:
        cached = r.get(cache_key)
        if cached:
            return json.loads(cached)
    except redis.RedisError:
        pass  # Cache failure should not break the application
    profile = db.query("SELECT * FROM users WHERE id = %s", user_id)
    try:
        r.set(cache_key, json.dumps(profile), ex=300)
    except redis.RedisError:
        pass  # Best-effort caching
    return profile
```

```python
# BAD — no error handling (cache outage breaks reads), no TTL
def get_user_profile(user_id: int) -> dict:
    cached = r.get(f"user:{user_id}:profile")  # Throws on Redis failure
    if cached:
        return json.loads(cached)
    profile = db.query("SELECT * FROM users WHERE id = %s", user_id)
    r.set(f"user:{user_id}:profile", json.dumps(profile))  # No TTL
    return profile
```

---

## Stampede Protection

When a popular cache entry expires, many concurrent requests may try to recompute it simultaneously — the "thundering herd" problem.

### Lock-Based (Mutex)

Only one request recomputes; others wait or serve stale data.

```python
# Python — Redis lock for stampede protection
def get_with_lock(cache_key: str, compute_fn, ttl: int = 300, lock_ttl: int = 10):
    cached = r.get(cache_key)
    if cached:
        return json.loads(cached)
    lock = r.lock(f"lock:{cache_key}", timeout=lock_ttl, blocking_timeout=5)
    if lock.acquire(blocking=True):
        try:
            cached = r.get(cache_key)  # Double-check after acquiring lock
            if cached:
                return json.loads(cached)
            value = compute_fn()
            r.set(cache_key, json.dumps(value), ex=ttl)
            return value
        finally:
            lock.release()
    raise TimeoutError("Cache recomputation in progress")
```

**Go:** Use `golang.org/x/sync/singleflight` — `group.Do(key, computeFn)` deduplicates concurrent requests for the same key. Only one goroutine computes; others block and receive the same result.

### Probabilistic Early Expiration (XFetch)

Recompute before expiry, with probability increasing as expiry approaches.

```python
# Python — XFetch algorithm
import math, random

def xfetch_get(cache_key: str, compute_fn, ttl: int = 300, beta: float = 1.0):
    """beta controls eagerness: higher beta = earlier recomputation."""
    cached = r.get(cache_key)
    remaining_ttl = r.ttl(cache_key)
    if cached and remaining_ttl > 0:
        delta = ttl * beta
        if remaining_ttl > delta * (-math.log(random.random())):
            return json.loads(cached)  # Serve cached — not yet time to refresh
    value = compute_fn()
    r.set(cache_key, json.dumps(value), ex=ttl)
    return value
```

### Stale-While-Revalidate

Serve the stale value immediately and recompute asynchronously in the background. Store entries with an extended TTL (`stale_ttl`); when the primary TTL window has passed but the entry still exists, return the stale value and spawn a background thread/task to refresh it. On a complete miss, compute synchronously.

---

## HTTP Caching

HTTP caching reduces server load by allowing clients, proxies, and CDNs to serve cached responses.

### Cache-Control Directives

| Directive | Meaning | Use Case |
|-----------|---------|----------|
| `max-age=N` | Response is fresh for N seconds | Most cacheable responses |
| `s-maxage=N` | Override `max-age` for shared caches (CDNs, proxies) | Different TTL for CDN vs browser |
| `no-cache` | Must revalidate with origin before using cached copy | Dynamic content that changes frequently |
| `no-store` | Do not cache at all | Sensitive data (PII, auth tokens, financial) |
| `private` | Only browser may cache (not CDN/proxy) | User-specific responses |
| `public` | Any cache may store | Shared public content |
| `must-revalidate` | Once stale, must revalidate before use | Critical data freshness |
| `stale-while-revalidate=N` | Serve stale for N seconds while revalidating in background | Non-critical freshness, improved UX |
| `stale-if-error=N` | Serve stale for N seconds if origin returns error | Resilience during outages |
| `immutable` | Content will never change (skip revalidation) | Versioned static assets (`app.a1b2c3.js`) |

### Conditional Requests

| Header (Response) | Header (Request) | Mechanism |
|--------------------|-----------------|-----------|
| `ETag: "abc123"` | `If-None-Match: "abc123"` | Content hash comparison |
| `Last-Modified: Thu, 01 Jan 2026 00:00:00 GMT` | `If-Modified-Since: Thu, 01 Jan 2026 00:00:00 GMT` | Timestamp comparison |

**ETag is preferred** over Last-Modified because it handles sub-second changes and content-based validation.

### Vary Header

The `Vary` header tells caches that the response varies by certain request headers. Without it, a cache may serve the wrong response variant. `Vary: *` effectively disables caching — avoid it.

```
Vary: Accept-Encoding, Accept-Language
```

### Framework-Specific Examples

**Express (Node.js):**

```javascript
// GOOD — proper Cache-Control for different response types
app.use("/static", express.static("public", { maxAge: "1y", immutable: true }));

app.get("/api/products", (req, res) => {
  res.set("Cache-Control", "public, max-age=60, stale-while-revalidate=300");
  res.set("ETag", computeETag(products));
  if (req.headers["if-none-match"] === res.get("ETag")) return res.status(304).end();
  res.json(products);
});
```

```javascript
// BAD — no cache headers (browser behavior is unpredictable)
app.get("/api/products", (req, res) => { res.json(products); });
```

**FastAPI (Python):**

```python
# GOOD — Cache-Control and ETag support
@app.get("/api/products")
async def get_products(request: Request, response: Response):
    products = await fetch_products()
    etag = md5(json.dumps(products).encode()).hexdigest()
    if request.headers.get("if-none-match") == f'"{etag}"':
        return Response(status_code=304)
    response.headers["Cache-Control"] = "public, max-age=60, stale-while-revalidate=300"
    response.headers["ETag"] = f'"{etag}"'
    return products
```

**Django:** Use `@cache_control(public=True, max_age=60)` for header-based caching, `@cache_page(60 * 15)` for full page caching.

**Go:** Set `w.Header().Set("Cache-Control", "public, max-age=60")` and `w.Header().Set("ETag", etag)` manually. Check `r.Header.Get("If-None-Match")` and return `304` on match.

---

## Memoization Patterns

Memoization caches function return values based on arguments. Use for pure functions called repeatedly with the same inputs.

### Python

```python
# GOOD — lru_cache with bounded size
from functools import lru_cache

@lru_cache(maxsize=512)
def compute_tax(amount: float, state: str) -> float:
    return amount * fetch_tax_rate(state)
```

```python
# BAD — unbounded cache (memory leak for unbounded input space)
@lru_cache(maxsize=None)  # Grows forever
def compute_tax(amount: float, state: str) -> float:
    return amount * fetch_tax_rate(state)
```

```python
# GOOD — TTL-based memoization with cachetools
from cachetools import TTLCache, cached

cache = TTLCache(maxsize=1024, ttl=300)

@cached(cache, lock=threading.Lock())
def get_exchange_rate(from_ccy: str, to_ccy: str) -> float:
    return external_api.get_rate(from_ccy, to_ccy)
```

### JavaScript / TypeScript

```typescript
// GOOD — Map-based memoize with max size
function memoize<T extends (...args: any[]) => any>(
  fn: T, options: { maxSize?: number } = {}
): T {
  const { maxSize = 1000 } = options;
  const cache = new Map<string, ReturnType<T>>();
  return ((...args: Parameters<T>): ReturnType<T> => {
    const key = JSON.stringify(args);
    if (cache.has(key)) return cache.get(key)!;
    const result = fn(...args);
    if (cache.size >= maxSize) cache.delete(cache.keys().next().value);
    cache.set(key, result);
    return result;
  }) as T;
}
```

```typescript
// BAD — Map-based cache without eviction (memory leak)
const cache = new Map<string, any>();
function getPermissions(userId: string) {
  if (cache.has(userId)) return cache.get(userId);
  const perms = db.queryPermissions(userId);
  cache.set(userId, perms);  // Never evicted — grows forever
  return perms;
}
```

### Go

```go
// GOOD — bounded cache with sync.RWMutex, TTL, and max size
// Use github.com/dgraph-io/ristretto or github.com/hashicorp/golang-lru for production
type MemCache[K comparable, V any] struct {
    mu      sync.RWMutex
    entries map[K]struct{ Value V; Expiry time.Time }
    maxSize int
    ttl     time.Duration
}
```

```go
// BAD — sync.Map without eviction or TTL (grows forever)
var cache sync.Map
func GetUser(id string) *User {
    if v, ok := cache.Load(id); ok { return v.(*User) }
    user := db.QueryUser(id)
    cache.Store(id, user)  // Never evicted
    return user
}
```

### Java

```java
// GOOD — Caffeine cache with size limit, TTL, and metrics
LoadingCache<String, UserProfile> profileCache = Caffeine.newBuilder()
    .maximumSize(10_000)
    .expireAfterWrite(Duration.ofMinutes(5))
    .refreshAfterWrite(Duration.ofMinutes(4))  // Async refresh before expiry
    .recordStats()
    .build(userId -> userRepository.findById(userId));
```

```java
// BAD — HashMap as cache without eviction or thread safety
private static final Map<String, UserProfile> cache = new HashMap<>();
public UserProfile getProfile(String userId) {
    if (cache.containsKey(userId)) return cache.get(userId);
    UserProfile profile = userRepository.findById(userId);
    cache.put(userId, profile);  // Grows forever, not thread-safe
    return profile;
}
```

---

## Cache Metrics

Monitor these metrics to validate cache effectiveness and detect problems.

| Metric | Target | What It Tells You | Action If Off-Target |
|--------|--------|-------------------|---------------------|
| **Hit ratio** | > 90% | % of requests served from cache | Increase TTL, warm cache, review eviction policy |
| **Miss ratio** | < 10% | % of requests hitting origin | Investigate key distribution, check for cache-busting |
| **Eviction rate** | Low, steady | Cache is full and evicting entries | Increase cache size or reduce TTL |
| **Latency (get/set)** | < 1ms (L2) | Cache operation overhead | Check network, connection pool, serialization |
| **Memory usage** | < 80% of max | Cache memory consumption | Right-size max memory, review value sizes |
| **Key count** | Below max | Number of cached entries | Check for key-space explosion |

### Redis INFO Stats Example

```bash
# Hit/miss ratio
redis-cli INFO stats | grep -E "keyspace_hits|keyspace_misses"
# keyspace_hits:1234567    keyspace_misses:12345
# Hit ratio = 1234567 / (1234567 + 12345) = 99.0% — healthy

# Memory usage
redis-cli INFO memory | grep -E "used_memory_human|maxmemory_human|mem_fragmentation_ratio"
# used_memory_human:2.50G   maxmemory_human:4.00G   mem_fragmentation_ratio:1.12

# Eviction stats
redis-cli INFO stats | grep evicted_keys
# evicted_keys:0 — healthy    evicted_keys:50000 — cache too small
```

### Application-Level Cache Metrics

```python
# Python — expose cache stats as Prometheus metrics
from prometheus_client import Counter, Gauge

cache_hits = Counter("app_cache_hits_total", "Cache hits", ["cache_name"])
cache_misses = Counter("app_cache_misses_total", "Cache misses", ["cache_name"])
cache_size = Gauge("app_cache_size", "Current cache entry count", ["cache_name"])

def cached_get(cache_name: str, key: str, compute_fn):
    cached = cache.get(key)
    if cached is not None:
        cache_hits.labels(cache_name=cache_name).inc()
        return cached
    cache_misses.labels(cache_name=cache_name).inc()
    value = compute_fn()
    cache.set(key, value)
    cache_size.labels(cache_name=cache_name).set(cache.currsize)
    return value
```

---

## When NOT to Cache

| Situation | Why Not to Cache | What to Do Instead |
|-----------|-----------------|-------------------|
| **Write-heavy data** | Cache invalidated faster than read; low hit ratio | Optimize write path (batch, async) |
| **Security-sensitive data** | Cached PII/tokens increase attack surface | `Cache-Control: no-store`; encrypt if caching |
| **Rapidly changing data** | TTL must be extremely short to stay fresh | WebSockets, SSE, or conditional requests |
| **Low-latency sources** | Origin already fast (< 1ms); cache adds complexity | Measure before caching |
| **Strict consistency** | Stale data causes incorrect behavior | Write-through or skip caching |
| **Large, unique payloads** | Each response unique; cache will never hit | Cache shared components separately |
| **Low-traffic paths** | Entry expires before reuse | Focus caching on high-traffic paths |

### Decision Checklist

Before adding a cache:

1. **Read-to-write ratio > 10:1?** If not, caching may not help.
2. **Can the app tolerate stale data?** If not, caching adds complexity for little benefit.
3. **Is the origin slow enough?** Measure origin latency first.
4. **Is the key space bounded?** Unbounded key spaces lead to memory exhaustion.
5. **Do you have an invalidation plan?** If you cannot answer "how does the cache know the data changed," do not cache it.
6. **Can you monitor the cache?** An unmonitored cache is a liability.

---

## Cache immutability & identity-keyed staleness (P6)

Two failure modes that a bounded, correctly-invalidated cache still allows:

- **Return immutable or defensively copied.** A shared cached object handed back to callers must be **immutable** or **defensively copied** — returning a mutable shared object invites cross-caller corruption (one caller mutates it, every other caller sees the change). Copy **only** at the point an external API demands a mutable buffer, not preemptively — a preemptive copy on every read defeats the cache. In numpy, mark the cached array **read-only** (`arr.flags.writeable = False`) so a mutation fails loud rather than corrupting silently.
- **Never serve a modified-content path by its original identity.** A cache keyed on an **identity** (a frame id, a row key, an object id) serves a **stale/wrong** value when a caller passes *modified* content under that same identity. Any what-if / counterfactual / "modified input" path must be scored on its **own content**, never re-fetched by the original key. Prefer a **structural** guarantee — assert the modification is real, refuse a mismatched reuse — over a comment or convention.

*» e.g.* a cached filter-design array was returned `writeable=False` and copied only immediately before the one external call needing a mutable buffer; separately, a batched scorer scored a "keeper-removed" counterfactual over *explicit* content slices, never a frame-id re-fetch, and a later design made the mistake **structurally impossible** by asserting the derived-vs-original diff.

## Best Practices

- Start with L1 (in-process) caching for the highest-traffic, lowest-latency wins before adding distributed layers
- Always set a `maxsize` or memory limit on in-process caches — unbounded caches are memory leaks
- Always set a TTL — even a long one (24 hours) is better than no expiry
- Use cache-aside as the default pattern unless you have specific consistency requirements
- Implement stampede protection for any cache key that serves more than 100 requests per second
- Add `Cache-Control` headers to every HTTP response — do not rely on browser defaults
- Use `ETag` for dynamic content and `immutable` for versioned static assets
- Monitor hit ratio, eviction rate, and memory usage from day one
- Warm critical caches on deployment to avoid cold-start latency spikes
- Separate cache failure from application failure — a cache miss should fall through to the origin, not crash
- Version cache keys when the serialization format changes to avoid deserialization errors

## Anti-Patterns

- Caching without TTL or eviction — guarantees stale data and memory growth
- Using `Cache-Control: no-cache, no-store` on all responses including static assets
- Caching user-specific data in shared/public caches — serves one user's data to another
- Relying on cache for data durability — caches are ephemeral by design
- Cache key collisions from poor key design (e.g., using only `user_id` when response varies by locale)
- Ignoring `Vary` headers — causes CDNs and proxies to serve incorrect response variants
- Setting identical TTLs on all cache entries — causes synchronized expiration storms
- Using `@lru_cache` on methods without accounting for `self` (caches per-instance, not per-argument)
- Caching error responses with long TTLs — one transient failure poisons the cache for the TTL duration
