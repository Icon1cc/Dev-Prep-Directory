"""
You are given a string s representing a postfix expression. Convert this postfix expression to an infix expression.
Postfix expression: The expression of the form a b op. When an operator is followed by two operands.
Infix expression: The expression of the form a op b. When an operator is in between every pair of operands.
"""

def postfix_to_infix(expression):
    stack = []
    for char in expression:
        if char.isalnum():  # If the character is an operand (number or variable)
            stack.append(char)
        else:  # The character is an operator
            operand2 = stack.pop()
            operand1 = stack.pop()
            new_expr = f'({operand1} {char} {operand2})'
            stack.append(new_expr)

    return stack[-1]  # The final infix expression will be at the top of the stack
test_expression = "AB+CD-*"
print("Postfix Expression: ", test_expression)
print("Infix Expression: ", postfix_to_infix(test_expression))  
