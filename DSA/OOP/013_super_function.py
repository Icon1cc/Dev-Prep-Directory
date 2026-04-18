"""
Problem 013: Using super() to Call Parent Methods

Difficulty: Beginner
Topic: The super() Function

=== PROBLEM DESCRIPTION ===

Sometimes you want to extend (not replace) a parent's method. Use `super()`
to call the parent's version, then add your own logic.

Your Task:
-----------
1. Create a parent class `Vehicle`:
   - `__init__` accepts `brand` and `model`
   - Stores them as instance attributes

2. Create a child class `Car(Vehicle)`:
   - `__init__` accepts `brand`, `model`, and `num_doors`
   - Use `super().__init__(brand, model)` to call parent's __init__
   - Then set `self.num_doors = num_doors`

3. Create a child class `Motorcycle(Vehicle)`:
   - `__init__` accepts `brand`, `model`, and `has_sidecar` (boolean)
   - Use super() to call parent's __init__
   - Then set the sidecar attribute

4. Add `__str__` method to each class showing all attributes

Expected Output:
----------------
Car: Toyota Camry with 4 doors
Motorcycle: Harley Davidson Sportster (sidecar: False)

=== CONCEPTS TO LEARN ===
- `super()` returns a temporary object of the parent class
- Use it to call parent methods without explicitly naming the parent
- Common pattern: call super().__init__() then add child-specific attributes
- This avoids code duplication

=== STARTER CODE ===
"""

# Write your solution below this line
# -----------------------------------



# Test your solution
# ------------------
# car = Car("Toyota", "Camry", 4)
# motorcycle = Motorcycle("Harley Davidson", "Sportster", False)
#
# print(car)
# print(motorcycle)
