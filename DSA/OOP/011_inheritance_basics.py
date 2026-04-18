"""
Problem 011: Introduction to Inheritance

Difficulty: Beginner
Topic: Inheritance Basics

=== PROBLEM DESCRIPTION ===

Inheritance allows a class (child) to inherit attributes and methods from
another class (parent). This promotes code reuse and establishes "is-a"
relationships (e.g., a Dog IS an Animal).

Your Task:
-----------
1. Create a parent class called `Animal`:
   - `__init__` accepts `name` and `species`
   - Add method `make_sound()` that returns "Some generic sound"
   - Add method `info()` that returns "Name: X, Species: Y"

2. Create a child class called `Dog` that inherits from `Animal`:
   - Use the syntax: class Dog(Animal):
   - For now, just use `pass` (it inherits everything from Animal)

3. Create a Dog with name="Buddy" and species="Canine"
4. Call both info() and make_sound() on the Dog

Expected Output:
----------------
Name: Buddy, Species: Canine
Some generic sound

=== CONCEPTS TO LEARN ===
- Use `class Child(Parent):` syntax for inheritance
- Child classes automatically get all parent's attributes and methods
- The child class is also called "subclass" or "derived class"
- The parent class is also called "superclass" or "base class"

=== STARTER CODE ===
"""

# Write your solution below this line
# -----------------------------------



# Test your solution
# ------------------
# dog = Dog("Buddy", "Canine")
# print(dog.info())
# print(dog.make_sound())
