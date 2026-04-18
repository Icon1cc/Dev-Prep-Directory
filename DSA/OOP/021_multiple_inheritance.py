"""
Problem 021: Multiple Inheritance Basics

Difficulty: Intermediate
Topic: Multiple Inheritance

=== PROBLEM DESCRIPTION ===

Python supports multiple inheritance - a class can inherit from multiple
parent classes. The child class gets attributes and methods from all parents.

Your Task:
-----------
1. Create class `Flyable`:
   - Method `fly()` returns "Flying high!"

2. Create class `Swimmable`:
   - Method `swim()` returns "Swimming deep!"

3. Create class `Duck` that inherits from BOTH Flyable and Swimmable:
   - `__init__` accepts `name`
   - Method `quack()` returns "Quack!"

4. Create a Duck and demonstrate it can fly, swim, AND quack

Expected Output:
----------------
Donald can: Flying high!
Donald can: Swimming deep!
Donald says: Quack!

=== CONCEPTS TO LEARN ===
- Syntax: class Child(Parent1, Parent2):
- Child inherits from all parents
- Order matters for method resolution (more on this later)
- Be cautious: multiple inheritance can get complex

=== STARTER CODE ===
"""

# Write your solution below this line
# -----------------------------------



# Test your solution
# ------------------
# duck = Duck("Donald")
# print(f"{duck.name} can: {duck.fly()}")
# print(f"{duck.name} can: {duck.swim()}")
# print(f"{duck.name} says: {duck.quack()}")
