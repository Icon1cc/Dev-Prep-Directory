# Hot Partition Problem

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                        HOT PARTITION PROBLEM                                  ║
║             When One Partition Gets All the Load                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

## What is a Hot Partition?

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      THE HOT PARTITION PROBLEM                               │
│                                                                              │
│  SCENARIO: You sharded your database beautifully across 10 nodes            │
│                                                                              │
│  Expected:        Actual:                                                    │
│                                                                              │
│  Node 1: ████     Node 1: ████████████████████████  ← HOT!                 │
│  Node 2: ████     Node 2: █                                                 │
│  Node 3: ████     Node 3: █                                                 │
│  Node 4: ████     Node 4: █                                                 │
│  Node 5: ████     Node 5: █                                                 │
│  Node 6: ████     Node 6: █                                                 │
│  Node 7: ████     Node 7: █                                                 │
│  Node 8: ████     Node 8: █                                                 │
│  Node 9: ████     Node 9: █                                                 │
│  Node 10:████     Node 10: █                                                │
│                                                                              │
│  RESULT:                                                                     │
│  ├── Node 1 is overloaded, responding slowly or failing                    │
│  ├── Nodes 2-10 are nearly idle                                            │
│  ├── System performance = hot partition's performance                      │
│  └── You're paying for 10 nodes but getting capacity of 1                  │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Common Causes

### 1. Skewed Partition Keys

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                   SKEWED PARTITION KEYS                                      │
│                                                                              │
│  EXAMPLE: E-commerce partitioned by seller_id                               │
│                                                                              │
│  Partition key: seller_id                                                   │
│                                                                              │
│  Seller Distribution:                                                        │
│  ├── Amazon (seller_id=1): 10 million products                             │
│  ├── Small seller A: 50 products                                            │
│  ├── Small seller B: 100 products                                           │
│  └── ... millions of small sellers                                          │
│                                                                              │
│  Result: Partition with seller_id=1 has millions of records                │
│          Other partitions have dozens                                        │
│                                                                              │
│  EXAMPLE: Social media partitioned by user_id                               │
│                                                                              │
│  ├── Kim Kardashian: 300 million followers                                 │
│  ├── Average user: 500 followers                                            │
│                                                                              │
│  Result: Celebrity partitions are HOT                                       │
│                                                                              │
│  EXAMPLE: Time-series partitioned by date                                   │
│                                                                              │
│  Partition key: date                                                        │
│  ├── Today's partition: ALL writes go here                                 │
│  ├── Yesterday's partition: Some reads                                      │
│  ├── Last week's partition: Rare access                                    │
│                                                                              │
│  Result: Current date partition always hot                                  │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2. Temporal Hotspots

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    TEMPORAL HOTSPOTS                                         │
│                                                                              │
│  SCENARIO: Flash sale starts at 12:00 PM                                   │
│                                                                              │
│  11:59: ─────────────────────────                                          │
│  12:00: ████████████████████████████████████████████████  ← SPIKE!         │
│  12:01: ██████████████████████████████████                                 │
│  12:05: ████████████████                                                   │
│  12:10: ─────────────                                                       │
│                                                                              │
│  If items are partitioned by item_id:                                       │
│  └── Sale item partition gets 1000x normal traffic                         │
│                                                                              │
│  OTHER EXAMPLES:                                                            │
│  ├── Viral tweet: partition for that tweet_id overwhelmed                  │
│  ├── Breaking news: article_id partition overwhelmed                       │
│  ├── Product launch: new product partition overwhelmed                     │
│  └── Celebrity death: related content partitions overwhelmed               │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Detection

### Monitoring for Hot Partitions

