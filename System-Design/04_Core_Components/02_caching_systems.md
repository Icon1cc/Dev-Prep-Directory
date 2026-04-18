# Caching Systems

## What is Caching?

**Caching** stores copies of frequently accessed data in a fast-access storage layer to reduce latency and load on the primary data store.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Why Caching Matters                                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Without Cache:                   With Cache:                          │
│   ──────────────                   ───────────                          │
│                                                                         │
│   Request ─────► Database          Request ─────► Cache                │
│            100ms latency                       │    │                   │
│                                                │    │ 1ms (hit)        │
│                                                │    ▼                   │
│                                                │  Response             │
│                                                │                        │
│                                                └─(miss)─► Database     │
│                                                           100ms         │
│                                                               │         │
│                                                    Store ◄────┘         │
│                                                    in cache             │
│                                                                         │
│   Speed Comparison:                                                     │
│   ─────────────────                                                     │
│   • L1 CPU Cache:     ~1 ns                                            │
│   • L2 CPU Cache:     ~4 ns                                            │
│   • RAM:              ~100 ns                                          │
│   • SSD:              ~100 μs                                          │
│   • HDD:              ~10 ms                                           │
│   • Network (LAN):    ~1 ms                                            │
│   • Network (WAN):    ~100 ms                                          │
│                                                                         │
│   Cache is 100-1000x faster than database!                             │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Cache Placement

### 1. Client-Side Cache

```
┌─────────┐
│ Browser │ ← Caches static files, API responses
│  Cache  │   (localStorage, sessionStorage, HTTP cache)
└─────────┘
```

### 2. CDN Cache

```
┌─────────┐
│   CDN   │ ← Caches static content at edge locations
│  Cache  │   (images, CSS, JS, videos)
└─────────┘
```

### 3. Application Cache (Focus of this document)

```
┌─────────┐    ┌─────────┐    ┌──────────┐
│  App    │───►│  Cache  │───►│ Database │
│ Server  │    │ (Redis) │    │(Postgres)│
└─────────┘    └─────────┘    └──────────┘
```

### 4. Database Cache

```
┌──────────┐
│ Database │ ← Query cache, buffer pool
│  Cache   │   (internal to database)
└──────────┘
```

---

## Caching Strategies

### 1. Cache-Aside (Lazy Loading)

Application manages the cache. Most common pattern.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Cache-Aside Pattern                                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   READ:                                                                 │
│   ─────                                                                 │
│                                                                         │
│   ┌─────────┐     1. Check cache                                       │
│   │   App   │─────────────────────►┌─────────┐                         │
│   │         │                      │  Cache  │                         │
│   │         │◄─────────────────────└─────────┘                         │
│   │         │     2a. HIT: return data                                 │
│   │         │                                                          │
│   │         │     2b. MISS: query DB                                   │
│   │         │─────────────────────►┌─────────┐                         │
│   │         │                      │   DB    │                         │
│   │         │◄─────────────────────└─────────┘                         │
│   │         │     3. Store in cache                                    │
│   │         │─────────────────────►┌─────────┐                         │
│   └─────────┘                      │  Cache  │                         │
│                                    └─────────┘                         │
│                                                                         │
│   Code:                                                                 │
│   ─────                                                                 │
│   def get_user(user_id):                                               │
│       # 1. Check cache                                                 │
│       user = cache.get(f"user:{user_id}")                             │
│       if user:                                                         │
│           return user  # Cache hit                                     │
│                                                                         │
│       # 2. Cache miss - query database                                 │
│       user = db.query("SELECT * FROM users WHERE id = ?", user_id)    │
│                                                                         │
│       # 3. Store in cache for next time                                │
│       cache.set(f"user:{user_id}", user, ttl=3600)                    │
│       return user                                                      │
│                                                                         │
│   Pros:                          Cons:                                 │
│   ─────                          ─────                                 │
│   • Only caches what's needed    • Cache miss penalty (3 trips)        │
│   • Cache can be down (graceful) • Data can become stale               │
│   • Simple to implement          • App must handle cache logic         │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 2. Read-Through Cache

