"""
Problem 020: Comparing Instance, Class, and Static Methods

Difficulty: Intermediate
Topic: Method Types Comparison

=== PROBLEM DESCRIPTION ===

Let's create one class that uses all three method types to understand
when to use each:
- Instance methods: Need access to instance data (self)
- Class methods: Need access to class data (cls), often for alternative constructors
- Static methods: Don't need access to instance or class, utility functions

Your Task:
-----------
1. Create a class `Employee`:
   - Class attribute: `company = "TechCorp"`
   - Class attribute: `raise_percentage = 0.05` (5%)

2. Instance method: `__init__(self, name, salary)`
   - Store name and salary as instance attributes

3. Instance method: `apply_raise(self)`
   - Increase salary by raise_percentage
   - Needs self (instance salary) and class attribute (raise_percentage)

4. Class method: `set_raise_percentage(cls, percentage)`
   - Updates the class-level raise_percentage
   - Affects ALL employees

5. Class method: `from_string(cls, emp_string)`
   - Parses "name-salary" format and creates Employee

6. Static method: `is_workday(day)`
   - Returns True if day (0-6, Mon-Sun) is a workday (0-4)
   - Doesn't need any employee or class data

Expected Output:
----------------
Alice's salary: $50000
After raise: $52500.00
New raise percentage set to 10%
Bob's salary after 10% raise: $66000.00
Is Monday a workday? True
Is Saturday a workday? False

=== STARTER CODE ===
"""

# Write your solution below this line
# -----------------------------------



# Test your solution
# ------------------
# emp1 = Employee("Alice", 50000)
# print(f"Alice's salary: ${emp1.salary}")
# emp1.apply_raise()
# print(f"After raise: ${emp1.salary:.2f}")
#
# Employee.set_raise_percentage(0.10)
# print("New raise percentage set to 10%")
#
# emp2 = Employee.from_string("Bob-60000")
# emp2.apply_raise()
# print(f"Bob's salary after 10% raise: ${emp2.salary:.2f}")
#
# print(f"Is Monday a workday? {Employee.is_workday(0)}")
# print(f"Is Saturday a workday? {Employee.is_workday(5)}")