```python
class HotPartitionDetector:
    """
    Detect hot partitions through monitoring
    """

    def __init__(self, threshold_ratio=5.0):
        # Partition is "hot" if > 5x average load
        self.threshold_ratio = threshold_ratio
        self.partition_metrics = {}  # partition_id -> metrics

    def record_request(self, partition_id: str, latency_ms: float):
        """Record a request to a partition"""
        if partition_id not in self.partition_metrics:
            self.partition_metrics[partition_id] = {
                'request_count': 0,
                'total_latency': 0,
                'timestamps': []
            }

        metrics = self.partition_metrics[partition_id]
        metrics['request_count'] += 1
        metrics['total_latency'] += latency_ms
        metrics['timestamps'].append(time.time())

    def get_hot_partitions(self, window_seconds=60):
        """Get list of hot partitions"""
        now = time.time()
        cutoff = now - window_seconds

        # Calculate requests per partition in window
        partition_loads = {}
        for partition_id, metrics in self.partition_metrics.items():
            recent = [t for t in metrics['timestamps'] if t > cutoff]
            partition_loads[partition_id] = len(recent)

        if not partition_loads:
            return []

        average_load = sum(partition_loads.values()) / len(partition_loads)
        if average_load == 0:
            return []

        # Find partitions significantly above average
        hot = []
        for partition_id, load in partition_loads.items():
            ratio = load / average_load
            if ratio > self.threshold_ratio:
                hot.append({
                    'partition_id': partition_id,
                    'load': load,
                    'ratio': ratio,
                    'avg_latency': self._get_avg_latency(partition_id)
                })

        return sorted(hot, key=lambda x: x['ratio'], reverse=True)

    def _get_avg_latency(self, partition_id):
        metrics = self.partition_metrics.get(partition_id)
        if not metrics or metrics['request_count'] == 0:
            return 0
        return metrics['total_latency'] / metrics['request_count']
```

### Key Metrics to Monitor

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                  HOT PARTITION METRICS                                       │
│                                                                              │
│  PER-PARTITION:                                                             │
│  ├── Request rate (QPS)                                                    │
│  ├── P50, P95, P99 latency                                                 │
│  ├── Error rate                                                             │
│  ├── CPU/memory utilization                                                │
│  └── Queue depth (pending requests)                                        │
│                                                                              │
│  CROSS-PARTITION:                                                           │
│  ├── Standard deviation of request rates                                   │
│  ├── Coefficient of variation (σ/μ)                                        │
│  ├── Max/average ratio                                                      │
│  └── Gini coefficient of load distribution                                 │
│                                                                              │
│  ALERTS:                                                                    │
│  ├── Partition load > 5x average                                           │
│  ├── Partition latency > 2x average                                        │
│  ├── Single partition > 20% of total load                                  │
│  └── Rapid increase in partition load (10x in 1 minute)                   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Solutions

### Solution 1: Add Randomness to Keys (Write Sharding)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    WRITE SHARDING                                            │
│                                                                              │
│  PROBLEM: All writes for item_id=123 go to same partition                  │
│                                                                              │
│  SOLUTION: Add random suffix to spread writes                               │
│                                                                              │
│  Original key: item_id=123                                                  │
│  Sharded keys: item_id=123#0, item_id=123#1, ... item_id=123#9             │
│                                                                              │
│  Before:                       After:                                        │
│                                                                              │
│  item_id=123 ──► Partition A   item_id=123#0 ──► Partition A              │
│  item_id=123 ──► Partition A   item_id=123#1 ──► Partition B              │
│  item_id=123 ──► Partition A   item_id=123#2 ──► Partition C              │
│  item_id=123 ──► Partition A   item_id=123#3 ──► Partition D              │
│                                                                              │
│  TRADE-OFF: Reads must query all suffixes and aggregate                    │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

