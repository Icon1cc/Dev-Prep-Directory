"""
Problem 032: Context Managers (__enter__ and __exit__)

Difficulty: Intermediate
Topic: Context Manager Protocol

=== PROBLEM DESCRIPTION ===

Context managers are used with the `with` statement to handle setup and cleanup.
They implement __enter__ (called at start) and __exit__ (called at end, even if
an exception occurs).

Your Task:
-----------
1. Create a class `Timer`:
   - `__enter__` - records start time, returns self
   - `__exit__` - calculates and prints elapsed time
   - Should work with: `with Timer() as t:`

2. Create a class `FileManager`:
   - `__init__(filename, mode)` - stores filename and mode
   - `__enter__` - opens file, returns file object
   - `__exit__` - closes file (even if exception occurred)
   - Handle exceptions gracefully

3. Create a class `DatabaseConnection` (simulated):
   - `__enter__` - prints "Connected", returns self
   - `__exit__` - prints "Disconnected"
   - Method `execute(query)` - prints the query

Expected Output:
----------------
Timer started
Doing some work...
Elapsed time: 0.10 seconds

File content written and file closed properly

Connected to database
Executing: SELECT * FROM users
Disconnected from database

=== CONCEPTS TO LEARN ===
- __enter__ is called when entering the `with` block
- __exit__ receives exception info (exc_type, exc_val, exc_tb)
- Return True from __exit__ to suppress exceptions
- Use contextlib.contextmanager for simpler context managers

=== STARTER CODE ===
"""

import time

# Write your solution below this line
# -----------------------------------



# Test your solution
# ------------------
# # Timer example
# with Timer():
#     print("Doing some work...")
#     time.sleep(0.1)
#
# print()
#
# # FileManager example (create a test file)
# with FileManager("test_context.txt", "w") as f:
#     f.write("Hello, Context Manager!")
# print("File content written and file closed properly")
#
# # Clean up test file
# import os
# os.remove("test_context.txt")
#
# print()
#
# # Database example
# with DatabaseConnection() as db:
#     db.execute("SELECT * FROM users")
