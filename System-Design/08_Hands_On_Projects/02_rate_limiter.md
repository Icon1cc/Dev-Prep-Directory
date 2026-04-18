# Project 2: Rate Limiter

Build rate limiting algorithms from scratch.

## Problem Description

```
┌────────────────────────────────────────────────────────────────┐
│                      RATE LIMITER                               │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Design a rate limiter that:                                   │
│  • Limits requests to N per time window                        │
│  • Returns True if request is allowed, False otherwise         │
│                                                                 │
│  Example: Allow 5 requests per minute                          │
│  - Requests 1-5: Allowed                                       │
│  - Request 6: Denied (over limit)                              │
│  - After 1 minute: Counter resets                              │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

## Algorithms Covered

1. **Token Bucket** - Smooth rate limiting with burst handling
2. **Sliding Window Log** - Precise but memory-intensive
3. **Sliding Window Counter** - Good balance of precision and memory

---

## Algorithm 1: Token Bucket

```
┌────────────────────────────────────────────────────────────────┐
│                     TOKEN BUCKET                                │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Concept:                                                      │
│  • Bucket holds tokens (max = bucket_size)                     │
│  • Tokens added at fixed rate (refill_rate per second)         │
│  • Each request consumes one token                             │
│  • No tokens = request denied                                  │
│                                                                 │
│  ┌─────────────────────────────────────────┐                   │
│  │           Token Bucket                   │                   │
│  │  ┌───────────────────────────────────┐  │                   │
│  │  │  ○ ○ ○ ○ ○ ○ ○ ○ (8 tokens)      │  │                   │
│  │  └───────────────────────────────────┘  │                   │
│  │            ▲                    │        │                   │
│  │            │                    ▼        │                   │
│  │      Tokens added          Token taken   │                   │
│  │      every interval        per request   │                   │
│  └─────────────────────────────────────────┘                   │
│                                                                 │
│  Good for: Allowing bursts while maintaining average rate      │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

### Python Implementation

```python
import time

class TokenBucket:
    def __init__(self, bucket_size: int, refill_rate: float):
        """
        Args:
            bucket_size: Maximum tokens in bucket
            refill_rate: Tokens added per second
        """
        self.bucket_size = bucket_size
        self.refill_rate = refill_rate
        self.tokens = bucket_size
        self.last_refill = time.time()

    def allow_request(self) -> bool:
        """Check if request is allowed and consume a token."""
        self._refill()

        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False

    def _refill(self):
        """Add tokens based on time elapsed."""
        now = time.time()
        elapsed = now - self.last_refill

        # Add tokens proportional to elapsed time
        tokens_to_add = elapsed * self.refill_rate
        self.tokens = min(self.bucket_size, self.tokens + tokens_to_add)
        self.last_refill = now


# Test
if __name__ == "__main__":
    # 5 tokens max, 1 token per second refill
    limiter = TokenBucket(bucket_size=5, refill_rate=1)

    # Should allow first 5 requests
    for i in range(5):
        print(f"Request {i+1}: {limiter.allow_request()}")  # True

    # 6th request should be denied
    print(f"Request 6: {limiter.allow_request()}")  # False

    # Wait and try again
    time.sleep(2)
    print(f"After 2 seconds: {limiter.allow_request()}")  # True
```

---

## Algorithm 2: Sliding Window Log

```
┌────────────────────────────────────────────────────────────────┐
│                   SLIDING WINDOW LOG                            │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Concept:                                                      │
│  • Store timestamp of each request                             │
│  • Count requests in current window                            │
│  • Remove expired timestamps                                    │
│                                                                 │
│  Timeline:                                                     │
│  ─────────────────────────────────────────────────────────►    │
│    │     │  │    │   │                    │                    │
│   t1    t2 t3   t4  t5                   now                   │
│    └─────────────────────────────────────┘                     │
│         Window (60 seconds)                                    │
│         Count = 5 requests                                     │
│                                                                 │
│  Good for: Precise counting                                    │
│  Bad for: Memory usage at high traffic                         │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

### Python Implementation

```python
import time
from collections import deque

class SlidingWindowLog:
    def __init__(self, max_requests: int, window_seconds: int):
        """
        Args:
            max_requests: Max requests allowed in window
            window_seconds: Size of time window in seconds
        """
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.timestamps = deque()

    def allow_request(self) -> bool:
        """Check if request is allowed."""
        now = time.time()
        window_start = now - self.window_seconds

        # Remove expired timestamps
        while self.timestamps and self.timestamps[0] < window_start:
            self.timestamps.popleft()

        # Check if under limit
        if len(self.timestamps) < self.max_requests:
            self.timestamps.append(now)
            return True
        return False