```python
import random
from typing import List, Any

class ShardedCounter:
    """
    Counter that shards writes across multiple keys to avoid hot partition
    Used by: DynamoDB (atomic counters), Cassandra (counter columns)
    """

    def __init__(self, key: str, num_shards: int = 10):
        self.key = key
        self.num_shards = num_shards
        self.db = {}  # Simulated database

    def _shard_key(self, shard_id: int) -> str:
        return f"{self.key}#shard{shard_id}"

    def increment(self, value: int = 1) -> None:
        """
        Increment counter - write goes to random shard
        """
        # Pick random shard - spreads writes
        shard_id = random.randint(0, self.num_shards - 1)
        shard_key = self._shard_key(shard_id)

        # Atomic increment on that shard
        current = self.db.get(shard_key, 0)
        self.db[shard_key] = current + value

    def get_count(self) -> int:
        """
        Get total count - must read ALL shards
        """
        total = 0
        for shard_id in range(self.num_shards):
            shard_key = self._shard_key(shard_id)
            total += self.db.get(shard_key, 0)
        return total


class ShardedTimeSeries:
    """
    Time series that shards by adding random suffix to timestamp
    """

    def __init__(self, metric_name: str, num_shards: int = 100):
        self.metric_name = metric_name
        self.num_shards = num_shards

    def write_point(self, timestamp: int, value: float) -> str:
        """
        Write data point with sharded key
        """
        shard_id = random.randint(0, self.num_shards - 1)
        partition_key = f"{self.metric_name}#{timestamp}#{shard_id}"

        # Write to database
        return partition_key

    def read_range(self, start_ts: int, end_ts: int) -> List[dict]:
        """
        Read range - must query all shards for each timestamp
        """
        results = []
        for ts in range(start_ts, end_ts + 1):
            for shard_id in range(self.num_shards):
                partition_key = f"{self.metric_name}#{ts}#{shard_id}"
                # Query this partition
                # Merge results

        return results
```

### Solution 2: Caching Hot Data

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    CACHING FOR HOT DATA                                      │
│                                                                              │
│  Most hot partition problems are READ problems                              │
│  Solution: Cache the hot data in front of the partition                    │
│                                                                              │
│  Without Cache:                                                              │
│                                                                              │
│  Requests ──────────────────────────────────► Hot Partition                │
│  1000 QPS                                     1000 QPS to DB                │
│                                               (overwhelmed)                  │
│                                                                              │
│  With Cache:                                                                │
│                                                                              │
│  Requests ──► Cache ──(miss)──► Hot Partition                              │
│  1000 QPS     950 hits          50 QPS to DB                               │
│               (95% hit rate)    (manageable)                                │
│                                                                              │
│  APPROACHES:                                                                │
│  ├── Application-level cache (Redis/Memcached)                             │
│  ├── Read replicas for hot partitions                                      │
│  ├── CDN for read-heavy static content                                     │
│  └── Local in-process cache for very hot items                             │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

```python
class HotSpotCache:
    """
    Adaptive cache that automatically caches hot items
    """

    def __init__(self, db, cache, hot_threshold=100):
        self.db = db
        self.cache = cache
        self.hot_threshold = hot_threshold
        self.access_counts = {}  # key -> count in current window
        self.window_start = time.time()
        self.window_size = 60  # seconds

    def get(self, key: str) -> Any:
        self._record_access(key)

        # Check cache first
        cached = self.cache.get(key)
        if cached is not None:
            return cached

        # Cache miss - get from DB
        value = self.db.get(key)

        # If key is hot, cache it
        if self._is_hot(key):
            self.cache.set(key, value, ttl=60)

        return value

    def _record_access(self, key: str):
        now = time.time()

        # Reset window if needed
        if now - self.window_start > self.window_size:
            self.access_counts = {}
            self.window_start = now

        self.access_counts[key] = self.access_counts.get(key, 0) + 1

    def _is_hot(self, key: str) -> bool:
        return self.access_counts.get(key, 0) > self.hot_threshold
```

