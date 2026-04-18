"""
Problem 057: Building an LRU Cache

Difficulty: Advanced
Topic: Data Structure Implementation (INTERVIEW FAVORITE!)

=== PROBLEM DESCRIPTION ===

LRU (Least Recently Used) Cache is a cache that evicts the least recently
used item when it reaches capacity. It must support O(1) get and put operations.

This uses a combination of:
- Hash map for O(1) lookup
- Doubly linked list for O(1) removal and insertion

Your Task:
-----------
1. Create a `DLLNode` class (Doubly Linked List Node):
   - `__init__(key, value)` - stores key, value, prev, next

2. Create an `LRUCache` class:
   - `__init__(capacity)` - maximum number of items
   - `get(key)` - return value if exists, move to front (most recent)
   - `put(key, value)` - insert/update, move to front, evict LRU if full
   - Both operations must be O(1)!

3. Internal structure:
   - `_cache` - dict mapping key to DLLNode
   - `_head`, `_tail` - dummy nodes for easier list manipulation
   - Helper methods: `_remove(node)`, `_add_to_front(node)`

Expected Output:
----------------
put(1, 'A'), put(2, 'B'), put(3, 'C')
get(1): A  (1 is now most recent)
put(4, 'D')  (capacity reached, evict LRU which is 2)
get(2): None  (2 was evicted)
get(3): C
Cache state: [(4, D), (3, C), (1, A)]  (most recent first)

=== CONCEPTS TO LEARN ===
- Combine hash map + doubly linked list
- Head = most recent, Tail = least recent
- Get: move accessed node to head
- Put: add to head, if full remove from tail
- VERY common interview question!

=== STARTER CODE ===
"""

# Write your solution below this line
# -----------------------------------



# Test your solution
# ------------------
# cache = LRUCache(3)
#
# cache.put(1, 'A')
# cache.put(2, 'B')
# cache.put(3, 'C')
# print("put(1, 'A'), put(2, 'B'), put(3, 'C')")
#
# print(f"get(1): {cache.get(1)}  (1 is now most recent)")
#
# cache.put(4, 'D')
# print("put(4, 'D')  (capacity reached, evict LRU which is 2)")
#
# print(f"get(2): {cache.get(2)}  (2 was evicted)")
# print(f"get(3): {cache.get(3)}")
#
# # Show cache state (implement __str__ or similar)
# print(f"Cache contents: {list(cache._cache.keys())}")
