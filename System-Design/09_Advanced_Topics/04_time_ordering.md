# Time and Ordering in Distributed Systems

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                      TIME AND ORDERING                                        ║
║            Why Clocks Are Unreliable and What To Do About It                  ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

## The Problem with Time

In distributed systems, you cannot rely on wall-clock time. This is one of the most counterintuitive aspects of distributed computing.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                  WHY TIME IS HARD IN DISTRIBUTED SYSTEMS                     │
│                                                                              │
│  You might think: "Just synchronize all clocks with NTP!"                   │
│                                                                              │
│  Reality:                                                                    │
│  ├── NTP accuracy: 1-50ms on internet, 0.1-1ms on LAN                      │
│  ├── Clock drift: Quartz clocks drift ~1 second per day                    │
│  ├── Clock jumps: NTP corrections can jump time forward or backward        │
│  ├── Leap seconds: Occasional 61-second minutes                            │
│  └── Network delay: Variable, unpredictable                                 │
│                                                                              │
│  EXAMPLE PROBLEM:                                                           │
│                                                                              │
│  Server A (clock slightly fast):  10:00:00.100                             │
│  Server B (clock slightly slow):  10:00:00.000                             │
│                                                                              │
│  Timeline:                                                                   │
│  T1: User updates record on Server A (timestamp: 10:00:00.100)             │
│  T2: Update propagates to Server B                                          │
│  T3: User updates same record on Server B (timestamp: 10:00:00.050)        │
│                                                                              │
│  Problem: B's update has EARLIER timestamp but happened LATER!             │
│  If we use timestamps for conflict resolution: WRONG ANSWER                │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Types of Time

### Physical Clocks vs Logical Clocks

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    PHYSICAL vs LOGICAL CLOCKS                                │
│                                                                              │
│  PHYSICAL CLOCKS                                                            │
│  ════════════════                                                           │
│  └── Wall-clock time (what time is it?)                                    │
│  └── Measured in seconds since epoch                                        │
│  └── Synchronized via NTP, GPS, atomic clocks                               │
│  └── UNRELIABLE across machines                                             │
│                                                                              │
│  LOGICAL CLOCKS                                                             │
│  ═══════════════                                                            │
│  └── Counter-based ordering                                                 │
│  └── "Did A happen before B?"                                               │
│  └── No relation to wall-clock time                                         │
│  └── RELIABLE for ordering events                                           │
│                                                                              │
│  KEY INSIGHT:                                                               │
│  Usually we don't need to know WHEN something happened                      │
│  We need to know what happened FIRST (ordering)                             │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Lamport Clocks

Leslie Lamport's logical clock algorithm (1978) - foundational to distributed systems.

### The Happens-Before Relation

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     HAPPENS-BEFORE RELATION (→)                              │
│                                                                              │
│  Event A "happens-before" Event B (written A → B) if:                       │
│                                                                              │
│  1. A and B are in same process, and A comes before B                       │
│                                                                              │
│  2. A is sending a message, B is receiving that message                     │
│                                                                              │
│  3. Transitivity: if A → B and B → C, then A → C                           │
│                                                                              │
│  CONCURRENT EVENTS:                                                         │
│  If neither A → B nor B → A, events are concurrent (A || B)                │
│  We cannot determine which happened "first"                                 │
│                                                                              │
│                                                                              │
│  Process 1    Process 2    Process 3                                        │
│      │            │            │                                            │
│     (a)           │            │        a → b (same process)                │
│      │            │            │                                            │
│     (b)──────────►(c)          │        b → c (message)                     │
│      │            │            │                                            │
│      │           (d)───────────►(e)     d → e (message)                     │
│      │            │            │                                            │
│     (f)           │           (g)       f || g (concurrent!)                │
│      │            │            │                                            │
│                                                                              │
│  We know: a → b → c → d → e                                                │
│  But: f and g are CONCURRENT - no ordering possible!                       │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Lamport Clock Algorithm

