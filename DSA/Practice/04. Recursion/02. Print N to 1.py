"""
Print numbers from N to 1 using recursion.
"""

def print_N_to_1(n):
    if n <= 0:
        return
    print(n)
    print_N_to_1(n - 1)
try:
    N = int(input("Enter a positive integer N: "))
    if N < 1:
        print("Please enter a positive integer greater than 0.")
    else:
        print_N_to_1(N)
except ValueError:  
    print("Invalid input. Please enter a positive integer.")