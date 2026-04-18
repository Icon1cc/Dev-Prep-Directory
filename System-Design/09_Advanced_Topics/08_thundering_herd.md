# Thundering Herd Problem

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                       THUNDERING HERD PROBLEM                                 ║
║               When Recovery Causes More Problems Than the Failure             ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

## What is the Thundering Herd?

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    THE THUNDERING HERD                                       │
│                                                                              │
│  SCENARIO:                                                                   │
│  A service goes down. When it comes back up, all waiting requests           │
│  rush in simultaneously, overwhelming it immediately.                        │
│                                                                              │
│  Normal operation:     Service down:        Service back up:                │
│                                                                              │
│  ─────►               ─────► X              ─────────────────►              │
│  ─────►  [Service]    ─────► X  [Service]   ─────────────────►  [Service]  │
│  ─────►               ─────► X  (waiting)   ─────────────────►  (crushed!) │
│  ─────►               ─────► X              ─────────────────►              │
│                                              ▲                               │
│  10 QPS                queued               1000+ simultaneous              │
│                                                                              │
│  RESULT: Service immediately fails again under the flood                    │
│                                                                              │
│  This pattern repeats:                                                       │
│  up → crushed → down → back up → crushed → down → ...                      │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Common Scenarios

### 1. Cache Expiration

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    CACHE EXPIRATION THUNDERING HERD                          │
│                                                                              │
│  SCENARIO: Popular item in cache expires                                    │
│                                                                              │
│  Before expiration:                                                          │
│  1000 requests/sec → Cache (hit!) → return cached value                    │
│                                                                              │
│  TTL expires at T=100:                                                      │
│  Request 1 at T=100.001: Cache miss → Query DB                             │
│  Request 2 at T=100.001: Cache miss → Query DB                             │
│  Request 3 at T=100.002: Cache miss → Query DB                             │
│  ...                                                                         │
│  Request 1000 at T=100.010: Cache miss → Query DB                          │
│                                                                              │
│  All 1000 requests hit the database simultaneously!                        │
│                                                                              │
│         │                                                                    │
│         │    ████████████████████████                                       │
│  DB     │    ████████████████████████  ← Spike at cache expiry            │
│  Load   │    ████████████████████████                                       │
│         │────────────────────────────────────────────────────────► Time    │
│                      ▲                                                       │
│              Cache TTL expires                                               │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2. Service Recovery

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    SERVICE RECOVERY THUNDERING HERD                          │
│                                                                              │
│  SCENARIO: Backend service restarts after crash                             │
│                                                                              │
│  1. Service crashes at T=0                                                  │
│  2. Load balancer marks service unhealthy                                   │
│  3. Requests queue up at load balancer (or retry in clients)               │
│  4. Service starts at T=60                                                  │
│  5. Health check passes at T=65                                             │
│  6. Load balancer sends ALL queued requests                                │
│  7. Service overwhelmed, crashes again                                      │
│                                                                              │
│  Timeline:                                                                   │
│                                                                              │
│  T=0         T=60        T=65         T=66                                 │
│  crash       start       healthy      crash again                          │
│    │           │           │             │                                  │
│    │           │    ───────┼────────────►│                                  │
│    │           │    all    │  flood of   │                                  │
│    │           │    queued │  requests   │                                  │
│    │           │    wait   │             │                                  │
│    ▼           ▼           ▼             ▼                                  │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 3. Lock Release

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    LOCK RELEASE THUNDERING HERD                              │
│                                                                              │
│  SCENARIO: Distributed lock protects expensive operation                    │
│                                                                              │
│  Thread 1 holds lock, doing expensive work                                  │
│  Threads 2-1000 waiting for lock                                            │
│                                                                              │
│  Thread 1 releases lock:                                                     │
│  ├── OS wakes up ALL 999 waiting threads                                   │
│  ├── All try to acquire lock simultaneously                                │
│  ├── Only one wins                                                          │
│  ├── 998 go back to sleep                                                  │
│  └── Massive context switching overhead                                     │
│                                                                              │
│  In distributed systems:                                                     │
│  ├── 1000 processes watching ZooKeeper lock                                │
│  ├── Lock released                                                          │
│  ├── ZooKeeper notifies all 1000                                           │
│  ├── All 1000 try to acquire                                               │
│  └── Network flooded with requests                                          │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Solutions

### Solution 1: Jittered Backoff

