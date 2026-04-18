"""
Problem 029: The __hash__ Method (Making Objects Hashable)

Difficulty: Intermediate
Topic: Dunder Methods

=== PROBLEM DESCRIPTION ===

For objects to be used as dictionary keys or in sets, they must be hashable.
This requires implementing `__hash__`. The rule: if two objects are equal
(__eq__ returns True), they MUST have the same hash.

Your Task:
-----------
1. Create a class `Person`:
   - `__init__(name, ssn)` - SSN (Social Security Number) is unique
   - `__eq__` - two people are equal if they have the same SSN
   - `__hash__` - hash should be based on SSN (the unique identifier)
   - `__repr__` - for debugging

2. Create multiple Person objects
3. Add them to a set (requires hashability)
4. Use them as dictionary keys

Expected Output:
----------------
Set of people: {Person('Alice', '111'), Person('Bob', '222')}
Adding Alice again (same SSN) - set size unchanged: 2
Dictionary: {Person('Alice', '111'): 'Engineer', Person('Bob', '222'): 'Manager'}

=== CONCEPTS TO LEARN ===
- Objects with __eq__ but no __hash__ become unhashable
- Hash must be consistent: equal objects must hash equally
- Hash should be based on immutable attributes
- Use hash() of a tuple of the identifying attributes

=== STARTER CODE ===
"""

# Write your solution below this line
# -----------------------------------



# Test your solution
# ------------------
# p1 = Person("Alice", "111")
# p2 = Person("Bob", "222")
# p3 = Person("Alice Smith", "111")  # Same SSN as p1
#
# people = {p1, p2}
# print(f"Set of people: {people}")
#
# people.add(p3)  # Same SSN as Alice, shouldn't add
# print(f"Adding Alice again (same SSN) - set size unchanged: {len(people)}")
#
# roles = {p1: "Engineer", p2: "Manager"}
# print(f"Dictionary: {roles}")
