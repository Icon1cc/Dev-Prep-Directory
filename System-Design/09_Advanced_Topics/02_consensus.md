# Consensus Algorithms

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                        CONSENSUS ALGORITHMS                                   ║
║                  How Distributed Nodes Agree on State                         ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

## The Problem

In a distributed system, multiple nodes need to agree on shared state. This sounds simple but is actually one of the hardest problems in computer science.

### Why Is Consensus Hard?

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     THE CONSENSUS CHALLENGE                                  │
│                                                                              │
│  Imagine 5 servers need to agree on who is the leader:                      │
│                                                                              │
│     Server A: "I'll be leader!"                                             │
│     Server B: "No, I'll be leader!"                                         │
│     Server C: "I vote for A"                                                │
│     Server D: "I vote for B"                                                │
│     Server E: (network partition - can't communicate)                       │
│                                                                              │
│  Problems:                                                                   │
│  ├── Messages can be delayed, lost, or duplicated                           │
│  ├── Nodes can crash and restart                                            │
│  ├── Network can partition (split-brain)                                    │
│  ├── No global clock - can't say "decide at exactly 3:00 PM"               │
│  └── Nodes might disagree on who's alive                                    │
│                                                                              │
│  We need: Agreement even when some nodes fail or can't communicate          │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### FLP Impossibility

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    FLP IMPOSSIBILITY THEOREM (1985)                          │
│                                                                              │
│  "In an asynchronous distributed system, consensus is impossible            │
│   if even ONE node can crash."                                               │
│                                                                              │
│  What this means:                                                            │
│  ├── You CANNOT guarantee consensus will be reached in bounded time         │
│  ├── A slow node is indistinguishable from a crashed node                   │
│  └── Perfect consensus is theoretically impossible                          │
│                                                                              │
│  How real systems work around this:                                         │
│  ├── Use timeouts (assume slow = dead)                                      │
│  ├── Use randomization                                                      │
│  └── Accept that consensus might take arbitrarily long                     │
│                                                                              │
│  Practical result: Systems work most of the time, but can stall             │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Paxos: The Original

### Basic Idea

Paxos was invented by Leslie Lamport. It's theoretically elegant but notoriously difficult to understand and implement.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        PAXOS ROLES                                           │
│                                                                              │
│  PROPOSER                                                                    │
│  └── Proposes values for consensus                                          │
│                                                                              │
│  ACCEPTOR                                                                    │
│  └── Accepts or rejects proposals                                           │
│      └── Majority of acceptors must agree                                   │
│                                                                              │
│  LEARNER                                                                     │
│  └── Learns the decided value                                               │
│                                                                              │
│  (In practice, one node often plays all three roles)                        │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Paxos Phases

```
PHASE 1: PREPARE
════════════════

Proposer                              Acceptors
    │                                  │  │  │
    │──── Prepare(n) ─────────────────►│  │  │
    │                                  │  │  │
    │◄─── Promise(n, prev_value) ──────│  │  │
    │                                     │  │
    │◄─── Promise(n, null) ───────────────│  │
    │                                        │
    │◄─── Promise(n, null) ──────────────────│

Proposer asks: "Will you promise not to accept any proposal < n?"
Acceptors reply: "Yes, and here's the highest proposal I've seen"


PHASE 2: ACCEPT
═══════════════

Proposer                              Acceptors
    │                                  │  │  │
    │──── Accept(n, value) ───────────►│  │  │
    │                                  │  │  │
    │◄─── Accepted(n) ─────────────────│  │  │
    │                                     │  │
    │◄─── Accepted(n) ────────────────────│  │
    │                                        │
    │◄─── Accepted(n) ───────────────────────│

Proposer says: "Accept this value with proposal number n"
If majority accepts: consensus reached!
```

### Why Paxos Is Hard

```
Problems with Paxos:
├── Multiple proposers can conflict (livelock)
├── Proposal numbers must be globally unique
├── Implementation details are tricky
├── Multi-Paxos for sequences of values is complex
└── Lamport's paper is notoriously hard to read

"The dirty little secret of the Paxos algorithm is that while it
 is elegant, it is still very difficult to implement correctly."
                                           - Google engineers
```

## Raft: Understandable Consensus

Raft was designed specifically to be understandable. Same guarantees as Paxos, but much clearer.

### Raft Key Concepts

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         RAFT FUNDAMENTALS                                    │
│                                                                              │
│  KEY INSIGHT: Break consensus into three sub-problems:                      │
│  ├── 1. Leader Election                                                     │
│  ├── 2. Log Replication                                                     │
│  └── 3. Safety                                                              │
│                                                                              │
│  NODE STATES:                                                                │
│  ┌──────────┐         ┌───────────┐         ┌──────────┐                   │
│  │ FOLLOWER │ ◄─────► │ CANDIDATE │ ◄─────► │  LEADER  │                   │
│  └──────────┘         └───────────┘         └──────────┘                   │
│       │                     ▲                     │                         │
│       │                     │                     │                         │
│       └─────────────────────┴─────────────────────┘                         │
│              (on timeout)       (loses election / higher term)              │
│                                                                              │
│  TERMS:                                                                      │
│  ├── Time is divided into "terms" (like election cycles)                   │
│  ├── Each term has at most one leader                                       │
│  ├── Terms act as logical clocks                                            │
│  └── Stale term = stale information, reject it                             │
│                                                                              │
│       Term 1    │    Term 2     │    Term 3    │    Term 4                 │
│    ────────────┴───────────────┴──────────────┴──────────────►             │
│    Leader: A    │  Leader: B   │  (no leader) │  Leader: C                 │
│                 │              │   election   │                             │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Leader Election

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       RAFT LEADER ELECTION                                   │
│                                                                              │
│  INITIAL STATE: All nodes are followers                                     │
│                                                                              │
│  Node A        Node B        Node C        Node D        Node E             │
│  [Follower]    [Follower]    [Follower]    [Follower]    [Follower]         │
│      │             │             │             │             │               │
│      │             │             │             │             │               │
│      ▼             │             │             │             │               │
│  ┌────────┐        │             │             │             │               │
│  │Timeout!│        │             │             │             │               │
│  │No heart│        │             │             │             │               │
│  │-beat   │        │             │             │             │               │
│  └────────┘        │             │             │             │               │
│      │             │             │             │             │               │
│      ▼             │             │             │             │               │
│  [Candidate]       │             │             │             │               │
│  Term: 1           │             │             │             │               │
│      │             │             │             │             │               │
│      ├──RequestVote(term=1)──────┴─────────────┴─────────────┤              │
│      │                                                       │               │
│      │◄─────────────────VoteGranted─────────────────────────│              │
│      │             │             │             │             │               │
│      ▼             │             │             │             │               │
│  [LEADER]      [Follower]    [Follower]    [Follower]    [Follower]         │
│  Term: 1        Term: 1       Term: 1       Term: 1       Term: 1           │
│      │             │             │             │             │               │
│      ├───────AppendEntries (heartbeat)───────────────────────┤              │
│      │             │             │             │             │               │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Election Rules

```python
class RaftNode:
    """
    Simplified Raft node implementation
    """

    def __init__(self, node_id, peers):
        self.node_id = node_id
        self.peers = peers

        # Persistent state
        self.current_term = 0
        self.voted_for = None
        self.log = []

        # Volatile state
        self.state = "follower"
        self.leader_id = None

        # Timing
        self.election_timeout = self._random_timeout()
        self.last_heartbeat = time.time()

    def _random_timeout(self):
        """Random timeout between 150-300ms prevents split votes"""
        return random.uniform(0.15, 0.30)

    def check_election_timeout(self):
        """Called periodically - start election if no heartbeat"""
        if self.state == "leader":
            return

        if time.time() - self.last_heartbeat > self.election_timeout:
            self.start_election()

    def start_election(self):
        """Become candidate and request votes"""
        self.state = "candidate"
        self.current_term += 1
        self.voted_for = self.node_id  # Vote for self
        votes_received = 1  # Self-vote

        print(f"Node {self.node_id}: Starting election for term {self.current_term}")

        # Request votes from all peers
        for peer in self.peers:
            response = peer.request_vote(
                term=self.current_term,
                candidate_id=self.node_id,
                last_log_index=len(self.log) - 1,
                last_log_term=self._get_last_log_term()
            )

            if response['vote_granted']:
                votes_received += 1

            # Check if we got majority
            if votes_received > len(self.peers) // 2:
                self.become_leader()
                return

        # Didn't get majority - reset timeout and wait
        self.state = "follower"
        self.election_timeout = self._random_timeout()

    def request_vote(self, term, candidate_id, last_log_index, last_log_term):
        """Handle RequestVote RPC from candidate"""

        # Rule 1: Reply false if term < currentTerm
        if term < self.current_term:
            return {'term': self.current_term, 'vote_granted': False}

        # Update term if candidate has higher term
        if term > self.current_term:
            self.current_term = term
            self.voted_for = None
            self.state = "follower"

        # Rule 2: Vote if haven't voted yet AND candidate's log is up-to-date
        vote_granted = False
        if self.voted_for is None or self.voted_for == candidate_id:
            if self._is_log_up_to_date(last_log_index, last_log_term):
                vote_granted = True
                self.voted_for = candidate_id
                self.last_heartbeat = time.time()  # Reset election timer

        return {'term': self.current_term, 'vote_granted': vote_granted}

    def _is_log_up_to_date(self, candidate_last_index, candidate_last_term):
        """
        Raft's log comparison: candidate must have log at least as up-to-date
        """
        my_last_term = self._get_last_log_term()
        my_last_index = len(self.log) - 1

        # Higher term wins
        if candidate_last_term != my_last_term:
            return candidate_last_term > my_last_term

        # Same term: longer log wins
        return candidate_last_index >= my_last_index

    def become_leader(self):
        """Transition to leader state"""
        self.state = "leader"
        self.leader_id = self.node_id
        print(f"Node {self.node_id}: Became leader for term {self.current_term}")

        # Send initial heartbeat immediately
        self.send_heartbeat()

    def send_heartbeat(self):
        """Leader sends heartbeats to prevent elections"""
        for peer in self.peers:
            peer.append_entries(
                term=self.current_term,
                leader_id=self.node_id,
                entries=[],  # Empty for heartbeat
                leader_commit=self.commit_index
            )
```

### Log Replication

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        RAFT LOG REPLICATION                                  │
│                                                                              │
│  Client sends command to Leader                                             │
│                                                                              │
│  1. Leader appends to its log (uncommitted)                                 │
│  2. Leader sends AppendEntries to all followers                             │
│  3. Followers append to their logs and respond                              │
│  4. Once majority acknowledges, Leader commits                              │
│  5. Leader notifies followers of commit                                     │
│  6. All nodes apply committed entries to state machine                      │
│                                                                              │
│                                                                              │
│  LEADER LOG:                                                                │
│  ┌────┬────┬────┬────┬────┬────┬────┬────┐                                 │
│  │ 1  │ 1  │ 1  │ 2  │ 3  │ 3  │ 3  │ 3  │  ← term                        │
│  ├────┼────┼────┼────┼────┼────┼────┼────┤                                 │
│  │x←1 │y←9 │y←2 │x←3 │y←7 │x←5 │x←4 │z←2 │  ← command                     │
│  └────┴────┴────┴────┴────┴────┴────┴────┘                                 │
│    1    2    3    4    5    6    7    8     ← index                        │
│                             ▲                                               │
│                             │                                               │
│                        commitIndex (majority replicated)                    │
│                                                                              │
│  FOLLOWER LOG (slightly behind):                                            │
│  ┌────┬────┬────┬────┬────┬────┬────┐                                      │
│  │ 1  │ 1  │ 1  │ 2  │ 3  │ 3  │ 3  │                                      │
│  ├────┼────┼────┼────┼────┼────┼────┤                                      │
│  │x←1 │y←9 │y←2 │x←3 │y←7 │x←5 │x←4 │                                      │
│  └────┴────┴────┴────┴────┴────┴────┘                                      │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Log Replication Code

```python
def append_entries(self, term, leader_id, prev_log_index, prev_log_term,
                   entries, leader_commit):
    """
    Handle AppendEntries RPC from leader
    """
    # Rule 1: Reply false if term < currentTerm
    if term < self.current_term:
        return {'term': self.current_term, 'success': False}

    # Update state
    self.current_term = term
    self.state = "follower"
    self.leader_id = leader_id
    self.last_heartbeat = time.time()

    # Rule 2: Reply false if log doesn't contain entry at prevLogIndex
    # matching prevLogTerm
    if prev_log_index >= 0:
        if prev_log_index >= len(self.log):
            return {'term': self.current_term, 'success': False}
        if self.log[prev_log_index]['term'] != prev_log_term:
            # Delete conflicting entries
            self.log = self.log[:prev_log_index]
            return {'term': self.current_term, 'success': False}

    # Rule 3: Append any new entries not already in the log
    for i, entry in enumerate(entries):
        log_index = prev_log_index + 1 + i
        if log_index < len(self.log):
            if self.log[log_index]['term'] != entry['term']:
                # Conflict - delete this and all following
                self.log = self.log[:log_index]
                self.log.append(entry)
        else:
            self.log.append(entry)

    # Rule 4: Update commitIndex if leader's is higher
    if leader_commit > self.commit_index:
        self.commit_index = min(leader_commit, len(self.log) - 1)
        self._apply_committed_entries()

    return {'term': self.current_term, 'success': True}


def _apply_committed_entries(self):
    """Apply committed log entries to state machine"""
    while self.last_applied < self.commit_index:
        self.last_applied += 1
        entry = self.log[self.last_applied]
        self.state_machine.apply(entry['command'])
```

## Raft Safety Properties

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      RAFT SAFETY GUARANTEES                                  │
│                                                                              │
│  1. ELECTION SAFETY                                                         │
│     └── At most one leader per term                                         │
│         (majority vote required, nodes vote once per term)                  │
│                                                                              │
│  2. LEADER APPEND-ONLY                                                      │
│     └── Leader never overwrites or deletes its own log entries              │
│         (only appends new entries)                                          │
│                                                                              │
│  3. LOG MATCHING                                                            │
│     └── If two logs have entry with same index and term,                    │
│         all preceding entries are identical                                 │
│         (AppendEntries consistency check)                                   │
│                                                                              │
│  4. LEADER COMPLETENESS                                                     │
│     └── If entry is committed in a term, it will be in all                 │
│         future leaders' logs                                                │
│         (candidates must have up-to-date log to win)                       │
│                                                                              │
│  5. STATE MACHINE SAFETY                                                    │
│     └── If a node has applied entry at index, no other node                │
│         will apply different entry at that index                            │
│         (committed entries are permanent)                                   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Raft vs Paxos Comparison

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        RAFT vs PAXOS                                         │
│                                                                              │
│  Aspect              │ Paxos                  │ Raft                        │
│  ════════════════════╪════════════════════════╪═════════════════════════════│
│  Understandability   │ Notoriously difficult  │ Designed to be clear        │
│  Leader              │ Not required           │ Strong leader required      │
│  Log gaps            │ Can have gaps          │ No gaps allowed             │
│  Membership changes  │ Complex                │ Joint consensus             │
│  Implementation      │ Many variations        │ Single specification        │
│  Real-world use      │ Google Chubby          │ etcd, Consul, CockroachDB   │
│                                                                              │
│  KEY INSIGHT:                                                               │
│  Paxos and Raft provide the SAME guarantees                                 │
│  Raft is just easier to understand and implement correctly                  │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Where Consensus Is Used

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    CONSENSUS IN REAL SYSTEMS                                 │
│                                                                              │
│  COORDINATION SERVICES                                                       │
│  ├── ZooKeeper (ZAB - ZooKeeper Atomic Broadcast)                          │
│  ├── etcd (Raft)                                                            │
│  └── Consul (Raft)                                                          │
│                                                                              │
│  DISTRIBUTED DATABASES                                                       │
│  ├── CockroachDB (Raft)                                                     │
│  ├── TiDB (Raft)                                                            │
│  ├── YugabyteDB (Raft)                                                      │
│  └── Google Spanner (Paxos)                                                 │
│                                                                              │
│  MESSAGE QUEUES                                                             │
│  ├── Kafka (Uses ZooKeeper, moving to KRaft)                               │
│  └── Pulsar (BookKeeper consensus)                                          │
│                                                                              │
│  WHAT THEY USE IT FOR:                                                      │
│  ├── Leader election                                                        │
│  ├── Metadata storage                                                       │
│  ├── Configuration management                                               │
│  ├── Distributed locks                                                      │
│  └── Replicated state machines                                              │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Interview Tips

### What to Know

```
JUNIOR/MID:
├── Know consensus exists and why it's hard
├── Basic understanding of leader election
└── Know where it's used (ZooKeeper, etcd)

SENIOR:
├── Understand Raft at a high level
├── Know the phases: election, replication, commit
├── Understand quorum (majority) requirements
└── Know trade-offs (availability during partition)

STAFF+:
├── Deep understanding of Raft phases
├── Can discuss split-brain scenarios
├── Understand log compaction/snapshotting
├── Can compare Raft vs Paxos
└── Know practical implementation challenges
```

### Common Interview Questions

**Q: Why does Raft need a majority (quorum)?**
```
A: To ensure any two quorums overlap by at least one node.
   This guarantees that committed entries survive leader changes.

   5 nodes → need 3 for quorum
   Any two groups of 3 must share at least 1 node
   That shared node has the committed entry
```

**Q: What happens if the network partitions?**
```
A: The partition with majority continues operating.
   The minority partition cannot elect a leader or commit.
   When partition heals, minority catches up to majority.

   [A, B, C] | [D, E]  (partition)
       │         │
   Can elect    Cannot elect
   Can commit   Cannot commit
```

**Q: Why random election timeouts?**
```
A: To prevent split votes where everyone times out simultaneously.
   Random timeouts ensure one node usually times out first
   and wins the election before others start.
```

### Red Flags

```
❌ "Consensus guarantees immediate consistency"
   → Wrong - consensus can be slow during elections

❌ "All nodes must agree"
   → Only need majority (quorum)

❌ "The leader is a single point of failure"
   → Leader can be re-elected if it fails

❌ Confusing consensus with 2PC
   → Different problems, different solutions
```

## Summary

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            KEY TAKEAWAYS                                     │
│                                                                              │
│  1. CONSENSUS PROBLEM                                                       │
│     └── Getting distributed nodes to agree on shared state                  │
│     └── Hard because of failures, delays, partitions                        │
│                                                                              │
│  2. PAXOS                                                                   │
│     └── Original consensus algorithm                                        │
│     └── Theoretically elegant but hard to understand                        │
│     └── Used in Google systems                                              │
│                                                                              │
│  3. RAFT                                                                    │
│     └── Designed for understandability                                      │
│     └── Leader-based: one leader per term                                   │
│     └── Three sub-problems: election, replication, safety                   │
│     └── Used in etcd, Consul, CockroachDB                                   │
│                                                                              │
│  4. KEY CONCEPTS                                                            │
│     └── Quorum: majority must agree                                         │
│     └── Terms: logical time periods                                         │
│     └── Log: ordered sequence of commands                                   │
│     └── Commit: entry replicated to majority                                │
│                                                                              │
│  5. FOR INTERVIEWS                                                          │
│     └── Understand WHY consensus is hard                                    │
│     └── Know Raft at high level                                             │
│     └── Know where it's used                                                │
│     └── Understand quorum requirements                                      │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Resources

- **Raft Visualization**: https://raft.github.io/ (amazing interactive demo)
- **Raft Paper**: "In Search of an Understandable Consensus Algorithm"
- **etcd Documentation**: Real-world Raft implementation

---

**Next:** [Leader Election](./03_leader_election.md) - Practical patterns for electing leaders
