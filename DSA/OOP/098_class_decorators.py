"""
Problem 098: Class Decorators

Difficulty: Advanced
Topic: Metaprogramming

=== PROBLEM DESCRIPTION ===

Class decorators modify or enhance classes at definition time. They're a
powerful alternative to metaclasses for many use cases.

Your Task:
-----------
1. Create a @singleton decorator:
   - Ensures only one instance of decorated class exists

2. Create a @frozen decorator:
   - Makes class instances immutable after creation
   - Raises error on attribute modification

3. Create a @auto_repr decorator:
   - Automatically generates __repr__ from __init__ parameters
   - Inspects function signature

4. Create a @traced decorator:
   - Logs all method calls with arguments and return values
   - Useful for debugging

5. Create a @deprecated decorator:
   - Marks class as deprecated
   - Warns on instantiation

6. Create a @register decorator factory:
   - @register('plugins') adds class to 'plugins' registry
   - Support multiple registries

Expected Output:
----------------
@singleton:
a = SingletonClass()
b = SingletonClass()
a is b: True

@frozen:
obj = FrozenClass(x=1, y=2)
obj.x = 3  # Raises FrozenError!

@auto_repr:
Point(1, 2) -> 'Point(x=1, y=2)'

@traced:
obj.method(1, 2)
  TRACE: method(1, 2) -> 3

@deprecated:
OldClass()  # Warning: OldClass is deprecated, use NewClass

@register('handlers'):
Available handlers: ['JsonHandler', 'XmlHandler']

=== CONCEPTS TO LEARN ===
- Class decorators receive class and return class
- Can modify class attributes, add methods
- Decorator factories for parameterized decorators
- Alternative to metaclasses

=== STARTER CODE ===
"""

import functools
import warnings
from typing import Any

# Write your solution below this line
# -----------------------------------



# Test your solution
# ------------------
# Demonstrate each class decorator
