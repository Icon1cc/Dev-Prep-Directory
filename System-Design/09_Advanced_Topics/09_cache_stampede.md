# Cache Stampede

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                          CACHE STAMPEDE                                       ║
║              When Cache Expiry Brings Down Your System                        ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

## What is Cache Stampede?

Cache stampede (also called cache breakdown or dog-piling) is a specific type of thundering herd that occurs when a cached item expires and multiple concurrent requests all try to regenerate it simultaneously.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      CACHE STAMPEDE VISUALIZED                               │
│                                                                              │
│  NORMAL OPERATION:                                                          │
│  ════════════════                                                           │
│                                                                              │
│  Request ──► Cache ──► HIT ──► Return cached value                         │
│  Request ──► Cache ──► HIT ──► Return cached value                         │
│  Request ──► Cache ──► HIT ──► Return cached value                         │
│                                                                              │
│  DB Load: 0 (all served from cache)                                        │
│                                                                              │
│                                                                              │
│  STAMPEDE (TTL expires):                                                    │
│  ═══════════════════════                                                    │
│                                                                              │
│  Request 1 ──► Cache ──► MISS ──► Query DB ──┐                             │
│  Request 2 ──► Cache ──► MISS ──► Query DB ──┤                             │
│  Request 3 ──► Cache ──► MISS ──► Query DB ──┤                             │
│  Request 4 ──► Cache ──► MISS ──► Query DB ──┼──► DATABASE                 │
│  Request 5 ──► Cache ──► MISS ──► Query DB ──┤    OVERWHELMED!             │
│  ...                                          │                             │
│  Request N ──► Cache ──► MISS ──► Query DB ──┘                             │
│                                                                              │
│  DB Load: N concurrent queries for SAME data!                              │
│                                                                              │
│  All N requests are doing the SAME expensive work                          │
│  Only one result is needed, but N are computed                             │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Why It's Particularly Dangerous

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                   WHY CACHE STAMPEDE IS DEADLY                               │
│                                                                              │
│  1. AMPLIFICATION EFFECT                                                    │
│     ────────────────────                                                    │
│     Popular item (1000 QPS) expires                                         │
│     → 1000 DB queries in the same second                                   │
│     → Each query might be expensive (joins, aggregations)                  │
│     → 1000x amplification of backend load                                  │
│                                                                              │
│  2. CASCADING FAILURE                                                       │
│     ─────────────────                                                       │
│     DB overwhelmed → Queries time out                                      │
│     → Cache never gets populated                                           │
│     → More requests pile up                                                │
│     → DB gets worse                                                         │
│     → Feedback loop of doom                                                │
│                                                                              │
│  3. SYNCHRONIZED EXPIRY                                                     │
│     ────────────────────                                                    │
│     Many items cached at same time (e.g., startup, bulk load)             │
│     → All expire together                                                   │
│     → Massive synchronized stampede                                        │
│                                                                              │
│  4. HOT KEY VULNERABILITY                                                   │
│     ───────────────────────                                                 │
│     Popular items have the worst stampedes                                  │
│     → More requests = bigger stampede                                      │
│     → Most important data = most vulnerable                                │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Solution 1: Cache Locking

The most common solution - only allow one request to regenerate the cache.

```python
import threading
import time
from typing import Any, Callable, Optional
import redis

class CacheLock:
    """
    Distributed lock to prevent cache stampede
    """

    def __init__(self, redis_client: redis.Redis, cache_client: redis.Redis):
        self.redis = redis_client
        self.cache = cache_client
        self.lock_timeout = 10  # seconds
        self.wait_timeout = 5   # seconds

    def get_with_lock(self, key: str, generator: Callable, ttl: int = 300) -> Any:
        """
        Get from cache, or regenerate with distributed lock
        """
        # Try cache first
        value = self.cache.get(key)
        if value is not None:
            return self._deserialize(value)

        # Cache miss - try to acquire lock
        lock_key = f"lock:{key}"
        lock_acquired = self.redis.set(
            lock_key,
            "1",
            nx=True,  # Only set if not exists
            ex=self.lock_timeout
        )

        if lock_acquired:
            try:
                # We got the lock - regenerate cache
                value = generator()
                self.cache.setex(key, ttl, self._serialize(value))
                return value
            finally:
                # Release lock
                self.redis.delete(lock_key)
        else:
            # Someone else is regenerating - wait for cache
            return self._wait_for_cache(key, generator, ttl)

    def _wait_for_cache(self, key: str, generator: Callable,
                        ttl: int, poll_interval: float = 0.05) -> Any:
        """
        Wait for cache to be populated by another process
        """
        start = time.time()

        while time.time() - start < self.wait_timeout:
            value = self.cache.get(key)
            if value is not None:
                return self._deserialize(value)
            time.sleep(poll_interval)

        # Timeout - try to regenerate ourselves
        # This handles case where lock holder crashed
        return self.get_with_lock(key, generator, ttl)

    def _serialize(self, value: Any) -> bytes:
        import json
        return json.dumps(value).encode()

    def _deserialize(self, data: bytes) -> Any:
        import json
        return json.loads(data.decode())


class LocalCacheLock:
    """
    In-process locking for single-server scenarios
    """

    def __init__(self):
        self.locks = {}
        self.lock_manager = threading.Lock()

    def get_with_lock(self, key: str, cache: dict,
                      generator: Callable, ttl: int = 300) -> Any:
        """
        Get from cache with per-key locking
        """
        # Try cache first (no lock needed)
        if key in cache and cache[key]['expires_at'] > time.time():
            return cache[key]['value']

        # Get or create lock for this key
        with self.lock_manager:
            if key not in self.locks:
                self.locks[key] = threading.Lock()
            lock = self.locks[key]

        with lock:
            # Double-check cache (another thread might have populated it)
            if key in cache and cache[key]['expires_at'] > time.time():
                return cache[key]['value']

            # Regenerate
            value = generator()
            cache[key] = {
                'value': value,
                'expires_at': time.time() + ttl
            }
            return value
```

