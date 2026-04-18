"""
Problem 061: SOLID Principles - Liskov Substitution Principle

Difficulty: Intermediate-Advanced
Topic: Design Principles

=== PROBLEM DESCRIPTION ===

The Liskov Substitution Principle (LSP) states that objects of a superclass
should be replaceable with objects of subclasses without breaking the program.

"If S is a subtype of T, then objects of type T may be replaced with objects
of type S without altering any desirable property of the program."

Your Task:
-----------
1. BEFORE (Bad Design) - Classic Rectangle/Square problem:
   - `Rectangle` with width and height setters
   - `Square` inherits from Rectangle but breaks when width != height
   - This violates LSP!

2. AFTER (Good Design) - Proper hierarchy:
   - `Shape` ABC with `area()` method
   - `Rectangle` and `Square` both extend Shape independently
   - OR use composition instead of inheritance

3. Demonstrate another LSP violation:
   - `Bird` class with `fly()` method
   - `Penguin` extends Bird but can't fly!
   - Fix with proper abstraction

Expected Output:
----------------
BAD: Rectangle/Square hierarchy
Rectangle area: 20 (width=4, height=5)
Setting square width to 4, height to 5...
Square area: 25 (both became 5!) - LSP VIOLATED!

GOOD: Separate shapes
Rectangle area: 20
Square area: 25

BAD: Bird/Penguin hierarchy
Sparrow flies!
Penguin... raises exception - LSP VIOLATED!

GOOD: Proper bird hierarchy
Sparrow can fly!
Penguin can swim!

=== CONCEPTS TO LEARN ===
- Subclasses must honor parent's contract
- Don't inherit just to reuse code
- "Is-a" relationship must be behavioral, not just structural
- Prefer composition over inheritance when in doubt

=== STARTER CODE ===
"""

from abc import ABC, abstractmethod

# Write your solution below this line
# -----------------------------------

# BAD: Rectangle/Square (LSP violation)


# GOOD: Separate shapes


# BAD: Bird/Penguin (LSP violation)


# GOOD: Proper bird hierarchy



# Test your solution
# ------------------
# Print demonstrations as shown in expected output
