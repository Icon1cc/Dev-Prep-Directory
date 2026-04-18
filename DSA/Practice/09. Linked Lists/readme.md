# Linked List - Complete Reference Guide

## Table of Contents
1. [Simple Linked List](#simple-linked-list) - [Code: Simple Linked List.py](./01.%20Simple%20Linked%20List.py)
2. [Traversing a Linked List](#traversing-a-linked-list) - [Code: Traversing a linked list.py](./02.%20Traversing%20a%20linked%20list.py)
3. [Search in Linked List](#search-in-linked-list) - [Code: Search in Linked List.py](./03.%20Search%20in%20Linked%20List.py)
4. [Insert at Beginning](#insert-at-beginning) - [Code: Insert at the beginning of linked list.py](./04.%20Insert%20at%20the%20beginning%20of%20linked%20list.py)
5. [Insert at End](#insert-at-end) - [Code: Insert at the end of linked list.py](./05.%20Insert%20at%20the%20end%20of%20linked%20list.py)
6. [Insert at Given Position](#insert-at-given-position) - [Code: Insert at a given position in singly linked list.py](./06.%20Insert%20at%20a%20given%20position%20in%20singly%20linked%20list.py)
7. [Delete First Node](#delete-first-node) - [Code: Delete first node of linked list.py](./07.%20Delete%20first%20node%20of%20linked%20list.py)
8. [Delete Last Node](#delete-last-node) - [Code: Delete last node of linked list.py](./08.%20Delete%20last%20node%20of%20linked%20list.py)
9. [Delete Node with Pointer Only](#delete-node-with-pointer-only) - [Code: Delete a node with only pointer given to it.py](./09.%20Delete%20a%20node%20with%20only%20pointer%20given%20to%20it.py)
10. [Sorted Insert](#sorted-insert) - [Code: Sorted Insert in a linked list.py](./10.%20Sorted%20Insert%20in%20a%20linked%20list.py)
11. [Insert in Middle](#insert-in-middle) - [Code: Insert a node in the middle of linked list.py](./11.%20Insert%20a%20node%20in%20the%20middle%20of%20linked%20list.py)
12. [N-th Node from End](#nth-node-from-end) - [Code: Find n-th Node from the end of the linked list.py](./12.%20Find%20n-th%20Node%20from%20the%20end%20of%20the%20linked%20list.py)
13. [Remove Duplicates from Sorted](#remove-duplicates-from-sorted) - [Code: Remove duplicates from a sorted linked list.py](./13.%20Remove%20duplicates%20from%20a%20sorted%20linked%20list.py)
14. [Reverse a Linked List](#reverse-a-linked-list) - [Code: Reverse a linked list.py](./14.%20Reverse%20a%20linked%20list.py)
15. [Recursive Reverse (Way 1)](#recursive-reverse-way-1) - [Code: Recursive Reverse a linked list way 1.py](./15.%20Recursive%20Reverse%20a%20linked%20list%20way%201.py)
16. [Recursive Reverse (Way 2)](#recursive-reverse-way-2) - [Code: Recursive Reverse a linked list way 2.py](./16.%20Recursive%20Reverse%20a%20linked%20list%20way%202.py)

---

## Understanding Linked Lists

### What is a Linked List?
A **linked list** is a linear data structure where elements (nodes) are stored in separate memory locations and connected via pointers/references.

### Node Structure
```python
class Node:
    def __init__(self, data):
        self.data = data    # Store the value
        self.next = None    # Reference to next node
```

### Linked List vs Array

| Feature | Array | Linked List |
|---------|-------|-------------|
| Memory | Contiguous | Non-contiguous |
| Access | O(1) by index | O(n) sequential |
| Insertion (beginning) | O(n) | O(1) |
| Insertion (end) | O(1) amortized | O(n) without tail |
| Deletion (beginning) | O(n) | O(1) |
| Size | Fixed (static) | Dynamic |
| Cache Performance | Better (locality) | Worse (scattered) |

### Types of Linked Lists
1. **Singly Linked List**: Each node points to next (→)
2. **Doubly Linked List**: Each node points to next and previous (⟷)
3. **Circular Linked List**: Last node points back to first (circular)

This guide covers **Singly Linked Lists**.

---

## Simple Linked List
**📁 Implementation:** [Simple Linked List.py](./01.%20Simple%20Linked%20List.py)

### Node Class
```python
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
```

### LinkedList Class
```python
class LinkedList:
    def __init__(self):
        self.head = None  # Start of the list
```

### Creating a Linked List
```python
# Create nodes
node1 = Node(10)
node2 = Node(20)
node3 = Node(30)

# Link them
node1.next = node2
node2.next = node3

# Create linked list
ll = LinkedList()
ll.head = node1
```

**Visual Representation:**
```
head → [10|•] → [20|•] → [30|None]
```

### Basic Operations Overview
- **Traversal**: Visit each node sequentially
- **Search**: Find node with specific value
- **Insert**: Add new node (beginning, end, position)
- **Delete**: Remove node (beginning, end, specific)

---

## Traversing a Linked List
**📁 Implementation:** [Traversing a linked list.py](./02.%20Traversing%20a%20linked%20list.py)

### Problem
Visit and print all nodes in the linked list.

### Logic
Start from head, follow `next` pointers until reaching `None`.

### Implementation
```python
def traverse(head):
    current = head
    while current is not None:
        print(current.data, end=" → ")
        current = current.next
    print("None")
```

### How It Works
```
List: 10 → 20 → 30 → None

Step 1: current = head (10)
        Print 10
        current = current.next (20)

Step 2: current = 20
        Print 20
        current = current.next (30)

Step 3: current = 30
        Print 30
        current = current.next (None)

Step 4: current = None, exit loop
```

### Recursive Traversal
```python
def traverse_recursive(head):
    if head is None:
        return
    print(head.data, end=" → ")
    traverse_recursive(head.next)
```

### Time Complexity
- **Time**: O(n) - visit each node once
- **Space**: O(1) iterative, O(n) recursive (call stack)

### Use Cases
- Printing linked list
- Counting nodes
- Accessing all elements

---

## Search in Linked List
**📁 Implementation:** [Search in Linked List.py](./03.%20Search%20in%20Linked%20List.py)

### Problem
Find if a value exists in the linked list and return its position (1-indexed) or -1.

### Iterative Approach
```python
def search(head, key):
    current = head
    position = 1
    
    while current is not None:
        if current.data == key:
            return position
        current = current.next
        position += 1
    
    return -1  # Not found
```

### Recursive Approach
```python
def search_recursive(head, key, position=1):
    if head is None:
        return -1
    if head.data == key:
        return position
    return search_recursive(head.next, key, position + 1)
```

### Time Complexity
- **Best Case**: O(1) - element at head
- **Average Case**: O(n/2) = O(n)
- **Worst Case**: O(n) - element at end or not present

### Space Complexity
- **Iterative**: O(1)
- **Recursive**: O(n) - call stack

### Example
```
List: 10 → 20 → 30 → 40

search(head, 30) → 3
search(head, 50) → -1
```

---

## Insert at Beginning
**📁 Implementation:** [Insert at the beginning of linked list.py](./04.%20Insert%20at%20the%20beginning%20of%20linked%20list.py)

### Problem
Add a new node at the start of the linked list.

### Logic
1. Create new node
2. Point new node's next to current head
3. Update head to new node

### Implementation
```python
def insert_at_beginning(head, data):
    new_node = Node(data)
    new_node.next = head
    return new_node  # New head
```

### Visual Example
```
Before: head → [20|•] → [30|None]

Insert 10 at beginning:

Step 1: Create node [10|None]
Step 2: Point it to current head
        [10|•] → [20|•] → [30|None]
Step 3: Update head
        head → [10|•] → [20|•] → [30|None]

After: 10 → 20 → 30
```

### Time Complexity
- **Time**: O(1) - constant time operation
- **Space**: O(1) - one new node

### When to Use
- Implementing stack (push operation)
- When order doesn't matter
- When frequent insertions at start

---

## Insert at End
**📁 Implementation:** [Insert at the end of linked list.py](./05.%20Insert%20at%20the%20end%20of%20linked%20list.py)

### Problem
Add a new node at the end of the linked list.

### Logic
1. Create new node
2. If list is empty, make it head
3. Otherwise, traverse to last node
4. Point last node's next to new node

### Implementation
```python
def insert_at_end(head, data):
    new_node = Node(data)
    
    # Empty list
    if head is None:
        return new_node
    
    # Traverse to last node
    current = head
    while current.next is not None:
        current = current.next
    
    # Insert at end
    current.next = new_node
    return head
```

### Visual Example
```
Before: head → [10|•] → [20|None]

Insert 30 at end:

Step 1: Create node [30|None]
Step 2: Traverse to last node (20)
Step 3: Point last.next to new node
        [10|•] → [20|•] → [30|None]

After: 10 → 20 → 30
```

### Time Complexity
- **Time**: O(n) - must traverse entire list
- **Space**: O(1)

### Optimization with Tail Pointer
```python
class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None  # Track last node
    
    def insert_at_end_optimized(self, data):
        new_node = Node(data)
        if self.tail is None:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
```

**With tail**: O(1) insertion at end

---

## Insert at Given Position
**📁 Implementation:** [Insert at a given position in singly linked list.py](./06.%20Insert%20at%20a%20given%20position%20in%20singly%20linked%20list.py)

### Problem
Insert a node at a specific position (1-indexed).

### Logic
1. If position is 1, insert at beginning
2. Traverse to (position - 1)th node
3. Insert new node after it

### Implementation
```python
def insert_at_position(head, data, position):
    new_node = Node(data)
    
    # Position 1 = insert at beginning
    if position == 1:
        new_node.next = head
        return new_node
    
    # Traverse to (position-1)th node
    current = head
    for i in range(1, position - 1):
        if current is None:
            return head  # Invalid position
        current = current.next
    
    if current is None:
        return head  # Invalid position
    
    # Insert
    new_node.next = current.next
    current.next = new_node
    
    return head
```

### Visual Example
```
Before: 10 → 20 → 40 → None

Insert 30 at position 3:

Step 1: Traverse to node at position 2 (20)
Step 2: new_node.next = current.next (40)
        [30|•] → [40|None]
Step 3: current.next = new_node
        [20|•] → [30|•] → [40|None]

After: 10 → 20 → 30 → 40
```

### Time Complexity
- **Time**: O(n) - may need to traverse to position
- **Space**: O(1)

### Edge Cases
- Position 1: Insert at beginning
- Position > length: Invalid or insert at end
- Empty list: Only valid if position = 1

---

## Delete First Node
**📁 Implementation:** [Delete first node of linked list.py](./07.%20Delete%20first%20node%20of%20linked%20list.py)

### Problem
Remove the first node from the linked list.

### Logic
Simply move head to the next node. Old head becomes garbage collected.

### Implementation
```python
def delete_first(head):
    if head is None:
        return None  # Empty list
    return head.next  # Return new head
```

### Visual Example
```
Before: head → [10|•] → [20|•] → [30|None]

Delete first:

Step 1: new_head = head.next (20)
        head → [10|•]    [20|•] → [30|None]
                 ↓        ↑
              (garbage)   new head

After: head → [20|•] → [30|None]
```

### Time Complexity
- **Time**: O(1) - constant time
- **Space**: O(1)

### Edge Cases
- Empty list: Return None
- Single node: Returns None (empty list)

---

## Delete Last Node
**📁 Implementation:** [Delete last node of linked list.py](./08.%20Delete%20last%20node%20of%20linked%20list.py)

### Problem
Remove the last node from the linked list.

### Logic
1. Traverse to second-last node
2. Set its next to None

### Implementation
```python
def delete_last(head):
    # Empty list or single node
    if head is None or head.next is None:
        return None
    
    # Traverse to second-last node
    current = head
    while current.next.next is not None:
        current = current.next
    
    # Remove last node
    current.next = None
    return head
```

### Visual Example
```
Before: [10|•] → [20|•] → [30|None]

Delete last:

Step 1: Traverse to second-last (20)
Step 2: Set current.next = None
        [10|•] → [20|None]    [30]
                                ↓
                            (garbage)

After: [10|•] → [20|None]
```

### Time Complexity
- **Time**: O(n) - must traverse to second-last
- **Space**: O(1)

### Edge Cases
- Empty list: Return None
- Single node: Return None
- Two nodes: Head points to None

---

## Delete Node with Pointer Only
**📁 Implementation:** [Delete a node with only pointer given to it.py](./09.%20Delete%20a%20node%20with%20only%20pointer%20given%20to%20it.py)

### Problem
Delete a node when you only have a pointer to that node (not the head). Assume it's not the last node.

### Logic (Copy and Delete Trick)
Since we can't access the previous node:
1. Copy data from next node to current node
2. Delete the next node

### Implementation
```python
def delete_node_with_pointer(node):
    # Cannot delete if it's the last node
    if node is None or node.next is None:
        return
    
    # Copy next node's data
    node.data = node.next.data
    
    # Delete next node
    node.next = node.next.next
```

### Visual Example
```
Before: [10|•] → [20|•] → [30|•] → [40|None]
                   ↑
              delete this

Step 1: Copy next node's data (30) to current
        [10|•] → [30|•] → [30|•] → [40|None]
                   ↑

Step 2: Point current to next.next
        [10|•] → [30|•] ----------→ [40|None]
                          [30|•]
                            ↓
                        (garbage)

After: [10|•] → [30|•] → [40|None]
```

### Time Complexity
- **Time**: O(1) - constant time
- **Space**: O(1)

### Limitations
- **Cannot delete last node** (no next node to copy from)
- **Not true deletion** (copies data, doesn't actually remove the node)
- Used in interview questions to test understanding

---

## Sorted Insert
**📁 Implementation:** [Sorted Insert in a linked list.py](./10.%20Sorted%20Insert%20in%20a%20linked%20list.py)

### Problem
Insert a node in a sorted linked list such that the list remains sorted.

### Logic
1. If list is empty or data < head.data, insert at beginning
2. Traverse until finding position where current < data < next
3. Insert new node between them

### Implementation
```python
def sorted_insert(head, data):
    new_node = Node(data)
    
    # Empty list or insert at beginning
    if head is None or data < head.data:
        new_node.next = head
        return new_node
    
    # Find position
    current = head
    while current.next is not None and current.next.data < data:
        current = current.next
    
    # Insert
    new_node.next = current.next
    current.next = new_node
    
    return head
```

### Visual Example
```
Before: 10 → 20 → 40 → 50
Insert: 30

Step 1: Traverse while next.data < 30
        current at 20 (next is 40 > 30, stop)

Step 2: Insert 30 between 20 and 40
        10 → 20 → 30 → 40 → 50

After: Sorted list maintained
```

### Time Complexity
- **Time**: O(n) - may traverse entire list
- **Space**: O(1)

### Use Cases
- Maintaining sorted order
- Merge sorted lists
- Priority queues

---

## Insert in Middle
**📁 Implementation:** [Insert a node in the middle of linked list.py](./11.%20Insert%20a%20node%20in%20the%20middle%20of%20linked%20list.py)

### Problem
Insert a node at the exact middle of the linked list.

### Logic (Two Pointer / Slow-Fast)
Use slow and fast pointers to find middle:
- Slow moves 1 step
- Fast moves 2 steps
- When fast reaches end, slow is at middle

### Implementation
```python
def insert_in_middle(head, data):
    new_node = Node(data)
    
    # Empty list
    if head is None:
        return new_node
    
    # Single node
    if head.next is None:
        head.next = new_node
        return head
    
    # Find middle using slow-fast pointers
    slow = head
    fast = head.next
    
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
    
    # Insert after slow (middle position)
    new_node.next = slow.next
    slow.next = new_node
    
    return head
```

### Visual Example
```
Before: 10 → 20 → 30 → 40 → 50
Insert: 25 in middle

Step 1: Find middle using slow-fast
        slow at 30 (middle)

Step 2: Insert after slow
        10 → 20 → 30 → 25 → 40 → 50

For even length: inserts after first middle
For odd length: inserts after exact middle
```

### Time Complexity
- **Time**: O(n) - traverse half the list
- **Space**: O(1)

---

## N-th Node from End
**📁 Implementation:** [Find n-th Node from the end of the linked list.py](./12.%20Find%20n-th%20Node%20from%20the%20end%20of%20the%20linked%20list.py)

### Problem
Find the n-th node from the end of the linked list.

Example: List = 10→20→30→40→50, n=2 → Result: 40

### Approach 1: Two Pass
```python
def nth_from_end_two_pass(head, n):
    # First pass: count nodes
    length = 0
    current = head
    while current is not None:
        length += 1
        current = current.next
    
    # Second pass: go to (length - n + 1)th node from start
    if n > length:
        return None
    
    current = head
    for i in range(length - n):
        current = current.next
    
    return current.data
```

**Time**: O(n), **Space**: O(1)

### Approach 2: Two Pointer (Optimal - Single Pass)
```python
def nth_from_end(head, n):
    # Move first pointer n steps ahead
    first = head
    for i in range(n):
        if first is None:
            return None  # n > length
        first = first.next
    
    # Move both pointers until first reaches end
    second = head
    while first is not None:
        first = first.next
        second = second.next
    
    return second.data
```

### How Two Pointer Works
```
List: 10 → 20 → 30 → 40 → 50 → None
Find 2nd from end (40)

Step 1: Move first pointer 2 steps ahead
first:         30 → 40 → 50 → None
second: 10 → 20 → 30 → 40 → 50 → None

Step 2: Move both until first reaches None
first:                        None
second:                40 → 50 → None

Result: second.data = 40
```

### Time Complexity
- **Two Pass**: O(n) - traverse twice
- **Two Pointer**: O(n) - single traversal

### Space Complexity
- Both: O(1)

### Edge Cases
- n > length: Return None or error
- n = 1: Last node
- n = length: First node

---

## Remove Duplicates from Sorted
**📁 Implementation:** [Remove duplicates from a sorted linked list.py](./13.%20Remove%20duplicates%20from%20a%20sorted%20linked%20list.py)

### Problem
Remove duplicate nodes from a sorted linked list.

Example: 10→10→20→20→30 → 10→20→30

### Logic
Since list is sorted, duplicates are adjacent. Compare current with next and skip duplicates.

### Implementation
```python
def remove_duplicates(head):
    if head is None:
        return None
    
    current = head
    while current is not None and current.next is not None:
        if current.data == current.next.data:
            # Skip duplicate
            current.next = current.next.next
        else:
            # Move to next distinct value
            current = current.next
    
    return head
```

### Visual Example
```
Before: 10 → 10 → 20 → 20 → 20 → 30 → 30

Step 1: current at first 10
        10.data == 10.next.data (10)
        Skip: 10 --------→ 20 → 20 → 20 → 30 → 30

Step 2: current still at 10
        10.data != 10.next.data (20)
        Move: current = 20

Step 3: current at first 20
        20.data == 20.next.data (20)
        Skip: 10 → 20 --------→ 20 → 30 → 30

Step 4: Continue until all duplicates removed

After: 10 → 20 → 30
```

### Time Complexity
- **Time**: O(n) - single pass
- **Space**: O(1) - in-place removal

### For Unsorted List
Would need O(n²) nested loops or O(n) with hash set.

---

## Reverse a Linked List
**📁 Implementation:** [Reverse a linked list.py](./14.%20Reverse%20a%20linked%20list.py)

### Problem
Reverse the linked list so that last node becomes first.

Example: 10→20→30→40 → 40→30→20→10

### Iterative Approach (Three Pointers)
```python
def reverse_iterative(head):
    prev = None
    current = head
    
    while current is not None:
        next_node = current.next  # Save next
        current.next = prev        # Reverse link
        prev = current             # Move prev forward
        current = next_node        # Move current forward
    
    return prev  # New head
```

### Visual Example
```
Before: 10 → 20 → 30 → None

Initial: prev=None, current=10

Step 1: next_node = 20
        current.next = None
        None ← 10    20 → 30 → None
        prev = 10, current = 20

Step 2: next_node = 30
        current.next = 10
        None ← 10 ← 20    30 → None
        prev = 20, current = 30

Step 3: next_node = None
        current.next = 20
        None ← 10 ← 20 ← 30
        prev = 30, current = None

Return prev (30 is new head)

After: 30 → 20 → 10 → None
```

### Time Complexity
- **Time**: O(n) - visit each node once
- **Space**: O(1) - only three pointers

### Key Points
- **Three pointers needed**: prev, current, next
- **Links reversed one by one**
- **Return prev** (not current) as new head

---

## Recursive Reverse (Way 1)
**📁 Implementation:** [Recursive Reverse a linked list way 1.py](./15.%20Recursive%20Reverse%20a%20linked%20list%20way%201.py)

### Problem
Reverse linked list using recursion - first approach.

### Logic (Reverse from End)
1. Recursively reach the last node (new head)
2. On the way back, reverse links

### Implementation
```python
def reverse_recursive_way1(head):
    # Base case: empty or single node
    if head is None or head.next is None:
        return head
    
    # Recursive call
    new_head = reverse_recursive_way1(head.next)
    
    # Reverse the link
    head.next.next = head
    head.next = None
    
    return new_head
```

### How It Works
```
List: 10 → 20 → 30 → None

Call reverse(10):
    Call reverse(20):
        Call reverse(30):
            Return 30 (base case)
        
        # Back at 20
        20.next.next = 20  →  30.next = 20  →  30 → 20
        20.next = None      →  30 → 20 → None
        Return 30
    
    # Back at 10
    10.next.next = 10  →  20.next = 10  →  30 → 20 → 10
    10.next = None     →  30 → 20 → 10 → None
    Return 30

New head: 30
Result: 30 → 20 → 10 → None
```

### Time Complexity
- **Time**: O(n) - visit each node
- **Space**: O(n) - recursion call stack

---

## Recursive Reverse (Way 2)
**📁 Implementation:** [Recursive Reverse a linked list way 2.py](./16.%20Recursive%20Reverse%20a%20linked%20list%20way%202.py)

### Problem
Reverse linked list using recursion - alternative approach.

### Logic (Pass Previous Node)
Pass previous node as parameter and reverse links during recursion.

### Implementation
```python
def reverse_recursive_way2(current, prev=None):
    # Base case: reached end
    if current is None:
        return prev  # prev is new head
    
    # Save next node
    next_node = current.next
    
    # Reverse current link
    current.next = prev
    
    # Recurse with next node
    return reverse_recursive_way2(next_node, current)
```

### How It Works
```
List: 10 → 20 → 30 → None

Call reverse(10, None):
    next = 20
    10.next = None  →  None ← 10
    Call reverse(20, 10):
        next = 30
        20.next = 10  →  None ← 10 ← 20
        Call reverse(30, 20):
            next = None
            30.next = 20  →  None ← 10 ← 20 ← 30
            Call reverse(None, 30):
                Return 30 (base case)
            Return 30
        Return 30
    Return 30

Result: 30 → 20 → 10 → None
```

### Comparison: Recursive Way 1 vs Way 2

| Aspect | Way 1 | Way 2 |
|--------|-------|-------|
| **Approach** | Reverse on way back | Reverse on way forward |
| **Parameters** | Only head | Current and previous |
| **Reversal Point** | After recursive call | Before recursive call |
| **Intuition** | Reach end, then reverse | Reverse while going forward |

### Time Complexity
- **Time**: O(n)
- **Space**: O(n) - call stack

Both recursive approaches are less space-efficient than iterative but demonstrate recursion concepts.

---

## Comparison Summary

### Time Complexity Table

| Operation | Time | Space | Notes |
|-----------|------|-------|-------|
| Traverse | O(n) | O(1) | Visit all nodes |
| Search | O(n) | O(1) | Linear search |
| Insert at Beginning | O(1) | O(1) | Just update head |
| Insert at End | O(n) | O(1) | Or O(1) with tail pointer |
| Insert at Position | O(n) | O(1) | Traverse to position |
| Delete First | O(1) | O(1) | Just update head |
| Delete Last | O(n) | O(1) | Traverse to second-last |
| Delete with Pointer | O(1) | O(1) | Copy-delete trick |
| Sorted Insert | O(n) | O(1) | Find position |
| Insert in Middle | O(n) | O(1) | Slow-fast pointers |
| N-th from End | O(n) | O(1) | Two pointer technique |
| Remove Duplicates | O(n) | O(1) | For sorted list |
| Reverse (Iterative) | O(n) | O(1) | Three pointers |
| Reverse (Recursive) | O(n) | O(n) | Call stack |

---

## Linked List Patterns

### Pattern 1: Two Pointer (Slow-Fast)
Used for finding middle, detecting cycles, finding n-th from end.

```python
def find_middle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow  # Middle node
```

### Pattern 2: Two Pointer (Leading-Following)
Used for n-th from end.

```python
def nth_from_end(head, n):
    first = second = head
    # Move first n steps ahead
    for _ in range(n):
        first = first.next
    # Move both together
    while first:
        first = first.next
        second = second.next
    return second
```

### Pattern 3: Dummy Node
Simplifies edge cases (empty list, deleting head).

```python
def delete_value(head, value):
    dummy = Node(0)
    dummy.next = head
    current = dummy
    
    while current.next:
        if current.next.data == value:
            current.next = current.next.next
        else:
            current = current.next
    
    return dummy.next  # New head
```

### Pattern 4: Runner Technique
One pointer moves faster than another.

```python
def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False
```

---

## Advantages of Linked Lists

### 1. Dynamic Size
No need to specify size upfront, grows/shrinks as needed.

### 2. Efficient Insertions/Deletions
O(1) insertion/deletion at beginning (vs O(n) for arrays).

### 3. No Memory Waste
Only allocates memory for existing elements.

### 4. Implementation of Other Structures
- Stack (push/pop at head)
- Queue (enqueue at tail, dequeue at head)
- Graph adjacency lists

---

## Disadvantages of Linked Lists

### 1. No Random Access
Cannot access element by index in O(1) time.

### 2. Extra Memory
Each node requires extra space for pointer.

### 3. Poor Cache Locality
Nodes scattered in memory, not cache-friendly.

### 4. Traversal Only in One Direction
(For singly linked list - need doubly for backward traversal)

---

## Common Mistakes to Avoid

### 1. Losing Reference to Head
```python
# ❌ Wrong
def insert_at_beginning(head, data):
    new_node = Node(data)
    new_node.next = head
    head = new_node  # Local variable, doesn't update outside

# ✅ Correct
def insert_at_beginning(head, data):
    new_node = Node(data)
    new_node.next = head
    return new_node  # Return new head
```

### 2. Not Handling Empty List
```python
# ❌ May crash
def delete_first(head):
    return head.next  # NoneType has no attribute 'next'

# ✅ Check for None
def delete_first(head):
    if head is None:
        return None
    return head.next
```

### 3. Infinite Loop (Cycle)
```python
# ❌ Creates cycle
node.next = head
head = node
# This creates a cycle if node was already in list

# ✅ Be careful with pointer manipulation
```

### 4. Losing Nodes During Insertion
```python
# ❌ Wrong order
current.next = new_node
new_node.next = current.next  # Lost original next!

# ✅ Correct order
new_node.next = current.next
current.next = new_node
```

### 5. Not Updating Head After Modification
```python
# Remember: Operations may change head
head = insert_at_beginning(head, 10)
head = delete_first(head)
head = reverse(head)
```

---

## Edge Cases to Test

### Always Test With:
1. **Empty list**: `head = None`
2. **Single node**: `10 → None`
3. **Two nodes**: `10 → 20 → None`
4. **Large list**: Many nodes
5. **Duplicates**: `10 → 10 → 20 → 20`
6. **All same values**: `5 → 5 → 5 → 5`
7. **Position = 1**: Insert/delete at head
8. **Position = length**: Insert/delete at end
9. **Invalid position**: Position > length or < 1

---

## When to Use Linked Lists

### Use Linked Lists When:
- **Frequent insertions/deletions** at beginning
- **Size unknown** or changes frequently
- **No random access** needed
- Implementing **stacks, queues, graphs**
- **Memory fragmentation** is acceptable

### Use Arrays When:
- Need **random access** (index-based)
- **Frequent access** by position
- **Cache performance** matters
- Size is **relatively fixed**
- **Binary search** needed

---

## Linked List vs Array - Detailed Comparison

| Operation | Array | Linked List |
|-----------|-------|-------------|
| **Access by index** | O(1) | O(n) |
| **Search** | O(n) unsorted, O(log n) sorted | O(n) |
| **Insert at beginning** | O(n) | O(1) |
| **Insert at end** | O(1) amortized | O(n) or O(1) with tail |
| **Insert at position** | O(n) | O(n) |
| **Delete at beginning** | O(n) | O(1) |
| **Delete at end** | O(1) | O(n) or O(1) with tail |
| **Delete at position** | O(n) | O(n) |
| **Memory** | Contiguous, fixed | Scattered, dynamic |
| **Cache performance** | Good | Poor |
| **Extra memory** | None | Pointer per node |

---

## Interview Tips

### Common Interview Questions
1. **Reverse a linked list** - Know iterative and recursive
2. **Detect cycle** - Floyd's cycle detection (slow-fast)
3. **Find middle** - Slow-fast pointers
4. **Merge two sorted lists**
5. **Remove n-th node from end** - Two pointers
6. **Check if palindrome**
7. **Add two numbers** (represented as linked lists)
8. **Clone list with random pointer**

### What Interviewers Look For
- **Edge case handling** (empty, single node)
- **Pointer manipulation** skills
- **Time/space complexity** awareness
- **Multiple approaches** (iterative vs recursive)
- **Clean code** with proper naming

### Tips for Success
1. **Draw diagrams** - Visualize pointer changes
2. **Test edge cases** - Empty, single, two nodes
3. **Explain as you code** - Walk through your logic
4. **Consider optimizations** - Can you do it in one pass?
5. **Practice pointer manipulation** - This is the core skill

---

## Advanced Linked List Concepts

### 1. Doubly Linked List
Each node has `prev` and `next` pointers.

```python
class DoublyNode:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None
```

**Advantages**: Bidirectional traversal, easier deletion  
**Disadvantages**: More memory for extra pointer

### 2. Circular Linked List
Last node points back to first (forms a circle).

```python
# Creating circular list
last.next = head  # Connect last to first
```

**Use Cases**: Round-robin scheduling, circular buffers

### 3. Skip List
Multiple levels of linked lists for faster search (O(log n)).

### 4. XOR Linked List
Space-efficient doubly linked list using XOR of addresses.

---

## Practice Problems

### Easy
1. Find length of linked list
2. Print linked list in reverse
3. Check if linked list is palindrome
4. Merge two sorted linked lists
5. Remove all occurrences of a value

### Medium
1. Add two numbers represented as linked lists
2. Find intersection point of two linked lists
3. Flatten a multilevel linked list
4. Clone a linked list with random pointers
5. Partition list around value

### Hard
1. Reverse nodes in k-groups
2. Merge k sorted linked lists
3. LRU Cache implementation
4. Find median in stream using linked list
5. Design a data structure with insert, delete, getRandom in O(1)

---

## Implementation Best Practices

### 1. Use Descriptive Variable Names
```python
# ❌ Confusing
def f(h, d):
    n = N(d)
    n.n = h
    return n

# ✅ Clear
def insert_at_beginning(head, data):
    new_node = Node(data)
    new_node.next = head
    return new_node
```

### 2. Handle Edge Cases First
```python
def delete_first(head):
    if head is None:  # Handle edge case first
        return None
    return head.next
```

### 3. Draw Before Coding
Always draw the linked list and pointer changes before implementing.

### 4. Use Helper Functions
```python
def get_length(head):
    count = 0
    current = head
    while current:
        count += 1
        current = current.next
    return count

# Use in other functions
def nth_from_end(head, n):
    length = get_length(head)
    # ... rest of logic
```

### 5. Maintain Invariants
Document what each pointer represents and maintain consistency.

---

## Common Linked List Operations - Code Snippets

### Count Nodes
```python
def count_nodes(head):
    count = 0
    current = head
    while current:
        count += 1
        current = current.next
    return count
```

### Print in Reverse (Recursive)
```python
def print_reverse(head):
    if head is None:
        return
    print_reverse(head.next)
    print(head.data, end=" ")
```

### Get Middle Node
```python
def get_middle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow
```

### Detect Cycle (Floyd's Algorithm)
```python
def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False
```

### Find Cycle Start Point
```python
def find_cycle_start(head):
    slow = fast = head
    
    # Find meeting point
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            break
    else:
        return None  # No cycle
    
    # Find start of cycle
    slow = head
    while slow != fast:
        slow = slow.next
        fast = fast.next
    
    return slow
```

---

## Memory Management

### Python's Garbage Collection
Python automatically deletes nodes with no references.

```python
# This node will be garbage collected
head = head.next  # Old head has no references now
```

### In Other Languages (C/C++)
Must manually free memory:

```c
// C code
Node* temp = head;
head = head->next;
free(temp);  // Must manually free
```

---

## Complexity Cheat Sheet

### Time Complexity
- **Access**: O(n)
- **Search**: O(n)
- **Insert (beginning)**: O(1)
- **Insert (end)**: O(n) or O(1) with tail
- **Insert (middle)**: O(n)
- **Delete (beginning)**: O(1)
- **Delete (end)**: O(n)
- **Delete (middle)**: O(n)

### Space Complexity
- **Storage**: O(n) - n nodes
- **Operations**: O(1) iterative, O(n) recursive

---
