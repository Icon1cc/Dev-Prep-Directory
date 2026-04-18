# Rate Limiters

## What is Rate Limiting?

**Rate Limiting** controls the number of requests a client can make to an API within a time window. It protects services from abuse, ensures fair usage, and prevents system overload.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Why Rate Limiting Matters                            │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Without Rate Limiting:                                               │
│   ──────────────────────                                                │
│                                                                         │
│   Malicious User ──► 100,000 requests/sec ──► Server Crash!           │
│   Buggy Client  ──► Infinite loop          ──► Resource exhaustion    │
│   Scraper       ──► Mass data extraction   ──► Cost explosion         │
│                                                                         │
│   With Rate Limiting:                                                  │
│   ─────────────────                                                     │
│                                                                         │
│   User ──► Rate Limiter ──► if under limit ──► Server                 │
│                │                                                        │
│                └──► if over limit ──► 429 Too Many Requests            │
│                                                                         │
│   Benefits:                                                            │
│   ─────────                                                             │
│   • Prevent DDoS attacks                                               │
│   • Ensure fair usage among clients                                    │
│   • Reduce cost (API calls cost money)                                │
│   • Maintain service quality                                           │
│   • Revenue model (tiered API access)                                  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Rate Limiting Algorithms

### 1. Token Bucket

Most common algorithm. Tokens are added at a constant rate; requests consume tokens.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Token Bucket Algorithm                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Configuration:                                                       │
│   • Bucket capacity: 10 tokens (max burst)                            │
│   • Refill rate: 1 token/second                                       │
│                                                                         │
│   Bucket: [●][●][●][●][●][○][○][○][○][○]  (5 tokens available)       │
│                                                                         │
│   Time=0:  Request arrives                                             │
│            Bucket has 5 tokens                                         │
│            Request allowed, consume 1 token                            │
│            Bucket: [●][●][●][●][○][○][○][○][○][○]                     │
│                                                                         │
│   Time=1:  3 requests arrive simultaneously                           │
│            Bucket refilled +1, now has 5 tokens                        │
│            All 3 allowed, consume 3 tokens                             │
│            Bucket: [●][●][○][○][○][○][○][○][○][○]                     │
│                                                                         │
│   Time=2:  5 requests arrive                                          │
│            Bucket refilled +1, now has 3 tokens                        │
│            3 allowed, 2 rejected (429)                                 │
│                                                                         │
│   Key Properties:                                                      │
│   ───────────────                                                       │
│   • Allows bursts (up to bucket capacity)                             │
│   • Smooths traffic over time                                          │
│   • Simple to implement                                                │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Python Implementation:**

```python
import time
from threading import Lock

class TokenBucket:
    def __init__(self, capacity: int, refill_rate: float):
        """
        Args:
            capacity: Maximum tokens (burst size)
            refill_rate: Tokens added per second
        """
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = capacity
        self.last_refill = time.time()
        self.lock = Lock()

    def _refill(self):
        """Add tokens based on elapsed time"""
        now = time.time()
        elapsed = now - self.last_refill
        tokens_to_add = elapsed * self.refill_rate
        self.tokens = min(self.capacity, self.tokens + tokens_to_add)
        self.last_refill = now

    def allow_request(self, tokens: int = 1) -> bool:
        """
        Check if request is allowed.
        Returns True if allowed, False if rate limited.
        """
        with self.lock:
            self._refill()
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            return False

# Usage
bucket = TokenBucket(capacity=10, refill_rate=1)  # 1 token/sec

for i in range(15):
    if bucket.allow_request():
        print(f"Request {i+1}: Allowed")
    else:
        print(f"Request {i+1}: Rate limited!")
```

### 2. Leaky Bucket

