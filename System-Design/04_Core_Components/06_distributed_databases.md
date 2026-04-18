# Distributed Databases

## What is a Distributed Database?

A **Distributed Database** stores data across multiple machines (nodes) in a network, appearing as a single logical database to applications. This enables horizontal scaling, fault tolerance, and geographic distribution.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Single vs Distributed Database                       │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Single Database:                 Distributed Database:               │
│   ────────────────                 ─────────────────────                │
│                                                                         │
│   ┌─────────────────┐             ┌─────────────────────────┐          │
│   │   Application   │             │      Application        │          │
│   └────────┬────────┘             └───────────┬─────────────┘          │
│            │                                  │                         │
│            ▼                        ┌─────────┴─────────┐              │
│   ┌─────────────────┐               │                   │              │
│   │                 │               ▼                   ▼              │
│   │    Database     │         ┌─────────┐         ┌─────────┐         │
│   │  (single node)  │         │  Node 1 │◄───────►│  Node 2 │         │
│   │                 │         └────┬────┘         └────┬────┘         │
│   └─────────────────┘              │                   │              │
│                                    │    ┌─────────┐    │              │
│   Limitations:                     └───►│  Node 3 │◄───┘              │
│   • Vertical scaling only               └─────────┘                    │
│   • Single point of failure                                            │
│   • Geographic limitations          Data distributed across nodes      │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Key Concepts

### 1. Replication

Copying data to multiple nodes for availability and read performance.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Replication Strategies                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   SINGLE-LEADER (Master-Slave):                                        │
│   ─────────────────────────────                                         │
│                                                                         │
│   Client Writes ──► Primary ──┬──► Replica 1 (async)                  │
│                               └──► Replica 2 (async)                  │
│                                                                         │
│   Client Reads ───► Any node                                           │
│                                                                         │
│   Pros: Simple, strong consistency for writes                          │
│   Cons: Primary is bottleneck, failover complexity                     │
│                                                                         │
│   ─────────────────────────────────────────────────────────────────────│
│                                                                         │
│   MULTI-LEADER:                                                        │
│   ─────────────                                                         │
│                                                                         │
│   US Region          EU Region                                         │
│   ┌─────────┐       ┌─────────┐                                       │
│   │ Leader  │◄─────►│ Leader  │ (sync or async)                       │
│   └────┬────┘       └────┬────┘                                       │
│        │                 │                                             │
│   ┌────┴────┐       ┌────┴────┐                                       │
│   │Replicas │       │Replicas │                                       │
│   └─────────┘       └─────────┘                                       │
│                                                                         │
│   Pros: Write scalability, multi-region                               │
│   Cons: Conflict resolution needed                                     │
│                                                                         │
│   ─────────────────────────────────────────────────────────────────────│
│                                                                         │
│   LEADERLESS:                                                          │
│   ───────────                                                           │
│                                                                         │
│   Client writes to ANY node (quorum-based)                            │
│                                                                         │
│   Write ──┬──► Node 1 ✓                                               │
│           ├──► Node 2 ✓  (2 of 3 = success)                          │
│           └──► Node 3 ✗                                               │
│                                                                         │
│   Pros: No single point of failure                                     │
│   Cons: Complex consistency, conflict handling                         │
│                                                                         │
│   Examples: Cassandra, DynamoDB                                        │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 2. Partitioning (Sharding)