# Test
if __name__ == "__main__":
    # 5 requests per 60 seconds
    limiter = SlidingWindowLog(max_requests=5, window_seconds=60)

    # Should allow first 5
    for i in range(5):
        print(f"Request {i+1}: {limiter.allow_request()}")  # True

    # 6th should be denied
    print(f"Request 6: {limiter.allow_request()}")  # False
```

---

## Algorithm 3: Sliding Window Counter

```
┌────────────────────────────────────────────────────────────────┐
│                 SLIDING WINDOW COUNTER                          │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Concept:                                                      │
│  • Divide time into fixed windows                              │
│  • Count requests per window                                   │
│  • Interpolate between windows for smooth limiting             │
│                                                                 │
│  Windows:                                                      │
│  ┌─────────────────┬─────────────────┐                        │
│  │  Previous (5)   │  Current (3)    │                        │
│  └─────────────────┴─────────────────┘                        │
│                         │                                      │
│                        now                                     │
│                                                                 │
│  Estimated count = prev * (1 - position) + curr * position    │
│  If position is 0.3: 5 * 0.7 + 3 * 0.3 = 4.4                  │
│                                                                 │
│  Good for: Memory efficient, reasonably accurate               │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

### Python Implementation

```python
import time

class SlidingWindowCounter:
    def __init__(self, max_requests: int, window_seconds: int):
        """
        Args:
            max_requests: Max requests allowed in window
            window_seconds: Size of time window in seconds
        """
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.current_window_start = 0
        self.current_count = 0
        self.previous_count = 0

    def allow_request(self) -> bool:
        """Check if request is allowed."""
        now = time.time()
        current_window = int(now // self.window_seconds)

        # Check if we've moved to a new window
        if current_window != self.current_window_start:
            if current_window == self.current_window_start + 1:
                # Moved to next window
                self.previous_count = self.current_count
            else:
                # Moved multiple windows (long gap)
                self.previous_count = 0

            self.current_count = 0
            self.current_window_start = current_window

        # Calculate position within current window (0 to 1)
        window_position = (now % self.window_seconds) / self.window_seconds

        # Estimate total requests using weighted average
        estimated_count = (
            self.previous_count * (1 - window_position) +
            self.current_count
        )

        if estimated_count < self.max_requests:
            self.current_count += 1
            return True
        return False


# Test
if __name__ == "__main__":
    # 5 requests per 10 seconds
    limiter = SlidingWindowCounter(max_requests=5, window_seconds=10)

    for i in range(7):
        result = limiter.allow_request()
        print(f"Request {i+1}: {result}")
```

---

## Comparison

| Algorithm | Memory | Precision | Burst Handling |
|-----------|--------|-----------|----------------|
| Token Bucket | O(1) | Approximate | Allows bursts |
| Sliding Log | O(n) | Exact | No bursts |
| Sliding Counter | O(1) | Approximate | Smoothed |

---

## Distributed Rate Limiting

For production systems, you need distributed rate limiting:

```python
import redis
import time

class DistributedRateLimiter:
    """Rate limiter using Redis for distributed systems."""

    def __init__(self, redis_client, key_prefix: str,
                 max_requests: int, window_seconds: int):
        self.redis = redis_client
        self.key_prefix = key_prefix
        self.max_requests = max_requests
        self.window_seconds = window_seconds

    def allow_request(self, user_id: str) -> bool:
        """Check if request is allowed for given user."""
        key = f"{self.key_prefix}:{user_id}"
        now = time.time()
        window_start = now - self.window_seconds

        pipe = self.redis.pipeline()

        # Remove old entries
        pipe.zremrangebyscore(key, 0, window_start)

        # Count current entries
        pipe.zcard(key)

        # Add new entry
        pipe.zadd(key, {str(now): now})

        # Set expiration
        pipe.expire(key, self.window_seconds)

        results = pipe.execute()
        current_count = results[1]

        return current_count < self.max_requests


# Usage (requires Redis)
# redis_client = redis.Redis(host='localhost', port=6379)
# limiter = DistributedRateLimiter(redis_client, "ratelimit", 100, 60)
# allowed = limiter.allow_request("user_123")
```

---

## Extensions

1. **Per-User Limits**: Different limits for different user tiers
2. **Hierarchical Limits**: Global + per-user + per-endpoint limits
3. **Graceful Degradation**: Return retry-after header when limited
4. **Metrics**: Track limit hits for monitoring

---

*Next: [URL Shortener](03_url_shortener.md) →*
