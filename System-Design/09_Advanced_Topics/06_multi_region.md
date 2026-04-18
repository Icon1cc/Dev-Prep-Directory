# Multi-Region Replication

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                     MULTI-REGION REPLICATION                                  ║
║                Building Globally Distributed Systems                          ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

## Why Multi-Region?

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    REASONS FOR MULTI-REGION                                  │
│                                                                              │
│  1. LATENCY                                                                 │
│     └── Users in Tokyo shouldn't wait 200ms for US servers                 │
│     └── Local region = 10-50ms vs cross-continent = 100-200ms              │
│                                                                              │
│  2. AVAILABILITY                                                            │
│     └── Entire region can fail (natural disaster, power outage)            │
│     └── Multi-region = survive regional failures                           │
│                                                                              │
│  3. DATA SOVEREIGNTY                                                        │
│     └── GDPR: EU data must stay in EU                                      │
│     └── China, Russia, etc. have data localization laws                    │
│                                                                              │
│  4. DISASTER RECOVERY                                                       │
│     └── Can failover to another region                                      │
│     └── RPO/RTO requirements often mandate multi-region                    │
│                                                                              │
│  THE CHALLENGE:                                                             │
│  ═══════════════                                                            │
│  Speed of light is ~200km/ms in fiber                                       │
│  NY to London: ~5500km = ~55ms round trip minimum                          │
│  NY to Tokyo: ~10800km = ~108ms round trip minimum                         │
│                                                                              │
│  You CANNOT make this faster. Physics wins.                                │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Replication Topologies

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                   REPLICATION TOPOLOGIES                                     │
│                                                                              │
│  1. PRIMARY-SECONDARY (Master-Slave)                                        │
│     ══════════════════════════════════                                      │
│                                                                              │
│     ┌─────────────┐                                                         │
│     │   PRIMARY   │  ◄── All writes go here                                │
│     │   (US-East) │                                                         │
│     └──────┬──────┘                                                         │
│            │                                                                 │
│       async│replication                                                      │
│            │                                                                 │
│     ┌──────┴──────┬─────────────┐                                          │
│     ▼             ▼             ▼                                           │
│  ┌──────┐    ┌──────┐    ┌──────┐                                          │
│  │ Read │    │ Read │    │ Read │  ◄── Reads can go to any                 │
│  │Replica    │Replica    │Replica                                           │
│  │EU-West    │Asia │    │US-West│                                          │
│  └──────┘    └──────┘    └──────┘                                          │
│                                                                              │
│  Pros: Simple, strong consistency for writes                                │
│  Cons: Write latency for non-primary regions, single point of failure      │
│                                                                              │
│                                                                              │
│  2. MULTI-PRIMARY (Multi-Master)                                           │
│     ═══════════════════════════════                                         │
│                                                                              │
│     ┌──────┐         ┌──────┐         ┌──────┐                             │
│     │Primary│ ◄─────► │Primary│ ◄─────► │Primary│                           │
│     │US-East│         │EU-West│         │ Asia │                            │
│     └──────┘         └──────┘         └──────┘                             │
│        │                 │                 │                                │
│        ▼                 ▼                 ▼                                │
│     Reads &           Reads &           Reads &                             │
│     Writes            Writes            Writes                              │
│                                                                              │
│  Pros: Low write latency everywhere                                         │
│  Cons: Conflict resolution complexity, eventual consistency                │
│                                                                              │
│                                                                              │
│  3. PARTITIONED BY REGION                                                   │
│     ════════════════════════                                                │
│                                                                              │
│     ┌──────────────────────────────────────────────┐                       │
│     │  US Users' Data          EU Users' Data      │                       │
│     │  ┌──────┐               ┌──────┐            │                       │
│     │  │US-East│               │EU-West│            │                       │
│     │  │Primary│               │Primary│            │                       │
│     │  └──────┘               └──────┘            │                       │
│     │     │                       │                │                       │
│     │     ▼                       ▼                │                       │
│     │  ┌──────┐               ┌──────┐            │                       │
│     │  │US-West│               │EU-East│            │                       │
│     │  │Replica│               │Replica│            │                       │
│     │  └──────┘               └──────┘            │                       │
│     └──────────────────────────────────────────────┘                       │
│                                                                              │
│  Pros: Data locality, compliance, lower latency                            │
│  Cons: Cross-region queries are slow, routing complexity                   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Consistency Challenges

