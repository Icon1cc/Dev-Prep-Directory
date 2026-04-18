# Leader Election

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                           LEADER ELECTION                                     ║
║                  Choosing One Node to Coordinate Others                       ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

## Why Leader Election?

Many distributed systems benefit from having a single leader (or master) that coordinates operations:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    WHY HAVE A LEADER?                                        │
│                                                                              │
│  BENEFITS:                                                                   │
│  ├── Simplifies coordination (one decision maker)                           │
│  ├── Avoids conflicts in concurrent operations                              │
│  ├── Enables sequential ordering of operations                              │
│  ├── Reduces complexity of consensus on every operation                     │
│  └── Easier to reason about system behavior                                 │
│                                                                              │
│  WITHOUT LEADER (peer-to-peer):                                             │
│  ├── Every node must coordinate with every other node                       │
│  ├── Conflict resolution is complex                                         │
│  └── Higher message complexity O(n²)                                        │
│                                                                              │
│  WITH LEADER:                                                                │
│  ├── Nodes only talk to leader                                              │
│  ├── Leader makes decisions                                                 │
│  └── Lower message complexity O(n)                                          │
│                                                                              │
│  USE CASES:                                                                  │
│  ├── Database primary selection                                             │
│  ├── Kafka partition leaders                                                │
│  ├── Redis Sentinel master election                                         │
│  ├── Kubernetes control plane (etcd leader)                                │
│  └── Distributed lock services                                              │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## The Split-Brain Problem

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      THE SPLIT-BRAIN NIGHTMARE                               │
│                                                                              │
│  SCENARIO: Network partition creates two "leaders"                          │
│                                                                              │
│     Before Partition:                                                        │
│     ┌─────────────────────────────────────────┐                             │
│     │  Leader A ◄────────────────► Followers  │                             │
│     │    (B, C, D, E)                         │                             │
│     └─────────────────────────────────────────┘                             │
│                                                                              │
│     After Partition:                                                         │
│     ┌───────────────┐     ║     ┌───────────────┐                          │
│     │  "Leader" A   │     ║     │  "Leader" C   │                          │
│     │  Followers: B │     ║     │  Followers:   │                          │
│     │               │     ║     │  D, E         │                          │
│     └───────────────┘     ║     └───────────────┘                          │
│                           ║                                                  │
│                      Network                                                 │
│                      Partition                                               │
│                                                                              │
│  PROBLEM:                                                                    │
│  ├── Both sides think they're the leader                                    │
│  ├── Both accept writes                                                     │
│  ├── When partition heals: DATA CONFLICT!                                   │
│  └── Which writes win? Data loss possible!                                  │
│                                                                              │
│  SOLUTION: Quorum-based leader election                                     │
│  └── Only side with majority can have leader                               │
│  └── Minority side knows it can't elect leader                             │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Leader Election Approaches

### 1. Bully Algorithm

The simplest approach - highest ID wins:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        BULLY ALGORITHM                                       │
│                                                                              │
│  RULE: Node with highest ID becomes leader                                  │
│                                                                              │
│  When a node detects leader is down:                                        │
│                                                                              │
│  Node 2 detects leader (5) is down                                          │
│      │                                                                       │
│      ├──── "ELECTION" to higher IDs (3, 4) ──────►                         │
│      │                                                                       │
│  Node 3 receives election message                                           │
│      │                                                                       │
│      ├──── "OK" to Node 2 (I'm higher, I'll take over)                     │
│      │                                                                       │
│      ├──── "ELECTION" to Node 4 ──────►                                    │
│      │                                                                       │
│  Node 4 receives election message                                           │
│      │                                                                       │
│      ├──── "OK" to Node 3                                                  │
│      │                                                                       │
│      ├──── No higher nodes to contact                                      │
│      │                                                                       │
│      └──── "COORDINATOR" to all (I am the new leader!)                     │
│                                                                              │
│  Result: Node 4 (highest alive) becomes leader                              │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

