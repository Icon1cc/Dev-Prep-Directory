"""
Write a recursive function to calculate the sum of digits of a given number.
"""

def sum_of_digits(n):
    if n == 0:
        return 0
    return n % 10 + sum_of_digits(n // 10)
try:
    N = int(input("Enter a non-negative integer to calculate the sum of its digits: "))
    if N < 0:
        print("Please enter a non-negative integer.")
    else:
        result = sum_of_digits(N)
        print(f"The sum of the digits of {N} is {result}.")
except ValueError:
    print("Invalid input. Please enter a non-negative integer.")