### The CAP Reality

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                  MULTI-REGION CAP TRADE-OFFS                                 │
│                                                                              │
│  SCENARIO: Network partition between US and EU                              │
│                                                                              │
│       US Region              ║              EU Region                       │
│     ┌──────────┐            ║            ┌──────────┐                      │
│     │  Primary │            ║            │ Replica  │                      │
│     │  Node A  │──── X ─────║─────X ─────│  Node B  │                      │
│     └──────────┘    ▲       ║            └──────────┘                      │
│                     │       ║                                               │
│              Network partition                                               │
│                                                                              │
│  OPTION 1: CHOOSE CONSISTENCY (CP)                                          │
│  ─────────────────────────────────                                          │
│  EU region stops accepting writes                                           │
│  ├── Write: "Sorry, primary unavailable"                                   │
│  ├── Read: Return last known value OR reject                               │
│  └── Result: EU users experience downtime                                  │
│                                                                              │
│  OPTION 2: CHOOSE AVAILABILITY (AP)                                         │
│  ─────────────────────────────────                                          │
│  Both regions continue accepting writes                                     │
│  ├── Write: Accept locally, sync later                                     │
│  ├── Read: Return local value (maybe stale)                                │
│  └── Result: Potential conflicts when partition heals                      │
│                                                                              │
│  REAL SYSTEMS: Usually pick AP with conflict resolution                    │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Conflict Resolution Strategies

```python
from typing import Dict, List, Any
from dataclasses import dataclass
from datetime import datetime
import json

@dataclass
class WriteRecord:
    value: Any
    timestamp: datetime
    region: str
    vector_clock: Dict[str, int]

class ConflictResolver:
    """
    Different strategies for resolving multi-region conflicts
    """

    @staticmethod
    def last_writer_wins(writes: List[WriteRecord]) -> WriteRecord:
        """
        Simple: latest timestamp wins

        Pros: Simple, deterministic
        Cons: Clock skew can cause unexpected results, data loss
        """
        return max(writes, key=lambda w: w.timestamp)

    @staticmethod
    def region_priority(writes: List[WriteRecord],
                       priority: List[str]) -> WriteRecord:
        """
        Designated "primary" region wins ties

        Pros: Predictable, no data loss from primary
        Cons: Secondary region changes may be lost
        """
        def region_rank(w):
            try:
                return priority.index(w.region)
            except ValueError:
                return len(priority)

        # First by priority, then by timestamp
        return min(writes, key=lambda w: (region_rank(w), -w.timestamp.timestamp()))

    @staticmethod
    def merge_crdt_counter(writes: List[WriteRecord]) -> int:
        """
        CRDT G-Counter: merge by taking max per region

        Pros: Automatic resolution, no data loss
        Cons: Only works for specific data types
        """
        merged = {}
        for write in writes:
            region = write.region
            value = write.value  # Assume value is region's counter
            merged[region] = max(merged.get(region, 0), value)
        return sum(merged.values())

    @staticmethod
    def merge_set_union(writes: List[WriteRecord]) -> set:
        """
        CRDT G-Set: merge by union

        Pros: No conflicts possible
        Cons: Items can never be removed
        """
        result = set()
        for write in writes:
            result.update(write.value)
        return result

    @staticmethod
    def return_all_siblings(writes: List[WriteRecord]) -> List[WriteRecord]:
        """
        Return all conflicting values, let application resolve

        Pros: No data loss, application-specific logic
        Cons: Complexity pushed to application
        """
        # Filter to concurrent writes only
        siblings = []
        for w1 in writes:
            is_superseded = False
            for w2 in writes:
                if w1 != w2 and _happens_before(w1.vector_clock, w2.vector_clock):
                    is_superseded = True
                    break
            if not is_superseded:
                siblings.append(w1)
        return siblings


def _happens_before(vc1: Dict[str, int], vc2: Dict[str, int]) -> bool:
    """Check if vc1 happens before vc2"""
    all_keys = set(vc1.keys()) | set(vc2.keys())
    less_or_equal = all(vc1.get(k, 0) <= vc2.get(k, 0) for k in all_keys)
    strictly_less = any(vc1.get(k, 0) < vc2.get(k, 0) for k in all_keys)
    return less_or_equal and strictly_less
```

## Replication Patterns

