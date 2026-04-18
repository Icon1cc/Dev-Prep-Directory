"""
You are given a string s representing an infix expression. Convert this infix expression to a postfix expression.

Infix expression: The expression of the form a op b. When an operator is in between every pair of operands.
Postfix expression: The expression of the form a b op. When an operator is followed for every pair of operands.
"""

def infix_to_postfix(expression):
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
    stack = []
    postfix = []

    for char in expression:
        if char.isalnum():  # If the character is an operand (number or variable)
            postfix.append(char)
        elif char in precedence:  # If the character is an operator
            while (stack and stack[-1] != '(' and
                   precedence[stack[-1]] >= precedence[char]):
                postfix.append(stack.pop())
            stack.append(char)
        elif char == '(':  # If the character is '(', push it to the stack
            stack.append(char)
        elif char == ')':  # If the character is ')', pop from stack to postfix until '(' is found
            while stack and stack[-1] != '(':
                postfix.append(stack.pop())
            stack.pop()  # Pop the '(' from the stack
    # Pop all the remaining operators from the stack
    while stack:
        postfix.append(stack.pop())

    return ''.join(postfix)

test_expression = "a+b*(c^d-e)^(f+g*h)-i"
print("Infix Expression: ", test_expression)
print("Postfix Expression: ", infix_to_postfix(test_expression))
