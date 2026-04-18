"""
Problem 010: Building a Shopping Cart Class

Difficulty: Beginner
Topic: Working with Collections in Classes

=== PROBLEM DESCRIPTION ===

Classes often contain collections (lists, dictionaries) as attributes.
Let's build a shopping cart that manages a list of items.

Your Task:
-----------
1. Create a class called `ShoppingCart`
2. `__init__` should initialize an empty list called `items`
3. Add method `add_item(name, price, quantity=1)`:
   - Add item as a dictionary: {"name": name, "price": price, "quantity": quantity}
4. Add method `remove_item(name)`:
   - Remove item with matching name (if it exists)
5. Add method `get_total()`:
   - Return sum of (price * quantity) for all items
6. Add method `display_cart()`:
   - Print each item and the total

Expected Output:
----------------
Shopping Cart:
- Apple x2: $1.00
- Banana x3: $0.50
- Orange x1: $0.75
Total: $4.25

=== CONCEPTS TO LEARN ===
- Using lists and dictionaries as instance attributes
- Be careful: always initialize mutable objects in __init__, not as class attributes!
- Iterating over collections within methods

=== STARTER CODE ===
"""

# Write your solution below this line
# -----------------------------------



# Test your solution
# ------------------
# cart = ShoppingCart()
# cart.add_item("Apple", 0.50, 2)
# cart.add_item("Banana", 0.50, 3)
# cart.add_item("Orange", 0.75)
# cart.display_cart()
