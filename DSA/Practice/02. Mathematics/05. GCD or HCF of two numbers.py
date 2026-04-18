"""
Write a python function to compute the Greatest Common Divisor (GCD) or Highest Common Factor (HCF) of two numbers using the Euclidean algorithm.
"""

# def gcd(a, b):
#     while a != b:
#         if a > b:
#             a = a-b
#         else:
#             b = b-a
#     return a

# num1 = int(input("Enter first number: "))
# num2 = int(input("Enter second number: "))
# print(f"GCD of {num1} and {num2} is: {gcd(num1, num2)}")


def gcd(a, b):
    while b:
        a,b = b, a % b
    return a

num1 = int(input("Enter first number: "))
num2 = int(input("Enter second number: "))
print(f"GCD of {num1} and {num2} is: {gcd(num1, num2)}")