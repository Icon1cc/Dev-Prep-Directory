"""
Problem 001: Create Your First Class

Difficulty: Beginner
Topic: Class Basics

=== PROBLEM DESCRIPTION ===

A class is a blueprint for creating objects. Think of it like a template
that defines what attributes (data) and methods (functions) an object will have.

Your Task:
-----------
1. Create a class called `Dog` with NO attributes or methods (use `pass`)
2. Create an instance (object) of the Dog class called `my_dog`
3. Print the type of `my_dog` to verify it's a Dog object

Expected Output:
----------------
<class '__main__.Dog'>

=== CONCEPTS TO LEARN ===
- The `class` keyword is used to define a class
- Class names should use PascalCase (e.g., MyClass, DogBreed)
- Creating an instance is called "instantiation"
- Use `pass` as a placeholder when a class has no content yet

=== STARTER CODE ===
"""

# Write your solution below this line
# -----------------------------------

class Dog:
    pass

my_dog = Dog()


# Test your solution
# ------------------
# Uncomment the following lines to test:
print(type(my_dog))