```python
class BullyNode:
    """
    Bully algorithm implementation
    """

    def __init__(self, node_id, all_nodes):
        self.node_id = node_id
        self.all_nodes = all_nodes  # {id: node}
        self.leader_id = max(all_nodes.keys())  # Initially highest is leader
        self.is_election_in_progress = False

    def detect_leader_failure(self):
        """Called when leader heartbeat times out"""
        if self.node_id == self.leader_id:
            return  # I am the leader

        # Check if leader is actually down
        if not self._ping(self.leader_id):
            self.start_election()

    def start_election(self):
        """Initiate election process"""
        if self.is_election_in_progress:
            return

        self.is_election_in_progress = True
        print(f"Node {self.node_id}: Starting election")

        # Send ELECTION to all higher-ID nodes
        higher_nodes = [nid for nid in self.all_nodes if nid > self.node_id]

        if not higher_nodes:
            # I am the highest - become leader
            self.declare_victory()
            return

        # Ask higher nodes to take over
        got_ok = False
        for higher_id in higher_nodes:
            response = self._send_election(higher_id)
            if response == "OK":
                got_ok = True

        if not got_ok:
            # No higher node responded - I become leader
            self.declare_victory()
        else:
            # Wait for COORDINATOR message from winner
            # Higher node will run its own election
            pass

        self.is_election_in_progress = False

    def receive_election(self, from_node):
        """Handle incoming ELECTION message"""
        if from_node < self.node_id:
            # I'm higher - respond OK and start my own election
            self._send_ok(from_node)
            self.start_election()
            return "OK"
        return None

    def declare_victory(self):
        """Announce self as new leader"""
        self.leader_id = self.node_id
        print(f"Node {self.node_id}: I am the new leader!")

        # Notify all other nodes
        for node_id, node in self.all_nodes.items():
            if node_id != self.node_id:
                node.receive_coordinator(self.node_id)

    def receive_coordinator(self, new_leader_id):
        """Handle COORDINATOR message"""
        self.leader_id = new_leader_id
        self.is_election_in_progress = False
        print(f"Node {self.node_id}: Accepted {new_leader_id} as leader")
```

### 2. Ring Algorithm

Nodes arranged in logical ring, election message travels around:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         RING ALGORITHM                                       │
│                                                                              │
│              ┌───────────────────────────────────┐                          │
│              │                                   │                          │
│              │    ┌─────┐          ┌─────┐      │                          │
│              │    │  1  │ ◄─────── │  5  │      │                          │
│              │    └──┬──┘          └──▲──┘      │                          │
│              │       │                │         │                          │
│              │       │                │         │                          │
│              │       ▼                │         │                          │
│              │    ┌─────┐          ┌─────┐      │                          │
│              │    │  2  │ ──────── │  4  │      │                          │
│              │    └──┬──┘          └──▲──┘      │                          │
│              │       │                │         │                          │
│              │       │    ┌─────┐    │         │                          │
│              │       └──► │  3  │ ───┘         │                          │
│              │            └─────┘              │                          │
│              │                                   │                          │
│              └───────────────────────────────────┘                          │
│                                                                              │
│  PROCESS:                                                                    │
│  1. Node 2 detects leader is down                                           │
│  2. Node 2 sends [2] to next node (3)                                       │
│  3. Node 3 appends ID: [2, 3], forwards to 4                               │
│  4. Node 4 appends ID: [2, 3, 4], forwards to 5                            │
│  5. Node 5 appends ID: [2, 3, 4, 5], forwards to 1                         │
│  6. Node 1 appends ID: [2, 3, 4, 5, 1], forwards to 2                      │
│  7. Node 2 sees own ID - election complete                                  │
│  8. Highest in list (5) becomes leader                                      │
│  9. Node 2 sends COORDINATOR message around ring                            │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 3. Raft-based Election (Production Standard)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    RAFT LEADER ELECTION                                      │
│                                                                              │
│  KEY CONCEPTS:                                                              │
│  ├── Terms (logical time periods)                                           │
│  ├── Randomized timeouts                                                    │
│  ├── Majority vote requirement                                              │
│  └── One vote per node per term                                             │
│                                                                              │
│  PROCESS:                                                                    │
│  1. Follower doesn't hear from leader (timeout)                             │
│  2. Becomes candidate, increments term                                      │
│  3. Votes for self, requests votes from others                              │
│  4. If majority votes: becomes leader                                       │
│  5. If loses: returns to follower                                           │
│                                                                              │
│  WHY IT WORKS:                                                              │
│  ├── Random timeouts prevent simultaneous elections                         │
│  ├── Majority requirement prevents split-brain                              │
│  ├── Term numbers resolve stale leaders                                     │
│  └── Log up-to-date check ensures consistency                              │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 4. ZooKeeper-based Election

