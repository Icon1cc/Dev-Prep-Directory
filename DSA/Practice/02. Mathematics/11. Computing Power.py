"""
Write a Python function to find the computational power of a number raised to another number.
"""

def compute_power(base, exponent):
    if exponent == 0:
        return 1
    
    if exponent < 0:
        base = 1 / base
        exponent = -exponent
        
    half_power = compute_power(base, exponent // 2)
    if exponent % 2 == 0:
        return half_power * half_power
    else:
        return half_power * half_power * base

# Main program
try:
    base = float(input("Enter the base number: "))
    exponent = float(input("Enter the exponent number: "))
    result = compute_power(base, exponent)
    print(f"{base} raised to the power of {exponent} is: {result}")
except ValueError:
    print("Invalid input. Please enter numeric values for base and exponent.")