Cache is responsible for loading data from database.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Read-Through Pattern                                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌─────────┐     1. Request                                           │
│   │   App   │─────────────────────►┌─────────┐                         │
│   │         │                      │  Cache  │                         │
│   │         │                      │  (with  │                         │
│   │         │                      │ loader) │                         │
│   │         │                      └────┬────┘                         │
│   │         │                           │ 2. If miss, cache loads      │
│   │         │                           │    from DB                   │
│   │         │                           ▼                              │
│   │         │                      ┌─────────┐                         │
│   │         │                      │   DB    │                         │
│   │         │◄─────────────────────└─────────┘                         │
│   └─────────┘     3. Return data                                       │
│                                                                         │
│   App doesn't know about database - cache handles it                   │
│                                                                         │
│   Pros:                          Cons:                                 │
│   ─────                          ─────                                 │
│   • Simpler application code     • Cache must know how to load        │
│   • Consistent caching logic     • First request always slow          │
│   • Cache never has stale data   • Tight coupling cache ↔ DB          │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 3. Write-Through Cache

Data is written to cache AND database synchronously.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Write-Through Pattern                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌─────────┐     1. Write request                                     │
│   │   App   │─────────────────────►┌─────────┐                         │
│   │         │                      │  Cache  │                         │
│   │         │                      └────┬────┘                         │
│   │         │                           │ 2. Cache writes to DB        │
│   │         │                           │    (synchronous)             │
│   │         │                           ▼                              │
│   │         │                      ┌─────────┐                         │
│   │         │◄─────────────────────│   DB    │                         │
│   └─────────┘     3. Confirm write └─────────┘                         │
│                                                                         │
│   Every write goes to both cache AND database                          │
│                                                                         │
│   Pros:                          Cons:                                 │
│   ─────                          ─────                                 │
│   • Cache always has latest data • Write latency increased            │
│   • Data consistency             • Cache may store unused data        │
│   • Simple read path             • Both must succeed                  │
│                                                                         │
│   Best for: Read-heavy workloads with consistency requirements        │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 4. Write-Behind (Write-Back) Cache

Write to cache immediately, persist to database asynchronously.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Write-Behind Pattern                                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌─────────┐     1. Write request                                     │
│   │   App   │─────────────────────►┌─────────┐                         │
│   │         │                      │  Cache  │                         │
│   │         │◄─────────────────────└────┬────┘                         │
│   │         │     2. Immediate ack      │                              │
│   └─────────┘                           │ 3. Async write               │
│                                         │    (batched)                 │
│                                         ▼                              │
│                                    ┌─────────┐                         │
│                                    │   DB    │                         │
│                                    └─────────┘                         │
│                                                                         │
│   Write queue: [write1, write2, write3] ──► Batch write to DB         │
│                                                                         │
│   Pros:                          Cons:                                 │
│   ─────                          ─────                                 │
│   • Fast writes                  • Data loss risk if cache fails      │
│   • Reduced DB load              • Complexity of async writes         │
│   • Batching efficiency          • Eventual consistency               │
│                                                                         │
│   Best for: Write-heavy workloads where some data loss is acceptable  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 5. Write-Around Cache

Write directly to database, bypassing cache.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Write-Around Pattern                                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   WRITE:                          READ (Cache-Aside):                  │
│   ──────                          ────────────────────                  │
│   ┌─────────┐                     ┌─────────┐                          │
│   │   App   │                     │   App   │                          │
│   └────┬────┘                     └────┬────┘                          │
│        │ 1. Write directly             │ 1. Check cache               │
│        │                               ▼                               │
│        │                          ┌─────────┐                          │
│        │                          │  Cache  │                          │
│        │                          └────┬────┘                          │
│        │                               │ 2. Miss → query DB           │
│        ▼                               ▼                               │
│   ┌─────────┐                     ┌─────────┐                          │
│   │   DB    │                     │   DB    │                          │
│   └─────────┘                     └─────────┘                          │
│                                                                         │
│   Cache only populated on read (prevents caching write-once data)      │
│                                                                         │
│   Pros:                          Cons:                                 │
│   ─────                          ─────                                 │
│   • No cache pollution           • First read always slow             │
│   • Good for write-once data     • Higher read latency initially      │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Cache Invalidation

**The two hardest problems in computer science: cache invalidation and naming things.**