## Solution 2: Probabilistic Early Expiration (XFetch)

Prevent stampede by probabilistically regenerating before expiry.

```python
import random
import math
import time
from typing import Any, Callable

class XFetchCache:
    """
    XFetch algorithm: Probabilistically refresh cache before expiry
    Paper: "Optimal Probabilistic Cache Stampede Prevention"
    """

    def __init__(self, cache, db, beta: float = 1.0):
        """
        beta: controls how early we start probabilistic refresh
              higher beta = earlier refresh = more DB load but fewer stampedes
        """
        self.cache = cache
        self.db = db
        self.beta = beta

    def get(self, key: str, generator: Callable, ttl: int = 300) -> Any:
        """
        Get with XFetch probabilistic early expiration
        """
        result = self.cache.get_with_metadata(key)

        if result is None:
            # Cache miss - must regenerate
            return self._regenerate(key, generator, ttl)

        value, delta, expiry = result
        now = time.time()
        ttl_remaining = expiry - now

        if ttl_remaining <= 0:
            # Actually expired - must regenerate
            return self._regenerate(key, generator, ttl)

        # XFetch decision: should we probabilistically refresh?
        # As we get closer to expiry, probability increases
        if self._should_refresh_early(ttl_remaining, delta):
            # Refresh in background, return current value
            self._async_regenerate(key, generator, ttl)

        return value

    def _should_refresh_early(self, ttl_remaining: float,
                               delta: float) -> bool:
        """
        XFetch probability calculation

        P(refresh) = exp(-delta / (ttl_remaining * beta))

        Where:
        - delta = time to regenerate the value
        - ttl_remaining = time until expiry
        - beta = tuning parameter

        This gives:
        - Low probability when TTL is high (far from expiry)
        - High probability when TTL is low (close to expiry)
        - Higher probability when regeneration is slow (high delta)
        """
        if delta <= 0:
            delta = 0.1  # Minimum delta

        # Random factor for probabilistic decision
        random_factor = -math.log(random.random())

        # XFetch formula
        threshold = delta * self.beta * random_factor

        return ttl_remaining <= threshold

    def _regenerate(self, key: str, generator: Callable, ttl: int) -> Any:
        """Regenerate and cache value, recording delta"""
        start = time.time()
        value = generator()
        delta = time.time() - start

        self.cache.set_with_metadata(key, value, ttl, delta)
        return value

    def _async_regenerate(self, key: str, generator: Callable, ttl: int):
        """Regenerate in background"""
        import threading
        thread = threading.Thread(
            target=self._regenerate,
            args=(key, generator, ttl)
        )
        thread.start()
```

## Solution 3: Stale-While-Revalidate

Return stale data immediately while refreshing in background.

