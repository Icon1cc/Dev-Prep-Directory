"""
Write a Python function that counts the number of digits in a given integer.
"""

def count_int(n):
    if n == 0:
        return 1
    n = abs(n)
    count = 0
    while n > 0:
        n = n // 10
        count += 1
    return count
    
n = int(input("Please enter a integer: "))
print(count_int(n))