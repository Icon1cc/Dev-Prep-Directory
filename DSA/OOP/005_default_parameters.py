"""
Problem 005: Default Parameter Values in __init__

Difficulty: Beginner
Topic: Default Arguments

=== PROBLEM DESCRIPTION ===

Just like regular functions, the `__init__` method can have default
parameter values. This makes some arguments optional when creating objects.

Your Task:
-----------
1. Create a class called `Student`
2. The `__init__` should accept:
   - `name` (required)
   - `grade` (optional, default=0)
   - `school` (optional, default="Unknown")
3. Add a method `display_info()` that prints all student information
4. Create three students:
   - Student with only name: "Alice"
   - Student with name and grade: "Bob", 85
   - Student with all info: "Charlie", 92, "MIT"
5. Display info for all three

Expected Output:
----------------
Student: Alice, Grade: 0, School: Unknown
Student: Bob, Grade: 85, School: Unknown
Student: Charlie, Grade: 92, School: MIT

=== CONCEPTS TO LEARN ===
- Default parameters must come after required parameters
- Default values are used when arguments are not provided
- This pattern is common for flexible object creation

=== STARTER CODE ===
"""

# Write your solution below this line
# -----------------------------------

class Student:
    def __init__(self, name, grade=0, school="Unknown"):
        self.name = name
        self.grade = grade
        self.school = school

    def display_info(self):
        print(f"Student: {self.name}, Grade: {self.grade}, School: {self.school}")



# Test your solution
# ------------------
student1 = Student("Alice")
student2 = Student("Bob", 85)
student3 = Student("Charlie", 92, "MIT")

student1.display_info()
student2.display_info()
student3.display_info()
