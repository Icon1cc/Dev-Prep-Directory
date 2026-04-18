"""
Problem 019: Static Methods with @staticmethod

Difficulty: Intermediate
Topic: Static Methods

=== PROBLEM DESCRIPTION ===

Static methods don't receive any automatic first argument (no self, no cls).
They're essentially regular functions that live inside a class for organizational
purposes. Use them for utility functions related to the class.

Your Task:
-----------
1. Create a class `MathUtils`:
   - This class will contain math-related utility functions
   - No __init__ needed (we won't create instances)

2. Add static methods:
   - `is_prime(n)`: Returns True if n is prime, False otherwise
   - `factorial(n)`: Returns n! (factorial of n)
   - `gcd(a, b)`: Returns greatest common divisor using Euclidean algorithm
   - `lcm(a, b)`: Returns least common multiple (a * b // gcd(a, b))

3. Call these methods directly on the class (no instance needed)

Expected Output:
----------------
Is 17 prime? True
Is 18 prime? False
5! = 120
GCD(48, 18) = 6
LCM(4, 6) = 12

=== CONCEPTS TO LEARN ===
- @staticmethod decorator defines a static method
- No self or cls parameter
- Called on the class: MathUtils.is_prime(17)
- Used for utility functions that don't need instance/class data

=== STARTER CODE ===
"""

# Write your solution below this line
# -----------------------------------



# Test your solution
# ------------------
# print(f"Is 17 prime? {MathUtils.is_prime(17)}")
# print(f"Is 18 prime? {MathUtils.is_prime(18)}")
# print(f"5! = {MathUtils.factorial(5)}")
# print(f"GCD(48, 18) = {MathUtils.gcd(48, 18)}")
# print(f"LCM(4, 6) = {MathUtils.lcm(4, 6)}")
