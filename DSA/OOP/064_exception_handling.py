"""
Problem 064: Exception Handling in OOP

Difficulty: Intermediate
Topic: Error Handling

=== PROBLEM DESCRIPTION ===

Good OOP design includes proper exception handling. This involves:
- Creating custom exception classes
- Using exception hierarchies
- Raising exceptions at appropriate times
- Handling exceptions gracefully

Your Task:
-----------
1. Create a custom exception hierarchy:
   - `BankError(Exception)` - base exception for all bank errors
   - `InsufficientFundsError(BankError)` - not enough balance
   - `InvalidAmountError(BankError)` - negative or zero amount
   - `AccountNotFoundError(BankError)` - account doesn't exist
   - `AccountLockedError(BankError)` - account is locked

2. Create a `BankAccount` class that uses these exceptions:
   - `__init__(account_id, balance, is_locked=False)`
   - `deposit(amount)` - raises InvalidAmountError if amount <= 0
   - `withdraw(amount)` - raises appropriate exceptions
   - `transfer(amount, target_account)` - handle multiple error cases

3. Create a `Bank` class:
   - `accounts` dict of account_id -> BankAccount
   - `get_account(account_id)` - raises AccountNotFoundError
   - `transfer(from_id, to_id, amount)` - handles all exceptions

Expected Output:
----------------
Deposit $100 to account-1: Success, balance = $600
Withdraw $1000: InsufficientFundsError - Balance $600 insufficient for $1000
Withdraw $-50: InvalidAmountError - Amount must be positive
Access locked account: AccountLockedError - Account is locked
Transfer from unknown: AccountNotFoundError - Account 'unknown' not found

All bank errors caught:
- InsufficientFundsError
- InvalidAmountError
- AccountLockedError
- AccountNotFoundError

=== CONCEPTS TO LEARN ===
- Custom exceptions communicate specific error conditions
- Exception hierarchies allow catching groups of related errors
- Include relevant information in exception messages
- Always validate inputs and raise appropriate exceptions

=== STARTER CODE ===
"""

# Write your solution below this line
# -----------------------------------

# Custom exception hierarchy


# BankAccount class


# Bank class



# Test your solution
# ------------------
# Demonstrate various exception scenarios
