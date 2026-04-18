# Replication Strategies

## What is Replication?

**Simple explanation**: Replication is keeping copies of the same data on multiple machines. If one machine dies, others have the data. It's like having backup keys to your house—lose one, and you're still not locked out.

**Technical definition**: Database replication is the process of copying data from one database server (the primary) to one or more other servers (replicas) to ensure data redundancy, improve availability, and distribute read load.

```
WITHOUT REPLICATION:                 WITH REPLICATION:
┌─────────────────┐                 ┌─────────────────┐
│   Single DB     │                 │   Primary DB    │
│                 │                 │                 │
│   All data      │                 │   All data      │
│   Single copy   │                 │   (Source)      │
└─────────────────┘                 └────────┬────────┘
        │                                    │
        │                           ┌────────┴────────┐
        ▼                           │                 │
   If it dies,               ┌──────▼──────┐   ┌──────▼──────┐
   DATA LOST!                │  Replica 1  │   │  Replica 2  │
                             │  (Copy)     │   │  (Copy)     │
                             └─────────────┘   └─────────────┘
                                    │
                                    ▼
                             If primary dies,
                             replicas survive!
```

## Why Replicate?

| Goal | How Replication Helps |
|------|----------------------|
| **High Availability** | If primary fails, replica takes over |
| **Read Scalability** | Distribute reads across multiple servers |
| **Disaster Recovery** | Replicas in different data centers survive regional failures |
| **Reduce Latency** | Place replicas closer to users geographically |
| **Backup Without Downtime** | Backup from replica, not production primary |

## Replication Topologies

### 1. Single-Leader (Primary-Replica) Replication

**How it works**: One server (leader/primary) handles all writes. It replicates changes to followers (replicas) which handle reads.

```
                    WRITES
                       │
                       ▼
              ┌────────────────┐
              │    LEADER      │
              │   (Primary)    │
              │                │
              │  Handles all   │
              │    writes      │
              └───────┬────────┘
                      │
           ┌──────────┼──────────┐
           │          │          │
           ▼          ▼          ▼
      ┌─────────┐ ┌─────────┐ ┌─────────┐
      │Follower1│ │Follower2│ │Follower3│
      │ (Read)  │ │ (Read)  │ │ (Read)  │
      └─────────┘ └─────────┘ └─────────┘
           ▲          ▲          ▲
           │          │          │
           └──────────┴──────────┘
                   READS
```

**Synchronous vs Asynchronous**:

```
SYNCHRONOUS:
┌────────┐  1. Write  ┌────────┐
│ Client │ ─────────► │ Leader │
└────────┘            └───┬────┘
                          │ 2. Replicate
                          ▼
                    ┌──────────┐
                    │ Follower │ 3. ACK
                    └────┬─────┘
                         │
                         ▼
                4. Success to Client

✓ Strong consistency
✗ Higher latency (wait for replica)
✗ Availability hit if replica is slow


ASYNCHRONOUS:
┌────────┐  1. Write  ┌────────┐
│ Client │ ─────────► │ Leader │ 2. Success to Client
└────────┘            └───┬────┘
                          │
                          │ 3. Replicate (background)
                          ▼
                    ┌──────────┐
                    │ Follower │
                    └──────────┘

✓ Low latency
✓ High availability
✗ May lose data if leader fails before replication
```

**Pros**:
- Simple to understand and implement
- No write conflicts (single write point)
- Read scalability (add more followers)

**Cons**:
- Leader is single point of failure for writes
- Replication lag can cause stale reads
- Leader can become bottleneck

**When to use**:
- Read-heavy workloads (10:1 or higher read:write ratio)
- Applications that can tolerate slight staleness
- Most common choice for web applications

---

### 2. Multi-Leader Replication

**How it works**: Multiple servers can accept writes. Each leader replicates its changes to all other leaders.

```
                    ┌─────────────────────────────────┐
                    │                                 │
              ┌─────▼─────┐                   ┌───────▼───┐
   Writes ──► │  Leader 1 │ ◄───Replicate───► │  Leader 2 │ ◄── Writes
              │  (US)     │                   │  (EU)     │
              └─────┬─────┘                   └─────┬─────┘
                    │                               │
              ┌─────▼─────┐                   ┌─────▼─────┐
              │ Followers │                   │ Followers │
              └───────────┘                   └───────────┘
```

