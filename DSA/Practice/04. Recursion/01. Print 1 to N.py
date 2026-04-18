"""
Print numbers from 1 to N using recursion.
"""

def print_1_to_N(n):
    if n == 0:
        return
    print_1_to_N(n - 1)
    print(n)
try:
    N = int(input("Enter a positive integer N: "))
    if N < 1:
        print("Please enter a positive integer greater than 0.")
    else:
        print_1_to_N(N)
except ValueError:  
    print("Invalid input. Please enter a positive integer.")
