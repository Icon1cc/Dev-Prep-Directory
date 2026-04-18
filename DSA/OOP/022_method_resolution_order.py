"""
Problem 022: Method Resolution Order (MRO)

Difficulty: Intermediate
Topic: MRO in Multiple Inheritance

=== PROBLEM DESCRIPTION ===

When a class inherits from multiple parents, Python uses Method Resolution Order
(MRO) to determine which method to call. Python uses the C3 linearization algorithm.

Your Task:
-----------
1. Create this class hierarchy (Diamond Problem):

        A
       / \
      B   C
       \ /
        D

2. Class A: method `greet()` returns "Hello from A"
3. Class B(A): method `greet()` returns "Hello from B"
4. Class C(A): method `greet()` returns "Hello from C"
5. Class D(B, C): no greet method (inherits from parents)

6. Create instance of D and call greet()
7. Print the MRO of class D using D.__mro__ or D.mro()

Expected Output:
----------------
D's greeting: Hello from B
MRO: D -> B -> C -> A -> object

=== CONCEPTS TO LEARN ===
- Python resolves methods left-to-right, depth-first, but skips duplicates
- The MRO ensures each class appears only once
- Use ClassName.__mro__ or ClassName.mro() to see the order
- Understanding MRO is crucial for complex inheritance

=== STARTER CODE ===
"""

# Write your solution below this line
# -----------------------------------



# Test your solution
# ------------------
# d = D()
# print(f"D's greeting: {d.greet()}")
# print(f"MRO: {' -> '.join(cls.__name__ for cls in D.__mro__)}")
