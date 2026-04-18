# Project 4: Consistent Hashing

Build a consistent hashing ring for distributed systems.

## Problem Description

```
┌────────────────────────────────────────────────────────────────┐
│                   CONSISTENT HASHING                            │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Problem with simple hashing:                                  │
│  • hash(key) % N servers                                       │
│  • When N changes, MOST keys remap to different servers!       │
│  • Adding 1 server: ~100% cache invalidation                   │
│                                                                 │
│  Consistent hashing solution:                                  │
│  • Arrange servers on a ring (0 to 2^32)                       │
│  • Hash keys to positions on ring                              │
│  • Key goes to next server clockwise                           │
│  • Adding 1 server: Only ~1/N keys remap                       │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

## Visualization

```
         CONSISTENT HASHING RING

              0 (= 2^32)
                 │
            ┌────┴────┐
           ╱          ╲
         ╱     S1      ╲
        │   (pos 50)    │
        │               │    ← Key "user_123" (hash=120)
   S4   │               │       goes to S2 (next clockwise)
(pos 300)               S2
        │            (pos 150)
        │               │
         ╲             ╱
          ╲    S3    ╱
           ╲(pos 220)╱
            └───────┘

  When S2 is removed:
  - Only keys between S1 and S2 move to S3
  - Other keys stay on their servers
```

## Python Implementation

```python
import hashlib
from bisect import bisect_right
from typing import Optional, List

class ConsistentHash:
    """
    Consistent hashing implementation with virtual nodes.
    """

    def __init__(self, nodes: List[str] = None, virtual_nodes: int = 100):
        """
        Args:
            nodes: Initial list of server names
            virtual_nodes: Number of virtual nodes per server
        """
        self.virtual_nodes = virtual_nodes
        self.ring = {}           # hash_value -> node_name
        self.sorted_keys = []    # Sorted list of hash values

        if nodes:
            for node in nodes:
                self.add_node(node)

    def _hash(self, key: str) -> int:
        """Generate hash value for a key."""
        return int(hashlib.md5(key.encode()).hexdigest(), 16)

    def add_node(self, node: str) -> None:
        """Add a server node to the ring."""
        for i in range(self.virtual_nodes):
            virtual_key = f"{node}:{i}"
            hash_value = self._hash(virtual_key)
            self.ring[hash_value] = node
            self.sorted_keys.append(hash_value)

        self.sorted_keys.sort()

    def remove_node(self, node: str) -> None:
        """Remove a server node from the ring."""
        for i in range(self.virtual_nodes):
            virtual_key = f"{node}:{i}"
            hash_value = self._hash(virtual_key)

            if hash_value in self.ring:
                del self.ring[hash_value]
                self.sorted_keys.remove(hash_value)

    def get_node(self, key: str) -> Optional[str]:
        """Get the server node responsible for a key."""
        if not self.ring:
            return None

        hash_value = self._hash(key)

        # Find first node with hash >= key's hash
        idx = bisect_right(self.sorted_keys, hash_value)

        # Wrap around to first node if past the end
        if idx == len(self.sorted_keys):
            idx = 0

        return self.ring[self.sorted_keys[idx]]

    def get_nodes_for_key(self, key: str, count: int = 3) -> List[str]:
        """Get multiple nodes for replication."""
        if not self.ring:
            return []

        hash_value = self._hash(key)
        idx = bisect_right(self.sorted_keys, hash_value)

        nodes = []
        seen = set()

        for _ in range(len(self.sorted_keys)):
            if idx >= len(self.sorted_keys):
                idx = 0

            node = self.ring[self.sorted_keys[idx]]
            if node not in seen:
                nodes.append(node)
                seen.add(node)

                if len(nodes) >= count:
                    break

            idx += 1

        return nodes


def demonstrate_consistency():
    """Show how consistent hashing minimizes remapping."""
    print("=== Demonstrating Consistent Hashing ===\n")

    # Create ring with 3 servers
    ch = ConsistentHash(['server1', 'server2', 'server3'], virtual_nodes=100)

    # Map some keys
    keys = [f"user_{i}" for i in range(10)]

    print("Initial mapping (3 servers):")
    initial_mapping = {}
    for key in keys:
        node = ch.get_node(key)
        initial_mapping[key] = node
        print(f"  {key} -> {node}")

    # Add a server
    print("\n--- Adding server4 ---\n")
    ch.add_node('server4')

    print("After adding server4:")
    remapped = 0
    for key in keys:
        node = ch.get_node(key)
        changed = " (CHANGED)" if node != initial_mapping[key] else ""
        if changed:
            remapped += 1
        print(f"  {key} -> {node}{changed}")

    print(f"\nKeys remapped: {remapped}/{len(keys)} ({remapped/len(keys)*100:.1f}%)")
    print(f"Expected: ~{100/4:.1f}% (1/N where N=4 servers)")

    # Remove a server
    print("\n--- Removing server2 ---\n")
    ch.remove_node('server2')

    print("After removing server2:")
    for key in keys:
        node = ch.get_node(key)
        print(f"  {key} -> {node}")


