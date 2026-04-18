"""
Write a program to find the modular multiplicative inverse of an integer 'a' under modulo 'm' using the Extended Euclidean Algorithm.
"""

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b%a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y
def mod_inverse(a, m):
    gcd, x, y = extended_gcd(a, m)
    if gcd != 1:
        return None  # Inverse doesn't exist
    else:
        return x % m
try:
    a = int(input("Enter integer a: "))
    m = int(input("Enter modulo m: "))
    if m <= 0:
        print("Modulo m must be a positive integer.")
    else:
        inverse = mod_inverse(a, m)
        if inverse is None:
            print(f"The modular multiplicative inverse of {a} under modulo {m} does not exist.")
        else:
            print(f"The modular multiplicative inverse of {a} under modulo {m} is: {inverse}")
except ValueError:
    print("Invalid input. Please enter integers for a and m.")
    