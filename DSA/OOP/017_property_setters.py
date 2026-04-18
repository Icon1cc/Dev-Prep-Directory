"""
Problem 017: Property Decorators - Setters

Difficulty: Intermediate
Topic: Properties with Setters

=== PROBLEM DESCRIPTION ===

You can also define setters for properties, allowing controlled assignment.
This is useful for validation, transformation, or triggering side effects
when a value is set.

Your Task:
-----------
1. Create a class `Temperature`:
   - Store temperature internally in Celsius as `_celsius`

2. Create a property `celsius`:
   - Getter returns `_celsius`
   - Setter validates: must be >= -273.15 (absolute zero)
   - If invalid, raise ValueError with message

3. Create a property `fahrenheit`:
   - Getter converts and returns: (celsius * 9/5) + 32
   - Setter converts from F to C and stores: (fahrenheit - 32) * 5/9

4. Demonstrate setting temperature in both units

Expected Output:
----------------
25°C = 77.00°F
Setting to 100°F...
37.78°C = 100.00°F
Attempting invalid temperature...
Error: Temperature cannot be below absolute zero (-273.15°C)

=== CONCEPTS TO LEARN ===
- Use @property_name.setter to define a setter
- Setters enable validation before assignment
- Can have computed setters that transform values
- Properties provide a clean interface for complex logic

=== STARTER CODE ===
"""

# Write your solution below this line
# -----------------------------------



# Test your solution
# ------------------
# temp = Temperature(25)  # 25°C
# print(f"{temp.celsius}°C = {temp.fahrenheit:.2f}°F")
#
# print("Setting to 100°F...")
# temp.fahrenheit = 100
# print(f"{temp.celsius:.2f}°C = {temp.fahrenheit:.2f}°F")
#
# print("Attempting invalid temperature...")
# try:
#     temp.celsius = -300  # Below absolute zero
# except ValueError as e:
#     print(f"Error: {e}")
