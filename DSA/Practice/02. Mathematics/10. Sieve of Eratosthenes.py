"""
Write a Python function to print all prime numbers up to a given positive integer 
using the Sieve of Eratosthenes algorithm.
"""
def sieve_of_eratosthenes(n):
    # Step 1: Create a boolean array, assume all numbers are prime initially
    primes = [True] * (n + 1)
    
    # Step 2: Mark non-primes
    p = 2
    while (p * p <= n):
        if primes[p]:  # If p is still marked as prime
            # Mark all multiples of p starting from p²
            for i in range(p * p, n + 1, p):
                primes[i] = False
        p += 1
    
    # Step 3: Collect all prime numbers
    prime_numbers = [p for p in range(2, n + 1) if primes[p]]
    return prime_numbers

try:
    num = int(input("Enter a positive number: "))
    if num < 2:
        print("Please enter a number greater than or equal to 2.")
    else:
        prime_numbers = sieve_of_eratosthenes(num)
        if prime_numbers:
            print(f"Prime numbers up to {num} are: {prime_numbers}")
        else:
            print(f"No prime numbers up to {num}.")
except ValueError:
    print("Invalid input. Please enter a number.")
