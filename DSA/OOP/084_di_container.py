"""
Problem 084: Implementing a Dependency Injection Container

Difficulty: Advanced
Topic: Real-world Application

=== PROBLEM DESCRIPTION ===

Build a DI (Dependency Injection) Container that manages object creation
and dependencies automatically. This is fundamental to modern frameworks.

Your Task:
-----------
1. Create a `Container` class:
   - `register(interface, implementation)` - register a class
   - `register_singleton(interface, implementation)` - single instance
   - `resolve(interface)` - create/return instance with dependencies
   - Auto-resolve constructor dependencies

2. Support different lifetimes:
   - `Transient` - new instance every time
   - `Singleton` - same instance always
   - `Scoped` - same instance within a scope

3. Support decorator registration:
   - `@container.injectable` - marks class for auto-registration
   - `@container.singleton` - marks as singleton

4. Implement auto-wiring:
   - Inspect __init__ type hints
   - Automatically inject required dependencies

Expected Output:
----------------
Registering services...
  UserRepository registered as singleton
  EmailService registered as transient
  UserService registered (depends on UserRepository, EmailService)

Resolving UserService...
  Creating UserRepository (singleton)
  Creating EmailService (transient)
  Creating UserService
  Injecting: UserRepository, EmailService

user_service.create_user('Alice'):
  Repository: Saving user Alice
  Email: Sending welcome email to alice@email.com

Resolving again...
  UserRepository (reusing singleton)
  Creating EmailService (new transient)

=== CONCEPTS TO LEARN ===
- Inversion of Control (IoC)
- Dependency Injection patterns
- Service lifetimes
- Type introspection for auto-wiring

=== STARTER CODE ===
"""

from typing import Type, TypeVar, get_type_hints
from enum import Enum

# Write your solution below this line
# -----------------------------------



# Test your solution
# ------------------
# Create container, register services, resolve dependencies
