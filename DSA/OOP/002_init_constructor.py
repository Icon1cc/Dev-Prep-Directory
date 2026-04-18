"""
Problem 002: Class with Attributes using __init__

Difficulty: Beginner
Topic: Constructor Method (__init__)

=== PROBLEM DESCRIPTION ===

The `__init__` method is a special method called a "constructor". It runs
automatically when you create a new instance of a class. It's used to
initialize the object's attributes.

Your Task:
-----------
1. Create a class called `Person`
2. Define an `__init__` method that takes `name` and `age` as parameters
3. Store these as instance attributes using `self.name` and `self.age`
4. Create a Person instance with name="Alice" and age=25
5. Print the person's name and age

Expected Output:
----------------
Name: Alice
Age: 25

=== CONCEPTS TO LEARN ===
- `__init__` is the constructor method (double underscores = "dunder" method)
- `self` refers to the current instance being created
- `self.attribute_name` creates an instance attribute
- Instance attributes are unique to each object

=== STARTER CODE ===
"""

# Write your solution below this line
# -----------------------------------

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age


# Test your solution
# ------------------
person1 = Person("Alice", 25)
print(f"Name: {person1.name}")
print(f"Age: {person1.age}")
