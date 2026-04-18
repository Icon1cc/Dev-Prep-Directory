"""
Problem 096: Duck Typing and EAFP

Difficulty: Intermediate
Topic: Python Philosophy

=== PROBLEM DESCRIPTION ===

Python follows "duck typing" - if it walks like a duck and quacks like a duck,
it's a duck. Also learn EAFP (Easier to Ask for Forgiveness than Permission)
vs LBYL (Look Before You Leap).

Your Task:
-----------
1. Demonstrate duck typing:
   - Function that works with ANY object that has required methods
   - No inheritance or interface required

2. Compare EAFP vs LBYL:
   - LBYL: Check conditions before acting
   - EAFP: Try and handle exceptions
   - Show when each is appropriate

3. Create a file-like object:
   - Implements read(), write(), close()
   - Works with code expecting file objects

4. Create a numeric-like object:
   - Implements __add__, __mul__, etc.
   - Works with code expecting numbers

5. Use hasattr/getattr carefully:
   - When to check vs try
   - Callable checking

Expected Output:
----------------
Duck Typing:
Making duck speak: Quack!
Making dog speak: Woof!
Making robot speak: Beep boop!
(All work because they have speak() method)

LBYL style:
if hasattr(obj, 'speak'):
    obj.speak()

EAFP style (preferred in Python):
try:
    obj.speak()
except AttributeError:
    print("Can't speak")

File-like object:
Writing 'Hello' to StringBuffer
Reading from StringBuffer: 'Hello'
Works with any code expecting file!

Numeric-like object:
Money(10) + Money(5) = Money(15)
Money(10) * 3 = Money(30)

=== CONCEPTS TO LEARN ===
- Duck typing: focus on behavior, not type
- EAFP: try/except is often better than checking first
- Protocols: objects just need right methods
- Python's flexibility vs static typing

=== STARTER CODE ===
"""

# Write your solution below this line
# -----------------------------------



# Test your solution
# ------------------
# Demonstrate duck typing and EAFP
