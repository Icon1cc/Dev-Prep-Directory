"""
Problem 091: Unit Testing OOP Code

Difficulty: Intermediate
Topic: Testing Best Practices

=== PROBLEM DESCRIPTION ===

Learn how to properly test object-oriented code using unittest and pytest.
Testing is crucial for interview preparation and real-world development.

Your Task:
-----------
1. Create a `Calculator` class to test:
   - `add(a, b)`, `subtract(a, b)`, `multiply(a, b)`, `divide(a, b)`
   - `divide` raises ZeroDivisionError for zero divisor

2. Write unittest.TestCase tests:
   - `test_add` - test addition with various inputs
   - `test_subtract` - test subtraction
   - `test_divide_by_zero` - test exception is raised
   - Use setUp() for test fixtures

3. Create a `BankAccount` class and test it:
   - Test deposit, withdraw, transfer
   - Test insufficient funds exception
   - Test multiple accounts interacting

4. Learn mocking:
   - Mock external dependencies
   - Use unittest.mock.Mock, patch
   - Test a class that depends on API/database

5. Test coverage concepts:
   - Line coverage
   - Branch coverage
   - Test edge cases

Expected Output:
----------------
Running tests...

test_add_positive_numbers ... ok
test_add_negative_numbers ... ok
test_subtract ... ok
test_multiply ... ok
test_divide ... ok
test_divide_by_zero ... ok
test_deposit ... ok
test_withdraw ... ok
test_insufficient_funds ... ok
test_transfer ... ok
test_api_call_mocked ... ok

----------------------------------------------------------------------
Ran 11 tests in 0.003s

OK

=== CONCEPTS TO LEARN ===
- unittest framework basics
- Test class inherits from unittest.TestCase
- setUp/tearDown for fixtures
- Assertions: assertEqual, assertTrue, assertRaises
- Mocking external dependencies

=== STARTER CODE ===
"""

import unittest
from unittest.mock import Mock, patch

# Write your solution below this line
# -----------------------------------

# Classes to test


# Test classes



# Run tests
# ------------------
# if __name__ == '__main__':
#     unittest.main()
