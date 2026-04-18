"""
Problem 014: isinstance() and issubclass() Functions

Difficulty: Beginner
Topic: Type Checking

=== PROBLEM DESCRIPTION ===

Python provides built-in functions to check object types and class relationships:
- isinstance(obj, class): Is this object an instance of this class?
- issubclass(class1, class2): Is class1 a subclass of class2?

Your Task:
-----------
1. Create class hierarchy:
   - `Animal` (parent)
   - `Dog(Animal)` (child)
   - `Cat(Animal)` (child)

2. Create instances: dog1 = Dog(), cat1 = Cat()

3. Use isinstance() to check:
   - Is dog1 a Dog? (True)
   - Is dog1 an Animal? (True - inheritance!)
   - Is dog1 a Cat? (False)

4. Use issubclass() to check:
   - Is Dog a subclass of Animal? (True)
   - Is Cat a subclass of Animal? (True)
   - Is Dog a subclass of Cat? (False)

Expected Output:
----------------
isinstance checks:
dog1 is Dog: True
dog1 is Animal: True
dog1 is Cat: False

issubclass checks:
Dog is subclass of Animal: True
Cat is subclass of Animal: True
Dog is subclass of Cat: False

=== CONCEPTS TO LEARN ===
- isinstance() checks the object's type and its parent types
- issubclass() checks class hierarchy relationships
- Useful for type validation and polymorphic code

=== STARTER CODE ===
"""

# Write your solution below this line
# -----------------------------------



# Test your solution
# ------------------
# (Write your own tests based on the expected output)
