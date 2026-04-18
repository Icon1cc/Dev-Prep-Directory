"""
Write a python program to check if a string is a palindrome or not.
"""

def is_palindrome(s):
    low = 0
    high = len(s) - 1
    while low < high:
        if s[low] != s[high]:
            return False
        low += 1
        high -= 1
    return True

try:
    input_string = input("Enter a string: ")
    if is_palindrome(input_string):
        print(f'"{input_string}" is a palindrome.')
    else:
        print(f'"{input_string}" is not a palindrome.')
except Exception as e:
    print(f"An error occurred: {e}")    