```python
class LamportClock:
    """
    Lamport logical clock implementation
    """

    def __init__(self):
        self.time = 0

    def tick(self):
        """
        Called before any local event
        """
        self.time += 1
        return self.time

    def send_message(self):
        """
        Called when sending a message
        Returns timestamp to include in message
        """
        self.time += 1
        return self.time

    def receive_message(self, message_timestamp):
        """
        Called when receiving a message
        Updates clock based on sender's timestamp
        """
        # Take maximum of local and received, then increment
        self.time = max(self.time, message_timestamp) + 1
        return self.time

    def get_time(self):
        return self.time


# Example usage
class Process:
    def __init__(self, pid):
        self.pid = pid
        self.clock = LamportClock()
        self.events = []

    def local_event(self, description):
        """Record a local event"""
        timestamp = self.clock.tick()
        event = (timestamp, self.pid, description)
        self.events.append(event)
        print(f"Process {self.pid}: {description} at Lamport time {timestamp}")
        return event

    def send(self, other_process, message):
        """Send message to another process"""
        timestamp = self.clock.send_message()
        print(f"Process {self.pid}: Sending '{message}' at Lamport time {timestamp}")
        other_process.receive(self.pid, timestamp, message)

    def receive(self, sender_pid, sender_timestamp, message):
        """Receive message from another process"""
        timestamp = self.clock.receive_message(sender_timestamp)
        print(f"Process {self.pid}: Received '{message}' from {sender_pid}, "
              f"updated time to {timestamp}")


# Demonstration
p1 = Process(1)
p2 = Process(2)

p1.local_event("Start")           # P1: time = 1
p1.local_event("Read file")       # P1: time = 2
p1.send(p2, "Hello")              # P1: time = 3, P2: time = 4
p2.local_event("Process data")    # P2: time = 5
p2.send(p1, "Response")           # P2: time = 6, P1: time = 7
```

### Lamport Clock Properties

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                   LAMPORT CLOCK PROPERTIES                                   │
│                                                                              │
│  GUARANTEES:                                                                │
│  ├── If A → B, then LC(A) < LC(B)                                          │
│  └── Causal ordering is preserved                                           │
│                                                                              │
│  LIMITATIONS:                                                               │
│  ├── If LC(A) < LC(B), we CANNOT conclude A → B                            │
│  │   (could be concurrent events)                                           │
│  └── Cannot detect concurrent events                                        │
│                                                                              │
│  EXAMPLE:                                                                    │
│                                                                              │
│  Process 1      Process 2                                                   │
│     │              │                                                        │
│    (1)            (1)     Both do local events, both have LC=1             │
│     │              │                                                        │
│    (2)            (2)     Both increment again, both have LC=2             │
│     │              │                                                        │
│                                                                              │
│  Both events at LC=2 are concurrent!                                        │
│  But Lamport clocks can't tell us this                                      │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Vector Clocks

Vector clocks extend Lamport clocks to detect concurrent events.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       VECTOR CLOCKS                                          │
│                                                                              │
│  Instead of single counter, maintain vector of counters                     │
│  One entry per process in the system                                        │
│                                                                              │
│  For 3 processes: [P1_time, P2_time, P3_time]                              │
│                                                                              │
│  RULES:                                                                     │
│  1. Initial: all zeros [0, 0, 0]                                           │
│  2. Local event: increment own entry                                        │
│  3. Send: increment own entry, attach vector to message                    │
│  4. Receive: merge vectors (element-wise max), then increment own          │
│                                                                              │
│  COMPARISON:                                                                │
│  V1 < V2 iff all(V1[i] <= V2[i]) AND any(V1[i] < V2[i])                   │
│  If neither V1 < V2 nor V2 < V1, events are CONCURRENT                     │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Vector Clock Example

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    VECTOR CLOCK WALKTHROUGH                                  │
│                                                                              │
│  Process 1         Process 2         Process 3                              │
│  [P1,P2,P3]        [P1,P2,P3]        [P1,P2,P3]                             │
│                                                                              │
│  [0,0,0]           [0,0,0]           [0,0,0]     Initial                    │
│     │                 │                 │                                    │
│  [1,0,0]              │                 │        P1: local event            │
│     │                 │                 │                                    │
│     ├────msg────────► │                 │                                    │
│     │              [1,1,0]              │        P2: receive, merge+inc     │
│     │                 │                 │                                    │
│     │                 │              [0,0,1]     P3: local event            │
│     │                 │                 │                                    │
│     │                 ├──────────────►  │                                    │
│     │                 │              [1,1,2]     P3: receive, merge+inc     │
│     │                 │                 │                                    │
│  [2,0,0]              │                 │        P1: local event            │
│     │                 │                 │                                    │
│                                                                              │
│  COMPARISONS:                                                                │
│  [1,1,0] vs [0,0,1]: Neither < other → CONCURRENT!                         │
│  [1,0,0] vs [1,1,2]: [1,0,0] < [1,1,2] → happens-before                   │
│  [2,0,0] vs [1,1,2]: Neither < other → CONCURRENT!                         │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Vector Clock Implementation

