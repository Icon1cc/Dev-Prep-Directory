# Doubly Linked List - Complete Reference Guide

## Table of Contents

1. [Creation of Doubly Linked List](#creation-of-doubly-linked-list) - [Code: 01. Creation of 3 node doubly linked list.py](./01.%20Creation%20of%203%20node%20doubly%20linked%20list.py)
2. [Insert at Beginning](#insert-at-beginning) - [Code: 02. Insert at the beginning of DLL.py](./02.%20Insert%20at%20the%20beginning%20of%20DLL.py)
3. [Insert at End](#insert-at-end) - [Code: 03. Insert at the end of DLL.py](./03.%20Insert%20at%20the%20end%20of%20DLL.py)
4. [Delete Head](#delete-head) - [Code: 04. Delete the head of DLL.py](./04.%20Delete%20the%20head%20of%20DLL.py)
5. [Delete Last Node](#delete-last-node) - [Code: 05. Delete the last node of DLL.py](./05.%20Delete%20the%20last%20node%20of%20DLL.py)
6. [Reverse DLL](#reverse-a-doubly-linked-list) - [Code: 06. Reverse a DLL.py](./06.%20Reverse%20a%20DLL.py)

---

## Understanding Doubly Linked Lists

### What is a Doubly Linked List?

A **Doubly Linked List (DLL)** is a linked list where each node contains:
- **Data**: The value stored
- **Next pointer**: Reference to the next node
- **Previous pointer**: Reference to the previous node

### Node Structure
```python
class Node:
    def __init__(self, data):
        self.data = data
        self.prev = None  # Pointer to previous node
        self.next = None  # Pointer to next node
```

### Visual Representation
```
     ┌─────────────────────────────────────┐
     │                                     │
None ← [10] ⟷ [20] ⟷ [30] ⟷ [40] → None
                                     │
                                     └─────┘
       head                          tail

Each node:
┌──────┬──────┬──────┐
│ prev │ data │ next │
└──────┴──────┴──────┘
```

### Comparison: Singly vs Doubly Linked List

| Feature | Singly Linked List | Doubly Linked List |
|---------|-------------------|-------------------|
| Pointers per node | 1 (next) | 2 (prev, next) |
| Traversal | Forward only | Forward and backward |
| Memory per node | Less | More (extra pointer) |
| Delete with pointer | Copy trick needed | Direct deletion |
| Insert before node | O(n) | O(1) |
| Reverse traversal | Not possible | O(n) |
| Implementation | Simpler | More complex |

### Advantages of Doubly Linked List

1. **Bidirectional traversal**: Can move both forward and backward
2. **Easier deletion**: Can delete a node with only its pointer
3. **Insert before**: Easy to insert before a given node
4. **Reverse operations**: Natural support for reverse traversal

### Disadvantages

1. **Extra memory**: Each node needs two pointers
2. **Complex operations**: More pointers to update
3. **More error-prone**: Easy to mess up bidirectional links

---

## Creation of Doubly Linked List
**📁 Implementation:** [01. Creation of 3 node doubly linked list.py](./01.%20Creation%20of%203%20node%20doubly%20linked%20list.py)

### Problem
Create a doubly linked list with nodes connected bidirectionally.

### Implementation

```python
class Node:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None

# Create nodes
node1 = Node(10)
node2 = Node(20)
node3 = Node(30)

# Connect forward
node1.next = node2
node2.next = node3

# Connect backward
node2.prev = node1
node3.prev = node2
```

### Visual Step-by-Step

```
Step 1: Create nodes
[10]  [20]  [30]  (all disconnected)

Step 2: Connect forward (next pointers)
[10] → [20] → [30]

Step 3: Connect backward (prev pointers)
[10] ⟷ [20] ⟷ [30]

Final:
None ← [10] ⟷ [20] ⟷ [30] → None
```

### Display Functions

```python
def display_forward(head):
    """Traverse using next pointers"""
    temp = head
    while temp:
        print(temp.data, end=" ⟷ ")
        temp = temp.next
    print("None")

def display_backward(tail):
    """Traverse using prev pointers"""
    temp = tail
    while temp:
        print(temp.data, end=" ⟷ ")
        temp = temp.prev
    print("None")
```

### Time Complexity
- **Creation**: O(1) per node
- **Traversal**: O(n)

---

## Insert at Beginning
**📁 Implementation:** [02. Insert at the beginning of DLL.py](./02.%20Insert%20at%20the%20beginning%20of%20DLL.py)

### Problem
Insert a new node at the beginning of a doubly linked list.

### Implementation

```python
def insert_at_beginning(head, data):
    new_node = Node(data)

    # Empty list
    if head is None:
        return new_node

    # Non-empty list
    new_node.next = head    # New node points to current head
    head.prev = new_node    # Current head points back to new node

    return new_node         # New node is the new head
```

### Visual Example

```
Before:
None ← [10] ⟷ [20] ⟷ [30] → None
        ↑
       head

Insert 5 at beginning:

Step 1: Create new_node [5]
Step 2: new_node.next = head
        [5] → [10] ⟷ [20] ⟷ [30]
Step 3: head.prev = new_node
        [5] ⟷ [10] ⟷ [20] ⟷ [30]
Step 4: Return new_node as head

After:
None ← [5] ⟷ [10] ⟷ [20] ⟷ [30] → None
        ↑
       head
```

### Time Complexity
- **O(1)** - Constant time, no traversal needed

### Space Complexity
- **O(1)** - Only creates one new node

---

## Insert at End
**📁 Implementation:** [03. Insert at the end of DLL.py](./03.%20Insert%20at%20the%20end%20of%20DLL.py)

### Problem
Insert a new node at the end of a doubly linked list.

### Implementation

```python
def insert_at_end(head, data):
    new_node = Node(data)

    # Empty list
    if head is None:
        return new_node

    # Traverse to the last node
    current = head
    while current.next is not None:
        current = current.next

    # Link the new node
    current.next = new_node
    new_node.prev = current

    return head
```

### With Tail Pointer (O(1))

```python
class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def insert_at_end(self, data):
        new_node = Node(data)

        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
```

### Visual Example

```
Before:
None ← [10] ⟷ [20] ⟷ [30] → None
                       ↑
                     (last)

Insert 40 at end:

Step 1: Traverse to last node (30)
Step 2: [30].next = new_node
Step 3: new_node.prev = [30]

After:
None ← [10] ⟷ [20] ⟷ [30] ⟷ [40] → None
```

### Time Complexity

| Approach | Time |
|----------|------|
| Without tail pointer | O(n) |
| With tail pointer | O(1) |

---

## Delete Head
**📁 Implementation:** [04. Delete the head of DLL.py](./04.%20Delete%20the%20head%20of%20DLL.py)

### Problem
Delete the first node (head) of a doubly linked list.

### Implementation

```python
def delete_head(head):
    # Empty list
    if head is None:
        return None

    # Single node
    if head.next is None:
        return None

    # Multiple nodes
    new_head = head.next
    new_head.prev = None

    return new_head
```

### Visual Example

```
Before:
None ← [10] ⟷ [20] ⟷ [30] → None
        ↑
       head

Delete head:

Step 1: new_head = head.next ([20])
Step 2: new_head.prev = None

After:
None ← [20] ⟷ [30] → None
        ↑
       head
```

### Time Complexity
- **O(1)** - Direct access to head

### Edge Cases
- Empty list → Return `None`
- Single node → Return `None`
- Multiple nodes → Return second node

---

## Delete Last Node
**📁 Implementation:** [05. Delete the last node of DLL.py](./05.%20Delete%20the%20last%20node%20of%20DLL.py)

### Problem
Delete the last node of a doubly linked list.

### Implementation

```python
def delete_last(head):
    # Empty list
    if head is None:
        return None

    # Single node
    if head.next is None:
        return None

    # Traverse to last node
    current = head
    while current.next is not None:
        current = current.next

    # Update second-last node
    current.prev.next = None

    return head
```

### With Tail Pointer

```python
def delete_last(self):
    if self.tail is None:
        return

    if self.head == self.tail:  # Single node
        self.head = None
        self.tail = None
    else:
        self.tail = self.tail.prev
        self.tail.next = None
```

### Visual Example

```
Before:
None ← [10] ⟷ [20] ⟷ [30] → None
                       ↑
                     (last)

Delete last node:

Step 1: Traverse to last node (30)
Step 2: Access second-last via current.prev (20)
Step 3: Set [20].next = None

After:
None ← [10] ⟷ [20] → None
```

### Time Complexity

| Approach | Time |
|----------|------|
| Without tail pointer | O(n) |
| With tail pointer | O(1) |

---

## Reverse a Doubly Linked List
**📁 Implementation:** [06. Reverse a DLL.py](./06.%20Reverse%20a%20DLL.py)

### Problem
Reverse a doubly linked list so that the last node becomes first.

### Key Insight
For each node, swap its `prev` and `next` pointers.

### Implementation

```python
def reverse(head):
    if head is None:
        return None

    current = head

    while current is not None:
        # Swap prev and next
        current.prev, current.next = current.next, current.prev

        # Track new head (will be last processed node)
        head = current

        # Move to "next" (which is now stored in prev after swap)
        current = current.prev

    return head
```

### Visual Step-by-Step

```
Before:
None ← [10] ⟷ [20] ⟷ [30] → None

Step 1: At node [10]
- Swap: prev=None, next=[20] → prev=[20], next=None
- Move to prev (which was next): [20]

After Step 1:
[10] ← [20] ⟷ [30]
(10's next is now None, prev is [20])

Step 2: At node [20]
- Swap: prev=[10], next=[30] → prev=[30], next=[10]
- Move to prev: [30]

Step 3: At node [30]
- Swap: prev=[20], next=None → prev=None, next=[20]
- Move to prev: None (exit loop)

After:
None ← [30] ⟷ [20] ⟷ [10] → None
        ↑
    new head
```

### Alternative: Using Extra Variable

```python
def reverse(head):
    current = head
    new_head = None

    while current:
        # Save next
        next_node = current.next

        # Reverse pointers
        current.next = current.prev
        current.prev = next_node

        # Track new head
        new_head = current

        # Move to next (saved)
        current = next_node

    return new_head
```

### Time Complexity
- **O(n)** - Visit each node once

### Space Complexity
- **O(1)** - In-place reversal

---

## Comparison Summary

### Time Complexity Table

| Operation | Singly LL | Doubly LL | DLL with Tail |
|-----------|-----------|-----------|---------------|
| Insert at Beginning | O(1) | O(1) | O(1) |
| Insert at End | O(n) | O(n) | O(1) |
| Delete Head | O(1) | O(1) | O(1) |
| Delete Last | O(n) | O(n) | O(1) |
| Delete Given Node | O(n)* | O(1) | O(1) |
| Reverse | O(n) | O(n) | O(n) |
| Traverse Forward | O(n) | O(n) | O(n) |
| Traverse Backward | N/A | O(n) | O(n) |

*Singly LL requires finding previous node

### Space Complexity
- **Per node**: O(1) extra for prev pointer compared to singly LL
- **Total**: O(n) for n nodes

---

## Key Implementation Patterns

### Pattern 1: Empty List Check
```python
if head is None:
    return new_node  # or None for delete
```

### Pattern 2: Single Node Check
```python
if head.next is None:  # Only one node
    # Handle specially
```

### Pattern 3: Linking Two Nodes
```python
# Link node1 → node2
node1.next = node2
node2.prev = node1
```

### Pattern 4: Unlinking a Node
```python
# Remove middle_node
if middle_node.prev:
    middle_node.prev.next = middle_node.next
if middle_node.next:
    middle_node.next.prev = middle_node.prev
```

### Pattern 5: Traversal
```python
# Forward
current = head
while current:
    # process current
    current = current.next

# Backward
current = tail
while current:
    # process current
    current = current.prev
```

---

## Applications of Doubly Linked List

### 1. Browser History
Navigate forward and backward through visited pages.
```python
class BrowserHistory:
    def __init__(self):
        self.current = None

    def visit(self, url):
        new_page = Node(url)
        if self.current:
            new_page.prev = self.current
            self.current.next = new_page
        self.current = new_page

    def back(self):
        if self.current.prev:
            self.current = self.current.prev

    def forward(self):
        if self.current.next:
            self.current = self.current.next
```

### 2. LRU Cache
Least Recently Used cache implementation.
- Most recent at head
- Least recent at tail
- O(1) access and update

### 3. Undo/Redo Functionality
Text editors, drawing applications.

### 4. Music Player
Previous and next track navigation.

### 5. Deck of Cards
Easy to draw from top or bottom.

---

## Common Mistakes to Avoid

### 1. Forgetting to Update Both Pointers
```python
# ❌ Wrong - only updates next
new_node.next = head
head = new_node

# ✅ Correct - updates both
new_node.next = head
head.prev = new_node
head = new_node
```

### 2. Not Handling Prev of New Head
```python
# ❌ Wrong
new_head = head.next
return new_head

# ✅ Correct
new_head = head.next
new_head.prev = None
return new_head
```

### 3. Null Pointer Issues
```python
# ❌ Dangerous
current.prev.next = current.next  # What if prev is None?

# ✅ Safe
if current.prev:
    current.prev.next = current.next
```

---

## Edge Cases to Test

1. **Empty list**: `head = None`
2. **Single node**: `head.next = None, head.prev = None`
3. **Two nodes**: Minimal DLL structure
4. **Operations at head**: Special handling for prev = None
5. **Operations at tail**: Special handling for next = None
6. **Middle operations**: General case

---

## Interview Tips

### Common Questions
1. Implement LRU Cache using DLL + HashMap
2. Flatten a multilevel DLL
3. Convert binary tree to DLL
4. Merge two sorted DLLs
5. Delete all occurrences of a key

### Key Points to Emphasize
- Always update both `prev` and `next` pointers
- Handle edge cases (empty, single node)
- Consider maintaining tail pointer for O(1) end operations
- DLL enables O(1) deletion with just node pointer

---