```python
import random
import time
from typing import Callable, Any

def exponential_backoff_with_jitter(
    operation: Callable,
    max_retries: int = 5,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    jitter_factor: float = 0.5
) -> Any:
    """
    Retry with exponential backoff and jitter to prevent thundering herd

    Key insight: Add randomness so retries don't synchronize
    """
    for attempt in range(max_retries):
        try:
            return operation()
        except Exception as e:
            if attempt == max_retries - 1:
                raise

            # Calculate base delay: 1, 2, 4, 8, 16...
            delay = min(base_delay * (2 ** attempt), max_delay)

            # Add jitter: randomize delay to spread out retries
            jitter = delay * jitter_factor * random.random()
            actual_delay = delay + jitter

            print(f"Attempt {attempt + 1} failed. Retrying in {actual_delay:.2f}s")
            time.sleep(actual_delay)


def full_jitter_backoff(attempt: int, base_delay: float = 1.0,
                        max_delay: float = 60.0) -> float:
    """
    AWS-style full jitter: random(0, min(cap, base * 2^attempt))
    Provides maximum spread of retry times
    """
    exp_delay = min(max_delay, base_delay * (2 ** attempt))
    return random.uniform(0, exp_delay)


def decorrelated_jitter_backoff(prev_delay: float, base_delay: float = 1.0,
                                max_delay: float = 60.0) -> float:
    """
    Decorrelated jitter: sleep = min(cap, random(base, sleep * 3))
    Good balance of spread and bounded retry time
    """
    return min(max_delay, random.uniform(base_delay, prev_delay * 3))
```

### Solution 2: Cache Stampede Prevention

```python
import threading
import time
import random
from typing import Any, Callable, Optional

class StampedeProtectedCache:
    """
    Cache with multiple strategies to prevent stampede
    """

    def __init__(self, cache, db, default_ttl=300):
        self.cache = cache
        self.db = db
        self.default_ttl = default_ttl
        self.locks = {}  # key -> lock
        self.lock_manager = threading.Lock()

    def get_with_lock(self, key: str) -> Any:
        """
        Strategy 1: Locking - only one thread refreshes cache

        Other threads wait for the refresh to complete
        """
        value = self.cache.get(key)
        if value is not None:
            return value

        # Get or create lock for this key
        with self.lock_manager:
            if key not in self.locks:
                self.locks[key] = threading.Lock()
            lock = self.locks[key]

        with lock:
            # Double-check: another thread might have populated cache
            value = self.cache.get(key)
            if value is not None:
                return value

            # This thread refreshes the cache
            value = self.db.get(key)
            self.cache.set(key, value, ttl=self.default_ttl)
            return value

    def get_with_early_expiration(self, key: str,
                                   early_expiration_pct: float = 0.1) -> Any:
        """
        Strategy 2: Probabilistic early expiration

        Some requests refresh cache before TTL expires
        Spreads cache refreshes over time
        """
        value, ttl_remaining = self.cache.get_with_ttl(key)

        if value is None:
            # Cache miss - must refresh
            value = self.db.get(key)
            self.cache.set(key, value, ttl=self.default_ttl)
            return value

        # Probabilistically refresh if close to expiration
        # As TTL approaches 0, probability increases
        remaining_pct = ttl_remaining / self.default_ttl

        if remaining_pct < early_expiration_pct:
            # Calculate refresh probability
            # At 10% remaining: ~10% chance to refresh
            # At 1% remaining: ~90% chance to refresh
            refresh_probability = 1 - (remaining_pct / early_expiration_pct)

            if random.random() < refresh_probability:
                # This request refreshes (async, return stale)
                self._async_refresh(key)

        return value

    def get_with_stale_while_revalidate(self, key: str) -> Any:
        """
        Strategy 3: Return stale value while refreshing

        Never blocks on cache refresh
        Like HTTP stale-while-revalidate
        """
        value, is_stale = self.cache.get_with_stale_flag(key)

        if value is None:
            # True miss - must wait
            value = self.db.get(key)
            self.cache.set(key, value, ttl=self.default_ttl)
            return value

        if is_stale:
            # Return stale value immediately
            # Refresh in background
            self._async_refresh(key)

        return value

    def _async_refresh(self, key: str):
        """Background refresh"""
        thread = threading.Thread(
            target=self._refresh_cache,
            args=(key,)
        )
        thread.start()

    def _refresh_cache(self, key: str):
        value = self.db.get(key)
        self.cache.set(key, value, ttl=self.default_ttl)
```

### Solution 3: Request Coalescing

