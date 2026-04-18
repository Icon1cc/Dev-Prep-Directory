"""
Problem 063: SOLID Principles - Dependency Inversion Principle

Difficulty: Intermediate-Advanced
Topic: Design Principles

=== PROBLEM DESCRIPTION ===

The Dependency Inversion Principle (DIP) states:
- High-level modules should not depend on low-level modules
- Both should depend on abstractions
- Abstractions should not depend on details
- Details should depend on abstractions

Your Task:
-----------
1. BEFORE (Bad Design) - Direct dependency:
   - `NotificationService` directly creates `EmailSender`
   - Cannot switch to SMS without modifying NotificationService
   - Hard to test (can't mock EmailSender)

2. AFTER (Good Design) - Dependency injection:
   - `MessageSender` ABC with `send(message, recipient)` method
   - `EmailSender`, `SMSSender`, `PushSender` implement MessageSender
   - `NotificationService` takes MessageSender in constructor
   - Easy to switch implementations and test

3. Show dependency injection patterns:
   - Constructor injection (most common)
   - Setter injection
   - Interface injection

Expected Output:
----------------
BAD: NotificationService directly depends on EmailSender
Cannot switch sender without modifying NotificationService

GOOD: NotificationService depends on MessageSender abstraction
With EmailSender: Sending EMAIL to user@example.com: Hello!
With SMSSender: Sending SMS to +1234567890: Hello!
With PushSender: Sending PUSH to device_123: Hello!

Testing with MockSender:
Message 'Test message' sent to 'test_user' (mocked)

=== CONCEPTS TO LEARN ===
- Depend on abstractions, not concrete implementations
- Inject dependencies through constructor
- Makes code testable (can inject mocks)
- Enables flexible configuration

=== STARTER CODE ===
"""

from abc import ABC, abstractmethod

# Write your solution below this line
# -----------------------------------

# BAD: Direct dependency


# GOOD: Dependency inversion with abstraction



# Test your solution
# ------------------
# Demonstrate bad vs good design as shown in expected output
