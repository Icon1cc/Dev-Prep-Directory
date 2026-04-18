"""
Write a Python function to find all divisors of a given positive integer.
"""

def div_num(n):
    alllist = []
    for i in range (1, int(n**0.5)+1):
        if n % i == 0:
            alllist.append(i)
            if i*i != n: 
                alllist.append(n // i)
    alllist.sort()
    return alllist

try:
    num = int(input("Enter a positive number: "))
    divisors = div_num(num)
    if divisors:
        print(f"The divisors of {num} are: {divisors}")
except ValueError:
    print("Invalid input. Please enter a number.") 