Processes requests at a constant rate, like water leaking from a bucket.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Leaky Bucket Algorithm                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Configuration:                                                       │
│   • Bucket capacity: 10 (queue size)                                  │
│   • Leak rate: 1 request/second (processing rate)                     │
│                                                                         │
│   Visualization:                                                       │
│                                                                         │
│        Requests arrive (variable rate)                                 │
│              │ │ │ │                                                   │
│              ▼ ▼ ▼ ▼                                                   │
│         ┌───────────────┐                                             │
│         │ Queue (bucket)│ ← Overflow if full = rejected              │
│         │  [req][req]   │                                             │
│         │  [req][req]   │                                             │
│         └───────┬───────┘                                             │
│                 │                                                       │
│                 ▼ Constant rate out (leak)                            │
│              1 req/sec                                                 │
│                 │                                                       │
│                 ▼                                                       │
│              Server                                                    │
│                                                                         │
│   Difference from Token Bucket:                                        │
│   ─────────────────────────────                                         │
│   Token Bucket: Allows bursts, then rate limits                       │
│   Leaky Bucket: Always processes at constant rate                     │
│                                                                         │
│   Token = permits burst traffic                                       │
│   Leaky = smooths traffic into steady flow                           │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 3. Fixed Window Counter

Counts requests in fixed time windows.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Fixed Window Counter                                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Configuration: 100 requests per minute                               │
│                                                                         │
│   Time: ──────────────────────────────────────────────────►           │
│                                                                         │
│        │←── Window 1 ──►│←── Window 2 ──►│←── Window 3 ──►│          │
│        │    00:00-01:00  │    01:00-02:00  │    02:00-03:00  │          │
│        │                 │                 │                 │          │
│        │   Count: 87     │   Count: 23     │   Count: 0      │          │
│        │   (allowed)     │   (allowed)     │   (allowed)     │          │
│                                                                         │
│   Problem - Burst at window boundary:                                  │
│   ─────────────────────────────────────                                 │
│                                                                         │
│   Time: ──────────────────────────────────────────────────►           │
│        │        │←── Window 1 ──►│←── Window 2 ──►│                  │
│        │        │    00:00-01:00  │    01:00-02:00  │                  │
│        │        │                 │                 │                  │
│        │        │         [100]   [100]            │                  │
│        │        │           ▲       ▲              │                  │
│        │        │           └───┬───┘              │                  │
│        │        │               │                  │                  │
│        │        │     200 requests in ~1 second!  │                  │
│        │        │        (00:59 to 01:01)         │                  │
│                                                                         │
│   Pros: Simple, memory efficient                                      │
│   Cons: Can allow 2x limit at window boundaries                      │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 4. Sliding Window Log

Tracks timestamp of each request. More accurate but memory intensive.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Sliding Window Log                                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Configuration: 5 requests per 60 seconds                             │
│                                                                         │
│   Current time: 12:01:30                                              │
│   Window: 12:00:30 - 12:01:30                                         │
│                                                                         │
│   Request log:                                                         │
│   [12:00:15] ← Outside window, remove                                 │
│   [12:00:35] ← In window, count                                       │
│   [12:00:50] ← In window, count                                       │
│   [12:01:05] ← In window, count                                       │
│   [12:01:20] ← In window, count                                       │
│                                                                         │
│   Count in window: 4                                                   │
│   New request at 12:01:30: Allowed (4 < 5)                           │
│   Log becomes: [12:00:35, 12:00:50, 12:01:05, 12:01:20, 12:01:30]     │
│                                                                         │
│   Pros: Accurate, no boundary burst problem                           │
│   Cons: Memory intensive (stores all timestamps)                      │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 5. Sliding Window Counter

