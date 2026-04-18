"""
Problem 056: Building a Min Heap Class

Difficulty: Advanced
Topic: Data Structure Implementation

=== PROBLEM DESCRIPTION ===

A heap is a complete binary tree where each parent is smaller (min-heap)
or larger (max-heap) than its children. The root is always the min/max.
Heaps are used for priority queues and heap sort.

Array representation:
- Parent of index i: (i-1) // 2
- Left child of index i: 2*i + 1
- Right child of index i: 2*i + 2

Your Task:
-----------
1. Create a `MinHeap` class:
   - `__init__()` - initialize with empty list
   - `insert(value)` - add value and bubble up
   - `extract_min()` - remove and return minimum, then heapify down
   - `peek()` - return minimum without removing
   - `size()` - return number of elements
   - `is_empty()` - return True if empty

2. Helper methods:
   - `_bubble_up(index)` - move element up until heap property satisfied
   - `_bubble_down(index)` - move element down until heap property satisfied
   - `_parent(index)`, `_left_child(index)`, `_right_child(index)`

3. Build heap from list:
   - `heapify(lst)` - classmethod, creates heap from list in O(n)

Expected Output:
----------------
Heap after inserts: [1, 3, 2, 7, 6, 4, 5]
Extract min: 1
Extract min: 2
Heap now: [3, 6, 4, 7]

Heapify [5, 3, 8, 1, 2]: [1, 2, 8, 5, 3]

=== CONCEPTS TO LEARN ===
- Complete binary tree stored in array
- Heap property: parent <= children (min heap)
- Insert: add at end, bubble up - O(log n)
- Extract: remove root, move last to root, bubble down - O(log n)
- Heapify: build heap from array - O(n)

=== STARTER CODE ===
"""

# Write your solution below this line
# -----------------------------------



# Test your solution
# ------------------
# heap = MinHeap()
# for val in [4, 2, 7, 1, 6, 3, 5]:
#     heap.insert(val)
#
# print(f"Heap after inserts: {heap.heap}")
# print(f"Extract min: {heap.extract_min()}")
# print(f"Extract min: {heap.extract_min()}")
# print(f"Heap now: {heap.heap}")
#
# print()
#
# # Heapify
# heap2 = MinHeap.heapify([5, 3, 8, 1, 2])
# print(f"Heapify [5, 3, 8, 1, 2]: {heap2.heap}")
