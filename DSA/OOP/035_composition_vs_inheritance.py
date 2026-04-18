"""
Problem 035: Composition vs Inheritance

Difficulty: Intermediate
Topic: Design Principles

=== PROBLEM DESCRIPTION ===

"Favor composition over inheritance" is a key design principle.
- Inheritance: "is-a" relationship (Dog IS AN Animal)
- Composition: "has-a" relationship (Car HAS AN Engine)

Composition is often more flexible because you can change components at runtime.

Your Task:
-----------
1. Create component classes:
   - `Engine` with methods: start(), stop(), accelerate()
   - `Transmission` with method: shift_gear(gear)
   - `Stereo` with methods: turn_on(), turn_off(), play(song)

2. Create a `Car` class using COMPOSITION:
   - Has an Engine, Transmission, and Stereo as attributes
   - Method `start()` starts the engine and turns on stereo
   - Method `drive(gear)` uses transmission and engine

3. Demonstrate changing a component at runtime:
   - Create a `SportsEngine` with more powerful accelerate()
   - Swap out the engine in an existing car

Expected Output:
----------------
Starting car...
Engine started
Stereo on
Shifting to gear 1
Accelerating...

Upgrading to sports engine...
Accelerating... VROOOOM! (Sports Mode)

=== CONCEPTS TO LEARN ===
- Composition provides more flexibility than inheritance
- Components can be swapped at runtime
- Easier to test (can mock components)
- Avoids deep inheritance hierarchies

=== STARTER CODE ===
"""

# Write your solution below this line
# -----------------------------------



# Test your solution
# ------------------
# car = Car()
# print("Starting car...")
# car.start()
# car.drive(1)
#
# print("\nUpgrading to sports engine...")
# car.engine = SportsEngine()
# car.engine.accelerate()
