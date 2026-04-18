# Circular Linked List - Complete Reference Guide

## Table of Contents

1. [Create and Traverse](#create-and-traverse-circular-linked-list) - [Code: 01. Create and traverse through a simple circular linked list.py](./01.%20Create%20and%20traverse%20through%20a%20simple%20circular%20linked%20list.py)
2. [Insert at Beginning](#insert-at-beginning) - [Code: 02. Insert at the beginning of circular linked list.py](./02.%20Insert%20at%20the%20beginning%20of%20circular%20linked%20list.py)
3. [Insert at End](#insert-at-end) - [Code: 03. Insert at the end of circular linked list.py](./03.%20Insert%20at%20the%20end%20of%20circular%20linked%20list.py)
4. [Delete Head](#delete-head-of-circular-linked-list) - [Code: 04. Delete head of circular linked list.py](./04.%20Delete%20head%20of%20circular%20linked%20list.py)
5. [Delete K-th Node](#delete-k-th-node) - [Code: 05. Delete kth node of circular linked list.py](./05.%20Delete%20kth%20node%20of%20circular%20linked%20list.py)

---

## Understanding Circular Linked Lists

### What is a Circular Linked List?

A **Circular Linked List** is a variation of linked list where the last node points back to the first node, creating a circle. There is no `None` at the end.

### Visual Representation

```
Regular Linked List:
  head → [10] → [20] → [30] → None

Circular Linked List:
  head → [10] → [20] → [30] ─┐
          ↑                   │
          └───────────────────┘
```

### Node Structure
```python
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None  # Points to next node (or back to head)
```

### Key Characteristics

| Feature | Regular Linked List | Circular Linked List |
|---------|---------------------|----------------------|
| Last node points to | `None` | First node (head) |
| Traversal ends when | `current.next == None` | `current.next == head` |
| Can reach head from any node | No | Yes |
| Natural loop structure | No | Yes |

### Advantages of Circular Linked List

1. **Any node can be starting point**: Useful for round-robin scheduling
2. **Efficient for queue implementations**: No need to maintain separate head and tail
3. **Continuous traversal**: Can traverse the entire list from any node
4. **No null checks at end**: Every node has a valid next pointer

### Disadvantages

1. **More complex operations**: Need to handle circular nature
2. **Infinite loop risk**: Easy to create infinite loops if not careful
3. **Harder to detect end**: Must track starting point to know when traversal is complete

---

## Create and Traverse Circular Linked List
**📁 Implementation:** [01. Create and traverse through a simple circular linked list.py](./01.%20Create%20and%20traverse%20through%20a%20simple%20circular%20linked%20list.py)

### Problem
Create a circular linked list and traverse through all nodes.

### Implementation

```python
class CircularLinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)

        if not self.head:
            # First node: point to itself
            self.head = new_node
            self.head.next = self.head
        else:
            # Traverse to last node
            temp = self.head
            while temp.next != self.head:
                temp = temp.next

            # Insert at end
            temp.next = new_node
            new_node.next = self.head
```

### Traversal Logic

```python
def display(self):
    if self.head:
        temp = self.head
        while True:
            print(temp.data, end=" → ")
            temp = temp.next
            if temp == self.head:  # Back to start
                break
        print("(HEAD)")
```

### Visual Example

```
Creating list: [A, B, C, D]

Step 1: Add A
  head → [A] ─┐
         ↑    │
         └────┘

Step 2: Add B
  head → [A] → [B] ─┐
          ↑         │
          └─────────┘

Step 3: Add C
  head → [A] → [B] → [C] ─┐
          ↑               │
          └───────────────┘

Step 4: Add D
  head → [A] → [B] → [C] → [D] ─┐
          ↑                     │
          └─────────────────────┘
```

### Time Complexity

| Operation | Time | Notes |
|-----------|------|-------|
| Append | O(n) | Must traverse to find last node |
| Display | O(n) | Visit each node once |

### Space Complexity
- **O(1)** - Only uses temporary pointer variables

---

## Insert at Beginning
**📁 Implementation:** [02. Insert at the beginning of circular linked list.py](./02.%20Insert%20at%20the%20beginning%20of%20circular%20linked%20list.py)

### Problem
Insert a new node at the beginning of a circular linked list.

### Challenge
Unlike regular linked list, we need to update the **tail's next pointer** to point to the new head.

### Approach 1: With Tail Pointer (O(1))

```python
class CircularLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def insert_at_beginning(self, key):
        new_node = Node(key)

        if self.head is None:
            self.head = new_node
            self.tail = new_node
            new_node.next = self.head
        else:
            new_node.next = self.head  # New node points to current head
            self.tail.next = new_node  # Tail now points to new node
            self.head = new_node       # Update head
```

### Approach 2: Without Tail Pointer (O(n))

```python
def insert_at_beginning(head, key):
    new_node = Node(key)

    if head is None:
        new_node.next = new_node
        return new_node

    # Find the tail (node whose next is head)
    current = head
    while current.next != head:
        current = current.next

    # Insert at beginning
    new_node.next = head
    current.next = new_node

    return new_node  # New head
```

### Visual Example

```
Before: head → [10] → [20] → [30] ─┐
                ↑                   │
                └───────────────────┘

Insert 5 at beginning:

Step 1: Create new node [5]
Step 2: [5].next = head ([10])
Step 3: Find tail ([30]), set tail.next = [5]
Step 4: Update head to [5]

After:  head → [5] → [10] → [20] → [30] ─┐
                ↑                         │
                └─────────────────────────┘
```

### Time Complexity

| Approach | Time | Space |
|----------|------|-------|
| With tail pointer | O(1) | O(1) |
| Without tail pointer | O(n) | O(1) |

### Why Maintain Tail Pointer?
Maintaining a tail pointer makes insertion at both beginning and end **O(1)** operations.

---

## Insert at End
**📁 Implementation:** [03. Insert at the end of circular linked list.py](./03.%20Insert%20at%20the%20end%20of%20circular%20linked%20list.py)

### Problem
Insert a new node at the end of a circular linked list.

### Implementation

```python
def insert_at_end(head, key):
    new_node = Node(key)

    if head is None:
        new_node.next = new_node
        return new_node

    # Traverse to last node
    current = head
    while current.next != head:
        current = current.next

    # Insert at end
    current.next = new_node
    new_node.next = head

    return head  # Head unchanged
```

### With Tail Pointer (O(1))

```python
def insert_at_end(self, key):
    new_node = Node(key)

    if self.head is None:
        self.head = new_node
        self.tail = new_node
        new_node.next = self.head
    else:
        self.tail.next = new_node  # Old tail points to new node
        self.tail = new_node       # Update tail
        self.tail.next = self.head # New tail points to head
```

### Visual Example

```
Before: head → [10] → [20] → [30] ─┐
                ↑                   │
                └───────────────────┘

Insert 40 at end:

Step 1: Traverse to last node (30)
Step 2: [30].next = new_node ([40])
Step 3: [40].next = head ([10])

After:  head → [10] → [20] → [30] → [40] ─┐
                ↑                          │
                └──────────────────────────┘
```

### Time Complexity

| Approach | Time | Space |
|----------|------|-------|
| Without tail pointer | O(n) | O(1) |
| With tail pointer | O(1) | O(1) |

---

## Delete Head of Circular Linked List
**📁 Implementation:** [04. Delete head of circular linked list.py](./04.%20Delete%20head%20of%20circular%20linked%20list.py)

### Problem
Delete the first node (head) of a circular linked list.

### Implementation

```python
def delete_head(head):
    # Case 1: Empty list
    if head is None:
        return None

    # Case 2: Only one node
    if head.next == head:
        return None

    # Case 3: Multiple nodes
    # Find the tail
    current = head
    while current.next != head:
        current = current.next

    # Update tail's next to skip old head
    current.next = head.next

    # Return new head
    return head.next
```

### Visual Example

```
Before: head → [10] → [20] → [30] ─┐
                ↑                   │
                └───────────────────┘

Delete head (10):

Step 1: Find tail (30)
Step 2: tail.next = head.next ([20])
Step 3: Return new head ([20])

After:  head → [20] → [30] ─┐
                ↑           │
                └───────────┘
```

### Edge Cases

| Case | Before | After |
|------|--------|-------|
| Empty list | `None` | `None` |
| Single node | `[10]→(self)` | `None` |
| Multiple nodes | `[10]→[20]→[30]→...` | `[20]→[30]→...` |

### Time Complexity
- **O(n)** - Must traverse to find tail
- **O(1)** with tail pointer

---

## Delete K-th Node
**📁 Implementation:** [05. Delete kth node of circular linked list.py](./05.%20Delete%20kth%20node%20of%20circular%20linked%20list.py)

### Problem
Delete the k-th node (1-indexed) from a circular linked list.

### Implementation

```python
def delete_kth_node(head, k):
    # Case 1: Empty list
    if head is None:
        return None

    # Case 2: Single node
    if head.next == head:
        return None

    # Case 3: Delete head (k == 1)
    if k == 1:
        # Find tail
        current = head
        while current.next != head:
            current = current.next

        # Update tail and head
        current.next = head.next
        return head.next

    # Case 4: Delete k-th node (k > 1)
    current = head
    # Traverse to (k-1)th node
    for _ in range(k - 2):
        current = current.next

    # Skip the k-th node
    current.next = current.next.next

    return head
```

### Visual Example

```
Before: head → [10] → [20] → [30] → [40] → [50] ─┐
                ↑                                 │
                └─────────────────────────────────┘

Delete 3rd node (30):

Step 1: Traverse to 2nd node (20)
Step 2: [20].next = [20].next.next ([40])

After:  head → [10] → [20] → [40] → [50] ─┐
                ↑                          │
                └──────────────────────────┘
```

### Time Complexity
- **O(n)** worst case - may need to traverse entire list
- **O(k)** for k-th node specifically

### Space Complexity
- **O(1)** - Only uses temporary pointers

---

## Comparison Summary

### Time Complexity Table

| Operation | Without Tail | With Tail |
|-----------|--------------|-----------|
| Insert at Beginning | O(n) | O(1) |
| Insert at End | O(n) | O(1) |
| Delete Head | O(n) | O(1) |
| Delete K-th Node | O(k) | O(k) |
| Traverse | O(n) | O(n) |
| Search | O(n) | O(n) |

### Key Implementation Patterns

#### Pattern 1: Finding the Tail
```python
current = head
while current.next != head:
    current = current.next
# Now current is the tail
```

#### Pattern 2: Traversal with Termination
```python
if head:
    temp = head
    while True:
        # Process temp.data
        temp = temp.next
        if temp == head:
            break
```

#### Pattern 3: Empty List Check
```python
if head is None:
    return None

# Single node check
if head.next == head:
    # Only one node
```

---

## Applications of Circular Linked List

### 1. Round-Robin Scheduling
CPU scheduling where each process gets equal time slice in circular order.

```python
def round_robin(processes, time_quantum):
    current = head
    while processes_remaining:
        execute(current.data, time_quantum)
        current = current.next  # Move to next process
```

### 2. Circular Buffer
Fixed-size buffer that wraps around.

### 3. Music Playlist (Loop Mode)
When the last song ends, start from the first song.

### 4. Multiplayer Games
Turn-based games where players take turns in circular order.

### 5. Josephus Problem
Classic problem of eliminating every k-th person in a circle.

```python
def josephus(n, k):
    # Create circular list of n people
    # Repeatedly delete every k-th person
    # Return the survivor
```

---

## Circular vs Regular Linked List

| Aspect | Regular | Circular |
|--------|---------|----------|
| Last node points to | `None` | Head |
| End detection | `node == None` | `node == head` |
| Reach any node from any node | Need to restart | Always possible |
| Traversal | Has natural end | Must track start |
| Insert at end (no tail) | O(n) | O(n) |
| Implementation complexity | Simpler | Slightly more complex |
| Risk of infinite loop | Lower | Higher |

---

## Common Mistakes to Avoid

### 1. Infinite Loop in Traversal
```python
# ❌ Wrong - infinite loop
while current:
    current = current.next

# ✅ Correct
while True:
    current = current.next
    if current == head:
        break
```

### 2. Forgetting to Update Tail's Next
```python
# ❌ Wrong - breaks circular structure
new_node.next = head
head = new_node
# Tail still points to old head!

# ✅ Correct
new_node.next = head
tail.next = new_node  # Update tail's next
head = new_node
```

### 3. Not Handling Single Node Case
```python
# ❌ Wrong
def delete_head(head):
    tail.next = head.next
    return head.next  # Fails if only one node

# ✅ Correct
def delete_head(head):
    if head.next == head:  # Single node
        return None
    # ... rest of logic
```

---

## Edge Cases to Test

1. **Empty list**: `head = None`
2. **Single node**: `head.next == head`
3. **Two nodes**: Minimal circular structure
4. **K > list length**: Handle invalid k
5. **K = 1**: Deleting head
6. **K = length**: Deleting tail

---

## Interview Tips

### Common Questions
1. Detect if a linked list is circular
2. Find the length of a circular linked list
3. Split a circular list into two halves
4. Check if a linked list has a cycle (Floyd's algorithm)

### Key Points to Remember
- Always track the starting point for traversal termination
- Maintain tail pointer for O(1) operations
- Handle empty and single-node cases explicitly
- Be careful with pointer updates to maintain circular structure

---
