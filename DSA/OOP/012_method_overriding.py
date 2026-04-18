"""
Problem 012: Method Overriding

Difficulty: Beginner
Topic: Inheritance - Overriding Methods

=== PROBLEM DESCRIPTION ===

Child classes can override (replace) methods inherited from the parent.
When you call the method on the child object, it uses the child's version.

Your Task:
-----------
1. Create a parent class `Animal`:
   - `__init__` accepts `name`
   - `speak()` method returns "Some sound"

2. Create child class `Dog(Animal)`:
   - Override `speak()` to return "Woof!"

3. Create child class `Cat(Animal)`:
   - Override `speak()` to return "Meow!"

4. Create child class `Cow(Animal)`:
   - Override `speak()` to return "Moo!"

5. Create instances of each and call speak()

Expected Output:
----------------
Buddy says: Woof!
Whiskers says: Meow!
Bessie says: Moo!

=== CONCEPTS TO LEARN ===
- Override a method by defining it again in the child class
- The child's version completely replaces the parent's for that class
- This is a form of polymorphism (same method name, different behavior)

=== STARTER CODE ===
"""

# Write your solution below this line
# -----------------------------------



# Test your solution
# ------------------
# dog = Dog("Buddy")
# cat = Cat("Whiskers")
# cow = Cow("Bessie")
#
# print(f"{dog.name} says: {dog.speak()}")
# print(f"{cat.name} says: {cat.speak()}")
# print(f"{cow.name} says: {cow.speak()}")
