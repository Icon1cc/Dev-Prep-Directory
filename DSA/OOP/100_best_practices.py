"""
Problem 100: OOP Best Practices and Code Review

Difficulty: Advanced
Topic: Best Practices Summary

=== PROBLEM DESCRIPTION ===

This final problem summarizes OOP best practices. You'll review code and
identify issues, then refactor to follow best practices.

Your Task:
-----------
1. Review and fix code violating OOP principles:
   - Identify SRP, OCP, LSP, ISP, DIP violations
   - Refactor to follow SOLID principles

2. Review naming conventions:
   - Classes: PascalCase
   - Methods/attributes: snake_case
   - Constants: UPPER_CASE
   - Private: _single_underscore
   - Name mangling: __double_underscore

3. Review common anti-patterns:
   - God class (does too much)
   - Anemic domain model (no behavior, just data)
   - Circular dependencies
   - Deep inheritance hierarchies

4. Review documentation:
   - Docstrings for classes and methods
   - Type hints
   - When comments are necessary

5. Create a "code review checklist":
   - SOLID principles
   - DRY (Don't Repeat Yourself)
   - KISS (Keep It Simple, Stupid)
   - YAGNI (You Aren't Gonna Need It)

=== BAD CODE TO REVIEW ===
"""

# --- BAD CODE START ---
# Review this code and identify all issues

class user:  # Bad: lowercase class name
    all_users = []  # Bad: mutable class attribute

    def __init__(self, n, e, p):  # Bad: unclear parameter names
        self.n = n  # Bad: unclear attribute names
        self.e = e
        self.p = p
        user.all_users.append(self)

    def send_email(self, subject, body):  # Bad: SRP violation
        # User shouldn't know how to send emails
        print(f"Sending email to {self.e}")

    def save_to_db(self):  # Bad: SRP violation
        # User shouldn't know about database
        print(f"INSERT INTO users VALUES ({self.n}, {self.e})")

    def validate(self):  # Bad: SRP violation
        if '@' not in self.e:
            return False
        return True

class admin(user):  # Bad: lowercase, poor naming
    def delete_user(self, user):
        user.all_users.remove(user)  # Bad: accessing internals


# --- BAD CODE END ---


# --- GOOD CODE START ---
# Write your refactored version below
"""

Your Task:
-----------
Refactor the bad code above to follow best practices:

1. Proper naming conventions
2. Single Responsibility Principle
3. Dependency Injection
4. Proper encapsulation
5. Clear documentation

Expected Structure:
------------------
- User class (just user data)
- EmailService class (handles emails)
- UserRepository class (handles persistence)
- UserValidator class (handles validation)
- Admin class (proper inheritance or composition)

Expected Output:
----------------
CODE REVIEW CHECKLIST:

[x] Naming: Classes use PascalCase
[x] Naming: Methods use snake_case
[x] SOLID: Single Responsibility
[x] SOLID: Dependency Injection used
[x] DRY: No code duplication
[x] Encapsulation: Private attributes protected
[x] Documentation: Docstrings present
[x] Types: Type hints used

Refactored code demo:
User 'Alice' created
Email sent to alice@email.com
User saved to database

=== STARTER CODE FOR REFACTORED VERSION ===
"""

from abc import ABC, abstractmethod
from typing import Optional, List

# Write your refactored solution below this line
# -----------------------------------



# Test your solution
# ------------------
# Demonstrate the properly designed classes
