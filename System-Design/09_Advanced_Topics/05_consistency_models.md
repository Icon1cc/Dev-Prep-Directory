# Data Consistency Models

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                       CONSISTENCY MODELS                                      ║
║              What Guarantees Can Distributed Systems Provide?                 ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

## Why Consistency Models Matter

When data is replicated across multiple nodes, what guarantees do readers get? This is the fundamental question that consistency models answer.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                  THE CONSISTENCY SPECTRUM                                    │
│                                                                              │
│  STRONG                                                            WEAK     │
│  ◄──────────────────────────────────────────────────────────────────────►   │
│                                                                              │
│  Linearizable   Sequential   Causal   Read-Your   Monotonic   Eventual     │
│  (Strictest)    Consistency  Consis-  -Writes     Reads       Consistency  │
│                              tency                            (Weakest)    │
│                                                                              │
│  ◄─────────────────────────────────────────────────────────────────────►   │
│  More coordination needed                   Less coordination needed        │
│  Higher latency                             Lower latency                   │
│  Lower availability                         Higher availability             │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Strong Consistency (Linearizability)

The strongest consistency model - the system behaves as if there's only one copy of the data.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      LINEARIZABILITY                                         │
│                                                                              │
│  GUARANTEE:                                                                  │
│  Every operation appears to execute atomically at some point               │
│  between its invocation and response.                                       │
│                                                                              │
│  AS IF: Single copy of data with instant operations                        │
│                                                                              │
│  EXAMPLE (Linearizable):                                                    │
│                                                                              │
│  Client A:  ├─── write(x=1) ────┤                                          │
│  Client B:       ├─── read(x) ────┤  returns 0 or 1, not both             │
│  Client C:            ├─── read(x) ────┤  if B got 1, C must get 1        │
│                                                                              │
│  Timeline: ──────────────────────────────────────────────────────►         │
│                    │                                                        │
│            linearization point (write happened "here")                      │
│                                                                              │
│  EXAMPLE (NOT Linearizable):                                                │
│                                                                              │
│  Client A:  ├─── write(x=1) ────┤                                          │
│  Client B:       ├─── read(x) ────┤  returns 1                             │
│  Client C:            ├─── read(x) ────┤  returns 0  ← VIOLATION!          │
│                                                                              │
│  If B sees the new value, C (starting after B) must also see it            │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Implementing Linearizability

```python
class LinearizableRegister:
    """
    Linearizable register using consensus (like Raft)
    Every read and write goes through the leader
    """

    def __init__(self, raft_cluster):
        self.raft = raft_cluster

    def write(self, key, value):
        """
        Write by proposing to Raft log
        Returns only after majority acknowledges
        """
        # Propose to Raft - this is linearizable
        return self.raft.propose(Operation('write', key, value))

    def read(self, key):
        """
        Read must also go through Raft to be linearizable!

        Why? The leader might have been deposed and not know it.
        A "read" that just reads local state might be stale.
        """
        # Option 1: Read through Raft log
        return self.raft.propose(Operation('read', key))

        # Option 2: Leader confirms it's still leader (quorum read)
        # if self.raft.confirm_leadership():
        #     return self.local_store.get(key)
```

### Cost of Linearizability

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                 COST OF LINEARIZABILITY                                      │
│                                                                              │
│  LATENCY:                                                                   │
│  ├── Every operation requires consensus                                     │
│  ├── Minimum 1 round-trip to majority of nodes                             │
│  └── Cross-datacenter: 100ms+ per operation                                │
│                                                                              │
│  AVAILABILITY:                                                              │
│  ├── Requires majority of nodes available                                   │
│  ├── Network partition → minority cannot serve requests                    │
│  └── This is the "CP" in CAP theorem                                       │
│                                                                              │
│  THROUGHPUT:                                                                │
│  ├── All operations serialized through leader                              │
│  ├── Single point of bottleneck                                            │
│  └── Scaling requires sharding                                              │
│                                                                              │
│  WHEN TO USE:                                                               │
│  ├── Financial transactions                                                 │
│  ├── Distributed locks                                                      │
│  ├── Unique ID generation                                                   │
│  └── Any "coordination" workload                                           │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Sequential Consistency

