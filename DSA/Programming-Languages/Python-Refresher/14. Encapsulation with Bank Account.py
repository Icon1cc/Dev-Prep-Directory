"""
Description: Create a BankAccount class that demonstrates encapsulation.
The constructor __init__ should accept an initial_balance and store it in a "private" attribute (e.g., _balance).
Create a public method get_balance() that returns the current balance.
Create a public method deposit(amount) that adds to the balance.
Create a public method withdraw(amount) that subtracts from the balance but only if amount is not greater than the current balance. If funds are insufficient, it should print an error message and not alter the balance.
"""

class BankAccount:
    def __init__(self, initial_balance):
        self._balance = initial_balance  # private attribute

    def get_balance(self):
        return self._balance

    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
        else:
            print("Deposit amount must be positive")

    def withdraw(self, amount):
        if amount <= self._balance:
            self._balance -= amount
        else:
            print("Insufficient funds")

initial_balance = float(input("Enter initial balance: "))
account = BankAccount(initial_balance)  
print("Current Balance:", account.get_balance())
deposit_amount = float(input("Enter amount to deposit: "))
account.deposit(deposit_amount)
print("Balance after deposit:", account.get_balance())
withdraw_amount = float(input("Enter amount to withdraw: "))
account.withdraw(withdraw_amount)
print("Balance after withdrawal:", account.get_balance())
