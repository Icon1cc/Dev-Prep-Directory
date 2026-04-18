"""
Problem 027: Comparison Magic Methods (__lt__, __le__, __gt__, __ge__)

Difficulty: Intermediate
Topic: Dunder/Magic Methods

=== PROBLEM DESCRIPTION ===

Python provides magic methods for all comparison operators:
- __eq__: ==
- __ne__: !=
- __lt__: <
- __le__: <=
- __gt__: >
- __ge__: >=

Your Task:
-----------
1. Create a class `Version` for software version comparison:
   - `__init__(major, minor, patch)` - e.g., Version(1, 2, 3) for "1.2.3"
   - `__str__` returns "major.minor.patch"

2. Implement comparison methods to compare versions:
   - Compare by major first, then minor, then patch
   - Example: 1.2.3 < 1.2.4 < 1.3.0 < 2.0.0

3. Implement: __eq__, __lt__, __le__, __gt__, __ge__

4. Test by sorting a list of Version objects

Expected Output:
----------------
Versions: 2.0.0, 1.2.3, 1.2.4, 1.3.0, 1.0.0
Sorted: 1.0.0, 1.2.3, 1.2.4, 1.3.0, 2.0.0
1.2.3 < 1.2.4: True
1.2.3 >= 1.2.3: True

=== CONCEPTS TO LEARN ===
- Implement __lt__ and __eq__, then others can be derived
- Python's sort() uses __lt__ for ordering
- functools.total_ordering can auto-generate missing comparisons

=== STARTER CODE ===
"""

# Write your solution below this line
# -----------------------------------



# Test your solution
# ------------------
# versions = [
#     Version(2, 0, 0),
#     Version(1, 2, 3),
#     Version(1, 2, 4),
#     Version(1, 3, 0),
#     Version(1, 0, 0)
# ]
#
# print(f"Versions: {', '.join(str(v) for v in versions)}")
# versions.sort()
# print(f"Sorted: {', '.join(str(v) for v in versions)}")
#
# v1 = Version(1, 2, 3)
# v2 = Version(1, 2, 4)
# print(f"{v1} < {v2}: {v1 < v2}")
# print(f"{v1} >= {v1}: {v1 >= Version(1, 2, 3)}")
