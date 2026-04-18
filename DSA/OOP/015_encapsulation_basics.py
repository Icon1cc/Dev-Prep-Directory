"""
Problem 015: Encapsulation - Public and Private Attributes

Difficulty: Beginner-Intermediate
Topic: Encapsulation

=== PROBLEM DESCRIPTION ===

Encapsulation is about hiding internal details and controlling access to data.
In Python:
- Public attributes: accessible from anywhere (normal attributes)
- Protected attributes: prefix with single underscore (_attr) - convention only
- Private attributes: prefix with double underscore (__attr) - name mangled

Your Task:
-----------
1. Create a class `BankAccount`:
   - `owner` - public attribute (anyone can access)
   - `_balance` - protected attribute (convention: internal use)
   - `__pin` - private attribute (harder to access from outside)

2. `__init__` accepts owner, initial_balance, and pin

3. Add methods:
   - `get_balance()` - returns _balance
   - `verify_pin(pin)` - returns True if pin matches __pin
   - `change_pin(old_pin, new_pin)` - changes pin if old_pin is correct

4. Demonstrate accessing public vs private attributes

Expected Output:
----------------
Owner: Alice
Balance via method: 1000
Direct _balance access: 1000
Attempting __pin access raises AttributeError
PIN verification: True

=== CONCEPTS TO LEARN ===
- Python doesn't have true private attributes (unlike Java/C++)
- Single underscore is a convention meaning "internal use"
- Double underscore triggers "name mangling" (_ClassName__attr)
- Use getter/setter methods to control access to sensitive data

=== STARTER CODE ===
"""

# Write your solution below this line
# -----------------------------------



# Test your solution
# ------------------
# account = BankAccount("Alice", 1000, "1234")
# print(f"Owner: {account.owner}")
# print(f"Balance via method: {account.get_balance()}")
# print(f"Direct _balance access: {account._balance}")
#
# try:
#     print(account.__pin)  # This will fail!
# except AttributeError:
#     print("Attempting __pin access raises AttributeError")
#
# print(f"PIN verification: {account.verify_pin('1234')}")
