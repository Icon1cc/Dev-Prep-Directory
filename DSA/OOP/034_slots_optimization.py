"""
Problem 034: __slots__ for Memory Optimization

Difficulty: Advanced
Topic: Memory Optimization

=== PROBLEM DESCRIPTION ===

By default, Python stores instance attributes in a dictionary (__dict__).
Using __slots__ tells Python to use a more compact internal representation,
which can save memory for many instances.

Your Task:
-----------
1. Create class `PointWithDict` (normal class):
   - `__init__(x, y)` - stores x and y
   - Has __dict__ (can add attributes dynamically)

2. Create class `PointWithSlots`:
   - Define `__slots__ = ['x', 'y']`
   - `__init__(x, y)` - stores x and y
   - NO __dict__ (cannot add new attributes)

3. Create 100,000 instances of each and compare:
   - Memory usage (using sys.getsizeof on the objects)
   - Try adding a new attribute `z` to both (one will fail)

Expected Output:
----------------
PointWithDict: Can add new attributes dynamically
PointWithDict has __dict__: True

PointWithSlots: Cannot add new attributes
PointWithSlots has __dict__: False
Error adding attribute: 'PointWithSlots' object has no attribute 'z'

Memory comparison (approximate):
PointWithDict instance: ~56 bytes + ~112 bytes for __dict__
PointWithSlots instance: ~56 bytes (no __dict__)

=== CONCEPTS TO LEARN ===
- __slots__ prevents __dict__ creation, saving ~100 bytes per instance
- Cannot add attributes not listed in __slots__
- Useful for classes with many instances (millions of objects)
- __slots__ is inherited but needs to be empty in subclasses

=== STARTER CODE ===
"""

import sys

# Write your solution below this line
# -----------------------------------



# Test your solution
# ------------------
# # Test PointWithDict
# p1 = PointWithDict(3, 4)
# p1.z = 5  # Can add new attribute
# print("PointWithDict: Can add new attributes dynamically")
# print(f"PointWithDict has __dict__: {hasattr(p1, '__dict__')}")
#
# print()
#
# # Test PointWithSlots
# p2 = PointWithSlots(3, 4)
# print("PointWithSlots: Cannot add new attributes")
# print(f"PointWithSlots has __dict__: {hasattr(p2, '__dict__')}")
# try:
#     p2.z = 5  # This will fail!
# except AttributeError as e:
#     print(f"Error adding attribute: {e}")
#
# print("\nMemory comparison (approximate):")
# print(f"PointWithDict instance: {sys.getsizeof(p1)} bytes + {sys.getsizeof(p1.__dict__)} bytes for __dict__")
# print(f"PointWithSlots instance: {sys.getsizeof(p2)} bytes (no __dict__)")