**Conflict Resolution**:

```
CONFLICT SCENARIO:
User A (US): Update profile.name = "Alice"    (timestamp: 10:00:01)
User B (EU): Update profile.name = "Alicia"   (timestamp: 10:00:02)

Both writes succeed locally, but conflict when replicated!

RESOLUTION STRATEGIES:

1. Last-Write-Wins (LWW):
   - Higher timestamp wins
   - Simple but can lose data
   - profile.name = "Alicia" (10:00:02 wins)

2. Merge Values:
   - Combine conflicting changes
   - profile.name = "Alice/Alicia" or prompt user

3. Custom Logic:
   - Application-specific rules
   - e.g., "US region takes precedence"

4. Conflict-free Replicated Data Types (CRDTs):
   - Data structures designed to merge automatically
   - Counters, sets, registers
```

**Pros**:
- No single point of failure for writes
- Better write throughput
- Good for multi-region deployments

**Cons**:
- Write conflicts are complex to handle
- More complex to implement and debug
- Potential for divergent data

**When to use**:
- Multi-data center deployments
- Collaborative editing (Google Docs style)
- Offline-first applications

---

### 3. Leaderless Replication

**How it works**: No designated leader. Any node can accept reads and writes. Clients write to multiple nodes and read from multiple nodes.

```
                    ┌─────────┐
              ┌─────│  Node A │─────┐
              │     └─────────┘     │
              │                     │
         ┌────▼────┐           ┌────▼────┐
         │  Node B │◄─────────►│  Node C │
         └────┬────┘           └────┬────┘
              │                     │
              │     ┌─────────┐     │
              └─────│  Node D │─────┘
                    └─────────┘

Client writes to multiple nodes simultaneously
```

**Quorum Reads and Writes**:

```
N = total nodes
W = write quorum (nodes that must acknowledge write)
R = read quorum (nodes that must respond to read)

RULE: W + R > N ensures overlap (at least one node has latest data)

Example: N=3, W=2, R=2

WRITE: "name=Alice"
┌────────┐
│ Client │──┬──► Node A: ✓ ACK
└────────┘  │
            ├──► Node B: ✓ ACK (W=2 achieved, success!)
            │
            └──► Node C: (may or may not receive)

READ:
┌────────┐
│ Client │──┬──► Node A: "name=Alice"
└────────┘  │
            ├──► Node B: "name=Alice"
            │
            └──► Node C: "name=Bob" (stale)

Client takes most recent value: "name=Alice"
```

**Quorum Configuration Trade-offs**:

| Configuration | Properties |
|--------------|------------|
| W=N, R=1 | Fast reads, slow writes |
| W=1, R=N | Fast writes, slow reads |
| W=N/2+1, R=N/2+1 | Balanced, majority quorum |
| W=1, R=1 | Weak consistency, possible stale reads |

**Pros**:
- No single point of failure
- High availability (survives node failures)
- Tunable consistency

**Cons**:
- Complex conflict resolution
- Higher latency for strong consistency
- More complex client logic

**When to use**:
- Highly available systems (Cassandra, DynamoDB)
- Eventually consistent data
- Multi-region deployments

---

## Replication Lag

### The Problem

```
Timeline:
t=0     t=1     t=2     t=3     t=4
│       │       │       │       │
▼       ▼       ▼       ▼       ▼
┌───────────────────────────────────────────┐
│ Leader  │ Write │       │       │         │
│         │ X=10  │       │       │         │
├─────────┼───────┼───────┼───────┼─────────┤
│ Replica │       │       │ X=10  │         │ ← Lag = 2 time units
│         │       │       │arrives│         │
├─────────┼───────┼───────┼───────┼─────────┤
│ Client  │       │Read X │       │         │
│ reads   │       │from   │       │         │
│ replica │       │replica│       │         │
│         │       │X=OLD! │       │         │ ← Stale read!
└─────────┴───────┴───────┴───────┴─────────┘
```

### Read-Your-Own-Writes

**Problem**: User writes data, immediately reads, gets old value.

