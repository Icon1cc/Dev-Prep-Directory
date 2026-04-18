"""
Write a Python program to check whether a given number is a palindrome or not using recursion.
"""

def is_number_palindrome(n, rev=0):
    # Base case: if n is 0, return the reversed number
    if n == 0:
        return rev
    else:
        # Get the last digit of n and add it to rev
        rev = rev * 10 + n % 10
        # Recursive call with the remaining digits of n
        return is_number_palindrome(n // 10, rev)
    
try:    
    num = int(input("Enter a number to check if it is a palindrome: "))
    reversed_num = is_number_palindrome(num)
    if num == reversed_num:
        print(f"{num} is a palindrome.")
    else:
        print(f"{num} is not a palindrome.")
except ValueError:
    print("Invalid input! Please enter an integer.")
    