"""
Problem 006: Class vs Instance Attributes

Difficulty: Beginner
Topic: Class Attributes

=== PROBLEM DESCRIPTION ===

Class attributes are shared by ALL instances of a class, while instance
attributes are unique to each object. Class attributes are defined
directly in the class body, outside of any method.

Your Task:
-----------
1. Create a class called `Employee`
2. Add a CLASS attribute `company_name = "TechCorp"` (shared by all employees)
3. Add a CLASS attribute `employee_count = 0` (to track total employees)
4. In `__init__`, accept `name` and `salary` as INSTANCE attributes
5. In `__init__`, increment `employee_count` by 1 each time an employee is created
6. Add a method `display()` that shows the employee's name, salary, and company
7. Create 3 employees and show that they all share the same company name
8. Print the total employee count

Expected Output:
----------------
Alice works at TechCorp with salary $50000
Bob works at TechCorp with salary $60000
Charlie works at TechCorp with salary $55000
Total employees: 3

=== CONCEPTS TO LEARN ===
- Class attributes are defined outside __init__, inside the class
- Access class attributes via ClassName.attribute or self.attribute
- Modifying class attributes affects all instances
- Use class attributes for data shared across all objects

=== STARTER CODE ===
"""

# Write your solution below this line
# -----------------------------------

class Employee:
    company_name = "TechCorp"  # Class attribute shared by all employees
    employee_count = 0         # Class attribute to track total employees

    def __init__(self, name, salary):
        self.name = name       # Instance attribute for employee's name
        self.salary = salary   # Instance attribute for employee's salary
        Employee.employee_count += 1  # Increment employee count when a new employee is created

    def display(self):
        print(f"{self.name} works at {Employee.company_name} with salary ${self.salary}")

# Test your solution
# ------------------
emp1 = Employee("Alice", 50000)
emp2 = Employee("Bob", 60000)
emp3 = Employee("Charlie", 55000)

emp1.display()
emp2.display()
emp3.display()
print(f"Total employees: {Employee.employee_count}")

