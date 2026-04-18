"""
Problem 016: Property Decorators - Getters

Difficulty: Intermediate
Topic: Properties

=== PROBLEM DESCRIPTION ===

The @property decorator allows you to define methods that can be accessed
like attributes. This provides a clean interface while maintaining control
over how values are retrieved.

Your Task:
-----------
1. Create a class `Circle`:
   - `__init__` accepts `radius`

2. Create a @property called `diameter`:
   - Returns radius * 2

3. Create a @property called `area`:
   - Returns pi * radius^2 (use math.pi)

4. Create a @property called `circumference`:
   - Returns 2 * pi * radius

5. Access these properties WITHOUT parentheses (like attributes)

Expected Output:
----------------
Radius: 5
Diameter: 10
Area: 78.54
Circumference: 31.42

=== CONCEPTS TO LEARN ===
- @property decorator turns a method into a "getter"
- Access it like an attribute (circle.area, not circle.area())
- Computed properties can depend on other attributes
- Provides clean API while encapsulating computation

=== STARTER CODE ===
"""

import math

# Write your solution below this line
# -----------------------------------



# Test your solution
# ------------------
# circle = Circle(5)
# print(f"Radius: {circle.radius}")
# print(f"Diameter: {circle.diameter}")
# print(f"Area: {circle.area:.2f}")
# print(f"Circumference: {circle.circumference:.2f}")
