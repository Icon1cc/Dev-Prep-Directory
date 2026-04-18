"""
Problem 046: __getattr__ and __setattr__ - Attribute Access Control

Difficulty: Advanced
Topic: Dunder Methods

=== PROBLEM DESCRIPTION ===

Python provides methods to intercept attribute access:
- __getattr__: Called when attribute is NOT found normally
- __getattribute__: Called for EVERY attribute access (be careful!)
- __setattr__: Called for EVERY attribute assignment
- __delattr__: Called when deleting an attribute

Your Task:
-----------
1. Create a class `FlexibleObject`:
   - __getattr__ returns f"Attribute '{name}' not found, returning default"
   - This makes all attribute access "safe" (never raises AttributeError)

2. Create a class `LoggedObject`:
   - __setattr__ logs all attribute assignments
   - __getattribute__ logs all attribute accesses
   - Be careful to avoid infinite recursion!

3. Create a class `ImmutableObject`:
   - __setattr__ raises error after initialization
   - Only allows setting attributes in __init__

Expected Output:
----------------
FlexibleObject:
obj.name = Alice
obj.missing = Attribute 'missing' not found, returning default

LoggedObject:
Setting: name = Alice
Getting: name
Value: Alice

ImmutableObject:
Initial name: Alice
Error: Cannot modify immutable object

=== CONCEPTS TO LEARN ===
- Use object.__setattr__(self, name, value) to avoid recursion
- __getattr__ only called when attribute doesn't exist
- __getattribute__ called for EVERY access (including methods!)
- Great for proxies, lazy loading, logging

=== STARTER CODE ===
"""

# Write your solution below this line
# -----------------------------------



# Test your solution
# ------------------
# print("FlexibleObject:")
# obj = FlexibleObject()
# obj.name = "Alice"
# print(f"obj.name = {obj.name}")
# print(f"obj.missing = {obj.missing}")
#
# print("\nLoggedObject:")
# logged = LoggedObject()
# logged.name = "Alice"
# print(f"Value: {logged.name}")
#
# print("\nImmutableObject:")
# immutable = ImmutableObject(name="Alice")
# print(f"Initial name: {immutable.name}")
# try:
#     immutable.name = "Bob"
# except AttributeError as e:
#     print(f"Error: {e}")
