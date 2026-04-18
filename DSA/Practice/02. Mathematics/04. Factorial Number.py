"""
Write a Python function to print the factorial of a given number.
"""

def fact_n(n):
    n = abs(n)
    if n == 0 or n == 1:
        return 1
    num = 1
    for i in range(1, n+1):
        num = num * i
    return num
    
n = int(input("Enter a number: "))
print(f"Factorial of a given number is: {fact_n(n)} ")