"""
Write a Python function to find the prime factorization of a given number.
"""
def prime_factorization(n):
    factors = []
    # Check for number of 2s that divide n
    while n % 2 == 0:
        factors.append(2)
        n //= 2
    # n must be odd at this point, so we can skip even numbers
    for i in range(3, int(n**0.5) + 1, 2):
        while n % i == 0:
            factors.append(i)
            n //= i
    # This condition is to check if n is a prime number greater than 2
    if n > 2:
        factors.append(n)
    return factors  
try:
    number = int(input("Enter a number to find its prime factorization: "))
    if number <= 1:
        print("Please enter a number greater than 1.")
    else:
        print(f"Prime factorization of {number} is: {prime_factorization(number)}")
except ValueError:
    print("Invalid input. Please enter a valid integer.")