Many systems use ZooKeeper/etcd for leader election:

```python
import kazoo
from kazoo.client import KazooClient
from kazoo.recipe.election import Election

class ZooKeeperLeaderElection:
    """
    Leader election using ZooKeeper
    """

    def __init__(self, zk_hosts, election_path, node_id):
        self.zk = KazooClient(hosts=zk_hosts)
        self.zk.start()

        self.election_path = election_path
        self.node_id = node_id
        self.is_leader = False

    def run_for_leader(self, on_elected, on_demoted):
        """
        Participate in leader election
        """
        election = Election(self.zk, self.election_path, self.node_id)

        def leader_func():
            """Called when this node becomes leader"""
            self.is_leader = True
            print(f"Node {self.node_id}: I am now the leader!")
            on_elected()

            # Block while leader - ZK watches handle demotion
            while self.is_leader:
                time.sleep(1)

        # This blocks until we become leader
        # When leader fails, next in line gets notified
        election.run(leader_func)

    def resign(self):
        """Voluntarily give up leadership"""
        self.is_leader = False


class ZooKeeperLeaderElectionManual:
    """
    Manual implementation using ephemeral sequential nodes
    """

    def __init__(self, zk_hosts, election_path, node_id):
        self.zk = KazooClient(hosts=zk_hosts)
        self.zk.start()
        self.election_path = election_path
        self.node_id = node_id
        self.my_node = None

    def run_for_leader(self):
        """
        Create ephemeral sequential node and check if we're leader
        """
        # Ensure election path exists
        self.zk.ensure_path(self.election_path)

        # Create ephemeral sequential node
        # Ephemeral = deleted when session ends (node dies)
        # Sequential = ZK appends sequence number
        self.my_node = self.zk.create(
            f"{self.election_path}/node_",
            value=self.node_id.encode(),
            ephemeral=True,
            sequence=True
        )

        self._check_leadership()

    def _check_leadership(self):
        """
        Check if we're the leader (lowest sequence number)
        """
        children = self.zk.get_children(self.election_path)
        children.sort()  # Sort by sequence number

        my_seq = self.my_node.split("_")[-1]
        lowest_seq = children[0].split("_")[-1]

        if my_seq == lowest_seq:
            print(f"Node {self.node_id}: I am the leader!")
            return True
        else:
            # Watch the node just before us
            # When it's deleted, we might become leader
            my_index = children.index(f"node_{my_seq}")
            watch_node = children[my_index - 1]

            @self.zk.DataWatch(f"{self.election_path}/{watch_node}")
            def watch_predecessor(data, stat):
                if stat is None:  # Node was deleted
                    self._check_leadership()

            print(f"Node {self.node_id}: Watching {watch_node}")
            return False
```