### Synchronous vs Asynchronous

```
┌─────────────────────────────────────────────────────────────────────────────┐
│            SYNCHRONOUS vs ASYNCHRONOUS REPLICATION                           │
│                                                                              │
│  SYNCHRONOUS (Strong Consistency):                                          │
│  ═════════════════════════════════                                          │
│                                                                              │
│  Client ──► Primary ──► Secondary ──► Primary ──► Client                   │
│         write      replicate    ack        ack                              │
│                                                                              │
│  └────────────────── wait ─────────────────────┘                           │
│                                                                              │
│  Latency: Primary write + network to secondary + secondary write            │
│  Cross-region: 100-200ms+ per write                                         │
│                                                                              │
│  Used by: Google Spanner (with TrueTime)                                   │
│                                                                              │
│                                                                              │
│  ASYNCHRONOUS (Eventual Consistency):                                       │
│  ════════════════════════════════════                                       │
│                                                                              │
│  Client ──► Primary ──► Client                                             │
│         write      ack                                                      │
│             │                                                               │
│             └──► Secondary (later, in background)                          │
│                                                                              │
│  Latency: Just primary write time                                           │
│  Local write: 1-10ms                                                        │
│                                                                              │
│  Used by: Most systems (DynamoDB, Cassandra, MongoDB)                      │
│                                                                              │
│                                                                              │
│  SEMI-SYNCHRONOUS (Quorum):                                                 │
│  ═══════════════════════════                                                │
│                                                                              │
│  Client ──► Primary + 1 Secondary ──► Client                               │
│         write to quorum        ack                                          │
│             │                                                               │
│             └──► Remaining secondaries (async)                             │
│                                                                              │
│  Latency: Primary + fastest secondary                                       │
│  Usually: Local secondary available, fast                                   │
│                                                                              │
│  Used by: CockroachDB (Raft-based)                                         │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Implementation Pattern

```python
class MultiRegionDatabase:
    """
    Multi-region database with configurable consistency
    """

    def __init__(self, local_region: str, regions: Dict[str, 'RegionNode']):
        self.local_region = local_region
        self.regions = regions
        self.local_node = regions[local_region]

    async def write_sync(self, key: str, value: Any) -> bool:
        """
        Synchronous write: wait for all regions
        Highest consistency, highest latency
        """
        tasks = []
        for region, node in self.regions.items():
            task = asyncio.create_task(node.write(key, value))
            tasks.append(task)

        results = await asyncio.gather(*tasks, return_exceptions=True)

        # All must succeed
        return all(r is True for r in results)

    async def write_async(self, key: str, value: Any) -> bool:
        """
        Asynchronous write: return after local write
        Lowest consistency, lowest latency
        """
        # Write locally
        success = await self.local_node.write(key, value)

        if success:
            # Replicate in background (don't wait)
            for region, node in self.regions.items():
                if region != self.local_region:
                    asyncio.create_task(
                        self._replicate_with_retry(node, key, value)
                    )

        return success

    async def write_quorum(self, key: str, value: Any,
                          quorum: int = None) -> bool:
        """
        Quorum write: wait for majority of regions
        Balanced consistency and latency
        """
        if quorum is None:
            quorum = len(self.regions) // 2 + 1

        tasks = []
        for region, node in self.regions.items():
            task = asyncio.create_task(node.write(key, value))
            tasks.append(task)

        # Wait for quorum
        successes = 0
        for coro in asyncio.as_completed(tasks):
            try:
                result = await coro
                if result:
                    successes += 1
                    if successes >= quorum:
                        return True
            except Exception:
                pass

        return False

    async def read_local(self, key: str) -> Any:
        """Read from local region only (fastest, may be stale)"""
        return await self.local_node.read(key)

    async def read_quorum(self, key: str) -> Any:
        """Read from quorum, return latest value"""
        quorum = len(self.regions) // 2 + 1

        tasks = []
        for region, node in self.regions.items():
            task = asyncio.create_task(node.read_with_version(key))
            tasks.append(task)

        responses = []
        for coro in asyncio.as_completed(tasks):
            try:
                value, version = await coro
                responses.append((value, version))
                if len(responses) >= quorum:
                    break
            except Exception:
                pass

        if len(responses) < quorum:
            raise QuorumNotReached()

        # Return highest version
        latest = max(responses, key=lambda x: x[1])
        return latest[0]

    async def _replicate_with_retry(self, node, key, value,
                                    max_retries=3):
        """Replicate with exponential backoff"""
        for attempt in range(max_retries):
            try:
                await node.write(key, value)
                return
            except Exception as e:
                wait_time = 2 ** attempt
                await asyncio.sleep(wait_time)

        # Final failure: add to retry queue
        await self._add_to_retry_queue(node, key, value)
