"""
Problem 038: Factory Design Pattern

Difficulty: Intermediate
Topic: Design Patterns

=== PROBLEM DESCRIPTION ===

The Factory pattern provides an interface for creating objects without specifying
their exact class. It's useful when the creation logic is complex or when you
want to decouple object creation from usage.

Your Task:
-----------
1. Create a base class `Animal` with abstract method `speak()`

2. Create subclasses: `Dog`, `Cat`, `Bird` - each with their own speak()

3. Create a `AnimalFactory` class with:
   - Static method `create_animal(animal_type)` that returns the appropriate animal
   - Raises ValueError for unknown types

4. Create a more advanced `VehicleFactory`:
   - Different vehicle types: Car, Motorcycle, Truck
   - Each has attributes: brand, model, price
   - Factory method accepts a dictionary of specs

Expected Output:
----------------
Dog says: Woof!
Cat says: Meow!
Bird says: Tweet!
Unknown animal type!

Vehicle: Toyota Camry ($25000)
Vehicle: Harley Sportster ($15000)

=== CONCEPTS TO LEARN ===
- Factory encapsulates object creation logic
- Client code doesn't need to know concrete classes
- Easy to add new types without changing client code
- Can validate parameters and handle errors centrally

=== STARTER CODE ===
"""

from abc import ABC, abstractmethod

# Write your solution below this line
# -----------------------------------



# Test your solution
# ------------------
# # Simple Factory
# dog = AnimalFactory.create_animal("dog")
# cat = AnimalFactory.create_animal("cat")
# bird = AnimalFactory.create_animal("bird")
#
# print(f"Dog says: {dog.speak()}")
# print(f"Cat says: {cat.speak()}")
# print(f"Bird says: {bird.speak()}")
#
# try:
#     unknown = AnimalFactory.create_animal("dragon")
# except ValueError as e:
#     print("Unknown animal type!")
#
# print()
#
# # Vehicle Factory
# car_specs = {"type": "car", "brand": "Toyota", "model": "Camry", "price": 25000}
# motorcycle_specs = {"type": "motorcycle", "brand": "Harley", "model": "Sportster", "price": 15000}
#
# car = VehicleFactory.create_vehicle(car_specs)
# motorcycle = VehicleFactory.create_vehicle(motorcycle_specs)
#
# print(f"Vehicle: {car}")
# print(f"Vehicle: {motorcycle}")
