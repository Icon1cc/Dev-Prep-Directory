"""
Check if two strings are anagrams of each other.
"""

def are_anagrams(str1, str2):
    # 1. Length Check
    if len(str1) != len(str2):
        return False
    
    # 2. Build Frequency Map
    count = {}
    for char in str1:
        count[char] = count.get(char, 0) + 1
        
    # 3. Decrement and Check
    for char in str2:
        # If char doesn't exist OR we have used up all instances of it
        if char not in count or count[char] == 0:
            return False
        count[char] -= 1
        
    # 4. Success
    # If we survive the loop and lengths are equal, it MUST be an anagram.
    return True

try:
    string1 = input("Enter the first string: ")
    string2 = input("Enter the second string: ")
    if are_anagrams(string1, string2):
        print(f'"{string1}" and "{string2}" are anagrams.')
    else:
        print(f'"{string1}" and "{string2}" are not anagrams.')
except Exception as e:
    print(f"An error occurred: {e}")