Weaker than linearizability but still provides strong ordering.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    SEQUENTIAL CONSISTENCY                                    │
│                                                                              │
│  GUARANTEE:                                                                  │
│  Operations from ALL processes appear in SOME sequential order             │
│  that is consistent with program order of each process.                    │
│                                                                              │
│  KEY DIFFERENCE FROM LINEARIZABILITY:                                       │
│  Operations don't need to respect real-time ordering                        │
│  Just need to be consistent with each process's local order                │
│                                                                              │
│  EXAMPLE (Sequential but not Linearizable):                                 │
│                                                                              │
│  Real-time:                                                                  │
│  Client A: write(x=1) ─────────────────────────────────────                │
│  Client B: ──────────── write(x=2) ────────────────────────                │
│  Client C: ───────────────────────── read(x)=2, read(x)=1                  │
│                                                                              │
│  This is sequentially consistent!                                           │
│  Global order could be: write(x=2), write(x=1), read, read                 │
│  C sees: 2 then 1 (consistent with this order)                             │
│                                                                              │
│  NOT Linearizable: Real-time says write(1) finished before write(2)        │
│  started, so 1 should be "older" than 2                                    │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Causal Consistency

Preserves cause-and-effect relationships while allowing more concurrency.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     CAUSAL CONSISTENCY                                       │
│                                                                              │
│  GUARANTEE:                                                                  │
│  If operation A "causes" operation B, everyone sees A before B             │
│  Concurrent operations may be seen in different orders                      │
│                                                                              │
│  "CAUSES" means:                                                            │
│  ├── Same process, A happens before B                                       │
│  ├── A is a write, B reads that value                                      │
│  └── Transitivity: A causes B, B causes C → A causes C                     │
│                                                                              │
│  EXAMPLE:                                                                    │
│                                                                              │
│  Alice posts: "I got the job!"                                              │
│  Bob (sees post) comments: "Congratulations!"                               │
│                                                                              │
│  Bob's comment is CAUSALLY DEPENDENT on Alice's post                       │
│  Everyone must see Alice's post before Bob's comment                        │
│                                                                              │
│  But if Carol also comments at same time:                                   │
│  ├── User 1 might see: Alice, Bob, Carol                                   │
│  └── User 2 might see: Alice, Carol, Bob                                   │
│  Both orderings are valid (Bob and Carol are concurrent)                   │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────┐           │
│  │  Alice: "I got the job!"                                    │           │
│  │         │                                                    │           │
│  │         ├────► Bob: "Congratulations!"  ─┐                  │           │
│  │         │                                │                   │           │
│  │         └────► Carol: "Great news!" ─────┼─► Both valid    │           │
│  │               (concurrent with Bob)      │    orderings    │           │
│  │                                          │                   │           │
│  └─────────────────────────────────────────────────────────────┘           │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

```python
class CausallyConsistentStore:
    """
    KV store with causal consistency using vector clocks
    """

    def __init__(self, node_id, all_nodes):
        self.node_id = node_id
        self.vector_clock = {n: 0 for n in all_nodes}
        self.store = {}  # key -> (value, vector_clock)
        self.pending_writes = []  # writes waiting for dependencies

    def write(self, key, value, dependencies=None):
        """
        Write with causal dependencies
        dependencies: vector clock from previous read
        """
        if dependencies:
            # Wait for all dependencies to be satisfied
            self._wait_for_dependencies(dependencies)

        # Increment our clock
        self.vector_clock[self.node_id] += 1

        # Store with current vector clock
        self.store[key] = (value, self.vector_clock.copy())

        # Replicate to other nodes
        self._replicate(key, value, self.vector_clock.copy())

    def read(self, key):
        """
        Read and return value with its vector clock (for dependencies)
        """
        if key in self.store:
            value, vc = self.store[key]
            return value, vc.copy()
        return None, self.vector_clock.copy()

    def receive_write(self, key, value, write_vc):
        """
        Receive replicated write from another node
        """
        # Check if we have all causal dependencies
        if self._has_dependencies(write_vc):
            self._apply_write(key, value, write_vc)
        else:
            # Queue for later
            self.pending_writes.append((key, value, write_vc))

    def _has_dependencies(self, write_vc):
        """
        Check if all writes that causally precede this one are applied
        """
        for node, time in write_vc.items():
            if node == self.node_id:
                continue
            if self.vector_clock.get(node, 0) < time - 1:
                return False
        return True

    def _apply_write(self, key, value, write_vc):
        """Apply write and update vector clock"""
        # Merge vector clocks
        for node, time in write_vc.items():
            self.vector_clock[node] = max(
                self.vector_clock.get(node, 0), time
            )

        # Apply write
        self.store[key] = (value, write_vc)

        # Check pending writes
        self._process_pending_writes()
```

