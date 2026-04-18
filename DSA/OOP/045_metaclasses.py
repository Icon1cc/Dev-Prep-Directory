"""
Problem 045: Metaclasses - Classes of Classes

Difficulty: Advanced
Topic: Metaclasses

=== PROBLEM DESCRIPTION ===

A metaclass is a class whose instances are classes. Just as objects are
instances of classes, classes are instances of metaclasses. By default,
all classes use `type` as their metaclass.

Your Task:
-----------
1. Understand the basics:
   - type('MyClass', (), {}) creates a class dynamically
   - Explore: type(object), type(type)

2. Create a metaclass `AutoMethodMeta`:
   - Automatically adds a `describe()` method to all classes
   - The method returns "I am a {ClassName} object"

3. Create a metaclass `SingletonMeta`:
   - Ensures only one instance of the class exists
   - (This is another way to implement Singleton!)

4. Create a metaclass `ValidatorMeta`:
   - Checks that all classes have required methods
   - Raise error if a required method is missing

Expected Output:
----------------
Creating class dynamically with type:
<class '__main__.DynamicClass'>

AutoMethodMeta:
I am a Dog object
I am a Cat object

SingletonMeta:
Same instance: True

ValidatorMeta:
Error: Class MissingMethod must implement: process

=== CONCEPTS TO LEARN ===
- Metaclasses customize class creation
- __new__ creates the class, __init__ initializes it
- __call__ controls instance creation
- Use sparingly - "if you're not sure if you need them, you don't"

=== STARTER CODE ===
"""

# Write your solution below this line
# -----------------------------------



# Test your solution
# ------------------
# # Dynamic class creation
# print("Creating class dynamically with type:")
# DynamicClass = type('DynamicClass', (), {'value': 42})
# print(type(DynamicClass))
#
# print("\nAutoMethodMeta:")
# class Dog(metaclass=AutoMethodMeta):
#     pass
# class Cat(metaclass=AutoMethodMeta):
#     pass
# print(Dog().describe())
# print(Cat().describe())
#
# print("\nSingletonMeta:")
# class Database(metaclass=SingletonMeta):
#     pass
# db1 = Database()
# db2 = Database()
# print(f"Same instance: {db1 is db2}")
#
# print("\nValidatorMeta:")
# try:
#     class MissingMethod(metaclass=ValidatorMeta):
#         required_methods = ['process']
#         pass  # Missing process method!
# except TypeError as e:
#     print(f"Error: {e}")
