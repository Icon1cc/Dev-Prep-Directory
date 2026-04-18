"""
Problem 075: Chain of Responsibility Pattern

Difficulty: Intermediate-Advanced
Topic: Behavioral Design Pattern

=== PROBLEM DESCRIPTION ===

The Chain of Responsibility pattern passes a request along a chain of handlers.
Each handler either processes the request or passes it to the next handler.

Your Task:
-----------
1. Create a `Handler` ABC:
   - `set_next(handler)` - set next handler in chain
   - `handle(request)` - process or pass to next

2. Create a logging system with handlers:
   - `DebugHandler` - handles DEBUG level messages
   - `InfoHandler` - handles INFO level messages
   - `WarningHandler` - handles WARNING level messages
   - `ErrorHandler` - handles ERROR level messages
   - Each handler has a threshold and passes lower levels up the chain

3. Create an authentication chain:
   - `AuthenticationHandler` - verify credentials
   - `AuthorizationHandler` - check permissions
   - `ValidationHandler` - validate request data
   - `RateLimitHandler` - check rate limits

Expected Output:
----------------
Logging chain:
DEBUG: Detailed debugging info (handled by DebugHandler)
INFO: General information (handled by InfoHandler)
WARNING: Potential problem (handled by WarningHandler)
ERROR: Error occurred! (handled by ErrorHandler)

Authentication chain:
Request: /admin/users (user: admin)
  Auth: User authenticated
  Authz: User authorized for admin access
  Valid: Request validated
  Rate: Rate limit OK
Request processed successfully!

Request: /admin/users (user: guest)
  Auth: User authenticated
  Authz: DENIED - insufficient permissions
Request blocked by authorization

=== CONCEPTS TO LEARN ===
- Handlers form a chain, each can break or continue
- Request passes along until handled
- Decouples sender from receiver
- Easy to add/remove/reorder handlers

=== STARTER CODE ===
"""

from abc import ABC, abstractmethod

# Write your solution below this line
# -----------------------------------



# Test your solution
# ------------------
# Demonstrate both chains
