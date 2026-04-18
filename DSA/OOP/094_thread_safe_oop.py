"""
Problem 094: Thread-Safe OOP

Difficulty: Advanced
Topic: Concurrency

=== PROBLEM DESCRIPTION ===

Learn how to write thread-safe classes that can be used in multi-threaded
applications without data corruption.

Your Task:
-----------
1. Create a thread-safe `Counter`:
   - Use threading.Lock to protect increment/decrement
   - Demonstrate race condition without lock
   - Show correct behavior with lock

2. Create a thread-safe `BankAccount`:
   - `deposit()` and `withdraw()` are atomic
   - `transfer()` between accounts (need both locks - careful of deadlock!)
   - Use RLock for reentrant locking

3. Create a thread-safe `Singleton`:
   - Double-checked locking pattern
   - Ensure only one instance even with concurrent creation

4. Create a `ThreadSafeQueue`:
   - Producer-consumer pattern
   - Use Condition for wait/notify
   - Bounded buffer with blocking put/get

5. Demonstrate thread-safe property access:
   - Atomic reads and writes
   - Using @property with locks

Expected Output:
----------------
Race condition demo (without lock):
Expected: 100000, Got: 87234 (WRONG!)

With lock:
Expected: 100000, Got: 100000 (CORRECT!)

Thread-safe transfer:
Account A: $1000, Account B: $1000
10 threads transferring...
Account A: $1000, Account B: $1000 (total preserved!)

Thread-safe Singleton:
100 threads creating singleton...
All got same instance: True

Producer-Consumer:
Producer: Produced 10 items
Consumer: Consumed 10 items

=== CONCEPTS TO LEARN ===
- threading.Lock for mutual exclusion
- threading.RLock for reentrant locking
- threading.Condition for coordination
- Avoiding deadlocks (lock ordering)
- Thread-safe lazy initialization

=== STARTER CODE ===
"""

import threading
import time
from typing import Any

# Write your solution below this line
# -----------------------------------



# Test your solution
# ------------------
# Demonstrate thread safety scenarios