```java
// Java implementation with Curator (ZooKeeper client library)
public class CuratorLeaderElection {
    private final CuratorFramework client;
    private final LeaderSelector leaderSelector;
    private final String nodeId;

    public CuratorLeaderElection(String zkHosts, String path, String nodeId) {
        this.nodeId = nodeId;

        client = CuratorFrameworkFactory.newClient(
            zkHosts,
            new ExponentialBackoffRetry(1000, 3)
        );
        client.start();

        leaderSelector = new LeaderSelector(client, path, new LeaderSelectorListener() {
            @Override
            public void takeLeadership(CuratorFramework client) throws Exception {
                System.out.println(nodeId + ": I am now the leader!");

                // Do leader work here
                // Method returns when leadership is relinquished
                doLeaderWork();
            }

            @Override
            public void stateChanged(CuratorFramework client, ConnectionState state) {
                if (state == ConnectionState.SUSPENDED || state == ConnectionState.LOST) {
                    // Lost ZK connection - must assume not leader
                    System.out.println(nodeId + ": Lost ZK connection, assuming not leader");
                }
            }
        });

        // Auto-requeue for leadership when released
        leaderSelector.autoRequeue();
    }

    public void start() {
        leaderSelector.start();
    }

    public void stop() {
        leaderSelector.close();
        client.close();
    }
}
```

## Leader Election with Leases

Leases provide time-bounded leadership, preventing indefinite leadership during network issues:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     LEASE-BASED LEADERSHIP                                   │
│                                                                              │
│  CONCEPT:                                                                    │
│  ├── Leader holds a "lease" (lock with timeout)                            │
│  ├── Lease must be renewed periodically                                     │
│  ├── If not renewed, leadership expires                                     │
│  └── Other nodes can acquire after expiry                                   │
│                                                                              │
│  Timeline:                                                                   │
│  ═════════                                                                   │
│                                                                              │
│  Leader A:                                                                   │
│  ├── Acquires lease at T=0 (valid for 30s)                                 │
│  ├── Renews at T=20 (valid until T=50)                                     │
│  ├── Renews at T=40 (valid until T=70)                                     │
│  ├── Network partition at T=45                                              │
│  ├── Cannot renew - lease expires at T=70                                  │
│  └── Loses leadership                                                       │
│                                                                              │
│  Other nodes:                                                                │
│  └── After T=70, can compete for lease                                      │
│                                                                              │
│  SAFETY:                                                                     │
│  ├── Leader must stop acting BEFORE lease expires                          │
│  ├── Add safety margin: stop at T=65 if lease expires at T=70              │
│  └── Prevents "zombie leader" problem                                       │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

```python
import time
import threading
from datetime import datetime, timedelta

class LeaseBasedLeader:
    """
    Leader election using time-based leases
    """

    def __init__(self, node_id, lease_store, lease_duration_sec=30):
        self.node_id = node_id
        self.lease_store = lease_store  # Redis, etcd, etc.
        self.lease_duration = lease_duration_sec
        self.safety_margin = lease_duration_sec * 0.2  # 20% safety margin

        self.is_leader = False
        self.lease_expiry = None
        self.renewal_thread = None
        self.stop_flag = threading.Event()

    def try_acquire_leadership(self):
        """
        Try to become leader by acquiring lease
        """
        # Try to set lease with our node_id (only if not exists or expired)
        acquired = self.lease_store.set_if_not_exists(
            key="leader_lease",
            value=self.node_id,
            ttl_seconds=self.lease_duration
        )

        if acquired:
            self.is_leader = True
            self.lease_expiry = datetime.now() + timedelta(seconds=self.lease_duration)
            self._start_renewal_thread()
            print(f"Node {self.node_id}: Acquired leadership")
            return True

        # Check if we already hold the lease
        current_leader = self.lease_store.get("leader_lease")
        if current_leader == self.node_id:
            self.is_leader = True
            self._renew_lease()
            return True

        return False

    def _start_renewal_thread(self):
        """Start background thread to renew lease"""
        self.stop_flag.clear()
        self.renewal_thread = threading.Thread(target=self._renewal_loop)
        self.renewal_thread.start()

    def _renewal_loop(self):
        """Periodically renew lease"""
        renewal_interval = self.lease_duration / 3  # Renew at 1/3 of lease time

        while not self.stop_flag.is_set():
            time.sleep(renewal_interval)

            if not self._renew_lease():
                # Failed to renew - lost leadership
                self._handle_leadership_loss()
                break

    def _renew_lease(self):
        """Extend the lease"""
        try:
            success = self.lease_store.extend_if_owner(
                key="leader_lease",
                expected_value=self.node_id,
                ttl_seconds=self.lease_duration
            )

            if success:
                self.lease_expiry = datetime.now() + timedelta(seconds=self.lease_duration)
                return True
            else:
                return False
        except Exception as e:
            print(f"Failed to renew lease: {e}")
            return False

    def _handle_leadership_loss(self):
        """Called when leadership is lost"""
        self.is_leader = False
        self.lease_expiry = None
        print(f"Node {self.node_id}: Lost leadership")

    def is_safe_to_act_as_leader(self):
        """
        Check if it's safe to perform leader actions
        Includes safety margin before lease expiry
        """
        if not self.is_leader or self.lease_expiry is None:
            return False

        # Add safety margin
        safe_until = self.lease_expiry - timedelta(seconds=self.safety_margin)
        return datetime.now() < safe_until

    def resign(self):
        """Voluntarily give up leadership"""
        self.stop_flag.set()
        if self.renewal_thread:
            self.renewal_thread.join()

        self.lease_store.delete_if_owner(
            key="leader_lease",
            expected_value=self.node_id
        )
        self.is_leader = False
        self.lease_expiry = None
```