```

## Active-Active vs Active-Passive

```
┌─────────────────────────────────────────────────────────────────────────────┐
│               ACTIVE-ACTIVE vs ACTIVE-PASSIVE                                │
│                                                                              │
│  ACTIVE-PASSIVE (Hot Standby):                                              │
│  ═════════════════════════════                                              │
│                                                                              │
│     Active (US-East)           Passive (US-West)                            │
│     ┌──────────────┐           ┌──────────────┐                            │
│     │  ████████    │   async   │  ░░░░░░░░    │                            │
│     │  ████████    │ ────────► │  ░░░░░░░░    │                            │
│     │  Serving     │   repl    │  Standby     │                            │
│     │  Traffic     │           │  (no traffic)│                            │
│     └──────────────┘           └──────────────┘                            │
│                                                                              │
│     On failure: Promote passive to active                                   │
│     RTO: Minutes to hours (depends on automation)                          │
│     Wasted resources: Passive region is idle                               │
│                                                                              │
│                                                                              │
│  ACTIVE-ACTIVE (Multi-Region):                                              │
│  ═════════════════════════════                                              │
│                                                                              │
│     Active (US-East)           Active (EU-West)                            │
│     ┌──────────────┐           ┌──────────────┐                            │
│     │  ████████    │   async   │  ████████    │                            │
│     │  ████████    │ ◄───────► │  ████████    │                            │
│     │  Serving     │   repl    │  Serving     │                            │
│     │  US Traffic  │           │  EU Traffic  │                            │
│     └──────────────┘           └──────────────┘                            │
│                                                                              │
│     On failure: Other region absorbs traffic                                │
│     RTO: Seconds (just DNS/routing change)                                 │
│     Better utilization: Both regions active                                │
│     More complex: Need conflict resolution                                  │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Global Traffic Management

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    ROUTING STRATEGIES                                        │
│                                                                              │
│  1. GEO-BASED ROUTING                                                       │
│     ═════════════════                                                       │
│     Route based on user's geographic location                               │
│                                                                              │
│     US User ──► GeoDNS ──► us-east.example.com                             │
│     EU User ──► GeoDNS ──► eu-west.example.com                             │
│     Asia User ─► GeoDNS ──► ap-northeast.example.com                       │
│                                                                              │
│  2. LATENCY-BASED ROUTING                                                   │
│     ═══════════════════════                                                 │
│     Route to region with lowest latency                                     │
│     AWS Route 53, Cloudflare, etc. measure this                            │
│                                                                              │
│  3. WEIGHTED ROUTING                                                        │
│     ═════════════════                                                       │
│     Distribute traffic by percentage                                        │
│     Useful for gradual rollouts                                             │
│                                                                              │
│     us-east: 70%                                                            │
│     us-west: 30%                                                            │
│                                                                              │
│  4. FAILOVER ROUTING                                                        │
│     ══════════════════                                                      │
│     Primary region until health check fails                                │
│     Then route to secondary                                                 │
│                                                                              │
│     Primary: us-east (health: ✓) ──► Route here                           │
│     Secondary: us-west (standby)                                            │
│                                                                              │
│     Primary: us-east (health: ✗) ──► Failover                             │
│     Secondary: us-west ◄─────────── Route here now                         │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Real-World Patterns

