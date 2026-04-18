"""
Problem 049: Generators as Iterators

Difficulty: Intermediate
Topic: Generators

=== PROBLEM DESCRIPTION ===

Generators are a simpler way to create iterators. A function with `yield`
becomes a generator. Each yield pauses the function and returns a value.

Your Task:
-----------
1. Create a generator function `countdown(n)`:
   - Yields n, n-1, n-2, ..., 0

2. Create a generator function `fibonacci(limit)`:
   - Yields Fibonacci numbers (up to limit numbers)

3. Create a generator function `infinite_counter(start=0)`:
   - Yields infinite sequence: start, start+1, start+2, ...
   - Use itertools.islice to get first N values

4. Create a generator that reads a large file line by line:
   - `read_large_file(filepath)`
   - Memory efficient - doesn't load entire file

5. Create a generator expression (one-liner):
   - Squares of even numbers from 0-20

Expected Output:
----------------
Countdown: 5, 4, 3, 2, 1, 0
Fibonacci: 0, 1, 1, 2, 3, 5, 8, 13
First 5 from infinite: 10, 11, 12, 13, 14
Even squares: 0, 4, 16, 36, 64, 100, 144, 196, 256, 324, 400

=== CONCEPTS TO LEARN ===
- `yield` makes a function a generator
- Generators are lazy - compute values on demand
- Memory efficient for large data
- Generator expressions: (x**2 for x in range(10))

=== STARTER CODE ===
"""

from itertools import islice

# Write your solution below this line
# -----------------------------------



# Test your solution
# ------------------
# print("Countdown:", ", ".join(str(x) for x in countdown(5)))
# print("Fibonacci:", ", ".join(str(x) for x in fibonacci(8)))
# print("First 5 from infinite:", ", ".join(str(x) for x in islice(infinite_counter(10), 5)))
#
# # Generator expression
# even_squares = (x**2 for x in range(21) if x % 2 == 0)
# print("Even squares:", ", ".join(str(x) for x in even_squares))