## Fencing Tokens

Prevent stale leaders from making changes after losing leadership:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        FENCING TOKENS                                        │
│                                                                              │
│  PROBLEM:                                                                    │
│  ═════════                                                                   │
│  Leader A gets lease, then gets stuck in GC pause                          │
│  Lease expires, Leader B takes over                                         │
│  Leader A wakes up, thinks it's still leader                               │
│  Both A and B write to storage - CORRUPTION!                                │
│                                                                              │
│  Timeline:                                                                   │
│  T=0:   A gets lease (token=33)                                             │
│  T=10:  A starts long GC pause                                              │
│  T=30:  A's lease expires                                                   │
│  T=32:  B gets lease (token=34)                                             │
│  T=35:  B writes to storage with token=34                                   │
│  T=40:  A wakes up, tries to write with token=33                           │
│  T=40:  Storage REJECTS write (33 < 34)  ← SAVED!                          │
│                                                                              │
│  SOLUTION:                                                                   │
│  ═════════                                                                   │
│  Each leadership acquisition gets monotonically increasing token            │
│  Storage only accepts writes with latest token                              │
│                                                                              │
│  ┌────────────┐         ┌────────────┐         ┌────────────┐              │
│  │  Leader A  │         │  Leader B  │         │  Storage   │              │
│  │  token=33  │         │  token=34  │         │  last=34   │              │
│  └─────┬──────┘         └─────┬──────┘         └─────┬──────┘              │
│        │                      │                      │                      │
│        │     write(token=34)  │                      │                      │
│        │                      ├─────────────────────►│                      │
│        │                      │◄────────OK───────────│                      │
│        │                      │                      │                      │
│        │     write(token=33)                         │                      │
│        ├────────────────────────────────────────────►│                      │
│        │◄────────REJECTED (33 < 34)──────────────────│                      │
│        │                                             │                      │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

```python
class FencedStorage:
    """
    Storage that uses fencing tokens to prevent stale writes
    """

    def __init__(self):
        self.data = {}
        self.fencing_tokens = {}  # key -> last_token

    def write(self, key, value, fencing_token):
        """
        Write only if fencing token is >= last seen token
        """
        last_token = self.fencing_tokens.get(key, 0)

        if fencing_token < last_token:
            raise StaleLeaderError(
                f"Rejected: token {fencing_token} < last token {last_token}"
            )

        self.data[key] = value
        self.fencing_tokens[key] = fencing_token
        return True

    def read(self, key):
        return self.data.get(key)


class LeaderWithFencing:
    """
    Leader that uses fencing tokens for all writes
    """

    def __init__(self, node_id, lease_store, storage):
        self.node_id = node_id
        self.lease_store = lease_store
        self.storage = storage
        self.fencing_token = None

    def acquire_leadership(self):
        # Get monotonically increasing fencing token with lease
        result = self.lease_store.acquire_with_token(
            key="leader_lease",
            value=self.node_id
        )

        if result:
            self.fencing_token = result['token']
            return True
        return False

    def write_data(self, key, value):
        """All writes must include fencing token"""
        if self.fencing_token is None:
            raise NotLeaderError("Not the leader")

        try:
            self.storage.write(key, value, self.fencing_token)
        except StaleLeaderError:
            # We're a stale leader - stop immediately
            self.fencing_token = None
            raise
```

