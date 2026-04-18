"""
Problem 018: Class Methods with @classmethod

Difficulty: Intermediate
Topic: Class Methods

=== PROBLEM DESCRIPTION ===

Class methods receive the class itself as the first argument (cls), not an
instance (self). They can access and modify class-level attributes and are
often used as alternative constructors.

Your Task:
-----------
1. Create a class `Date`:
   - `__init__` accepts `year`, `month`, `day`
   - Add `__str__` to display as "YYYY-MM-DD"

2. Add a class method `from_string(cls, date_string)`:
   - Accepts string in format "YYYY-MM-DD"
   - Parses it and returns a new Date instance
   - This is an "alternative constructor"

3. Add a class method `today(cls)`:
   - Returns a Date instance with current date
   - Use datetime.date.today()

4. Create dates using both the regular constructor and class methods

Expected Output:
----------------
Regular constructor: 2024-01-15
From string: 2023-12-25
Today: (current date)

=== CONCEPTS TO LEARN ===
- @classmethod decorator defines a class method
- First parameter is `cls` (the class), not `self` (an instance)
- Common use: alternative constructors
- Can be called on the class: Date.from_string("...")

=== STARTER CODE ===
"""

from datetime import date as dt_date

# Write your solution below this line
# -----------------------------------



# Test your solution
# ------------------
# date1 = Date(2024, 1, 15)
# print(f"Regular constructor: {date1}")
#
# date2 = Date.from_string("2023-12-25")
# print(f"From string: {date2}")
#
# date3 = Date.today()
# print(f"Today: {date3}")
