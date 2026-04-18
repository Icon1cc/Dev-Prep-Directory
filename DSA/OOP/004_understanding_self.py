"""
Problem 004: The self Parameter Explained

Difficulty: Beginner
Topic: Understanding self

=== PROBLEM DESCRIPTION ===

`self` is a reference to the current instance of the class. It allows
each object to keep track of its own data separately from other objects.

Your Task:
-----------
1. Create a class called `Counter`
2. In `__init__`, initialize an attribute `count` to 0
3. Add a method `increment()` that increases count by 1
4. Add a method `decrement()` that decreases count by 1
5. Add a method `get_count()` that returns the current count
6. Create two separate Counter objects
7. Increment the first counter 3 times
8. Increment the second counter 1 time
9. Print both counts to show they are independent

Expected Output:
----------------
Counter 1: 3
Counter 2: 1

=== CONCEPTS TO LEARN ===
- Each instance has its own copy of instance attributes
- `self` ensures methods work on the correct object's data
- Multiple objects of the same class are independent

=== STARTER CODE ===
"""

# Write your solution below this line
# -----------------------------------

class Counter:
    def __init__(self):
        self.count = 0

    def increment(self):
        self.count += 1

    def decrement(self):
        self.count -= 1

    def get_count(self):
        return self.count


# Test your solution
# ------------------
counter1 = Counter()
counter2 = Counter()

counter1.increment()
counter1.increment()
counter1.increment()

counter2.increment()

print(f"Counter 1: {counter1.get_count()}")
print(f"Counter 2: {counter2.get_count()}")