## Read-Your-Writes Consistency

A session-level guarantee: you see your own writes.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                   READ-YOUR-WRITES CONSISTENCY                               │
│                                                                              │
│  GUARANTEE:                                                                  │
│  If a process writes value V, subsequent reads by SAME process             │
│  will see V (or later value), never older values.                          │
│                                                                              │
│  WITHOUT Read-Your-Writes (confusing for users!):                          │
│                                                                              │
│  User updates profile picture                                                │
│  User refreshes page                                                         │
│  User sees OLD profile picture (read from stale replica)                   │
│  User thinks update failed!                                                  │
│                                                                              │
│  WITH Read-Your-Writes:                                                     │
│                                                                              │
│  User updates profile picture                                                │
│  User refreshes page                                                         │
│  System ensures user sees their update                                       │
│                                                                              │
│  IMPLEMENTATION APPROACHES:                                                 │
│  ├── Sticky sessions (always read from same replica)                       │
│  ├── Version vectors (track what client has seen)                          │
│  ├── Read from primary after writes                                         │
│  └── Write-through cache                                                    │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

```python
class ReadYourWritesStore:
    """
    Store with read-your-writes guarantee using session tokens
    """

    def __init__(self, replicas):
        self.replicas = replicas
        self.primary = replicas[0]

    def write(self, session_id, key, value):
        """Write to primary, get version"""
        version = self.primary.write(key, value)

        # Return session token containing last write version
        return SessionToken(
            last_write_version={key: version},
            last_write_time=time.time()
        )

    def read(self, session_id, key, session_token=None):
        """
        Read ensuring we see at least our own writes
        """
        if session_token and key in session_token.last_write_version:
            required_version = session_token.last_write_version[key]

            # Try to find replica with this version
            for replica in self.replicas:
                value, version = replica.read(key)
                if version >= required_version:
                    return value, version

            # Fallback to primary (guaranteed to have latest)
            return self.primary.read(key)

        else:
            # No recent write to this key - any replica is fine
            return self._read_from_any_replica(key)
```

## Monotonic Reads

Once you see a value, you never see older values.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      MONOTONIC READS                                         │
│                                                                              │
│  GUARANTEE:                                                                  │
│  If a process reads value V1, subsequent reads will return                 │
│  V1 or a more recent value, never older.                                   │
│                                                                              │
│  WITHOUT Monotonic Reads (time travel!):                                    │
│                                                                              │
│  Read 1 (from replica A): balance = $100                                   │
│  Read 2 (from replica B): balance = $80   ← older value!                   │
│  Read 3 (from replica C): balance = $100                                   │
│                                                                              │
│  User sees: $100 → $80 → $100 (confusing!)                                 │
│                                                                              │
│  WITH Monotonic Reads:                                                      │
│                                                                              │
│  Read 1: balance = $100                                                     │
│  Read 2: balance = $100 or $110 (never $80)                               │
│  Read 3: balance >= Read 2's value                                         │
│                                                                              │
│  IMPLEMENTATION:                                                            │
│  ├── Track "high water mark" of versions seen                              │
│  ├── Only read from replicas with version >= high water mark               │
│  └── Or use sticky sessions                                                │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Eventual Consistency

