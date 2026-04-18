"""
Problem 003: Adding Methods to a Class

Difficulty: Beginner
Topic: Instance Methods

=== PROBLEM DESCRIPTION ===

Methods are functions defined inside a class. Instance methods can access
and modify the object's attributes using `self`.

Your Task:
-----------
1. Create a class called `Rectangle`
2. The `__init__` method should accept `width` and `height` parameters
3. Add a method called `area()` that returns the area (width * height)
4. Add a method called `perimeter()` that returns the perimeter (2 * (width + height))
5. Create a Rectangle with width=5 and height=3
6. Print its area and perimeter

Expected Output:
----------------
Area: 15
Perimeter: 16

=== CONCEPTS TO LEARN ===
- Instance methods always take `self` as their first parameter
- Methods can access instance attributes via `self.attribute_name`
- Methods can return values just like regular functions
- Call methods using dot notation: object.method()

=== STARTER CODE ===
"""

# Write your solution below this line
# -----------------------------------

class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)


# Test your solution
# ------------------
rect = Rectangle(5, 3)
print(f"Area: {rect.area()}")
print(f"Perimeter: {rect.perimeter()}")
