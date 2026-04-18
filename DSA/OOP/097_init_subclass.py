"""
Problem 097: __init_subclass__ for Class Registration

Difficulty: Advanced
Topic: Modern Python Features

=== PROBLEM DESCRIPTION ===

Python 3.6+ provides __init_subclass__ as a simpler alternative to metaclasses
for customizing subclass creation. It's called whenever a class is subclassed.

Your Task:
-----------
1. Create a plugin registration system:
   - Base class `Plugin` with __init_subclass__
   - Subclasses are automatically registered
   - No metaclass needed!

2. Create a serialization system:
   - Base class `Serializable`
   - __init_subclass__ validates required methods exist
   - Auto-generates serializers

3. Create a validation system:
   - __init_subclass__ enforces that subclasses define certain attributes
   - Raise error at class definition time if missing

4. Pass arguments to __init_subclass__:
   - class MyPlugin(Plugin, register=True, priority=10)
   - Handle keyword arguments in __init_subclass__

5. Combine with class decorators:
   - Show equivalence and when to use each

Expected Output:
----------------
Plugin Registration:
class AudioPlugin(Plugin): ...  # Auto-registered!
class VideoPlugin(Plugin): ...  # Auto-registered!

Available plugins: ['AudioPlugin', 'VideoPlugin']

Validation:
class ValidModel(Model):
    table_name = 'users'  # Required attribute

class InvalidModel(Model):  # Raises error!
    pass  # Missing table_name

Error: InvalidModel must define 'table_name'

With arguments:
class HighPriorityPlugin(Plugin, priority=10):
    pass

HighPriorityPlugin.priority = 10

=== CONCEPTS TO LEARN ===
- __init_subclass__(cls, **kwargs) called on subclassing
- Simpler than metaclasses for many use cases
- Can validate and modify subclasses
- Supports keyword arguments

=== STARTER CODE ===
"""

# Write your solution below this line
# -----------------------------------



# Test your solution
# ------------------
# Demonstrate __init_subclass__ use cases