Splitting data across nodes to enable horizontal scaling.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Partitioning Strategies                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   HASH PARTITIONING:                                                   │
│   ──────────────────                                                    │
│                                                                         │
│   partition = hash(key) % num_partitions                               │
│                                                                         │
│   user_123 → hash("123") % 3 = 1 → Partition 1                        │
│   user_456 → hash("456") % 3 = 0 → Partition 0                        │
│   user_789 → hash("789") % 3 = 2 → Partition 2                        │
│                                                                         │
│   Pros: Even distribution                                              │
│   Cons: No range queries, resharding is complex                       │
│                                                                         │
│   ─────────────────────────────────────────────────────────────────────│
│                                                                         │
│   RANGE PARTITIONING:                                                  │
│   ───────────────────                                                   │
│                                                                         │
│   Partition 0: A-M                                                     │
│   Partition 1: N-Z                                                     │
│                                                                         │
│   user_alice → Partition 0                                            │
│   user_zack  → Partition 1                                            │
│                                                                         │
│   Pros: Range queries work, data locality                             │
│   Cons: Hotspots possible (if names cluster)                          │
│                                                                         │
│   ─────────────────────────────────────────────────────────────────────│
│                                                                         │
│   CONSISTENT HASHING:                                                  │
│   ───────────────────                                                   │
│                                                                         │
│          Node A                                                        │
│            ●                                                            │
│        ╱       ╲        Keys hash to position on ring                 │
│      ●           ●      Keys owned by next node clockwise             │
│   Node D       Node B                                                  │
│      ●           ●                                                     │
│        ╲       ╱                                                       │
│            ●                                                            │
│          Node C                                                        │
│                                                                         │
│   Pros: Adding/removing nodes moves minimal data                      │
│   Cons: Can cause uneven distribution without virtual nodes           │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Consistency Models

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Consistency Models                                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   STRONG CONSISTENCY:                                                  │
│   ───────────────────                                                   │
│   Every read returns the most recent write                             │
│   All nodes see same data at same time                                 │
│                                                                         │
│   Write(x=5) ──► All replicas have x=5 before ACK                     │
│   Read() ──► Always returns 5                                         │
│                                                                         │
│   Pros: Predictable, easy to reason about                             │
│   Cons: Higher latency, lower availability                            │
│                                                                         │
│   ─────────────────────────────────────────────────────────────────────│
│                                                                         │
│   EVENTUAL CONSISTENCY:                                                │
│   ─────────────────────                                                 │
│   Given enough time, all replicas converge                             │
│   Reads may return stale data temporarily                              │
│                                                                         │
│   Write(x=5) ──► Primary has x=5                                      │
│   Read() ──► May return old value (x=3) briefly                       │
│   Later Read() ──► Returns x=5                                        │
│                                                                         │
│   Pros: High availability, low latency                                │
│   Cons: Complex application logic, stale reads                        │
│                                                                         │
│   ─────────────────────────────────────────────────────────────────────│
│                                                                         │
│   CAUSAL CONSISTENCY:                                                  │
│   ───────────────────                                                   │
│   Operations that are causally related are seen in order              │
│   Concurrent operations may be seen in different orders               │
│                                                                         │
│   If: Write(x=5) happens-before Read(x) → Read returns 5              │
│   Concurrent writes: May be seen in different orders                  │
│                                                                         │
│   ─────────────────────────────────────────────────────────────────────│
│                                                                         │
│   READ-YOUR-WRITES:                                                    │
│   ─────────────────                                                     │
│   User always sees their own writes                                   │
│                                                                         │
│   User writes x=5 → Same user reads → Returns 5                       │
│   Other users may see stale data                                      │
│                                                                         │
│   Implementation: Route user to same replica, or use sessions         │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## CAP Theorem Revisited

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    CAP Theorem in Practice                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│         Consistency (C)                                                │
│              ╱╲                                                         │
│             ╱  ╲                                                        │
│            ╱    ╲                                                       │
│           ╱ CP   ╲                                                      │
│          ╱        ╲                                                     │
│         ╱──────────╲                                                    │
│        ╱            ╲                                                   │
│       ╱      CA      ╲                                                  │
│      ╱________________╲                                                 │
│   Availability (A)  Partition                                          │
│              AP     Tolerance (P)                                      │
│                                                                         │
│   CA: Not realistic (network partitions happen)                        │
│   CP: Choose consistency over availability (e.g., HBase)              │
│   AP: Choose availability over consistency (e.g., Cassandra)          │
│                                                                         │
│   PACELC Extension:                                                    │
│   ─────────────────                                                     │
│   If Partition → choose A or C                                        │
│   Else (normal operation) → choose Latency or Consistency             │
│                                                                         │
│   Example decisions:                                                   │
│   • Banking: CP (consistency critical)                                │
│   • Social media: AP (availability matters more)                      │
│   • Shopping cart: AP with conflict resolution                        │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Quorum-Based Systems

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Quorum Reads and Writes                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   N = Total replicas                                                   │
│   W = Write quorum (must acknowledge)                                  │
│   R = Read quorum (must respond)                                       │
│                                                                         │
│   Guarantee strong consistency when: W + R > N                         │
│                                                                         │
│   Example: N=3, W=2, R=2                                              │
│   ─────────────────────────                                             │
│                                                                         │
│   Write request:                                                       │
│   Client ──┬──► Node 1 ✓                                              │
│            ├──► Node 2 ✓  W=2 satisfied, ACK to client               │
│            └──► Node 3 (async later)                                  │
│                                                                         │
│   Read request:                                                        │
│   Client ──┬──► Node 1 (v2)                                           │
│            ├──► Node 2 (v2)  R=2 satisfied, return v2                 │
│            └──► Node 3 (not queried)                                  │
│                                                                         │
│   Why it works:                                                        │
│   W=2, R=2, N=3 → At least 1 node has latest (2+2>3)                 │
│                                                                         │
│   Common configurations:                                               │
│   ──────────────────────                                                │
│   W=1, R=N  → Fast writes, slow reads (all must respond)             │
│   W=N, R=1  → Slow writes, fast reads                                 │
│   W=N/2+1, R=N/2+1 → Balanced (typical)                              │
│                                                                         │
│   Sloppy Quorum:                                                       │
│   ──────────────                                                        │
│   If preferred nodes unavailable, write to any N nodes                │
│   "Hinted handoff" repairs later                                      │
│   Trades consistency for availability                                  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Common Distributed Databases

