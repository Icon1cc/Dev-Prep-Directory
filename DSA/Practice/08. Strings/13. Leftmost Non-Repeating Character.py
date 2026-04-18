"""
Find the leftmost non-repeating character in a given string.
"""

def leftmost_non_repeating_character(s: str) -> str:
    count = [0] * 256

    for char in s:
        count[ord(char)] += 1
    for i in range(len(s)):
        if count[ord(s[i])] == 1:
            return s[i]
    return None
try:
    user_input = input("Enter a string: ")
    result = leftmost_non_repeating_character(user_input)
    print(f"Leftmost non-repeating character: {result}")
except Exception as e:
    print(f"An error occurred: {e}")