"""
Write a Python function to calculate the iterative power of a number raised to another number.
"""

def iterative_power(base, exponent):
    result = 1
    while exponent > 0:
        if exponent % 2 != 0:
            result *= base
        base *= base
        exponent //= 2
    return result

# Main program
try:
    base = float(input("Enter the base number: "))
    exponent = int(input("Enter the exponent number (non-negative integer): "))
    if exponent < 0:
        print("Please enter a non-negative integer for the exponent.")
    else:
        result = iterative_power(base, exponent)
        print(f"{base} raised to the power of {exponent} is: {result}")
except ValueError:
    print("Invalid input. Please enter numeric values for base and a non-negative integer for exponent.")