```python
from typing import Dict, List, Tuple, Optional

class VectorClock:
    """
    Vector clock for detecting causality and concurrency
    """

    def __init__(self, process_id: str, all_processes: List[str]):
        self.process_id = process_id
        self.clock: Dict[str, int] = {p: 0 for p in all_processes}

    def tick(self) -> Dict[str, int]:
        """Increment own component for local event"""
        self.clock[self.process_id] += 1
        return self.clock.copy()

    def send(self) -> Dict[str, int]:
        """Prepare timestamp for sending message"""
        self.clock[self.process_id] += 1
        return self.clock.copy()

    def receive(self, other_clock: Dict[str, int]) -> Dict[str, int]:
        """Merge received clock and increment own"""
        # Element-wise max
        for process, time in other_clock.items():
            self.clock[process] = max(self.clock.get(process, 0), time)

        # Increment own
        self.clock[self.process_id] += 1
        return self.clock.copy()

    def get_clock(self) -> Dict[str, int]:
        return self.clock.copy()

    @staticmethod
    def compare(vc1: Dict[str, int], vc2: Dict[str, int]) -> str:
        """
        Compare two vector clocks
        Returns: 'before', 'after', 'concurrent', or 'equal'
        """
        all_keys = set(vc1.keys()) | set(vc2.keys())

        less_or_equal = True
        greater_or_equal = True
        all_equal = True

        for key in all_keys:
            v1 = vc1.get(key, 0)
            v2 = vc2.get(key, 0)

            if v1 < v2:
                greater_or_equal = False
                all_equal = False
            elif v1 > v2:
                less_or_equal = False
                all_equal = False

        if all_equal:
            return 'equal'
        elif less_or_equal:
            return 'before'  # vc1 happened before vc2
        elif greater_or_equal:
            return 'after'   # vc1 happened after vc2
        else:
            return 'concurrent'


# Example: Conflict detection in distributed database
class DistributedKVStore:
    """
    Key-value store using vector clocks for conflict detection
    """

    def __init__(self, node_id: str, all_nodes: List[str]):
        self.node_id = node_id
        self.all_nodes = all_nodes
        self.clock = VectorClock(node_id, all_nodes)
        # Store: key -> [(value, vector_clock)]
        self.store: Dict[str, List[Tuple[any, Dict[str, int]]]] = {}

    def put(self, key: str, value: any,
            context: Optional[Dict[str, int]] = None) -> Dict[str, int]:
        """
        Put value with optional context (previous read's clock)
        """
        if context:
            self.clock.receive(context)

        timestamp = self.clock.tick()

        # Remove values that this write supersedes
        if key in self.store:
            self.store[key] = [
                (v, vc) for (v, vc) in self.store[key]
                if VectorClock.compare(vc, timestamp) != 'before'
            ]
            self.store[key].append((value, timestamp))
        else:
            self.store[key] = [(value, timestamp)]

        return timestamp

    def get(self, key: str) -> List[Tuple[any, Dict[str, int]]]:
        """
        Get all current values (may have conflicts/siblings)
        """
        if key not in self.store:
            return []

        # Return all concurrent values
        return self.store[key].copy()

    def resolve_conflict(self, key: str, resolved_value: any):
        """
        Client resolves conflict by providing merged value
        """
        if key not in self.store:
            return

        # Merge all existing clocks
        merged_clock = {}
        for _, vc in self.store[key]:
            for process, time in vc.items():
                merged_clock[process] = max(merged_clock.get(process, 0), time)

        # Create new value with merged clock
        self.clock.receive(merged_clock)
        timestamp = self.clock.tick()
        self.store[key] = [(resolved_value, timestamp)]
```

## Hybrid Logical Clocks (HLC)

