"""
Write a recursive function to calculate the factorial of a given number.
"""

def factorial(n):
    if n == 0 or n ==1:
        return 1
    return n*factorial(n - 1)
try:
    N = int(input("Enter a non-negative integer to calculate its factorial: "))
    if N < 0:
        print("Please enter a non-negative integer.")
    else:
        result = factorial(N)
        print(f"The factorial of {N} is {result}.")
except ValueError:
    print("Invalid input. Please enter a non-negative integer.")