### Solution 3: Composite Partition Keys

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                  COMPOSITE PARTITION KEYS                                    │
│                                                                              │
│  Instead of partitioning by single attribute,                               │
│  use multiple attributes to spread load                                     │
│                                                                              │
│  EXAMPLE: Time-series data                                                  │
│                                                                              │
│  Bad: Partition by date only                                                │
│  Key: 2024-01-15                                                            │
│  Result: All of today's data in one partition                               │
│                                                                              │
│  Better: Partition by date + metric_id                                      │
│  Key: 2024-01-15#cpu_usage                                                  │
│  Key: 2024-01-15#memory                                                     │
│  Key: 2024-01-15#disk_io                                                    │
│  Result: Today's data spread across partitions                              │
│                                                                              │
│  Best: Partition by date + metric_id + shard                               │
│  Key: 2024-01-15#cpu_usage#shard0                                          │
│  Key: 2024-01-15#cpu_usage#shard1                                          │
│  Result: Even more distribution                                              │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Solution 4: Request Coalescing

```python
import asyncio
from typing import Dict, Any, List
from collections import defaultdict

class RequestCoalescer:
    """
    Coalesce multiple requests for same key into single DB query

    If 1000 users request same viral tweet:
    - Without coalescing: 1000 DB queries
    - With coalescing: 1 DB query, 1000 responses
    """

    def __init__(self, db, coalesce_window_ms=10):
        self.db = db
        self.coalesce_window = coalesce_window_ms / 1000
        self.pending: Dict[str, asyncio.Future] = {}
        self.locks: Dict[str, asyncio.Lock] = defaultdict(asyncio.Lock)

    async def get(self, key: str) -> Any:
        """
        Get value, coalescing concurrent requests
        """
        async with self.locks[key]:
            # If there's already a pending request for this key, wait for it
            if key in self.pending:
                return await self.pending[key]

            # Create a new future for this request
            future = asyncio.Future()
            self.pending[key] = future

        try:
            # Small delay to collect more requests
            await asyncio.sleep(self.coalesce_window)

            # Make single DB query
            value = await self.db.get(key)

            # Resolve the future - all waiters get the value
            future.set_result(value)
            return value

        finally:
            # Cleanup
            async with self.locks[key]:
                if key in self.pending:
                    del self.pending[key]


class BatchingCache:
    """
    Batch multiple cache misses into single DB query
    """

    def __init__(self, db, cache, batch_size=100, batch_timeout_ms=5):
        self.db = db
        self.cache = cache
        self.batch_size = batch_size
        self.batch_timeout = batch_timeout_ms / 1000
        self.pending_keys: List[str] = []
        self.pending_futures: Dict[str, asyncio.Future] = {}
        self.lock = asyncio.Lock()

    async def get_many(self, keys: List[str]) -> Dict[str, Any]:
        """
        Get multiple keys, batching cache misses
        """
        results = {}
        misses = []

        # Check cache first
        for key in keys:
            cached = self.cache.get(key)
            if cached is not None:
                results[key] = cached
            else:
                misses.append(key)

        if misses:
            # Batch the misses
            db_results = await self._batch_get(misses)
            results.update(db_results)

            # Cache the results
            for key, value in db_results.items():
                self.cache.set(key, value)

        return results

    async def _batch_get(self, keys: List[str]) -> Dict[str, Any]:
        """
        Batch multiple keys into single DB multi-get
        """
        return await self.db.multi_get(keys)
```

### Solution 5: Partition Splitting

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    PARTITION SPLITTING                                       │
│                                                                              │
│  When a partition becomes hot, automatically split it                       │
│                                                                              │
│  Before (hot):                                                               │
│                                                                              │
│  Partition A: ████████████████████████████████████████                     │
│               keys: a-z                                                      │
│               load: 10000 QPS                                                │
│                                                                              │
│  After (split):                                                              │
│                                                                              │
│  Partition A1: ████████████████████                                         │
│                keys: a-m                                                     │
│                load: 5000 QPS                                                │
│                                                                              │
│  Partition A2: ████████████████████                                         │
│                keys: n-z                                                     │
│                load: 5000 QPS                                                │
│                                                                              │
│  Used by:                                                                    │
│  ├── DynamoDB (Adaptive Capacity)                                          │
│  ├── Azure Cosmos DB (Partition Splitting)                                 │
│  ├── Google Cloud Spanner (Auto-splitting)                                 │
│  └── Apache HBase (Region splitting)                                       │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Prevention Strategies

