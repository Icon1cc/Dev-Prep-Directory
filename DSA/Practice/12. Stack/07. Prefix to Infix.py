"""
You are given a string s representing a prefix expression. Convert this prefix expression to an infix expression.

Prefix expression: The expression of the form op a b. When an operator is followed by two operands.
Infix expression: The expression of the form a op b. When an operator is in between every pair of operands.
"""

def custom_reverse(expression):
    temp_stack = []
    for char in expression:
        temp_stack.append(char)
    while temp_stack:
        yield temp_stack.pop()

def prefix_to_infix(expression):
    stack = []
    # Using our custom reverse function
    for char in custom_reverse(expression):
        if char.isalnum():  
            stack.append(char)
        else:  
            operand1 = stack.pop()
            operand2 = stack.pop()
            new_expr = f'({operand1} {char} {operand2})'
            stack.append(new_expr)

    return stack[-1] 

test_expression = "*+AB-CD"
print("Prefix Expression: ", test_expression)
print("Infix Expression: ", prefix_to_infix(test_expression))