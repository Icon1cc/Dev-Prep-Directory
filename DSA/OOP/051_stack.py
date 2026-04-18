"""
Problem 051: Building a Stack Class

Difficulty: Intermediate
Topic: Data Structure Implementation

=== PROBLEM DESCRIPTION ===

A stack is a LIFO (Last In, First Out) data structure. Think of a stack
of plates - you can only add/remove from the top.

Your Task:
-----------
1. Create a `Stack` class:
   - `__init__(max_size=None)` - optional maximum size
   - `push(item)` - add item to top (raise error if full)
   - `pop()` - remove and return top item (raise error if empty)
   - `peek()` - return top item without removing (raise error if empty)
   - `is_empty()` - return True if empty
   - `is_full()` - return True if at max_size
   - `size()` - return current number of items
   - `__str__` - visual representation (top at right)

2. Create a custom `StackEmptyError` exception
3. Create a custom `StackFullError` exception

4. Implement practical use case:
   - `check_balanced_parentheses(expression)` using a stack
   - Returns True if parentheses are balanced

Expected Output:
----------------
Stack: [1, 2, 3] <- top
Peek: 3
Pop: 3
Stack after pop: [1, 2] <- top
Is empty: False

Balanced "((()))": True
Balanced "((()": False
Balanced "())(": False

=== CONCEPTS TO LEARN ===
- LIFO principle
- All operations are O(1)
- Used in: function calls, undo operations, parsing
- Foundation for more complex algorithms

=== STARTER CODE ===
"""

# Write your solution below this line
# -----------------------------------



# Test your solution
# ------------------
# stack = Stack()
# stack.push(1)
# stack.push(2)
# stack.push(3)
#
# print(f"Stack: {stack}")
# print(f"Peek: {stack.peek()}")
# print(f"Pop: {stack.pop()}")
# print(f"Stack after pop: {stack}")
# print(f"Is empty: {stack.is_empty()}")
#
# print()
#
# # Balanced parentheses
# print(f'Balanced "((()))": {check_balanced_parentheses("((()))")}')
# print(f'Balanced "((()": {check_balanced_parentheses("((()")}')
# print(f'Balanced "())(": {check_balanced_parentheses("())(")}')
