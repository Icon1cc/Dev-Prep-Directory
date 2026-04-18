"""
Problem 053: Building a Binary Search Tree

Difficulty: Intermediate-Advanced
Topic: Data Structure Implementation

=== PROBLEM DESCRIPTION ===

A Binary Search Tree (BST) is a tree where:
- Left subtree contains only nodes with values LESS than parent
- Right subtree contains only nodes with values GREATER than parent
- Both subtrees are also BSTs

Your Task:
-----------
1. Create a `TreeNode` class:
   - `__init__(value)` - value, left=None, right=None

2. Create a `BinarySearchTree` class:
   - `insert(value)` - insert value in correct position
   - `search(value)` - return True if value exists
   - `delete(value)` - remove node with value
   - `find_min()` - return minimum value
   - `find_max()` - return maximum value

3. Implement traversals (return list of values):
   - `inorder()` - left, root, right (gives sorted order!)
   - `preorder()` - root, left, right
   - `postorder()` - left, right, root
   - `level_order()` - breadth-first, level by level

4. Additional methods:
   - `height()` - return height of tree
   - `is_valid_bst()` - verify BST property holds

Expected Output:
----------------
Inorder (sorted): [2, 3, 4, 5, 6, 7, 8]
Preorder: [5, 3, 2, 4, 7, 6, 8]
Postorder: [2, 4, 3, 6, 8, 7, 5]
Level order: [5, 3, 7, 2, 4, 6, 8]
Min: 2, Max: 8
Height: 3
Search 4: True
Is valid BST: True

=== CONCEPTS TO LEARN ===
- BST property enables O(log n) search/insert
- Traversals: DFS (in/pre/post), BFS (level)
- Deletion has 3 cases: leaf, one child, two children
- Fundamental interview data structure

=== STARTER CODE ===
"""

from collections import deque

# Write your solution below this line
# -----------------------------------



# Test your solution
# ------------------
# bst = BinarySearchTree()
# for val in [5, 3, 7, 2, 4, 6, 8]:
#     bst.insert(val)
#
# print(f"Inorder (sorted): {bst.inorder()}")
# print(f"Preorder: {bst.preorder()}")
# print(f"Postorder: {bst.postorder()}")
# print(f"Level order: {bst.level_order()}")
# print(f"Min: {bst.find_min()}, Max: {bst.find_max()}")
# print(f"Height: {bst.height()}")
# print(f"Search 4: {bst.search(4)}")
# print(f"Is valid BST: {bst.is_valid_bst()}")
