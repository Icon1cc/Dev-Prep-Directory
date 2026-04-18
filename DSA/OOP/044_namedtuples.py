"""
Problem 044: Named Tuples - Lightweight Classes

Difficulty: Intermediate
Topic: Immutable Data Structures

=== PROBLEM DESCRIPTION ===

Named tuples are immutable, lightweight classes. They're like regular tuples
but with named fields. Great for simple data containers that shouldn't change.

Your Task:
-----------
1. Create a named tuple `Point` using collections.namedtuple:
   - Fields: x, y
   - Access by name (point.x) or index (point[0])

2. Create a named tuple `Person` with defaults using typing.NamedTuple:
   - Fields: name, age, city (default="Unknown")
   - This is the modern, type-hinted approach

3. Create a named tuple `RGB` for colors:
   - Fields: red, green, blue (all integers 0-255)
   - Add a method `to_hex()` that returns hex color code
   - (Yes, you can add methods to named tuples!)

4. Demonstrate immutability - trying to modify raises error

Expected Output:
----------------
Point: Point(x=3, y=4)
Access by name: 3, Access by index: 4

Person: Person(name='Alice', age=30, city='Unknown')

RGB(255, 128, 0) as hex: #ff8000

Trying to modify namedtuple...
Error: can't set attribute

=== CONCEPTS TO LEARN ===
- Named tuples are immutable
- Memory efficient (no __dict__)
- Can use _replace() to create modified copies
- _asdict() converts to dictionary
- _fields shows field names

=== STARTER CODE ===
"""

from collections import namedtuple
from typing import NamedTuple

# Write your solution below this line
# -----------------------------------



# Test your solution
# ------------------
# # Basic namedtuple
# p = Point(3, 4)
# print(f"Point: {p}")
# print(f"Access by name: {p.x}, Access by index: {p[0]}")
#
# print()
#
# # NamedTuple with defaults
# person = Person("Alice", 30)
# print(f"Person: {person}")
#
# print()
#
# # RGB with method
# color = RGB(255, 128, 0)
# print(f"{color} as hex: {color.to_hex()}")
#
# print()
#
# # Immutability
# print("Trying to modify namedtuple...")
# try:
#     p.x = 10
# except AttributeError as e:
#     print(f"Error: {e}")
