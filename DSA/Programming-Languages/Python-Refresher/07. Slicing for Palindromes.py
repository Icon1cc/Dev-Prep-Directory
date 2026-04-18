"""
Description: Write a function is_palindrome_slicing(s) that takes a string s and returns True if the string is a palindrome, and False otherwise. A palindrome is a word that reads the same forwards and backwards. Your implementation must use string slicing to perform the reversal and comparison.
Example 1:
Input: s = "racecar"
Output: True
Example 2:
Input: s = "python"
Output: False
"""

def is_palindrome_slicing(s):
    return s == s[::-1]

s = input("Enter the string: ").lower()
print(is_palindrome_slicing(s))
