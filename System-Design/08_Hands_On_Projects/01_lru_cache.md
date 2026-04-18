# Project 1: LRU Cache

Build a Least Recently Used (LRU) cache from scratch.

## Problem Description

```
┌────────────────────────────────────────────────────────────────┐
│                      LRU CACHE                                  │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Design a cache with fixed capacity that:                      │
│  • get(key): Return value if exists, else -1                   │
│  • put(key, value): Insert or update key-value pair            │
│  • When cache is full, evict LEAST RECENTLY USED item          │
│                                                                 │
│  All operations must be O(1) time complexity!                  │
│                                                                 │
│  Example:                                                       │
│  cache = LRUCache(2)  # capacity = 2                           │
│  cache.put(1, 1)      # cache: {1=1}                           │
│  cache.put(2, 2)      # cache: {1=1, 2=2}                      │
│  cache.get(1)         # returns 1, cache: {2=2, 1=1}          │
│  cache.put(3, 3)      # evicts key 2, cache: {1=1, 3=3}       │
│  cache.get(2)         # returns -1 (not found)                 │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

## Design Discussion

### Why This Data Structure?

```
REQUIREMENTS:
• O(1) lookup by key → Need HashMap
• O(1) insertion/deletion → Need LinkedList
• Track recency order → Need ordered structure

SOLUTION: HashMap + Doubly Linked List

┌─────────────────────────────────────────────────────────────────┐
│                                                                  │
│  HashMap: key → Node                                            │
│  ┌─────┬─────┬─────┐                                           │
│  │ k1  │ k2  │ k3  │ ─────► O(1) lookup                        │
│  └──┬──┴──┬──┴──┬──┘                                           │
│     │     │     │                                               │
│     ▼     ▼     ▼                                               │
│  ┌─────────────────────────────────────┐                       │
│  │ HEAD ↔ Node1 ↔ Node2 ↔ Node3 ↔ TAIL │ ─► O(1) add/remove   │
│  └─────────────────────────────────────┘                       │
│     ▲                               ▲                           │
│     │                               │                           │
│   Most                            Least                         │
│   Recent                          Recent                        │
│                                   (evict this)                  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Solution: Python

```python
class Node:
    """Doubly linked list node."""
    def __init__(self, key: int = 0, value: int = 0):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}  # key -> Node

        # Dummy head and tail for easier list operations
        self.head = Node()  # Most recently used
        self.tail = Node()  # Least recently used
        self.head.next = self.tail
        self.tail.prev = self.head

    def get(self, key: int) -> int:
        """Get value by key. Returns -1 if not found."""
        if key not in self.cache:
            return -1

        # Move to front (most recently used)
        node = self.cache[key]
        self._remove(node)
        self._add_to_front(node)

        return node.value

    def put(self, key: int, value: int) -> None:
        """Insert or update key-value pair."""
        if key in self.cache:
            # Update existing node
            node = self.cache[key]
            node.value = value
            self._remove(node)
            self._add_to_front(node)
        else:
            # Create new node
            node = Node(key, value)
            self.cache[key] = node
            self._add_to_front(node)

            # Evict if over capacity
            if len(self.cache) > self.capacity:
                lru = self.tail.prev
                self._remove(lru)
                del self.cache[lru.key]

    def _remove(self, node: Node) -> None:
        """Remove node from linked list."""
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_to_front(self, node: Node) -> None:
        """Add node right after head."""
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node


# Test the implementation
if __name__ == "__main__":
    cache = LRUCache(2)

    cache.put(1, 1)
    cache.put(2, 2)
    print(cache.get(1))       # Output: 1

    cache.put(3, 3)           # Evicts key 2
    print(cache.get(2))       # Output: -1 (not found)

    cache.put(4, 4)           # Evicts key 1
    print(cache.get(1))       # Output: -1 (not found)
    print(cache.get(3))       # Output: 3
    print(cache.get(4))       # Output: 4

    print("All tests passed!")
```

---

## Solution: Java

```java
import java.util.HashMap;
import java.util.Map;

class LRUCache {

    class Node {
        int key;
        int value;
        Node prev;
        Node next;

        Node(int key, int value) {
            this.key = key;
            this.value = value;
        }
    }

    private int capacity;
    private Map<Integer, Node> cache;
    private Node head;
    private Node tail;

    public LRUCache(int capacity) {
        this.capacity = capacity;
        this.cache = new HashMap<>();

        // Dummy head and tail
        head = new Node(0, 0);
        tail = new Node(0, 0);
        head.next = tail;
        tail.prev = head;
    }

    public int get(int key) {
        if (!cache.containsKey(key)) {
            return -1;
        }

        Node node = cache.get(key);
        remove(node);
        addToFront(node);

        return node.value;
    }

    public void put(int key, int value) {
        if (cache.containsKey(key)) {
            Node node = cache.get(key);
            node.value = value;
            remove(node);
            addToFront(node);
        } else {
            Node node = new Node(key, value);
            cache.put(key, node);
            addToFront(node);

            if (cache.size() > capacity) {
                Node lru = tail.prev;
                remove(lru);
                cache.remove(lru.key);
            }
        }
    }

    private void remove(Node node) {
        node.prev.next = node.next;
        node.next.prev = node.prev;
    }

    private void addToFront(Node node) {
        node.next = head.next;
        node.prev = head;
        head.next.prev = node;
        head.next = node;
    }

    public static void main(String[] args) {
        LRUCache cache = new LRUCache(2);

        cache.put(1, 1);
        cache.put(2, 2);
        System.out.println(cache.get(1));  // 1

        cache.put(3, 3);                    // Evicts 2
        System.out.println(cache.get(2));  // -1

        cache.put(4, 4);                    // Evicts 1
        System.out.println(cache.get(1));  // -1
        System.out.println(cache.get(3));  // 3
        System.out.println(cache.get(4));  // 4

        System.out.println("All tests passed!");
    }
}
```

---

## How to Run

### Python
```bash
python lru_cache.py
```

### Java
```bash
javac LRUCache.java
java LRUCache
```

---

## Extensions

Try implementing these variations:

### 1. TTL (Time-To-Live)
```
Add expiration time for each entry.
get() returns -1 if entry has expired.
```

### 2. Thread-Safe LRU
```
Make the cache safe for concurrent access.
Hint: Use locks or ConcurrentHashMap.
```

### 3. LRU with Different Eviction
```
Implement LFU (Least Frequently Used) cache.
Track access count instead of recency.
```

---

## Interview Tips

When asked about LRU cache in interviews:

```
1. CLARIFY: Single-threaded or multi-threaded?
2. STATE: Need O(1) for both get and put
3. EXPLAIN: Why HashMap + Doubly Linked List
4. CODE: Start with the data structure
5. TEST: Walk through an example
```

---

*Next: [Rate Limiter](02_rate_limiter.md) →*
