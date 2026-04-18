"""
Problem 043: Data Classes (Python 3.7+)

Difficulty: Intermediate
Topic: Modern Python OOP

=== PROBLEM DESCRIPTION ===

The @dataclass decorator automatically generates __init__, __repr__, __eq__,
and other methods. It's perfect for classes that mainly hold data.

Your Task:
-----------
1. Create a regular class `PointRegular` with x, y coordinates:
   - Write __init__, __repr__, __eq__ manually

2. Create the same thing as a dataclass `PointDataclass`:
   - Use @dataclass decorator
   - Just define the fields - methods are auto-generated!

3. Create a more complex dataclass `Employee`:
   - Fields: name, employee_id, salary, department (default="Engineering")
   - Use `field()` for default factory (for mutable defaults)
   - Make it ordered (add order=True for comparison methods)
   - Add a custom method `give_raise(percent)`

4. Create a frozen (immutable) dataclass `Config`:
   - Use `frozen=True`
   - Attempting to modify raises FrozenInstanceError

Expected Output:
----------------
Regular class: Point(3, 4)
Dataclass: PointDataclass(x=3, y=4)
Equal: True

Employee: Employee(name='Alice', employee_id=101, salary=50000, department='Engineering')
After raise: 55000.0

Frozen config - cannot modify!
Error: cannot assign to field 'debug'

=== CONCEPTS TO LEARN ===
- @dataclass reduces boilerplate code
- Options: frozen, order, eq, repr, hash
- field() for default values, especially for mutable defaults
- Can still add custom methods

=== STARTER CODE ===
"""

from dataclasses import dataclass, field
from typing import List

# Write your solution below this line
# -----------------------------------



# Test your solution
# ------------------
# # Compare regular class vs dataclass
# p1 = PointRegular(3, 4)
# p2 = PointDataclass(3, 4)
# print(f"Regular class: {p1}")
# print(f"Dataclass: {p2}")
# print(f"Equal: {PointDataclass(3, 4) == PointDataclass(3, 4)}")
#
# print()
#
# # Employee dataclass
# emp = Employee("Alice", 101, 50000)
# print(f"Employee: {emp}")
# emp.give_raise(10)
# print(f"After raise: {emp.salary}")
#
# print()
#
# # Frozen dataclass
# print("Frozen config - cannot modify!")
# config = Config(debug=True, log_level="INFO")
# try:
#     config.debug = False
# except Exception as e:
#     print(f"Error: {e}")
