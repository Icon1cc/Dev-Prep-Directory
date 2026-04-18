"""
Problem 009: Building a Simple Bank Account Class

Difficulty: Beginner
Topic: Practical Class Design

=== PROBLEM DESCRIPTION ===

Let's put together what we've learned to build a practical class.
A BankAccount class should manage deposits, withdrawals, and balance tracking.

Your Task:
-----------
1. Create a class called `BankAccount`
2. `__init__` should accept:
   - `owner` (account holder's name)
   - `balance` (optional, default=0)
3. Add method `deposit(amount)`:
   - Add amount to balance
   - Print confirmation message
4. Add method `withdraw(amount)`:
   - If sufficient funds: subtract amount and print confirmation
   - If insufficient funds: print "Insufficient funds!" and don't change balance
5. Add method `get_balance()` that returns current balance
6. Implement `__str__` to show "Account owner: X, Balance: $Y"

Expected Output:
----------------
Account owner: Alice, Balance: $100
Deposited $50. New balance: $150
Withdrew $30. New balance: $120
Insufficient funds!
Final balance: $120

=== CONCEPTS TO LEARN ===
- Combining multiple concepts into a cohesive class
- Adding validation logic in methods
- Maintaining object state through method calls

=== STARTER CODE ===
"""

# Write your solution below this line
# -----------------------------------



# Test your solution
# ------------------
# account = BankAccount("Alice", 100)
# print(account)
# account.deposit(50)
# account.withdraw(30)
# account.withdraw(200)  # Should fail
# print(f"Final balance: ${account.get_balance()}")
