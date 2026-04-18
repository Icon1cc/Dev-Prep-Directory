"""
Problem 036: Mixins - Reusable Functionality

Difficulty: Intermediate-Advanced
Topic: Design Patterns

=== PROBLEM DESCRIPTION ===

Mixins are small classes that provide specific functionality to be "mixed in"
to other classes. They're not meant to stand alone - they add capabilities
to existing classes through multiple inheritance.

Your Task:
-----------
1. Create mixin `JsonMixin`:
   - Method `to_json()` returns JSON representation of __dict__
   - Method `from_json(json_str)` creates instance from JSON (classmethod)

2. Create mixin `ComparableMixin`:
   - Requires subclass to have a `comparison_key` property
   - Implements __lt__, __le__, __gt__, __ge__, __eq__ using comparison_key

3. Create mixin `LoggingMixin`:
   - Method `log(message)` prints timestamped message with class name

4. Create class `Product` that uses all three mixins:
   - Attributes: name, price, quantity
   - comparison_key returns price (for sorting by price)

Expected Output:
----------------
JSON: {"name": "Widget", "price": 25.0, "quantity": 100}
From JSON: Widget ($25.0)
Cheaper: Widget ($25.0)
[2024-01-15 10:30:00] Product: Item created

=== CONCEPTS TO LEARN ===
- Mixins add reusable functionality without deep inheritance
- Keep mixins focused on ONE capability
- Naming convention: suffix with "Mixin"
- Place mixins before the main class in inheritance list

=== STARTER CODE ===
"""

import json
from datetime import datetime

# Write your solution below this line
# -----------------------------------



# Test your solution
# ------------------
# p1 = Product("Widget", 25.0, 100)
# p2 = Product("Gadget", 50.0, 50)
#
# # JsonMixin test
# print(f"JSON: {p1.to_json()}")
# p3 = Product.from_json('{"name": "Widget", "price": 25.0, "quantity": 100}')
# print(f"From JSON: {p3.name} (${p3.price})")
#
# # ComparableMixin test
# cheaper = p1 if p1 < p2 else p2
# print(f"Cheaper: {cheaper.name} (${cheaper.price})")
#
# # LoggingMixin test
# p1.log("Item created")
