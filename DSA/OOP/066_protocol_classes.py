"""
Problem 066: Protocol Classes (Structural Subtyping)

Difficulty: Advanced
Topic: Modern Python OOP (Python 3.8+)

=== PROBLEM DESCRIPTION ===

Protocol classes enable structural subtyping (duck typing with type hints).
A class doesn't need to explicitly inherit from a Protocol - it just needs
to have the required methods/attributes.

Your Task:
-----------
1. Create a `Drawable` Protocol:
   - Defines `draw(self) -> str` method
   - Any class with a `draw` method is considered Drawable

2. Create classes that "implement" Drawable (without inheriting):
   - `Circle` with `draw()` returning "Drawing a circle"
   - `Rectangle` with `draw()` returning "Drawing a rectangle"
   - `Text` with `draw()` returning "Drawing text: {content}"

3. Create a function `render(items: list[Drawable]) -> None`:
   - Calls draw() on each item
   - Works with any class that has draw() method

4. Create a `Comparable` Protocol:
   - Defines `__lt__(self, other) -> bool`
   - Use with sorting functions

5. Create a `SupportsClose` Protocol:
   - Defines `close(self) -> None`
   - Useful for context managers

Expected Output:
----------------
Rendering items:
Drawing a circle
Drawing a rectangle
Drawing text: Hello, World!

Sorting comparable items:
[Score(60), Score(75), Score(90)]

File implements SupportsClose: True
String implements SupportsClose: False

=== CONCEPTS TO LEARN ===
- Protocol = structural subtyping (duck typing)
- No inheritance required - just method signatures
- @runtime_checkable allows isinstance() checks
- More flexible than ABCs
- from typing import Protocol (Python 3.8+)

=== STARTER CODE ===
"""

from typing import Protocol, runtime_checkable

# Write your solution below this line
# -----------------------------------



# Test your solution
# ------------------
# Demonstrate Protocol-based type checking