Modern systems often use Hybrid Logical Clocks - combining physical time with logical ordering.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    HYBRID LOGICAL CLOCKS                                     │
│                                                                              │
│  MOTIVATION:                                                                │
│  ├── Physical time is useful (timestamps, TTLs, debugging)                 │
│  ├── But physical time is unreliable for ordering                          │
│  └── HLC: best of both worlds                                              │
│                                                                              │
│  FORMAT: (physical_time, logical_counter)                                   │
│                                                                              │
│  RULES:                                                                     │
│  ├── Physical time provides rough ordering and human-readable time         │
│  ├── Logical counter breaks ties when physical times are close             │
│  └── Always >= physical time, always >= last timestamp                     │
│                                                                              │
│  ALGORITHM:                                                                  │
│  Local event or send:                                                       │
│    l' = max(l, pt)    # pt = current physical time                         │
│    if l' == l:                                                              │
│        c' = c + 1     # increment counter                                  │
│    else:                                                                     │
│        c' = 0         # reset counter                                       │
│    return (l', c')                                                          │
│                                                                              │
│  Receive:                                                                    │
│    l' = max(l, m.l, pt)  # m.l = message's l                               │
│    if l' == l == m.l:                                                       │
│        c' = max(c, m.c) + 1                                                │
│    elif l' == l:                                                            │
│        c' = c + 1                                                           │
│    elif l' == m.l:                                                          │
│        c' = m.c + 1                                                         │
│    else:                                                                     │
│        c' = 0                                                               │
│    return (l', c')                                                          │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

```python
import time

class HybridLogicalClock:
    """
    Hybrid Logical Clock implementation
    Used in CockroachDB, MongoDB, and other modern systems
    """

    def __init__(self, max_clock_drift_ms: int = 500):
        self.l = 0  # Physical time component
        self.c = 0  # Logical counter
        self.max_drift = max_clock_drift_ms

    def _physical_time_ms(self) -> int:
        """Get current physical time in milliseconds"""
        return int(time.time() * 1000)

    def now(self) -> tuple:
        """
        Generate timestamp for local event
        """
        pt = self._physical_time_ms()

        if pt > self.l:
            self.l = pt
            self.c = 0
        else:
            self.c += 1

        return (self.l, self.c)

    def send(self) -> tuple:
        """Generate timestamp for sending message"""
        return self.now()

    def receive(self, msg_l: int, msg_c: int) -> tuple:
        """
        Update clock on receiving message
        """
        pt = self._physical_time_ms()

        # Sanity check: don't accept timestamps too far in future
        if msg_l - pt > self.max_drift:
            raise ClockDriftError(f"Message timestamp too far in future")

        old_l = self.l

        # l' = max(l, m.l, pt)
        self.l = max(self.l, msg_l, pt)

        if self.l == old_l == msg_l:
            self.c = max(self.c, msg_c) + 1
        elif self.l == old_l:
            self.c = self.c + 1
        elif self.l == msg_l:
            self.c = msg_c + 1
        else:
            self.c = 0

        return (self.l, self.c)

    def get_timestamp(self) -> tuple:
        return (self.l, self.c)

    @staticmethod
    def compare(ts1: tuple, ts2: tuple) -> int:
        """
        Compare two HLC timestamps
        Returns: -1 if ts1 < ts2, 0 if equal, 1 if ts1 > ts2
        """
        if ts1[0] != ts2[0]:
            return -1 if ts1[0] < ts2[0] else 1
        if ts1[1] != ts2[1]:
            return -1 if ts1[1] < ts2[1] else 1
        return 0
```

## TrueTime (Google Spanner)