```
SOLUTION: Read-Your-Own-Writes
┌────────────────────────────────────────────┐
│ After a write, route subsequent reads      │
│ from that user to the leader (or wait      │
│ for replica to catch up)                   │
└────────────────────────────────────────────┘

Implementation:
1. Track last_write_timestamp per user
2. If read_time < last_write_time + threshold:
   - Route to leader, OR
   - Wait for replica to catch up
```

### Monotonic Reads

**Problem**: User sees data go "backwards" in time.

```
SOLUTION: Monotonic Reads
┌────────────────────────────────────────────┐
│ Route all reads from the same user to      │
│ the same replica (sticky sessions)         │
└────────────────────────────────────────────┘
```

## Failover

When a leader fails, a follower must be promoted.

### Failover Process

```
┌─────────────────────────────────────────────────────────────┐
│                    FAILOVER PROCESS                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. DETECTION                                                │
│     Heartbeat timeout (typically 10-30 seconds)             │
│                                                              │
│  2. ELECTION                                                 │
│     Choose most up-to-date replica                          │
│                                                              │
│  3. RECONFIGURATION                                          │
│     - Promote replica to leader                             │
│     - Redirect clients to new leader                        │
│     - Other replicas follow new leader                      │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Failover Pitfalls

```
SPLIT BRAIN:
Old leader comes back online, thinks it's still leader
Solution: Fencing tokens (old leader's writes rejected)

DATA LOSS:
Async replication means new leader may be behind
Solution: Accept possible data loss or use sync replication

CASCADING FAILURES:
Failover triggers flood of reconnections
Solution: Rate limit reconnections, gradual traffic shift
```

## Comparison Table

| Aspect | Single-Leader | Multi-Leader | Leaderless |
|--------|--------------|--------------|------------|
| **Write Throughput** | Limited by leader | High | High |
| **Read Throughput** | High (add replicas) | High | High |
| **Consistency** | Easy | Conflict resolution needed | Tunable |
| **Availability** | Leader SPOF | High | Highest |
| **Complexity** | Low | High | Medium |
| **Use Cases** | Most apps | Multi-region | Highly available |
| **Examples** | MySQL, PostgreSQL | CouchDB | Cassandra, DynamoDB |

## Interview Questions

### Basic
1. "What is database replication and why is it needed?"
2. "What's the difference between synchronous and asynchronous replication?"
3. "How does read scaling work with replication?"

### Intermediate
4. "What is replication lag and how do you handle it?"
5. "How does failover work? What can go wrong?"
6. "Explain the differences between single-leader and multi-leader replication."

### Advanced
7. "How would you design replication for a global application?"
8. "What is split-brain and how do you prevent it?"
9. "How do quorum reads/writes work in leaderless replication?"

## Sample Interview Answer

**Q: "You're designing a social media application. How would you set up database replication?"**

**Strong Answer**:
"I'd use single-leader replication with asynchronous followers for this read-heavy workload.

**Architecture**:
- One primary in the main region handling all writes
- Multiple read replicas (3-5) in the same region for read scaling
- One or two replicas in other geographic regions for latency

**Why single-leader**: Social media is read-heavy (maybe 100:1 read:write). Single-leader gives us simple consistency model.

**Handling replication lag**:
- For the user who posted: read-your-own-writes by routing to leader for 5 seconds after posting
- For other users: eventual consistency is acceptable
- Monotonic reads via sticky sessions

**Failover**:
- Automated failover with 30-second detection threshold
- Most up-to-date replica promoted
- Accept that we might lose a few seconds of writes"

## Key Takeaways

```
┌────────────────────────────────────────────────────────────────┐
│                 REPLICATION DECISION GUIDE                      │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  What's your primary goal?                                     │
│                                                                 │
│  ├── High Availability                                         │
│  │   └── Any replication + automated failover                  │
│  │                                                              │
│  ├── Read Scalability                                          │
│  │   └── Single-leader + many read replicas                    │
│  │                                                              │
│  ├── Write Scalability                                         │
│  │   └── Sharding (replication alone won't help)               │
│  │                                                              │
│  ├── Multi-Region Low Latency                                  │
│  │   └── Multi-leader or leaderless                            │
│  │                                                              │
│  └── Maximum Availability                                      │
│      └── Leaderless with quorum                                │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

---

*Next: [Partitioning Schemes](03_partitioning.md) →*
