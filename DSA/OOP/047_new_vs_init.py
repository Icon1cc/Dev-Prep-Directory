"""
Problem 047: __new__ vs __init__ - Object Creation

Difficulty: Advanced
Topic: Object Lifecycle

=== PROBLEM DESCRIPTION ===

Understanding the difference between __new__ and __init__:
- __new__: Creates and returns a NEW instance (static method, takes cls)
- __init__: Initializes an EXISTING instance (takes self)

__new__ is rarely overridden except for:
- Immutable types (str, int, tuple) that can't be modified in __init__
- Singleton pattern
- Custom memory allocation

Your Task:
-----------
1. Create a class `ShowLifecycle`:
   - Override __new__ to print when called
   - Override __init__ to print when called
   - Observe the order of calls

2. Create an immutable `UpperStr` class (subclass of str):
   - Override __new__ to convert string to uppercase
   - Cannot use __init__ because str is immutable!

3. Create a `CachedObject` class:
   - __new__ checks if an object with same args already exists
   - Returns cached instance instead of creating new one

Expected Output:
----------------
Lifecycle:
__new__ called with cls=<class 'ShowLifecycle'>
__init__ called with self=<ShowLifecycle>

UpperStr:
UpperStr("hello") = HELLO

CachedObject:
Creating new object for: key1
Returning cached object for: key1
Same object: True

=== CONCEPTS TO LEARN ===
- __new__ creates, __init__ initializes
- __new__ must return an instance (or None)
- If __new__ returns wrong type, __init__ won't be called
- __new__ is useful for immutable types and object caching

=== STARTER CODE ===
"""

# Write your solution below this line
# -----------------------------------



# Test your solution
# ------------------
# print("Lifecycle:")
# obj = ShowLifecycle()
#
# print("\nUpperStr:")
# upper = UpperStr("hello")
# print(f'UpperStr("hello") = {upper}')
#
# print("\nCachedObject:")
# obj1 = CachedObject("key1")
# obj2 = CachedObject("key1")  # Should return cached
# print(f"Same object: {obj1 is obj2}")
