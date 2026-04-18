"""
Problem 082: Implementing a Plugin System

Difficulty: Advanced
Topic: Real-world Application

=== PROBLEM DESCRIPTION ===

Build a plugin system that allows dynamically loading and registering
plugins at runtime. This demonstrates metaclasses, ABCs, and registry patterns.

Your Task:
-----------
1. Create a `Plugin` ABC:
   - `name` property (abstract)
   - `version` property (abstract)
   - `activate()` method
   - `deactivate()` method
   - `execute(data)` abstract method

2. Create a `PluginRegistry` (using metaclass or decorator):
   - Automatically registers all Plugin subclasses
   - `get_plugin(name)` - returns plugin class
   - `list_plugins()` - returns all registered plugins

3. Create a `PluginManager`:
   - `load_plugin(name)` - instantiate and activate plugin
   - `unload_plugin(name)` - deactivate and remove
   - `execute_all(data)` - run all active plugins

4. Create sample plugins:
   - `LoggingPlugin` - logs all data
   - `ValidationPlugin` - validates data format
   - `TransformPlugin` - transforms data (uppercase, etc.)

Expected Output:
----------------
Available plugins:
- LoggingPlugin (v1.0)
- ValidationPlugin (v1.0)
- TransformPlugin (v2.0)

Loading plugins...
LoggingPlugin activated
ValidationPlugin activated

Processing data: {'message': 'hello world'}
[LOG] Processing: {'message': 'hello world'}
[VALID] Data is valid
Result: {'message': 'hello world', 'valid': True}

Loading TransformPlugin...
Result: {'message': 'HELLO WORLD', 'valid': True, 'transformed': True}

=== CONCEPTS TO LEARN ===
- Auto-registration using metaclass or __init_subclass__
- Plugin architecture for extensibility
- Dynamic loading and configuration
- Separation of core and extensions

=== STARTER CODE ===
"""

from abc import ABC, abstractmethod

# Write your solution below this line
# -----------------------------------



# Test your solution
# ------------------
# Demonstrate the plugin system
