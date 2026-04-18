"""
Problem 023: Polymorphism - Same Interface, Different Behavior

Difficulty: Intermediate
Topic: Polymorphism

=== PROBLEM DESCRIPTION ===

Polymorphism means "many forms". It allows objects of different classes to be
treated uniformly through a common interface. Each class implements the interface
in its own way.

Your Task:
-----------
1. Create a base class `Shape`:
   - Method `area()` raises NotImplementedError
   - Method `perimeter()` raises NotImplementedError

2. Create `Rectangle(Shape)`:
   - `__init__(width, height)`
   - Implement area() and perimeter()

3. Create `Circle(Shape)`:
   - `__init__(radius)`
   - Implement area() and perimeter()

4. Create `Triangle(Shape)`:
   - `__init__(a, b, c)` - three sides
   - Implement area() using Heron's formula
   - Implement perimeter()

5. Create a function `print_shape_info(shape)` that works with ANY shape
   - Prints the area and perimeter

Expected Output:
----------------
Rectangle: Area = 20, Perimeter = 18
Circle: Area = 78.54, Perimeter = 31.42
Triangle: Area = 6.00, Perimeter = 12

=== CONCEPTS TO LEARN ===
- Polymorphism: same method name, different implementations
- Duck typing: "If it walks like a duck and quacks like a duck..."
- The function doesn't care about the type, just that it has area() and perimeter()
- NotImplementedError signals that subclasses MUST override the method

=== STARTER CODE ===
"""

import math

# Write your solution below this line
# -----------------------------------



# Test your solution
# ------------------
# shapes = [
#     Rectangle(4, 5),
#     Circle(5),
#     Triangle(3, 4, 5)
# ]
#
# for shape in shapes:
#     print_shape_info(shape)