Google's approach to distributed time using hardware and bounded uncertainty.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      GOOGLE TRUETIME                                         │
│                                                                              │
│  CONCEPT:                                                                   │
│  Instead of returning a single timestamp, TrueTime returns an INTERVAL     │
│                                                                              │
│  TT.now() returns [earliest, latest]                                        │
│  Actual time is GUARANTEED to be within this interval                       │
│                                                                              │
│  IMPLEMENTATION:                                                             │
│  ├── GPS receivers in every datacenter                                      │
│  ├── Atomic clocks as backup                                                │
│  ├── Multiple time sources, cross-validated                                 │
│  └── Uncertainty typically 1-7 milliseconds                                 │
│                                                                              │
│  USAGE IN SPANNER:                                                          │
│  To ensure T1 commits before T2:                                            │
│  ├── T1 commits at time s1                                                  │
│  ├── Wait until TT.after(s1) is true                                       │
│  ├── Then T2 can start                                                      │
│  └── This is called "commit wait"                                          │
│                                                                              │
│  │◄──── uncertainty ────►│                                                  │
│  │                       │                                                  │
│  [earliest ────────────► latest]                                            │
│                                                                              │
│  If s1.latest < s2.earliest, we KNOW s1 happened before s2                 │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Comparison of Clock Types

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     CLOCK TYPE COMPARISON                                    │
│                                                                              │
│  Type          │ Detects    │ Concurrent │ Real Time │ Used In             │
│                │ Causality  │ Detection  │           │                     │
│  ══════════════╪════════════╪════════════╪═══════════╪═════════════════════│
│  Physical      │ No         │ No         │ Yes       │ Logging, TTL        │
│  Lamport       │ Partial    │ No         │ No        │ Total ordering      │
│  Vector        │ Yes        │ Yes        │ No        │ DynamoDB, Riak      │
│  HLC           │ Partial    │ No         │ Yes       │ CockroachDB, MongoDB│
│  TrueTime      │ Yes        │ Yes        │ Yes       │ Google Spanner      │
│                                                                              │
│  TRADE-OFFS:                                                                │
│  ├── Lamport: Simple but can't detect concurrent events                    │
│  ├── Vector: Detect concurrency but grows with # of nodes                  │
│  ├── HLC: Good balance for most systems                                    │
│  └── TrueTime: Best guarantees but needs special hardware                  │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Interview Tips

### Common Questions

**Q: Why can't we just use NTP-synchronized clocks?**
```
A: Three problems:
   1. NTP accuracy is limited (1-50ms on internet)
   2. Clocks drift between sync intervals
   3. Clock can jump backward during correction

   Result: Two events at "same time" may have happened
   seconds apart, or in reverse order.
```

**Q: When would you use vector clocks vs Lamport clocks?**
```
A: Lamport clocks:
   - When you need total ordering
   - When detecting concurrency isn't needed
   - Lower overhead (single integer)

   Vector clocks:
   - When you need to detect concurrent updates
   - Conflict resolution in distributed databases
   - Higher overhead (vector of integers)
```

**Q: How does Amazon DynamoDB handle conflicts?**
```
A: DynamoDB uses vector clocks:
   1. Each write includes context (vector clock)
   2. If writes are concurrent, both are kept as "siblings"
   3. On read, client receives all siblings
   4. Client resolves conflict and writes back
   5. This is "last writer wins" or application-resolved
```

### Red Flags

```
❌ "Just use timestamps for ordering"
   → Shows lack of distributed systems understanding

❌ "NTP keeps all clocks synchronized"
   → Underestimates clock synchronization difficulty

❌ Not knowing about concurrent events
   → Missing key concept in distributed systems

❌ Confusing Lamport clocks with vector clocks
   → Know the difference!
```

## Summary

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           KEY TAKEAWAYS                                      │
│                                                                              │
│  1. PHYSICAL TIME IS UNRELIABLE                                             │
│     └── Clocks drift, jump, and have limited accuracy                       │
│     └── Cannot use for ordering across machines                             │
│                                                                              │
│  2. LOGICAL CLOCKS SOLVE ORDERING                                           │
│     └── Lamport clocks: simple, total ordering                              │
│     └── Vector clocks: detect concurrent events                             │
│     └── HLC: combines physical and logical benefits                         │
│                                                                              │
│  3. HAPPENS-BEFORE IS KEY CONCEPT                                           │
│     └── A → B means A causally precedes B                                   │
│     └── If neither A → B nor B → A, events are concurrent                  │
│     └── Concurrent events have no defined ordering                          │
│                                                                              │
│  4. PRACTICAL APPLICATIONS                                                  │
│     └── DynamoDB: vector clocks for conflict detection                      │
│     └── CockroachDB: HLC for ordering                                       │
│     └── Spanner: TrueTime for global consistency                            │
│                                                                              │
│  5. FOR INTERVIEWS                                                          │
│     └── Know why physical clocks are unreliable                             │
│     └── Explain Lamport clock algorithm                                     │
│     └── Know when to use vector clocks                                      │
│     └── Understand trade-offs                                               │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

**Next:** [Consistency Models](./05_consistency_models.md) - Understanding different consistency guarantees
