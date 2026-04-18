"""
Write a Python function that checks whether a given integer is a palindrome.
"""

def palin(n):
    n = str(abs(n))
    return n == n[::-1]

n = int(input("Enter a number: "))
print(palin(n))