### Invalidation Strategies

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Cache Invalidation Strategies                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   1. TIME-TO-LIVE (TTL)                                                │
│      ──────────────────                                                 │
│      cache.set("user:123", data, ttl=3600)  # Expires in 1 hour       │
│                                                                         │
│      Pros: Simple, predictable                                         │
│      Cons: Can serve stale data until TTL expires                      │
│                                                                         │
│   2. EXPLICIT INVALIDATION                                             │
│      ───────────────────────                                            │
│      # When user is updated:                                           │
│      db.update("UPDATE users SET name = ? WHERE id = ?", name, id)    │
│      cache.delete("user:123")  # Invalidate cache                     │
│                                                                         │
│      Pros: No stale data                                               │
│      Cons: Must track all cache keys, can miss invalidations          │
│                                                                         │
│   3. EVENT-BASED INVALIDATION                                          │
│      ──────────────────────────                                         │
│      # Listen to database changes (CDC)                                │
│      def on_user_update(event):                                        │
│          cache.delete(f"user:{event.user_id}")                        │
│                                                                         │
│      Pros: Decoupled, catches all changes                              │
│      Cons: Infrastructure complexity, eventual consistency             │
│                                                                         │
│   4. VERSION-BASED INVALIDATION                                        │
│      ──────────────────────────                                         │
│      # Include version in key                                          │
│      cache.set(f"user:123:v{version}", data)                          │
│      # New version = old key naturally expires                         │
│                                                                         │
│      Pros: No explicit invalidation needed                             │
│      Cons: Storage overhead, stale versions linger                     │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Cache Eviction Policies

When cache is full, which entries to remove?

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Eviction Policies                                    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   1. LRU (Least Recently Used) - Most Common                           │
│      ─────────────────────────────────────────                          │
│      Evicts the entry that hasn't been accessed for the longest time   │
│                                                                         │
│      Access: A B C D E A C                                             │
│      Cache:  [A C E D B] → Evict B (oldest access)                     │
│                                                                         │
│   2. LFU (Least Frequently Used)                                       │
│      ───────────────────────────                                        │
│      Evicts the entry with the lowest access count                     │
│                                                                         │
│      A(5) B(2) C(8) D(1) → Evict D (lowest count)                     │
│                                                                         │
│   3. FIFO (First In, First Out)                                        │
│      ──────────────────────────                                         │
│      Evicts the oldest entry regardless of access pattern              │
│                                                                         │
│   4. Random                                                            │
│      ──────                                                             │
│      Randomly evicts an entry (simple, surprisingly effective)         │
│                                                                         │
│   5. TTL-based                                                         │
│      ─────────                                                          │
│      Evicts entries closest to expiration                              │
│                                                                         │
│   Comparison:                                                           │
│   ───────────                                                           │
│   Policy │ Pros                    │ Cons                              │
│   ───────┼─────────────────────────┼───────────────────────────────── │
│   LRU    │ Good general purpose    │ Scan-resistant issues            │
│   LFU    │ Keeps hot data          │ Slow to adapt to changes         │
│   FIFO   │ Simple, predictable     │ Ignores access patterns          │
│   Random │ Simple, no overhead     │ May evict hot data               │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Cache Problems and Solutions

