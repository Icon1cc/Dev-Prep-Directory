"""
Write a recursive function to check if a given string is a palindrome.
"""

def is_palindrome(s, start, end):
    if  start >= end:
        return True
    if s[start] != s[end]:
        return False
    return is_palindrome(s, start + 1, end - 1)
try:    
    S = input("Enter a string to check if it is a palindrome: ")
    result = is_palindrome(S)
    if result:
        print(f'"{S}" is a palindrome.')
    else:
        print(f'"{S}" is not a palindrome.')
except Exception as e:
    print("An error occurred:", e)