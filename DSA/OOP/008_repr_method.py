"""
Problem 008: The __repr__ Method (Developer Representation)

Difficulty: Beginner
Topic: Magic/Dunder Methods

=== PROBLEM DESCRIPTION ===

While `__str__` is for end-users, `__repr__` is for developers.
It should return a string that could ideally recreate the object.
When `__str__` is not defined, Python falls back to `__repr__`.

Your Task:
-----------
1. Create a class called `Point`
2. The `__init__` should accept `x` and `y` coordinates
3. Implement `__repr__` to return "Point(x, y)" format
4. Implement `__str__` to return "(x, y)" format
5. Demonstrate the difference between str() and repr()

Expected Output:
----------------
str: (3, 5)
repr: Point(3, 5)

=== CONCEPTS TO LEARN ===
- `__repr__` is for debugging and development
- `__str__` is for user-friendly display
- If only `__repr__` is defined, it's used for both
- Convention: `__repr__` should look like valid Python code

=== STARTER CODE ===
"""

# Write your solution below this line
# -----------------------------------

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

    def __str__(self):
        return f"({self.x}, {self.y})"


# Test your solution
# ------------------
point = Point(3, 5)
print(f"str: {str(point)}")
print(f"repr: {repr(point)}")
