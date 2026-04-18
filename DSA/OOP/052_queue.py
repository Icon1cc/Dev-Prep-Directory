"""
Problem 052: Building a Queue Class

Difficulty: Intermediate
Topic: Data Structure Implementation

=== PROBLEM DESCRIPTION ===

A queue is a FIFO (First In, First Out) data structure. Think of a line
at a store - first person in line is served first.

Your Task:
-----------
1. Create a `Queue` class:
   - `__init__(max_size=None)` - optional maximum size
   - `enqueue(item)` - add item to back
   - `dequeue()` - remove and return front item
   - `front()` - return front item without removing
   - `rear()` - return back item without removing
   - `is_empty()` - return True if empty
   - `size()` - return current number of items
   - `__str__` - visual: front [1, 2, 3] back

2. Create a `PriorityQueue` class:
   - Items have priorities (lower number = higher priority)
   - `enqueue(item, priority)` - add with priority
   - `dequeue()` - remove highest priority item

3. Implement practical use case:
   - `HotPotatoSimulation(names, num)` - circular queue game
   - Pass the "potato" num times, eliminate the holder

Expected Output:
----------------
Queue: front [1, 2, 3] back
Dequeue: 1
Queue after dequeue: front [2, 3] back

Priority Queue:
Dequeue (highest priority): Task A
Dequeue (next): Task C

Hot Potato winner: Alice (from ["Alice", "Bob", "Charlie", "David", "Eve"])

=== CONCEPTS TO LEARN ===
- FIFO principle
- enqueue/dequeue operations
- Priority queues order by priority, not arrival
- Used in: BFS, task scheduling, printer queues

=== STARTER CODE ===
"""

# Write your solution below this line
# -----------------------------------



# Test your solution
# ------------------
# # Basic Queue
# q = Queue()
# q.enqueue(1)
# q.enqueue(2)
# q.enqueue(3)
#
# print(f"Queue: {q}")
# print(f"Dequeue: {q.dequeue()}")
# print(f"Queue after dequeue: {q}")
#
# print("\nPriority Queue:")
# pq = PriorityQueue()
# pq.enqueue("Task B", priority=2)
# pq.enqueue("Task A", priority=1)  # Higher priority (lower number)
# pq.enqueue("Task C", priority=2)
#
# print(f"Dequeue (highest priority): {pq.dequeue()}")
# print(f"Dequeue (next): {pq.dequeue()}")
#
# print()
#
# # Hot Potato
# names = ["Alice", "Bob", "Charlie", "David", "Eve"]
# winner = hot_potato_simulation(names, 7)
# print(f"Hot Potato winner: {winner} (from {names})")
