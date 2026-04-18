"""
Problem 050: Building a Linked List Class

Difficulty: Intermediate
Topic: Data Structure Implementation

=== PROBLEM DESCRIPTION ===

A linked list is a fundamental data structure. Each node contains data and
a reference to the next node. This is a common interview topic!

Your Task:
-----------
1. Create a `Node` class:
   - `__init__(data)` - stores data and next (default None)

2. Create a `LinkedList` class:
   - `__init__()` - initializes empty list (head = None)
   - `append(data)` - add node at the end
   - `prepend(data)` - add node at the beginning
   - `delete(data)` - remove first node with matching data
   - `find(data)` - return True if data exists
   - `__len__` - return number of nodes
   - `__iter__` - allow iteration over values
   - `__str__` - display as "1 -> 2 -> 3 -> None"

3. Add advanced methods:
   - `reverse()` - reverse the list in place
   - `get(index)` - get value at index
   - `insert(index, data)` - insert at specific position

Expected Output:
----------------
List: 1 -> 2 -> 3 -> 4 -> None
Length: 4
Find 3: True
After delete 2: 1 -> 3 -> 4 -> None
Reversed: 4 -> 3 -> 1 -> None
Element at index 1: 3

=== CONCEPTS TO LEARN ===
- Each node points to the next node
- Operations: O(1) prepend, O(n) append/search
- Understanding pointers/references
- Common interview data structure

=== STARTER CODE ===
"""

# Write your solution below this line
# -----------------------------------



# Test your solution
# ------------------
# ll = LinkedList()
# ll.append(1)
# ll.append(2)
# ll.append(3)
# ll.append(4)
#
# print(f"List: {ll}")
# print(f"Length: {len(ll)}")
# print(f"Find 3: {ll.find(3)}")
#
# ll.delete(2)
# print(f"After delete 2: {ll}")
#
# ll.reverse()
# print(f"Reversed: {ll}")
#
# print(f"Element at index 1: {ll.get(1)}")