The weakest model - replicas will eventually converge.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    EVENTUAL CONSISTENCY                                      │
│                                                                              │
│  GUARANTEE:                                                                  │
│  If no new writes occur, eventually all replicas will return               │
│  the same value.                                                            │
│                                                                              │
│  NO GUARANTEE ABOUT:                                                        │
│  ├── How long "eventually" takes                                           │
│  ├── What you see in the meantime                                          │
│  └── Order of updates                                                       │
│                                                                              │
│  Timeline:                                                                   │
│                                                                              │
│  Write(x=1) at Primary                                                      │
│       │                                                                      │
│       │    Replica A: x=1 ─────────────────────────────────►               │
│       │                                                                      │
│       │    Replica B: x=?  x=?  x=?  x=1 ───────────────────►              │
│       │                                    ▲                                │
│       │                                    │                                │
│       │                              "Eventually"                           │
│       │                                                                      │
│                                                                              │
│  CONFLICT RESOLUTION:                                                       │
│  Since order isn't guaranteed, conflicts need resolution:                   │
│  ├── Last-Writer-Wins (LWW): timestamp decides                             │
│  ├── Application-level merge (e.g., shopping cart union)                   │
│  ├── CRDTs (Conflict-free Replicated Data Types)                           │
│  └── Read-repair with quorum                                               │
│                                                                              │
│  WHEN TO USE:                                                               │
│  ├── Social media views/likes (approximate is fine)                        │
│  ├── DNS (eventual propagation)                                            │
│  ├── Caching layers                                                         │
│  └── Analytics data                                                         │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Quorum Consistency

A practical middle-ground using read/write quorums.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     QUORUM CONSISTENCY                                       │
│                                                                              │
│  N = total replicas                                                         │
│  W = write quorum (replicas that must acknowledge write)                   │
│  R = read quorum (replicas that must respond to read)                      │
│                                                                              │
│  RULE: W + R > N ensures overlap                                           │
│                                                                              │
│  Example: N=5, W=3, R=3                                                     │
│                                                                              │
│  Write to 3 replicas:    [✓] [✓] [✓] [ ] [ ]                              │
│  Read from 3 replicas:   [✓] [ ] [✓] [✓] [ ]                              │
│                              ▲                                              │
│                              │                                               │
│                         Overlap! At least 1 replica has latest             │
│                                                                              │
│  CONFIGURATIONS:                                                            │
│  ├── W=N, R=1: Fast reads, slow writes, highest consistency                │
│  ├── W=1, R=N: Fast writes, slow reads, highest consistency                │
│  ├── W=R=(N+1)/2: Balanced                                                 │
│  └── W=1, R=1: Eventual consistency (no overlap guarantee)                 │
│                                                                              │
│  NOTE: Even with W+R>N, not linearizable!                                  │
│  ├── Different clients might read from different quorums                   │
│  ├── They might see different "latest" values                              │
│  └── Need additional coordination for linearizability                       │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

```python
class QuorumStore:
    """
    Key-value store with configurable quorum consistency
    """

    def __init__(self, replicas, W, R):
        self.replicas = replicas
        self.N = len(replicas)
        self.W = W  # Write quorum
        self.R = R  # Read quorum

        assert W + R > self.N, "W + R must be > N for consistency"

    def write(self, key, value):
        """Write to W replicas"""
        version = int(time.time() * 1000000)  # Microsecond timestamp
        successes = 0
        errors = []

        for replica in self.replicas:
            try:
                replica.write(key, value, version)
                successes += 1
                if successes >= self.W:
                    return True
            except Exception as e:
                errors.append(e)

        if successes < self.W:
            raise WriteQuorumError(
                f"Only {successes}/{self.W} writes succeeded"
            )

    def read(self, key):
        """Read from R replicas, return latest"""
        responses = []
        errors = []

        for replica in self.replicas:
            try:
                value, version = replica.read(key)
                responses.append((value, version))
                if len(responses) >= self.R:
                    break
            except Exception as e:
                errors.append(e)

        if len(responses) < self.R:
            raise ReadQuorumError(
                f"Only {len(responses)}/{self.R} reads succeeded"
            )

        # Return value with highest version
        latest = max(responses, key=lambda x: x[1])

        # Optional: read-repair (update stale replicas)
        self._read_repair(key, latest[0], latest[1])

        return latest[0]

    def _read_repair(self, key, value, version):
        """Update any replica that has stale data"""
        for replica in self.replicas:
            try:
                _, replica_version = replica.read(key)
                if replica_version < version:
                    replica.write(key, value, version)
            except:
                pass
```

