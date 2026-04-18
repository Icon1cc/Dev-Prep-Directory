"""
Write a program to check if the given expression has balanced parentheses or not. The expression will contain three types of parentheses: (), {}, and [].
"""

def is_balanced_parentheses(expression):
    stack = []
    parentheses_map = {')': '(', '}': '{', ']': '['}

    for char in expression:
        if char in parentheses_map.values():
            stack.append(char)
        elif char in parentheses_map.keys():
            if not stack or stack[-1] != parentheses_map[char]:
                return False
            stack.pop()

    return len(stack) == 0
# Example usage
expression = "{[()()]}"
if is_balanced_parentheses(expression):
    print("The expression has balanced parentheses.")
else:
    print("The expression does not have balanced parentheses.")


# def is_balanced_parentheses(expression):
#     stack = []
#     # Map closing brackets to their corresponding opening brackets
#     parentheses_map = {')': '(', '}': '{', ']': '['}

#     for char in expression:
#         # 1. If it's an opening bracket, push to stack
#         if char in parentheses_map.values():
#             stack.append(char)
        
#         # 2. If it's a closing bracket
#         elif char in parentheses_map.keys():
#             # Case A: Stack is empty (nothing to match with) -> Invalid
#             # Case B: Top of stack doesn't match current closer -> Invalid
#             if not stack or stack[-1] != parentheses_map[char]:
#                 return False
            
#             # 3. Match found, remove the opening bracket
#             stack.pop()

#     # 4. If stack is empty, all brackets were matched. 
#     # If not empty, we have orphan opening brackets.
#     return len(stack) == 0
