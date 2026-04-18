"""
Find the leftmost repeating character in a given string.
"""

# def leftmost_repeating_character(s: str) -> str:
#     char_index = {}
#     leftmost_index = len(s)

#     for index, char in enumerate(s):
#         if char in char_index:
#             leftmost_index = min(leftmost_index, char_index[char])
#         else:
#             char_index[char] = index

#     return s[leftmost_index] if leftmost_index != len(s) else None


def leftmost_repeating_character(s: str) -> str:
    count = [0] * 256

    for char in s:
        count[ord(char)] += 1
    for i in range(len(s)):
        if count[ord(s[i])] > 1:
            return s[i]
    return None

try:
    user_input = input("Enter a string: ")
    result = leftmost_repeating_character(user_input)
    print(f"Leftmost repeating character: {result}")
except Exception as e:
    print(f"An error occurred: {e}")