## Consistency Model Comparison

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                  CONSISTENCY MODEL COMPARISON                                │
│                                                                              │
│  Model            │ Latency │ Availability │ Complexity │ Use Case          │
│  ═════════════════╪═════════╪══════════════╪════════════╪═══════════════════│
│  Linearizable     │ High    │ Low          │ High       │ Distributed locks │
│  Sequential       │ Medium  │ Medium       │ High       │ Shared memory     │
│  Causal           │ Medium  │ High         │ Medium     │ Social apps       │
│  Read-your-writes │ Low     │ High         │ Low        │ User sessions     │
│  Monotonic reads  │ Low     │ High         │ Low        │ Client caching    │
│  Eventual         │ Low     │ Very High    │ Low        │ Analytics, DNS    │
│                                                                              │
│  PRACTICAL GUIDANCE:                                                        │
│  ├── Default to eventual consistency when possible                         │
│  ├── Add stronger guarantees only where needed                             │
│  ├── Mix models: strong for writes, weaker for reads                       │
│  └── Consider client-side caching with monotonic reads                     │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Interview Tips

### Common Questions

**Q: What's the difference between linearizability and serializability?**
```
A: Different contexts:
   - Linearizability: Single-object consistency in distributed systems
   - Serializability: Multi-object transaction isolation in databases

   Linearizability is about REAL-TIME ordering of operations
   Serializability is about ISOLATION of transactions

   Spanner provides both: "strict serializability"
```

**Q: How do you choose a consistency model?**
```
A: Consider:
   1. What does the application need?
      - Banking: Strong consistency
      - Social media views: Eventual is fine

   2. What can you afford in latency?
      - Cross-datacenter linearizable = 100ms+

   3. What happens during partitions?
      - Need availability? Use weaker consistency

   4. Can you tolerate inconsistency?
      - Brief: maybe OK
      - Permanent: usually not OK
```

**Q: Explain eventual consistency problems and solutions**
```
A: Problems:
   - Stale reads
   - Lost updates (concurrent writes)
   - Ordering violations

   Solutions:
   - CRDTs for automatic conflict resolution
   - Vector clocks for conflict detection
   - Read repair for consistency
   - Anti-entropy processes
```

### Red Flags

```
❌ "Just use strong consistency everywhere"
   → Shows lack of understanding of trade-offs

❌ Confusing consistency models
   → Know the differences!

❌ "Eventual consistency means data might be lost"
   → Wrong - it means temporary staleness, not data loss

❌ Not considering the CAP theorem
   → Consistency and availability trade-off during partitions
```

## Summary

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          KEY TAKEAWAYS                                       │
│                                                                              │
│  1. CONSISTENCY IS A SPECTRUM                                               │
│     └── From linearizable (strongest) to eventual (weakest)                 │
│     └── Stronger = more coordination = higher latency                       │
│                                                                              │
│  2. LINEARIZABILITY                                                         │
│     └── Acts like single copy of data                                       │
│     └── Expensive: requires consensus                                       │
│     └── Use for: locks, coordination                                        │
│                                                                              │
│  3. CAUSAL CONSISTENCY                                                      │
│     └── Preserves cause-and-effect                                          │
│     └── Good balance of consistency and performance                         │
│     └── Use for: social apps, collaborative editing                         │
│                                                                              │
│  4. EVENTUAL CONSISTENCY                                                    │
│     └── Replicas converge "eventually"                                      │
│     └── Highest availability and performance                                │
│     └── Use for: analytics, caching, low-priority data                     │
│                                                                              │
│  5. PRACTICAL ADVICE                                                        │
│     └── Start weak, strengthen only where needed                            │
│     └── Mix models in same system                                           │
│     └── Client-side techniques (session tokens) help a lot                 │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

**Next:** [Multi-Region Replication](./06_multi_region.md) - Consistency across datacenters
