"""
Problem 026: Magic Method __eq__ (Equality Comparison)

Difficulty: Intermediate
Topic: Dunder/Magic Methods

=== PROBLEM DESCRIPTION ===

The `__eq__` method defines how two objects are compared for equality using `==`.
By default, objects are compared by identity (memory address), not value.

Your Task:
-----------
1. Create a class `Point`:
   - `__init__(x, y)`

2. WITHOUT __eq__: Create two points with same coordinates, compare them
   - They will NOT be equal (different objects in memory)

3. Implement `__eq__(self, other)`:
   - Return True if both x and y coordinates match
   - Handle the case where `other` is not a Point

4. WITH __eq__: Same two points should now be equal

Expected Output:
----------------
Without __eq__:
p1 == p2: False (they're different objects)

With __eq__:
p1 == p2: True (same coordinates)
p1 == "not a point": False

=== CONCEPTS TO LEARN ===
- __eq__ is called when using == operator
- Should return True, False, or NotImplemented
- Always check if `other` is the right type
- If __eq__ is defined, you should also define __hash__ (or set it to None)

=== STARTER CODE ===
"""

# Write your solution below this line
# -----------------------------------

# First, create Point WITHOUT __eq__ to see default behavior


# Now create Point WITH __eq__



# Test your solution
# ------------------
# # Without __eq__
# class PointNoEq:
#     def __init__(self, x, y):
#         self.x = x
#         self.y = y
#
# p1 = PointNoEq(3, 4)
# p2 = PointNoEq(3, 4)
# print("Without __eq__:")
# print(f"p1 == p2: {p1 == p2} (they're different objects)")
#
# # With __eq__
# p1 = Point(3, 4)
# p2 = Point(3, 4)
# print("\nWith __eq__:")
# print(f"p1 == p2: {p1 == p2} (same coordinates)")
# print(f'p1 == "not a point": {p1 == "not a point"}')
