"""
Problem 065: Type Hints and Static Type Checking

Difficulty: Intermediate
Topic: Modern Python OOP

=== PROBLEM DESCRIPTION ===

Type hints improve code readability and enable static type checking with
tools like mypy. They don't affect runtime but help catch errors early.

Your Task:
-----------
1. Create a type-hinted `User` class:
   - Attributes: name (str), email (str), age (int), is_active (bool)
   - Method type hints for parameters and return values

2. Create a type-hinted `UserManager` class:
   - `users: dict[str, User]` - maps email to User
   - `add_user(user: User) -> None`
   - `get_user(email: str) -> User | None`
   - `get_active_users() -> list[User]`
   - `get_users_by_age(min_age: int, max_age: int) -> list[User]`

3. Use advanced type hints:
   - `Optional[T]` for nullable values
   - `Union[A, B]` for multiple types
   - `Callable[[args], return]` for function types
   - `TypeVar` for generic types
   - `Generic[T]` for generic classes

4. Create a generic `Repository[T]` class:
   - Works with any entity type
   - `add(item: T) -> None`
   - `get(id: str) -> T | None`
   - `get_all() -> list[T]`

Expected Output:
----------------
User: Alice (alice@email.com), age 30, active: True
Active users: ['Alice', 'Charlie']
Users aged 25-35: ['Alice', 'Bob']

Generic Repository:
Added User: Alice
Added Product: Laptop
All users: [User('Alice')]
All products: [Product('Laptop')]

=== CONCEPTS TO LEARN ===
- Type hints: str, int, list[T], dict[K, V]
- Optional[T] = T | None
- Callable for function types
- TypeVar and Generic for generic programming
- Run mypy for static type checking

=== STARTER CODE ===
"""

from typing import TypeVar, Generic, Callable, Optional, Any
from dataclasses import dataclass

# Write your solution below this line
# -----------------------------------



# Test your solution
# ------------------
# Demonstrate type-hinted classes
