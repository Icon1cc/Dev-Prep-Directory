"""
Write a Python function to calculate the Least Common Multiple (LCM) of two numbers.
"""

def gcd(a, b):
    while b:
        a,b = b, a % b
    return a
    
def lcm(a, b):
    if a == 0 or b == 0:
        return 0
    lcm = a*b // gcd(a, b)
    return lcm

num1 = int(input("Enter first number: "))
num2 = int(input("Enter second number: "))
print(f"LCM of {num1} and {num2} is: {lcm(num1, num2)}")