def demonstrate_replication():
    """Show how to get multiple nodes for replication."""
    print("\n=== Demonstrating Replication ===\n")

    ch = ConsistentHash(['server1', 'server2', 'server3', 'server4'], virtual_nodes=100)

    key = "important_data"
    nodes = ch.get_nodes_for_key(key, count=3)

    print(f"Key '{key}' should be replicated to:")
    for i, node in enumerate(nodes, 1):
        print(f"  {i}. {node}")


if __name__ == "__main__":
    demonstrate_consistency()
    demonstrate_replication()
```

---

## Java Implementation

```java
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.*;

public class ConsistentHash {

    private final int virtualNodes;
    private final SortedMap<Long, String> ring = new TreeMap<>();

    public ConsistentHash(List<String> nodes, int virtualNodes) {
        this.virtualNodes = virtualNodes;
        for (String node : nodes) {
            addNode(node);
        }
    }

    private long hash(String key) {
        try {
            MessageDigest md = MessageDigest.getInstance("MD5");
            byte[] digest = md.digest(key.getBytes());
            long hash = 0;
            for (int i = 0; i < 8; i++) {
                hash = (hash << 8) | (digest[i] & 0xFF);
            }
            return hash;
        } catch (NoSuchAlgorithmException e) {
            throw new RuntimeException(e);
        }
    }

    public void addNode(String node) {
        for (int i = 0; i < virtualNodes; i++) {
            String virtualKey = node + ":" + i;
            ring.put(hash(virtualKey), node);
        }
    }

    public void removeNode(String node) {
        for (int i = 0; i < virtualNodes; i++) {
            String virtualKey = node + ":" + i;
            ring.remove(hash(virtualKey));
        }
    }

    public String getNode(String key) {
        if (ring.isEmpty()) {
            return null;
        }

        long hashValue = hash(key);
        SortedMap<Long, String> tailMap = ring.tailMap(hashValue);

        Long nodeHash = tailMap.isEmpty() ? ring.firstKey() : tailMap.firstKey();
        return ring.get(nodeHash);
    }

    public static void main(String[] args) {
        List<String> nodes = Arrays.asList("server1", "server2", "server3");
        ConsistentHash ch = new ConsistentHash(nodes, 100);

        System.out.println("Initial mapping:");
        for (int i = 0; i < 10; i++) {
            String key = "user_" + i;
            System.out.println("  " + key + " -> " + ch.getNode(key));
        }

        System.out.println("\nAdding server4...");
        ch.addNode("server4");

        System.out.println("\nAfter adding server4:");
        for (int i = 0; i < 10; i++) {
            String key = "user_" + i;
            System.out.println("  " + key + " -> " + ch.getNode(key));
        }
    }
}
```

---

## Key Concepts

### Virtual Nodes

```
WHY VIRTUAL NODES?

Without virtual nodes (3 servers):
┌────────────────────────────────────────────────────────────────┐
│                                                                 │
│  Ring with uneven distribution:                                │
│                                                                 │
│       S1                                                        │
│        ●──────────────────────●                                │
│                               S2                                │
│                    Large gap!                                   │
│        ●──────────────────────●                                │
│       S3                                                        │
│                                                                 │
│  Result: Unbalanced load                                       │
│                                                                 │
└────────────────────────────────────────────────────────────────┘

With virtual nodes (3 servers × 100 virtual each):
┌────────────────────────────────────────────────────────────────┐
│                                                                 │
│  Ring with many points per server:                             │
│                                                                 │
│  S1.0 S3.5 S2.3 S1.7 S3.2 S2.9 S1.4 ...                       │
│    ●    ●    ●    ●    ●    ●    ●                             │
│                                                                 │
│  Result: Even distribution!                                    │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

### Comparison: Simple vs Consistent Hashing

| Aspect | Simple (% N) | Consistent |
|--------|--------------|------------|
| Add server | ~100% keys move | ~1/N keys move |
| Remove server | ~100% keys move | ~1/N keys move |
| Load balance | Even (with good hash) | Even (with virtual nodes) |
| Complexity | O(1) | O(log N) |

---

## Extensions

### 1. Weighted Nodes
```python
def add_node_weighted(self, node: str, weight: int) -> None:
    """Add node with custom weight (more virtual nodes = more keys)."""
    virtual_count = self.virtual_nodes * weight
    for i in range(virtual_count):
        virtual_key = f"{node}:{i}"
        hash_value = self._hash(virtual_key)
        self.ring[hash_value] = node
        self.sorted_keys.append(hash_value)
    self.sorted_keys.sort()
```

### 2. Bounded Load
```python
def get_node_bounded(self, key: str, load_factor: float = 1.25) -> str:
    """Get node considering current load (avoid hot spots)."""
    # Implementation would track current load per node
    # and skip overloaded nodes
    pass
```

---

*Next: [Load Balancer](05_load_balancer.md) →*