```
┌─────────────────────────────────────────────────────────────────────────────┐
│               PREVENTING HOT PARTITIONS                                      │
│                                                                              │
│  1. CHOOSE PARTITION KEYS WISELY                                           │
│     ├── High cardinality (many distinct values)                            │
│     ├── Even distribution (not skewed)                                      │
│     ├── Access pattern awareness                                            │
│     └── Avoid: timestamps, sequential IDs, status fields                   │
│                                                                              │
│  2. TEST WITH REALISTIC DATA                                                │
│     ├── Load test with actual data distribution                            │
│     ├── Include hot items in tests                                         │
│     └── Test with traffic spikes                                           │
│                                                                              │
│  3. DESIGN FOR SKEW                                                         │
│     ├── Assume some keys will be 1000x hotter                              │
│     ├── Build in sharding capability                                        │
│     └── Have caching strategy ready                                        │
│                                                                              │
│  4. MONITORING FROM DAY ONE                                                 │
│     ├── Track per-partition metrics                                        │
│     ├── Alert on imbalance                                                 │
│     └── Dashboard showing distribution                                      │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Interview Tips

### Common Questions

**Q: How would you handle a viral tweet scenario?**
```
A: Multi-layer approach:
   1. CDN caching for the tweet content
   2. Application cache (Redis) for metadata
   3. Write sharding for engagement counters
   4. Request coalescing for concurrent reads
   5. Rate limiting per user
   6. Async processing for non-critical updates
```

**Q: Your partition key is user_id and one user has 100x the data of others. Solutions?**
```
A: Depends on the pattern:

   Read-heavy:
   - Cache that user's data aggressively
   - Read replicas for that partition

   Write-heavy:
   - Composite key: user_id + timestamp bucket
   - Write sharding: user_id + shard_id

   Both:
   - Consider different storage for power users
   - Async aggregation instead of real-time
```

### Red Flags

```
❌ "Just add more partitions"
   → Doesn't help if key distribution is skewed

❌ Not considering partition key design upfront
   → Hard to change later

❌ "Cache everything"
   → Doesn't help write-heavy hot spots

❌ Ignoring the monitoring aspect
   → Can't fix what you can't see
```

## Summary

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          KEY TAKEAWAYS                                       │
│                                                                              │
│  1. HOT PARTITIONS ARE COMMON                                               │
│     └── Real data is rarely uniformly distributed                           │
│     └── Temporal patterns create hotspots                                   │
│                                                                              │
│  2. DETECTION IS CRITICAL                                                   │
│     └── Monitor per-partition metrics                                       │
│     └── Alert on imbalance                                                  │
│     └── Track max/average ratios                                            │
│                                                                              │
│  3. SOLUTIONS DEPEND ON PATTERN                                             │
│     └── Read-heavy: Caching, replicas                                       │
│     └── Write-heavy: Sharding, batching                                     │
│     └── Both: Composite keys, splitting                                     │
│                                                                              │
│  4. PREVENTION > CURE                                                       │
│     └── Choose partition keys carefully                                     │
│     └── Design for skew from the start                                      │
│     └── Test with realistic distributions                                   │
│                                                                              │
│  5. TRADE-OFFS                                                              │
│     └── Sharding: Spreads writes, complicates reads                        │
│     └── Caching: Helps reads, stale data concerns                          │
│     └── Splitting: Automatic but complex                                    │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

**Next:** [Thundering Herd Problem](./08_thundering_herd.md) - When recovery causes more problems
