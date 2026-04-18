"""
Problem 076: Proxy Design Pattern

Difficulty: Intermediate-Advanced
Topic: Structural Design Pattern

=== PROBLEM DESCRIPTION ===

The Proxy pattern provides a surrogate or placeholder for another object
to control access to it. Types of proxies:
- Virtual Proxy: Lazy initialization of expensive objects
- Protection Proxy: Access control
- Remote Proxy: Local representative for remote object
- Logging Proxy: Adds logging to method calls

Your Task:
-----------
1. Create a `Image` interface (ABC):
   - `display()` - show the image

2. Create `RealImage`:
   - Expensive to create (simulates loading from disk)
   - `__init__(filename)` loads image data

3. Create `ProxyImage` (Virtual Proxy):
   - Doesn't load until display() is called (lazy loading)
   - Creates RealImage only when needed

4. Create `ProtectionProxy`:
   - Controls access based on user role
   - Only admin can delete, anyone can view

5. Create `LoggingProxy`:
   - Wraps any object and logs all method calls
   - Records timestamp and arguments

Expected Output:
----------------
Virtual Proxy:
Creating ProxyImage (no loading yet)
First display() - loading now...
  Loading image from photo.jpg
  Displaying photo.jpg
Second display() - already loaded
  Displaying photo.jpg

Protection Proxy:
User 'admin' viewing document: Success
User 'guest' viewing document: Success
User 'admin' deleting document: Success
User 'guest' deleting document: Access denied!

Logging Proxy:
[2024-03-18 10:30:00] Called add(2, 3) -> 5
[2024-03-18 10:30:00] Called multiply(4, 5) -> 20

=== CONCEPTS TO LEARN ===
- Proxy has same interface as real object
- Controls access/adds behavior without changing real object
- Lazy loading saves resources
- Protection proxies add security

=== STARTER CODE ===
"""

from abc import ABC, abstractmethod
from datetime import datetime

# Write your solution below this line
# -----------------------------------



# Test your solution
# ------------------
# Demonstrate each type of proxy
