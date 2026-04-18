"""
Problem 060: SOLID Principles - Open/Closed Principle

Difficulty: Intermediate
Topic: Design Principles

=== PROBLEM DESCRIPTION ===

The Open/Closed Principle (OCP) states that classes should be:
- OPEN for extension (can add new behavior)
- CLOSED for modification (don't change existing code)

Achieve this through abstraction and polymorphism.

Your Task:
-----------
1. BEFORE (Bad Design) - Create a `DiscountCalculator` class:
   - Has if/elif chain for different customer types
   - Adding new customer type requires modifying the class

2. AFTER (Good Design) - Refactor using strategy pattern:
   - `DiscountStrategy` ABC with `calculate(price)` method
   - `RegularCustomerDiscount` - 0% discount
   - `PremiumCustomerDiscount` - 10% discount
   - `VIPCustomerDiscount` - 20% discount
   - `DiscountCalculator` takes a strategy and calculates

3. Demonstrate adding a new discount type WITHOUT modifying existing code

Expected Output:
----------------
Bad design: Adding new customer type requires modifying DiscountCalculator

Good design:
Regular price: $100.00, After discount: $100.00
Premium price: $100.00, After discount: $90.00
VIP price: $100.00, After discount: $80.00

Adding new type (Employee - 15% off) without modifying existing code:
Employee price: $100.00, After discount: $85.00

=== CONCEPTS TO LEARN ===
- Extend behavior through new classes, not modifications
- Use abstraction (ABC) to define extension points
- Strategy pattern enables OCP
- Makes code more maintainable and testable

=== STARTER CODE ===
"""

from abc import ABC, abstractmethod

# Write your solution below this line
# -----------------------------------

# BAD DESIGN - Violates OCP


# GOOD DESIGN - Open for extension, closed for modification



# Test your solution
# ------------------
# print("Bad design: Adding new customer type requires modifying DiscountCalculator")
# print("\nGood design:")
#
# price = 100.00
#
# calc_regular = DiscountCalculator(RegularCustomerDiscount())
# calc_premium = DiscountCalculator(PremiumCustomerDiscount())
# calc_vip = DiscountCalculator(VIPCustomerDiscount())
#
# print(f"Regular price: ${price:.2f}, After discount: ${calc_regular.calculate(price):.2f}")
# print(f"Premium price: ${price:.2f}, After discount: ${calc_premium.calculate(price):.2f}")
# print(f"VIP price: ${price:.2f}, After discount: ${calc_vip.calculate(price):.2f}")
#
# print("\nAdding new type (Employee - 15% off) without modifying existing code:")
#
# class EmployeeDiscount(DiscountStrategy):
#     def calculate(self, price):
#         return price * 0.85
#
# calc_employee = DiscountCalculator(EmployeeDiscount())
# print(f"Employee price: ${price:.2f}, After discount: ${calc_employee.calculate(price):.2f}")
