"""
Write a recursive function to find the fibonacci series up to a given number of terms.
"""

def fibonacci(n):
    if n == 0 or n == 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
try:
    N = int(input("Enter the number of terms for the Fibonacci series: "))
    if N <= 0:
        print("Please enter a positive integer.")
    else:
        print(f"Fibonacci series up to {N} terms:")
        for i in range(N):
            print(fibonacci(i), end=' ')
        print()
except ValueError:
    print("Invalid input. Please enter a positive integer.")