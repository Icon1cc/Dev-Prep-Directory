"""
Write a Python program to reverse a given string.
"""

def reverse_string(s):
    result = ""
    for char in s:
        result = char + result
    return result

# Indexing

"""
    def reverse_string(s):
        return s[::-1]
"""

try:
    input_str = input("Enter a string to reverse: ")
    reversed_str = reverse_string(input_str)
    print(f"Reversed String: '{reversed_str}'")
except Exception as e:
    print(f"An error occurred: {e}")