Hybrid: combines fixed window efficiency with sliding window accuracy.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Sliding Window Counter                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Configuration: 100 requests per minute                               │
│                                                                         │
│   Current time: 01:15 (15 seconds into window 2)                      │
│                                                                         │
│   │←──── Window 1 ────►│←──── Window 2 ────►│                        │
│   │    00:00 - 01:00    │    01:00 - 02:00    │                        │
│   │    Count: 80        │    Count: 30        │                        │
│   │                     │◄───┤                │                        │
│   │                     │ 15s │                │                        │
│                                                                         │
│   Calculation:                                                         │
│   ────────────                                                          │
│   Sliding window: 00:15 - 01:15                                       │
│                                                                         │
│   Window 1 contribution: 80 × (45/60) = 60                            │
│                          (45 seconds of window 1 in sliding window)   │
│                                                                         │
│   Window 2 contribution: 30 × (15/60) = 7.5                           │
│                          (15 seconds of window 2 in sliding window)   │
│                                                                         │
│   Total: 60 + 7.5 = 67.5 ≈ 68 requests                               │
│                                                                         │
│   New request: Allowed (68 < 100)                                     │
│                                                                         │
│   Pros: Memory efficient (only 2 counters), accurate                  │
│   Cons: Approximation (not 100% accurate)                             │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Distributed Rate Limiting

### Challenge

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Distributed Rate Limiting Challenge                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   User makes 100 requests/sec                                         │
│   Limit: 100/sec                                                       │
│                                                                         │
│   With 10 servers (each has local rate limiter):                      │
│                                                                         │
│   User ──┬──► Server 1: 10 req/sec ✓                                 │
│          ├──► Server 2: 10 req/sec ✓                                 │
│          ├──► Server 3: 10 req/sec ✓                                 │
│          │    ...                                                      │
│          └──► Server 10: 10 req/sec ✓                                │
│                                                                         │
│   Total: 100 req/sec passes! (should be limited)                      │
│                                                                         │
│   Solution: Centralized rate limiter                                  │
│                                                                         │
│   User ──► Rate Limiter (Redis) ──► Servers                          │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Redis Implementation

```python
import redis
import time

class DistributedRateLimiter:
    def __init__(self, redis_client, key_prefix="ratelimit"):
        self.redis = redis_client
        self.key_prefix = key_prefix

    def is_allowed_sliding_window(
        self,
        user_id: str,
        limit: int,
        window_seconds: int
    ) -> bool:
        """
        Sliding window counter using Redis sorted sets.
        """
        key = f"{self.key_prefix}:{user_id}"
        now = time.time()
        window_start = now - window_seconds

        pipe = self.redis.pipeline()

        # Remove old entries
        pipe.zremrangebyscore(key, 0, window_start)

        # Count current entries
        pipe.zcard(key)

        # Add current request (will commit if allowed)
        pipe.zadd(key, {str(now): now})

        # Set TTL
        pipe.expire(key, window_seconds)

        results = pipe.execute()
        current_count = results[1]

        if current_count < limit:
            return True
        else:
            # Remove the request we optimistically added
            self.redis.zrem(key, str(now))
            return False

    def is_allowed_token_bucket(
        self,
        user_id: str,
        capacity: int,
        refill_rate: float
    ) -> bool:
        """
        Token bucket using Redis Lua script for atomicity.
        """
        key = f"{self.key_prefix}:bucket:{user_id}"

        lua_script = """
        local key = KEYS[1]
        local capacity = tonumber(ARGV[1])
        local refill_rate = tonumber(ARGV[2])
        local now = tonumber(ARGV[3])

        local bucket = redis.call('HMGET', key, 'tokens', 'last_refill')
        local tokens = tonumber(bucket[1]) or capacity
        local last_refill = tonumber(bucket[2]) or now

        -- Calculate tokens to add
        local elapsed = now - last_refill
        tokens = math.min(capacity, tokens + (elapsed * refill_rate))

        -- Check if request is allowed
        if tokens >= 1 then
            tokens = tokens - 1
            redis.call('HMSET', key, 'tokens', tokens, 'last_refill', now)
            redis.call('EXPIRE', key, 3600)
            return 1
        else
            redis.call('HMSET', key, 'tokens', tokens, 'last_refill', now)
            return 0
        end
        """

        result = self.redis.eval(
            lua_script,
            1,
            key,
            capacity,
            refill_rate,
            time.time()
        )
        return result == 1

# Usage
redis_client = redis.Redis(host='localhost', port=6379)
limiter = DistributedRateLimiter(redis_client)

user_id = "user_123"

# Check rate limit
if limiter.is_allowed_sliding_window(user_id, limit=100, window_seconds=60):
    print("Request allowed")
else:
    print("Rate limited!")
```

