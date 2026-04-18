"""
Problem 031: The __call__ Method (Callable Objects)

Difficulty: Intermediate
Topic: Dunder Methods

=== PROBLEM DESCRIPTION ===

The `__call__` method makes an object callable like a function. This is useful
for objects that need to maintain state between calls, like counters or caches.

Your Task:
-----------
1. Create a class `Counter`:
   - `__init__(start=0)` - initializes count
   - `__call__()` - increments and returns the count
   - Each time you "call" the counter object, it increments

2. Create a class `Multiplier`:
   - `__init__(factor)` - stores the multiplication factor
   - `__call__(value)` - returns value * factor
   - Acts like a customized function

3. Create a class `CallTracker`:
   - `__init__(func)` - wraps any function
   - `__call__(*args, **kwargs)` - calls the function and tracks call count
   - Attribute `call_count` tracks number of times called

Expected Output:
----------------
Counter: 1, 2, 3
Double of 5: 10
Triple of 5: 15
add called 3 times

=== CONCEPTS TO LEARN ===
- __call__ makes instances callable with ()
- Useful for stateful functions, decorators, and function wrappers
- isinstance(obj, Callable) returns True for callable objects

=== STARTER CODE ===
"""

# Write your solution below this line
# -----------------------------------



# Test your solution
# ------------------
# # Counter example
# counter = Counter()
# print(f"Counter: {counter()}, {counter()}, {counter()}")
#
# # Multiplier example
# double = Multiplier(2)
# triple = Multiplier(3)
# print(f"Double of 5: {double(5)}")
# print(f"Triple of 5: {triple(5)}")
#
# # CallTracker example
# def add(a, b):
#     return a + b
#
# tracked_add = CallTracker(add)
# tracked_add(1, 2)
# tracked_add(3, 4)
# tracked_add(5, 6)
# print(f"add called {tracked_add.call_count} times")