### Pattern 1: Global Read, Regional Write

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                 GLOBAL READ, REGIONAL WRITE                                  │
│                                                                              │
│  Use case: User profiles, settings, content                                 │
│                                                                              │
│  Architecture:                                                               │
│                                                                              │
│                      Write ──► Regional Primary                             │
│                                      │                                      │
│                             async replication                               │
│                                      │                                      │
│                                      ▼                                      │
│     ┌──────────────────────────────────────────────────────┐               │
│     │                  Global Read Replicas                 │               │
│     │                                                       │               │
│     │   US-East      EU-West      Asia      US-West        │               │
│     │   Replica      Replica      Replica    Replica       │               │
│     │     ◄── Read from any replica ──►                   │               │
│     │                                                       │               │
│     └──────────────────────────────────────────────────────┘               │
│                                                                              │
│  Consistency: Strong for writes, eventual for reads                        │
│  Latency: Low reads everywhere, writes go to primary                      │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Pattern 2: Follow-the-Sun

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      FOLLOW-THE-SUN                                          │
│                                                                              │
│  Primary moves based on business hours                                      │
│                                                                              │
│  00:00 - 08:00 UTC: Asia Primary                                           │
│  08:00 - 16:00 UTC: Europe Primary                                         │
│  16:00 - 00:00 UTC: Americas Primary                                       │
│                                                                              │
│     ┌──────────────────────────────────────────────────────┐               │
│     │    Asia           Europe          Americas           │               │
│     │                                                       │               │
│     │   ██████          ░░░░░░          ░░░░░░            │ 02:00 UTC     │
│     │   PRIMARY         Replica         Replica            │               │
│     │                                                       │               │
│     │   ░░░░░░          ██████          ░░░░░░            │ 10:00 UTC     │
│     │   Replica         PRIMARY         Replica            │               │
│     │                                                       │               │
│     │   ░░░░░░          ░░░░░░          ██████            │ 18:00 UTC     │
│     │   Replica         Replica         PRIMARY            │               │
│     │                                                       │               │
│     └──────────────────────────────────────────────────────┘               │
│                                                                              │
│  Benefit: Primary is always in "awake" region                              │
│  Challenge: Primary transitions need careful coordination                   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Interview Tips

### Common Questions

**Q: How do you design a globally consistent system?**
```
A: Options:
   1. Synchronous replication (high latency)
      - Google Spanner approach with TrueTime
      - Paxos/Raft across regions

   2. Accept eventual consistency
      - Most common approach
      - Design for conflict resolution
      - Use CRDTs where possible

   3. Partition by region
      - User data stays in their region
      - Cross-region only for global data
```

**Q: How do you handle cross-region failures?**
```
A: Layers of defense:
   1. Health checks detect failure
   2. DNS/load balancer routes away
   3. Writes queue for later replay
   4. Read from replicas continue
   5. Conflict resolution when back up
```

**Q: What's the trade-off between latency and consistency?**
```
A: Fundamental trade-off:
   - Strong consistency = wait for cross-region round trip
   - Eventual consistency = local latency, resolve conflicts later

   Numbers:
   - Same region: 1-10ms
   - Cross-continent: 100-200ms

   Most systems choose:
   - Strong consistency for critical data
   - Eventual consistency for everything else
```

### Red Flags

```
❌ "Just replicate everything synchronously"
   → Shows lack of understanding of latency constraints

❌ Ignoring conflict resolution
   → Multi-region eventually needs to handle conflicts

❌ "Eventual consistency means data loss"
   → Wrong - it means temporary staleness

❌ Not considering data sovereignty
   → Legal requirements matter
```

## Summary

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          KEY TAKEAWAYS                                       │
│                                                                              │
│  1. WHY MULTI-REGION                                                        │
│     └── Latency (be close to users)                                         │
│     └── Availability (survive regional failures)                            │
│     └── Compliance (data sovereignty)                                       │
│                                                                              │
│  2. TOPOLOGIES                                                              │
│     └── Primary-Secondary: Simple, higher write latency                     │
│     └── Multi-Primary: Low latency, conflict complexity                     │
│     └── Partitioned: Data locality, routing complexity                      │
│                                                                              │
│  3. CONSISTENCY TRADE-OFFS                                                  │
│     └── Sync replication: Strong consistency, high latency                  │
│     └── Async replication: Low latency, eventual consistency               │
│     └── Quorum: Middle ground                                               │
│                                                                              │
│  4. CONFLICT RESOLUTION                                                     │
│     └── Last-writer-wins (simple but data loss)                            │
│     └── CRDTs (automatic, limited data types)                              │
│     └── Application-level (most control, most work)                        │
│                                                                              │
│  5. PRACTICAL PATTERNS                                                      │
│     └── Global read, regional write                                         │
│     └── Active-active with geo-routing                                      │
│     └── Mix consistency levels per use case                                 │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

**Next:** [Hot Partition Problem](./07_hot_partitions.md) - Handling uneven data distribution