```python
import time
import threading
from typing import Any, Callable, Optional

class StaleWhileRevalidateCache:
    """
    Cache that returns stale data while refreshing in background

    Similar to HTTP Cache-Control: stale-while-revalidate
    """

    def __init__(self, cache, db,
                 stale_ttl: int = 60,  # How long stale data is acceptable
                 refresh_timeout: int = 30):  # Max time to wait for refresh
        self.cache = cache
        self.db = db
        self.stale_ttl = stale_ttl
        self.refresh_timeout = refresh_timeout
        self.refreshing = set()  # Keys currently being refreshed
        self.refresh_lock = threading.Lock()

    def get(self, key: str, generator: Callable, ttl: int = 300) -> Any:
        """
        Get value, returning stale if available while refreshing
        """
        result = self.cache.get_with_metadata(key)

        if result is None:
            # No data at all - must wait for fresh
            return self._refresh_and_wait(key, generator, ttl)

        value, created_at = result
        now = time.time()
        age = now - created_at

        if age < ttl:
            # Fresh data
            return value

        if age < ttl + self.stale_ttl:
            # Stale but acceptable - return immediately, refresh async
            self._trigger_async_refresh(key, generator, ttl)
            return value

        # Too stale - must wait for fresh
        return self._refresh_and_wait(key, generator, ttl)

    def _trigger_async_refresh(self, key: str,
                                generator: Callable, ttl: int):
        """Start async refresh if not already in progress"""
        with self.refresh_lock:
            if key in self.refreshing:
                return  # Already being refreshed
            self.refreshing.add(key)

        def refresh():
            try:
                value = generator()
                self.cache.set_with_metadata(key, value, time.time())
            finally:
                with self.refresh_lock:
                    self.refreshing.discard(key)

        thread = threading.Thread(target=refresh)
        thread.start()

    def _refresh_and_wait(self, key: str,
                          generator: Callable, ttl: int) -> Any:
        """Refresh and wait for result"""
        # Check if already being refreshed
        with self.refresh_lock:
            if key in self.refreshing:
                # Wait for refresh to complete
                return self._wait_for_refresh(key, generator, ttl)
            self.refreshing.add(key)

        try:
            value = generator()
            self.cache.set_with_metadata(key, value, time.time())
            return value
        finally:
            with self.refresh_lock:
                self.refreshing.discard(key)

    def _wait_for_refresh(self, key: str,
                          generator: Callable, ttl: int) -> Any:
        """Wait for ongoing refresh to complete"""
        start = time.time()

        while time.time() - start < self.refresh_timeout:
            result = self.cache.get_with_metadata(key)
            if result:
                value, created_at = result
                if time.time() - created_at < ttl:
                    return value
            time.sleep(0.05)

        # Timeout - refresh ourselves
        return self._refresh_and_wait(key, generator, ttl)
```

## Solution 4: Request Coalescing

Combine multiple identical requests into one.

```python
import asyncio
from typing import Any, Callable, Dict
from collections import defaultdict

class AsyncRequestCoalescer:
    """
    Coalesce concurrent requests for the same key

    If 1000 requests for the same key arrive while one is in-flight,
    all 1000 share the single result
    """

    def __init__(self, cache, db):
        self.cache = cache
        self.db = db
        self.pending: Dict[str, asyncio.Future] = {}
        self.pending_lock = asyncio.Lock()

    async def get(self, key: str, generator: Callable) -> Any:
        """
        Get value, coalescing concurrent requests
        """
        # Check cache first
        value = await self.cache.get(key)
        if value is not None:
            return value

        # Check if request is already pending
        async with self.pending_lock:
            if key in self.pending:
                # Wait for existing request
                return await self.pending[key]

            # Create future for this request
            future = asyncio.Future()
            self.pending[key] = future

        try:
            # Make the actual call
            value = await generator()
            await self.cache.set(key, value)

            # Resolve future for all waiters
            future.set_result(value)
            return value

        except Exception as e:
            future.set_exception(e)
            raise

        finally:
            async with self.pending_lock:
                if key in self.pending:
                    del self.pending[key]


class SyncRequestCoalescer:
    """
    Synchronous version using threading
    """

    def __init__(self, cache, db):
        self.cache = cache
        self.db = db
        self.pending = {}
        self.pending_lock = threading.Lock()

    def get(self, key: str, generator: Callable) -> Any:
        # Check cache
        value = self.cache.get(key)
        if value is not None:
            return value

        # Check/create pending request
        with self.pending_lock:
            if key in self.pending:
                event, result_holder = self.pending[key]
            else:
                event = threading.Event()
                result_holder = {'value': None, 'error': None}
                self.pending[key] = (event, result_holder)
                is_leader = True

        if not is_leader:
            # Wait for leader to complete
            event.wait(timeout=30)
            if result_holder['error']:
                raise result_holder['error']
            return result_holder['value']

        # We're the leader - do the work
        try:
            value = generator()
            self.cache.set(key, value)
            result_holder['value'] = value
            return value
        except Exception as e:
            result_holder['error'] = e
            raise
        finally:
            event.set()
            with self.pending_lock:
                if key in self.pending:
                    del self.pending[key]
```

## Solution 5: External Cache Refresh

Decouple cache refresh from request path.

