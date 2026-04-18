"""
Problem 099: functools for OOP

Difficulty: Intermediate
Topic: Standard Library

=== PROBLEM DESCRIPTION ===

The functools module provides tools that are extremely useful in OOP:
@total_ordering, @cached_property, @singledispatch, and more.

Your Task:
-----------
1. Use @functools.total_ordering:
   - Only implement __eq__ and __lt__
   - Get __le__, __gt__, __ge__ automatically

2. Use @functools.cached_property:
   - Property computed once and cached
   - Useful for expensive computations

3. Use @functools.singledispatch:
   - Generic function that dispatches based on first argument type
   - Like method overloading in other languages

4. Use @functools.lru_cache with methods:
   - Cache method results
   - Be careful with self reference!

5. Use functools.partial:
   - Create specialized versions of methods
   - Partial application of arguments

Expected Output:
----------------
@total_ordering:
Version(1, 2) < Version(1, 3): True
Version(1, 2) <= Version(1, 2): True
Version(1, 2) > Version(1, 1): True
(All from just __eq__ and __lt__!)

@cached_property:
First access: Computing expensive value... 42
Second access: 42 (cached, instant!)

@singledispatch:
process(42) -> "Processing integer: 42"
process("hello") -> "Processing string: HELLO"
process([1, 2, 3]) -> "Processing list of 3 items"

@lru_cache with method:
fib(100) = 354224848179261915075 (computed once, cached)
fib(100) = 354224848179261915075 (from cache, instant)

functools.partial:
multiply_by_2 = partial(multiply, 2)
multiply_by_2(5) = 10

=== CONCEPTS TO LEARN ===
- total_ordering reduces boilerplate
- cached_property for lazy, cached attributes
- singledispatch for type-based dispatch
- lru_cache for memoization
- partial for partial function application

=== STARTER CODE ===
"""

import functools
from functools import total_ordering, cached_property, singledispatch, lru_cache, partial

# Write your solution below this line
# -----------------------------------



# Test your solution
# ------------------
# Demonstrate each functools feature
