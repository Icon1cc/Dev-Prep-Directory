"""
Problem 068: Copy and Deepcopy

Difficulty: Intermediate
Topic: Object Copying

=== PROBLEM DESCRIPTION ===

Python provides two types of copying:
- Shallow copy: Creates new object but references same nested objects
- Deep copy: Creates new object AND copies all nested objects

Your Task:
-----------
1. Create a `Address` class with: street, city, country

2. Create a `Person` class with:
   - name (str)
   - address (Address)
   - friends (list of Person)

3. Implement `__copy__` for shallow copy:
   - New Person but same Address object

4. Implement `__deepcopy__` for deep copy:
   - New Person AND new Address object

5. Demonstrate the difference:
   - Shallow: changing address affects both
   - Deep: objects are fully independent

Expected Output:
----------------
Original: Alice at 123 Main St
Shallow copy: Alice at 123 Main St

Changing original's street to '456 Oak Ave'...
Original: Alice at 456 Oak Ave
Shallow copy: Alice at 456 Oak Ave  (ALSO CHANGED!)

Deep copy: Alice at 123 Main St
Changing original's street to '789 Pine Rd'...
Original: Alice at 789 Pine Rd
Deep copy: Alice at 123 Main St  (UNCHANGED!)

=== CONCEPTS TO LEARN ===
- import copy; copy.copy() for shallow copy
- import copy; copy.deepcopy() for deep copy
- Implement __copy__ and __deepcopy__ for custom behavior
- Important for avoiding unexpected mutations

=== STARTER CODE ===
"""

import copy

# Write your solution below this line
# -----------------------------------



# Test your solution
# ------------------
# Demonstrate shallow vs deep copy behavior
