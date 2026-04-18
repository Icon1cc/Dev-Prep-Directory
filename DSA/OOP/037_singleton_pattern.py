"""
Problem 037: Singleton Design Pattern

Difficulty: Intermediate
Topic: Design Patterns

=== PROBLEM DESCRIPTION ===

The Singleton pattern ensures a class has only ONE instance and provides a
global access point to it. Common uses: database connections, configuration
managers, logging.

Your Task:
-----------
1. Implement Singleton using __new__ method:
   - Create class `DatabaseConnection`
   - Override `__new__` to return existing instance if one exists
   - Store the single instance as a class attribute

2. Implement Singleton using a decorator:
   - Create a `singleton` decorator function
   - Apply it to any class to make it a singleton

3. Implement Singleton using metaclass (advanced):
   - Create `SingletonMeta` metaclass
   - Classes using this metaclass become singletons

Expected Output:
----------------
Method 1 - __new__:
Same instance: True

Method 2 - Decorator:
Same instance: True

Method 3 - Metaclass:
Same instance: True

=== CONCEPTS TO LEARN ===
- Singleton ensures only one instance exists
- Multiple ways to implement: __new__, decorator, metaclass
- __new__ is called before __init__ and actually creates the object
- Be careful: singletons can make testing harder

=== STARTER CODE ===
"""

# Write your solution below this line
# -----------------------------------

# Method 1: Using __new__


# Method 2: Using a decorator


# Method 3: Using a metaclass



# Test your solution
# ------------------
# print("Method 1 - __new__:")
# db1 = DatabaseConnection()
# db2 = DatabaseConnection()
# print(f"Same instance: {db1 is db2}")
#
# print("\nMethod 2 - Decorator:")
# @singleton
# class Logger:
#     pass
# log1 = Logger()
# log2 = Logger()
# print(f"Same instance: {log1 is log2}")
#
# print("\nMethod 3 - Metaclass:")
# class Config(metaclass=SingletonMeta):
#     pass
# cfg1 = Config()
# cfg2 = Config()
# print(f"Same instance: {cfg1 is cfg2}")
