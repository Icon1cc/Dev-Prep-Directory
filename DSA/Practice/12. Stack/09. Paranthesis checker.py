"""
Write a program to check whether the parentheses are balanced or not. For example, the string "(()())" is balanced, while the string "(()" is not balanced.
"""

def is_balanced_parentheses(s):
    stack = []
    parentheses_map = {')': '(', '}': '{', ']': '['}

    for char in s:
        if char in parentheses_map.values():  # If it's an opening parenthesis
            stack.append(char)
        elif char in parentheses_map.keys():  # If it's a closing parenthesis
            if not stack or stack[-1] != parentheses_map[char]:
                return False  # Not balanced
            stack.pop()  # Pop the matching opening parenthesis

    return len(stack) == 0  # If stack is empty, parentheses are balanced

# Test cases
test_string1 = "(()())"
test_string2 = "(()"
print(f"{test_string1} is balanced: {is_balanced_parentheses(test_string1)}")
print(f"{test_string2} is balanced: {is_balanced_parentheses(test_string2)}")