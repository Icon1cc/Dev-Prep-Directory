"""
Problem 048: Implementing a Custom Iterator

Difficulty: Intermediate
Topic: Iterator Protocol

=== PROBLEM DESCRIPTION ===

The iterator protocol requires two methods:
- __iter__: Returns the iterator object (usually self)
- __next__: Returns the next value, raises StopIteration when done

Your Task:
-----------
1. Create a `CountDown` iterator:
   - __init__(start) - starts from this number
   - Counts down to 0
   - Each __next__ returns current value and decrements

2. Create a `Fibonacci` iterator:
   - __init__(limit) - maximum number of values to generate
   - Generates Fibonacci sequence: 0, 1, 1, 2, 3, 5, 8, ...

3. Create a `Range` iterator (simplified version of built-in):
   - __init__(start, stop, step=1)
   - Generates values from start to stop (exclusive)

Expected Output:
----------------
Countdown: 5, 4, 3, 2, 1, 0

First 10 Fibonacci: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34

Range(0, 10, 2): 0, 2, 4, 6, 8

=== CONCEPTS TO LEARN ===
- __iter__ returns an iterator (object with __next__)
- __next__ returns values until StopIteration
- Iterators can only go forward, not backward
- Can be used in for loops, list(), etc.

=== STARTER CODE ===
"""

# Write your solution below this line
# -----------------------------------



# Test your solution
# ------------------
# print("Countdown:", ", ".join(str(x) for x in CountDown(5)))
#
# print("\nFirst 10 Fibonacci:", ", ".join(str(x) for x in Fibonacci(10)))
#
# print("\nRange(0, 10, 2):", ", ".join(str(x) for x in Range(0, 10, 2)))
