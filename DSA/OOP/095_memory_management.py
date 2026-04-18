"""
Problem 095: Memory Management and Garbage Collection

Difficulty: Advanced
Topic: Python Internals

=== PROBLEM DESCRIPTION ===

Understand how Python manages memory and garbage collection. This is
important for writing efficient code and debugging memory issues.

Your Task:
-----------
1. Explore reference counting:
   - Use sys.getrefcount() to see reference counts
   - Understand when objects are destroyed

2. Create circular reference example:
   - Object A references B, B references A
   - Show that reference counting alone can't collect them
   - Use gc module to collect cycles

3. Implement __del__ destructor:
   - Understand when it's called
   - Pitfalls of __del__ (resurrection, circular refs)

4. Use weakref to break circular references:
   - Compare strong vs weak references
   - WeakValueDictionary for caches

5. Profile memory usage:
   - Use tracemalloc to track allocations
   - Identify memory leaks
   - Use sys.getsizeof() for object sizes

Expected Output:
----------------
Reference counting:
x = [1, 2, 3]
ref count: 2 (x + getrefcount argument)
y = x
ref count: 3
del y
ref count: 2

Circular reference:
Created A -> B -> A cycle
del a, b (but objects not collected!)
gc.collect(): Collected 2 objects

Weak references:
Strong ref: Object exists
Weak ref after del strong: Object was garbage collected

Memory profiling:
Before: 1.2 MB
Creating 100000 objects...
After: 15.4 MB
Top allocations:
  example.py:45 - 14.2 MB

=== CONCEPTS TO LEARN ===
- Reference counting for immediate cleanup
- Garbage collector for cycles
- __del__ method caveats
- weakref for caches and observers
- Memory profiling tools

=== STARTER CODE ===
"""

import sys
import gc
import weakref
import tracemalloc

# Write your solution below this line
# -----------------------------------



# Test your solution
# ------------------
# Demonstrate memory management concepts
