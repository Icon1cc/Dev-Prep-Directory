"""
Problem 059: SOLID Principles - Single Responsibility Principle

Difficulty: Intermediate
Topic: Design Principles

=== PROBLEM DESCRIPTION ===

The Single Responsibility Principle (SRP) states that a class should have
only ONE reason to change. Each class should do ONE thing well.

Your Task:
-----------
1. BEFORE (Bad Design) - Create a `User` class that does everything:
   - Stores user data (name, email)
   - Validates email
   - Saves to database
   - Sends email notifications
   - Generates reports
   This violates SRP!

2. AFTER (Good Design) - Refactor into separate classes:
   - `User` - only stores user data
   - `EmailValidator` - validates email format
   - `UserRepository` - handles database operations
   - `EmailService` - sends email notifications
   - `UserReportGenerator` - generates user reports

3. Show how the refactored code is easier to test and maintain

Expected Output:
----------------
Bad design: User class has 5 responsibilities - hard to test/maintain!

Good design:
- User: stores data
- EmailValidator: validates email format
- UserRepository: saves/loads users
- EmailService: sends emails
- UserReportGenerator: generates reports

Each class can be tested independently!

=== CONCEPTS TO LEARN ===
- One class = One responsibility
- Easier to test, maintain, and understand
- Changes to one feature don't affect others
- Foundation for clean architecture

=== STARTER CODE ===
"""

import re

# Write your solution below this line
# -----------------------------------

# BAD DESIGN - Violates SRP (for demonstration)


# GOOD DESIGN - Each class has single responsibility



# Test your solution
# ------------------
# # Bad design (demonstration only - don't do this!)
# print("Bad design: User class has 5 responsibilities - hard to test/maintain!")
#
# print("\nGood design:")
#
# # Each class does one thing
# validator = EmailValidator()
# print(f"- EmailValidator: {validator.is_valid('test@email.com')}")
#
# user = User("Alice", "alice@email.com")
# print(f"- User: stores data - {user.name}, {user.email}")
#
# repo = UserRepository()
# repo.save(user)
# print(f"- UserRepository: saves/loads users")
#
# email_service = EmailService()
# email_service.send(user.email, "Welcome!")
# print(f"- EmailService: sends emails")
#
# report_gen = UserReportGenerator()
# print(f"- UserReportGenerator: generates reports")
#
# print("\nEach class can be tested independently!")
