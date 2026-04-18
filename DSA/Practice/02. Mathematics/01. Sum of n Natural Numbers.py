"""
Write a function to print sum of N natural numbers.
"""

def sum_of_natural_numbers(n):
    return n * (n+1)/2
    
n = int(input("Enter the number: "))
print(sum_of_natural_numbers(n))