### SQL (NewSQL)

| Database | Type | Consistency | Use Case |
|----------|------|-------------|----------|
| CockroachDB | Distributed SQL | Strong | OLTP, global |
| TiDB | MySQL compatible | Strong | MySQL replacement |
| Spanner | Google Cloud | Strong | Global ACID |
| YugabyteDB | PostgreSQL compatible | Strong | Cloud native |

### NoSQL

| Database | Type | Consistency | Use Case |
|----------|------|-------------|----------|
| Cassandra | Wide column | Tunable | Time series, IoT |
| DynamoDB | Key-value | Tunable | Serverless, AWS |
| MongoDB | Document | Configurable | Flexible schema |
| Redis Cluster | In-memory | Eventual | Caching, sessions |

---

## Handling Failures

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Failure Scenarios                                    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   1. NODE FAILURE                                                      │
│      ────────────                                                       │
│      Node dies → Replicas serve reads                                 │
│      → Data re-replicated to maintain RF                              │
│                                                                         │
│   2. NETWORK PARTITION                                                 │
│      ─────────────────                                                  │
│      Split brain possible                                              │
│      CP: Minority partition becomes read-only                          │
│      AP: Both partitions accept writes (conflict later)               │
│                                                                         │
│   3. SLOW NODE                                                         │
│      ─────────                                                          │
│      Timeout and retry on other replicas                              │
│      Speculative execution (send to multiple, take first)             │
│                                                                         │
│   4. DATA CORRUPTION                                                   │
│      ───────────────                                                    │
│      Checksums detect corruption                                       │
│      Read repair from healthy replicas                                 │
│                                                                         │
│   Recovery Mechanisms:                                                 │
│   ────────────────────                                                  │
│   • Read repair: Fix stale data on read                               │
│   • Anti-entropy: Background synchronization                          │
│   • Merkle trees: Efficient comparison of data                        │
│   • Hinted handoff: Store writes for failed nodes                     │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## When to Use / When NOT to Use

### When to Use Distributed Database

✅ Data exceeds single machine capacity
✅ Need high availability (can't afford downtime)
✅ Geographic distribution required
✅ Read/write throughput beyond single node
✅ Need horizontal scaling

### When NOT to Use

❌ Data fits on single node
❌ Strong ACID transactions across all data
❌ Simple queries, no scaling needs
❌ Team lacks distributed systems expertise
❌ Cost-sensitive (more nodes = more cost)

---

## Interview Traps

| Trap | What They're Testing | Good Answer |
|------|---------------------|-------------|
| "How to handle split brain?" | Partition handling | Leader election, quorum, or accept conflicts and resolve |
| "Why not just add replicas?" | Understanding limits | Replication doesn't scale writes; need partitioning |
| "ACID in distributed DB?" | Trade-off awareness | Possible but expensive (2PC); many use eventual consistency |
| "Cassandra vs MongoDB?" | Technology selection | Cassandra for scale/availability; MongoDB for flexibility/queries |

---

**Next:** Continue to [07_search_systems.md](./07_search_systems.md) to learn about full-text search.
