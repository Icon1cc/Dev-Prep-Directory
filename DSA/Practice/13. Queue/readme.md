# Queue - Complete Reference Guide

## Table of Contents

1. [Basic Queue Operations](#basic-queue-operations) - [Code: 01. Basic operations using queue.py](./01.%20Basic%20operations%20using%20queue.py)
2. [Queue in Python](#queue-in-python) - [Code: 02. Queue in Python.py](./02.%20Queue%20in%20Python.py)
3. [Queue Using List](#queue-using-list) - [Code: 03. Queue using list.py](./03.%20Queue%20using%20list.py)
4. [Queue Using Deque](#queue-using-deque) - [Code: 04. Queue using Deque.py](./04.%20Queue%20using%20Deque.py)
5. [Linked List Implementation](#linked-list-implementation-of-queue) - [Code: 05. Linked List implementation of queue.py](./05.%20Linked%20List%20implementation%20of%20queue.py)
6. [Circular Queue](#circular-queue-implementation) - [Code: 06. Queue implementation using circular list.py](./06.%20Queue%20implementation%20using%20circular%20list.py)
7. [Stack Using Queue](#implement-stack-using-queue) - [Code: 07. Implement stack using queue.py](./07.%20Implement%20stack%20using%20queue.py)

---

## Understanding Queues

### What is a Queue?

A **Queue** is a linear data structure that follows the **FIFO** (First In, First Out) principle. The first element added is the first one to be removed, like a line of people waiting.

### Visual Representation

```
Enqueue (Add) →  ┌───┬───┬───┬───┐  → Dequeue (Remove)
                 │ D │ C │ B │ A │
                 └───┴───┴───┴───┘
                Rear            Front

A was added first, A will be removed first.
```

### Core Operations

| Operation | Description | Time Complexity |
|-----------|-------------|-----------------|
| **Enqueue** | Add element to rear | O(1) |
| **Dequeue** | Remove element from front | O(1)* |
| **Front/Peek** | View front element | O(1) |
| **Rear** | View rear element | O(1) |
| **isEmpty** | Check if queue is empty | O(1) |
| **Size** | Return number of elements | O(1) |

*O(1) with proper implementation (deque or linked list)

### Queue vs Stack

| Feature | Queue (FIFO) | Stack (LIFO) |
|---------|--------------|--------------|
| Insert at | Rear | Top |
| Remove from | Front | Top |
| Order | First In, First Out | Last In, First Out |
| Use case | Scheduling, BFS | Function calls, DFS |

### Real-World Analogies

1. **Bank line**: First customer served first
2. **Printer queue**: First document printed first
3. **Call center**: Calls answered in order received
4. **Traffic at intersection**: First car goes first

---

## Basic Queue Operations
**📁 Implementation:** [01. Basic operations using queue.py](./01.%20Basic%20operations%20using%20queue.py)

### Core Operations

```python
from collections import deque

class Queue:
    def __init__(self):
        self.queue = deque()

    def enqueue(self, item):
        """Add element to rear"""
        self.queue.append(item)

    def dequeue(self):
        """Remove and return front element"""
        if not self.is_empty():
            return self.queue.popleft()
        raise IndexError("Dequeue from empty queue")

    def get_front(self):
        """View front element without removing"""
        if not self.is_empty():
            return self.queue[0]
        return None

    def get_rear(self):
        """View rear element without removing"""
        if not self.is_empty():
            return self.queue[-1]
        return None

    def is_empty(self):
        """Check if queue is empty"""
        return len(self.queue) == 0

    def size(self):
        """Return number of elements"""
        return len(self.queue)

    def display(self):
        """Show all elements"""
        return list(self.queue)
```

### Usage Example

```python
q = Queue()
q.enqueue(10)
q.enqueue(20)
q.enqueue(30)

print(q.display())      # [10, 20, 30]
print(q.get_front())    # 10
print(q.get_rear())     # 30
print(q.dequeue())      # 10
print(q.display())      # [20, 30]
```

---

## Queue in Python
**📁 Implementation:** [02. Queue in Python.py](./02.%20Queue%20in%20Python.py)

### Built-in Options

Python provides several ways to implement queues:

#### 1. collections.deque (Recommended)
```python
from collections import deque

queue = deque()
queue.append(1)      # Enqueue
queue.append(2)
queue.append(3)
front = queue.popleft()  # Dequeue: 1
```

#### 2. queue.Queue (Thread-Safe)
```python
from queue import Queue

q = Queue()
q.put(1)             # Enqueue
q.put(2)
front = q.get()      # Dequeue: 1
```

#### 3. List (Not Recommended for Large Queues)
```python
queue = []
queue.append(1)      # Enqueue: O(1)
front = queue.pop(0) # Dequeue: O(n) - Inefficient!
```

### Comparison

| Method | Enqueue | Dequeue | Thread-Safe | Use Case |
|--------|---------|---------|-------------|----------|
| deque | O(1) | O(1) | No | General use |
| Queue | O(1) | O(1) | Yes | Multi-threaded |
| List | O(1)* | O(n) | No | Avoid for queues |

*Amortized O(1)

---

## Queue Using List
**📁 Implementation:** [03. Queue using list.py](./03.%20Queue%20using%20list.py)

### Implementation

```python
class ListQueue:
    def __init__(self):
        self.queue = []

    def enqueue(self, item):
        """O(1) amortized - append to end"""
        self.queue.append(item)

    def dequeue(self):
        """O(n) - remove from front requires shifting"""
        if not self.is_empty():
            return self.queue.pop(0)
        raise IndexError("Dequeue from empty queue")

    def get_front(self):
        return self.queue[0] if self.queue else None

    def get_rear(self):
        return self.queue[-1] if self.queue else None

    def is_empty(self):
        return len(self.queue) == 0

    def size(self):
        return len(self.queue)
```

### Why O(n) for Dequeue?

When removing from index 0, all elements must shift:

```
Before pop(0): [A, B, C, D, E]
                ↓
After pop(0):  [B, C, D, E]
               ← All elements shift left

This shifting takes O(n) time.
```

### When to Use
- Simple implementation needed
- Small queues
- Infrequent dequeue operations

### When to Avoid
- Large queues
- Frequent dequeue operations
- Performance-critical applications

---

## Queue Using Deque
**📁 Implementation:** [04. Queue using Deque.py](./04.%20Queue%20using%20Deque.py)

### Implementation

```python
from collections import deque

class DequeQueue:
    def __init__(self):
        self.queue = deque()

    def enqueue(self, item):
        """O(1) - append to right"""
        self.queue.append(item)

    def dequeue(self):
        """O(1) - remove from left"""
        if not self.is_empty():
            return self.queue.popleft()
        raise IndexError("Dequeue from empty queue")

    def get_front(self):
        return self.queue[0] if self.queue else None

    def get_rear(self):
        return self.queue[-1] if self.queue else None

    def is_empty(self):
        return len(self.queue) == 0

    def size(self):
        return len(self.queue)
```

### Why deque is Better

`deque` is implemented as a doubly-linked list of blocks:

```
deque internal structure:
[Block 1] ⟷ [Block 2] ⟷ [Block 3]
   ↓            ↓           ↓
[items]     [items]     [items]

O(1) operations at both ends!
```

### deque Methods

| Method | Operation | Time |
|--------|-----------|------|
| `append(x)` | Add to right | O(1) |
| `appendleft(x)` | Add to left | O(1) |
| `pop()` | Remove from right | O(1) |
| `popleft()` | Remove from left | O(1) |
| `rotate(n)` | Rotate n steps | O(n) |

### Best Practice
**Always use `deque` for queue implementations** unless you need thread-safety.

---

## Linked List Implementation of Queue
**📁 Implementation:** [05. Linked List implementation of queue.py](./05.%20Linked%20List%20implementation%20of%20queue.py)

### Implementation

```python
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedListQueue:
    def __init__(self):
        self.front = None
        self.rear = None
        self._size = 0

    def enqueue(self, item):
        """Add to rear - O(1)"""
        new_node = Node(item)

        if self.is_empty():
            self.front = new_node
            self.rear = new_node
        else:
            self.rear.next = new_node
            self.rear = new_node

        self._size += 1

    def dequeue(self):
        """Remove from front - O(1)"""
        if self.is_empty():
            raise IndexError("Dequeue from empty queue")

        data = self.front.data
        self.front = self.front.next

        # Queue became empty
        if self.front is None:
            self.rear = None

        self._size -= 1
        return data

    def get_front(self):
        return self.front.data if self.front else None

    def get_rear(self):
        return self.rear.data if self.rear else None

    def is_empty(self):
        return self.front is None

    def size(self):
        return self._size
```

### Visual Representation

```
Enqueue A, B, C:

Step 1: Enqueue A
front → [A|None] ← rear

Step 2: Enqueue B
front → [A|•] → [B|None] ← rear

Step 3: Enqueue C
front → [A|•] → [B|•] → [C|None] ← rear

Dequeue:
front → [B|•] → [C|None] ← rear
(A removed)
```

### Advantages
- True O(1) for both enqueue and dequeue
- No resizing needed
- Dynamic size

### Disadvantages
- Extra memory for pointers
- No random access
- Poor cache locality

---

## Circular Queue Implementation
**📁 Implementation:** [06. Queue implementation using circular list.py](./06.%20Queue%20implementation%20using%20circular%20list.py)

### What is a Circular Queue?

A **Circular Queue** (Ring Buffer) is a fixed-size queue where the end wraps around to the beginning, efficiently using space.

### Visual Representation

```
Linear view of circular queue (size 5):
┌───┬───┬───┬───┬───┐
│ A │ B │ C │   │   │
└───┴───┴───┴───┴───┘
  ↑           ↑
front        rear

After more operations (wrapping):
┌───┬───┬───┬───┬───┐
│ F │   │   │ D │ E │
└───┴───┴───┴───┴───┘
      ↑       ↑
    rear    front

Circular view:
      [0]
    ↙     ↘
  [4]       [1]
    ↖     ↗
  [3] ← [2]
```

### Implementation

```python
class CircularQueue:
    def __init__(self, capacity):
        self.capacity = capacity
        self.queue = [None] * capacity
        self.front = 0
        self.rear = -1
        self._size = 0

    def enqueue(self, item):
        """Add to rear with wraparound"""
        if self.is_full():
            raise OverflowError("Queue is full")

        self.rear = (self.rear + 1) % self.capacity
        self.queue[self.rear] = item
        self._size += 1

    def dequeue(self):
        """Remove from front with wraparound"""
        if self.is_empty():
            raise IndexError("Queue is empty")

        data = self.queue[self.front]
        self.queue[self.front] = None
        self.front = (self.front + 1) % self.capacity
        self._size -= 1
        return data

    def get_front(self):
        return self.queue[self.front] if not self.is_empty() else None

    def get_rear(self):
        return self.queue[self.rear] if not self.is_empty() else None

    def is_empty(self):
        return self._size == 0

    def is_full(self):
        return self._size == self.capacity

    def size(self):
        return self._size
```

### Key Formula

```python
# Next position with wraparound
next_index = (current_index + 1) % capacity

# Example: capacity = 5
# Position 4 + 1 = 5 % 5 = 0 (wraps to start)
```

### Advantages
- Fixed memory usage
- O(1) operations
- Efficient space utilization
- No memory allocation during operations

### Use Cases
- Buffering (audio, video)
- Producer-consumer problems
- CPU scheduling
- Traffic systems

---

## Implement Stack Using Queue
**📁 Implementation:** [07. Implement stack using queue.py](./07.%20Implement%20stack%20using%20queue.py)

### Problem
Implement LIFO (Stack) behavior using FIFO (Queue) operations.

### Approach: Costly Push

Make push O(n), pop O(1).

```python
from collections import deque

class StackUsingQueue:
    def __init__(self):
        self.queue = deque()

    def push(self, x):
        """O(n) - Rotate to put new element at front"""
        size = len(self.queue)
        self.queue.append(x)

        # Rotate: move all previous elements to back
        for _ in range(size):
            self.queue.append(self.queue.popleft())

    def pop(self):
        """O(1) - Front is always the top"""
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self.queue.popleft()

    def top(self):
        """O(1) - View front"""
        if self.is_empty():
            return None
        return self.queue[0]

    def is_empty(self):
        return len(self.queue) == 0
```

### How Push Works

```
Queue before push(30): [20, 10]  (20 is at front = top of stack)

Push 30:
1. Append 30: [20, 10, 30]
2. Rotate 2 elements:
   - Move 20 to back: [10, 30, 20]
   - Move 10 to back: [30, 20, 10]

Queue after: [30, 20, 10]  (30 is at front = new top)
```

### Alternative: Costly Pop

Make push O(1), pop O(n).

```python
def push(self, x):
    """O(1)"""
    self.queue.append(x)

def pop(self):
    """O(n) - Move n-1 elements, then pop"""
    size = len(self.queue)
    for _ in range(size - 1):
        self.queue.append(self.queue.popleft())
    return self.queue.popleft()
```

### Comparison

| Approach | Push | Pop | When to Use |
|----------|------|-----|-------------|
| Costly Push | O(n) | O(1) | Frequent pops |
| Costly Pop | O(1) | O(n) | Frequent pushes |

---

## Comparison Summary

### Implementation Comparison

| Implementation | Enqueue | Dequeue | Space | Best For |
|----------------|---------|---------|-------|----------|
| List | O(1)* | O(n) | Dynamic | Simple, small queues |
| Deque | O(1) | O(1) | Dynamic | General use |
| Linked List | O(1) | O(1) | Dynamic | Guaranteed O(1) |
| Circular Array | O(1) | O(1) | Fixed | Fixed-size buffers |

*Amortized

### Time Complexity Table

| Operation | List | Deque | Linked List | Circular |
|-----------|------|-------|-------------|----------|
| Enqueue | O(1)* | O(1) | O(1) | O(1) |
| Dequeue | O(n) | O(1) | O(1) | O(1) |
| Front | O(1) | O(1) | O(1) | O(1) |
| Rear | O(1) | O(1) | O(1) | O(1) |
| isEmpty | O(1) | O(1) | O(1) | O(1) |

---

## Applications of Queue

### 1. BFS (Breadth-First Search)

```python
from collections import deque

def bfs(graph, start):
    visited = set()
    queue = deque([start])
    visited.add(start)

    while queue:
        node = queue.popleft()
        print(node, end=' ')

        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
```

### 2. Task Scheduling

```python
class TaskScheduler:
    def __init__(self):
        self.tasks = deque()

    def add_task(self, task):
        self.tasks.append(task)

    def process_next(self):
        if self.tasks:
            return self.tasks.popleft()
        return None
```

### 3. Print Queue

```python
class PrintQueue:
    def __init__(self):
        self.queue = deque()

    def add_document(self, doc):
        self.queue.append(doc)
        print(f"Added: {doc}")

    def print_next(self):
        if self.queue:
            doc = self.queue.popleft()
            print(f"Printing: {doc}")
            return doc
        print("Queue empty")
```

### 4. Producer-Consumer

```python
from queue import Queue
import threading

def producer(q, items):
    for item in items:
        q.put(item)
        print(f"Produced: {item}")

def consumer(q):
    while True:
        item = q.get()
        print(f"Consumed: {item}")
        q.task_done()
```

---

## Queue Variants

### 1. Priority Queue

Elements dequeued based on priority, not order.

```python
import heapq

class PriorityQueue:
    def __init__(self):
        self.heap = []

    def enqueue(self, priority, item):
        heapq.heappush(self.heap, (priority, item))

    def dequeue(self):
        return heapq.heappop(self.heap)[1]
```

### 2. Double-Ended Queue (Deque)

Insert/remove from both ends.

```python
from collections import deque

d = deque()
d.append(1)       # Add to right
d.appendleft(0)   # Add to left
d.pop()           # Remove from right
d.popleft()       # Remove from left
```

### 3. Blocking Queue

Waits if empty (useful for multi-threading).

```python
from queue import Queue

q = Queue()
q.put(item)           # Add
item = q.get()        # Blocks until item available
item = q.get(timeout=5)  # Wait max 5 seconds
```

---

## Common Patterns

### Pattern 1: Level Order Traversal

```python
def level_order(root):
    if not root:
        return []

    result = []
    queue = deque([root])

    while queue:
        level_size = len(queue)
        level = []

        for _ in range(level_size):
            node = queue.popleft()
            level.append(node.val)

            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        result.append(level)

    return result
```

### Pattern 2: Sliding Window Maximum

```python
def max_sliding_window(nums, k):
    result = []
    dq = deque()  # Store indices

    for i, num in enumerate(nums):
        # Remove indices out of window
        while dq and dq[0] < i - k + 1:
            dq.popleft()

        # Remove smaller elements
        while dq and nums[dq[-1]] < num:
            dq.pop()

        dq.append(i)

        if i >= k - 1:
            result.append(nums[dq[0]])

    return result
```

---

## Edge Cases to Test

1. **Empty queue**: Dequeue/front on empty
2. **Single element**: Enqueue one, dequeue one
3. **Full queue**: Circular queue overflow
4. **Wraparound**: Circular queue indices
5. **Interleaved operations**: Mix of enqueue/dequeue
6. **Same elements**: Queue with duplicates

---

## Interview Tips

### Common Questions
1. Implement queue using stacks
2. Implement stack using queues
3. Design circular queue
4. First non-repeating character in stream
5. Sliding window maximum
6. Rotting oranges (BFS)
7. Number of islands (BFS)

### Key Points
- FIFO principle
- Use deque for O(1) operations
- Know when to use queue vs stack
- Circular queue for fixed-size buffers
- BFS uses queue, DFS uses stack

---