### 1. Cache Stampede (Thundering Herd)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Cache Stampede                                       │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Problem:                                                              │
│   ────────                                                              │
│   Popular key expires → 1000 requests hit database simultaneously     │
│                                                                         │
│   Time=0: Cache has "popular_item"                                     │
│   Time=T: TTL expires, cache empty                                     │
│   Time=T+1ms: 1000 requests arrive                                     │
│        All 1000 → Cache MISS → All 1000 → Database                    │
│        💥 Database overwhelmed!                                        │
│                                                                         │
│   Solutions:                                                            │
│   ──────────                                                            │
│                                                                         │
│   1. LOCKING (Mutex)                                                   │
│      ────────────────                                                   │
│      First request acquires lock → fetches from DB → updates cache    │
│      Other requests wait for lock → then read from cache              │
│                                                                         │
│      def get_with_lock(key):                                           │
│          value = cache.get(key)                                        │
│          if value:                                                     │
│              return value                                              │
│          if cache.acquire_lock(f"lock:{key}"):                        │
│              try:                                                      │
│                  value = db.query(key)                                 │
│                  cache.set(key, value)                                 │
│              finally:                                                  │
│                  cache.release_lock(f"lock:{key}")                    │
│          else:                                                         │
│              # Wait and retry                                          │
│              time.sleep(0.1)                                           │
│              return cache.get(key)                                     │
│          return value                                                  │
│                                                                         │
│   2. EARLY EXPIRATION (Probabilistic)                                  │
│      ────────────────────────────────                                   │
│      Some requests refresh cache before TTL                            │
│                                                                         │
│   3. BACKGROUND REFRESH                                                │
│      ────────────────────                                               │
│      Worker refreshes popular keys before they expire                  │
│                                                                         │
│   4. STALE-WHILE-REVALIDATE                                           │
│      ───────────────────────                                            │
│      Return stale data immediately, refresh in background              │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 2. Cache Penetration

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Cache Penetration                                    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Problem:                                                              │
│   ────────                                                              │
│   Requests for non-existent data always hit database                   │
│   (Attacker requests user_id=-1 repeatedly)                            │
│                                                                         │
│   Request for "user:-1" → Cache MISS → Database → Not found           │
│   Next request → Cache MISS → Database → Not found                     │
│   (Database queried every time!)                                       │
│                                                                         │
│   Solutions:                                                            │
│   ──────────                                                            │
│                                                                         │
│   1. CACHE NULL VALUES                                                 │
│      ──────────────────                                                 │
│      cache.set("user:-1", NULL, ttl=300)  # Cache "not found"         │
│                                                                         │
│   2. BLOOM FILTER                                                      │
│      ────────────                                                       │
│      Check bloom filter first → if definitely not exists, skip DB     │
│                                                                         │
│      if not bloom_filter.might_contain("user:-1"):                    │
│          return None  # Definitely doesn't exist                       │
│      # Might exist, check DB                                           │
│                                                                         │
│   3. INPUT VALIDATION                                                  │
│      ────────────────                                                   │
│      Validate user_id format before querying                           │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 3. Hot Key Problem

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Hot Key Problem                                      │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Problem:                                                              │
│   ────────                                                              │
│   Single key gets massive traffic → single cache node overloaded       │
│   (Celebrity tweet, viral product, etc.)                               │
│                                                                         │
│   Solutions:                                                            │
│   ──────────                                                            │
│                                                                         │
│   1. LOCAL CACHE (L1)                                                  │
│      ─────────────────                                                  │
│      App server caches hot keys locally                                │
│      Client → Local Cache → Redis → Database                          │
│                                                                         │
│   2. REPLICATE HOT KEYS                                                │
│      ─────────────────────                                              │
│      Store same key on multiple shards                                 │
│      key → "key:0", "key:1", "key:2"                                  │
│      Read from random shard                                            │
│                                                                         │
│   3. RATE LIMITING                                                     │
│      ─────────────                                                      │
│      Limit requests per key                                            │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Redis: The Industry Standard

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Redis Overview                                       │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Key Features:                                                         │
│   ─────────────                                                         │
│   • In-memory data store                                               │
│   • Sub-millisecond latency                                            │
│   • Rich data structures (strings, lists, sets, hashes, sorted sets)  │
│   • Persistence options (RDB snapshots, AOF logs)                      │
│   • Replication and clustering                                         │
│   • Pub/sub messaging                                                  │
│   • Lua scripting                                                      │
│                                                                         │
│   Common Commands:                                                      │
│   ────────────────                                                      │
│   SET key value [EX seconds]    # Store with optional TTL             │
│   GET key                       # Retrieve value                       │
│   DEL key                       # Delete key                           │
│   INCR key                      # Atomic increment                     │
│   EXPIRE key seconds            # Set TTL                              │
│   TTL key                       # Get remaining TTL                    │
│   HSET hash field value         # Hash set                             │
│   HGET hash field               # Hash get                             │
│   LPUSH list value              # List push                            │
│   ZADD sorted_set score member  # Sorted set add                       │
│                                                                         │
│   Use Cases:                                                           │
│   ──────────                                                            │
│   • Session storage                                                    │
│   • Page caching                                                       │
│   • Leaderboards (sorted sets)                                         │
│   • Rate limiting                                                      │
│   • Real-time analytics                                                │
│   • Message queues                                                     │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## When to Use / When NOT to Use

### When to Use Caching

✅ Read-heavy workloads (read:write > 10:1)
✅ Data that doesn't change frequently
✅ Expensive computations
✅ High latency operations
✅ Hot data with temporal locality

### When NOT to Use

❌ Write-heavy workloads (cache invalidation nightmare)
❌ Data that changes frequently
❌ Strong consistency requirements
❌ Low latency already sufficient
❌ Simple queries on small datasets

---

## Interview Traps

| Trap | What They're Testing | Good Answer |
|------|---------------------|-------------|
| "How to handle cache invalidation?" | Understanding trade-offs | TTL for simplicity, explicit invalidation for consistency, event-based for scale |
| "Cache-aside vs read-through?" | Pattern knowledge | Cache-aside: app controls; Read-through: cache handles loading |
| "What if cache goes down?" | Resilience thinking | Graceful degradation to DB, circuit breaker, fallback |
| "How to prevent cache stampede?" | Problem-solving | Locking, early refresh, or stale-while-revalidate |

---

**Next:** Continue to [03_message_queues.md](./03_message_queues.md) to learn about async processing.