## Comparison of Approaches

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                  LEADER ELECTION COMPARISON                                  │
│                                                                              │
│  Approach       │ Complexity │ Split-brain │ Dependencies │ Use Case        │
│  ═══════════════╪════════════╪═════════════╪══════════════╪═════════════════│
│  Bully          │ Low        │ Possible    │ None         │ Simple systems  │
│  Ring           │ Medium     │ Possible    │ None         │ Token rings     │
│  Raft           │ High       │ Prevented   │ None         │ Consensus       │
│  ZooKeeper      │ Medium     │ Prevented   │ ZK cluster   │ Most common     │
│  Lease-based    │ Medium     │ Time-based  │ Lease store  │ Simpler setups  │
│                                                                              │
│  RECOMMENDATION:                                                            │
│  ├── Production systems: ZooKeeper/etcd-based                              │
│  ├── New distributed DB: Implement Raft                                    │
│  ├── Simple coordination: Lease-based with fencing                         │
│  └── Learning: Start with Bully, then Raft                                 │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Interview Tips

### Common Questions

**Q: How do you prevent split-brain in leader election?**
```
A: Use quorum-based election:
   - Only majority partition can elect leader
   - This prevents multiple leaders
   - Minority partition knows it can't have leader

   Additional safety with fencing tokens:
   - Each leader gets monotonic token
   - Storage rejects writes with old tokens
```

**Q: What's the difference between ZooKeeper election and Raft?**
```
A: Implementation level:
   - Raft: Algorithm for consensus (implement yourself)
   - ZooKeeper: Service that provides leader election (use as client)

   When to use:
   - Building distributed database: Implement Raft
   - Application needs coordination: Use ZooKeeper/etcd
```

**Q: How do you handle the "zombie leader" problem?**
```
A: Multiple layers:
   1. Lease-based leadership with strict expiry
   2. Safety margin: stop acting before lease expires
   3. Fencing tokens: storage rejects stale leader writes
   4. Epoch numbers: similar to fencing tokens
```

### Red Flags

```
❌ "Just pick the node with highest ID"
   → Doesn't handle network partitions

❌ Not considering split-brain
   → Shows lack of distributed systems understanding

❌ "Leader election is simple"
   → Famous last words in distributed systems

❌ Forgetting about network partitions
   → The main challenge in leader election
```

## Summary

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          KEY TAKEAWAYS                                       │
│                                                                              │
│  1. WHY LEADERS                                                             │
│     └── Simplify coordination in distributed systems                        │
│     └── Reduce message complexity                                           │
│     └── Enable sequential ordering                                          │
│                                                                              │
│  2. THE HARD PART                                                           │
│     └── Preventing split-brain during network partitions                    │
│     └── Handling leader failures gracefully                                 │
│     └── Detecting stale leaders                                             │
│                                                                              │
│  3. SOLUTIONS                                                               │
│     └── Quorum: majority must agree                                         │
│     └── Leases: time-bounded leadership                                     │
│     └── Fencing tokens: reject stale writes                                 │
│                                                                              │
│  4. PRACTICAL CHOICE                                                        │
│     └── Use ZooKeeper/etcd for most applications                           │
│     └── Implement Raft for databases/consensus systems                      │
│     └── Always include fencing for safety                                   │
│                                                                              │
│  5. INTERVIEW FOCUS                                                         │
│     └── Understand split-brain problem                                      │
│     └── Know quorum requirements                                            │
│     └── Discuss failure scenarios                                           │
│     └── Mention fencing tokens                                              │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

**Next:** [Time and Ordering](./04_time_ordering.md) - How distributed systems handle time
