"""
Problem 028: Arithmetic Magic Methods (__add__, __sub__, etc.)

Difficulty: Intermediate
Topic: Operator Overloading

=== PROBLEM DESCRIPTION ===

You can make custom objects work with arithmetic operators by implementing:
- __add__: +
- __sub__: -
- __mul__: *
- __truediv__: /
- __floordiv__: //
- __mod__: %
- __pow__: **

Your Task:
-----------
1. Create a class `Vector` for 2D vectors:
   - `__init__(x, y)`
   - `__str__` returns "Vector(x, y)"

2. Implement arithmetic operations:
   - __add__: Add two vectors (x1+x2, y1+y2)
   - __sub__: Subtract two vectors (x1-x2, y1-y2)
   - __mul__: Scalar multiplication (x*scalar, y*scalar)
   - __truediv__: Scalar division
   - __neg__: Negation (-x, -y) using __neg__

3. Add a method `magnitude()` that returns the length: sqrt(x^2 + y^2)

Expected Output:
----------------
v1 = Vector(3, 4)
v2 = Vector(1, 2)
v1 + v2 = Vector(4, 6)
v1 - v2 = Vector(2, 2)
v1 * 2 = Vector(6, 8)
v1 / 2 = Vector(1.5, 2.0)
-v1 = Vector(-3, -4)
|v1| = 5.0

=== CONCEPTS TO LEARN ===
- Operators call these magic methods behind the scenes
- Return a NEW object, don't modify the original
- For commutative operations (3 * vector), also implement __rmul__

=== STARTER CODE ===
"""

import math

# Write your solution below this line
# -----------------------------------



# Test your solution
# ------------------
# v1 = Vector(3, 4)
# v2 = Vector(1, 2)
#
# print(f"v1 = {v1}")
# print(f"v2 = {v2}")
# print(f"v1 + v2 = {v1 + v2}")
# print(f"v1 - v2 = {v1 - v2}")
# print(f"v1 * 2 = {v1 * 2}")
# print(f"v1 / 2 = {v1 / 2}")
# print(f"-v1 = {-v1}")
# print(f"|v1| = {v1.magnitude()}")