```python
import asyncio
from typing import Dict, Any

class RequestCoalescer:
    """
    Coalesce concurrent requests for the same resource

    If 1000 requests come in for the same key while DB is queried,
    only make ONE DB query and share the result
    """

    def __init__(self, db):
        self.db = db
        self.in_flight: Dict[str, asyncio.Future] = {}
        self.locks: Dict[str, asyncio.Lock] = {}

    async def get(self, key: str) -> Any:
        # Get lock for this key
        if key not in self.locks:
            self.locks[key] = asyncio.Lock()

        async with self.locks[key]:
            # Check if request is already in flight
            if key in self.in_flight:
                # Wait for existing request
                return await self.in_flight[key]

            # Create future for this request
            future = asyncio.Future()
            self.in_flight[key] = future

        try:
            # Make the actual DB call
            result = await self.db.get(key)
            future.set_result(result)
            return result
        except Exception as e:
            future.set_exception(e)
            raise
        finally:
            # Cleanup
            async with self.locks[key]:
                if key in self.in_flight:
                    del self.in_flight[key]
```

### Solution 4: Token Bucket Rate Limiting

```python
import time
import threading

class TokenBucket:
    """
    Rate limit requests to prevent thundering herd from overwhelming backend
    """

    def __init__(self, rate: float, capacity: float):
        """
        rate: tokens per second added to bucket
        capacity: maximum tokens in bucket
        """
        self.rate = rate
        self.capacity = capacity
        self.tokens = capacity
        self.last_update = time.time()
        self.lock = threading.Lock()

    def acquire(self, tokens: int = 1, block: bool = True,
                timeout: float = None) -> bool:
        """
        Try to acquire tokens. Returns True if successful.
        """
        start = time.time()

        while True:
            with self.lock:
                self._refill()

                if self.tokens >= tokens:
                    self.tokens -= tokens
                    return True

            if not block:
                return False

            if timeout and (time.time() - start) > timeout:
                return False

            # Wait a bit before retrying
            time.sleep(0.01)

    def _refill(self):
        """Add tokens based on time elapsed"""
        now = time.time()
        elapsed = now - self.last_update
        self.tokens = min(
            self.capacity,
            self.tokens + elapsed * self.rate
        )
        self.last_update = now


class GradualRecovery:
    """
    Gradually increase traffic to a recovering service
    """

    def __init__(self, initial_rate: float = 10,
                 max_rate: float = 1000,
                 ramp_duration: float = 60):
        self.initial_rate = initial_rate
        self.max_rate = max_rate
        self.ramp_duration = ramp_duration
        self.recovery_start = None
        self.bucket = None

    def start_recovery(self):
        """Called when service becomes healthy"""
        self.recovery_start = time.time()
        self.bucket = TokenBucket(
            rate=self.initial_rate,
            capacity=self.initial_rate * 2
        )

    def should_allow_request(self) -> bool:
        """Check if request should be allowed during recovery"""
        if self.recovery_start is None:
            return True  # Not in recovery mode

        elapsed = time.time() - self.recovery_start

        if elapsed > self.ramp_duration:
            # Recovery complete
            self.recovery_start = None
            return True

        # Calculate current rate based on ramp
        progress = elapsed / self.ramp_duration
        current_rate = self.initial_rate + (
            (self.max_rate - self.initial_rate) * progress
        )

        # Update bucket rate
        self.bucket.rate = current_rate
        self.bucket.capacity = current_rate * 2

        return self.bucket.acquire(block=False)
```

### Solution 5: Circuit Breaker with Gradual Recovery

```python
import time
from enum import Enum
from typing import Callable

class CircuitState(Enum):
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Failing, reject requests
    HALF_OPEN = "half_open"  # Testing if recovered

class CircuitBreaker:
    """
    Circuit breaker with gradual recovery to prevent thundering herd
    """

    def __init__(self,
                 failure_threshold: int = 5,
                 recovery_timeout: float = 30,
                 half_open_max_calls: int = 3,
                 gradual_recovery_duration: float = 60):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.half_open_max_calls = half_open_max_calls
        self.gradual_recovery_duration = gradual_recovery_duration

        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.last_failure_time = None
        self.half_open_calls = 0
        self.recovery_start = None
        self.successful_calls_in_recovery = 0

    def call(self, operation: Callable):
        """Execute operation with circuit breaker protection"""

        if self.state == CircuitState.OPEN:
            if self._should_attempt_recovery():
                self.state = CircuitState.HALF_OPEN
                self.half_open_calls = 0
                self.recovery_start = time.time()
            else:
                raise CircuitBreakerOpen("Service unavailable")

        if self.state == CircuitState.HALF_OPEN:
            if not self._should_allow_half_open_call():
                raise CircuitBreakerOpen("Recovery in progress")

        try:
            result = operation()
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise

    def _should_attempt_recovery(self) -> bool:
        """Check if enough time has passed to try recovery"""
        if self.last_failure_time is None:
            return True
        return (time.time() - self.last_failure_time) > self.recovery_timeout

    def _should_allow_half_open_call(self) -> bool:
        """
        During half-open state, gradually increase allowed calls
        This prevents thundering herd on recovery
        """
        if self.recovery_start is None:
            return True

        elapsed = time.time() - self.recovery_start
        progress = min(elapsed / self.gradual_recovery_duration, 1.0)

        # Gradually increase allowed calls
        # At 0%: allow 1 call
        # At 50%: allow 50% of normal
        # At 100%: allow all calls
        max_calls = max(1, int(self.half_open_max_calls * progress))

        return self.half_open_calls < max_calls

    def _on_success(self):
        """Handle successful call"""
        if self.state == CircuitState.HALF_OPEN:
            self.half_open_calls += 1
            self.successful_calls_in_recovery += 1

            # After enough successes, close circuit
            elapsed = time.time() - self.recovery_start
            if elapsed > self.gradual_recovery_duration:
                self.state = CircuitState.CLOSED
                self.failure_count = 0
        else:
            self.failure_count = 0

    def _on_failure(self):
        """Handle failed call"""
        self.failure_count += 1
        self.last_failure_time = time.time()

        if self.state == CircuitState.HALF_OPEN:
            # Recovery failed - back to open
            self.state = CircuitState.OPEN
        elif self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN
```