---

## Rate Limit Response

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Rate Limit Response Headers                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   HTTP/1.1 429 Too Many Requests                                       │
│   Content-Type: application/json                                       │
│   X-RateLimit-Limit: 100                                              │
│   X-RateLimit-Remaining: 0                                            │
│   X-RateLimit-Reset: 1609459200                                       │
│   Retry-After: 30                                                      │
│                                                                         │
│   {                                                                    │
│     "error": "rate_limit_exceeded",                                   │
│     "message": "Too many requests. Please retry after 30 seconds.",   │
│     "limit": 100,                                                     │
│     "remaining": 0,                                                   │
│     "reset_at": "2024-01-01T00:00:00Z"                               │
│   }                                                                    │
│                                                                         │
│   Headers Explanation:                                                 │
│   ────────────────────                                                  │
│   X-RateLimit-Limit:     Maximum requests allowed in window           │
│   X-RateLimit-Remaining: Requests remaining in current window         │
│   X-RateLimit-Reset:     Unix timestamp when window resets            │
│   Retry-After:           Seconds to wait before retrying             │
│                                                                         │
│   Include these in SUCCESSFUL responses too:                          │
│                                                                         │
│   HTTP/1.1 200 OK                                                      │
│   X-RateLimit-Limit: 100                                              │
│   X-RateLimit-Remaining: 45                                           │
│   X-RateLimit-Reset: 1609459200                                       │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Rate Limiting Strategies

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Rate Limiting Strategies                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   1. BY USER / API KEY                                                 │
│      ──────────────────                                                 │
│      user_123: 100 requests/minute                                    │
│      Fair distribution among users                                     │
│                                                                         │
│   2. BY IP ADDRESS                                                     │
│      ───────────────                                                    │
│      192.168.1.1: 1000 requests/minute                               │
│      Caveat: Users behind NAT share IP                                │
│                                                                         │
│   3. BY ENDPOINT                                                       │
│      ────────────                                                       │
│      POST /login: 5 requests/minute (prevent brute force)             │
│      GET /search: 60 requests/minute                                  │
│      POST /payment: 10 requests/minute                                │
│                                                                         │
│   4. BY TIER / PLAN                                                    │
│      ─────────────────                                                  │
│      Free tier:       100/day                                         │
│      Basic tier:      10,000/day                                      │
│      Pro tier:        100,000/day                                     │
│      Enterprise:      Unlimited                                       │
│                                                                         │
│   5. GLOBAL (System Protection)                                        │
│      ──────────────────────────                                         │
│      Total API: 1,000,000 requests/minute                             │
│      Protects overall system capacity                                 │
│                                                                         │
│   6. CONCURRENT REQUESTS                                               │
│      ──────────────────────                                             │
│      Max 10 simultaneous connections per user                        │
│      Prevents resource hogging                                        │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## When to Use / When NOT to Use

### When to Use Rate Limiting

✅ Public APIs (prevent abuse)
✅ Authentication endpoints (prevent brute force)
✅ Expensive operations (protect resources)
✅ Tiered pricing models
✅ Third-party API calls (stay under limits)

### When NOT to Use

❌ Internal services with trusted clients
❌ Health check endpoints
❌ Already behind API gateway with rate limiting
❌ When availability is more important than fairness

---

## Interview Traps

| Trap | What They're Testing | Good Answer |
|------|---------------------|-------------|
| "Token vs Leaky Bucket?" | Algorithm understanding | Token allows bursts; Leaky smooths to constant rate |
| "How to rate limit across servers?" | Distributed systems | Centralized store (Redis) with atomic operations |
| "Fixed window boundary problem?" | Edge case awareness | Use sliding window or accept 2x burst at boundaries |
| "What about legitimate traffic spikes?" | Business thinking | Graceful degradation, different limits per endpoint, alerting |

---

This completes the Core Components section. Each component is a tool in your system design toolbox—knowing when to use each one (and when not to) is key to acing interviews.
