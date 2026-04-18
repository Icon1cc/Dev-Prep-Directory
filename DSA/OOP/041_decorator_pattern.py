"""
Problem 041: Decorator Design Pattern (not Python decorators)

Difficulty: Intermediate-Advanced
Topic: Design Patterns

=== PROBLEM DESCRIPTION ===

The Decorator pattern attaches additional responsibilities to objects dynamically.
It provides a flexible alternative to subclassing for extending functionality.
Note: This is different from Python's @decorator syntax!

Your Task:
-----------
1. Create a base `Coffee` class:
   - `cost()` returns base price (2.00)
   - `description()` returns "Simple Coffee"

2. Create a `CoffeeDecorator` base class:
   - Takes a coffee object in __init__
   - Delegates cost() and description() to wrapped coffee

3. Create concrete decorators:
   - `MilkDecorator` - adds $0.50, adds "with Milk" to description
   - `SugarDecorator` - adds $0.25, adds "with Sugar"
   - `WhipDecorator` - adds $0.75, adds "with Whipped Cream"

4. Decorators can be stacked: coffee with milk, sugar, and whip

Expected Output:
----------------
Simple Coffee: $2.00
Coffee with Milk: $2.50
Coffee with Milk with Sugar: $2.75
Coffee with Milk with Sugar with Whipped Cream: $3.50

=== CONCEPTS TO LEARN ===
- Decorators wrap objects and add behavior
- Each decorator IS-A Coffee (same interface)
- Can be stacked infinitely
- Alternative to explosion of subclasses (CoffeeWithMilk, CoffeeWithMilkAndSugar, etc.)

=== STARTER CODE ===
"""

from abc import ABC, abstractmethod

# Write your solution below this line
# -----------------------------------



# Test your solution
# ------------------
# # Simple coffee
# coffee = Coffee()
# print(f"{coffee.description()}: ${coffee.cost():.2f}")
#
# # Add milk
# coffee_with_milk = MilkDecorator(Coffee())
# print(f"{coffee_with_milk.description()}: ${coffee_with_milk.cost():.2f}")
#
# # Add milk and sugar
# coffee_milk_sugar = SugarDecorator(MilkDecorator(Coffee()))
# print(f"{coffee_milk_sugar.description()}: ${coffee_milk_sugar.cost():.2f}")
#
# # Add everything!
# fancy_coffee = WhipDecorator(SugarDecorator(MilkDecorator(Coffee())))
# print(f"{fancy_coffee.description()}: ${fancy_coffee.cost():.2f}")