## Prevention Strategies

```
┌─────────────────────────────────────────────────────────────────────────────┐
│              THUNDERING HERD PREVENTION CHECKLIST                            │
│                                                                              │
│  CACHE LAYER:                                                                │
│  □ Use cache locking (single writer)                                        │
│  □ Implement stale-while-revalidate                                         │
│  □ Add jitter to TTLs                                                       │
│  □ Use probabilistic early expiration                                       │
│  □ Request coalescing for concurrent requests                               │
│                                                                              │
│  SERVICE LAYER:                                                              │
│  □ Exponential backoff with jitter on retries                               │
│  □ Circuit breaker with gradual recovery                                    │
│  □ Rate limiting during recovery                                            │
│  □ Load balancer slow start                                                 │
│                                                                              │
│  INFRASTRUCTURE:                                                             │
│  □ Health check with gradual traffic increase                               │
│  □ Connection pooling with limits                                           │
│  □ Queue with rate limiting                                                 │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Interview Tips

### Common Questions

**Q: How do you prevent cache stampede?**
```
A: Multiple approaches:
   1. Locking: Only one request refreshes, others wait
   2. Early expiration: Probabilistically refresh before TTL
   3. Stale-while-revalidate: Return stale, refresh async
   4. Request coalescing: Share single DB result

   Best practice: Combine multiple strategies
```

**Q: Service A is restarting and causing thundering herd. Solutions?**
```
A: Load balancer level:
   - Slow start: gradually increase traffic to new instance
   - Health checks with grace period

   Application level:
   - Exponential backoff with jitter
   - Circuit breaker with gradual recovery
   - Rate limiting during startup
```

### Red Flags

```
❌ "Just add more servers"
   → Doesn't help if all requests hit at once

❌ Fixed retry delays
   → Synchronized retries cause thundering herd

❌ Cache with fixed TTL, no protection
   → Guaranteed stampede at expiration

❌ Instant health check pass → full traffic
   → Recipe for immediate re-failure
```

## Summary

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          KEY TAKEAWAYS                                       │
│                                                                              │
│  1. THUNDERING HERD CAUSES                                                  │
│     └── Cache expiration                                                    │
│     └── Service recovery                                                    │
│     └── Lock release                                                        │
│     └── Any "many waiting for one" pattern                                 │
│                                                                              │
│  2. CORE SOLUTIONS                                                          │
│     └── Add randomness (jitter) to break synchronization                   │
│     └── Coalesce concurrent requests                                        │
│     └── Gradual recovery, not instant                                       │
│                                                                              │
│  3. CACHE-SPECIFIC                                                          │
│     └── Locking (single writer)                                            │
│     └── Stale-while-revalidate                                             │
│     └── Probabilistic early expiration                                     │
│                                                                              │
│  4. SERVICE-SPECIFIC                                                        │
│     └── Circuit breaker with gradual recovery                              │
│     └── Load balancer slow start                                           │
│     └── Rate limiting during recovery                                      │
│                                                                              │
│  5. THE PATTERN                                                             │
│     └── Detect the "many waiting for one" scenario                         │
│     └── Add randomness to break synchronization                            │
│     └── Gradual increase, not step function                                │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

**Next:** [Cache Stampede](./09_cache_stampede.md) - Deep dive into cache-specific thundering herd
