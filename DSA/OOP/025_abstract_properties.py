"""
Problem 025: Abstract Properties

Difficulty: Intermediate
Topic: Abstract Base Classes

=== PROBLEM DESCRIPTION ===

Abstract classes can also have abstract properties. Subclasses must implement
these properties, not just methods.

Your Task:
-----------
1. Create abstract class `Vehicle(ABC)`:
   - Abstract property: `max_speed` (each vehicle must define its max speed)
   - Abstract property: `fuel_type` (each vehicle must define its fuel)
   - Concrete method: `describe()` - returns description using the properties

2. Create `Car(Vehicle)`:
   - `__init__(brand, max_speed)`
   - Implement max_speed property (returns the stored value)
   - Implement fuel_type property (returns "Gasoline")

3. Create `ElectricCar(Vehicle)`:
   - `__init__(brand, max_speed)`
   - Implement max_speed property
   - Implement fuel_type property (returns "Electricity")

4. Create `Bicycle(Vehicle)`:
   - `__init__(brand)`
   - max_speed returns 30 (fixed)
   - fuel_type returns "Human Power"

Expected Output:
----------------
Toyota: Max speed 180 km/h, runs on Gasoline
Tesla: Max speed 250 km/h, runs on Electricity
Trek: Max speed 30 km/h, runs on Human Power

=== CONCEPTS TO LEARN ===
- Combine @property with @abstractmethod
- Order matters: @property must come BEFORE @abstractmethod
- Subclasses must implement abstract properties

=== STARTER CODE ===
"""

from abc import ABC, abstractmethod

# Write your solution below this line
# -----------------------------------



# Test your solution
# ------------------
# car = Car("Toyota", 180)
# electric = ElectricCar("Tesla", 250)
# bike = Bicycle("Trek")
#
# for vehicle in [car, electric, bike]:
#     print(vehicle.describe())