```python
import time
import threading
from typing import Callable, Dict, Set

class BackgroundRefreshCache:
    """
    Cache that refreshes in background, never on request path

    Requests always get cached data (possibly stale)
    Background job keeps cache fresh
    """

    def __init__(self, cache, db):
        self.cache = cache
        self.db = db
        self.registered_keys: Dict[str, dict] = {}
        self.refresh_thread = None
        self.stop_flag = threading.Event()

    def register(self, key: str, generator: Callable,
                 ttl: int = 300, refresh_interval: int = 240):
        """
        Register a key for background refresh
        """
        self.registered_keys[key] = {
            'generator': generator,
            'ttl': ttl,
            'refresh_interval': refresh_interval,
            'last_refresh': 0
        }

        # Initial load
        self._refresh_key(key)

    def get(self, key: str) -> Any:
        """
        Get from cache - never hits DB
        """
        return self.cache.get(key)

    def start_refresh_daemon(self):
        """Start background refresh thread"""
        self.stop_flag.clear()
        self.refresh_thread = threading.Thread(target=self._refresh_loop)
        self.refresh_thread.daemon = True
        self.refresh_thread.start()

    def stop_refresh_daemon(self):
        """Stop background refresh"""
        self.stop_flag.set()
        if self.refresh_thread:
            self.refresh_thread.join()

    def _refresh_loop(self):
        """Background loop that refreshes stale keys"""
        while not self.stop_flag.is_set():
            now = time.time()

            for key, config in self.registered_keys.items():
                time_since_refresh = now - config['last_refresh']

                if time_since_refresh >= config['refresh_interval']:
                    try:
                        self._refresh_key(key)
                    except Exception as e:
                        print(f"Failed to refresh {key}: {e}")
                        # Don't crash the loop

            time.sleep(1)  # Check every second

    def _refresh_key(self, key: str):
        """Refresh a single key"""
        config = self.registered_keys[key]
        value = config['generator']()
        self.cache.set(key, value, ex=config['ttl'])
        config['last_refresh'] = time.time()
```

## Comparison of Solutions

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    SOLUTION COMPARISON                                       │
│                                                                              │
│  Solution              │ Latency │ Complexity │ Consistency │ Best For      │
│  ══════════════════════╪═════════╪════════════╪═════════════╪═══════════════│
│  Locking               │ Medium  │ Medium     │ Fresh       │ General use   │
│  XFetch (prob. early)  │ Low     │ High       │ Fresh       │ High traffic  │
│  Stale-while-revali... │ Low     │ Medium     │ Stale OK    │ User-facing   │
│  Request coalescing    │ Medium  │ Medium     │ Fresh       │ Bursty loads  │
│  Background refresh    │ Low     │ Low        │ Stale OK    │ Predictable   │
│                                                                              │
│  RECOMMENDATION:                                                            │
│  ├── Start with: Locking + Stale-while-revalidate                          │
│  ├── Add: Request coalescing for hot keys                                  │
│  ├── Consider: XFetch for very high traffic                                │
│  └── Use: Background refresh for critical, slow-changing data             │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Interview Tips

### Common Questions

**Q: What causes cache stampede?**
```
A: Three main causes:
   1. TTL expiry of popular item
   2. Cache server restart (all keys lost)
   3. Synchronized cache population (bulk load)

   All result in many concurrent requests for same data
```

**Q: How do you choose between solutions?**
```
A: Consider:
   1. Consistency requirements
      - Must have fresh data? → Locking
      - Stale OK? → Stale-while-revalidate

   2. Latency sensitivity
      - Real-time? → Stale-while-revalidate
      - Can wait? → Locking

   3. Data change frequency
      - Slow-changing? → Background refresh
      - Dynamic? → XFetch or locking
```

### Red Flags

```
❌ "Just increase cache TTL"
   → Delays problem, doesn't solve it

❌ No cache warming on restart
   → Guaranteed stampede on cold start

❌ Fixed TTLs across all keys
   → Synchronized expiry causes stampede

❌ "Let the database handle it"
   → DB isn't designed for burst loads
```

## Summary

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          KEY TAKEAWAYS                                       │
│                                                                              │
│  1. CACHE STAMPEDE IS A THUNDERING HERD VARIANT                            │
│     └── Multiple requests regenerate same expired cache                    │
│     └── Can cascade into database failure                                  │
│                                                                              │
│  2. LOCKING IS THE FOUNDATION                                              │
│     └── Only one request regenerates                                       │
│     └── Others wait or get stale data                                      │
│                                                                              │
│  3. PROBABILISTIC EARLY REFRESH PREVENTS IT                                │
│     └── Refresh before actual expiry                                       │
│     └── Spread load over time                                              │
│                                                                              │
│  4. STALE-WHILE-REVALIDATE FOR LOW LATENCY                                │
│     └── Return stale immediately                                           │
│     └── Refresh in background                                              │
│                                                                              │
│  5. COMBINE STRATEGIES                                                      │
│     └── Locking + stale-while-revalidate is common                        │
│     └── Add coalescing for very hot keys                                   │
│     └── Background refresh for critical data                               │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

**Next:** [Observability](./10_observability.md) - Understanding what's happening in production
