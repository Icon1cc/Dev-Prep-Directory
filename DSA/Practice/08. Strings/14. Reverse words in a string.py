"""
Reverse Words in a String
"""

# def reverse_words(s: str) -> str:
#     words = s.split()

#     low = 0
#     high = len(words) - 1
#     while low < high:
#         words[low], words[high] = words[high], words[low]
#         low += 1
#         high -= 1
#     return ' '.join(words)

# First reversing the entire string and then reversing each word individually
def reverse_words(s: str) -> str:
    # Convert to list because Python strings are immutable
    # In C++, this step wouldn't exist (we'd just use the string directly)
    chars = list(s)
    n = len(chars)
    
    # Helper: Reverse a portion of the array [start, end]
    def reverse_section(start, end):
        while start < end:
            chars[start], chars[end] = chars[end], chars[start]
            start += 1
            end -= 1
            
    # 1. Reverse the WHOLE string
    reverse_section(0, n - 1)
    
    # 2. Reverse each word individually
    start = 0
    for end in range(n):
        # If we hit a space, reverse the word we just passed
        if chars[end] == ' ':
            reverse_section(start, end - 1)
            start = end + 1
            
    # Reverse the last word (since there is no space after it)
    reverse_section(start, n - 1)
    
    return "".join(chars)

try:
    user_input = input("Enter a string: ")
    result = reverse_words(user_input)
    print(f"Reversed words: {result}")
except Exception as e:
    print(f"An error occurred: {e}")