"""
Problem 040: Strategy Design Pattern

Difficulty: Intermediate
Topic: Design Patterns

=== PROBLEM DESCRIPTION ===

The Strategy pattern defines a family of algorithms, encapsulates each one,
and makes them interchangeable. The algorithm can be selected at runtime.
Think: different sorting algorithms, payment methods, compression strategies.

Your Task:
-----------
1. Create an ABC `PaymentStrategy`:
   - Abstract method `pay(amount)` -> bool

2. Create concrete strategies:
   - `CreditCardPayment(card_number)` - validates card, processes payment
   - `PayPalPayment(email)` - logs into PayPal, processes payment
   - `CryptoPayment(wallet_address)` - sends crypto, processes payment

3. Create `ShoppingCart`:
   - `items` list with methods `add_item(item, price)`
   - `get_total()` returns sum of prices
   - `checkout(payment_strategy)` uses the strategy to pay

4. Demonstrate switching payment strategies at runtime

Expected Output:
----------------
Cart total: $150.00
Paying $150.00 using Credit Card ending in 1234
Payment successful!

Switching to PayPal...
Paying $150.00 via PayPal account user@email.com
Payment successful!

=== CONCEPTS TO LEARN ===
- Strategies are interchangeable algorithms
- Context (ShoppingCart) doesn't know which strategy it's using
- Easy to add new strategies without modifying existing code
- Follows Open/Closed Principle

=== STARTER CODE ===
"""

from abc import ABC, abstractmethod

# Write your solution below this line
# -----------------------------------



# Test your solution
# ------------------
# cart = ShoppingCart()
# cart.add_item("Laptop", 100.00)
# cart.add_item("Mouse", 50.00)
#
# print(f"Cart total: ${cart.get_total():.2f}")
#
# # Pay with credit card
# cc_payment = CreditCardPayment("4111-1111-1111-1234")
# cart.checkout(cc_payment)
#
# print("\nSwitching to PayPal...")
# paypal_payment = PayPalPayment("user@email.com")
# cart.checkout(paypal_payment)
