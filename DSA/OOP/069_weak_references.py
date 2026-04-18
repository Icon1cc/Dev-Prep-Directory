"""
Problem 069: Weak References

Difficulty: Advanced
Topic: Memory Management

=== PROBLEM DESCRIPTION ===

Weak references allow you to refer to an object without preventing it from
being garbage collected. Useful for caches, observers, and avoiding circular
references.

Your Task:
-----------
1. Understand regular references vs weak references:
   - Regular: keeps object alive
   - Weak: allows garbage collection

2. Create a `Cache` class using WeakValueDictionary:
   - Cached objects can be garbage collected when not referenced elsewhere
   - Useful for memory-efficient caching

3. Create an `Observable` class using weak references:
   - Observers don't prevent garbage collection
   - Dead observers are automatically removed

4. Demonstrate circular reference handling:
   - Parent references Child, Child references Parent
   - Use weakref to break the cycle

Expected Output:
----------------
Strong reference: Object still exists
Weak reference after del: Object was garbage collected

WeakValueDictionary cache:
Cache hit: Large data object
After deleting strong ref: Cache miss (garbage collected)

Observable with weak observers:
Notifying 2 observers
Observer deleted, notifying 1 observer

=== CONCEPTS TO LEARN ===
- weakref.ref() creates a weak reference
- weakref.WeakValueDictionary, WeakKeyDictionary
- weakref.WeakSet for sets of objects
- Finalize for cleanup callbacks

=== STARTER CODE ===
"""

import weakref
import gc

# Write your solution below this line
# -----------------------------------



# Test your solution
# ------------------
# Demonstrate weak references and garbage collection
